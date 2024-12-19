import sqlite3
from werkzeug.security import generate_password_hash

# con = sqlite3.connect("../instance/database.db")
con = sqlite3.connect("instance/database.db")
cur = con.cursor()

users = [
    (
        1,
        "iliangchu@gmail.com",
        "褚翊喨",
        generate_password_hash("123456"),
    ),
]
cur.executemany(
    "INSERT INTO users VALUES(?, ?, ?, ?)", users
)
con.commit()
