import streamlit as st
from pathlib import Path
from datetime import datetime
import io
from text_utils import (
    to_upper, to_lower, strip_text, replace_text,
    count_substring, get_preview_lines, get_stats,
    validate_extension, make_timestamp, convert_text_for_format
)

st.set_page_config(page_title="Text Helper", layout="wide")

st.title("Text Helper — small but powerful")
st.markdown("A professional, intuitive dashboard to preview and edit `.txt` files.")

with st.sidebar:
    st.header("Upload & Mode")
    uploaded = st.file_uploader("Upload a .txt file", type=["txt"], help="Only .txt files supported.")
    mode = st.radio("Open mode", ["Read", "Append"], index=0)
    st.markdown("---")
    st.header("Download / Convert")
    target_format = st.selectbox("Save as format", [".txt", ".md", ".html", ".csv"], index=0)

if uploaded is None:
    st.info("Please upload a .txt file to begin.")
    st.stop()

filename = Path(uploaded.name)
if not validate_extension(filename.suffix):
    st.error("Only .txt files are supported.")
    st.stop()

# try decode safely
raw = uploaded.read()
try:
    text = raw.decode("utf-8")
except Exception:
    text = raw.decode("latin-1")

if "text" not in st.session_state:
    st.session_state.text = text

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Preview (first 20 lines)")
    preview = get_preview_lines(st.session_state.text, 20)
    st.code("\n".join(preview))

    st.subheader("String tools")
    replace_old = st.text_input("Replace: old")
    replace_new = st.text_input("Replace: new")
    count_str = st.text_input("Count occurrences of substring")

    b1, b2, b3 = st.columns(3)
    if b1.button("UPPERCASE"):
        st.session_state.text = to_upper(st.session_state.text)
    if b2.button("lowercase"):
        st.session_state.text = to_lower(st.session_state.text)
    if b3.button("strip"):
        st.session_state.text = strip_text(st.session_state.text)

    b4, b5 = st.columns(2)
    if b4.button("replace") and replace_old:
        st.session_state.text = replace_text(st.session_state.text, replace_old, replace_new)
    if b5.button("count") and count_str:
        st.info(f"Occurrences: {count_substring(st.session_state.text, count_str)}")

    st.subheader("Full text (editable)")
    st.text_area("Edit text", value=st.session_state.text, height=300, key="edit_area")

with col2:
    st.subheader("Stats")
    lines, words, chars = get_stats(st.session_state.text)
    st.metric("Lines", lines)
    st.metric("Words", words)
    st.metric("Chars", chars)
    st.markdown("---")
    st.subheader("Save / Append")
    if mode == "Read":
        st.info("Saving is disabled in Read mode.")
    else:
        extra = st.text_area("Extra text to append", height=150)
        if st.button("Save & Download"):
            final_text = st.session_state.text
            if extra.strip():
                final_text += "\n" + extra
            final_text += f"\n\nProcessed on: {make_timestamp()}"
            content_bytes, download_name = convert_text_for_format(final_text, filename.stem, target_format)
            st.download_button("Download edited file", data=content_bytes, file_name=download_name)

st.caption("Built with Streamlit | Functions in text_utils.py")
