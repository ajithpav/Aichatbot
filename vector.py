from unittest import result
import streamlit as st
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
import os
import openai
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
import torch
 
# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"
 
# Set up MongoDB connection
MONGO_URL = "mongodb+srv://sriramg:Coc54694@cluster0.uwofdgc.mongodb.net/"
MONGO_DBNAME = "vectorcollections"
COLLECTION = "datatest"
 
client = MongoClient(MONGO_URL)
db = client[MONGO_DBNAME]
vec_collection = db[COLLECTION]
 
# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()
chatgpt=ChatOpenAI()
 
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
        result = list(db.datatest.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "metrics_campaign",
                    "queryVector": input_vector,
                    "numCandidates": 50,
                    "limit": 5
                },
            },
            {
                "$project":{
                    "embedding":0,
                    "_id":0,
                    "score":{
                        "$meta":"searchScore"
                    },
                }
               
            }
        ]))
        print("results", result)
 
        # Display results
        for doc in result:
            print(doc)
            accountName=doc.get("accountName")
            campaign=doc.get("campaign")
            noaaRegion=doc.get("noaaRegion")
            cost=doc.get("cost")
            campaignId=doc.get("campaignId")
            impressions=doc.get("impressions")
            Date=doc.get("date")
 
            st.write("AccountName:",accountName)
            st.write("Campaign :",campaign)
            st.write("NoaaRegion :",noaaRegion)
            st.write("Cost :" , cost)
            st.write("campaignId:",campaignId)
            st.write("impressions:",impressions)
            st.write("Date:", Date)
            st.write("-------------------------")
 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
            # def convert_data_to_text(data):
            #     if isinstance(data, str):
            #         return data
            #     elif isinstance(data, list):
            #         return ', '.join(convert_data_to_text(item) for item in data)
            #     elif isinstance(data, dict):
            #         return ', '.join('{}: {}'.format(key, convert_data_to_text(value)) for key, value in data.items())
            #     else:
            #         return str(data)
                
            # data = (accountName)
            # text = convert_data_to_text(data)
 
            # st.write(text)
 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
           
            # data_text = f"{accountName} is a company running a campaign titled '{campaign}' in the {noaaRegion} region. This campaign has a cost of ${cost}, campaign ID '{campaignId}', and has received {impressions} impressions as of {Date}."
            chatgpt = ChatOpenAI()
            prompt = "can you give me detailed response for this:\n" + query
            response = chatgpt.predict(prompt)
            st.write("AI Response:", response)
            st.write("---------------------------------------------------------------------------------------------------------------------------------------")
 
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
        # response=ChatOpenAI(
        # model="gpt-4-1106-preview",
        # message = [
        #         {"role": "system", "content": "You are a useful assistant. Use the assistant's content to answer the user's query. Summarize your answer using the 'campaign' and 'campaignId' and 'AccountName' and 'Cost' metadata in your reply."},
        #         {"role": "assistant", "content": query},
        #         {"role": "user", "content": text},
        #             ]
        # )
        # st.write(response)
 
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 
        # prompt="The marketing insights of given data for the campaign is"
        # response=chatgpt.predict(prompt)
        # request=chatgpt.predict(text)
        # st.write(response + request)
 
 
 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
    # from transformers import Pipeline
 
# # Define the model and tokenizer
#     model_name = "HuggingFaceH4/zephyr-7b-beta"
#     tokenizer = model_name
#     if "/" in model_name:
#         tokenizer = model_name.split("/")[1]
 
# # Create the text generation pipeline
#     generator = Pipeline("text-generation", model=model_name, tokenizer=tokenizer)
 
# # Example usage
#     prompt = "Once upon a time"
#     generated_text = generator(prompt, max_length=50, do_sample=True)
#     print("Generated Text:", generated_text)
 
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
 
if __name__ == "__main__":
    main()