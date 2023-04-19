from flask import Flask,render_template,request,redirect
from models import db,EmployeeModel
from sqlalchemy_utils import create_database, database_exists

url = 'mysql://root:root@localhost/employee_db'
if not database_exists(url):
    create_database(url)

app = Flask(__name__)
 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/employee_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
 
@app.before_first_request
def create_table():
    db.create_all()


@app.route('/create' , methods = ['GET','POST'])
def create():
    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position = position)
        db.session.add(employee)
        db.session.commit()
        return redirect('/')
    return render_template('createpage.html')
 
@app.route('/')
def RetrieveList():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html',employees = employees)
 
 
@app.route('/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee = employee)
    return f"Employee with id ={id} Doenst exist"
 
 
@app.route('/update/<int:id>/',methods = ['GET','POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = EmployeeModel(employee_id=id, name=name, age=age, position = position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/{id}')
        return f"Employee with id = {id} Does nit exist"
 
    return render_template('update.html', employee = employee)
 
 
@app.route('/delete/<int:id>/', methods=['GET','POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/')
 
    return render_template('delete.html')
    
if __name__=="main":
    app.run(debug=True,host='localhost', port=5000)