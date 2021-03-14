import json

from website import login_manager
from website.dbCache import getDBData, updateMisc
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    users = getDBData()
    if users:
        for row in users:
            if str(row.id) == user_id:
                return User(row)
    return None


class User(UserMixin):
    def __init__(self, row):
        self.id = row.id
        self.misc = json.loads(row.misc)

        for item in ["members", "tasks", "assignedTo", "discord"]:
            if item not in self.misc:
                self.misc[item] = []

    @property
    def members(self):
        return [(i + 1, member) for i, member in enumerate(self.misc["members"])]

    def addTask(self, stmt, to):
        self.misc["tasks"].append(stmt)
        self.misc["assignedTo"].append(to)
        updateMisc(self.id, json.dumps(self.misc))

        from website import discordQ

        discordQ.put((self.misc["discord"][to - 1], stmt))

    def addMember(self, name, discord):
        self.misc["members"].append(name)
        self.misc["discord"].append(discord)
        updateMisc(self.id, json.dumps(self.misc))

    def getTasks(self, memidx):
        return [
            (i, task)
            for i, task in enumerate(self.misc["tasks"])
            if self.misc["assignedTo"][i] == memidx
        ]
