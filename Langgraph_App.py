# Model creation and initialization.
import getpass
import os

os.environ["GROQ_API_KEY"]="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"

from langchain.chat_models import init_chat_model
model=init_chat_model("llama3-8b-8192",model_provider="groq")

# Prompt template creation. 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt_template=ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "you are a helpful assistant, answer all the questions to best of your knowledge in German."
        ),
        MessagesPlaceholder(variable_name="messages")
    ]
)

from typing import Sequence
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START,MessagesState, StateGraph
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import Annotated, TypedDict

class State(TypedDict):
    messages:Annotated[Sequence[BaseMessage],add_messages]
    language=str

workflow=StateGraph(state_schema=State)

def call_model(state:State):
    prompt=prompt_template.invoke({"messages":state["messages"]})
    response=model.invoke(prompt)
    return {"messages":[response]}

workflow.add_edge(START,"model")
workflow.add_node("model",call_model)

memory=MemorySaver()
app=workflow.compile(checkpointer=memory)

