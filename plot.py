import streamlit as st
import bson
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
# from langchain_openai import OpenAIEmbeddings
import os
import openai

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Set up SentenceTransformer model
embedding_model = SentenceTransformer("thenlper/gte-large")

# Set up MongoDB connection
MONGO_URL = "mongodb+srv://ajith63073:zBtqgjXMPwU27XHA@vectordb.udkncxz.mongodb.net/"
MONGO_DBNAME = "sample_mflix"
COLLECTION = "prompt_collection"

client = MongoClient(MONGO_URL)
db = client[MONGO_DBNAME]
vec_collection = db[COLLECTION]

def main():
    # Streamlit title
    st.title("Vector Search App")

    # User input for query
    query = st.text_input("Enter your query:")

    # Search button
    if st.button("Search"):
        search_query(query)

def search_query(query):
    # Embed the input text
    input_vector = embedding_model.encode(query)
    input_vector_list = [float(x) for x in input_vector.tolist()]

    # Query the MongoDB Atlas vector search database
    results = db.prompt_collection.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "prompt_embeddings",
                "queryVector": input_vector_list,
                "numCandidates": 50,
                "limit": 1
            }
        }
    ])

    # Extract the most relevant answer from the results
    for doc in results:
         if doc.get("Resopnse") is not None:
                st.write("Response:", doc.get("Resopnse"))

if __name__ == "__main__":
    main()