import streamlit as st
import openai
import pymongo
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
import os

# Set up OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

# Set up MongoDB connection
MONGO_URL = "mongodb+srv://ajith63073:zBtqgjXMPwU27XHA@vectordb.udkncxz.mongodb.net/"
MONGO_DBNAME = "sample_mflix"
COLLECTION = "city_embedded"

client = MongoClient(MONGO_URL)
db = client[MONGO_DBNAME]
collection = db[COLLECTION]

# Initialize SentenceTransformer embeddings
embeddings = SentenceTransformer("thenlper/gte-large")

# Create index for "prompt_embeddings"
# collection.create_index([("prompt_embeddings", "2dsphere")])

# Define Streamlit app
def main():
    st.title("Vector Search App")

    # User input for query
    user_input = st.text_input("Enter your query:")

    if st.button("Search"):
        if not user_input:
            st.write("Please enter a valid query.")
            return

        # Embed the input text
        input_vector = embeddings.encode(user_input).tolist()

        # Query the MongoDB Atlas vector search database
        results = db.prompt_collection.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "prompt_embeddings",
                    "queryVector": input_vector,
                    "numCandidates": 50,
                    "limit": 1
                }
            }
        ])

        # Display results

        for doc in results:
            if doc.get("Response") is not None:
                st.write("Response:", doc.get("Response"))

if __name__ == "__main__":
    main()