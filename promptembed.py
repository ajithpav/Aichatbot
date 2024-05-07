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
COLLECTION ="prompts"

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DBNAME]
vec_collection = db[COLLECTION]

# Load JSON data from the file ViewBaseMetricsMarketingQuarterly
with open('/home/guest/polaris-dev.Promptss.json', 'r') as f:
    data = json.load(f)

# Embed the input text and store the vectors in the MongoDB database
for item in data:
    # Check if both 'Response' and 'prompt' keys exist in the dictionary
    if 'Resopnse' in item and 'prompt' in item:
        response_name = item['Resopnse']
        prompt_text = item['prompt']
        response_embedding = embeddings.embed_query(response_name)
        prompt_embedding = embeddings.embed_query(prompt_text)

        # Insert a new document with both embeddings
        vec_collection.insert_one({
            "Resopnse": response_name,
            "prompt": prompt_text,
            "Response_embedding": response_embedding,
            "prompt_embedding": prompt_embedding
        })
    else:
        print(f"Either 'Resopnse' or 'prompt' key not found in item: {item}")