from langgraph.graph import StateGraph, START, END
from graph.state import State
from graph.nodes import summarize_node, retrieve_node, chat_node
from langgraph.checkpoint.memory import InMemorySaver

def build_graph():
    builder = StateGraph(State)

    builder.add_node("summarize", summarize_node)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("chat", chat_node)

    builder.add_edge(START, "summarize")
    builder.add_edge("summarize", "retrieve")
    builder.add_edge("retrieve", "chat")
    builder.add_edge("chat", END)
    checkpointer = InMemorySaver()

    return builder.compile(checkpointer=checkpointer)
