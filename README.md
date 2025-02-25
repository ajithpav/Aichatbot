# Vector Search App

This is a Streamlit-based web application that integrates OpenAI's GPT model and MongoDB Atlas for vector search. The app allows users to input queries and retrieve the most relevant city/state information from a MongoDB database using vector embeddings.

## Features
- User-friendly interface using Streamlit.
- OpenAI-powered embeddings for query vectorization.
- MongoDB Atlas integration for vector search.
- Real-time responses for user queries.

## Installation
### Prerequisites
Make sure you have Python installed (>=3.7) and install the required dependencies:

```bash
pip install streamlit pymongo langchain-openai openai
```

## Environment Setup
Before running the application, set up your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your_openai_api_key_here"
```

Or replace the placeholder in `os.environ["OPENAI_API_KEY"]` within the script.

## MongoDB Configuration
This application connects to a MongoDB Atlas database. Update the following details in the script if necessary:

```python
MONGO_URL = "your_mongodb_connection_string"
MONGO_DBNAME = "your_database_name"
COLLECTION = "your_collection_name"
```

Ensure that your MongoDB Atlas instance has vector search enabled and that your collection is indexed properly.

## Running the Application
To start the application, execute the following command:

```bash
streamlit run app.py
```

## How It Works
1. The user inputs a query in the search bar.
2. The query is converted into an embedding vector using OpenAI's embeddings API.
3. The application performs a vector search in the MongoDB database.
4. The most relevant city/state information is retrieved and displayed.

## Example Usage
- Query: "Which state has the city Los Angeles?"
- Response: "California"

## Notes
- Ensure that the MongoDB collection contains properly stored embeddings under the `stateName_Embedding` field.
- The MongoDB `vector_index` should be created before running the search.
- Use a valid OpenAI API key to avoid authentication errors.

## License
This project is licensed under the MIT License.

## Author
Developed by [Ajithkumar P]

