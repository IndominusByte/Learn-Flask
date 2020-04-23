from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('template-form/index.html')

@app.route('/signup')
def signup():
    return render_template('template-form/signup.html')

@app.route('/thankyou')
def thankyou():
    first = request.args.get('first')
    last = request.args.get('last')
    return render_template('template-form/thankyou.html',first=first,last=last)

@app.errorhandler(404)
def not_found(e):
    return render_template('template-form/404.html'), 404
'''
#basic routing and inheritance file
@app.route('/')
def index():
    name = 'nyoman'
    numbers = list(range(3))
    dic = {'name':'pradipta dewantara'}
    return render_template('basic.html',name=name,numbers=numbers,dic=dic)

@app.route('/home')
def home():
    return render_template('inheritance/home.html')

@app.route('/puppy/<name>')
def puppy(name):
    return render_template('inheritance/puppy.html',name=name)
'''

if __name__ == "__main__":
    app.run(debug=True)
