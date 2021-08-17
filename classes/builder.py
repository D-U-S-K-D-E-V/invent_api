import os
import subprocess

class APIBuilder:

    def __init__(self, api_config, schema):
        self.api_schema = schema
        self.builder_config = api_config
        self.temp_dir = './templates'
        self.target_dir = str(api_config['target_dir']) + '/' + str(api_config['database_value']) + '-api'
        self.pip_dir = str(api_config['target_dir']) + '/' + str(api_config['database_value']) + '-api' + '/' + str(api_config['database_value']) + '-api' + '/Scripts'
        self.port_num = api_config['port_num']
        self.key_value = api_config['api_key']
        self.project_name = str(api_config['database_value'] + '_api')

    def create_tree(self):
        api_dir = [
            self.target_dir,
            self.target_dir + '/.vscode',
            self.target_dir + '/database',
            self.target_dir + '/database/credentials',
            self.target_dir + '/database/classes',
            self.target_dir + '/database/queries',
            self.target_dir + '/routes'
        ]
        
        init_file = '/__init__.py'

        for n in api_dir:
            os.mkdir(n)

        for m in api_dir:
            if m.endswith('-api') == False and m.endswith('.vscode') == False:
                create_file = open(m + init_file, 'x')
                create_file.close()
        
        settings_file = open(self.temp_dir + '/settings/settings.json', 'r')
        new_settings_file = open(self.target_dir + '/.vscode/settings.json', 'x')
        line_data = settings_file.readlines()

        for line in line_data:
            new_settings_file.write(line.replace('$PROJECT_NAME$', self.project_name))

    def add_server(self):
        server_code = open(self.temp_dir + '/server.txt', 'r')
        read_code = server_code.readlines()
        file_content = []

        for n in read_code:
            file_content.append(n.replace('$PORT_NUMBER$', str(self.port_num)))

        new_server_code = open(self.target_dir + '/server.py', 'x')

        for m in file_content:
            new_server_code.write(m)

        server_code.close()
        new_server_code.close()

    def add_envir(self):
        venv_command = ['python', '-m', 'venv', self.project_name]
        package_command = ' '.join([self.target_dir, 'pip install', 'mysql-connector-python'])
        try:
            subprocess.check_call(
                venv_command, cwd=self.target_dir
            )
            print("Envirnment Created Successfully!")
        except subprocess.CalledProcessError as error_message:
            print("An error has occured: \n" + str(error_message))
            
        try:
            subprocess.check_call(
                package_command,
                shell=True
            )
        except subprocess.CalledProcessError as error_message:
            print("An error has occured: \n" + str(error_message))



    def add_router(self):
        router_file = open(self.temp_dir + '/routes/req_router.txt', 'r')
        new_router_file = open(self.target_dir + '/routes/req_router.py', 'x')
        line_data = router_file.readlines()

        for line in line_data:
            new_router_file.write(line.replace('$API_KEY$', str(self.key_value)))

        router_file.close()
        new_router_file.close()

    def add_sql_classes(self):
        template_conn = open(self.temp_dir + '/database/db_conn.txt', 'r')
        built_conn = open(self.target_dir + '/database/classes/db_conn.py', 'x')
        line_data = template_conn.readlines()
        
        for line in line_data:
            built_conn.write(line
                .replace('$HOST_NAME$', "'" + self.builder_config['host_value'] + "'")
                .replace('$USER_NAME$', "'" + self.builder_config['user_value'] + "'")
                .replace('$PASSWORD$', "'" + self.builder_config['password_value'] + "'")
                .replace('$DATABASE_NAME$', "'" + self.builder_config['database_value'] + "'")
            )
        template_conn.close()
        built_conn.close()

    def add_selects(self):
        schema = self.api_schema
        x = 1
        qt = {
            'get_all_in_table': "SELECT * FROM $TABLE_NAME$",
            'get_all_in_table_match': "SELECT * FROM $TABLE_NAME$ WHERE $TABLE_NAME$.$COLUMN_NAME$ = '$COLUMN_VALUE$'",
            'get_all_in_table_search': "SELECT * FROM $TABLE_NAME$ WHERE $TABLE_NAME$.$COLUMN_NAME$ = '%$COLUMN_VALUE$%'",
            'get_column_in_table': "SELECT $TABLE_NAME$.$COLUMN_NAME$ FROM $TABLE_NAME$",
            'get_column_in_table_match': "SELECT $TABLE_NAME$.$COLUMN_NAME$ FROM $TABLE_NAME$ WHERE $TABLE_NAME$.$COLUMN_NAME$ = '$COLUMN_VALUE$'",
            'get_column_in_table_search': "SELECT $TABLE_NAME$.$COLUMN_NAME$ FROM $TABLE_NAME$ WHERE $TABLE_NAME$.$COLUMN_NAME$ LIKE '%$COLUMN_VALUE$%'"
        }
        qnt = {
            'get_all_in_table': 'get_all_in_$TABLE_NAME$',
            'get_all_in_table_match': 'get_all_in_$TABLE_NAME$_match_$COLUMN_NAME$',
            'get_all_in_table_search': 'get_all_in_$TABLE_NAME$_search_$COLUMN_NAME$',
            'get_column_in_table': 'get_$COLUMN_NAME$_in_$TABLE_NAME$',
            'get_column_in_table_match': 'get_$COLUMN_NAME$_in_$TABLE_NAME$_match_by_$MATCH_COLUMN$',
            'get_column_in_table_search': 'get_$COLUMN_NAME$_in_$TABLE_NAME$_search_by_$SEARCH_COLUMN$'
        }

        queries = {}

        for n in schema:
            queries[qnt['get_all_in_table'].replace('$TABLE_NAME$', n)] = qt['get_all_in_table'].replace('$TABLE_NAME$', n)
    
            for m in schema[n]:
                queries[qnt['get_column_in_table'].replace('$COLUMN_NAME$', m[0]).replace('$TABLE_NAME$', n)] = qt['get_column_in_table'].replace('$COLUMN_NAME$', m[0]).replace('$TABLE_NAME$', n)
                queries[qnt['get_all_in_table_match'].replace('$COLUMN_NAME$', m[0]).replace('$TABLE_NAME$', n)] = qt['get_all_in_table_match'].replace('$COLUMN_NAME$', m[0]).replace('$TABLE_NAME$', n)
                
                if m[1] == 'varchar':
                    queries[qnt['get_all_in_table_search'].replace('$COLUMN_NAME$', m[0]).replace('$TABLE_NAME$', n)] = qt['get_all_in_table_search'].replace('$COLUMN_NAME$', m[0]).replace('$TABLE_NAME$', n)
      
                for o in schema[n]:
                    queries[qnt['get_column_in_table_match'].replace('$TABLE_NAME$', n).replace('$COLUMN_NAME$', n).replace('$MATCH_COLUMN$', o[0])] = qt['get_column_in_table_match'].replace('$TABLE_NAME$', n).replace('$COLUMN_NAME$', n).replace('$MATCH_COLUMN$', o[0])
                    queries[qnt['get_column_in_table_search'].replace('$TABLE_NAME$', n).replace('$COLUMN_NAME$', n).replace('$SEARCH_COLUMN$', o[0])] = qt['get_column_in_table_search'].replace('$TABLE_NAME$', n).replace('$COLUMN_NAME$', n).replace('$SEARCH_COLUMN$', o[0])
                
        query_template = open(self.target_dir + '/database/queries/query_storage.py', 'x')
        query_template.write('def get_selects():')
        query_template.write('\n\tselect_list = {')
        
        for q in queries:
            if x == len(queries):
                query_template.write('\n\t\t' + '"' + q + '"' + ':' + '"' + str(queries[q]) + '"')
            else:
                x = x+1
                query_template.write('\n\t\t' + '"' + q + '"' + ':' + '"' + str(queries[q]) + '",')

        query_template.write('\n\t}')
        query_template.write('\n\treturn select_list')
        query_template.close()

    def add_inserts(self):
        schema = self.api_schema
        x = 1
        y = 1
        insert_temp_name = 'insert_$TABLE_NAME$'
        insert_temp_code = 'INSERT INTO $TABLE_NAME$($COLUMNS$) VALUES($VALUES$)'
        insert_statements = {}
        query_template = open(self.target_dir + '/database/queries/query_storage.py', 'a')
        
        query_template.write('\n\ndef get_inserts():')
        query_template.write('\n\tinsert_list = {')

        for table in schema:
            column_string = ''
            
            for columns in schema[table]:
                if y == len(schema[table]):
                    column_string += str(columns[0])
                else:
                    y = y + 1
                    column_string += str(columns[0]) + ', '

            insert_statements[insert_temp_name.replace('$TABLE_NAME$', table)] = insert_temp_code.replace('$TABLE_NAME$', table).replace('$COLUMNS$', column_string)

        for statement in insert_statements:
            if x == len(insert_statements):
                query_template.write('\n\t\t' + '"' + statement + '"' + ':' + '"' + str(insert_statements[statement]) + '"')
            else:
                x = x+1
                query_template.write('\n\t\t' + '"' + statement + '"' + ':' + '"' + str(insert_statements[statement]) + '",')

        query_template.write('\n\t}')
        query_template.write('\n\treturn insert_list')
        query_template.close()

    def add_updates(self):
        schema = self.api_schema
        x = 1
        update_temp_name_match = 'update_$TABLE_NAME$_by_$COLUMN_NAME$_match_by_$FILTER_COLUMN$'
        update_temp_name_search = 'update_$TABLE_NAME$_by_$COLUMN_NAME$_search_by_$FILTER_COLUMN$'
        update_temp_code_match = "UPDATE $TABLE_NAME$ SET $UPDATE_COLUMN$ = $UPDATE_VALUE$ WHERE $FILTER_COLUMN$ = '$FILTER_VALUE$'"
        update_temp_code_search = "UPDATE $TABLE_NAME$ SET $UPDATE_COLUMN$ = $UPDATE_VALUE$ WHERE $FILTER_COLUMN$ LIKE '%$FILTER_VALUE$%'"
        update_statements = {}
        query_template = open(self.target_dir + '/database/queries/query_storage.py', 'a')

        query_template.write('\n\ndef get_updates():')
        query_template.write('\n\tupdate_list = {')

        for table in schema:
            for column in schema[table]:
                for filter_column in schema[table]:
                    if filter_column[1] == 'varchar':
                        update_statements[update_temp_name_search.replace('$TABLE_NAME$', table).replace('$COLUMN_NAME$', column[0]).replace('$FILTER_COLUMN$', filter_column[0])] = update_temp_code_search.replace('$TABLE_NAME$', table).replace('$UPDATE_COLUMN$', column[0]).replace('$FILTER_COLUMN$', filter_column[0])
                        update_statements[update_temp_name_match.replace('$TABLE_NAME$', table).replace('$COLUMN_NAME$', column[0]).replace('$FILTER_COLUMN$', filter_column[0])] = update_temp_code_match.replace('$TABLE_NAME$', table).replace('$UPDATE_COLUMN$', column[0]).replace('$FILTER_COLUMN$', filter_column[0])
                    else:
                        update_statements[update_temp_name_match.replace('$TABLE_NAME$', table).replace('$COLUMN_NAME$', column[0]).replace('$FILTER_COLUMN$', filter_column[0])] = update_temp_code_match.replace('$TABLE_NAME$', table).replace('$UPDATE_COLUMN$', column[0]).replace('$FILTER_COLUMN$', filter_column[0])

        for statement in update_statements:
            if x == len(update_statements):
                query_template.write('\n\t\t' + '"' + statement + '"' + ':' + '"' + str(update_statements[statement]) + '"')
            else:
                x = x+1
                query_template.write('\n\t\t' + '"' + statement + '"' + ':' + '"' + str(update_statements[statement]) + '",')

        query_template.write('\n\t}')
        query_template.write('\n\treturn update_list')
        query_template.close()

