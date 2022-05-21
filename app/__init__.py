# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Import core packages
import os

# Import Flask 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate    import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Inject Flask magic
app = Flask(__name__)

# Load configuration
app.config.from_object('app.config.Config')

# Construct the DB Object (SQLAlchemy interface)
db = SQLAlchemy (app)
login_manager = LoginManager()
bcrypt =  Bcrypt()

# Enabel migration for our application
login_manager.init_app(app)
bcrypt.init_app(app)
Migrate(app, db)

# Import routing to render the pages
from app import views, models



login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
