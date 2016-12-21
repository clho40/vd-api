from flask import Flask, url_for
app = Flask(__name__)

@app.route('/object')
def api_object():
    return 'value1'

if __name__ == '__main__':
    app.run()