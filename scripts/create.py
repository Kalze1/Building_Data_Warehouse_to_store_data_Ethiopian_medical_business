import json
import psycopg2

# Replace with your JSON file path and database connection details
json_file = '../data/ChatExport_2024-10-10/result.json'
conn_string = "host='localhost' dbname='postgres' user='postgres' password='fykbz1and5'"

def create_database_from_json(json_file, conn_string):
    with open(json_file, 'r') as f:
        data = json.load(f)

    with psycopg2.connect(conn_string) as conn:
        cursor = conn.cursor()

        # Create tables based on the JSON data
        for table_name, table_data in data.items():
            columns = [f"{column_name} {data_type}" for column_name, data_type in table_data['columns'].items()]
            create_table_sql = f"CREATE TABLE {table_name} ({', '.join(columns)})"
            cursor.execute(create_table_sql)

            # Insert data into the tables
            for row in table_data['data']:
                insert_values = [f"'{value}'" for value in row.values()]
                insert_sql = f"INSERT INTO {table_name} VALUES ({', '.join(insert_values)})"
                cursor.execute(insert_sql)

        conn.commit()

create_database_from_json(json_file, conn_string)