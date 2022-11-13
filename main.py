from flask import Flask, render_template
import smtplib
import secrets
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.widgets import TextArea
import os
from dotenv import load_dotenv
import email_validator


### CONSTANTS ###
load_dotenv()
MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")


### CONTACT FORM ###
class ContactForm(FlaskForm):
    name = StringField(label='full name', validators=[DataRequired()])
    email = StringField(label='email', validators=[DataRequired(), Email()])
    number = StringField(label='phone number')
    message = StringField(label='message', validators=[DataRequired()], widget=TextArea())
    send = SubmitField(label="Send")


### FLASK INI ###
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


### MODALS ###
@app.route("/stop-video/<int:id>")
def stop_video(id):
    # replace video div content with "" when modal is closed, keep div ID
    return render_template("empty-modal.html", id=id)


@app.route("/modal/<int:id>")
def load_modal(id):
    # load video div when modal is open
    return render_template(f"modal{id}.html")


### MAIN ###
@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    # if form valid:
    if form.validate_on_submit():
        full_name = form.name.data
        email = form.email.data
        number = form.number.data
        message_text = form.message.data
        # the whole message must be encoded to see accented characters
        message = (
            f"Subject: New Portfolio Message\n\n {message_text} \nPhone number: {number} \nMail: {email} \nMessage from {full_name}").encode(
            'utf-8')

        with smtplib.SMTP('smtp.gmail.com', port=587, ) as connection:
            connection.ehlo()
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=f"sedlacek.radek@email.cz",
                msg=message
            )
        return render_template("index.html", alert=True, form=form)
    # if form NOT valid:
    for fieldName, errorMessages in form.errors.items():
        for err in errorMessages:
            return err
    return render_template("index.html", alert=False, form=form)


# TO TEST LOCALLY ###
if __name__ == "__main__":
    app.run(debug=True)