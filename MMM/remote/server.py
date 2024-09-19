from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from jinja2.sandbox import SandboxedEnvironment
import os
import secrets

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per second", "3600 per hour"],
    storage_uri="memory://",
)
env = SandboxedEnvironment()

def mean(lst):
    return sum(lst) / len(lst)

def median(lst, high=True):
    lst.sort(key=lambda x: x if high else -x)
    return lst[len(lst)//2]

def mode(lst):
    return max(lst, key=lst.count)

env.filters['mean'] = mean
env.filters['median'] = median
env.filters['mode'] = mode

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/run', methods=['POST'])
def run():
    try:
        return env.from_string(request.form['template']).render()
    except Exception as e:
        return f'An error occurred! ({e.__class__.__name__})'

@app.route('/flag', methods=['POST'])
def flag():
    if secrets.compare_digest(request.form['key'], os.environ['KEY']):
        with open('flag.txt', 'r') as f:
            return f.read()
    else:
        return 'Invalid key'


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)

