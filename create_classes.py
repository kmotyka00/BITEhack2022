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
from user_app.models import Classes


zumba1 = Classes(id=1, name="Zumba easy")
zumba2 = Classes(id=2, name="Zumba hard")
fitness1 = Classes(id=3, name="Fitness easy")
fitness2 = Classes(id=4, name="Fitness hard")

db.session.add(zumba1)
db.session.add(zumba2)
db.session.add(fitness1)
db.session.add(fitness2)
db.session.commit()