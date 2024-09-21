import streamlit as st
import requests
import time

# App Title and Description
st.set_page_config(page_title="Negotiation Chatbot", page_icon="🤖", layout="wide")
st.title("🛠️ Negotiation Chatbot")
st.write("This chatbot simulates a negotiation process between a customer and a supplier using AI.")

# Sidebar for additional controls
st.sidebar.header("Chatbot Controls")
initial_price = st.sidebar.slider("Initial Product Price", min_value=50, max_value=200, value=100, step=5)
min_price = st.sidebar.slider("Minimum Acceptable Price", min_value=50, max_value=200, value=75, step=5)
discount_factor = st.sidebar.slider("Discount Factor for Positive Sentiment (%)", min_value=0, max_value=100, value=20, step=1)
negotiation_power = st.sidebar.radio("Bot Negotiation Style", options=["Firm", "Flexible", "Very Flexible"])

st.sidebar.markdown("----")
# st.sidebar.write("Adjust the chatbot's behavior using these controls.")

# Chat history to keep track of the conversation
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

def display_chat_history():
    # Display chat history
    for i, chat in enumerate(st.session_state["chat_history"]):
        if chat["role"] == "user":
            st.write(f"**You**: {chat['content']}")
        else:
            st.write(f"**Chatbot**: {chat['content']}")

def add_to_chat_history(role, content):
    # Add chat messages to session state
    st.session_state["chat_history"].append({"role": role, "content": content})

# Chatbox for input
user_input = st.text_input("Enter your message or offer price:")
if st.button("Submit"):
    if user_input:
        add_to_chat_history("user", user_input)
        with st.spinner("Negotiating..."):
            # Send the user's message to the backend
            try:
                response = requests.post("http://localhost:5000/negotiate", json={"message": user_input})
                response_data = response.json()
                if response.status_code == 200:
                    chatbot_reply = response_data.get("reply", "No response from the chatbot.")
                    add_to_chat_history("chatbot", chatbot_reply)
                else:
                    st.error(f"Error: {response_data.get('error', 'Unknown error')}")
            except requests.ConnectionError:
                st.error("Connection to the backend failed. Please ensure the Flask server is running.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter a message or price before submitting.")

# Display chat history
st.write("### Chat History")
display_chat_history()

# Footer
st.markdown("---")
st.markdown("Created💡 by Anshul")

