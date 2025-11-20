from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp
import sqlite3
import config
from dbase import db_init

db_file = config.DB_FILE_PATH
db_init(db_file)

app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY
csrf = CSRFProtect(app)


# Define the Flask-WTF form
class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField("Phone", validators=[DataRequired(), Regexp(r'^\+?\d{7,15}$', message="Invalid phone number")])
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField("Send Message")


# Home page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()

    if form.validate_on_submit():
        # Save to SQLite
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO contacts (name, email, phone, message)
                VALUES (?, ?, ?, ?)
            ''', (form.name.data, form.email.data, form.phone.data, form.message.data))
            conn.commit()
            conn.close()
            flash("Your message has been sent successfully!", "success")
        except sqlite3.Error as e:
            flash(f"Database error: {e}", "danger")

        return redirect(url_for('index'))

    return render_template('index.html', form=form)


if __name__ == "__main__":
    app.run(debug=config.DEBUG)
