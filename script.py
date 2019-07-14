from flask import Flask, render_template,request,redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy,inspect
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   city = db.Column(db.String(50))
   address = db.Column(db.String(200))
   pin = db.Column(db.String(10))

   def __init__(self, name, city, address,pin):
         self.name = name
         self.city = city
         self.address = address
         self.pin = pin
   def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}



@app.route('/add_rec_api',methods=['POST'])
def add_new():
    try:
        params = request.get_json()
        for param in params:
            student = Students(param["name"],param["address"],param["city"],param["pin"])
            student.name = param["name"]
            student.address = param["address"]
            student.city = param["city"]
            student.pin = param["pin"]
            db.session.add(student)
        db.session.commit()
        return "result commited successfully"
    except:
         return "The commit was unsuccessful"

@app.route('/show_rec_api',methods = ['GET'])
def show_list():
    try:
        student = Students.query.all()
        student_temp = []
        for st in student:
            student_temp.append(st.toDict())

        return json.dumps(student_temp)
    except Exception as e:
        return str(e)

@app.route('/delete_rec',methods=['GET', 'POST'])
def delete_rec():
   try:
        params = request.get_json()
        json_str = json.dumps(params)
        resp_dict = json.loads(json_str)
        for del_rec in resp_dict:
            student_id = del_rec['id']
            Students.query.filter_by(id=student_id).delete()
        db.session.commit()

        return "The commit delete successful"
   except Exception as e:
        return str(e)

@app.route('/update_rec',methods = ['PUT'])
def update_rec():
    try:
        params = request.get_json()
        json_str = json.dumps(params)
        resp_dict = json.loads(json_str)
        for resp_dict1 in resp_dict:
            student_id = resp_dict1['id']
            student = Students.query.get(student_id)
            student.name = resp_dict1['name']
            student.city = resp_dict1['city']
            student.address = resp_dict1['address']
            student.pin = resp_dict1['pin']
        db.session.commit()
        return "The commit delete successful"

    except Exception as e:
          return str(e)


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)