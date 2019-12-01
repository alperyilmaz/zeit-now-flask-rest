# index.py
# original template from https://camillovisini.com/barebone-serverless-flask-rest-api-on-zeit-now/
# modifications from https://stackoverflow.com/a/51385027
from flask import Flask, request, send_file, Response, make_response
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

@api.route('/isPrime/<int:number>')
class isPrime(Resource):
    def get(self, number):
        #number=int(number)
        return number > 1 and all(number % i for i in range(2, int(number**0.5) + 1))

@api.route('/chaos/<int:number>')
class chaos(Resource):
    def get(self, number):
        import random
        import matplotlib.pyplot as plt
        from io import BytesIO
        from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
        from matplotlib.figure import Figure 

        def move_point(point,vertex):
            x=(point[0]+vertex[0])/2
            y=(point[1]+vertex[1])/2
            return (x,y)

        def nocache(response):
            """Add Cache-Control headers to disable caching a response"""
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            return response


        scaling=5
        # vertex={'A':(0.5,1), 'B':(0,0), 'C':(1,0)}
        vertex=[(0.5*scaling,0.86*scaling),(0,0),(1*scaling,0)]
        x=[]
        y=[]

        point=[0.5,0.3]
        x.append(point[0])
        y.append(point[1])

        for i in range(20000):
            random_index = random.randrange(0, 3)
            point=move_point(point,vertex[random_index])
            x.append(point[0])
            y.append(point[1])
        # taken from https://stackoverflow.com/q/50355293
        # applied the change in https://stackoverflow.com/a/50423300
        fig = Figure()
        plt.figure(1)
        #plt.figure(figsize=(20,20))
        plt.scatter(x,y,s=0.4)
        plt.scatter(*zip(*vertex), c='black')
        canvas = FigureCanvas(plt.figure(1)) 
        img_bytes = BytesIO()
        canvas.print_png(img_bytes)
        #plt.savefig(img_bytes)
        #img_bytes.seek(0)
        #return nocache(send_file(img_bytes, mimetype='image/png'))
        response = make_response(img_bytes.getvalue())
        response.mimetype = 'image/png'
        print(response)
        return response


if __name__ == '__main__':
    app.run(debug=True)

