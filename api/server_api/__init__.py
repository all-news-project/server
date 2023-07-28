import uuid

from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = str(uuid.uuid4())

from api.server_api import routes
