from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SECRET_KEY'] = 'your_secret_key'
# app.secret_key = 'secret_key' # tas pats kaip app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)


class User(db.Model):
    idd = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(dict(request.form))
        user_name = request.form['username_key']
        password = request.form['password_key']

        user = User.query.filter_by(username=user_name).first()
        if user:
            return render_template('register.html',
                                   message=user_name + 'username already exist!')
        new_user = User(username=user_name, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    return 'Login'
    # if 'username' in session:
    #     return redirect(url_for('home'))
    #
    # if request.method == 'POST':
    #     logusername = request.form['username']
    #     logpassword = request.form['password']
    #
    #     loguser = User.query.filter_by(username=logusername).first()
    #     if loguser and loguser.logpassword == logpassword

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
