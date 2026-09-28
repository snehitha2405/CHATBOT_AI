import streamlit as st
import ollama

# =========================
# PAGE SETTINGS
# =========================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# =========================
# CSS
# =========================

st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #f4f6fb;
}

/* Main width */
.block-container {
    max-width: 750px;
    padding-top: 35px;
}

/* Title */
h1 {
    text-align: center;
    color: #30364b !important;
}

/* Description */
.subtitle {
    text-align: center;
    color: #667085;
    margin-bottom: 25px;
}

/* Chat input */
[data-testid="stChatInput"] {
    background-color: white;
}

/* Chat input textarea */
[data-testid="stChatInput"] textarea {
    color: #202938 !important;
}

/* Send button */
.stButton button {
    background-color: #5b5bd6 !important;
    color: white !important;
    border-radius: 8px;
    border: none;
}

.stButton button:hover {
    background-color: #4646b8 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #98a2b3;
    font-size: 13px;
    margin-top: 25px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# TITLE
# =========================

st.title("🤖 AI Chatbot")

st.markdown(
    '<div class="subtitle">'
    'Ask questions and chat with your local AI assistant.'
    '</div>',
    unsafe_allow_html=True
)


# =========================
# CHAT HISTORY
# =========================

if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================
# DISPLAY CHAT HISTORY
# =========================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        # Markdown allows proper text, formatting and code
        st.markdown(message["content"])


# =========================
# USER INPUT
# =========================

user_input = st.chat_input(
    "Ask me anything..."
)


# =========================
# SEND TO OLLAMA
# =========================

if user_input:

    # Display user's message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Get AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = ollama.chat(
                    model="llama3.2",
                    messages=st.session_state.messages
                )

                ai_message = response["message"]["content"]

                # Display AI response properly
                st.markdown(ai_message)

                # Save AI response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ai_message
                })

            except Exception as e:

                st.error(
                    "Could not connect to Ollama."
                )

                st.write(
                    "Make sure Ollama is running and "
                    "the llama3.2 model is installed."
                )


# =========================
# CLEAR CHAT
# =========================

if st.button("🗑️ Clear Chat", use_container_width=True):

    st.session_state.messages = []

    st.rerun()


# =========================
# FOOTER
# =========================

st.markdown(
    '<div class="footer">'
    'Powered by Ollama • Llama 3.2 • Streamlit'
    '</div>',
    unsafe_allow_html=True
)
