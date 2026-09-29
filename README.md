\# Cloud-Based IoT Data Processing \& Analytics Pipeline



A cloud-based IoT data processing and analytics pipeline that ingests environmental sensor data into Azure Blob Storage, processes and validates it using Python and Pandas, loads the processed data into Azure SQL, and presents analytical insights through Power BI.



\## Architecture



Public IoT Dataset

&#x20;       ↓

Azure Blob Storage — Raw Data

&#x20;       ↓

Python + Pandas ETL

&#x20;       ↓

Azure Blob Storage — Processed Data

&#x20;       ↓

Azure SQL Database

&#x20;       ↓

SQL Analytical View

&#x20;       ↓

Power BI Dashboard



\## Technologies Used



\- Python

\- Pandas

\- NumPy

\- Microsoft Azure

\- Azure Blob Storage

\- Azure SQL Database

\- SQL

\- Power BI

\- pyodbc



\## Pipeline



\### 1. Data Ingestion



The public IoT dataset is uploaded to Azure Blob Storage in the `raw-data` container.



\### 2. Data Processing



Python and Pandas are used to:



\- Standardize column names

\- Validate data types

\- Check missing values

\- Check duplicate records

\- Validate numerical ranges

\- Generate a processed dataset



\### 3. Processed Data Storage



The validated dataset is uploaded to the `processed-data` container in Azure Blob Storage.



\### 4. Azure SQL Database



The processed data is loaded into the `iot\_sensor\_data` table in Azure SQL Database.



An analytical SQL view, `vw\_iot\_sensor\_summary`, provides summary metrics including:



\- Total records

\- Average soil moisture

\- Average temperature

\- Average air humidity

\- Pump ON records

\- Pump OFF records

\- Pump ON percentage



\### 5. Power BI



Power BI connects to Azure SQL to visualize the processed IoT data through KPI cards and analytical charts.



\## Dataset



The project uses a public smart-irrigation IoT dataset containing:



\- Soil moisture

\- Air temperature

\- Air humidity

\- Water motor ON/OFF status



The dataset contains 3,000 records.



\## Project Structure



```text

data engg pipeline project/

│

├── data/

│   ├── Raw Data/

│   └── Processed Data/

│

├── ETL/

│   ├── etl\_pipeline.py

│   ├── azure\_auth\_test.py

│   ├── sql\_connection\_test.py

│   ├── create\_sql\_table.py

│   ├── load\_sql\_data.py

│   ├── verify\_sql\_data.py

│   └── create\_sql\_analytics.py

│

├── .gitignore

├── requirements.txt

├── README.md

└── Cloud\_IoT\_Data\_Analytics\_Dashboard.pbix

