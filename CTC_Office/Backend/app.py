from flask import Flask, request
from flask_cors import CORS
from CTC import CTC_Office

api = Flask(__name__)
cors = CORS(api, resources={r"/api": {"origins":"*"}})

Office = CTC_Office
Office.addBlueLine()

@api.route('api/addTrain', ['GET', 'POST'])
def addTrain():
    Station = request.json['Station']
    Office.addTrain([Station])

