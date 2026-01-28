"""LangGraph Research Assistant Agent - StateGraph with Tool Calling"""

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver


# Define AgentState TypedDict with messages field
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]


class ResearchAgent:
    """Research assistant agent using LangGraph StateGraph with tool calling."""

    def __init__(self, checkpointer=None):
        self.system = """You are a smart research assistant. Use the search engine to look up information.
You are allowed to make multiple calls (either together or in sequence).
Only look up information when you are sure of what you want.
If you need to look up some information before asking a follow up question, you are allowed to do that!
"""
        # Initialize model and tools
        self.model = ChatOpenAI(model="gpt-4o")
        self.tool = TavilySearchResults(max_results=3)
        self.tools = {self.tool.name: self.tool}
        self.model = self.model.bind_tools([self.tool])

        # Create StateGraph
        graph = StateGraph(AgentState)

        # Add nodes
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)

        # Add conditional edge from "llm"
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )

        # Add edge from "action" back to "llm"
        graph.add_edge("action", "llm")

        # Set entry point
        graph.set_entry_point("llm")

        # Compile with checkpointer
        self.graph = graph.compile(checkpointer=checkpointer)

    def exists_action(self, state: AgentState) -> bool:
        """Check if the last message has tool calls."""
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState) -> dict:
        """Call the LLM with messages."""
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState) -> dict:
        """Execute tool calls."""
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            if t['name'] not in self.tools:
                result = "bad tool name, retry"
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(
                tool_call_id=t['id'],
                name=t['name'],
                content=str(result)
            ))
        return {'messages': results}


# Global agent with memory for conversation persistence
memory = MemorySaver()
agent = ResearchAgent(checkpointer=memory)

# Thread counter for unique conversations
_thread_counter = 0


def research_query(query: str, thread_id: str = None) -> str:
    """Run a research query and return the response."""
    global _thread_counter

    if thread_id is None:
        _thread_counter += 1
        thread_id = f"thread_{_thread_counter}"

    config = {"configurable": {"thread_id": thread_id}}
    messages = [HumanMessage(content=query)]

    result = agent.graph.invoke({"messages": messages}, config)
    return result['messages'][-1].content


def research_stream(query: str, thread_id: str = None):
    """Stream research query responses."""
    global _thread_counter

    if thread_id is None:
        _thread_counter += 1
        thread_id = f"thread_{_thread_counter}"

    config = {"configurable": {"thread_id": thread_id}}
    messages = [HumanMessage(content=query)]

    for event in agent.graph.stream({"messages": messages}, config):
        for node_name, value in event.items():
            if 'messages' in value:
                for msg in value['messages']:
                    if hasattr(msg, 'content') and msg.content:
                        yield node_name, msg.content
