from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from config import DBPass, DBUsername
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

app = Flask(__name__)
app.config["SECRET_KEY"] = "enterasecretkeyhere"

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

cloud_config = {"secure_connect_bundle": "secure-connect-tidyup.zip"}
auth_provider = PlainTextAuthProvider(DBUsername, DBPass)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

from website import routes


def startDebugServer(sharedQ):
    global discordQ
    discordQ = sharedQ
    app.run(debug=True)
