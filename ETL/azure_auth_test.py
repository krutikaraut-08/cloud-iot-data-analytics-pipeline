from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


# Authenticate using the Azure CLI login
credential = DefaultAzureCredential()


# Azure Storage account URL
account_url = "https://iotdatapipelinekr.blob.core.windows.net"


# Create a Blob Storage client
blob_service_client = BlobServiceClient(
    account_url=account_url,
    credential=credential
)


# List the containers in the storage account
print("Containers in storage account:")

for container in blob_service_client.list_containers():
    print("-", container.name)