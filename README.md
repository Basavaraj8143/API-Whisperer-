# API Guardian 🧠

An AI-powered web scraping and chat interface that extracts, analyzes, and responds to queries using Hugging Face Transformers.

## Overview
API Guardian handles both static and dynamic pages through a dual-scraping approach using BeautifulSoup and Selenium fallback.

## Features 🚀

- **Conversational Interface** 🗣️
  - Natural chat-like interaction
  - Human-friendly responses
  
- **AI Capabilities** 🧩
  - Powered by Hugging Face Transformers
  - Intelligent text understanding
  - Smart response generation

- **Web Scraping** 🌐
  - BeautifulSoup for static pages
  - Selenium fallback for dynamic content
  - Auto-retry mechanism
  - Error handling

- **Data Management** 💾
  - Local chunk storage
  - JSON-based data persistence
  - Efficient data retrieval

## Technology Stack 🧰

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit / Gradio |
| Backend | Python, Flask (optional) |
| AI/NLP | Hugging Face Transformers, SentencePiece |
| Scraping | BeautifulSoup, Selenium |
| Storage | JSON, CSV |
| Deployment | Hugging Face Spaces / GitHub Pages |

## Project Structure 📁

```
API-GUARDIAN/
├── __pycache__/          # Python cache files
├── embeddings/           # Embedded vectors
├── output/              # Generated files
├── venv/                # Virtual environment
├── .env                 # Environment config
├── app.py              # Main entry point
├── config.py           # Settings
├── rag_pipeline.py     # RAG pipeline
├── requirements.txt    # Dependencies
└── scraper.py         # Web scraping logic
```

## Quick Start 🚀

1. **Clone and Setup**
```bash
git clone https://github.com/<your-username>/API-GUARDIAN.git
cd API-GUARDIAN
python -m venv venv
venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Environment**
Create `.env` file:
```env
HF_TOKEN=your_huggingface_token_here
```

4. **Run Application**
```bash
streamlit run app.py
```

## Usage Example 💡

```python
from scraper import scrape_and_save

# Scrape and save data
scrape_and_save(
    start_url="https://example.com",
    max_pages=3
)
```

## Development 🛠️

- Run tests: `pytest`
- Format code: `black .`
- Check linting: `flake8`

## Contributing 🤝

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

## License 📄

MIT License - See [LICENSE](LICENSE) file

## Author 👨‍💻

**Basavaraj M N**  
KLE Institute of Technology, Hubli  
Student & Developer
