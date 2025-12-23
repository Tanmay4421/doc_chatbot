from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse
from graph.graph import build_graph

router = APIRouter()
graph = build_graph()

@router.post("/chat", response_class=PlainTextResponse)
def chat(
    message: str = Query(...),
    thread_id: str = Query(...),
    collection_name: str = Query(...)
):
    config = {"configurable": {"thread_id": thread_id}}

    final_message = ""

    for event in graph.stream(
        {
            "messages": message,
            "collection_name": collection_name,
        },
        config,
    ):

        if "chat" in event:
            print(event["chat"]["messages"])
            print(event["chat"].values())
            final_message = event["chat"]["messages"].content
    print(final_message)
    return final_message
