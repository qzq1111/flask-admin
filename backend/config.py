#!/usr/bin/env python
# -*- encoding: utf-8 -*-

DB_USER = "root"
DB_PASS = "123456"
DB_ADDR = "127.0.0.1:3306"
DB_NAME = "flask_admin"

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
