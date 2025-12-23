from typing import Optional, List
from langgraph.graph import MessagesState
from langmem.short_term import RunningSummary

class State(MessagesState):
    context: dict[str, RunningSummary]
    retrieved_docs: Optional[List[str]] = None
    collection_name: Optional[str] = None
