import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Assistant Chat",
    layout="wide"
)

# --- CUSTOM STYLING (CSS) ---
st.markdown("""
<style>
    /* Hide the default Streamlit header and footer */
    header, footer {
        visibility: hidden;
    }

    /******************************************************************
     * THE MAIN CHANGE IS HERE: Updated the .stApp background.        *
     ******************************************************************/
    .stApp {
        background-image: linear-gradient(135deg, #00EFF0 0%, #E0E2E6 100%);
        background-attachment: fixed; /* Keeps the gradient fixed during scroll */
    }

    /******************************************************************
     * Sidebar Styling (Unchanged)                                    *
     ******************************************************************/
    [data-testid="stSidebar"] {
        background-color: #1C1C1E;
        padding-top: 2rem;
    }

    .sidebar-text {
        color: #BFBFBF;
        font-size: 16px;
        padding: 10px 20px;
        display: block;
        font-weight: 500;
    }

    .sidebar-text:hover {
        background-color: #333333;
        color: white;
        text-decoration: none;
    }

    /******************************************************************
     * Main Chat Area Styling (Text colors updated for contrast)      *
     ******************************************************************/

    /* Title styling - now dark */
    h1 {
        color: #2E2E2E; /* UPDATED: Dark text for readability */
        font-weight: bold;
        padding-top: 1rem;
    }

    /* Assistant message styling - now dark */
    div[data-testid="stChatMessage"]:has(div[data-testid="chat-bubble-avatar-assistant"]) [data-testid="stChatMessageContent"] {
       color: #2E2E2E; /* UPDATED: Dark text */
       background-color: transparent;
    }

    /* Assistant avatar styling */
    [data-testid="chat-bubble-avatar-assistant"] {
        background-color: #2E2E2E;
        border-radius: 50%;
    }
    
    [data-testid="chat-bubble-avatar-assistant"] > div {
        color: white;
    }

    /* Timestamp styling - now dark */
    [data-testid="chat-message-timestamp"] {
        font-size: 0.75rem;
        color: #444444; /* UPDATED: Dark grey text */
        padding-top: 8px;
        padding-left: 58px;
        position: relative;
        top: -10px;
    }
    
    /******************************************************************
     * Floating Chat Input Bar Styling (Unchanged)                    *
     ******************************************************************/
    [data-testid="stChatFloatingInputContainer"] {
        background-color: #1C1C1E;
        padding: 10px 20px;
        border-top: 2px solid #000000;
        box-shadow: none;
    }

    [data-testid="stChatInput"] > div {
        background-color: #333333;
        border: none;
        border-radius: 12px;
    }
    
    [data-testid="baseButton-secondary"] {
        background-color: #333333;
        border-radius: 8px;
    }
    
    [data-testid="baseButton-secondary"]:hover {
        background-color: #444444;
    }

    [data-testid="baseButton-secondary"] svg {
        fill: #BFBFBF;
    }

</style>
""", unsafe_allow_html=True)


# --- APPLICATION LOGIC ---

st.markdown("<h1>AI Assistant Chat 🔗</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm Robin's AI assistant. How can I help you today?", "time": "02:23 PM"}
    ]

for message in st.session_state.messages:
    # Set avatar icon based on role
    avatar_icon = "🤖" if message["role"] == "assistant" else "😊"
    with st.chat_message(message["role"], avatar=avatar_icon):
        st.write(message["content"])
        # Custom div to apply specific timestamp styling
        st.markdown(f'<div data-testid="chat-message-timestamp">{message["time"]}</div>', unsafe_allow_html=True)


# Capture user input from the chat box
if prompt := st.chat_input("Type your message here..."):
    current_time = "12:04 PM"
    
    st.session_state.messages.append({"role": "user", "content": prompt, "time": current_time})
    with st.chat_message("user", avatar="😊"):
        st.write(prompt)
        st.markdown(f'<div data-testid="chat-message-timestamp">{current_time}</div>', unsafe_allow_html=True)
        
    error_response = "API Error: Failed to fetch. Please check if your server is running."
    st.session_state.messages.append({"role": "assistant", "content": error_response, "time": current_time})
    with st.chat_message("assistant", avatar="🤖"):
        st.write(error_response)
        st.markdown(f'<div data-testid="chat-message-timestamp">{current_time}</div>', unsafe_allow_html=True)