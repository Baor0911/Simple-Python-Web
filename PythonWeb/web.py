from flask import Flask, render_template, request,session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Bao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = password

@app.route('/')
def home():
    return 'Login and Signup page'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email:
            session['user'] = email
            found_user = User.query.filter_by(email = email).first()
            if found_user:
                flash('Email already used')
                return redirect(url_for('signup'))
            else:
                user = User(email = email, password = password)
                db.session.add(user)
                db.session.commit()
                flash('Signup success, return to login')

        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            flash('Success')
        else:
            flash('Wrong email or password, try again')

    return render_template('login.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)