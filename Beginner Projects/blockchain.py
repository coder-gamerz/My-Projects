import hashlib as h

class Block:
    def __init__(self, previous_block_hash, transaction_list):
        self.previous_block_hash = previous_block_hash
        self.transaction_list = transaction_list

        self.block_data = "-".join(transaction_list) + "-" + previous_block_hash
        self.block_hash = h.sha256(self.block_data.encode()).hexdigest()

t1 = "Anna sends 2 doge to Mike"
t2 = "Charlie sends 2 doge to Mike"
t3 = "Anna sends 2 doge to Charlie"
t4 = "Anna sends 2 doge to Bob"
t5 = "Bob sends 2 doge to Anna"
t6 = "Mike sends 2 doge to Anna"

initial_block = Block("Initial String", [t1, t2])

print(initial_block.block_data)
print(initial_block.block_hash)

second_block = Block(initial_block.block_hash, [t3, t4])

print(initial_block.block_data)
print(initial_block.block_hash)

# A simple blockchain / hashing program with lots of doge
