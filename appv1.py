import streamlit as st
import requests

st.set_page_config(
    page_title="PDF AI Assistant",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF AI Assistant")

st.write(
    "Upload a PDF file and let the AI agent analyze, summarize, "
    "and answer questions about it."
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

# -----------------------------------
# PDF Analysis
# -----------------------------------

if uploaded_file is not None:

    st.success(f"Selected file: {uploaded_file.name}")

    if st.button("Analyze PDF"):

        webhook_url = (
            "https://sabothneen.app.n8n.cloud/webhook/pdf-agents"
        )

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
                    files=files,
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success(
                        "Analysis completed successfully."
                    )

                    st.divider()

                    st.subheader("📌 Document Title")
                    st.write(
                        result.get(
                            "title",
                            "Title not available"
                        )
                    )

                    st.subheader("📝 Summary")
                    st.write(
                        result.get(
                            "summary",
                            "Summary not available"
                        )
                    )

                    st.subheader("🎯 Main Topic")
                    st.write(
                        result.get(
                            "main_topic",
                            "Main topic not available"
                        )
                    )

                    st.subheader("🔑 Key Points")

                    key_points = result.get(
                        "key_points",
                        []
                    )

                    if key_points:
                        for i, point in enumerate(
                            key_points,
                            start=1
                        ):
                            st.write(f"{i}. {point}")
                    else:
                        st.write(
                            "No key points available."
                        )

                else:

                    st.error(
                        f"Request failed with status code: "
                        f"{response.status_code}"
                    )

                    st.write(response.text)

            except Exception as e:

                st.error(
                    "Something went wrong while analyzing the PDF."
                )

                st.write(e)


# -----------------------------------
# PDF Question & Answer
# -----------------------------------

st.divider()

st.subheader("💬 Ask about this PDF")

question = st.text_input(
    "Enter your question"
)

if st.button("Ask AI"):

    if uploaded_file is None:

        st.warning(
            "Please upload a PDF first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        question_webhook_url = (
            "https://sabothneen.app.n8n.cloud/webhook/pdf-qa"
        )

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

            try:

                response = requests.post(
                    question_webhook_url,
                    files=files,
                    data=data,
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()

                    # Try different possible n8n response formats
                    answer = None

                    if "answer" in result:
                        answer = result["answer"]

                    elif (
                        "output" in result
                        and isinstance(
                            result["output"],
                            dict
                        )
                        and "answer" in result["output"]
                    ):
                        answer = result["output"]["answer"]

                    elif (
                        "output" in result
                        and isinstance(
                            result["output"],
                            str
                        )
                    ):
                        answer = result["output"]

                    elif "message" in result:
                        answer = result["message"]

                    if answer:

                        st.success(
                            "Answer generated successfully."
                        )

                        st.subheader("🤖 Answer")

                        st.write(answer)

                    else:

                        st.error(
                            "n8n returned a response, "
                            "but no answer field was found."
                        )

                        st.write(
                            "Response received from n8n:"
                        )

                        st.json(result)

                else:

                    st.error(
                        f"Request failed with status code: "
                        f"{response.status_code}"
                    )

                    st.write(response.text)

            except Exception as e:

                st.error(
                    "Something went wrong while "
                    "generating the answer."
                )

                st.write(e)
