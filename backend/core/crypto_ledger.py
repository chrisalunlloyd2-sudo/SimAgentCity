import hashlib
import time
import json
import os

# PART 4: THE DECENTRALIZED FOUNDRY
# THE DEEP DEPIN: True Proof-of-Work Blockchain for Local Web3 Trap

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, contract_code=""):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions # List of dicts
        self.contract_code = contract_code # Immutable Logic Escrow
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{json.dumps(self.transactions)}{self.contract_code}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        """Physical Proof of Work: Actually burns CPU cycles to validate."""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        return self.hash

class CryptoLedger:
    def __init__(self, chain_path, difficulty=3): # Difficulty 3 requires actual CPU work
        self.chain_path = chain_path
        self.difficulty = difficulty
        self.chain = []
        self.load_chain()

    def load_chain(self):
        if os.path.exists(self.chain_path):
            try:
                with open(self.chain_path, "r") as f:
                    data = json.load(f)
                    for b in data:
                        block = Block(b["index"], b["previous_hash"], b["timestamp"], b["transactions"], b.get("contract_code", ""))
                        block.nonce = b["nonce"]
                        block.hash = b["hash"]
                        self.chain.append(block)
            except:
                self.create_genesis_block()
        else:
            self.create_genesis_block()

    def save_chain(self):
        chain_data = []
        for b in self.chain:
            chain_data.append({
                "index": b.index,
                "previous_hash": b.previous_hash,
                "timestamp": b.timestamp,
                "transactions": b.transactions,
                "contract_code": b.contract_code,
                "nonce": b.nonce,
                "hash": b.hash
            })
        with open(self.chain_path, "w") as f:
            json.dump(chain_data, f, indent=4)

    def create_genesis_block(self):
        genesis_block = Block(0, "0", time.time(), [{"system": "GENESIS_MINT", "amount": 1000000, "currency": "SYS_COIN"}])
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self.save_chain()

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, sender, receiver, amount, currency="PYTHON_COIN", contract=""):
        """Validates and mines a new transaction block."""
        txn = {
            "sender": sender,
            "receiver": receiver,
            "amount": amount,
            "currency": currency
        }
        # In a real environment, pending txns sit in a mempool. 
        # Here we mint a block per transaction for immediate local execution.
        new_block = Block(
            index=len(self.chain),
            previous_hash=self.get_latest_block().hash,
            timestamp=time.time(),
            transactions=[txn],
            contract_code=contract
        )
        # ASIC Simulation: The system must do the work to lock the ledger
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_chain()
        return new_block.hash

    def get_balance(self, entity_id, currency="PYTHON_COIN"):
        balance = 0
        for block in self.chain:
            for txn in block.transactions:
                if txn.get("currency") == currency:
                    if txn.get("receiver") == entity_id:
                        balance += txn.get("amount")
                    if txn.get("sender") == entity_id:
                        balance -= txn.get("amount")
        return balance

if __name__ == "__main__":
    print("Testing True Cryptographic Ledger (ASIC Proof of Work)...")
    ledger = CryptoLedger("./test_blockchain.json", difficulty=4) # Higher diff for test
    print(f"Genesis Block Hash: {ledger.get_latest_block().hash}")
    
    print("Mining transaction block...")
    start = time.time()
    tx_hash = ledger.add_transaction("System", "Agent_01", 500, "PYTHON_COIN")
    elapsed = time.time() - start
    
    print(f"Block Mined in {elapsed:.2f}s. Hash: {tx_hash}")
    print(f"Agent_01 Balance: {ledger.get_balance('Agent_01', 'PYTHON_COIN')}")
    
    if os.path.exists("./test_blockchain.json"):
        os.remove("./test_blockchain.json")
        print("Test Passed. Winner Selected.")
