import sys
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except AttributeError:
    pass
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, BaseMessage, ToolMessage, AIMessage
from tools import (
    search_flights, search_hotels, calculate_budget,
    search_by_budget, compare_options, get_trip_summary,
)
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# 1. Đọc System Prompt
# ==================================================
with open("system_prompt.txt", "r", encoding="utf-8", errors="ignore") as f:
    SYSTEM_PROMPT = f.read()


# ==================================================
# 2. Khai báo State
# ==================================================
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# ==================================================
# 3. Khởi tạo LLM và Tools
# ==================================================
tools_list = [
    search_flights,
    search_hotels,
    calculate_budget,
    search_by_budget,
    compare_options,
    get_trip_summary,
]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)


# ==================================================
# 4. Agent Node
# ==================================================
def _clean(text):
    """Remove surrogate characters that break UTF-8 encoding on Windows."""
    if isinstance(text, str):
        return text.encode("utf-8", errors="replace").decode("utf-8")
    return text


def _sanitize_messages(messages):
    """Sanitize all message content to remove surrogates."""
    sanitized = []
    for msg in messages:
        if isinstance(msg, BaseMessage) and isinstance(msg.content, str):
            msg = msg.model_copy(update={"content": _clean(msg.content)})
        sanitized.append(msg)
    return sanitized


MAX_TOOL_CALLS = 5


def agent_node(state: AgentState) -> dict:
    messages = _sanitize_messages(state["messages"])

    # Gắn system prompt vào đầu nếu chưa có
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    # Đếm số lần đã gọi tool trong lượt này
    tool_call_count = sum(1 for m in messages if isinstance(m, ToolMessage))

    if tool_call_count >= MAX_TOOL_CALLS:
        print(f"⚠️ Đã đạt giới hạn {MAX_TOOL_CALLS} lần gọi tool, buộc trả lời.")
        # Gọi LLM không có tools để buộc trả lời trực tiếp
        response = llm.invoke(messages)
    else:
        response = llm_with_tools.invoke(messages)

    # Logging
    if isinstance(response, AIMessage) and response.tool_calls:
        for tc in response.tool_calls:
            print(f"🔧 Gọi tool: {tc['name']}({tc['args']})")
    else:
        print("💬 Trả lời trực tiếp")

    return {"messages": [response]}


# ==================================================
# 5. Xây dựng Graph
# ==================================================
builder = StateGraph(AgentState)

# Thêm nodes
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))

# Thêm edges
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()


# ==================================================
# 6. Chat Loop
# ==================================================
# ==================================================
# 6. Chat Loop
# ==================================================
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy - Tro ly Du lich Thong minh")
    print("  Go 'quit' de thoat")
    print("=" * 60)

    conversation_history = []

    while True:
        user_input = input("\nBan: ").strip()

        if user_input.lower() in ("quit", "exit", "q"):
            print("Tam biet! Chuc ban co chuyen di vui ve!")
            break

        if not user_input:
            continue

        # Thêm tin nhắn user dạng HumanMessage
        from langchain_core.messages import HumanMessage
        conversation_history.append(HumanMessage(content=user_input))

        print("\nTravelBuddy dang suy nghi...")

        try:
            result = graph.invoke({"messages": conversation_history})
            final = result["messages"][-1]
            content = final.content
            if isinstance(content, str):
                content = content.encode("utf-8", errors="replace").decode("utf-8")
            print(f"\nTravelBuddy: {content}")
            # Cập nhật history
            conversation_history = result["messages"]

        except Exception as e:
            print(f"Loi: {e}")