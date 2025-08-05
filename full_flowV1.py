#full_flowV1.py
import streamlit as st
from user_interaction_module import show_user_interaction
from chat_flow_module import show_chat_flow

#Page config
st.set_page_config(page_title="Chatbot Dashboard", layout="centered")

#Sidebar Navigation
st.sidebar.title("📂 Select Flow")
selected_flow = st.sidebar.radio("Pick a mode to explore:", ["Home", "User Interaction Flow", "Chat Flow"])

#Welcome Page
if selected_flow == "Home":
    st.title("🧠 Wikiquote Dashboard")
    st.markdown("""
    Welcome to the **Wikiquote Chatbot Showcase using GPT-4o**

    This app demonstrates two interaction styles:
    - 🤖 **User Interaction Flow**: See quotes before chatting
    - 💬 **Chat Flow**: Responds instantly without showing quotes

    Use the sidebar to switch between chatbot modes and explore how each one works!
    """)

#Run User Interaction Script
elif selected_flow == "User Interaction Flow":
    show_user_interaction()

#Run Chat Flow Script
elif selected_flow == "Chat Flow":
    show_chat_flow()
