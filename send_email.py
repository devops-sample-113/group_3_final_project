import smtplib
from email.message import EmailMessage
from time import sleep
import sqlite3
from datetime import datetime

with open("confidential/password.txt") as f:
    password = f.read()

EMAIL_ADDRESS = "iliangchu@gmail.com"
EMAIL_PASSWORD = password

def send_email(To, content):
    msg = EmailMessage()
    msg['Subject'] = "message from group 3 final project"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = To

    msg.set_content(content)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def notify():
    con = sqlite3.connect("instance/database.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM event WHERE sent='0'")
    events = res.fetchall()
    print(events)
    for event in events:
        if datetime.strptime(event[4], '%Y-%m-%d %H:%M:%S') < datetime.now():
            send_email(event[1], event[2])
            cur.execute("UPDATE event SET sent = 1 WHERE event_id=?", (event[0], ))
    con.commit()


while True:
    notify()
    sleep(10)
