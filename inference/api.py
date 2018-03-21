import os
from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from sklearn.externals import joblib

app = Flask(__name__)
api = Api(app)

class Prediction(Resource):
    def get(self):

        parser = reqparse.RequestParser()
        parser.add_argument('slength', type=float, help='slength cannot be converted')
        parser.add_argument('swidth', type=float, help='swidth cannot be converted')
        parser.add_argument('plength', type=float, help='plength cannot be converted')
        parser.add_argument('pwidth', type=float, help='pwidth cannot be converted')
        args = parser.parse_args()

        prediction = predict([[
                args['slength'], 
                args['swidth'], 
                args['plength'], 
                args['pwidth']
            ]])

        return {
                'slength': args['slength'],
                'swidth': args['swidth'],
                'plength': args['plength'],
                'pwidth': args['pwidth'],
                'species': prediction
               }

def predict(inputFeatures):
    mymodel = joblib.load(app.config.get('model_file'))
    prediction = mymodel.predict(inputFeatures)
    return prediction[0]

api.add_resource(Prediction, '/prediction')

if __name__ == '__main__':
    app.config['model_file'] = os.environ['MODEL_FILE']
    app.run(host='0.0.0.0', debug=False)
