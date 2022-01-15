#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import url_for, current_app
import secrets
import os
from user_app import mail
from flask_mail import Message


def send_reset_email(**kwargs):
    user = kwargs.get('user')
    app = kwargs.get('app')
    with app.app_context():
        try:
            token = user.get_token()
            msg = Message('Resetowanie hasła',
                          sender='noreply@panel.com',
                          recipients=[user.email])
            msg.body = f'''W celu zresetowania hasła wejdź w poniższy link:
            {url_for('users.token_reset', token=token, _external=True)} 

            Jeśli nie chcesz resetować hasła zignoruj tą wiadomość.
            '''
            mail.send(msg)
        except AttributeError:
            pass


def send_delete_email(**kwargs):
    user = kwargs.get('user')
    app = kwargs.get('app')
    with app.app_context():
        token = user.get_token()
        msg = Message('Usuwanie konta - panel studenta',
                      sender='noreply@panel.com',
                      recipients=[user.email])
        msg.body = f'''Aby usunąć konto wejdź w poniższy link:
        {url_for('users.delete_account', token=token, _external=True)} 

        Jeśli nie chcesz usuwać konta zignoruj tą wiadomość.
        '''
        mail.send(msg)


def send_confirm_email(**kwargs):
    user = kwargs.get('user')
    app = kwargs.get('app')
    with app.app_context():
        token = user.get_token()
        msg = Message('Potwierdzenie adresu email',
                      sender='noreply@panel.com',
                      recipients=[user.email])
        msg.body = f'''Aby aktywować konto wejdź w poniższy link:
            {url_for('users.confirm_email', token=token, _external=True)} 

            Jeśli nie chcesz zakładać konta zignoruj tą wiadomość.
            '''
        mail.send(msg)