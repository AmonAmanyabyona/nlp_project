#full_flowV2.py
import streamlit as st
from user_interaction_moduleV2 import show_user_interaction
from chat_flow_moduleV2 import show_chat_flow

# Page config
st.set_page_config(page_title="Dashboard", layout="centered")

# Initialize selected flow
if "selected_flow" not in st.session_state:
    st.session_state.selected_flow = "Home"

# Sidebar navigation using simple buttons
st.sidebar.title("📂Chatbot Navigation")

if st.sidebar.button("🏠 Home"):
    st.session_state.selected_flow = "Home"
if st.sidebar.button("🧠 User Interaction Flow"):
    st.session_state.selected_flow = "User Interaction Flow"
if st.sidebar.button("💬 Chat Flow"):
    st.session_state.selected_flow = "Chat Flow"

#Route based on selection
selected_flow = st.session_state.selected_flow

if selected_flow == "Home":
    st.title("🧠 Wikiquote Chatbot Dashboard")
    st.markdown("""
    Welcome to the **Wikiquote Showcase using LLAMA model**

    Explore two powerful chatbot experiences:
    - 🧠 **User Interaction Flow**: Reveals matched quotes before responding
    - 💬 **Chat Flow**: Responds instantly without showing quotes

    Use the sidebar to jump between chatbot modes and test how each behaves.
    """)

elif selected_flow == "User Interaction Flow":
    show_user_interaction()

elif selected_flow == "Chat Flow":
    show_chat_flow()
