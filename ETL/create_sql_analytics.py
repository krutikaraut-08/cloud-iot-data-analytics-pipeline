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


# --------------------------------------------------
# 4. Create analytical view
# --------------------------------------------------

cursor = connection.cursor()


create_view_query = """
CREATE OR ALTER VIEW vw_iot_sensor_summary
AS
SELECT
    COUNT(*) AS total_records,

    AVG(soil_moisture) AS average_soil_moisture,

    AVG(temperature) AS average_temperature,

    AVG(air_humidity) AS average_air_humidity,

    SUM(CASE
        WHEN pump_data = 1 THEN 1
        ELSE 0
    END) AS pump_on_records,

    SUM(CASE
        WHEN pump_data = 0 THEN 1
        ELSE 0
    END) AS pump_off_records,

    CAST(
        100.0 *
        SUM(CASE
            WHEN pump_data = 1 THEN 1
            ELSE 0
        END)
        / COUNT(*)
        AS DECIMAL(5,2)
    ) AS pump_on_percentage

FROM iot_sensor_data;
"""


cursor.execute(create_view_query)

connection.commit()


print("Analytical view created successfully!")


# --------------------------------------------------
# 5. Test the analytical view
# --------------------------------------------------

cursor.execute("""
    SELECT *
    FROM vw_iot_sensor_summary
""")


result = cursor.fetchone()


print("\nIoT Sensor Summary:")
print("Total records:", result[0])
print("Average soil moisture:", result[1])
print("Average temperature:", result[2])
print("Average air humidity:", result[3])
print("Pump ON records:", result[4])
print("Pump OFF records:", result[5])
print("Pump ON percentage:", result[6])


# --------------------------------------------------
# 6. Close connection
# --------------------------------------------------

cursor.close()
connection.close()

print("\nSQL connection closed.")