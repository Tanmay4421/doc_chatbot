from typing import TypedDict, List
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain.messages import AnyMessage, SystemMessage
from langchain_core.messages.utils import count_tokens_approximately
from langmem.short_term import SummarizationNode

from memory.qdrant import get_retriever

# ------------------------------------------------------------------
# Environment
# ------------------------------------------------------------------

load_dotenv(dotenv_path="creds.env")

# ------------------------------------------------------------------
# Models
# ------------------------------------------------------------------

model = init_chat_model(
    "gpt-4.1-mini",
    streaming=True,
)

summarization_model = model.bind(max_tokens=128)

# ------------------------------------------------------------------
# Summarization node (LangGraph node)
# ------------------------------------------------------------------

summarize_node = SummarizationNode(
    token_counter=count_tokens_approximately,
    model=summarization_model,
    max_tokens=256,
    max_tokens_before_summary=256,
    max_summary_tokens=128,
)

# ------------------------------------------------------------------
# State schema
# ------------------------------------------------------------------

class LLMInput(TypedDict, total=False):
    messages: List[AnyMessage]
    summarized_messages: List[AnyMessage]
    context: dict
    retrieved_docs: List[str]
    collection_name: str | None

# ------------------------------------------------------------------
# Retriever node
# ------------------------------------------------------------------

def retrieve_node(state: LLMInput):
    if not state.get("collection_name") or not state.get("messages"):
        return {"retrieved_docs": []}

    retriever = get_retriever(state["collection_name"])
    query = state["messages"][-1].content
    docs = retriever.invoke(query)

    return {
        "retrieved_docs": [d.page_content for d in docs]
    }

# ------------------------------------------------------------------
# Chat node
# ------------------------------------------------------------------

def chat_node(state: LLMInput):
    # SummarizationNode guarantees this *if it ran*
    running_summary = (
        state.get("context", {})
        .get("running_summary")
    )

    summary = running_summary.summary if running_summary else ""

    docs = "\n".join(state.get("retrieved_docs", []))

    system = SystemMessage(
        content=f"""
Conversation summary:
{summary}

Relevant documents:
{docs}
"""
    )

    return {
        "messages": model.invoke(
            [system, *state.get("summarized_messages", [])],
            stream=True,
        )
    }
