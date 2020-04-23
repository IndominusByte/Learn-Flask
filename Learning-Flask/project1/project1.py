from flask import Flask, render_template , request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def report():
    string = request.args.get('name')
    upper = any(list(map(lambda x: x.isupper(),string)))
    lower = any(list(map(lambda x: x.islower(),string)))
    number = string[-1].isdigit()
    #because it is generator and more eficiense
    test = any(x.isupper() for x in string)
    return render_template('report.html',upper=upper,lower=lower,number=number,test=test)

if __name__ == "__main__":
    app.run(debug=True)
