
import streamlit as st
from groq import Groq

# Add name to the page and icon
st.set_page_config(page_title="AI chat", page_icon="./media/AIchat.png", layout="centered")
# page title
st.title("My first st app")
# text input
name = st.text_input("What's your name?")
# greetings button
if (st.button("Hi")):
    st.write(f"Hi {name}, Welcome to this chatbot")
models = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']
def setupPage():
    #aad title to the page
    st.title("My AI chat")
    st.sidebar.title("AI settings") 
    chooseModel = st.sidebar.selectbox("Please, choose a model", options= models, index=0)
    return chooseModel

# 7th class
def createGroqUser():
    key = st.secrets["key"]
    return Groq(api_key=key)
def setupModel (client, model, entryMsj):
    return client.chat.completions.create(
        model= model,
        messages = [{"role": "user", "content": entryMsj}],
        stream = True
    )
def initializeState():
    if "messages" not in st.session_state:
        st.session_state.messages=[]

def updateHistory(role, content, avatar):
    st.session_state.messages.append(
    {"role":role, 
    "content":content, 
    "avatar":avatar
    })
def showHistory():
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"])
def chatArea(): 
    with st.container(): showHistory()

def generate_answer(complete_chat):
    complete_answer = ""
    for phrase in complete_chat:
        if phrase.choices[0].delta.content:
            complete_answer += phrase.choices[0].delta.content
            yield phrase.choices[0].delta.content
    return complete_answer
    
def main():
    model = setupPage()
    userClient = createGroqUser()
    initializeState()
    chatArea() 
    message = st.chat_input("Please, write a message")
    if message:
        updateHistory("user",message,"🧑🏻‍💻")
        complete_chat = setupModel(userClient, model, message) #

        if complete_chat: 
            with st.chat_message("assistant"):
                complete_answer = st.write_stream(generate_answer(complete_chat))
                updateHistory("assistant", complete_answer, "🤖")

                st.rerun()

if __name__ == "__main__":
    main()