from website import session

needToRecompute = True


def recompute():
    global cachedDBData, nextUserId, needToRecompute
    cachedDBData = [
        row
        for row in session.execute(
            "SELECT id, username, password, misc FROM keyspace1.data;"
        )
    ]
    for row in cachedDBData:
        print(row)
    nextUserId = 1 + max([row.id for row in cachedDBData]) if cachedDBData else 1
    needToRecompute = False


def getDBData():
    global cachedDBData, nextUserId, needToRecompute
    if needToRecompute:
        recompute()
    return cachedDBData


def addUser(username, password):
    global needToRecompute
    session.execute(
        """
    INSERT INTO keyspace1.data (id, username, password, misc)
    VALUES (%s, %s, %s, %s)
    """,
        (nextUserId, username, password, "{}"),
    )
    needToRecompute = True


def updateMisc(user_id, misc):
    global needToRecompute
    session.execute(
        "UPDATE keyspace1.data SET misc = %s WHERE id = %s",
        (misc, user_id),
    )
    needToRecompute = True
