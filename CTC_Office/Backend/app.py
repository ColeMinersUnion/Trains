from flask import Flask, request, jsonify
from flask_cors import CORS
from CTC import CTC_Office
from werkzeug.utils import secure_filename
import os

#*API CONFIG --
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'xlxs', 'csv', 'json'}
api = Flask(__name__)
cors = CORS(api, resources={r"/api": {"origins":"*"}})
api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#*--

#*Used for checking whether the file could be malicious
#*Taken from FLASK API documentation. 
#https://flask.palletsprojects.com/en/stable/patterns/fileuploads/#a-gentle-introduction
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    return jsonify({"blocks":maintenance}), 200

@api.route('api/schedule/file', methods=['GET', 'POST'])
def ScheduleFile():
    if 'file' not in request.files:
        return jsonify({"Status":"No file submitted"}), 400
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(api.config['UPLOAD_FOLDER'], filename))
        Office.uploadSchedule(filename)
        return jsonify({"Status":"Schedule Uploaded"}), 200
    else:
        return jsonify({"Status":"Schedule Failed"}), 500



if(__name__ == '__main__'):
    api.run(host="0.0.0.0", port=8000)