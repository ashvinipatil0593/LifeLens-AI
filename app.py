import streamlit as st
from PIL import Image
import pytesseract
from groq import Groq
from dotenv import load_dotenv
import os
import json
import re

load_dotenv()

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="LifeLens AI", page_icon="👁️", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #EEF5FF 0%, #F8FAFC 50%, #E0F2FE 100%);
}
.block-container {
    max-width: 1120px;
    padding-top: 1.5rem;
}
.hero {
    background: linear-gradient(135deg, #1D4ED8, #2563EB);
    color: white;
    padding: 30px;
    border-radius: 28px;
    box-shadow: 0 18px 45px rgba(37, 99, 235, 0.25);
    margin-bottom: 24px;
}
.hero h1 {
    font-size: 46px;
    margin-bottom: 4px;
}
.hero p {
    font-size: 18px;
    line-height: 1.5;
}
.badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    padding: 8px 14px;
    border-radius: 999px;
    margin-right: 8px;
    font-weight: 600;
    font-size: 13px;
}
.card {
    background: rgba(255,255,255,0.95);
    padding: 24px;
    border-radius: 24px;
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    border: 1px solid #E2E8F0;
    margin-bottom: 18px;
}
.result-card {
    background: white;
    padding: 22px;
    border-radius: 22px;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
    border: 1px solid #E2E8F0;
    margin-bottom: 16px;
}
.result-card h4 {
    color: #64748B;
    margin-bottom: 8px;
}
.result-card p {
    color: #0F172A;
    font-size: 18px;
    line-height: 1.6;
}
.metric-card {
    background: white;
    padding: 22px;
    border-radius: 22px;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
    border: 1px solid #E2E8F0;
    min-height: 135px;
}
.metric-card h4 {
    color: #64748B;
}
.metric-card h2 {
    color: #0F172A;
    font-size: 24px;
}
.warning-card {
    background: #FFF7ED;
    border-left: 7px solid #F59E0B;
    padding: 22px;
    border-radius: 22px;
    margin-bottom: 16px;
}
.action-card {
    background: #ECFDF5;
    border-left: 7px solid #22C55E;
    padding: 22px;
    border-radius: 22px;
    margin-bottom: 16px;
}
.tip-card {
    background: #F0F9FF;
    border-left: 7px solid #0EA5E9;
    padding: 22px;
    border-radius: 22px;
    margin-bottom: 16px;
}
.section-title {
    font-size: 25px;
    font-weight: 800;
    color: #0F172A;
    margin-top: 20px;
    margin-bottom: 14px;
}
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #1D4ED8);
    color: white;
    border: none;
    border-radius: 16px;
    padding: 14px 20px;
    font-size: 18px;
    font-weight: 700;
    width: 100%;
    box-shadow: 0 10px 24px rgba(37, 99, 235, 0.25);
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8, #1E3A8A);
    color: white;
}
div[data-testid="stFileUploader"] {
    background: #F8FAFC;
    border: 2px dashed #93C5FD;
    border-radius: 20px;
    padding: 16px;
}
.footer {
    text-align: center;
    color: #64748B;
    padding: 24px;
}
</style>
""", unsafe_allow_html=True)


def extract_json(text):
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                return None
    return None


def fallback_text(language):
    if language == "Marathi":
        return "स्पष्टपणे नमूद केलेले नाही"
    if language == "Hindi":
        return "स्पष्ट रूप से उल्लेख नहीं किया गया"
    return "Not clearly mentioned"


def clean_value(value, language):
    if value is None or str(value).strip() == "":
        return fallback_text(language)
    return str(value)


st.markdown("""
<div class="hero">
    <span class="badge">OCR Powered</span>
    <span class="badge">Groq AI</span>
    <span class="badge">English • Hindi • Marathi</span>
    <h1>👁️ LifeLens AI</h1>
    <p><b>See. Understand. Act.</b></p>
    <p>Upload bills, notices, letters, or circulars and get a simple explanation with the next action.</p>
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1.15, 0.85])

