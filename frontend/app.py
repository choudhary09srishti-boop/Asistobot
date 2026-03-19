import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Research Assistant",
    page_icon="📖",
    layout="wide"
)

# ── Custom CSS to match your design ──
st.markdown("""
<style>
    .main { background-color: #f4f6f9; }
    .block-container { padding-top: 2rem; max-width: 780px; }

    .source-circle {
        background: #E6F1FB;
        border: 2px solid #85B7EB;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.65rem;
        color: #0C447C;
        text-align: center;
        padding: 8px;
        font-family: monospace;
    }

    .content-card {
        background: #ffffff;
        border: 1.5px solid #85B7EB;
        border-radius: 10px;
        padding: 14px 18px;
        font-family: 'Georgia', serif;
        font-size: 1rem;
        line-height: 1.75;
        color: #3c424f;
    }

    .answer-card {
        background: #ffffff;
        border: 1.5px solid #d1d9e6;
        border-radius: 14px;
        padding: 20px 24px;
        font-family: 'Georgia', serif;
        font-size: 1.05rem;
        line-height: 1.8;
        color: #1a1d24;
        margin-bottom: 16px;
    }

    .follow-up-card {
        background: #E1F5EE;
        border: 1.5px solid #5DCAA5;
        border-radius: 10px;
        padding: 12px 18px;
        font-family: 'Georgia', serif;
        font-size: 0.95rem;
        color: #085041;
        font-style: italic;
    }

    .section-label {
        font-family: monospace;
        font-size: 0.65rem;
        color: #9ca3af;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .user-question {
        background: #1e3a5f;
        color: #dbeafe;
        border-radius: 16px 16px 3px 16px;
        padding: 12px 18px;
        font-family: 'Georgia', serif;
        font-size: 1.05rem;
        font-style: italic;
        display: inline-block;
        max-width: 70%;
        float: right;
        margin-bottom: 16px;
    }

    .stButton button {
        background-color: #1e3a5f;
        color: white;
        border-radius: 9px;
        border: none;
        padding: 10px 24px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .stButton button:hover {
        background-color: #1d4ed8;
    }
</style>
""", unsafe_allow_html=True)


# ── Session state setup ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "sources_uploaded" not in st.session_state:
    st.session_state.sources_uploaded = []
if "chatbot_mode" not in st.session_state:
    st.session_state.chatbot_mode = False


# ── SIDEBAR — upload sources ──
with st.sidebar:
    st.markdown("### 📁 Your Sources")
    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload PDF or DOCX",
        type=["pdf", "docx"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for file in uploaded_files:
            if file.name not in st.session_state.sources_uploaded:
                with st.spinner(f"Indexing {file.name}..."):
                    response = requests.post(
                        f"{API_URL}/upload",
                        files={"file": (file.name, file.read(), file.type)}
                    )
                    if response.status_code == 200:
                        st.session_state.sources_uploaded.append(file.name)
                        st.success(f"✅ {file.name}")
                    else:
                        st.error(f"❌ Failed: {file.name}")

    st.markdown("---")
    url_input = st.text_input("🌐 Paste a URL", placeholder="https://...")
    if st.button("Add URL") and url_input:
        with st.spinner("Scraping URL..."):
            response = requests.post(
                f"{API_URL}/upload_url",
                data={"url": url_input}
            )
            if response.status_code == 200:
                st.session_state.sources_uploaded.append(url_input)
                st.success("✅ URL indexed")
            else:
                st.error("❌ Could not extract content")

    st.markdown("---")

    if st.session_state.sources_uploaded:
        st.markdown("**Indexed sources:**")
        for src in st.session_state.sources_uploaded:
            name = src if len(src) < 28 else src[:26] + "…"
            st.markdown(f"📄 `{name}`")

    if st.button("🗑 Clear all sources"):
        requests.post(f"{API_URL}/clear")
        st.session_state.sources_uploaded = []
        st.session_state.messages = []
        st.session_state.chatbot_mode = False
        st.rerun()


# ── MAIN AREA ──
st.markdown("<div class='section-label'>Research Assistant</div>",
            unsafe_allow_html=True)

# Show previous messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"<div class='user-question'>{msg['content']}</div><div style='clear:both'></div>",
            unsafe_allow_html=True
        )

    elif msg["role"] == "answer":
        st.markdown("<div class='section-label'>Answer</div>",
                    unsafe_allow_html=True)
        st.markdown(
            f"<div class='answer-card'>{msg['content']}</div>",
            unsafe_allow_html=True
        )

    elif msg["role"] == "sources":
        if msg["content"]:
            st.markdown("<div class='section-label'>Sources</div>",
                        unsafe_allow_html=True)
            for source in msg["content"]:
                col1, col2 = st.columns([1, 5])
                with col1:
                    st.markdown(
                        f"<div class='source-circle'>"
                        f"{source['source']}<br/>"
                        f"p.{source['page']} ¶{source['para']}"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                with col2:
                    st.markdown(
                        f"<div class='content-card'>{source['text']}</div>",
                        unsafe_allow_html=True
                    )
                st.markdown("<br/>", unsafe_allow_html=True)

    elif msg["role"] == "follow_up":
        st.markdown(
            f"<div class='follow-up-card'>💬 {msg['content']}</div>",
            unsafe_allow_html=True
        )
        st.markdown("<br/>", unsafe_allow_html=True)


# ── INPUT BAR ──
st.markdown("---")

if not st.session_state.sources_uploaded:
    st.info("👆 Upload a PDF, DOCX or paste a URL in the sidebar to get started.")
else:
    placeholder = (
        "Ask a follow-up question…"
        if st.session_state.chatbot_mode
        else "Ask a question about your documents…"
    )

    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            question = st.text_input(
                "",
                placeholder=placeholder,
                label_visibility="collapsed"
            )
        with col2:
            submitted = st.form_submit_button("Ask →")

    if submitted and question.strip():
        # Save user question
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.spinner("Searching your documents…"):
            response = requests.post(
                f"{API_URL}/ask",
                data={"question": question}
            )

        if response.status_code == 200:
            result = response.json()

            # Save answer
            st.session_state.messages.append({
                "role": "answer",
                "content": result.get("answer", "")
            })

            # Save sources
            st.session_state.messages.append({
                "role": "sources",
                "content": result.get("sources", [])
            })

            # Save follow up
            follow_up = result.get("follow_up", "")
            if follow_up:
                st.session_state.messages.append({
                    "role": "follow_up",
                    "content": follow_up
                })

            # Switch to chatbot mode after first answer
            st.session_state.chatbot_mode = True
            st.rerun()

        else:
            st.error("Something went wrong. Is the backend running?")