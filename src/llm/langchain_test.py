import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=GROQ_API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"

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

# simple_chat()   #without history

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


result = chain.invoke({"text": "I am living in Hanoi or Paris."})
print(result.city)

