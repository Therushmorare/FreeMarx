import sys
import os
from flask import Flask, render_template, request, url_for, redirect,send_from_directory, jsonify,session, flash
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
#from flask_session import Session
from sqlalchemy import desc
from sqlalchemy import or_
import psycopg2
from psycopg2 import OperationalError
from datetime import date
import secrets
from database import db
from flask_bcrypt import Bcrypt
from api.login import login
from api.signup import company_signup, investor_signup
from models.investors import Investor
from models.company import Company
from api.create_investor_profile import profile, investorP
from api.company_steps import company_profile
from api.wallet import balance_create, top_up
from queries.investor_dashboard import *
from api.buy import buy_stocks
from api.sell import sell_stocks
from queries.company_dashboard import *
from models.equities import EquityInfo
from api.search import search
from api.share_update import equity_update

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['WORKER_TIMEOUT'] = 60

app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'database.db')

db.init_app(app)

bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['upload_folder'] = 'static/Profiles'
app.config['portfolio_folder'] = 'static/Portfolio'
app.config['founder_folder'] = 'static/Founder'
app.config['statements_folder'] = 'static/financials'

@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/investorLoginPage')
def investorLoginPage():
    return render_template('login.html')

@app.route('/companyLoginPage')
def companyLoginPage():
    return render_template('company_login.html')

@app.route('/investorSignupPage')
def investorSignupPage():
    return render_template('signup.html')

@app.route('/companySignupPage')
def companySignupPage():
    return render_template('company_signup.html')

@app.route('/investorProfileCreate/<string:id>')
def investorProfileCreate(id):
    user_id = id
    return render_template('create_profile.html', user_id = user_id)

@app.route('/balanceManagement/<string:id>')
def balanceManagement(id):
    user_id = id
    return render_template('balance.html', user_id = user_id)

@app.route('/investorDashboard/<string:id>')
def investorDashboard(id):
    user_id = id
    entities = companies_i(db)
    info = company_info_i(db)
    info2 = company_info_i(db)
    shares = equities_i(db)
    my_summary = port_data(user_id, db)
    my_info = investor_info(user_id, db)
    my_profile = investor_profile_info(user_id, db)

    return render_template('index.html', user_id = user_id, info = info, info2 = info2, entities = entities, shares = shares, my_summary = my_summary, my_info = my_info, my_profile = my_profile)

@app.route('/companySteps/<string:id>')
def companySteps(id):
    user_id = id
    return render_template('company_steps.html', user_id = user_id)

@app.route('/companyDashboard/<string:id>')
def companyDashboard(id):
    user_id = id
    equity = EquityInfo.query.filter_by(company_id = user_id).all()
    info = company_info(user_id, db)
    info2 = company_info(user_id, db)
    return render_template('company_dashboard.html', user_id = user_id, equity = equity, info = info, info2 = info2)

@app.route('/companyAccount/<string:id>')
def companyAccount(id):
    user_id = id
    equity = EquityInfo.query.filter_by(company_id = user_id).all()
    info = company_info(user_id, db)
    info2 = company_info_two(user_id, db)
    return render_template('company_profile.html', user_id = user_id, equity = equity, info = info, info2 = info2)


@app.route('/buyPage/<string:id>/<string:cid>')
def buyPage(id, cid):
    investor_id = id
    company_id = cid
    return render_template('buy.html', investor_id = investor_id, company_id = company_id)

@app.route('/sellPage/<string:id>/<string:rid>/<string:cid>')
def sellPage(id, rid, cid):
    investor_id = id
    receipt_id = rid
    company_id = cid
    return render_template('sell.html', investor_id = investor_id, receipt_id = receipt_id, company_id = company_id)

@app.route('/account/<string:id>')
def account(id):
    user_id = id
    my_info = investor_info(user_id, db)
    my_profile = investor_profile_info(user_id, db)
    return render_template('account.html', user_id = user_id, my_info = my_info, my_profile = my_profile)

@app.route('/view/<string:id>/<string:cid>')
def view(id, cid):
    user_id = id
    company_id = cid
    my_info = companies(company_id, db)
    basic_info = company_info(company_id, db)
    advanced_info = company_info_two(company_id, db)
    equity = equities(company_id, db)
    founder_info = founders(company_id, db)
    statements = financials(company_id, db)
    all_buys = buyers(company_id, db)
    all_sells = sellers(company_id, db)
    return render_template('company_page.html', user_id = user_id, company_id = company_id, my_info = my_info, basic_info = basic_info, advanced_info = advanced_info, equity = equity, founder_info = founder_info, statements = statements, all_buys = all_buys, all_sells = all_sells)

