import math
import mmh3
import logging
from bitarray import bitarray

logging.basicConfig(filename='test.log',level=logging.DEBUG)

class BloomFilter:
    
    # Restricting public access to class variables
    _capacity = 0
    _error_rate = None
    _bitarray = None
    
    def __init__(self, capacity, error_rate):
        
        
        if not (0 < error_rate < 1):
            raise ValueError("Error_rate must be between 0 and 1.")
        if not capacity > 1:
            raiseValueError("Capacity must be > 0")
            
        '''
        k --> num_slices
        m --> bits_per_slice
        M --> m * k
        '''
        num_slices = int(math.ceil(math.log(1.0 / error_rate, 2)))
        bits_per_slice = int(math.ceil(
            (capacity * abs(math.log(error_rate))) /
            (num_slices * (math.log(2) ** 2))))
        
        self.setter(error_rate, capacity, num_slices, bits_per_slice, 0)
        
        
        self._bitarray = bitarray(self._num_bits, endian='little')
        self._bitarray.setall(False)
        
    @property
    def capacity(self):
        '''
        This is the maximum number of insertions in the filter.
        Alternatively, it's the number of elements to store
        '''
        return self._capacity
    
    @property
    def item_count():
        '''
        This is the current number of items stored in the filter.
        '''
        return self._item_count
        
    def setter(self, error_rate, capacity, num_slices, bits_per_slice,count):
        self._error_rate = error_rate
        self._capacity = capacity
        self._num_slices = num_slices
        self._bits_per_slice = bits_per_slice
        self._num_bits = num_slices * bits_per_slice
        self._item_count = count
        
        
    def hash_generator(self, item):
        
        hashes = []
        for i in range(self._num_slices):
            
            # Digest for given item using 'i' as the seed
            digest = mmh3.hash(item, i) % self._bits_per_slice
            hashes.append(digest)
            
        return hashes
        
        
            
    def add(self, item):
        
        '''
        Adds an item to this bloom filter.
        Return: True if item added successfully, else False
        '''
        
        bitarr = self._bitarray
        bits_per_slice = self._bits_per_slice
        hashes = self.hash_generator(item)
        
        if self._item_count > self._capacity:
            raise IndexError("BloomFilter has exceeded capacity")
            
        offset = 0
        found_all_bits = True
        for hsh in hashes:
            if found_all_bits and not bitarr[offset + hsh]:
                found_all_bits = False
            
            self._bitarray[offset+hsh] = True
            offset += bits_per_slice
            
        if not found_all_bits:
            self._item_count += 1
            return True
        
        else: 
            logging.debug("Item--->{0} already existed or witnessed collisions with previous bit setting".format(item))
            return False
        
    def __contains__(self, item):
        
        '''
        Verifying an item's existence in the bloom filter
        Usage: "amartya" in b
        '''
        bits_per_slice = self._bits_per_slice
        bitarray = self._bitarray
        hashes = self.hash_generator(item)
        offset = 0
        for hsh in hashes:
            if not bitarray[offset + hsh]:
                return False
            offset += bits_per_slice
        return True
        
        
        