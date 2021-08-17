import mysql.connector as conn

class DB_Conn:

    def __init__(self, mysql_creds):
        self.appdb = conn.connect(
            host = mysql_creds['host_value'],
            user = mysql_creds['user_value'],
            password = mysql_creds['password_value'],
            database = mysql_creds['database_value']
        )
        self.creds = mysql_creds
        self.schema_query = "SELECT information_schema.tables.table_name FROM information_schema.tables WHERE information_schema.tables.table_schema = '$SCHEMA_NAME$'"
        self.column_query = "SELECT information_schema.columns.COLUMN_NAME, information_schema.columns.DATA_TYPE FROM information_schema.columns WHERE information_schema.columns.TABLE_SCHEMA = '$SCHEMA_NAME$' AND information_schema.columns.TABLE_NAME = '$TABLE_NAME$'"
    
    def get_metadata(self):
        
        metadata = {}
        tables = self.schema_query.replace('$SCHEMA_NAME$', self.creds['database_value'])
        
        cursor = self.appdb.cursor()
        cursor.execute(tables)
        columns = cursor.column_names
        rows = cursor.fetchall()
        schema_data = self.data_prep(columns, rows)
        
        for n in schema_data:
            column_query = self.column_query.replace('$SCHEMA_NAME$', self.creds['database_value']).replace('$TABLE_NAME$', schema_data[n]['TABLE_NAME'])
            cursor.execute(column_query)
            c = cursor.column_names
            r = cursor.fetchall()
            column_data = self.data_prep(c, r)
            metadata[schema_data[n]['TABLE_NAME']] = []

            for m in column_data:
                metadata[schema_data[n]['TABLE_NAME']].append([column_data[m]['COLUMN_NAME'], column_data[m]['DATA_TYPE']])

        return metadata

    def data_prep(self, columns, rows):
        response = {}
        x = 0
        for item in rows:
            row_data = {}
            for c_name, c_data in zip(columns, item):
                row_data[str(c_name)] = str(c_data)
            response[str(x)] = row_data
            x = x + 1
        return response