from flask import Flask, request, jsonify
from flask_cors import CORS
from CTC import CTC_Office

api = Flask(__name__)
cors = CORS(api, resources={r"/api": {"origins":"*"}})

Office = CTC_Office()
Office.addBlueLine()

@api.route('/api/addTrain', methods=['POST'])
def addTrain():
    Station = request.json['Station']
    Office.addTrain([Station])
    return 200, "Train has been added"

@api.route('/api/closeTrack', methods=["POST"])
def closeTrack():
    return jsonify({""})



if(__name__ == '__main__'):
    api.run(port=8000)