## CDE CoreSentiment Project: Wikipedia Pageview Sentiment Analysis

### Project Overview:
The objective of this project is to build a Stock Market Prediction Tool called CoreSentiment, which applies sentiment analysis based on Wikipedia pageviews for 4pm on 10th of October, 2024 for five companies (Amazon, Apple, Facebook, Google, and Microsoft). 
CoreSentiment assumes that an increase in a company's Wikipedia pageviews suggests a positive sentiment, indicating that the company's stock price is likely to increase. Conversely, a decrease in pageviews suggests negative sentiment, predicting a potential decrease in stock price.

### Project Data Source:
<p>[Wikimedia Pageviews Dumps for October 2024](https://dumps.wikimedia.org/other/pageviews)</p>
Detailed information about the structure of the pageviews data is available [here](https://dumps.wikimedia.org/other/pageviews/).

### Project Structure:
Airflow was installed using PyPi rather in place of Docker image due to resources required by Docker image
**Data Download**: The pipeline fetches compressed pageview data files from Wikimedia's official dumps, specifically for one-hour periods on a specified date.
**Data Extraction**: The downloaded .gz file is decompressed and converted into a CSV file.
**Data Filtering**: The CSV file is processed to extract pageview counts for the specified companies (Amazon, Apple, Facebook, Google, and Microsoft).
**Data Storage**: The processed data is transformed into SQL INSERT statements and written into a file, which is later executed to insert the records into a PostgreSQL database.

### Key Components
1. Airflow DAG (sentiment-analysis/sentiment.py)
The DAG is defined in this file, orchestrating the tasks of downloading, extracting, and processing the Wikipedia pageview data.

2. Python Functions (scripts/python/download_file.py)
Python functions are organized separately for modularity:
download_pageviews and fetch_page: Downloads the .gz file from Wikimedia's official dumps and extracts.
fetch_page: Generates SQL INSERT statements for the filtered data and inserts it into the PostgreSQL database.

4. SQL Scripts (scripts/sql/create_table.sql, scripts/sql/insert_data.sql) 
create_table.sql: This file contains the SQL schema definition for the sentiments table in PostgreSQL, where the extracted pageview data is stored.
insert_data.sql: This file contains the SQL insert statements.

### Design Rationale
Why Airflow?
Automation: Airflow is used to orchestrate ETL workflow.
Modularity: Using Airflow allows us to separate individual tasks (download, extraction, filtering, and database insertion), making the pipeline easier to manage and debug.

Why PostgreSQL?
Structured Data Storage: PostgreSQL is chosen for its robust support of SQL, making it suitable for storing and querying structured pageview data.
Scalability: As data volume increases, PostgreSQL offers scalability, and the table design ensures efficient querying of pageviews for selected companies.

Python Functions and SQL Separation
Maintainability: Keeping the Python processing logic and SQL schema in separate files makes the pipeline easier to manage. Any updates to the logic or schema can be done without affecting the overall flow of the DAG.
Reusability: The Python scripts can be reused or extended to handle other processing tasks, while the SQL scripts can be adapted to different database schema requirements.
