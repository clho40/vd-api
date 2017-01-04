from flask import Flask,request, jsonify
import sqlite3
app = Flask(__name__)
#SQLite is used as the database due to free hosting environment's restriction.
conn = sqlite3.connect('data.db')
conn.execute('''create table if not exists api_data (ID INTEGER PRIMARY KEY AUTOINCREMENT, DATA_KEY TEXT NOT NULL, DATA_VALUE TEXT, TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP); ''')
c = conn.cursor()

#Root
@app.route('/')
def index():
    return 'Home'

#Insert values. eg: url=http://url/object | body=JSON:{mykey:value1}
@app.route('/object', methods=['POST'])
def post_object():
    try:
        if isDatabaseOverLimit():
            return "Reached limit!"
        else:
            data=request.get_json()
            for key in data.keys():
                insert_object(key,data[key])
            return "Object(s) inserted"
    except:
        return "Error inserting values!"

#Retrieve values. eg: url=http://url/object/mykey or http://url/object/mykey?timestamp=1483539600
@app.route('/object/<key>', methods=['GET'])
def get_object(key):
    try:
        value = ""
        timestamp = request.args.get('timestamp')
        if timestamp is None:
            value = select_object(key)
        else:
            value = select_object_by_time(key,timestamp)
        return value
    except:
        return "Error getting values!"

#Select data value from database
def select_object(key):
    k = (key,)
    c.execute('select DATA_VALUE from api_data where DATA_KEY=? order by timestamp desc',k)
    value = c.fetchone()
    return 'No result!' if value is None else value

#Select data value from database correspond to the timestamp requested
def select_object_by_time(key,timestamp):
    k = (key,int(timestamp))
    c.execute("select DATA_VALUE from api_data where DATA_KEY=? and timestamp <= datetime(?, 'unixepoch') order by timestamp desc",k)
    value = c.fetchone()
    return 'No result!' if value is None else value

#Insert data value.
def insert_object(key,value):
    k = (key,value)
    conn.execute('insert into api_data (DATA_KEY,DATA_VALUE) values (?,?)',k)
    conn.commit()

#Set to maximum 1000 records to prevent server from overloading
def isDatabaseOverLimit():
    limit = 1000
    c.execute("select count(*) from api_data")
    count = c.fetchone()
    if count[0] >= limit:
        return True
    else:
        return False
	
#Since there's "version control" of the data value, each POST will ONLY insert new record instead of updating the existing ones in order to retrieve the value at any revision.
#Futher improvement can be made to limit how many revision to store in the database to prevent server from overload.

if __name__ == '__main__':
    app.run()