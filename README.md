![AI-Search-Engine Banner](https://github.com/Hussain-Murtazaa/Conversational-Groq-Chatbot/main/Banner.png)
# 🤖 AI Search Engine - ReAct Agent

An intelligent search assistant powered by AI reasoning that uses multiple tools (Web Search, Wikipedia, arXiv) to find and synthesize accurate information in real-time.

## ✨ Features

- **Multi-Tool Integration**: Searches across DuckDuckGo (Web), Wikipedia, and arXiv (Research Papers)
- **AI-Powered Reasoning**: Uses Groq LLM to think about the best tool for each query
- **ReAct Framework**: Implements Thought → Action → Observation → Conclusion pattern
- **Real-time Results**: Fetches current information from the web
- **User-Friendly UI**: Beautiful Streamlit interface with dark theme
- **Rate Limiting**: Built-in protection against spam requests
- **Error Handling**: Robust error management with informative messages
- **Token Efficient**: Optimized context management to reduce API costs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- GROQ API Key (Get one free at [console.groq.com](https://console.groq.com))

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Hussain-Murtazaa/AI_Search_engine.git
cd AI_Search_engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run search_engine.py
```

5. Open your browser and navigate to `http://localhost:8501`

## 📋 Requirements

```
streamlit>=1.28.0
groq>=0.4.0
python-dotenv>=1.0.0
duckduckgo-search>=3.9.0
wikipedia>=1.4.0
arxiv>=1.4.0
```

## 🎯 How It Works

1. **User Query**: You ask a question in the chat interface
2. **AI Reasoning**: The agent analyzes the query and decides which tool to use
3. **Tool Selection**:
   - **WebSearch**: For current events, news, and recent information
   - **Wikipedia**: For general knowledge, definitions, and historical facts
   - **arXiv**: For academic papers and research topics
4. **Information Retrieval**: The selected tool fetches relevant results
5. **Answer Synthesis**: The AI combines findings into a clear, concise answer

## ⚙️ Configuration

In the sidebar, you can customize:

- **GROQ API Key**: Your API key for the LLM (required)
- **Model**: Choose between `llama-3.1-8b-instant` or `gemma2-9b-it`
- **Max Reasoning Steps**: Set how many times the agent can think and act (1-6 steps)
- **Clear Chat History**: Reset all conversations

## 🔧 Project Structure

```
AI_Search_engine/
├── search_engine.py       # Main application file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not included)
└── README.md              # This file
```

## 💡 Example Queries

- "Who is the current president of Pakistan?"
- "What are the latest developments in AI?"
- "Explain quantum computing"
- "Find recent research on machine learning"
- "What are the top programming languages in 2024?"

## 🎨 Features Breakdown

### Frontend
- Dark gradient theme with modern UI
- Real-time chat interface
- Animated message transitions
- Tool usage indicators
- Expandable reasoning steps
- Rate limit notifications

### Backend
- Efficient token management with rolling history
- Rate limiting (5 requests per 60 seconds)
- Request timeouts (10 seconds)
- Robust error handling and recovery
- Flexible action parsing
- Context window optimization

## 🚨 Rate Limiting

The application includes built-in rate limiting:
- Maximum 5 requests per 60 seconds
- Prevents API abuse and excessive costs
- Shows remaining wait time if limit is exceeded

## ⚠️ Error Handling

The agent gracefully handles:
- API failures with informative messages
- Missing Wikipedia pages with alternative suggestions
- Network errors during search
- Malformed LLM responses
- Timeout errors

## 🔐 Security

- API keys stored in `.env` file (never committed)
- No sensitive data logged
- Input validation and sanitization
- Safe error messages without exposing sensitive info

## 📊 Performance Optimization

- **Token Efficiency**: Keeps only last 10 interactions in context
- **Result Truncation**: Limits tool results to prevent token bloat
- **Lazy Loading**: Only processes tools when needed
- **Timeout Protection**: 10-second timeout on all API calls

## 🎓 Use Cases

- Research and information gathering
- Academic paper discovery
- Current event tracking
- Fact-checking and verification
- Learning and knowledge exploration
- Quick answers to complex questions

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📝 License

This project is open source and available under the MIT License.

## 🙋 Support

If you encounter any issues:
1. Check that your GROQ API key is valid
2. Ensure all dependencies are installed
3. Verify your internet connection
4. Check the error messages in the sidebar

## 🔗 Links

- [GROQ Console](https://console.groq.com) - Get API Key
- [Streamlit Docs](https://docs.streamlit.io)
- [DuckDuckGo Search](https://duckduckgo.com)
- [arXiv API](https://arxiv.org/help/api)

---

**Created by**: [Hussain Murtazaa](https://github.com/Hussain-Murtazaa)

**Star ⭐ if you find this useful!**
