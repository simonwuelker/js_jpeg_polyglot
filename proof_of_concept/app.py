from flask import Flask, send_file

app = Flask(__name__)

@app.route('/image')
def image():
    return send_file('polyglot.jpg')

@app.route('/script')
def script():
    return send_file('polyglot.jpg')

@app.route('/')
def hello_world():
    return send_file("index.html")

if __name__ == '__main__':
   app.run()