@app.route('/portfolio/<string:id>')
def portfolio(id):
    user_id = id
    portfolio_data = port_data_two(db)
    company_info1 = company_info_i(db)
    company_info2 = company_info_two_i(db)
    my_wallet = wallet_info(user_id, db)
    my_info = investor_info(user_id, db)
    my_profile = investor_profile_info(user_id, db)
    return render_template('portfolio.html', user_id = user_id, portfolio_data = portfolio_data, company_info1 = company_info1, company_info2 = company_info2, my_wallet = my_wallet, my_info = my_info, my_profile = my_profile)

@app.route('/wallet/<string:id>')
def wallet(id):
    user_id = id
    my_wallet = wallet_info(user_id, db)
    purchases = buys_two(user_id, db)
    debits = topupdata(user_id, db)
    my_info = investor_info(user_id, db)
    my_profile = investor_profile_info(user_id, db)
    return render_template('wallet.html', user_id = user_id, my_wallet = my_wallet, purchases = purchases, debits = debits, my_info = my_info, my_profile = my_profile)

#login functionality
@app.route('/investorLoginFunction', methods=('GET', 'POST'))
def investorLoginFunction():
    if request.method == "POST":
        try:
            #form inputs
            emailText = request.form.get('email')
            passwordText = request.form.get('password')
            session["email"] = request.form.get("email")
            user = Investor.query.filter_by(email = emailText).first()
            if not user:
                return render_template('errors.html', err='User does not exist!')
            elif bcrypt.check_password_hash(user.password, passwordText) is False:
                return render_template('errors.html', err='Password is incorrect!')
            else:
                return redirect(url_for('investorDashboard', id = user.id))
        except OperationalError:
            return render_template('errors.html', err='There was a server error')
    return render_template('login.html')

@app.route('/companyLoginFunction', methods=('GET', 'POST'))
def companyLoginFunction():
    if request.method == "POST":
        try:
            #form inputs
            emailText = request.form.get('email')
            passwordText = request.form.get('password')
            session["email"] = request.form.get("email")
            user = Company.query.filter_by(email = emailText).first()
            if not user:
                return render_template('errors.html', err='User does not exist!')
            elif bcrypt.check_password_hash(user.password, passwordText) is False:
                return render_template('errors.html', err='Password is incorrect!')
            else:
                return redirect(url_for('companyDashboard', id = user.id))
        except OperationalError:
            return render_template('errors.html', err='There was a server error')
    return render_template('company_login.html')

#investor logout
@app.route('/investorLogout')
def investorLogout():
    session.pop('email', None)
    return redirect('/')

#company logout
@app.route('/companyLogout')
def companyLogout():
    session.pop('email', None)
    return redirect('/')

#signup functionality
@app.route('/investorSignupFunction', methods=('GET', 'POST'))
def investorSignupFunction():
    if request.method == 'POST':
        try:
            firstname = request.form.get('firstName')
            lastname = request.form.get('lastName')
            email = request.form.get('email')
            password = request.form.get('password')
            if not password:
                flash('Password must be non-empty.', 'error')
                return redirect(url_for('investorSignupFunction'))
            #hash password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            result = investor_signup(firstname, lastname, email, hashed_password)
            if result:
                return result
        except OperationalError:
            db.session.rollback()
            return render_template('server_error.html', err='Server interuption, please reload page..')
    return render_template('signup.html')

@app.route('/companySignupFunction', methods=('GET', 'POST'))
def companySignupFunction():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            #hash password
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            result = company_signup(email, hashed_password)
            if result:
                return result
        except OperationalError:
            db.session.rollback()
            return render_template('server_error.html', err='Server interuption, please reload page..')
    return render_template('signup.html')

#invstor profile
@app.route('/createInvestorProfile/<string:id>', methods=('GET', 'POST'))
def createInvestorProfile(id):
    if request.method == 'POST':
        try:
            picture = request.files['profileImage']
            bio = request.form.get('bio')
            upload_folder = app.config['upload_folder']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            picture.save(os.path.join(app.config['upload_folder'],picture.filename))
            img_file = picture.filename
            result = investorP(img_file, bio, id)
            if result:
                return result
        except OperationalError:
            return render_template('errors.html', err='Could not load page')
    return redirect(url_for('createInvestorprofile', id = id))

