import os
import json
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
import openai
import pymongo

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Connect to MongoDB Atlas
MONGO_URL="mongodb+srv://ajith63073:zBtqgjXMPwU27XHA@vectordb.udkncxz.mongodb.net/"
MONGO_DBNAME = "sample_mflix"
COLLECTION ="Cities"

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DBNAME]
vec_collection = db[COLLECTION]

def load_cities_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None

def embed_cities(cities_data):
    for item in cities_data:
        if all(key in item for key in ['city', 'stateName', 'countryName']):
            city = item['city']
            stateName = item['stateName']
            countryName = item['countryName']
            name_embedding = embeddings.embed_query(city)
            state_embedding = embeddings.embed_query(stateName)
            countryName_embedding = embeddings.embed_query(countryName)

            vec_collection.insert_many([{"city": city,"state":stateName,"countryName":countryName,"stateName_Embedding":state_embedding,"city_embedding": name_embedding,"countryName_Embeding":countryName_embedding}])
        else:
            print(f"Key 'city', 'stateName', or 'countryName' not found in item: {item}")

if __name__ == "__main__":
    cities_data = load_cities_data("/home/guest/polaris-dev.Cities.json")
    if cities_data:
        embed_cities(cities_data)