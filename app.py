from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return "hey there music enthusiast"

@app.route('/index')
def index():
    return render_template('index.html')


if __name__=="__main__":
    app.run(port=4500,debug=True)
