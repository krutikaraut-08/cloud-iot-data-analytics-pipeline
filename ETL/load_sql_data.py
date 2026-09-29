import struct

import pandas as pd
import pyodbc
from azure.identity import DefaultAzureCredential


# --------------------------------------------------
# 1. Load processed CSV
# --------------------------------------------------

file_path = r"data\Processed Data\processed_iot_data.csv"

df = pd.read_csv(file_path)

print("Processed dataset loaded successfully!")
print("Number of records:", len(df))


# --------------------------------------------------
# 2. Azure SQL details
# --------------------------------------------------

server = "iot-sql-server-kr3.database.windows.net"
database = "iot_data_db"


# --------------------------------------------------
# 3. Get Azure access token
# --------------------------------------------------

credential = DefaultAzureCredential()

token = credential.get_token(
    "https://database.windows.net/.default"
)


# Convert token for ODBC
token_bytes = token.token.encode("utf-16-le")

token_struct = struct.pack(
    f"<I{len(token_bytes)}s",
    len(token_bytes),
    token_bytes
)


# --------------------------------------------------
# 4. SQL connection
# --------------------------------------------------

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)


SQL_COPT_SS_ACCESS_TOKEN = 1256


connection = pyodbc.connect(
    connection_string,
    attrs_before={
        SQL_COPT_SS_ACCESS_TOKEN: token_struct
    }
)

print("Connected to Azure SQL successfully!")


# --------------------------------------------------
# 5. Insert data
# --------------------------------------------------

cursor = connection.cursor()

insert_query = """
INSERT INTO iot_sensor_data (
    soil_moisture,
    temperature,
    air_humidity,
    pump_data
)
VALUES (?, ?, ?, ?)
"""


records = list(
    df[
        [
            "soil_moisture",
            "temperature",
            "air_humidity",
            "pump_data"
        ]
    ].itertuples(index=False, name=None)
)


cursor.fast_executemany = True

cursor.executemany(
    insert_query,
    records
)

connection.commit()


print("Data inserted successfully!")
print("Records inserted:", len(records))


# --------------------------------------------------
# 6. Close connection
# --------------------------------------------------

cursor.close()
connection.close()

print("SQL connection closed.")