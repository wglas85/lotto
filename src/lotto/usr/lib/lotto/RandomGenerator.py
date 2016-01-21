'''
Created on 15.12.2015

@author: michi
'''

class RandomGenerator:
    def __init__(self):
        self.randomfp = open("/dev/urandom", 'rb')
        self.randomset = set()

    def nextNumber(self,maxValue):
        z = abs(int.from_bytes(self.randomfp.read(10),"big"))
        z = z % maxValue
        while z in self.randomset:
            z = abs(int.from_bytes(self.randomfp.read(10),"big"))
            z = z % maxValue
        self.randomset.add(z)
        return z
        
        
    def finalize(self):
        self.randomfp.close()
    def __del__(self):
        self.finalize()
