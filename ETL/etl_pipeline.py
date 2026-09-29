import pandas as pd

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient

file_path = r"data\Raw Data\Soil Moisture, Air Temperature and humidity, and Water Motor onoff Monitor data.AmritpalKaur.csv"

df = pd.read_csv(file_path)
print("Dataset loaded successfully!")

print("\nShape of dataset:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())
# Standardize column names

df.columns = [
    "soil_moisture",
    "temperature",
    "air_humidity",
    "pump_data"
]

print("\nUpdated column names:")
print(df.columns. tolist())
# Check for missing values

missing_values = df.isnull().sum()

print("\nMissing values:")
print(missing_values)
# Check for duplicate rows

duplicate_rows = df.duplicated().sum()

print("\nDuplicate rows:")
print(duplicate_rows)
# Check data types

print("\nData types:")
print(df.dtypes)
# Check basic statistics

print("\nBasic statistics:")
print(df.describe())
# Validate sensor value ranges

invalid_temperature = df[
    (df["temperature"] < 18) |
    (df["temperature"] > 39)
]

invalid_humidity = df[
    (df["air_humidity"] < 38) |
    (df["air_humidity"] > 82)
]

invalid_soil_moisture = df[
    (df["soil_moisture"] < 314) |
    (df["soil_moisture"] > 985)
]

invalid_pump_data = df[
    ~df["pump_data"].isin([0, 1])
]

print("\nInvalid temperature records:", len(invalid_temperature))
print("Invalid humidity records:", len(invalid_humidity))
print("Invalid soil moisture records:", len(invalid_soil_moisture))
print("Invalid pump status records:", len(invalid_pump_data))
# Create processed dataset

processed_df = df.copy()

# Save the processed dataset
output_path = r"data\Processed Data\processed_iot_data.csv"

processed_df.to_csv(output_path, index=False)

print("\nProcessed dataset saved successfully!")
print("File:", output_path)
# Connect to Azure Blob Storage

credential = DefaultAzureCredential()

account_url = "https://iotdatapipelinekr.blob.core.windows.net"

blob_service_client = BlobServiceClient(
    account_url=account_url,
    credential=credential
)

print("\nConnected to Azure Blob Storage!")
# Upload processed dataset to Azure Blob Storage

container_name = "processed-data"
blob_name = "processed_iot_data.csv"

blob_client = blob_service_client.get_blob_client(
    container=container_name,
    blob=blob_name
)

with open(output_path, "rb") as data:
    blob_client.upload_blob(
        data,
        overwrite=True
    )

print("\nProcessed dataset uploaded successfully!")
print("Azure container:", container_name)
print("Blob:", blob_name)