# Vector Search App

This project is a **Vector Search Application** using **Streamlit, OpenAI Embeddings, and MongoDB Atlas Vector Search**. It allows users to input queries, convert them into embeddings using OpenAI, and search for relevant results stored in MongoDB Atlas.

## Features
- Query vectorization using **OpenAI Embeddings**.
- Vector search in **MongoDB Atlas**.
- Streamlit-based UI for user interaction.

---

## Installation

### Prerequisites
- Python 3.7+
- MongoDB Atlas account
- OpenAI API key

### Steps
1. Clone the repository:
   ```sh
   git clone <repository_url>
   cd vector-search-app
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```sh
   export OPENAI_API_KEY="your_openai_api_key"
   ```
4. Run the Streamlit app:
   ```sh
   streamlit run app.py
   ```

---

## MongoDB Atlas Setup
1. Create a **MongoDB Atlas cluster**.
2. Add a database named `sample_mflix`.
3. Create collections:
   - `Cities`
   - `tenants`
4. Configure **Vector Search Index** in MongoDB Atlas.
5. Update **MongoDB connection string** in the code.

---

## Usage
### **Streamlit Application**
1. **Start the app** and enter a query.
2. **Search** for relevant data from MongoDB Atlas.
3. **Retrieve results** based on vector similarity.

### **Embedding and Storing Data in MongoDB**
The following Python script reads data from a JSON file, generates embeddings using OpenAI, and stores them in MongoDB Atlas:

```python
import os
import json
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
import pymongo

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings()

# Connect to MongoDB Atlas
MONGO_URL="your_mongo_connection_string"
MONGO_DBNAME = "sample_mflix"
COLLECTION ="tenants"

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DBNAME]
vec_collection = db[COLLECTION]

# Load JSON data from file
with open('Tenants.json', 'r') as f:
    data = json.load(f)

# Process and store embeddings
for item in data:
    if 'name' in item and 'shortName' in item and 'industryIds' in item:
        name_embedding = embeddings.embed_query(item['name'])
        shortName_embedding = embeddings.embed_query(item['shortName'])
        industryIds_embedding = embeddings.embed_query(item['industryIds'])
        
        vec_collection.insert_one({
            "name": item['name'],
            "shortName": item['shortName'],
            "industryIds": item['industryIds'],
            "name_embedding": name_embedding,
            "shortName_embedding": shortName_embedding,
            "industryIds_embedding": industryIds_embedding
        })
```

---

## Technologies Used
- **Python**
- **Streamlit** (for UI)
- **MongoDB Atlas** (for vector storage and search)
- **OpenAI Embeddings** (for text vectorization)
- **LangChain** (for AI-powered search)

---

## License
This project is licensed under the MIT License.

---

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

---

## Author
[Ajithkumar]

