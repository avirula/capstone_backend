from flask import Flask, request, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt 
from dotenv import load_dotenv 
import os

load_dotenv()
database_url = "postgresql:" + ":".join(os.environ.get("DATABASE_URL", "").split(":")[1:])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avirula.db'
db = SQLAlchemy(app)
basedir = os.path.abspath(os.path.dirname(__file__))
#db = SQLAlchemy(app)
ma = Marshmallow(app)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///avirula.db'
CORS(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password')

user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

@app.route('/user/add', methods=['POST'])
def add_user():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')
    
    post_data = request.get_json()
    username = post_data.get('username')
    password = post_data.get('password')
    
    possible_duplicate = db.session.query(User).filter(User.username == username).first()
    
    if possible_duplicate is not None:
        return jsonify('Error: The username is taken.')
    
    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username, encrypted_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify("Congrats you've signed up for an account!")



@app.route('/user/get', methods=['GET'])
def get_users():
    all_users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(all_users))

@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
    user = db.session.query(User).filter(User.id == id).first()
    db.session.delete(user)
    db.session.commit()
    
    return jsonify(f'The user {user.username} has been deleted.')

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    occupation = db.Column(db.String, nullable=True)
    pay = db.Column(db.Integer, unique=False)
    rent = db.Column(db.Integer, unique=False)
    vehicle_insurance = db.Column(db.Integer, unique=False)
    phone_bill = db.Column(db.Integer, unique=False)
    health_insurance = db.Column(db.Integer, unique=False)
    credit_card_bill = db.Column(db.Integer, unique=False)
    total_in_loans = db.Column(db.Integer, unique=False)
    tv_subscriptions_total = db.Column(db.Integer, unique=False)
    cable_bill = db.Column(db.Integer, unique=False)
    electric_bill = db.Column(db.Integer, unique=False)
    misc_expense_1 = db.Column(db.Integer, unique=False)
    misc_expense_2 = db.Column(db.Integer, unique=False)
    misc_expense_3 = db.Column(db.Integer, unique=False)
    misc_expense_4 = db.Column(db.Integer, unique=False)
   
    
    
    def __init__(self, name, occupation, pay, rent, vehicle_insurance, phone_bill, health_insurance, credit_card_bill, total_in_loans, tv_subscriptions_total,
                cable_bill, electric_bill, misc_expense_1, misc_expense_2, misc_expense_3, misc_expense_4):
        self.name = name
        self.occupation = occupation
        self.pay = pay
        self.rent = rent
        self.vehicle_insurance = vehicle_insurance
        self.phone_bill = phone_bill
        self.health_insurance = health_insurance
        self.credit_card_bill = credit_card_bill
        self.total_in_loans = total_in_loans
        self.tv_subscriptions_total = tv_subscriptions_total
        self.cable_bill = cable_bill
        self.electric_bill = electric_bill
        self.misc_expense_1 = misc_expense_1
        self.misc_expense_2 = misc_expense_2
        self.misc_expense_3 = misc_expense_3
        self.misc_expense_4 = misc_expense_4
        
class ExpenseSchema(ma.Schema):
    class Meta:
        fields = ("id","name", "occupation", "pay", "rent", "vehicle_insurance", "phone_bill", "health_insurance", "credit_card_bill", "total_in_loans", 
                  "tv_subscriptions_total", "cable_bill", "electric_bill", "misc_expense_1", "misc_expense_2", "misc_expense_3", "misc_expense_4")
        
expense_schema = ExpenseSchema()
multiple_expense_schema = ExpenseSchema(many=True)
        
