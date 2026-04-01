import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

# --- INITIALIZATION ---
st.set_page_config(page_title="Code Change Analyzer", layout="wide")

# 🔒 Hardcoded API Key (NOT SAFE for GitHub — use only locally)
GROQ_API_KEY = "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"

# Custom CSS
st.markdown("""
    <style>
    .centered-block {
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
        color: red;
    }

    div[data-testid="stCodeBlock"] > div {
        height: 800px !important;
        overflow-y: auto !important;
    }

    code {
        white-space: pre-wrap !important;
        word-break: break-all !important;
    }

    .stColumn {
        max-height: 800px;
        overflow-y: scroll;
    }

    div.stButton > button:first-child {
        display: block;
        margin: 0 auto;
        width: 250px;
        height: 50px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


# --- ANALYSIS FUNCTION ---
def analyze_changes(file1_content, file1_name, file2_content, file2_name):
    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""
    Compare these two Python files: '{file1_name}' and '{file2_name}'.
    
    FILE 1 ({file1_name}):
    \"\"\"
    {file1_content}
    \"\"\"
    
    FILE 2 ({file2_name}):
    \"\"\"
    {file2_content}
    \"\"\"
    
    Task: Act as a senior developer. Provide:
    1. Key features removed
    2. Key features added
    3. Technical logic changes
    4. Markdown comparison table
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


# --- UI ---
st.markdown('<div class="centered-block">', unsafe_allow_html=True)
st.title("📂 AI Code Change Analyzer")
st.info("Upload two versions of a script to see a feature-level diff powered by Groq.")

uploaded_files = st.file_uploader(
    "Upload two Python files",
    type=["py"],
    accept_multiple_files=True
)
st.markdown('</div>', unsafe_allow_html=True)


# --- LOGIC ---
if len(uploaded_files) == 2:
    file1, file2 = uploaded_files

    code1 = file1.getvalue().decode("utf-8")
    code2 = file2.getvalue().decode("utf-8")

    if st.button("Analyze Changes with AI", type="primary"):
        with st.spinner("Groq is thinking..."):
            analysis = analyze_changes(code1, file1.name, code2, file2.name)

            st.markdown("---")
            st.markdown("## 🤖 AI Analysis Results")
            st.markdown(analysis)

            # Copy button
            escaped = analysis.replace("`", "\\`").replace("\"", "\\\"")

            components.html(f"""
                <button onclick="copyToClipboard()" style="
                    background-color: #ff4b4b; color: white;
                    padding: 10px 20px; border-radius: 5px;
                    cursor: pointer; font-weight: bold;">
                    📋 Copy Report
                </button>
                <script>
                function copyToClipboard() {{
                    const text = `{escaped}`;
                    navigator.clipboard.writeText(text).then(() => {{
                        alert('Copied!');
                    }});
                }}
                </script>
            """, height=60)

elif len(uploaded_files) > 0:
    st.info("Please upload exactly two files.")
