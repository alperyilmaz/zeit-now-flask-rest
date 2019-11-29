# index.py
# original template from https://camillovisini.com/barebone-serverless-flask-rest-api-on-zeit-now/
# modifications from https://stackoverflow.com/a/51385027
from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app,
          version='0.1',
          title='Our sample API',
          description='This is our sample API'
)

@api.route('/hello_world')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/isPrime/<number>')
class isPrime(Resource):
    def get(self, number):
        number=int(number)
        return number > 1 and all(number % i for i in range(2, int(number**0.5) + 1))
 
if __name__ == '__main__':
    app.run(debug=False)

