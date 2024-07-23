import os
import streamlit as st
import psycopg2
import pandas as pd

class DatabaseHandler:

    def __init__(self):
        """
        Establishes a connection to the PostgreSQL database using the provided URI
        """
        try:            
            self.connection = psycopg2.connect(os.environ.get('POSTGRESQL_AI_URI'))  # Connect to the database
            self.cursor = self.connection.cursor()  # Initialize a cursor
        except Exception as e:
            st.error(f"Failed to connect to the database: {e}")
            raise

    def execute_sql(self, solution):
        try:
            _,final_query,_ = solution.split("```")
            final_query = final_query.strip('sql')
            self.cursor.execute(final_query)
            result = self.cursor.fetchall()
            return str(result)
        except Exception as e:
            st.error(f"Failed to save database details: {e}")
            raise
        finally:
            self.cursor.close()
            self.connection.close()

    def get_basic_table_details(self):
        """ run once in global_initialization
        Fetches basic details (table names, column names, and data types) of tables in the 'public' schema.

        Returns:
            list: A list of tuples containing table details.
        """

        query = """
        SELECT
            c.table_name,
            c.column_name,
            c.data_type
        FROM
            information_schema.columns c
        WHERE
            c.table_name IN (
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
        );
        """
        self.cursor.execute(query)
        tables_and_columns = self.cursor.fetchall()
        return tables_and_columns

    def get_db_schema(self):
        try:
            tables_and_columns = self.get_basic_table_details()  # Fetch table details
            df = pd.DataFrame(tables_and_columns, columns=['table_name', 'column_name', 'data_type'])
            csv_path = os.getenv('CSV_PATH')
            if not os.path.exists(csv_path):
                df.to_csv(csv_path, index=False)  # Save details to CSV file
            table_info = ''
            for table in df['table_name']:
                table_info += f'Information about table {table}:\n'
                table_info += df[df['table_name'] == table].to_string(index=False) + '\n\n\n'
            return table_info
        except Exception as e:
            st.error(f"Failed to save database details: {e}")
            raise
        finally:
            self.cursor.close()
            self.connection.close()
