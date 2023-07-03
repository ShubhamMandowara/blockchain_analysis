import hashlib
import json
import sqlite3
from typing import Dict
import time
from pydantic import BaseModel


class Block:
    def __init__(self, index: int, timestamp: int, data: Dict, previous_hash: str):
        """Initialize the block
        Args:
            index (int): Index no.
            timestamp (int): timestamp
            data (Dict): data
            previous_hash (str): previous hash
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Function to calculate hash no. of present block
        Returns:
        """
        data_string = str(self.index) + str(self.timestamp) + json.dumps(self.data) + self.previous_hash
        return hashlib.sha3_256(data_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        """Function to create a new block
        Returns:

        """
        return Block(index=0, timestamp=int(time.time()), data={"start": "Genesis Block"}, previous_hash="0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block: Block):
        if self.is_chain_valid():
            new_block.previous_hash = self.get_latest_block().hash
            new_block.hash = new_block.calculate_hash()
            self.chain.append(new_block)
        else:
            print('An error in chain')

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True


class TransactionModel(BaseModel):  # pydantic to check type
    sender: str
    recipient: str
    amount: float

if __name__ == '__main__':
    from flask import Flask, render_template, request
    import plotly.express as px
    import pandas as pd

    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    conn = sqlite3.connect('blockchain.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions 
                 (sender text, recipient text, amount real)''')
    blockchain = Blockchain()
    c.close()


    @app.route('/add_transaction', methods=['POST'])
    def add_transaction():
        with sqlite3.connect("blockchain.db") as con:
            local_c = con.cursor()
            data = request.get_json()
            transaction = TransactionModel(**data)
            local_c.execute("INSERT INTO transactions VALUES (?, ?, ?)",
                            (transaction.sender, transaction.recipient, transaction.amount))
            con.commit()
        return 'Transaction added successfully'


    @app.route('/dashboard')
    def dashboard():
        with sqlite3.connect("blockchain.db") as con:
            local_c = con.cursor()
            local_c.execute("SELECT * FROM transactions")
            transactions = local_c.fetchall()
            df = pd.DataFrame(transactions, columns=['sender', 'recipient', 'amount'])
            fig = px.bar(df, x='sender', y='amount', color='recipient', barmode='stack')
            return render_template('dashboard.html', plot=fig.to_html())


    app.run()
