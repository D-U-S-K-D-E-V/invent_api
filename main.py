from classes.db_conn import DB_Conn
from classes.builder import APIBuilder
import uuid

def main():

    print("Enter Host: ")
    host = input()
    print("Enter Username: ")
    user = input()
    print("Enter Password: ")
    password = input()
    print("Enter Database Name: ")
    database = input()
    print("Enter API Server Port Number: ")
    port_number = input()
    print("Enter Target Path (Must Be Full Path, No Spaces)")
    target_path = input()

    api_config = {
        'host_value': host,
        'user_value': user,
        'password_value': password,
        'database_value': database,
        'target_dir': target_path,
        'port_num': port_number,
        'api_key': "'" + str(uuid.uuid4()) + "'"
    }

    mysql = DB_Conn(api_config)
    results = mysql.get_metadata()
    builder = APIBuilder(api_config, results)
    
    builder.create_tree()
    builder.add_server()
    builder.add_selects()
    builder.add_inserts()
    builder.add_updates()
    builder.add_router()
    builder.add_sql_classes()
    builder.add_envir()

main()