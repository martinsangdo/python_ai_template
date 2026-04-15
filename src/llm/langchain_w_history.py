from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv(override=True)

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"
# 1. Setup
model = ChatGroq(model=MODEL_NAME)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

chain = prompt | model

# 3. Use a simple Python list to store messages
# We use HumanMessage and AIMessage objects
memory = []
def chat(user_input):
    response = chain.invoke({
        "input": user_input,
        "chat_history": memory
    })
    memory.append(HumanMessage(content=user_input))
    memory.append(AIMessage(content=response.content))
    return response.content

# --- Test it ---
print(chat("Hi, I'm an IT instructor from Hanoi."))
print(chat("What was the city I just mentioned?"))