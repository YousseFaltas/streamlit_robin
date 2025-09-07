import streamlit as st
import time

# backgroumd color background: linear-gradient(to bottom, #00EFF0 5%, #FFFFFF 40%);

# Page configuration
st.set_page_config(page_title="Robin - AI Chatbot", page_icon="🤖")

# --- STYLES ---
st.markdown("""
<style>
    /* More reliable selector for the main background */
    [data-testid="stAppViewContainer"] {
        /* Gradient background from your palette */
        background: linear-gradient(to bottom, #00EFF0 5%, #FFFFFF 40%);
        background-attachment: fixed;
    }

    /* Main header style */
    .st-emotion-cache-10trblm {
        color: #2E2E2E; /* Dark Grey for better contrast on gradient */
        font-family: 'monospace', sans-serif;
    }

    /* User message style */
    .st-emotion-cache-1c7y2kd {
        background-color: #00F700; /* Bright Green */
        border-radius: 20px 20px 5px 20px;
        padding: 10px;
        color: #2E2E2E; /* Dark text for contrast */
    }

    /* Bot message style */
    .st-emotion-cache-4oy321 {
        background-color: #FFFFFF; /* White for bot messages */
        border-radius: 20px 20px 20px 5px;
        padding: 10px;
        color: #2E2E2E; /* Dark Grey for text */
    }
    
    /* Base style for the input box */
    .stTextInput > div > div > input {
        background-color: #FFFFFF;
        color: #2E2E2E; /* Dark Grey for input text */
        border-radius: 10px;
        border: 2px solid #BFBFBF; /* Neutral light grey border */
        transition: border-color 0.3s ease, box-shadow 0.3s ease; /* Smooth transition */
    }
    
    /* Style for the input box WHEN FOCUSED (selected) */
    .stTextInput > div > div > input:focus {
        border-color: #00F700; /* Bright green border on focus */
        box-shadow: 0 0 5px #00F700; /* Add a subtle glow */
        outline: none; /* REMOVES THE BLACK/BLUE OUTLINE */
    }

    /* Send button style */
    .stButton > button {
        background-color: #00F700; /* Bright Green */
        color: #2E2E2E; /* Dark Grey text */
        border-radius: 10px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #A2FBAC; /* Lighter Green on hover */
        color: #2E2E2E;
    }

</style>
""", unsafe_allow_html=True)


# --- CHATBOT LOGIC ---

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "processing" not in st.session_state:
    st.session_state.processing = False

# Function to simulate a response
def generate_response(prompt):
    if "hello" in prompt.lower():
        return "Hi there! How can Robin's data science expertise help you today?"
    elif "data" in prompt.lower():
        return "Robin specializes in data analysis, machine learning models, and data visualization. What are you interested in?"
    elif "services" in prompt.lower():
        return "We offer a range of services from predictive analytics to natural language processing. Can I provide more details on a specific service?"
    else:
        return "That's an interesting question! As a demo bot, I have limited responses. A real Robin data scientist could provide a much more detailed answer."

# --- MAIN CHATBOT INTERFACE ---
st.title("Welcome to Robin 🤖")
st.markdown("Your Data Science Solutions Partner")

# Display prior chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("How can we help you?", disabled=st.session_state.processing, key="chat_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.processing = True
    st.rerun()

# Generate and display bot response if processing
if st.session_state.processing:
    last_prompt = st.session_state.messages[-1]["content"]
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = generate_response(last_prompt)
        
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    st.session_state.processing = False
    st.rerun()