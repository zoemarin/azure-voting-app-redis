from flask import Flask, request, render_template
import os
import random
import redis
import socket
import sys

app = Flask(__name__)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

if ("TITLE" in os.environ and os.environ['TITLE']):
    title = os.environ['TITLE']
else:
    title = app.config['TITLE']

if ("TPARAGRAPH1" in os.environ and os.environ['PARAGRAPH1']):
    paragraph = os.environ['PARAGRAPH1']
else:
    paragraph = app.config['PARAGRAPH1']

# Redis configurations
redis_server = os.environ['REDIS']

# Redis Connection
try:
    if "REDIS_PWD" in os.environ:
        r = redis.StrictRedis(host=redis_server,
                        port=6379,
                        password=os.environ['REDIS_PWD'])
    else:
        r = redis.Redis(redis_server)
    r.ping()
except redis.ConnectionError:
    exit('Failed to connect to Redis, terminating.')

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Init Redis

@app.route('/', methods=['GET', 'POST'])
def index():
    # Get current values
    # Return index with values
    return render_template("index.html",paragraph=paragraph, title=title)

if __name__ == "__main__":
    app.run()
