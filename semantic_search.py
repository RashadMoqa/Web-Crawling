import pandas as pd
import openai
import faiss
import numpy as np

# Initialize OpenAI API key, you can use yours
openai.api_key = 'sk-proj-EY0xN0jM7LOnluL5LnpuT3BlbkFJmxopoUPFBZ2pbKQDwKvc'

# Load data from Excel
df = pd.read_excel("output-10.xlsx")

# Extract relevant columns for semantic search
documents = df[['Name', 'Email', 'Activities', 'City']].astype(str).agg(', '.join, axis=1).tolist()

# Function to get embeddings
def get_embeddings(texts):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=texts
    )
    embeddings = [data['embedding'] for data in response['data']]
    return embeddings

# Generate embeddings for the documents
embeddings = get_embeddings(documents)

# Convert embeddings to a numpy array
embeddings_np = np.array(embeddings).astype('float32')

# Create a FAISS index
index = faiss.IndexFlatL2(embeddings_np.shape[1])
index.add(embeddings_np)

# Search and generate response function
def search_and_generate(query, k=5):
    # Step 1: Retrieve relevant documents
    query_embedding = get_embeddings([query])[0]
    query_embedding = np.array(query_embedding).astype('float32').reshape(1, -1)
    distances, indices = index.search(query_embedding, k)
    retrieved_docs = [documents[i] for i in indices[0]]

    # Step 2: Use the retrieved documents to generate a response
    context = "\n".join(retrieved_docs)
    prompt = f"The following documents are relevant to the query: {query}\n{context}\n\nBased on the above documents, provide a detailed response to the query."

    # Use gpt-3.5-turbo to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )
    
    generated_response = response.choices[0].message['content'].strip()
    return retrieved_docs, generated_response

# Example query
query = "I want a contractor specialized in building schools"
retrieved_docs, generated_response = search_and_generate(query)

# Display results
print("Retrieved Documents:")
for i, doc in enumerate(retrieved_docs):
    print(f"Document {i+1}: {doc}")

print("\nGenerated Response:")
print(generated_response)
