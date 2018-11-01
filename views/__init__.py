import os
import datetime
import requests
import json
from flask import Flask, render_template, request, send_from_directory, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

import hashlib
import time
from io import StringIO

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from email import encoders

# Get app
from .. import app
# Get texts for in email
from .. import texts
# Get email addresses
from .. import email_addresses

COMMASPACE = ', '
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def sendMail(to, fro, subject, text, text_html, files=[], server="localhost"):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = fro
    msg['To'] = COMMASPACE.join(to)
    msg['Subject'] = subject

    msg_text = MIMEMultipart('alternative')
    msg.attach(msg_text)
    msg_text.attach( MIMEText(text, 'plain') )
    msg_text.attach( MIMEText(text_html, 'html') )

    for file in files:
        if file.mimetype == 'application/pdf':
            part = MIMEApplication(file.read())
            part.add_header('Content-Disposition', 'attachment', filename=file.filename)
        else:
            part = MIMEImage(file.read(), name=file.filename)
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    send_result = smtp.sendmail( fro, to, msg.as_string() )
    smtp.close()
    return send_result



# Sending email
def mail(message, message_html, rec_name, rec_email, receipt, committee):
    receiver = ["Penningmeester <penningmeester-svid@tudelft.nl>", email_addresses.committee_emails[committee]]
    sender = "De Server <noreply@svid.nl>"

    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))
    subject = "Declaratie [{0}]".format(hash.hexdigest()[:8])

    return sendMail(receiver, sender, subject, message, message_html, [receipt])



# Enrolling function
def declare(form, files):

    try:
        purchase = form['purchase']
        amount = form['amount']
        committee = form['committee']
        post = form['post']
        date = form['date']
        name = form['name']
        email = form['email']
        iban = form['iban']
        owner = form['owner']
        receipt = files['receipt']
    except KeyError as e:
        app.logger.warn(e)
    except TypeError as e:
        app.logger.warn(e)

    # Check for empty fields
    if not purchase \
        or not amount \
        or not committee \
        or not post \
        or not date \
        or not name \
        or not email \
        or not iban \
        or not owner \
        or not receipt \
        or receipt.filename == '':
        return (json.dumps({ 'success': False, 'error': 'emptiness' }))

    if not allowed_file(receipt.filename):
        return (json.dumps({ 'success': False, 'error': 'file-not-allowed' }))

    message = texts.message.format(name, purchase, amount, committee, post,
        date, iban, owner, email)
    message_html = texts.message_html.format(name, purchase, amount, committee, post,
        date, iban, owner, email)

    # Try to send the confirmation mail
    mail_result = mail(message, message_html, name, email, receipt, committee)
    if len(mail_result) is not 0:
        app.logger.error(mail_result)
        return (json.dumps({
            'success': False,
            'error': 'mailing-error',
            'smtp-error': mail_result
        }), 500)

    return json.dumps({ 'success': True })



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/declare/", methods=['POST'])
def declare_call():
    return declare(request.form, request.files)



@app.errorhandler(404)
def page_not_found(e):
    return "404"

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')



if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
