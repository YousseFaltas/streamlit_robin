import streamlit as st
import time
import requests
import re

FASTAPI_URL = "https://ae94f64c684a.ngrok-free.app"

# --- LOGIN LOGIC (MODIFIED) ---

def check_login():
    """Displays an email login form and returns True if the email is valid."""
    st.set_page_config(page_title="Login - Robin AI", layout="centered")
    st.title("Welcome to Robin 🤖")
    st.markdown("Please enter your email to continue.")

    # CSS to style the text input container
    st.markdown("""
    <style>
        /* This targets the container holding the input field */
        [data-testid="stTextInput"] {
            border: 3px solid black !important;
            border-radius: 10px !important;
        }
        
        /* This ensures the actual input field inside has no border */
        div[data-baseweb="base-input"] {
            border: none !important;
            background-color: transparent !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Wrap the form in a div with the "login-container" class
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    with st.form("login_form"):
        # --- THIS IS THE KEY CHANGE ---
        email = st.text_input(
            "Email", 
            placeholder="Email", 
            label_visibility="collapsed", 
            key="email_input"
        )
        
        submitted = st.form_submit_button("Login")

        if submitted:
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if re.match(email_regex, email):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please enter a valid email address.")

    st.markdown('</div>', unsafe_allow_html=True)
    return False

# --- MAIN APP ---
# Function to simulate a response
def response(prompt):
    """
    Sends a prompt to the FastAPI backend and gets the response.
    """
    payload = {
        "message": prompt,
        "identifier": "x"  # Using a fixed identifier as requested
    }
    try:
        # Send a POST request to the FastAPI endpoint
        api_response = requests.post(FASTAPI_URL, json=payload)
        
        # Check for a successful response
        if api_response.status_code == 200:
            response_data = api_response.json()
            return response_data.get("answer", "Sorry, I couldn't get a valid response.")
        else:
            # Handle non-200 responses
            error_detail = api_response.json().get('detail', 'Unknown error')
            return f"Error from server: {error_detail}"

    except requests.exceptions.RequestException as e:
        # Handle connection errors
        st.error(f"Could not connect to the FastAPI server at {FASTAPI_URL}. Please ensure it is running.")
        return "Sorry, I'm having trouble connecting to my brain right now."
    
def main_app():
    st.set_page_config(page_title="Robin - AI Chatbot", page_icon="🤖")

    st.title("Welcome to Robin 🤖")
    st.markdown("Your Data Science & AI Partner")

    # Initialize session state variables
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "processing" not in st.session_state:
        st.session_state.processing = False

    # backgroundColor="#76dfd1ff"

    st.markdown("""
    <style>
        [data-testid="stHeader"] {
            display: none;
        }
        [data-testid="stAppViewContainer"] {
            /* A 5-stop gradient for an ultra-smooth transition */
            background: linear-gradient(
                to bottom, 
                #00EFF0 5%,   /* Original strong cyan */
                #A0F5F5 30%,  /* Your first light cyan */
                #CFFBFB 55%,  /* New: Very pale cyan */
                #EFFFFF 75%,  /* New: Almost white with a hint of cyan */
                #FFFFFF 90%   /* Final pure white */
            );
            background-attachment: fixed;
        }
        /* Target the chat input container */
        /* Main container for the chat input */
        [data-testid="stChatInput"] {
            /* This is the outer black border from your image */
            border: 3px solid black;
            border-radius: 25px; /* Adjust for more or less rounding */
            background-color: white; /* Ensures a solid background */
        }

        /* This targets the inner input field where the red highlight appears */
        div[data-baseweb="base-input"] {
            /* Removes the default border of the inner field */
            border: none !important;
            box-shadow: none !important; /* Removes any shadow effect */
        }

        /* This specifically handles the focused state */
        div[data-baseweb="base-input"]:focus-within {
            /* Removes the red border/shadow on focus */
            border: none !important;
            box-shadow: none !important;
        }
    </style>
    """, unsafe_allow_html=True)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        assistant_response = "Hi , how can i help you today?"
        message_placeholder.markdown(assistant_response)

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
            full_response = ""
            with st.spinner("Thinking..."):
                assistant_response = response(last_prompt)
                
                # Iterate over lines instead of words
                for line in assistant_response.splitlines():
                    for chunk in line.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        message_placeholder.markdown(full_response + "▌")
                    full_response = full_response + "\n"
                
                # Final display without the cursor
                message_placeholder.markdown(full_response)
            
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        
        st.session_state.processing = False
        st.rerun()


# --- APP ROUTER ---

# Initialize session state for login status if it doesn't exist
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Display login page or main app based on login status
if st.session_state.logged_in:
    main_app()
else:
    check_login()