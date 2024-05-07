import streamlit as st
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
import os
import openai

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Set up MongoDB connection
MONGO_URL = "mongodb+srv://ajith63073:zBtqgjXMPwU27XHA@vectordb.udkncxz.mongodb.net/"
MONGO_DBNAME = "sample_mflix"
COLLECTION = "Cities"

client = MongoClient(MONGO_URL)
db = client[MONGO_DBNAME]
vec_collection = db[COLLECTION]

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Define Streamlit app
def main():
    st.title("Vector Search App")

    # User input for query
    query = st.text_input("Enter your query:")
    print("Query_vector----->",query)

    if st.button("Search"):
        # Embed the input text
        input_vector = embeddings.embed_query(query)
        print("input_vector", input_vector)

        # Query the MongoDB Atlas vector search database
        results = (db.Cities.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "stateName_Embedding",
                    "queryVector": input_vector,
                    "numCandidates": 50,
                    "limit": 1
                },
            }
        ]))
        print("result", results)

        # Display results
        for doc in results:
            if doc.get("state") is not None:
                st.write("Response:", doc.get("state"))

if __name__ == "__main__":
    main()