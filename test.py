import streamlit as st
from chat_completion import chat_with_model  # ← Import from your Azure script

st.title("Azure ChatGPT-like App")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What's on your mind?"):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response using Azure-hosted model
    with st.chat_message("assistant"):
        try:
            reply = chat_with_model(prompt)
            st.markdown(reply)
        except Exception as e:
            reply = f"Error: {str(e)}"
            st.error(reply)

    # Append assistant response
    st.session_state.messages.append({"role": "assistant", "content": reply})
