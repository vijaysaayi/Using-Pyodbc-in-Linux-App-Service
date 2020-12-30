import pyodbc
import os
from flask import Flask, render_template
app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/GetFirstDocument/TableName/<tableName>')
def GetFirstDocument(tableName):
    connectionString = os.environ['SQLCONNSTR_DemoDb']
    connection = pyodbc.connect(connectionString)
    cursor = connection.cursor()

    cursor.execute(f"SELECT TOP 1 * FROM {tableName} ")
    row = cursor.fetchone()
    if(row):
        return f"First cell value is : {row[0]}"
    else:
        return "Issue connecting to SQL server"

@app.route('/',methods=["GET","POST"])
def index():
    return "Welcome to Azure App Services"
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
