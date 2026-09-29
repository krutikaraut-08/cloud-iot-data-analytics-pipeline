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


# Convert the token into the format required by ODBC
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


# Access-token attribute used by Microsoft ODBC Driver
SQL_COPT_SS_ACCESS_TOKEN = 1256


# Connect to Azure SQL
connection = pyodbc.connect(
    connection_string,
    attrs_before={
        SQL_COPT_SS_ACCESS_TOKEN: token_struct
    }
)


print("Azure SQL connection successful!")


# Test the database connection
cursor = connection.cursor()

cursor.execute("SELECT DB_NAME()")

database_name = cursor.fetchone()[0]

print("Connected database:", database_name)


cursor.close()
connection.close()

print("Connection closed successfully.")