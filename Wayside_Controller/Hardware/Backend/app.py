from flask import Flask, request, jsonify
from WaysideHardwareShell import WaysideShell

app = Flask(__name__)
wayside = WaysideShell()
#http://localhost:8000/block/maintenance 
@app.route('/block/maintenance', methods=['POST'])
def maintain(): 
    try:
        blocks = request.json['blocks']
        list_of_blocks = blocks.values()
        wayside.maintenance_blocks(list_of_blocks)
        return jsonify({'message': 'Maintenance blocks updated'}), 200
    except:
        return jsonify({'error': 'Internal Server Error'}), 500
    
@app.route('/block/signals', methods=['GET'])
def get_signals():
    return jsonify(wayside.get_blocks()), 200