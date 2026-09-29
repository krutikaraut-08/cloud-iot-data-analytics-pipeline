import struct

import pyodbc
from azure.identity import DefaultAzureCredential


# --------------------------------------------------
# 1. Azure SQL details
# --------------------------------------------------

server = "iot-sql-server-kr3.database.windows.net"
database = "iot_data_db"


# --------------------------------------------------
# 2. Get Azure access token
# --------------------------------------------------

credential = DefaultAzureCredential()

token = credential.get_token(
    "https://database.windows.net/.default"
)


token_bytes = token.token.encode("utf-16-le")

token_struct = struct.pack(
    f"<I{len(token_bytes)}s",
    len(token_bytes),
    token_bytes
)


# --------------------------------------------------
# 3. SQL connection
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


cursor = connection.cursor()


# --------------------------------------------------
# 4. Count records
# --------------------------------------------------

cursor.execute(
    "SELECT COUNT(*) FROM iot_sensor_data"
)

record_count = cursor.fetchone()[0]

print("\nTotal records:", record_count)


# --------------------------------------------------
# 5. Sensor statistics
# --------------------------------------------------

cursor.execute("""
    SELECT
        MIN(soil_moisture),
        MAX(soil_moisture),
        MIN(temperature),
        MAX(temperature),
        MIN(air_humidity),
        MAX(air_humidity)
    FROM iot_sensor_data
""")

stats = cursor.fetchone()

print("\nSensor ranges:")
print("Soil moisture:", stats[0], "to", stats[1])
print("Temperature:", stats[2], "to", stats[3])
print("Air humidity:", stats[4], "to", stats[5])


# --------------------------------------------------
# 6. Pump status counts
# --------------------------------------------------

cursor.execute("""
    SELECT
        pump_data,
        COUNT(*)
    FROM iot_sensor_data
    GROUP BY pump_data
    ORDER BY pump_data
""")

pump_results = cursor.fetchall()

print("\nPump status counts:")

for status, count in pump_results:
    print("Pump", status, ":", count)


# --------------------------------------------------
# 7. Close connection
# --------------------------------------------------

cursor.close()
connection.close()

print("\nSQL connection closed.")