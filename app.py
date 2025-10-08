import streamlit as st
import json
import os

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="API Guardian 🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("API Guardian 🛡️")
st.markdown("Browse and explore scraped API documentation content effortlessly.")

# -----------------------------
# Load Data
# -----------------------------
DATA_FILE = "output/docs.json"

if not os.path.exists(DATA_FILE):
    st.error(f"No data found. Please run the scraper first to generate {DATA_FILE}.")
    st.stop()

with open(DATA_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)["docs"]

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Filter Options")
titles = [doc["title"] for doc in data]
selected_title = st.sidebar.selectbox("Select a Document Title:", ["All"] + titles)

search_text = st.sidebar.text_input("Search in content:")

# -----------------------------
# Display Content
# -----------------------------
def display_doc(doc):
    st.subheader(doc["title"])
    st.markdown(f"**URL:** {doc['url']}")
    st.markdown(f"**Scraped on:** {doc['scraped_at']}")
    st.markdown("---")
    st.write(doc["content"][:5000])  # limit for large content

    if doc["code_examples"]:
        st.markdown("**Code Examples:**")
        for i, code in enumerate(doc["code_examples"], 1):
            st.code(code, language="python")
    st.markdown("===")

# Filter docs
filtered_docs = []
for doc in data:
    if selected_title != "All" and doc["title"] != selected_title:
        continue
    if search_text and search_text.lower() not in doc["content"].lower():
        continue
    filtered_docs.append(doc)

if filtered_docs:
    for doc in filtered_docs:
        display_doc(doc)
else:
    st.info("No documents found with the selected filters.")