with left:
    st.markdown("""
    <div class="card">
        <h2>📄 Upload Your Document</h2>
        <p>Upload an image of a bill, bank letter, government notice, college circular, receipt, or similar document.</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose document image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )

    language = st.selectbox("🌐 Explain in", ["Simple English", "Hindi", "Marathi"])
    show_ocr = st.checkbox("Show extracted OCR text")
    analyze = st.button("🔍 Analyze Document")

with right:
    st.markdown("""
    <div class="card">
        <h2>✨ How it helps</h2>
        <p>✅ Reads text from document image</p>
        <p>✅ Understands the document using AI</p>
        <p>✅ Explains in simple language</p>
        <p>✅ Shows amount, deadline, warning, and next action</p>
    </div>
    """, unsafe_allow_html=True)

if uploaded_file:
    st.markdown('<div class="section-title">📌 Uploaded Preview</div>', unsafe_allow_html=True)
    image = Image.open(uploaded_file)
    st.image(image, use_container_width=True)

    if analyze:
        groq_key = os.getenv("GROQ_API_KEY")

        if not groq_key:
            st.error("Groq API key missing. Add GROQ_API_KEY in .env file.")
        else:
            with st.spinner("🔍 Reading document using OCR..."):
                extracted_text = pytesseract.image_to_string(image)

            if not extracted_text.strip():
                st.error("No text detected. Please upload a clearer image.")
            else:
                if show_ocr:
                    st.markdown("### Extracted OCR Text")
                    st.text_area("OCR Result", extracted_text, height=180)

                client = Groq(api_key=groq_key)

                prompt = f"""
You are LifeLens AI.

The user selected output language: {language}

Document OCR text:
{extracted_text}

Return ONLY valid JSON. Do not add markdown. Do not add extra text.

Use this exact JSON structure:
{{
  "document_type": "",
  "simple_summary": "",
  "important_details": [],
  "amount_or_fees": "",
  "date_or_deadline": "",
  "risk_or_warning": "",
  "next_action": "",
  "helpful_tip": ""
}}

Language rules:
- If selected language is "Marathi", write ALL JSON values in Marathi using Devanagari script.
- If selected language is "Hindi", write ALL JSON values in Hindi using Devanagari script.
- If selected language is "Simple English", write ALL JSON values in simple English.
- JSON keys must remain in English.

Content rules:
- Keep the explanation simple and useful.
- Do not invent amounts, dates, names, deadlines, or warnings.
- If something is missing, write the selected-language equivalent of "Not clearly mentioned".
- For medical documents, do not diagnose.
- For legal or financial documents, do not give professional advice.
- The next_action must be practical and clear.
- If due date is not clearly visible, use bill date only as "Bill Date", not as deadline.
- If amount is unclear, write "Amount not clearly visible in uploaded image".
"""

                with st.spinner("🧠 AI is understanding and simplifying it..."):
                    try:
                        response = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[
                                {"role": "system", "content": "You explain documents simply and return only valid JSON in the selected language."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.2
                        )
                    except Exception:
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": "You explain documents simply and return only valid JSON in the selected language."},
                                {"role": "user", "content": prompt}
                            ],
                            temperature=0.2
                        )

                answer = response.choices[0].message.content
                result = extract_json(answer)

                if not result:
                    st.warning("AI response could not be formatted. Showing raw response:")
                    st.write(answer)
                else:
                    st.markdown('<div class="section-title">✅ AI Explanation</div>', unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="result-card">
                        <h4>📄 Document Type</h4>
                        <p><b>{clean_value(result.get("document_type"), language)}</b></p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="result-card">
                        <h4>📝 Simple Summary</h4>
                        <p>{clean_value(result.get("simple_summary"), language)}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    m1, m2 = st.columns(2)

                    with m1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>💰 Amount / Fees</h4>
                            <h2>{clean_value(result.get("amount_or_fees"), language)}</h2>
                        </div>
                        """, unsafe_allow_html=True)

                    with m2:
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>📅 Date / Deadline</h4>
                            <h2>{clean_value(result.get("date_or_deadline"), language)}</h2>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown('<div class="section-title">🔎 Important Details</div>', unsafe_allow_html=True)
                    details = result.get("important_details", [])

                    if details:
                        for item in details:
                            st.markdown(f"""
                            <div class="result-card">
                                <p>• {item}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.write(fallback_text(language))

                    st.markdown(f"""
                    <div class="warning-card">
                        <h3>⚠️ Risk or Warning</h3>
                        <p>{clean_value(result.get("risk_or_warning"), language)}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="action-card">
                        <h3>✅ Next Action</h3>
                        <p>{clean_value(result.get("next_action"), language)}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="tip-card">
                        <h3>💡 Helpful Tip</h3>
                        <p>{clean_value(result.get("helpful_tip"), language)}</p>
                    </div>
                    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    LifeLens AI | Built using Streamlit + Tesseract OCR + Groq AI
</div>
""", unsafe_allow_html=True)