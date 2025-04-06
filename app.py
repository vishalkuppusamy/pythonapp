from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return '<h1><center>Welcome here!</center></h1> <h2><center>This is a Sample Flask Application</center></h2>'

app.run(host='0.0.0.0', port=5000)
