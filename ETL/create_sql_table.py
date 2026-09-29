import struct

import pyodbc
from azure.identity import DefaultAzureCredential


# Azure SQL details
server = "iot-sql-server-kr3.database.windows.net"
database = "iot_data_db"


# Get Azure access token
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


# ODBC connection string
connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)


# Access-token attribute
SQL_COPT_SS_ACCESS_TOKEN = 1256


# Connect to Azure SQL
connection = pyodbc.connect(
    connection_string,
    attrs_before={
        SQL_COPT_SS_ACCESS_TOKEN: token_struct
    }
)


print("Connected to Azure SQL successfully!")


# Create cursor
cursor = connection.cursor()


# SQL table creation
create_table_query = """
IF NOT EXISTS (
    SELECT *
    FROM sys.tables
    WHERE name = 'iot_sensor_data'
)
BEGIN
    CREATE TABLE iot_sensor_data (
        soil_moisture FLOAT,
        temperature FLOAT,
        air_humidity FLOAT,
        pump_data INT
    )
END
"""


# Execute table creation
cursor.execute(create_table_query)

connection.commit()


print("Table 'iot_sensor_data' created successfully!")


# Close connection
cursor.close()
connection.close()

print("SQL connection closed.")