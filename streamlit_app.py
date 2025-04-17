import streamlit as st
from app.services.parser import extract_text
from app.services.analyzer import analyze_document

st.set_page_config(page_title="La5asni - Document Analyzer", layout="centered")

st.title("📄 La5asni - Document Analyzer")
st.markdown("Upload a training document (PDF or Word), and we’ll analyze it using AI to extract summaries, key points, and course modules. 🚀")

uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])

if uploaded_file:
    if st.button("🔍 Analyze Document"):
        with st.spinner("Analyzing... Please wait."):
            try:
                # ✅ Step 1: Extract text and metadata
                extracted = extract_text(uploaded_file.name, uploaded_file.getvalue())

                # ✅ Step 2: Run analysis
                result = analyze_document(extracted["text"])

                # ✅ Step 3: Show results
                st.success("✅ Analysis completed!")

                st.subheader("📊 File Insights")
                st.markdown(f"**Number of Pages:** {extracted['num_pages']}")
                st.markdown(f"**Useful Text Ratio:** {extracted['useful_text_ratio'] * 100:.1f}%")
                st.markdown(f"**Number of Key Points:** {result.num_key_points}")

                st.subheader("📌 Summary:")
                st.write(result.summary)

                st.subheader("✅ Key Learning Points:")
                for point in result.key_points:
                    st.markdown(f"- {point}")

                st.subheader("📚 Suggested Training Modules:")
                for module, minutes in zip(result.training_modules, result.estimated_minutes_per_module):
                    st.markdown(f"📘 **{module}** — _⏱ {minutes} mins_")

            except Exception as e:
                st.error(f"🚨 Error during analysis: {e}")
