#!/usr/bin/python
# -*- coding: utf-8 -*-
from dotenv import load_dotenv
load_dotenv()
import os
os.getenv('SQLALCHEMY_DATABASE_URI')
from user_app import create_app
app = create_app()
app.app_context().push()
from user_app import db
db.drop_all()
db.create_all()