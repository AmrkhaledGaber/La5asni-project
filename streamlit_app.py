import streamlit as st
import requests

st.set_page_config(page_title="La5asni - Document Analyzer", layout="centered")

st.title("📄 La5asni - Document Analyzer")
st.markdown("Upload a training document (PDF or Word), and we’ll analyze it using AI to extract summaries, key points, and course modules. 🚀")

uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file is not None:
    if st.button("🔍 Analyze Document"):
        with st.spinner("Analyzing... Please wait."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            try:
                response = requests.post("http://127.0.0.1:8000/api/v1/analyze/", files=files)

                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Analysis completed!")

                    # 🔹 Basic Info
                    st.subheader("📊 File Insights")
                    st.markdown(f"**Number of Pages:** {data['num_pages']}")
                    st.markdown(f"**Useful Text Ratio:** {data['useful_text_ratio'] * 100:.1f}%")
                    st.markdown(f"**Number of Key Points:** {data['num_key_points']}")

                    # 🔹 Summary
                    st.subheader("📌 Summary:")
                    st.write(data["summary"])

                    # 🔹 Key Points
                    st.subheader("✅ Key Learning Points:")
                    for point in data["key_points"]:
                        st.markdown(f"- {point}")

                    # 🔹 Modules with estimated time
                    st.subheader("📚 Suggested Training Modules:")
                    for module, minutes in zip(data["training_modules"], data["estimated_minutes_per_module"]):
                        st.markdown(f"📘 **{module}** — _⏱ {minutes} mins_")

                else:
                    st.error("❌ Something went wrong while processing the document.")
            except Exception as e:
                st.error(f"🚨 Error connecting to the backend: {e}")

# 🔹 Dashboard Section
st.divider()
st.header("📂 Past Analyses Dashboard")
st.caption("(Coming soon) View your previous document uploads and analyses here.")