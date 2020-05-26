import sys
import os
import random
from pymongo import MongoClient
import string

def main():
    print("Performance Benchmarking!")
    
    try:
        client = MongoClient("mongodb+srv://amartya:amartya@theghostempire-ozfmw.mongodb.net/test?retryWrites=true&w=majority")
    except ConnectionError:
        print("Server not available")
    
    db = client.get_database("test")
    coll = db.get_collection("bloom_users")
    
    f = open("usernames.txt", 'a+')
    letters = string.ascii_lowercase

    R = random.choice([1, 2, 3])

    for i in range(200):
        f.write(''.join(random.choice(letters) for i in range(10)))
        f.write('\n')

        mydict = { "name": ''.join(random.choice(letters) for i in range(10)) }
        x = coll.insert_one(mydict)
        print("Inserted:", x.inserted_id)

    


    
    #bloom_test = BloomFilter(20, 0.02)
    #bloom_test.add("basu")
    #bloom_test.add("basu")
    #if "basu" in bloom_test:
    #    print("Object exists")
    #else:
    #    print("The searched item does NOT exist in the cache. Read from persistent datastore")


if __name__ == "__main__":
    main()