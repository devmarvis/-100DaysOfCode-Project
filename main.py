from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_bootstrap import Bootstrap5
from wtforms.validators import Email, DataRequired, Length
from smtplib import SMTP
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()

app = Flask(__name__)
bootstrap = Bootstrap5(app)

app_pass = os.getenv("email_pass")
secret_key = os.getenv("secret_key")
app_email = os.getenv("app_email")

app.secret_key = secret_key

date = datetime.now()


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(),])
    email = StringField('Email', validators=[Email(), DataRequired(), Length(min=6)])
    message = TextAreaField('Message', validators=[DataRequired(),])
    submit = SubmitField('Send Email')


@app.route("/", methods=['GET', 'POST'])
def home():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        name = contact_form.name.data
        email = contact_form.email.data
        body = contact_form.message.data
        with SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(
                user=app_email,
                password=app_pass
            )
            connection.sendmail(
                from_addr=email,
                to_addrs='erobagacollins@gmail.com',
                msg=f"Subject: Portfolio Contact \n\nName: {name}\n{body}"
            )
        print(contact_form.email.data)
    return render_template("index.html", form=contact_form, year=date.year)


if __name__ == '__main__':
    app.run(debug=True)
