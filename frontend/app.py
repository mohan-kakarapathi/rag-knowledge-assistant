
import requests
import streamlit as st

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="RAG Knowledge Assistant",
    page_icon="📚",
)

st.title("📚 RAG Knowledge Assistant")
st.caption("Upload your documents and ask questions about their content.")

if "documents" not in st.session_state:
    st.session_state.documents = []

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------- Document upload --------------------

st.subheader("1. Upload documents")

uploaded_files = st.file_uploader(
    "Choose PDF or TXT files",
    type=["pdf", "txt"],
    accept_multiple_files=True,
)

if st.button("Upload and process documents"):
    if not uploaded_files:
        st.warning("Please select at least one file.")
    else:
        for uploaded_file in uploaded_files:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/documents/upload",
                        files={
                            "file": (
                                uploaded_file.name,
                                uploaded_file.getvalue(),
                                uploaded_file.type,
                            )
                        },
                        timeout=180,
                    )
                    response.raise_for_status()
                    document = response.json()

                    st.session_state.documents.append(document)

                    st.success(
                        f"Indexed {document['filename']} "
                        f"({document['chunks_count']} chunks)"
                    )

                except requests.exceptions.RequestException as exc:
                    detail = "Could not upload the document."
                    if getattr(exc, "response", None) is not None:
                        try:
                            detail = exc.response.json().get("detail", detail)
                        except ValueError:
                            pass
                    st.error(f"{uploaded_file.name}: {detail}")



# -------------------- Chat --------------------

st.subheader("2. Ask questions")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message["role"] == "assistant" and message.get("sources"):
            with st.expander("View retrieved sources"):
                for i, source in enumerate(message["sources"], start=1):
                    st.markdown(f"**Source {i}: {source['metadata'].get('source', 'Document')}**")
                    st.write(source["text"])
                    st.caption(f"Distance: {source['distance']:.4f}")

question = st.chat_input(
    "Ask a question about your documents..."
)


if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating an answer..."):
            try:
                response = requests.post(
                    f"{API_BASE}/ask",
                    json={
                        "question": question,
                    },
                    timeout=180,
                )

                response.raise_for_status()
                result = response.json()

                answer = result["answer"]
                sources = result.get("sources", [])

                st.markdown(answer)

                if sources:
                    with st.expander("View retrieved sources"):
                        for i, source in enumerate(sources, start=1):
                            st.markdown(
                                f"**Source {i}: "
                                f"{source['metadata'].get('source', 'Document')}**"
                            )
                            st.write(source["text"])
                            st.caption(
                                f"Distance: {source['distance']:.4f}"
                            )

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })

            except requests.exceptions.RequestException as exc:
                detail = "Could not reach the backend."

                if getattr(exc, "response", None) is not None:
                    try:
                        detail = exc.response.json().get(
                            "detail", detail
                        )
                    except ValueError:
                        pass

                st.error(detail)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": detail,
                })
