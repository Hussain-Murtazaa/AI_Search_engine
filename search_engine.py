# ---------------------------------------------------
#  IMPROVED SEARCH AGENT FOR CLASS DEMONSTRATION
#  Enhanced frontend with better styling and UX
# ---------------------------------------------------

import os
import re
import time
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from duckduckgo_search import DDGS
import wikipedia
import arxiv
from collections import deque

load_dotenv()

# -------------------------
# PAGE CONFIG & STYLING
# -------------------------
st.set_page_config(
    page_title="ReAct Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Chat messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin-bottom: 1rem;
        display: flex;
        gap: 1rem;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        border-left: 4px solid #60a5fa;
    }
    
    .assistant-message {
        background: rgba(30, 41, 59, 0.8);
        color: #e2e8f0;
        border-left: 4px solid #10b981;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }
    
    /* Headers */
    h1 {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    h3 {
        color: #cbd5e1;
        margin-top: 1.5rem;
    }
    
    /* Input area */
    .stChatInput {
        border-radius: 0.75rem !important;
        border: 1px solid #334155 !important;
        background: rgba(15, 23, 42, 0.9) !important;
    }
    
    .stChatInput input {
        color: #e2e8f0 !important;
        font-size: 1rem !important;
    }
    
    .stChatInput:focus-within {
        border: 1px solid #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: 700;
        color: #60a5fa;
        margin-bottom: 1rem;
    }
    
    /* Info/error boxes */
    .stInfo, .stWarning, .stError, .stSuccess {
        border-radius: 0.75rem !important;
    }
    
    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        border-left: 4px solid #3b82f6 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(59, 130, 246, 0.1);
        border-radius: 0.5rem;
        color: #60a5fa;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(59, 130, 246, 0.2);
    }
    
    /* Text styling */
    body {
        color: #cbd5e1;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------
# PAGE HEADER
# -------------------------
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 🤖 ReAct Agent")
    st.markdown("*Intelligent search assistant with reasoning*")
with col2:
    st.markdown("")
    st.markdown("")

st.markdown("---")

# -------------------------
# SIDEBAR CONFIGURATION
# -------------------------
with st.sidebar:
    st.markdown('<div class="sidebar-header">⚙️ Configuration</div>', unsafe_allow_html=True)
    st.divider()
    
    api_key = st.text_input("🔑 GROQ API Key", type="password", placeholder="gsk_...") or os.getenv("GROQ_API_KEY", "")
    
    model_name = st.selectbox(
        "🧠 Model",
        ["llama-3.1-8b-instant", "gemma2-9b-it"],
        help="Choose the LLM to power the agent"
    )
    
    max_steps = st.slider(
        "🔄 Max Reasoning Steps",
        1, 6, 3,
        help="More steps = deeper reasoning but slower"
    )
    
    st.divider()
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
    
    st.divider()
    st.markdown("""
    <div style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6;">
    <strong>How it works:</strong><br>
    1. You ask a question<br>
    2. Agent reasons about best tool<br>
    3. Searches Web, Wiki, or arXiv<br>
    4. Synthesizes answer<br>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "request_times" not in st.session_state:
    st.session_state.request_times = deque(maxlen=10)


# -------------------------
# RATE LIMITING
# -------------------------
def check_rate_limit(max_requests=5, window_seconds=60):
    """Prevent rapid-fire requests."""
    now = time.time()
    st.session_state.request_times.append(now)
    
    recent = [t for t in st.session_state.request_times if now - t < window_seconds]
    if len(recent) > max_requests:
        wait = int(window_seconds - (now - recent[0]))
        return False, f"⏱️ Too many requests. Wait {wait}s."
    return True, ""


# -------------------------
# TOOL FUNCTIONS
# -------------------------

def tool_web_search(query, k=3):
    """Search the web with better error handling and concise results."""
    try:
        with DDGS() as ddg:
            results = ddg.text(query, region="us-en", max_results=k)
            if not results:
                return "No web results found."
            
            lines = []
            for r in results:
                title = r.get("title", "No title")[:60]
                body = r.get("body", "")[:120]
                link = r.get("href", "")
                lines.append(f"• {title}\n  {body}\n  {link}")
            
            return "\n".join(lines)
    except Exception as e:
        return f"Web search error: {type(e).__name__} - {str(e)[:100]}"


def tool_wikipedia(query, sentences=1):
    """Fetch brief Wikipedia summary with better error handling."""
    try:
        wikipedia.set_lang("en")
        pages = wikipedia.search(query, results=1)
        if not pages:
            return "No Wikipedia page found."
        
        summary = wikipedia.summary(pages[0], sentences=sentences)
        return f"Wikipedia [{pages[0]}]: {summary}"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Wikipedia: Multiple matches. Try: {', '.join(e.options[:3])}"
    except Exception as e:
        return f"Wikipedia error: {type(e).__name__}"


def tool_arxiv(query):
    """Get top arXiv paper with error handling."""
    try:
        search = arxiv.Search(query=query, max_results=1, sort_by=arxiv.SortCriterion.Relevance)
        results = list(search.results())
        if not results:
            return "No arXiv papers found."
        
        paper = results[0]
        snippet = (paper.summary or "")[:250].replace("\n", " ").strip()
        return f"arXiv [{paper.title[:60]}...]\nLink: {paper.entry_id}\nAbstract: {snippet}..."
    except Exception as e:
        return f"arXiv error: {type(e).__name__}"


# -------------------------
# SYSTEM PROMPT
# -------------------------
SYSTEM_PROMPT = """You are a research assistant with 3 tools:
1) WebSearch - for current events, news, recent info
2) Wikipedia - for general knowledge, definitions, people, places
3) Arxiv - for academic papers and research

