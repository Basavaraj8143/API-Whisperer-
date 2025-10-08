import streamlit as st
from rag_pipeline import answer_question
from scraper import scrape_url, parse_content, save_to_json

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="API Guardian 🛡️",
    layout="wide"
)
st.title("API Guardian 🛡️")
st.markdown("Ask questions about any API documentation you have scraped.")

# ---------- SESSION STATE ----------
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

if 'temp' not in st.session_state:
    st.session_state['temp'] = 0.2
if 'max_tokens' not in st.session_state:
    st.session_state['max_tokens'] = 512

# ---------- SIDEBAR ----------
with st.sidebar:
    st.header("Settings")
    st.session_state['temp'] = st.slider("Temperature", 0.0, 1.0, st.session_state['temp'])
    st.session_state['max_tokens'] = st.number_input("Max Tokens", value=st.session_state['max_tokens'], step=50)

    st.markdown("---")
    st.header("Scrape New Docs")
    new_url = st.text_input("Enter API Doc URL")
    if st.button("Scrape & Save"):
        if new_url:
            try:
                html = scrape_url(new_url)
                doc_data = parse_content(html, new_url)  # Returns single document
                save_to_json([doc_data])  # Wrap in list before saving
                st.success("New API documentation scraped and saved!")
            except Exception as e:
                st.error(f"Error scraping documentation: {str(e)}")

# ---------- CHAT INTERFACE ----------
query = st.chat_input("Ask a question about the API...")

if query:
    # Call RAG pipeline
    result = answer_question(query, top_k=5)
    # Save to chat history
    st.session_state['chat_history'].append((query, result))

 # ---------- DISPLAY CHAT ----------
    st.markdown("### 💬 Chat History")
    for q, res in st.session_state['chat_history']:
        st.chat_message("user").write(q)
        with st.chat_message("assistant"):
            st.write(res['answer'])
            st.markdown(f"**Confidence:** {res['confidence']:.2f}")
            if res['sources']:
                with st.expander("📚 Sources"):
                    for src in res['sources']:
                        st.markdown(f"- [Link]({src})")