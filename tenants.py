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
COLLECTION = "Tenants"

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

    if st.button("Search"):
        # Embed the input text
        input_vector = embeddings.embed_query(query)
        # print("input_vector", input_vector)

        # Query the MongoDB Atlas vector search database
        results = list(db.tenants.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "billingAaddress_embedding",
                    "queryVector": input_vector,
                    "numCandidates": 50,
                    "limit": 1
                }
            }
        ]))
        # print("result", results)

        # Display results
        for doc in results:
            billingAaddress= doc.get("billingAaddress")
            st.write("BillingAaddress is:",billingAaddress)
            # billing_address = doc.get("billingAaddress")
            # website = doc.get("website")
            # status = doc .get("status")
            # memberships=doc.get("memberships")
            # dataStartDate=doc.get("dataStartDate")
            # companyType=doc.get("companyType")
            # if billing_address is not None:
            #     st.write("Billing Address:", billing_address)
            # if website is not None:
            #     st.write("Website is:", website)
            # if status is not None:
            #     st.write("staus is:",status)
            # if website is not None:
            #     st.write ("Membership is:",memberships)
            # if website is not None:
            #     st.write("DataStartDate is:",dataStartDate)
            # if companyType is not None:
            #     st.write("companyType is:",companyType)
                


if __name__ == "__main__":
    main()