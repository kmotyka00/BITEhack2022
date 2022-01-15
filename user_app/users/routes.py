#!/usr/bin/python
# -*- coding: utf-8 -*-
import shutil
from flask import render_template, url_for, flash, redirect, Blueprint, request, current_app
from flask_login import current_user, logout_user, login_required, login_user
import datetime
from user_app.utils import send_confirm_email, send_delete_email
from user_app.users.forms import LoginForm, RegistrationForm
from user_app.models import User
from user_app import bcrypt, db
import json
import requests

users = Blueprint('users', __name__, template_folder='templates')

HOURS_DISCRETE = {
    0 : "6:00 - 7:00",
    1 : "7:00 - 8:00",
    2 : "8:00 - 9:00",
    3 : "9:00 - 10:00",
    4 : "11:00 - 12:00",
    5 : "12:00 - 13:00",
    6 : "13:00 - 14:00",
    7 : "14:00 - 15:00",
    8 : "15:00 - 16:00",
    9 : "16:00 - 17:00",
    10 : "17:00 - 18:00",
    11 : "18:00 - 19:00",
    12 : "19:00 - 20:00",
    13 : "20:00 - 21:00",
    14 : "21:00 - 22:00",
    15 : "22:00 - 23:00",
    16 : "23:00 - 00:00",
    17 : "00:00 - 01:00"
}


DAYS_DISCRETE = [[0, "Poniedzialek"], [1, "Wtorek"], [2, "Sroda"], [3, "Czwartek"], [4, "Piatek"], [5, "Sobota"], [6, "Niedziela"]]
COURSES_DISCRETE = [[0, "CELLULITE KILLER"], [1, "ZUMBA"], [2, "ZUMBA ADVANCED"], [3,"FITNESS"], [4,"CROSSFIT"],
                    [5,"BRAZILIAN BUTT"], [6,"PILATES"], [7,"CITY PUMP"], [8,"STRETCHING"], [9,"YOGA"]]


@users.route("/", methods=['GET', 'POST'])
def home():
    """
    Return home page. This page is different for logged and
    not logged in users.
    """
    if current_user.is_authenticated:
        if current_user.confirmed:
            if request.args:
                user_preferences = {"id":current_user.id,
                                    "name":current_user.name,
                                    "surname":current_user.surname,
                                    "email":current_user.email}
                day_available = []
                days = {}
                activities = []
                for el in request.args:
                    if "-" in el:
                        day_id = int(el[:1])
                        time_id = int(el[2:])
                        if day_id in days.keys():
                            days[day_id].append(time_id)
                        else:
                            days[day_id] = [time_id]
                    else:
                        activities.append(int(el))
                for key in days.keys():
                    day_available.append([key, days[key]])

                user_preferences["classes"] = activities
                user_preferences["availability"] = day_available
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                requests.post("http://localhost:5001", data=json.dumps(user_preferences), headers=headers)


            return render_template("home_logged.html", days=DAYS_DISCRETE, hours=HOURS_DISCRETE, courses=COURSES_DISCRETE)
        else:
            return redirect(url_for('users.unconfirmed'))

    form_log = LoginForm()

    if form_log.validate_on_submit():
        user = User.query.filter_by(email=form_log.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form_log.password.data):
            login_user(user, remember=form_log.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.home'))
        else:
            flash('Niepoprawne logowanie. Sprawdź email i hasło', 'danger')
    return render_template("home_login.html", form_log=form_log)


@users.route("/register", methods=['GET', 'POST'])
def register():
    """
    Endpoint for registering new users. If user is already logged in he is
    redirected to home page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    form_reg = RegistrationForm()
    if form_reg.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form_reg.password.data).decode('utf-8')
        user = User(name=form_reg.name.data, surname=form_reg.surname.data, email=form_reg.email.data,
                    password=hashed_pass, confirmed=False)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        #flash(f'Utworzono konto dla: {form_reg.name.data} {form_reg.surname.data}! Na podany adres email za chwilę zostanie wysłana wiadomość z potwierdzeniem.', 'success')
        send_confirm_email(user=current_user, app=current_app)
        return redirect(url_for('users.unconfirmed'))
        #return redirect(url_for('users.home'))
    return render_template("registration.html", form_reg=form_reg, title="Rejestracja")


@users.route('/unconfirmed')
@login_required
def unconfirmed():
    """
    If users email is not confirmed he is shown this page.
    """
    if current_user.confirmed:
        return redirect('users.home')
    return render_template('unconfirmed.html')


@users.route('/confirm/<token>')
@login_required
def confirm_email(token):
    """
   Confirm user's email. If token is expired or invalid or user is already
   confirmed, appropriate message is flashed.
   """
    user = User.verify_token(token)
    if user is None:
        flash("Link aktywujący konto wygasł lub jest nieważny", "warning")
        return redirect(url_for('users.home'))
    if user.confirmed:
        flash('Konto zostało już aktywowane. Proszę się zalogować', 'success')
    else:
        user.confirmed = True
        user.confirmed_on = datetime.datetime.now()
        db.session.commit()
        flash('Email został potwierdzony', 'success')
    return redirect(url_for('users.home'))


@login_required
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('users.home'))


@users.route("/delete_account", methods=['GET', 'POST'])
@login_required
def request_delete():
    """
    Page to request account deletion.
    """
    send_delete_email(user=current_user, app=current_app)
    flash("Jeśli podany adres email jest powiązany z kontem została na niego wysłana "
          "informacja dotycząca usuwania konta.", 'info')
    return redirect(url_for('users.home'))


@users.route("/account/<token>", methods=['GET', 'POST'])
def delete_account(token):
    """
    Delete user's account.
    """
    user = User.verify_token(token)
    if user is None:
        # If token is expired or invalid flash information and redirect to home page.
        flash("Link usuwający konto wygasł lub jest nieważny", "warning")
        return redirect(url_for('users.home'))
    else:
        if current_user.is_authenticated:
            logout_user()
        db.session.delete(user)
        db.session.commit()
        flash(f'Konto zostało usunięte', 'success')
        return redirect(url_for('users.home'))
