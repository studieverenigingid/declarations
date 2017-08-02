import os
import datetime
import requests
import json
from flask import Flask, render_template, request, send_from_directory, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# Get app
from .. import app
# Get texts for in email
from .. import texts

from enum import Enum
class ApiClient:
	apiUri = 'https://api.elasticemail.com/v2'
	apiKey = '2b6b6e02-146e-4dd8-aa13-350e65292717'

	@staticmethod
	def Request(method, url, data):
		data['apikey'] = ApiClient.apiKey
		if method == 'POST':
			result = requests.post(ApiClient.apiUri + url, params = data)
		elif method == 'PUT':
			result = requests.put(ApiClient.apiUri + url, params = data)
		elif method == 'GET':
			attach = ''
			for key in data:
				attach = attach + key + '=' + data[key] + '&'
			url = url + '?' + attach[:-1]
			result = requests.get(ApiClient.apiUri + url)

		jsonMy = result.json()

		if jsonMy['success'] is False:
			return jsonMy['error']

		return jsonMy['data']

def Send(subject, EEfrom, fromName, to, bodyHtml, bodyText, isTransactional):
	return ApiClient.Request('POST', '/email/send', {
		'subject': subject,
		'from': EEfrom,
		'fromName': fromName,
		'to': to,
		'bodyHtml': bodyHtml,
		'bodyText': bodyText,
		'isTransactional': isTransactional})




# Sending email
def mail(message, message_html, rec_name, rec_email):
    sender = 'Penningmeester <penningmeester-svid@fmjansen.nl>'
    receiver = "{0} <{1}>".format(rec_name, rec_email)
    return Send("Declaratie (nog ff doorsturen)",
        "penningmeester-svid@fmjansen.nl",
        "Penningmeester - Studievereniging i.d",
        receiver,
        message_html,
        message,
        True)



# Enrolling function
def declare(form):

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
        or not owner:
        return (json.dumps({ 'success': False, 'error': 'emptiness' }))

    message = texts.message.format(name, purchase, amount, committee, post,
        date, iban, owner)
    message_html = texts.message_html.format(name, purchase, amount, committee, post,
        date, iban, owner)

    # Try to send the confirmation mail
    mail_result = mail(message, message_html, name, email)
    if not mail_result:
        app.logger.error(mail_result.text)
        return (json.dumps({ 'success': False, 'error': 'mailing-error' }), 500)

    return json.dumps({ 'success': True })



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/declare/", methods=['POST'])
def declare_call():
    return declare(request.form)



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
