import os
import re
import gzip
import shutil
import requests

def download_pageviews(datasource_url, downloads_folder):
    # Create downloads folder if it doesn't exist
    os.makedirs(downloads_folder, exist_ok=True)

    filename = re.split(pattern='/', string=datasource_url)[-1]
    gzipped_file = os.path.join(downloads_folder, filename)
    csv_file = os.path.join(downloads_folder, re.split(pattern=r'\.', string=filename)[0] + ".csv")
    
    # Download gzipped file
    response = requests.get(datasource_url, stream=True)
    with open(gzipped_file, 'wb') as f:
        f.write(response.content)
    
    # Unzip gzipped file
    with gzip.open(gzipped_file, 'rb') as f_in:
        with open(csv_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    return csv_file

def fetch_page(csv_file, output_sql_file):
    search_values = ['Facebook', 'Google', 'Apple', 'Amazon', 'Microsoft']
    count = 0  # Initialize count to 0
    # Open the extracted CSV file
    with open(csv_file) as f:
        for line in f:
            for search_value in search_values:
                if line.startswith(f'en.m {search_value} '):
                    my_val = line.split(' ')[-2]
                    count += 1
                    # Create SQL query
                    query = f"INSERT INTO sentiments (id, company, views) VALUES ({count}, '{search_value}', '{my_val}');\n"
                    with open(output_sql_file, 'a') as query_file:
                        query_file.write(query)
