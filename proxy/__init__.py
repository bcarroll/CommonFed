import logging
from flask import Flask
from flask import Markup
from flask import render_template
from flask import redirect

from flask_login import LoginManager
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from urllib.parse import quote_plus, unquote

from os import urandom, environ
from os.path import abspath, join, dirname

from proxy.lib.Configuration import get_config

basedir = abspath(dirname(__file__))
dbdir = abspath(join(basedir, 'db'))

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
if app.config['DEBUG']:
    app.config['SECRET_KEY'] = 'DEBUGGING'
else:
    app.config['SECRET_KEY'] = urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbdir + 'data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CONFIG'] = get_config()

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.session_protection = "strong"
login_manager.login_message_category = "info"
login_manager.login_view = "admin_login"

@app.route('/')
def index():
    """Default landing page"""
    return render_template('index.html', html_title='INDEX')

@app.route('/favicon.ico')
def favicon():
    """favicon.ico locator"""
    return redirect('/static/favicon.ico')

# Import views
import proxy.views.admin
import proxy.views.errors
import proxy.views.admin.certstore
import proxy.views.admin.saml_service_provider
import proxy.views.admin.saml_identity_provider

# Import database models
from proxy.models.Administrator import Administrator
from proxy.models.CertStore import CertStore
from proxy.models.ServiceProvider import ServiceProvider
from proxy.models.IdentityProvider import IdentityProvider

import proxy.cli.Admin
import proxy.cli.ServiceProvider
