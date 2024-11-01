from flask import Flask, request, jsonify
from flask_cors import CORS
from CTC import CTC_Office

api = Flask(__name__)
cors = CORS(api, resources={r"/api": {"origins":"*"}})

Office = CTC_Office()
Office.addBlueLine()

@api.route('/api/addTrain', methods=['GET', 'POST'])
def addTrain():
    Station = request.json
    print(Station['Station'])
    #Office.addTrain([Station])
    return jsonify({"Status": "Success", "Data": Station}), 200

@api.route('/api/closeTrack', methods=["POST"])
def closeTrack():
    return jsonify({""})

@api.route('/api/blocks', methods=['GET'])
def block_maintenance():
    maintenance = []
    for i in Office.line.graph:
        if(i.closed):
            maintenance.append(True)
        else:
            maintenance.append(False)
    return {"blocks":maintenance}




if(__name__ == '__main__'):
    api.run(host="0.0.0.0", port=8000)