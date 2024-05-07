import streamlit as st
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
 
import os
import openai
 
# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"
 
# Set up MongoDB connection
MONGO_URL = "mongodb+srv://sriramg:Coc54694@cluster0.uwofdgc.mongodb.net/"
MONGO_DBNAME = "Vectorcollections"
COLLECTION = "datatest"
 
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
        results = list(db.datacollections.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "metrics_campaign",
                    "queryVector": input_vector,
                    "numCandidates": 50,
                    "limit": 1
                },
            }
        ]))
        print("result", results)
 
        # Display results
        for doc in results:
            
            accountName=doc.get("accountName")
            campaign=doc.get("campaign")
            noaaRegion=doc.get("noaaRegion")
            cost=doc.get("cost")
            campaignId=doc.get("campaignId")
            impressions=doc.get("impressions")
            Date=doc.get("date")
 
            # lists.append(accountName,campaign,noaaRegion,cost,campaignId,impressions,Date)

            st.write("Account Name:" , accountName),
            st.write("Campaign :" , campaign),
            st.write("NoaaRegion :" , noaaRegion),
            st.write("Cost :" , cost),
            st.write("campaignId:",campaignId),
            st.write("impressions:",impressions),
            st.write("Date:", Date)
 
 
 
 
if __name__ == "__main__":
    main()