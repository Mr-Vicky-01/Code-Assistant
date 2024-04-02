import gradio as gr
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
import os

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

llm = ChatGoogleGenerativeAI(model="gemini-pro",
                             temperature=0.7)

template = """
You are a programming teaching assistant named CodeAI, created by Pachaiappan. Answer only the programming, error-fixing and code-related question that being asked. 
Important note, If Question non-related to coding or programming means, you have to say: "Please ask only coding-related questions." except those kind of questions "who are you", "who created you".
Question: {question}
"""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt,
                     llm=llm)

def code_assistant(question):
    prediction = llm_chain.run(question)
    return prediction

input_textbox = gr.Textbox(lines=2, placeholder="Enter your code-related question here...")
output_textbox = gr.Textbox(label="Response", lines=10)

examples = [
    ["create me a reverse loop in linked list"],
    ["Implement while loop in c"],
    ["Create a simple sanke game in python"]
]

iface = gr.Interface(fn=code_assistant, inputs=input_textbox, outputs=output_textbox, title="Code Assistant", description="This AI model assist your Coding related Questions.", examples=examples)
iface.launch()