from flask import (
    Blueprint, render_template, request, flash, redirect, url_for, current_app
)
import os
from email.message import EmailMessage
import ssl
import smtplib

from app.db import get_db

bp = Blueprint('mail', __name__, url_prefix="/")

@bp.route('/', methods=['GET'])
def index():
    search = request.args.get('search')
    db, c = get_db()

    if search is None:
        c.execute('SELECT * FROM email')
    else:
        c.execute('SELECT * FROM email WHERE content LIKE %s', ('%' + search + '%', ))
    mails= c.fetchall()
    return render_template('mails/index.html', mails=mails)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        email = request.form.get('email')
        subject = request.form.get('subject')
        content = request.form.get('content')
        errors = []

        if not email:
            errors.append('El email es requerido!')
        if not subject:
            errors.append('Aclara el asunto por favor!')
        if not content:
            errors.append('Tienes que poner un contenido!')

        if len(errors) > 0:
            for error in errors:
                flash(error)
        else:
            send(email, subject, content)
            db, c = get_db()
            c.execute("INSERT INTO email(email, subject, content) VALUES(%s,%s,%s)", (email, subject, content))
            db.commit()

            return redirect(url_for('mail.index'))
        

    return render_template('mails/create.html')


def send(to, subject, content):

    em = EmailMessage()
    em['From'] = current_app.config['EMAIL_SENDER']
    em['To'] = to
    em["Subject"] = subject
    em.set_content(content)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp: 
        smtp.login(email_sender,current_app.config['PASSWORD'])
        smtp.sendmail(email_sender, to, em.as_string())



