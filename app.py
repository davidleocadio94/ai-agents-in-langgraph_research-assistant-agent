"""Gradio interface for LangGraph Research Assistant Agent."""

import gradio as gr
from src.agent import research_query

# Store thread IDs for conversations
conversation_threads = {}


def single_query(query: str) -> str:
    """Handle a single research query."""
    if not query.strip():
        return ""
    return research_query(query)


def chat_response(message: str, history: list, conversation_id: str) -> tuple:
    """Handle chat messages with conversation memory."""
    if not message.strip():
        return "", history

    # Use conversation ID as thread ID for memory
    thread_id = f"chat_{conversation_id}" if conversation_id else None

    response = research_query(message, thread_id=thread_id)
    history.append((message, response))
    return "", history


def new_conversation():
    """Start a new conversation."""
    import uuid
    return [], str(uuid.uuid4())


with gr.Blocks(title="Research Assistant Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # Research Assistant Agent

        An AI research assistant powered by LangGraph StateGraph with Tavily search integration.
        The agent can search the web for current information and provide comprehensive answers.

        **Two modes available:**
        1. **Single Query** - Ask one-off research questions
        2. **Multi-turn Chat** - Have a conversation with memory
        """
    )

    with gr.Tabs():
        # Tab 1: Single Query
        with gr.TabItem("Single Query"):
            gr.Markdown("### Ask a research question")
            query_input = gr.Textbox(
                label="Your Question",
                placeholder="What are the latest developments in AI agents?",
                lines=3
            )
            query_btn = gr.Button("Research", variant="primary")
            query_output = gr.Textbox(label="Response", lines=10)

            query_btn.click(
                fn=single_query,
                inputs=query_input,
                outputs=query_output
            )

        # Tab 2: Multi-turn Chat
        with gr.TabItem("Multi-turn Chat"):
            gr.Markdown("### Research conversation with memory")
            gr.Markdown("*The agent remembers context from previous messages in the same conversation.*")

            chatbot = gr.Chatbot(height=400)
            conversation_id = gr.State("")

            msg = gr.Textbox(
                label="Your message",
                placeholder="Ask me anything...",
                lines=2
            )
            with gr.Row():
                send_btn = gr.Button("Send", variant="primary")
                new_btn = gr.Button("New Conversation", variant="secondary")

            # Initialize conversation on load
            demo.load(
                fn=new_conversation,
                outputs=[chatbot, conversation_id]
            )

            msg.submit(
                fn=chat_response,
                inputs=[msg, chatbot, conversation_id],
                outputs=[msg, chatbot]
            )
            send_btn.click(
                fn=chat_response,
                inputs=[msg, chatbot, conversation_id],
                outputs=[msg, chatbot]
            )
            new_btn.click(
                fn=new_conversation,
                outputs=[chatbot, conversation_id]
            )

    # Example queries
    gr.Markdown("### Example Research Questions")
    gr.Examples(
        examples=[
            ["What are the latest developments in AI agents and autonomous systems?"],
            ["Compare LangGraph and LangChain for building AI applications."],
            ["What is retrieval augmented generation (RAG) and how does it work?"],
            ["What are the top AI trends in 2024?"],
        ],
        inputs=query_input,
    )

if __name__ == "__main__":
    demo.launch()
