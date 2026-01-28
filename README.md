---
title: Research Assistant Agent
emoji: 🔍
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.9.0
app_file: app.py
pinned: false
---

# Research Assistant Agent

[![Live Demo](https://img.shields.io/badge/Live%20Demo-HuggingFace%20Spaces-blue)](https://huggingface.co/spaces/davidleocadio94DLAI/ai-agents-in-langgraph_research-assistant-agent)
[![Python](https://img.shields.io/badge/Python-3.10+-green)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-orange)](https://langchain-ai.github.io/langgraph/)

An AI research assistant powered by LangGraph StateGraph with Tavily search integration. The agent can search the web for current information and provide comprehensive answers with conversation memory.

## Features

- **StateGraph Architecture** - LangGraph-based agent with conditional routing
- **Tool Calling** - Integrated Tavily search for real-time web research
- **Conversation Memory** - Multi-turn conversations with context persistence
- **Streaming Support** - Real-time response streaming

## Tech Stack

![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991)
![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-1C3C3C)
![Tavily](https://img.shields.io/badge/Tavily-Search%20API-FF6B6B)
![Gradio](https://img.shields.io/badge/Gradio-UI-F97316)

## Getting Started

### Prerequisites

- Python 3.10+
- OpenAI API key
- Tavily API key

### Installation

```bash
# Clone the repository
git clone https://github.com/davidleocadio94/ai-agents-in-langgraph_research-assistant-agent.git
cd ai-agents-in-langgraph_research-assistant-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and TAVILY_API_KEY
```

### Run Locally

```bash
python app.py
```

Open http://localhost:7860 in your browser.

## Two Modes

### 1. Single Query
Ask one-off research questions and get comprehensive answers:
- Real-time web search
- Structured responses
- Source-backed information

### 2. Multi-turn Chat
Have conversations with memory:
- Context preserved across messages
- Follow-up questions understood
- Start new conversations anytime

## How It Works

The agent uses a LangGraph StateGraph with two nodes:

1. **LLM Node** - Processes messages and decides if tools are needed
2. **Action Node** - Executes Tavily search when called

The graph routes conditionally based on whether tool calls exist, creating a loop until the agent has enough information to respond.

## Example Queries

- "What are the latest developments in AI agents?"
- "Compare LangGraph and LangChain for building AI applications"
- "What is retrieval augmented generation (RAG)?"

---

Built as part of the [AI Agents in LangGraph](https://www.deeplearning.ai/short-courses/ai-agents-in-langgraph/) course on DeepLearning.AI
