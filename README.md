🧠 Intelligent Web Chat Scraper
An AI-powered web scraping and chat interface that extracts, analyzes, and responds to user queries using Hugging Face Transformers. It supports website scraping with Selenium fallback, allowing it to handle both static and dynamic pages — even those that block normal scraping.
🚀 Features

🗣️ Conversational Chat Interface — Chat with the system like a human.
🧩 AI-Powered Inference — Uses Hugging Face Transformers for intelligent text understanding and generation.
🌐 Smart Web Scraping — Automatically scrapes website content using BeautifulSoup and Selenium fallback for dynamic pages.
📂 Multi-Website Support — Works across many websites and formats.
💾 Chunk Storage — Saves processed website data locally in chunks.json for faster repeated queries.
🧱 Resilient Architecture — Automatically retries failed scrapes, skips broken URLs, and handles errors gracefully.
⚙️ Customizable Parameters — Control model, temperature, and max token limits directly from UI (if using Gradio).

🧰 Tech Stack
LayerTechnologyFrontend / InterfaceStreamlit / GradioBackendPython, Flask (optional)AI / NLPHugging Face Transformers, SentencePieceScrapingBeautifulSoup, Selenium (fallback)Data StorageJSON (chunks.json), CSVDeploymentHugging Face Spaces / GitHub Pages
⚙️ How It Works

User enters a query or URL.
The system scrapes the page using requests + BeautifulSoup.
If content is dynamically loaded, Selenium is used as fallback.
Scraped text is split into chunks and saved in chunks.json.
AI model processes these chunks via Hugging Face Transformers to generate intelligent responses.
Processed output is displayed in a clean chat interface.

📁 Project Structure
📦 API-GUARDIAN/
├── __pycache__/          # Python cache files
├── embeddings/           # Embedded vector representations
├── .gitignore           # Git ignore configuration
├── output/              # Generated output files
├── venv/                # Virtual environment
├── .env                 # Environment variables
├── app.py               # Main application entry point
├── config.py            # Configuration settings
├── rag_pipeline.py      # RAG (Retrieval-Augmented Generation) pipeline
├── requirements.txt     # All dependencies
└── scraper.py           # Web scraping logic (BeautifulSoup + Selenium fallback)
🔧 Setup Instructions
1️⃣ Clone the Repository
bashgit clone https://github.com/<your-username>/API-GUARDIAN.git
cd API-GUARDIAN
2️⃣ Set Up Virtual Environment
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3️⃣ Configure Environment Variables
Create a .env file in the root directory with your configuration:
envHF_TOKEN=your_huggingface_token_here
# Add other API keys and configurations as needed
4️⃣ Install Dependencies
bashpip install -r requirements.txt
5️⃣ Run the App
If using Gradio:
bashpython app.py
If using Streamlit:
bashstreamlit run app.py
🔑 Hugging Face Deployment
If deployed on Hugging Face Spaces:

Add your HF_TOKEN as a repository secret under Settings → Repository Secrets → New secret
The token will be automatically loaded from environment variables

📸 Snapshots
Show Image
Show Image
Show Image
Show Image
Show Image
🧠 Example Use
Input:
"Scrape the website https://example.com and summarize key topics."
Output:
"The website discusses machine learning frameworks, datasets, and AI benchmarks, focusing on model training efficiency."
🧩 Future Improvements

Add offline mode using Ollama for local AI inference.
Integrate vector database (FAISS / ChromaDB) for advanced retrieval.
Improve chunk storage efficiency and indexing.
Add multi-language support and voice interface.
Enhance RAG pipeline with better context retrieval.

👨‍💻 Authors
Developed by: Basavaraj M N
Institution: KLE Institute of Technology, Hubli
Role: Student & Developer
🪪 License
This project is licensed under the MIT License — feel free to use, modify, and share.

📝 Notes

The embeddings/ directory stores vector representations for efficient similarity search.
The output/ directory contains generated files and logs.
config.py centralizes all configuration settings for easy management.
rag_pipeline.py implements the Retrieval-Augmented Generation system for enhanced AI responses.
