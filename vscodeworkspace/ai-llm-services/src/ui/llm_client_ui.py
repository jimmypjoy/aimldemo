import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import requests
import streamlit as st

from llm.enums.llm_enum import LLMModel

API_URL = "http://127.0.0.1:8000/api/v1/llm/invoke"
DEFAULT_QUERY = "What is the capital of France?"
DEFAULT_MODEL_NAME = "gemini-3.1-pro-preview"

_model_options = [(m.model_name, m.name) for m in LLMModel]
_display_names = [d for d, _ in _model_options]
_default_index = _display_names.index(DEFAULT_MODEL_NAME)


def _call_api(payload: dict) -> dict:
    response = requests.post(API_URL, json=payload, timeout=60)
    response.raise_for_status()
    return response.json()


st.set_page_config(page_title="LLM Inference Client", layout="centered")
st.title("LLM Inference Client")
st.caption("Calls the local FastAPI service at `http://127.0.0.1:8000`")

with st.form("llm_form"):
    query = st.text_area("Query", value=DEFAULT_QUERY, height=100)

    col1, col2 = st.columns(2)
    with col1:
        selected_display = st.selectbox(
            "LLM Model",
            options=_display_names,
            index=_default_index,
        )
    with col2:
        user_role = st.text_input("User Role (optional)", value="user")

    prompt = st.text_area("System Prompt (optional)", value="", height=80)

    submitted = st.form_submit_button("Invoke LLM", use_container_width=True)

if submitted:
    enum_key = dict(_model_options)[selected_display]
    payload = {
        "query": query,
        "prompt": prompt,
        "llm_model": enum_key,
        "user_role": user_role,
    }

    with st.spinner(f"Calling {selected_display}..."):
        try:
            data = _call_api(payload)
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API. Make sure `python server.py` is running.")
            st.stop()
        except requests.exceptions.HTTPError as exc:
            st.error(f"API error {exc.response.status_code}: {exc.response.text}")
            st.stop()

    st.divider()

    success = data.get("success", False)
    response_time = data.get("response_time", 0.0)
    exception_message = data.get("exception_message")

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Model", selected_display)
    col_b.metric("Response Time", f"{response_time:.3f}s")
    col_c.metric("Status", "Success" if success else "Failed")

    if success:
        st.success("Response")
        st.write(data.get("llm_response", ""))
    else:
        st.error("Invocation failed")
        if exception_message:
            st.code(exception_message)
