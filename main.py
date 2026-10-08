import streamlit as st

from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

from agent import agent, messages as base_messages

if "history" not in st.session_state:
    st.session_state.history = list(base_messages)

st.title("hospital chat_bot")

user_text = st.chat_input("Введіть повідомлення")

if user_text is not None:
    human_message = HumanMessage(content=user_text)
    st.session_state.history.append(human_message)

    result = agent.invoke({"messages": st.session_state.history})
    st.session_state.history = result["messages"]

for message in st.session_state.history:
    if isinstance(message, (SystemMessage, ToolMessage)):
        continue
    if not message.text:
        continue
    role = "user" if isinstance(message, HumanMessage) else "AI"
    with st.chat_message(role):
        st.markdown(message.text)
