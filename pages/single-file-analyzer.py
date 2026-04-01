import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

# --- INITIALIZATION ---
st.set_page_config(page_title="AI Code Explainer", layout="wide")

# 🔒 Hardcoded API Key (ONLY for local use)
GROQ_API_KEY = "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"

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .centered-block {
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
    }

    div[data-testid="stCodeBlock"] > div {
        height: 500px !important;
        overflow-y: auto !important;
    }

    code {
        white-space: pre-wrap !important;
        word-break: break-all !important;
    }

    div.stButton > button:first-child {
        display: block;
        margin: 20px auto;
        width: 250px;
        height: 50px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- AI ANALYSIS FUNCTION ---
def explain_code(file_content, file_name):
    client = Groq(api_key=GROQ_API_KEY)

    prompt = f"""
    You are a senior software engineer.

    Analyze the following code file: '{file_name}'

    CODE:
    \"\"\"
    {file_content}
    \"\"\"

    Provide a structured explanation:
    1. Overall purpose of the code
    2. File structure (functions, classes, modules)
    3. Step-by-step logic explanation
    4. Important concepts used (e.g., OOP, APIs, loops, regex, ML, etc.)
    5. Potential improvements or best practices

    Use clear markdown formatting.
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

st.title("🧠 AI Code Explainer")
st.info("Upload a Python or code file to get a detailed explanation of its logic and structure.")

uploaded_file = st.file_uploader(
    "Upload a code file",
    type=["py", "js", "java", "cpp", "c", "ts", "go"]
)

st.markdown('</div>', unsafe_allow_html=True)


# --- LOGIC ---
if uploaded_file is not None:

    code = uploaded_file.getvalue().decode("utf-8")

    st.markdown("### 📄 Uploaded Code")
    st.code(code, language="python")

    if st.button("Explain Code with AI", type="primary"):
        with st.spinner("Analyzing code..."):
            explanation = explain_code(code, uploaded_file.name)

            st.markdown("---")
            st.markdown("## 🤖 AI Explanation")
            st.markdown(explanation)

            # Copy button
            escaped = explanation.replace("`", "\\`").replace("\"", "\\\"")

            components.html(f"""
                <button onclick="copyToClipboard()" style="
                    background-color: #4CAF50; color: white;
                    padding: 10px 20px; border-radius: 5px;
                    cursor: pointer; font-weight: bold;">
                    📋 Copy Explanation
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
