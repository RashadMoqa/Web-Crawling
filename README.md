# Web Crawler

This repository contains a Python web crawler using Beautiful Soup to scrape contractor data from Muqawil. The crawler focuses on extracting contractors' information from the Muqawil website (https://muqawil.org/en/contractors). Additionally, it implements a semantic search using RAG and the OpenAI Embedding model on this data, leveraging a Qdrant vector database, and providing a simple Streamlit front-end to test the search functionality.

## Architecture

The web crawler follows a simple architecture:

1. **Fetching Page URLs**: Retrieves contractor page URLs from Muqawil using requests and BeautifulSoup.
2. **Fetching Contractor Data**: Crawls contractor data from each contractor's page using Selenium WebDriver for JavaScript content.
3. **Fetching Contractors**: Gathers contractor data from multiple pages by iterating through page numbers.
4. **Saving output data**: Saves output to Excel file

The semantic search and front-end architecture:

1. **OpenAI Initialization**: Initializes the OpenAI client using your API key.
2. **Qdrant Client Setup**: Connects to the Qdrant server for vector search operations.
3. **Data Loading**: Loads data of web crawler.
4. **Text Embedding Generation**: Generates embeddings for relevant columns (Name, Email, Activities, City) using OpenAI's text-embedding-ada-002 model.
5. **FAISS Indexing**: Creates a FAISS index for efficient similarity search based on the generated embeddings.
6. **Search and Response Generation**: Implements a search function that retrieves relevant documents and generates a response using GPT-3.5 Turbo model based on user queries.
7. **Streamlit Front-End**: Sets up a Streamlit app for user interaction, allowing users to input queries and view retrieved documents along with generated responses.
   
**Setup**

To set up the web crawler, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/web-crawler.git

2.  Install the necessary libraries:

   ```bash
   pip install -r requirements.txt


3.  Run web crawler:
   python web_crawler.py
   python semantic_search.py
  streamlit run app.py


![Screenshot 2024-05-15 114307](https://github.com/RashadMoqa/Web-Crawling/assets/73494887/68022239-08ae-489a-8856-9331ca17b04c)

