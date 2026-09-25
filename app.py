import streamlit as st
import ollama
import requests
import json
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Ollama Local Chat", page_icon="🤖", layout="wide")

# Custom CSS for better chat appearance
st.markdown("""
    <style>
        .stChatMessage {
            border-radius: 15px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .stChatInputContainer {
            padding-bottom: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# --- UTILITY FUNCTIONS ---
def check_ollama_connection():
    """Check if the Ollama server is running on the local machine."""
    try:
        requests.get("http://localhost:11434/api/tags", timeout=2)
        return True
    except requests.exceptions.RequestException:
        return False

def get_available_models():
    """Fetch the list of models already pulled to the local Ollama instance."""
    try:
        models_info = ollama.list()
        return [m['name'] for m in models_info['models']]
    except Exception:
        return ["llama3", "mistral", "phi3"]

def response_generator(model, messages, options):
    """Generator to yield content chunks from Ollama for streaming."""
    try:
        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True,
            options=options
        )
        for chunk in stream:
            yield chunk['message']['content']
    except Exception as e:
        yield f"\n\n**Error:** {str(e)}"

def save_conversation():
    """Saves the current conversation to a JSON file."""
    if not st.session_state.messages:
        st.warning("No conversation to save!")
        return

    filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(st.session_state.messages, f, ensure_ascii=False, indent=4)
    st.success(f"Conversation saved to {filename}")

def export_transcript():
    """Exports the current conversation to a plain text file."""
    if not st.session_state.messages:
        st.warning("No conversation to export!")
        return

    text_content = ""
    for msg in st.session_state.messages:
        text_content += f"{msg['role'].capitalize()}: {msg['content']}\\n\\n"

    filename = f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text_content)
    st.success(f"Transcript exported to {filename}")

def load_conversation(uploaded_file):
    """Loads a conversation from an uploaded JSON file."""
    try:
        data = json.load(uploaded_file)
        if isinstance(data, list):
            st.session_state.messages = data
            st.success("Conversation loaded successfully!")
            st.rerun()
        else:
            st.error("Invalid file format. Expected a JSON list of messages.")
    except Exception as e:
        st.error(f"Error loading file: {e}")

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Configuration")

    # 1. Connection Status
    if not check_ollama_connection():
        st.error("🚨 Ollama is not running!")
        st.info("Please start the Ollama app on your machine to use this chatbot.")
        st.stop()
    else:
        st.success("✅ Ollama server connected")

    # 2. Model Selection
    available_models = get_available_models()
    selected_model = st.selectbox(
        "Select AI Model",
        options=available_models,
        help="Choose a model you have already 'pulled' via the Ollama CLI."
    )

    # 3. Persona/System Prompt
    system_prompt = st.text_area(
        "System Prompt",
        value="You are a helpful, concise, and friendly AI assistant.",
        help="Define the personality and constraints of the AI."
    )

    st.divider()
    st.subheader("🎚️ Model Parameters")

    # Model Hyperparameters
    temp = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1, help="Higher = more creative, Lower = more deterministic")
    top_p = st.slider("Top-P", 0.0, 1.0, 0.9, 0.05, help="Nucleus sampling: only considers top P% of probability mass")
    top_k = st.slider("Top-K", 1, 100, 40, 1, help="Only considers the top K most likely tokens")
    max_tokens = st.slider("Max Tokens", 128, 4096, 2048, 128, help="Limits the maximum length of the response")

    # Bundle options for Ollama
    model_options = {
        "temperature": temp,
        "top_p": top_p,
        "top_k": top_k,
        "num_predict": max_tokens
    }

    st.divider()
    st.subheader("📁 Conversation Management")

    # Save/Load/Export/Clear
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save JSON", use_container_width=True):
            save_conversation()
    with col2:
        if st.button("📄 Export TXT", use_container_width=True):
            export_transcript()

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    uploaded_file = st.file_uploader("Restore Chat (JSON)", type="json")
    if uploaded_file:
        load_conversation(uploaded_file)

# --- CHAT LOGIC ---

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Local AI Chatbot")
st.caption(f"Currently using: **{selected_model}** | Temp: {temp} | Top-P: {top_p}")

# Render existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input handling
if prompt := st.chat_input("Ask me anything..."):
    # Input Validation
    if not prompt.strip():
        st.warning("Please enter a message.")
    else:
        # 1. Append and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Generate and display assistant response
        with st.chat_message("assistant"):
            # Combine system prompt with chat history
            full_messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

            # Use st.write_stream for a professional typing effect
            # We pass the generator function with the specified options
            final_response = st.write_stream(response_generator(selected_model, full_messages, model_options))

            # Append the final accumulated response to history
            st.session_state.messages.append({"role": "assistant", "content": final_response})
