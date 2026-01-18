# 🍕 Pizza Restaurant RAG Assistant

A professional AI assistant that answers questions about pizza restaurants using customer reviews. Built with LangChain, Ollama LLMs, and Chroma vector database.

## 🚀 Features

- **AI-Powered Q&A**: Ask questions about pizza restaurants and get answers based on real reviews
- **Premium Web Interface**: Beautiful Streamlit interface with chat history and analytics
- **Fast Vector Search**: Retrieve relevant reviews using semantic search
- **Local LLM**: Runs completely offline using Ollama models
- **Easy to Use**: Simple setup and intuitive interface

## 📁 Project Structure

```
pizza_rag_project/
├── app/                    # Streamlit web interface
├── config/                # Configuration settings
├── core/                  # Constants and core utilities
├── data/                  # CSV data files
├── database/              # Vector database operations
├── models/                # LLM models and chains
├── chroma_langchain_db/   # Chroma vector database (auto-generated)
├── main.py               # CLI version
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- Required Ollama models pulled:
  ```bash
  ollama pull phi          # LLM model
  ollama pull mxbai-embed-large  # Embedding model
  ```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare Data
Place your `realistic_restaurant_reviews.csv` file in the `data/` directory.

## 🎮 Usage

### Option 1: Web Interface (Recommended)
```bash
streamlit run app/streamlit_app.py
```
Then open `http://localhost:8501` in your browser.

### Option 2: Command Line Interface
```bash
python main.py
```

### Option 3: Launcher
```bash
python run_app.py
```

## 🖥️ Interface Features

### Web Interface
- **💬 Chat Interface**: Natural conversation with the AI assistant
- **📊 Analytics Dashboard**: Visual insights and statistics
- **⚙️ Customizable Settings**: Adjust search parameters and models
- **💡 Sample Questions**: Quick-start with common queries
- **📱 Responsive Design**: Works on desktop and mobile

### Sample Questions
- "What's the best pizza place in town?"
- "Which restaurant has the best crust?"
- "Where can I find vegetarian pizza options?"
- "Which place has the fastest delivery?"

## 🛠️ Configuration

Edit `config/settings.py` to customize:
- LLM model (`phi`, `llama2`, `mistral`, etc.)
- Embedding model
- Search parameters
- File paths

## 🔧 Technical Details

### Built With
- **LangChain**: Framework for LLM applications
- **Ollama**: Local LLM inference
- **Chroma**: Vector database for semantic search
- **Streamlit**: Web interface framework
- **Pandas**: Data manipulation

### How It Works
1. **Data Ingestion**: CSV reviews are loaded and embedded
2. **Vector Storage**: Embeddings stored in Chroma database
3. **Semantic Search**: User questions matched to relevant reviews
4. **LLM Generation**: Phi model generates answers based on retrieved reviews
5. **Response Display**: Answers presented in user-friendly format

## 📊 Performance
- ⚡ Response time: 2-5 seconds
- 🔍 Retrieval accuracy: Top 5 most relevant reviews
- 💾 Storage: ~100MB for 1000 reviews with embeddings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details.

## 🙋 Support

For issues and questions:
1. Check the [Ollama documentation](https://github.com/ollama/ollama)
2. Review the LangChain docs
3. Open an issue in this repository

---

**Enjoy your pizza research! 🍕**