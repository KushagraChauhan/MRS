from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "hey there music enthusiast"

@app.route('/index')
def index():
    return "Index"


if __name__=="__main__":
    app.run(port=4500,debug=True)
