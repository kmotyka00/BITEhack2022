#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileSize
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from user_app.models import User, Classes
from flask_login import current_user
import re
from wtforms_sqlalchemy.fields import QuerySelectField


MIN_USR = 1
MIN_PASS = 8


def choice_classes():
    return Classes.query


class ChoiceForm(FlaskForm):
    opts = QuerySelectField(query_factory=choice_classes, allow_blank=True)


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(message='Pole wymagane'), Email(message='Niepoprawny format email')],
                        render_kw={"placeholder": "Email"})
    password = PasswordField('Hasło', validators=[DataRequired(message='Pole wymagane')],
                             render_kw={"placeholder": "Hasło"})
    remember = BooleanField("Zapamiętaj")
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    name = StringField('Imie',
                           validators=[DataRequired(message='Pole wymagane'), Length(min=MIN_USR,
                           message=f'Nazwa uzytkownika musi mieć minimum {MIN_USR} znaków')],
                           render_kw={"placeholder": "Imie"})

    surname = StringField('Nazwisko',
                       validators=[DataRequired(message='Pole wymagane'), Length(min=MIN_USR,
                                                                                 message=f'Nazwa uzytkownika musi mieć minimum {MIN_USR} znaków')],
                       render_kw={"placeholder": "Nazwisko"})

    email = StringField('Email', validators=[DataRequired(message='Pole wymagane'),
                                             Email(message='Niepoprawny format email')],
                        render_kw={"placeholder": "Email"})

    password = PasswordField(f'Hasło (minimum {MIN_PASS} znaków)',
                             validators=[DataRequired(message='Pole wymagane'),
                                         Length(min=MIN_PASS, message='Hasło musi mieć minimum '
                                                                                    f'{MIN_PASS} znaków')],
                             render_kw={"placeholder": f'Hasło (minimum {MIN_PASS} znaków)'})

    confirm_password = PasswordField('Powtórz hasło', validators=[DataRequired(message='Pole wymagane'),
                                                                  EqualTo('password', message='Hasła '
                                                                                              'muszą się zgadzać')],
                                     render_kw={"placeholder": "Powtórz hasło"})

    submit = SubmitField('Sign Up')

    def validate_name(self, username):
        if re.findall(r"[^a-zA-Z0-9_]", username.data):
            raise ValidationError("Nazwa użytkownika może zawierać tylko angielskie litery, cyfry "
                                  "oraz znak _")

    def validate_surname(self, username):
        if re.findall(r"[^a-zA-Z0-9_]", username.data):
            raise ValidationError("Nazwa użytkownika może zawierać tylko angielskie litery, cyfry "
                                  "oraz znak _")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email jest już zajęty")

    def validate_password(self, password):
        if re.findall(r"[^a-zA-Z0-9_!@#$%^&*]", password.data):
            raise ValidationError("Hasło może zawierać tylko angielskie litery, cyfry "
                                  "oraz znaki _!@#$%^&*")



