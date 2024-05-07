import os
import json
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
import openai
import pymongo
import pandas as pd

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Connect to MongoDB Atlas
MONGO_URL="mongodb+srv://ajith63073:zBtqgjXMPwU27XHA@vectordb.udkncxz.mongodb.net/"
MONGO_DBNAME = "sample_mflix"
COLLECTION ="tenants"

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DBNAME]
vec_collection = db[COLLECTION]

# Load JSON data from the file ViewBaseMetricsMarketingQuarterly
with open('/home/guest/polaris-dev.Tenants.json', 'r') as f:
    data = json.load(f)
    file= str(data)

# Embed the input text and store the vectors in the MongoDB database
for item in file:
    # Check if both 'Response' and 'prompt' keys exist in the dictionary
    if 'name' and 'shortName' and 'industryIds' in item  :
        dataSourceName_name = item['name']
        platform_text = item['shortName']
        industryIds_text=item['industryIds']
        Dtaname_embedding = embeddings.embed_query(dataSourceName_name)
        industri_embedding = embeddings.embed_query(platform_text)
        industryIds_embedding= embeddings.embed_query(industryIds_text)
        
        # Insert a new document with both embeddings
        vec_collection.insert_one({
            "dataSourceName": dataSourceName_name,
            "platform_text": platform_text,
            "industryIds_text":industryIds_text,
            "industryIds_text":industryIds_embedding,
            "name_embedding": Dtaname_embedding,
            "industri_embedding": industri_embedding

        

        })
    else:
        print(f"Either 'Resopnse' or 'prompt' key not found in item: {item}")