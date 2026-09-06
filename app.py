import streamlit as st
import requests

st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF AI Assistant")

st.write(
    "Upload a PDF file and let the AI agent analyze and summarize it."
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    st.success(f"Selected file: {uploaded_file.name}")

    if st.button("Analyze PDF"):

        webhook_url = "https://sabothneen.app.n8n.cloud/webhook/pdf-agents"

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        with st.spinner("Analyzing PDF..."):

            try:

                response = requests.post(
                    webhook_url,
                    files=files
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("Analysis completed successfully.")

                    st.divider()

                    st.subheader("📌 Document Title")
                    st.write(result["title"])

                    st.subheader("📝 Summary")
                    st.write(result["summary"])

                    st.subheader("🎯 Main Topic")
                    st.write(result["main_topic"])

                    st.subheader("🔑 Key Points")

                    for i, point in enumerate(
                        result["key_points"],
                        start=1
                    ):
                        st.write(f"{i}. {point}")

                else:

                    st.error(
                        f"Request failed with status code: "
                        f"{response.status_code}"
                    )

                    st.write(response.text)

            except Exception as e:

                st.error("Something went wrong.")

                st.write(e)



st.divider()
st.subheader("💬 Ask about this PDF")

question = st.text_input(
    "Enter your question"
)

if st.button("Ask AI"):

    question_webhook_url = "https://sabothneen.app.n8n.cloud/webhook/pdf-qa"

    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf"
        )
    }

    data = {
        "question": question
    }

    with st.spinner("Thinking..."):

        response = requests.post(
            question_webhook_url,
            files=files,
            data=data
        )

        if response.status_code == 200:

            result = response.json()

            st.success("Answer generated successfully.")
            st.subheader("🤖 Answer")
            st.write(result["answer"])

        else:

            st.error(
                f"Request failed with status code: "
                f"{response.status_code}"
            )

            st.write(response.text)
