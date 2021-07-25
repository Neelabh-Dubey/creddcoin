# -*- coding: utf-8 -*-
"""
Created on Fri Jul  9 18:04:57 2021

To be installed:
Flask: pip install Flask
Postman HTTP Client: https://www.getpostman.com/
Project created using spyder(Anaconda)

@author: Neelabh
"""

#importing libraries

import datetime
import hashlib
import json
from flask import Flask, jsonify

#building blockchain

class Blockchain:
    
    #initialising blockchain
    
    def __init__(self):
        self.chain = []  #list for cryptographic links between blocks
        self.create_block(proof = 1, prev_hash = '0') #creating genesis block
        
    #function for creating new block
        
    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prev_hash': prev_hash}
                 #'data': 'some data' can be added as field
        self.chain.append(block)
        return block
    
    #function for getting previous block
    
    def get_prev_block(self):
        return self.chain[-1]
    
    #function for proof of work
    
    def proof_of_work(self, prev_proof):
        new_proof=1 #initialise new_proof to 1 to explore hash pool
        check_proof=False
        while check_proof is False:
            #let say target start with 4 leading zeros
            #hash function should be not be symmetric like a+b is symmetric function
            hash_code=hashlib.sha256(str(new_proof**2-prev_proof**2).encode()).hexdigest()
            if hash_code[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    #function to generate hash for blocks
    
    def generate_hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    #check chain is valid
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_idx = 1
        while block_idx < len(chain):
            curr_block = chain[block_idx]
            if curr_block['prev_hash'] != self.generate_hash(previous_block):
                return False
            curr_proof = curr_block['proof']
            prev_proof = previous_block['proof']
            hash_code = hashlib.sha256(str(curr_proof**2 - prev_proof**2).encode()).hexdigest()
            if hash_code[:4] != '0000':
                return False
            previous_block = curr_block
            block_idx +=1
        return True
    
    #creating web app for our blockchain
    
app = Flask(__name__)
    
    #creating blockchain instance
blockchain = Blockchain()
    
    #mining block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    prev_block  = blockchain.get_prev_block()
    prev_proof  = prev_block['proof']
    proof = blockchain.proof_of_work(prev_proof)
    prev_hash = blockchain.generate_hash(prev_block)
    block = blockchain.create_block(proof,prev_hash)
    response = {'message': 'Congrats u digged it',
               'index': block['index'],
               'timestamp': block['timestamp'],
               'proof': block['proof'],
               'prev_hash': block['prev_hash']
               }
    return jsonify(response), 200


#get entire blockchain

@app.route('/get_blockchain', methods = ['GET'])
def get_blockchain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

#chain is valid

@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good, blockchain is good'}
    else:
        response = {'message': 'Problem...panic...'}
    return jsonify(response), 200
#run the app
app.run(host = '0.0.0.0', port = '5000')
    
        
        
    