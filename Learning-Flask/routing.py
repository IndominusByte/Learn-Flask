from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello world!</h1>"

@app.route('/information/<name>/<idd>')
def info(name,idd):
    return "<p>{} is nice person {}</p>".format(name,idd)

#exercise routing
@app.route('/puppy_latin/<name>')
def puppy_latin(name):
    if name[-1].lower() != 'y':
        return "<h1>{}</h1>".format(name + 'y')
    else:
        return "<h1>{}</h1>".format(name[:-1] + 'iful')

if __name__ == "__main__":
    app.run(debug=True)
