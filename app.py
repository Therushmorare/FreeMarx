from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/app')
def appPage():
    return render_template('index.html')

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/view')
def view():
    return render_template('company_page.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/wallet')
def wallet():
    return render_template('wallet.html')

app.static_folder = 'static'
if __name__ == "__main":
    app.run(host='0.0.0.0',port = 5000, debug = True)