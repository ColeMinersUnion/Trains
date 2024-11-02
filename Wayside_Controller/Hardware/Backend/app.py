from flask import Flask, request, jsonify
from flask_cors import CORS
from WaysideHardwareShell import WaysideShell

app = Flask(__name__)
wayside = WaysideShell()

#CTC -> Wayside Methods
#http://localhost:8000/block/maintenance 
@app.route('/block/maintenance', methods=['POST'])
def maintain(): 
    try:
        blocks = request.json
        print(blocks['blocks'])

        #TODO: Call Shell Maintenence Function

        return jsonify({'message': 'Maintenance blocks updated'}), 200
    except:
        return jsonify({'error': 'Internal Server Error'}), 500
    

#http://localhost:8000/block/dispatch
@app.route('/dispatch' , methods=['POST'])
def dispatch():
    try:
        dispatch = request.json
        print(dispatch['dispatch'])
        #TODO: Call Shell Dispatch Function
    except:
        return jsonify({'error': 'Internal Server Error'}), 500
    

#http://localhost:8000/block/occupancy
@app.route('/block/occupancy', methods=['POST'])
def occupancies():
    try:
        blocks = request.json
        print(blocks['blocks'])
        wayside.update(blocks)
        return jsonify({'message': 'Block occupancy updated'}), 200
    except:
        return jsonify({'error': 'Internal Server Error'}), 500




if (__name__ == '__main__'):
    app.run(host = "0.0.0.0", port=8000)