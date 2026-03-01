import streamlit as st
import requests

st.title("Titanic Data Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("chart"):
            st.image(msg["chart"])

prompt = st.chat_input("Ask about Titanic dataset...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.write(prompt)

    response = requests.post(
        "http://localhost:8000/ask",
        json={"question": prompt},
        timeout=60
    )

    data = response.json()

    chart_url = None
    if data.get("show_chart"):
        chart_url = "http://localhost:8000/chart"

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": data["answer"],
            "chart": chart_url
        }
    )

    with st.chat_message("assistant"):
        st.write(data["answer"])
        if chart_url:
            st.image(chart_url)