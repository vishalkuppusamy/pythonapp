from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return '<h1><center>Welcome to Pragra Devops Session!</center></h1> <h2><center>This is a Jenkins Pipeline for Sample Flask Application</center></h2>'

app.run(host='0.0.0.0', port=5000)
