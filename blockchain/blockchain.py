from hashlib import sha256
import time

class Block(object):
    def __init__(self, index, data, prev_hash=''):
        self.index = index
        self.data = data
        self.timestamp = time.time()
        self.prev_hash = prev_hash
        self.hash ='' 
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        d = {'index':self.index, 'data':self.data,
            'timestamp':self.timestamp, 'prev_hash':self.prev_hash,
            'nonce':self.nonce}
        string = str(d).encode()
        return sha256(string).hexdigest()

    def mine_block(self, difficulty):
        while (self.hash[:difficulty]!='0'*difficulty):
            self.nonce+=1
            self.hash = self.calculate_hash()

    def __str__(self):
        d = {'index':self.index, 'data':self.data,
            'timestamp':self.timestamp, 'prev_hash':self.prev_hash,
            'hash':self.hash, 'nonce':self.nonce}
        return str(d)

class Blockchain(object):
    def __init__(self, difficulty=2):
        self.chain = [self.create_genesis()]
        self.difficulty = difficulty

    def create_genesis(self):
        return Block(0,{'name':'Genesis'},'Genesis')

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self,block):
        block.prev_hash = self.get_last_block().hash
        block.mine_block(self.difficulty)
        self.chain.append(block)

    def is_valid_chain(self):
        for i in range(1,len(self.chain)):
            cur = self.chain[i]
            prev = self.chain[i-1]
            if (cur.hash != cur.calculate_hash()):
                print('Hash not calculated hash. Block {}'.format(cur.index))
                return False
            if (cur.hash[:self.difficulty]!='0'*self.difficulty):
                print('Hash without correct Proof of Work. Block {}'.format(cur.index))
                return False
            if (cur.prev_hash != prev.hash):
                print('Hash of previous block in block {} does not match'+
                        'previous block hash.'.format(cur.index))
                return False
        return True

    def blocks_to_string(self, sep='\n'):
        string = ''
        for block in self.chain:
            string+=block.__str__()+sep
        return string

def time_blockchains(diff_min=1, diff_max=5, blocks=10):
    chains = {}
    for diff in range(diff_min, diff_max+1):
        bc = Blockchain(diff)
        chains['diff'+str(diff)]={}
        times = []
        for i in range(blocks):
            start = time.time()
            bc.add_block(Block(i+1,'This is the {}thblock'.format(i+1),
                                bc.get_last_block().hash))
            times.append(time.time()-start)
        chains['diff'+str(diff)]['chain']=bc
        chains['diff'+str(diff)]['times']=times
    return chains
