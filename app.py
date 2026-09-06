import streamlit as st
import requests

st.title("PDF AI Assistant")

uploaded_file = st.file_uploader(
    "Upload a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success(f"File selected: {uploaded_file.name}")

    if st.button("Send PDF to n8n"):

        webhook_url = "https://sabothneen.app.n8n.cloud/webhook-test/pdf-agents"

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        response = requests.post(
            webhook_url,
            files=files
        )

        st.write("Status Code:", response.status_code)

        st.write("Response from n8n:")

        try:
            st.json(response.json())
        except:
            st.write(response.text)
