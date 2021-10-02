# __init__.py is a special Python file that allows a directory to become
# a Python package so it can be accessed using the 'import' statement.

from datetime import datetime
import os
import subprocess

""" from flask import Flask
from flask_script import Manager """
#import flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_mail import Mail
f""" rom flask_migrate import Migrate, MigrateCommand
from flask_user import UserManager
from flask_wtf.csrf import CSRFProtect
from flask import flash
import logging
import stripe
from flask_nav import Nav
from flask_nav.elements import *
from dtale.app import build_app
 """

#from nimbleAI import nimbleshared


# Instantiate Flask extensions
#csrf = CSRFProtect()
db = SQLAlchemy()
mail = Mail()
#migrate = Migrate()
#nav = Nav()


# Initialize Flask Application
def create_app(extra_config_settings={}):
    """Create a Flask application.
    """
    # Instantiate Flask
    app = Flask(__name__)

    db.init_app(app)


    # Setup Flask-Mail
    mail.init_app(app)

  
    # Setup an error-logger to send emails to app.config.ADMINS
    init_email_error_handler(app)

    # Setup Flask-User to handle user account related forms
    from .models.user_models import User
    from .views.main_views import user_profile_page



    version =  subprocess.check_output(["git", "describe"]).strip().decode()
    currentbranch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).strip().decode()
    last_tag_message = subprocess.check_output(["git", "show", "-s", "--format=%B"]).strip().decode()
    versioninfo = version + ' ' + currentbranch + ' | ' + last_tag_message


    @app.context_processor
    def context_processor():
        return dict(user_manager=user_manager)

    return app


def init_email_error_handler(app):
    """
    Initialize a logger to send emails on error-level messages.
    Unhandled exceptions will now send an email message to app.config.ADMINS.
    """
    #if app.debug: return  # Do not send error emails while developing

    # Retrieve email settings from app.config
    host = app.config['MAIL_SERVER']
    port = app.config['MAIL_PORT']
    from_addr = app.config['MAIL_DEFAULT_SENDER']
    username = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
