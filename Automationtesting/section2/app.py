from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return {'message':'nice'}

if __name__ == '__main__':
    app.run(debug=True)
