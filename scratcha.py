import os
from replit import db
from datetime import datetime
import scratchattach as scratch3
import requests
import random as r
#import uuid
#https://xnw7rh.deta.dev/get/
#import proxy

session_id = os.environ['session_id']
session = scratch3.Session(session_id, username="Knightbot63")
project_id = "790734555"
#project = scratch3.get_project(project_id)
conn = session.connect_cloud(project_id)
client = scratch3.CloudRequests(conn)
print("Working.")

#latestcomment = project.comments(limit=1, offset=0)
#print(latestcomment)

# list of people with admin (Max 5)
admin = []
CatBits_Team = ["Knightbot63", "ethernetexplorer", "Wolfieboy09"]

# Deprecated
bannedusers = [""]


# INTERNAL FUNCTION - This is not a request handler.
def ban_check(username):
  with open('banned.txt') as f:
    data = f.read()
    for item in data:
      if username in item:
        return True
      else:
        return None  # Don't change


def follower_count(self):
  text = requests.get(
    f"https://xnw7rh.deta.dev/get/https://scratch.mit.edu/users/{self}/followers/"
  ).text
  text = text.split("Followers (")[1]
  text = text.split(")")[0]
  return int(text)


def log(message):
  print(message)
  with open("log.txt", "a") as file:
    file.write("\n" + message)


# Returns if user is admin or not
@client.request
def isadmin(user):
  if user in admin:
    return "USER_IS_ADMIN"
  elif user in CatBits_Team:
    return "USER_IS_CATBITS_TEAM"
  else:
    return "USER_NOT_ADMIN"


#Returns if the user is banned


@client.request
def profile(user):
  requester = client.get_requester()
  keys = db.keys()
  log(f"Getting Profile: User: {user} | From: {requester}")
  if user in keys:
    count = follower_count(user)
    userbits = db[user]
    c = ["SEARCHING: " + user]
    c.append(f"Username: {user}")
    c.append(f"CatBit amount: {userbits}")
    c.append(f"Is admin: {user in admin}")
    c.append(f"Is CatBits Team: {user in CatBits_Team}")
    c.append(f"Follower Count (Scratch): {count}")
    return c
  else:
    return [
      "SEARCHING: " + user,
      "The profile you searched has not made an account.",
      "NOTE: search is case sensitive!"
    ]


# Sample request
@client.request
def ping():
  print("Ping request received")
  return "pong"


# Returns users balance
@client.request
def load(username):
  with open('banned.txt') as f:
    data = f.read()
    for item in data:
      if username in item:
        unformatted_ban_data = item.strip()
        ban_data = unformatted_ban_data.split(";")
    if 'ban_data' in locals() and username in ban_data:
      banned = []
      banned.append("Account Blocked")
      banned.append(f"Your account @{username} is banned!")
      banned.append(f"Moderator note: {ban_data[1]}")
      banned.append("If you think this is a mistake, contact @Knightbot63")
      return banned
    else:
      now = datetime.now()
      current_time = now.strftime("%H:%M:%S")
      keys = db.keys()
    if username in keys:
      log(f"Balance requested for '{username}'. Returning {db[username]}. " +
          current_time)
      return db[username]
    else:
      log("New user. Creating account...")
      db[username] = "250"
      log(f"Balance requested for '{username}'. Returning {db[username]}. " +
          current_time)
      return db[username]


# Send catbits
@client.request
def send(recipent, amount):
  if not ban_check(recipent) == None and ban_check(recipent):
    return "NOT_EXIST"
  requester = client.get_requester()
  log(f"SEND Requester: {requester} | Recipent: {recipent} | Amount: {amount}")
  keys = db.keys()
  if recipent in keys:
    if int(db[requester]) < int(amount):
      return "NOT_ENOUGH"
    else:
      reqBal = int(db[requester])
      recBal = int(db[recipent])
      reqBal -= int(amount)
      recBal += int(amount)
      db[requester] = reqBal
      db[recipent] = recBal
      return "SUCCESS"
  else:
    return "NOT_EXIST"


# Sample request
@client.request
def set(user, balance):
  requester = client.get_requester()
  log(f"{requester} set {user}'s balance to {balance} CatBits")
  keys = db.keys()
  if user in keys:
    db[user] = balance
    return "SUCCESS"
  else:
    return "NOT_EXIST"


# Search is now Profile since the 2.0.0 Update of CatBits
# Deprecated
@client.request
def search(user):
  keys = db.keys()
  if user in keys and not keys == '':
    requester = client.get_requester()
    log(f"{requester} is searching {user}'s CatBits.")
    return db[user]
  else:
    return 0


@client.request
def ban_user(user, reason):
  log(f"A CatBits Member is banning {user}! Check the banned.txt log.")
  with open("banned.txt", "a") as file:
    file.write('\n' + user + ';' + reason)
    return "Might've banned user."


@client.request  # am working on
def leaderboard():
  print("loading...")
  keys = db.keys()
  print(keys)
  return f"User:", min(keys)


@client.event
def on_ready():
  os.system("clear")
  log("\nRequest handler is running")


def start():
  client.run()
