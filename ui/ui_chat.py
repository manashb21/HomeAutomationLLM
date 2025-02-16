import streamlit as st
import requests

# API URL
FASTAPI_URL = "http://localhost:8000/generate"

st.title("💡 Light Automation Assistant")
# Dropdown for model selection
model_options = ["Llama 3.2 1B fine-tuned q4", "Qwen 2.5 0.5B fine-tuned q4"]
selected_model = st.selectbox("Select Model:", model_options, index=0)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
prompt = st.chat_input("How can I help you?")
if prompt:
    # Display user input
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Function to handle response streaming
    def response_generator():
        response = requests.post(
            FASTAPI_URL, json={"prompt": prompt, "model": selected_model}, stream=True
        )
        if response.status_code == 200:
            for chunk in response.iter_content(chunk_size=16):
                if chunk:
                    yield chunk.decode("utf-8")
        else:
            yield "❌ Error generating response! Check the backend."

    # Display assistant response in chat (streaming)
    with st.chat_message("assistant"):
        response_text = st.write_stream(response_generator())  # Streaming response dynamically
        st.session_state.messages.append({"role": "assistant", "content": response_text})
