#this file keeps the bot alive
from flask import Flask #using flask as the web server
from threading import Thread #runs on different thread from bot


app = Flask('')

@app.route('/')
def home():
  return "Hello, I am awake." #returns this message upon visiting the server

def run():
  app.run(host = '0.0.0.0', port = 8080)

def keep_alive():
  t = Thread(target=run)
  t.start()