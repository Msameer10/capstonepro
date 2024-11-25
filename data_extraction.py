        # Highlights of this code
        # 1. Data Extraction: Reads raw data from a CSV file using Python’s pandas library.
        # 2. Data Transformation: Cleans and preprocesses the data (e.g., handling missing values, normalizing columns).
        # 3. Data Loading: Connects to a MySQL database using the sqlalchemy library and loads the cleaned data into a target table.
        # 4. Error Logging: Includes basic error-handling mechanisms to log issues during the ETL process.

# pandas: For data manipulation.
# sqlalchemy: For database connection and operations.
# pymysql: For MySQL support in SQLAlchemy.

import pandas as pd
from sqlalchemy import create_engine

# ------------------------------------------------------------ Step 1: Extract Data
def extract_data(file_path):
    try:
        print("Extracting data from:", file_path)
        return pd.read_csv(file_path)                                          # read data from csv file
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None

# ------------------------------------------------------------ Step 2: Transform Data
def transform_data(data):
    try:
        print("Transforming data...")
        # Drop rows with missing values
        data = data.dropna()
        
        # Standardize column names
        data.columns = [col.strip().lower().replace(' ', '_') for col in data.columns]
        
        # Convert date column to a standard format
        if 'matchday_date' in data.columns:
            data['matchday_date'] = pd.to_datetime(data['matchday_date'])
        
        # Normalize player names
        if 'player_name' in data.columns:
            data['player_name'] = data['player_name'].str.title()
        
        return data
    except Exception as e:
        print(f"Error transforming data: {e}")
        return None

# ----------------------------------------------------------- Step 3: Load Data to Database
def load_data_to_db(data, db_connection, table_name):
    try:
        print("Loading data to database...")
        engine = create_engine(db_connection)
        data.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"Data successfully loaded into table: {table_name}")
    except Exception as e:
        print(f"Error loading data: {e}")

# Main ETL Workflow
if __name__ == "__main__":
    file_path = "<csv_file>"                                                        # input file
    db_connection = "<db_connection_link>"                                          # database connection (MySQL)
    target_table = "matchday_data"

    # Extract
    raw_data = extract_data(file_path)
    if raw_data is not None:
        # Transform
        cleaned_data = transform_data(raw_data)
        if cleaned_data is not None:
            # Load
            load_data_to_db(cleaned_data, db_connection, target_table)