#company profile
@app.route('/companyProfileSteps/<string:id>', methods=('GET', 'POST'))
def companyProfileSteps(id):
    if request.method == 'POST':
        try:
            logo_file = request.files['logoFile']
            company_name = request.form.get('company_name')
            sector = request.form.get('sector')
            industry = request.form.get('industry')
            number_of_employees = request.form.get('employees')
            details = request.form.get('company_details')
            founder_file = request.files['foundersFile']
            address = request.form.get('address')
            equity_type = request.form.get('equity_type')
            equity_quantity = request.form.get('quantity')
            goal = request.form.get('goal')
            financial_statements = request.files['financial_statements']
            upload_folder_1 = app.config['portfolio_folder']
            upload_folder_2 = app.config['founder_folder']
            upload_folder_3 = app.config['statements_folder']

            if not os.path.exists(upload_folder_1):
                os.makedirs(upload_folder_1)
            if not os.path.exists(upload_folder_2):
                os.makedirs(upload_folder_2)
            if not os.path.exists(upload_folder_3):
                os.makedirs(upload_folder_3)
            #add files to folders
            logo_file.save(os.path.join(app.config['portfolio_folder'], logo_file.filename))
            founder_file.save(os.path.join(app.config['founder_folder'], founder_file.filename))
            financial_statements.save(os.path.join(app.config['statements_folder'], financial_statements.filename))
            results = company_profile(logo_file.filename, company_name, sector, industry, number_of_employees, details, founder_file.filename, address, equity_type, equity_quantity, goal, financial_statements.filename, id)
            if results:
                return results
        except OperationalError:
            return render_template('errors.html', err='Could not load page')
    return redirect(url_for('companyProfileSteps', id = id))

#add money to wallet
@app.route('/addToWallet/<string:id>', methods=('GET', 'POST'))
def addToWallet(id):
    if request.method == "POST":
        try:
            account_type = request.form.get('type')
            account_amount = request.form.get('amount')
            result = balance_create(account_type, account_amount, id)
            if result:
                return result
        except OperationalError:
            return render_template('errors.html', err='Could not load page')
    return redirect(url_for('addToWallet', id = id))

#buy shares
@app.route('/buyShare/<string:id>/<string:cid>', methods=('GET', 'POST'))
def buyShare(id, cid):
    if request.method == "POST":
        try:
            share_type = 'ordinary shares'
            quantity = request.form.get('quantity')
            result = buy_stocks(cid, id, share_type, quantity)
            if result:
                return result
        except OperationalError:
            return render_template('errors.html', err='Could not load page')
    return redirect(url_for('investorDashboard', id = id))

#sell shares
@app.route('/sellShare/<string:id>/<string:rid>/<string:cid>', methods=('GET', 'POST'))
def sellShare(id, rid, cid):
    if request.method == "POST":
        try:
            quantity = request.form.get('quantity')
            result = sell_stocks(rid, id, cid, quantity)
            if result:
                return result
        except OperationalError:
            return render_template('errors.html', err='Could not load page')
    return redirect(url_for('investorDashboard', id = id))

#account top up
@app.route('/accountTopUp/<string:id>', methods=('GET', 'POST'))
def accountTopUp(id):
    if request.method == 'POST':
        try:
            type = request.form.get('type')
            amount = request.form.get('amount')
            result = top_up(type,amount, id)
            if result:
                return result
        except OperationalError:
            return render_template('errors.html', err='Could not load page')
    return redirect(url_for('wallet', id=id))

#search handle
@app.route('/searchCompany/<string:id>', methods=('GET', 'POST'))
def searchCompany(id):
    if request.method == 'POST':
        try:
            search_value = request.form.get('query')
            result = search(search_value, id)
            if result:
                return result
        except OperationalError:
            return render_template('errors.html', err='Could not load page')
    return render_template('search.html', user_id = id)

#share top ups
@app.route('/shareUpdate/<string:id>', methods=('GET', 'POST'))
def shareUpdate(id):
    if request.method == 'POST':
        try:
            type_val = request.form.get('equity_type')
            share_val = request.form.get('quantity')
            share_amount = request.form.get('goal')
            result = equity_update(id, type_val, share_val, share_amount)
            if result:
                return result
        except OperationalError:
            return render_template('errors.html', err='Could not find page')
    return redirect(url_for('companyDashboard', id=id))

app.static_folder = 'static'
if __name__ == "__main":
    app.run(host='0.0.0.0',port = 5000, debug = True)