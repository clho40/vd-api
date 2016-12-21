from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Home'
	
@app.route('/object/<key>')
def api_object(key):
    return 'value1'

if __name__ == '__main__':
    app.run()