from bloom import BloomFilter
from pymongo import MongoClient

def main():
    print("Hello!")
    client = MongoClient("mongodb+srv://amartya:blistering_barnacles@theghostempire-ozfmw.mongodb.net/test?retryWrites=true&w=majority")

    bloom_test = BloomFilter(20, 0.02)
    bloom_test.add("basu")
    bloom_test.add("basu")
    if "basu" in bloom_test:
        print("Object exists")
    else:
        print("The searched item does NOT exist in the cache. Read from persistent datastore")


if __name__ == "__main__":
    main()