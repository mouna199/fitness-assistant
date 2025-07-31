# Fitness Assistant 
A smart fitness assistant powered by AI that provides personalized exercise recommendations and fitness advice. This application uses RAG (Retrieval-Augmented Generation) technology to answer fitness-related questions based on a comprehensive exercise database.

## Features

- AI-powered fitness recommendations
- Comprehensive exercise database with 200+ exercises
- Personalized workout suggestions
- User-friendly web interface
- Vector search capabilities using Qdrant
- Responsive design

## Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8 or higher
- pip (Python package installer)
- Docker (for Qdrant vector database)
- OpenAI API key

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mouna199/fitness-assistant.git
cd fitness-assistant
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

1. Copy the environment template:
```bash
cp .envrc_template .envrc
```

2. Edit `.envrc` and add your OpenAI API key:
```bash
export OPENAI_API_KEY='your_openai_api_key_here'
```

3. Load the environment variables:
```bash
source .envrc
```

### 5. Start Qdrant Vector Database

The application uses Qdrant as the vector database. Start it using Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

## Running the Application

### Option 1: Web Application (Recommended)

Start the FastAPI web server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Then open your browser and navigate to:
```
http://localhost:8000
```

### Option 2: Command Line Testing

You can also test the application directly from the command line:

```bash
python main.py
```

This will run a test query and display the results in the terminal.

## Usage

1. **Web Interface**: 
   - Open your browser to `http://localhost:8000`
   - Type your fitness question in English
   - Get personalized exercise recommendations and advice

2. **Example Questions**:
   - "Give me exercises for hamstrings"
   - "What are the best chest exercises?"
   - "How to strengthen my core?"
   - "Exercises for building leg muscles"

## Project Structure

```
fitness-assistant/
├── app/
│   ├── __init__.py
│   ├── embedder.py          # Text embedding functionality
│   ├── llm.py              # Language model integration
│   ├── prompt_builder.py   # Prompt engineering
│   ├── rag_pipeline.py     # RAG implementation
│   ├── retriever.py        # Document retrieval logic
│   └── utils.py            # Utility functions
├── data/
│   ├── data.csv            # Exercise database
│   └── data_unclean.csv    # Raw data
├── templates/
│   └── index.html          # Web interface
├── notebooks/
│   └── code_propre.ipynb   # Data processing notebook
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .envrc_template        # Environment variables template
└── README.md              # This file
```

## Configuration

The application supports two backend modes:

- **Qdrant** (default): Uses vector similarity search for better semantic matching
- **MinSearch**: Uses traditional text search

You can change the backend by modifying the `BACKEND` variable in `main.py`:

```python
BACKEND = "qdrant"  # or "minsearch"
```

## Troubleshooting

### Common Issues

1. **Qdrant Connection Error**:
   - Make sure Docker is running
   - Ensure Qdrant container is started: `docker run -p 6333:6333 qdrant/qdrant`
   - Check if port 6333 is available

2. **OpenAI API Error**:
   - Verify your API key is correctly set in `.envrc`
   - Make sure you have sufficient API credits
   - Check your internet connection

3. **Module Import Errors**:
   - Ensure virtual environment is activated
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **Port Already in Use**:
   - Change the port: `uvicorn main:app --port 8001`
   - Or kill the process using the port

### Logs and Debugging

- Check FastAPI logs in the terminal where you started the server
- For detailed debugging, modify the logging level in the application code

## Development

### Adding New Exercises

1. Edit `data/data.csv` to add new exercises
2. Restart the application to reload the data
3. The vector embeddings will be automatically regenerated

### Customizing the Interface

- Modify `templates/index.html` for UI changes
- Update CSS styles within the HTML file

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request


## Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Make sure to include error messages and system information

## Acknowledgments

- LLM Zoomcamp
- Qdrant tutorial
- FastAPI documentation

---
