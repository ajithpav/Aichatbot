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
COLLECTION ="tenats"

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DBNAME]
vec_collection = db[COLLECTION]

# Load JSON data from the file ViewBaseMetricsMarketingQuarterly
with open('/home/guest/polaris-dev.Citiess.json', 'r') as f:
    data = json.load(f)

# Embed the input text and store the vectors in the MongoDB database

for item in data:
    print("Item",item)
    # Check if the key 'Response' exists in the dictionary

    if 'city' and'stateName' and "countryName" in item:
        city = item['city']
        print("city",city)
        stateName=item['stateName']
        print("stateName",stateName)
        countryName=item['countryName']
        # print("countryNAme":countryName)
        name_embedding = embeddings.embed_query(city)
        print("name_emb",name_embedding)
        state_embedding = embeddings.embed_query(stateName)
        print("state_emb",state_embedding)
        countryName_embedding=embeddings.embed_query(countryName)
        print("contry_emb",countryName_embedding)

        vec_collection.insert_many([{"city": city,"state":stateName,"countryName":countryName,"stateName_Embedding":state_embedding,"city_embedding": name_embedding,"countryName_Embeding":countryName_embedding}])
        # vec_collection.insert_many({"stateName":stateName,"State_embedding":state_embedding})
    else:
        print(f"Key 'Resopnse' not found in item: {item}")

# Embed the input text
# input_vector = embeddings.embed_query(input_text)
# print("================", input_vector)


# result = vec_collection.insert_one({"input_text": input_text, "input_vector": input_vector})

# print("rsult is--------------->", result)
# Query the MongoDB Atlas vector search database

# pipeline = [
#     {
#         "$vectorSearch": {
#             "index": "vector_index",
#             "path": "embedded_movies",city_embeddings,plot_embedding
#             "numCandidates":20,
#             "queryVector": input_vector,
#             "limit": 10
#         }
#     }, 
    # {
    #  "$project": {
    #      "_id": 1,
    #      "input_text": 1
    #  }   
    # }
# ]

# Query the MongoDB Atlas vector search database
# try:
#         results = db.embedded_movies.aggregate([
#             {
#                 "$vectorSearch": {
#                     "index": "vector_index",
#                     "path": "plot_embedding",
#                     "queryVector": input_vector,
#                     "numCandidates": 50,
#                     "limit": 1
#                 }
#             },
#             # {
            #       "$project": {
            #             "_id": 1,
            #             "plot_embedding": 0,
            #             "plot": 1,
            #             "genres": 0,
            #             "cast": 0,
            #             "poster": 0,
            #             "title": 1,
            #             "fullplot": 1,
            #             "languages": 0,            # "directors": 0,
            #             "writers": 0,
            #             "awards": 0,
            #       }
            # }
            # {
            #       "$project": {
            #             "score": { "$meta": "vectorSearchScore" }
            #       }
            # }
        # ])
        # print("results------------->",json(results))

        # for  doc in results:
        #     # print("========>",doc)
        #     if(doc.get("plot") is not None):
        #         print("plot is---->", doc.get("plot"))


        # for  doc in results:
        #     # print("========>",doc)
        #     if(doc.get("stateName") is not None):
        #         plot_name = doc.get("stateName")
        #         print("satename is", plot_name)
        #     if(doc.get("city")is not None): 
        #         plot_name = doc.get("city")
        #         print("city name is", plot_name)

        # response = openai.ChatCompletion.create(
        # engine="text-davinci-003",
        # prompt=f"{plot_name}",
        # max_tokens=100,
        # n=1,
        # stop=None,
        # temperature=0.5,
        # )
        # output_text = response.choices[0].text.strip()
        # print("OpenAI Response to Question:", output_text)

                

        # completion = openai.ChatCompletion.create(
        #     model="gpt-4-1106-preview",
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": f"Tell me about the {plot_name}."}
        #     ],
        #     temperature=0.5
        # )
        # print("prompt:", plot_name)
        # print("Response:", completion.choices[0].message.content)
        # print("-" * 50)

# except Exception as e:
#         print("Error during MongoDB aggregation:", e)

