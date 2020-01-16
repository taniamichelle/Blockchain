# Paste your version of blockchain.py from the basic_block_gp
# folder here
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }

        # Reset the current list of transactions
        self.current_transactions = []
        # Append the chain to the block
        self.chain.append(block)
        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block
        :param block": <dict> Block
        "return": <str>
        """
        # CREATE the block_string
        string_object = json.dumps(block, sort_keys=True).encode()

        # HASH this string using sha256
        raw_hash = hashlib.sha256(string_object)

        hex_hash = raw_hash.hexdigest()

        # RETURN the hashed block string in hexadecimal format
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        guess = f"{block_string}{proof}".encode()
        # Hash + digest the guess
        guess_hash = hashlib.sha256(guess).hexdigest()

        # return True or False
        # Slice hash and check if first six nums are 0s
        return guess_hash[:6] == "000000"


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    # Pull the data out of the POST
    data = request.get_json()
    id = data['id']
    new_proof = data['proof']
    last_blockstring = json.dumps(block)
    # If proof and ID present:
    if new_proof in data and id in data:
        last_block = blockchain.last_block
        if blockchain.valid_proof() is True:
            # a valid proof should fail for all senders except the first.
            # Run the proof of work algorithm to get the next proof
        last_proof = blockchain.proof_of_work(
            last_blockstring, new_proof)
        # Forge the new Block by adding it to the chain with the proof
        previous_hash = blockchain.hash(last_blockstring)  # Get prev hash
        block = blockchain.new_block(new_proof, previous_hash)
        response = {
            'message': "Valid proof and id received.",
            'index': len(blockchain.chain) + 1,
            'timestamp': time(),
            'transactions': blockchain.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        # return jsonify(response="Valid proof and id received."), 200
    # If proof or ID not present:
    elif last_block_proof not in data or id not in data:
        return jsonify(response="Error: Please provide valid proof and id."), 400
    #     response = {400: "Error: Please provide valid proof and id."}
    # return jsonify(response)


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # Return the chain and its current length
        'length': len(blockchain.chain),
        'chain': blockchain.chain
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def get_last_block():
    response = {
        # Return the last block in the chain
        'get_last_block': blockchain.last_block
    }
    return jsonify(response), 200


# Run the program on port 5555
if __name__ == '__main__':
    # set debug to true to autosave so you do not need to restart server
    app.run(host='0.0.0.0', port=5555, debug=True)
