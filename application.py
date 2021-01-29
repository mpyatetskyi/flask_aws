from flask import Flask

application = Flask(__name__)

@application.route('/')

def hello_world():
    return 'Hello to everyone. This is my monthly review'

if __name__ == '__main__':
    application.run(debug=True)