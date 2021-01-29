from flask import Flask

application = Flask(__name__)

@application.route('/')

def hello_world():
    return 'Hello to everybode. This is my first review'

if __name__ == '__main__':
    application.run(debug=True)