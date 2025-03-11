from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from langchain_core.messages import HumanMessage, BaseMessage
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from typing import Sequence
from typing_extensions import Annotated, TypedDict
import os


# ----- Flask and SocketIO Setup -----

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


# ----- LangGraph Initialization -----

# Setting up the GROQ API Key
os.environ["GROQ_API_KEY"] = "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"

# Initializing the Llama3 model with GROQ as provider
model = init_chat_model("llama3-8b-8192", model_provider="groq")

# Prompt Template (Language is hardcoded as German)
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant, answer all the questions to the best of your knowledge in German. Format them as bullet points when in need. do not clutter on a single line please"),
    MessagesPlaceholder(variable_name="messages")
])

# LangGraph State Definition
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# Defining the workflow
workflow = StateGraph(state_schema=State)

# Function to call the model
def call_model(state: State):
    prompt = prompt_template.invoke({"messages": state["messages"]})
    response = model.invoke(prompt)
    return {"messages": [response]}

# Adding nodes and edges to the workflow
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")

# Checkpoint memory for state persistence
memory = MemorySaver()
langgraph_app = workflow.compile(checkpointer=memory)

from langchain_core.messages import HumanMessage, AIMessageChunk


# ----- Session State Management -----
# To track user sessions and messages
user_states = {}

def get_or_create_state(session_id):
    if session_id not in user_states:
        user_states[session_id] = {"messages": []}
    return user_states[session_id]


# ----- Flask Routes and SocketIO Events -----

# Home route for rendering the UI
@app.route("/")
def home():
    return render_template('index.html')

# Handling messages from the frontend
@socketio.on('message')
def handle_message(data):
    session_id = data.get("session_id")
    user_input = data.get('message')

    # Validate input
    if not session_id or not user_input:
        emit('error', {'error': 'Invalid input'})
        return

    # Get or create session state
    state = get_or_create_state(session_id)
    state['messages'].append(HumanMessage(content=user_input))

    # Invoke the LangGraph model
    response = langgraph_app.invoke(
        {"messages": state['messages']},
        config={"configurable": {"thread_id": session_id}}
    )
    answer = response['messages'][-1].content if response['messages'] else "No response"
    formatted_answer=answer.replace("•","<br>•")

    # Send back the response to the client
    emit('response', {'message': formatted_answer})


# ----- Run the Flask Server -----
if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True, allow_unsafe_werkzeug=True)