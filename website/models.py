from website import login_manager, session
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    users = session.execute("SELECT id, username, password FROM keyspace1.data;")
    if users:
        for row in users:
            if str(row.id) == user_id:
                return User(user_id)
    return None


class User(UserMixin):
    def __init__(self, userId):
        self.id = userId
