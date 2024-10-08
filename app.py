from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os


# Get the absolute path to the directory containing app.py
basedir = os.path.abspath(os.path.dirname(__file__))

# Set the path to the SQLite database file
db_path = os.path.join(basedir, 'contacts.db')

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'infocohortsoln@gmail.com'
app.config['MAIL_PASSWORD'] = 'nfeq kips ucxp umqx'
mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)

@app.route('/')
def index():
    contact = Contact.query.all()
    contact= contact[0]
    print(contact.email,'query')
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    contact = request.form['contact']
    message = request.form['message']
    print(name,email,message,contact)

    contact = Contact(name=name, email=email,contact=contact , message=message)
    db.session.add(contact)
    db.session.commit()

    print(Contact.query.all(),'query')

    send_email_notification(name, email)

    return redirect(url_for('index'))

def send_email_notification(name, email):
    msg = Message(subject='Thank you for your inquiry',
                  sender='infocohortsoln@gmail.com',
                  recipients=[email])
    msg.body = f'Hi {name},\n\nThank you for contacting us. Our team will get back to you shortly regarding your inquiry.\n\nBest regards,\nInfo Cohort Solution'
    mail.send(msg)

if __name__ == '__main__':
	with app.app_context():
    		db.create_all()
    		app.run(host='0.0.0.0', port=5000,debug=True)