Choose the best tool. Format exactly:
Thought: <your reasoning>
Action: <WebSearch|Wikipedia|Arxiv>
Action Input: <search phrase>

Stop when you have enough info for a clear answer, then write:
Final Answer: <concise answer>
"""


# -------------------------
# PARSING
# -------------------------
def parse_agent_output(text):
    """Extract Action and Action Input with better flexibility."""
    action = None
    action_input = None
    
    lines = text.split("\n")
    for i, line in enumerate(lines):
        line_clean = line.strip()
        
        if line_clean.lower().startswith("action:"):
            action_match = re.search(r"(WebSearch|Wikipedia|Arxiv)", line_clean, re.I)
            if action_match:
                action = action_match.group(1).title()
        
        if line_clean.lower().startswith("action input:"):
            action_input = line_clean.split(":", 1)[1].strip()
            if action_input.startswith('"') and action_input.endswith('"'):
                action_input = action_input[1:-1]
    
    return action, action_input


# -------------------------
# AGENT LOOP
# -------------------------
def mini_agent(client, model, question, max_iters=3):
    """Run agent with token efficiency and better error handling."""
    
    history_window = deque(maxlen=10)
    observation = None
    
    for step in range(1, max_iters + 1):
        convo_lines = [f"Question: {question}"]
        convo_lines.extend(history_window)
        if observation:
            convo_lines.append(f"Observation: {observation}")
        
        convo = "\n".join(convo_lines)
        
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": convo},
                ],
                temperature=0.2,
                max_tokens=400,
                timeout=10,
            )
            text = resp.choices[0].message.content or ""
        except Exception as e:
            return f"❌ API Error: {str(e)[:100]}"
        
        with st.expander(f"🧠 Reasoning Step {step}", expanded=(step == 1)):
            st.markdown(text)
        
        if "Final Answer:" in text:
            return text.split("Final Answer:", 1)[1].strip()
        
        action, action_input = parse_agent_output(text)
        
        if not action or not action_input:
            return "❌ Agent couldn't determine next action. Try rephrasing."
        
        st.info(f"🔍 Using **{action}**: `{action_input[:50]}...`")
        
        if action == "Websearch":
            observation = tool_web_search(action_input)
        elif action == "Wikipedia":
            observation = tool_wikipedia(action_input)
        elif action == "Arxiv":
            observation = tool_arxiv(action_input)
        else:
            observation = f"Unknown tool: {action}"
        
        history_window.append(f"Thought: Using {action}")
        history_window.append(f"Action: {action}")
        history_window.append(f"Action Input: {action_input}")
        history_window.append(f"Observation: {observation[:200]}")
    
    try:
        summary = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Provide a brief, clear answer in 1-2 sentences."},
                {"role": "user", "content": "\n".join(list(history_window)[-6:])},
            ],
            temperature=0.2,
            max_tokens=200,
            timeout=10,
        )
        return summary.choices[0].message.content
    except Exception as e:
        return f"❌ Summarization failed: {str(e)[:100]}"


# -------------------------
# CHAT DISPLAY & INPUT
# -------------------------

# Display chat history
if st.session_state.chat_history:
    for exchange in st.session_state.chat_history:
        st.markdown(f'<div class="chat-message user-message">👤 <b>You:</b> {exchange["user"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-message assistant-message">🤖 <b>Agent:</b> {exchange["assistant"]}</div>', unsafe_allow_html=True)
    st.divider()

# Input area
query = st.chat_input("💬 Ask me anything...")

if query:
    allowed, msg = check_rate_limit()
    if not allowed:
        st.error(msg)
    elif not api_key:
        st.error("🔑 Please add your GROQ API Key in the sidebar.")
    else:
        st.markdown(f'<div class="chat-message user-message">👤 <b>You:</b> {query}</div>', unsafe_allow_html=True)
        
        client = Groq(api_key=api_key)
        with st.spinner("🤔 Agent is thinking..."):
            answer = mini_agent(client, model=model_name, question=query, max_iters=max_steps)
        
        st.markdown(f'<div class="chat-message assistant-message">🤖 <b>Agent:</b> {answer}</div>', unsafe_allow_html=True)
        st.session_state.chat_history.append({"user": query, "assistant": answer})
        st.rerun()