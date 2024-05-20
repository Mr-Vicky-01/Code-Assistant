import streamlit as st
import os
import google.generativeai as genai
import time

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

icons = {"assistant": "robot.png", "user": "man-kddi.png"}

model = genai.GenerativeModel('gemini-1.5-flash-latest')
prompt = """You are a programming teaching assistant named GenXAI(Generative eXpert AI), created by Pachaiappan [linkdin](https://www.linkedin.com/in/pachaiappan) an AI Specialist. Answer only the programming, error-fixing and code-related question that being asked. 
Important note, If Question non-related to coding or programming means, you have to say: 'Please ask only coding-related questions.' except those kind of questions "who are you", "who created you".
previous_chat:  
{chat_history}
Human: {human_input}
Chatbot:"""

previous_response = ""
def get_response(query):
    global previous_response
    
    for i in st.session_state['history']:
        if i is not None:
            previous_response += f"Human: {i[0]}\n Chatbot: {i[1]}\n"

    response = model.generate_content(prompt.format(human_input=query, chat_history=previous_response))
    st.session_state['history'].append((query, response.text))
    return response.text


def response_streaming(text):
    for i in text:
        yield i
        time.sleep(0.001)

st.title("GenXAi")
st.caption("I am Generative EXpert Assistant for Programming Related Task!")

st.markdown("""
    <style>
    .justified-text {
        text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.header("ABOUT:")
    
    st.caption("""
        <div class="justified-text">
            This is GenXai (Generation Expert AI), designed to assist with programming-related questions. This AI can help you answer your coding queries, fix errors, and much more. Additionally, you can chat with GenXai to build and refine your questions, facilitating a more productive conversation.
        </div>
        """, unsafe_allow_html=True)
    
    for _ in range(17):
        st.write("") 
    st.subheader("Build By:")
    st.write("[Pachaiappan❤️](https://github.com/Mr-Vicky-01)")
    st.write("contact: [Email](mailto:pachaiappan1102@gamil.com)")

if 'messages' not in st.session_state:
    st.session_state.messages = [{'role': 'assistant', 'content': "I'm Here to help your programming realted questions😉"}]

if 'history' not in st.session_state:
    st.session_state.history = [] 

for message in st.session_state.messages:
    with st.chat_message(message['role'], avatar=icons[message['role']]):
        st.write(message['content'])
        
user_input = st.chat_input("Ask Your Questions 👉..")
if user_input:
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    with st.chat_message("user", avatar="man-kddi.png"):
        st.write(user_input)
        
    with st.spinner("Thinking..."):
        response = get_response(user_input)
        
    with st.chat_message("user", avatar="robot.png"):
        st.write_stream(response_streaming(response))
        
    message = {"role": "assistant", "content": response}
    st.session_state.messages.append(message) 