@app.route('/expense/add', methods=['POST'])
def add_expense():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')
    
    post_data = request.get_json()
    name = post_data.get('name')
    occupation = post_data.get('occupation')
    pay = post_data.get('pay')
    rent = post_data.get('rent')
    vehicle_insurance = post_data.get('vehicle_insurance')
    phone_bill = post_data.get('phone_bill')
    health_insurance = post_data.get('health_insurance')
    credit_card_bill = post_data.get('credit_card_bill')
    total_in_loans = post_data.get('total_in_loans')
    tv_subscriptions_total = post_data.get('tv_subscriptions_total')
    cable_bill = post_data.get('cable_bill')
    electric_bill = post_data.get('electric_bill')
    misc_expense_1 = post_data.get('misc_expense_1')
    misc_expense_2 = post_data.get('misc_expense_2')
    misc_expense_3 = post_data.get('misc_expense_3')
    misc_expense_4 = post_data.get('misc_expense_4')
  
    expense = db.session.query(Expense).filter(Expense.name == name).first()
    
    if name == None:
        return jsonify("Error: data must have a 'Name' key.")
    if expense:
        return jsonify("Error: expense must be unique.")
    if occupation == None:
        return jsonify("Error: data must have an 'Occupation' key .")
    
    new_expense = Expense(name, occupation, pay, rent, vehicle_insurance, phone_bill, health_insurance, credit_card_bill, total_in_loans,
                          tv_subscriptions_total, cable_bill, electric_bill, misc_expense_1, misc_expense_2, misc_expense_3, misc_expense_4)
    db.session.add(new_expense)
    db.session.commit()
    
    return jsonify("You've added a new expense!")

@app.route('/expense/get', methods=["GET"])
def get_expenses():
    expenses = db.session.query(Expense).all()
    return jsonify(multiple_expense_schema.dump(expenses))
    return []

@app.route('/expense/delete/<id>', methods=["DELETE"])
def delete_expense_by_id(id):
    expense = db.session.query(Expense).filter(Expense.id == id).first()
    db.session.delete(expense)
    db.session.commit()
    
    return jsonify("The expense has been deleted.")

@app.route('/expense/update/<id>', methods=["PUT", "PATCH"])
def update_expense_by_name(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json!')
    
    post_data = request.get_json()
    name = post_data.get('name')
    occupation = post_data.get('occupation')
    pay = post_data.get('pay')
    rent = post_data.get('rent')
    vehicle_insurance = post_data.get('vehicle_insurance')
    phone_bill = post_data.get('phone_bill')
    health_insurance = post_data.get('health_insurance')
    credit_card_bill = post_data.get('credit_card_bill')
    total_in_loans = post_data.get('total_in_loans')
    tv_subscriptions_total = post_data.get('tv_subscriptions_total')
    cable_bill = post_data.get('cable_bill')
    electric_bill = post_data.get('electric_bill')
    misc_expense_1 = post_data.get('misc_expense_1')
    misc_expense_2 = post_data.get('misc_expense_2')
    misc_expense_3 = post_data.get('misc_expense_3')
    misc_expense_4 = post_data.get('misc_expense_4')
    
        
    expense = db.session.query(Expense).filter(Expense.id == id).first()

    if name != None:
        expense.name = name
    if occupation != None:
        expense.occupation = occupation
    if pay != None:
        expense.pay = pay
    if rent != None:
        expense.rent = rent
    if vehicle_insurance != None:
        expense.vehicle_insurance = vehicle_insurance
    if phone_bill != None:
        expense.phone_bill = phone_bill
    if health_insurance != None:
        expense.health_insurance = health_insurance
    if credit_card_bill != None:
        expense.credit_card_bill = credit_card_bill
    if total_in_loans != None:
        expense.total_in_loans = total_in_loans
    if tv_subscriptions_total != None:
        expense.tv_subscriptions_total = tv_subscriptions_total
    if cable_bill != None:
        expense.cable_bill = cable_bill
    if electric_bill != None:
        expense.electric_bill = electric_bill
    if misc_expense_1 != None:
        expense.misc_expense_1 = misc_expense_1
    if misc_expense_2 != None:
        expense.misc_expense_2 = misc_expense_2
    if misc_expense_3 != None:
        expense.misc_expense_3 = misc_expense_3
    if misc_expense_4 != None:
        expense.misc_expense_4 = misc_expense_4
    
    db.session.commit()
    return jsonify("Expense has been updated!")
            
if __name__ == "__main__":
    app.run(debug=True)
    
