from flask import Blueprint, jsonify, request
from app.blockchain import Blockchain

blockchain_blueprint = Blueprint('blockchain', __name__)
blockchain = Blockchain()

@blockchain_blueprint.route('/chain', methods=['GET'])
def get_chain():
    chain_data = [{
        "header": {
            "hash": block.hash,
            "prev_hash": block.prev_hash,
            "timestamp": block.timestamp
        },
        "body": {
            "hash": block.body_hash,
            "timestamp": block.timestamp,
            "sender": block.sender,
            "receiver": block.receiver,
            "data": block.data,
            "spam": block.spam
        }
    } for block in blockchain.chain]
    return jsonify({"chain": chain_data, "length": len(blockchain.chain)})

@blockchain_blueprint.route('/add_block', methods=['POST'])
def add_block():
    values = request.get_json()
    required_fields = ['sender', 'receiver', 'data', 'spam']
    if not all(field in values for field in required_fields):
        return 'Missing values', 400

    block = blockchain.add_block(values['sender'], values['receiver'], values['data'], values['spam'])
    return jsonify({"message": "Block added", "block": block.hash}), 201

@blockchain_blueprint.route('/validate', methods=['GET'])
def validate_chain():
    valid = blockchain.is_valid_chain()
    return jsonify({"valid": valid}), 200
