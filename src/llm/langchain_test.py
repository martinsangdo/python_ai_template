import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"  #fake the model name to see crash in Langsmith


def simple_chat():
    continue_chating = True
    while continue_chating:
        user_input = input("You: ")
        if user_input == "quit":
            continue_chating = False
        else:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": user_input}],
            )
            print(completion.choices[0].message.content)

simple_chat()   #without history

def stream_with_history():
    history = [{"role": "system", "content": "You are a fast AI assistant."}]
    continue_chating = True
    while continue_chating:
        user_input = input("You: ")
        if user_input == "quit":
            continue_chating = False
        else:
            history.append({"role": "user", "content": user_input})
            stream = client.chat.completions.create( model=MODEL_NAME, messages=history, stream=True)
            print("AI: ", end="")
            full_response = ""
            for chunk in stream:
                # Check if there is content in the chunk
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_response += content
            print("\n")
            # Save the full response so the AI remembers it next time
            history.append({"role": "assistant", "content": full_response})
            # print('history', history)

# stream_with_history()

def summarize_history(old_messages):
    summary_prompt = f"Summarize the key points of this conversation in 2 sentences: {old_messages}"
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": summary_prompt}]
    )
    return response.choices[0].message.content

#///////////// 
from pydantic import BaseModel
class CityCountry(BaseModel):
    city: str
    country: str


from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq
from langchain.globals import set_verbose, set_debug
set_verbose(True)

parser = JsonOutputParser()

model = ChatGroq(model=MODEL_NAME)
structured_llm = model.with_structured_output(CityCountry)
chain = ChatPromptTemplate.from_template("Extract the city and country from: {text}.") | structured_llm


#Return ONLY a JSON list of objects with 'city' and 'country' keys.
# chain = ChatPromptTemplate.from_template("Extract the city and country from: {text}.") | model | parser

# result = chain.invoke({"text": "I am living in Hawaii."})
# print(result.city)

from typing import List
from pydantic import BaseModel

# 1. Define what ONE location looks like
class Location(BaseModel):
    city: str
    country: str

# 2. Define the FINAL structure as a LIST of locations
class LocationsList(BaseModel):
    locations: List[Location]

# 3. Bind the list schema to the model
structured_llm = model.with_structured_output(LocationsList)
chain = ChatPromptTemplate.from_template("Extract the city and country from: {text}.") | structured_llm

# 4. Invoke
# result = chain.invoke({"text": "I am living in Hanoi or Paris."})

# 5. Print the results
# for item in result.locations:
#     print(item.city)


#test pull prompt from hub
from langchain import hub

# prompt = hub.pull("check_python_syntax")
# chain = prompt | model
# result = chain.invoke({"sentence": "var b = 9;"})
# print(result.content)

#compare prompts
v1_template = ChatPromptTemplate.from_template("Explain this concept: {input}")
# hub.push("it-tutor", v1_template)

v2_template = ChatPromptTemplate.from_messages([
    ("system", "You are a strict IT instructor. Explain concepts but NEVER give the direct answer to coding homework. Use technical analogies."),
    ("human", "{input}")
])
# Pushing to the same name creates 'Version 2' automatically
# hub.push("it-tutor", v2_template)

### Test the tokens used
# chain = v2_template | model
# response = chain.invoke({"input": "What is DevOps?"})
# # Most providers store this in usage_metadata
# print(f"Prompt Tokens: {response.usage_metadata['input_tokens']}")
# print(f"Completion Tokens: {response.usage_metadata['output_tokens']}")
# print(f"Total Tokens: {response.usage_metadata['total_tokens']}")