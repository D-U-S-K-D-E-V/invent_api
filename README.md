# Invent API
This tool is a python console application that generates a MySQL Restful API based on data entered into the console.

## Basic Setup
To get started, make sure the interpreter for Python is pointed to the virtual envirnment included in the project. Once that is done, open a terminal and type "main.py". From there, the terminal will ask for a mysql host, mysql account username, mysql account password, directory to built the api at (you can copy to another location later if need be), and a port number. The final step is to run "pip install mysql-connector-python" in a terminal within VS code witht he generated API folder open. To run the new API, type "python server.py"

*Note: This setup assumes you're using VS code as your editor.

### Usage
To use the API, you'll want to use the following convention in your URLs. 

Template SELECT:
    localhost:0000/key=00000000-0000-0000-0000-000000000000/query=get_all_in_table_match/filter=*filter_value* (if match of search query)

Template INSERT:
    localhost:0000/key=00000000-0000-0000-0000-000000000000/query=insert_article
    
    body={
        [
            *value*,
            *value*,
            *value*
        ]
    }

Example UPDATE:
    localhost:0000/key=00000000-0000-0000-0000-000000000000/query=update_table_by_column_search_by_column
    
    body={
        value: *value*
        filter: *filter_value*
    }
