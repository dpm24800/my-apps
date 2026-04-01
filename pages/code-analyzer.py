import streamlit as st
from groq import Groq
import streamlit.components.v1 as components

# --- INITIALIZATION ---
st.set_page_config(page_title="Code Change Analyzer", layout="wide") # centered/wide

# Get your API key from https://console.groq.com/keys

# Hardcoded API Key
GROQ_API_KEY = "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"

# For local testing, you can hardcode it or use st.secrets

GROQ_API_KEY = st.sidebar.text_input(
    "Enter Groq API Key", 
    value=GROQ_API_KEY,
    type="password"
)

# Custom CSS for UI Layout and Code Blocks
st.markdown("""
    <style>
    /* Centering the Upper and Lower parts */
    .centered-block {
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
        color: red;
    }
    
    /* Code Blocks: Fixed 800px height with sync scrolling */
    div[data-testid="stCodeBlock"] > div {
        height: 800px !important;
        min-height: 800px !important;
        max-height: 800px !important;
        overflow-y: auto !important;
    }

    /* Force word wrap and syntax readability */
    code {
        white-space: pre-wrap !important;
        word-break: break-all !important;
    }

    .stColumn {
        max-height: 800px;
        overflow-y: scroll;
    }

    .stElementContainer, .stHeading {
        margin: 0 auto;
    }

    div.stElementContainer:last-of-type {
        /* styles for the last div with class "my-class" */
        /* width: 900px; */
        /* border: 1px solid red; */
    }
    
    /* Centering the primary action button */
    div.stButton > button:first-child {
        display: block;
        margin: 0 auto;
        width: 250px;
        height: 50px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def analyze_changes(file1_content, file1_name, file2_content, file2_name):
    if not GROQ_API_KEY:
        st.error("Please enter your Groq API Key in the sidebar!")
        return

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
    
    Task: Act as a senior developer. Provide a clear, bulleted summary of:
    1. Key features removed from the first file.
    2. Key features added in the second file.
    3. Technical logic changes (e.g., changes in libraries, constants, or functions).
    4. Use a markdown table for a quick comparison.
    """

    # prompt = f"""
    # Compare these two Python files: '{file1_name}' and '{file2_name}'.
    # FILE 1: {file1_content}
    # FILE 2: {file2_content}
    # Task: Summary of removed features, added features, logic changes, and a comparison table.
    # """

    # prompt = f"""
    # Compare these two Python files: '{file1_name}' and '{file2_name}'.
    
    # FILE 1: {file1_content}
    # FILE 2: {file2_content}
    
    # Task: Provide a clear summary of:
    # 1. Key features removed from the first file.
    # 2. Key features added in the second file.
    # 3. Technical logic/library changes.
    # 4. A markdown table for quick comparison.
    # """

    # prompt = f"""
    # Compare these two Python files: '{file1_name}' and '{file2_name}'.
    
    # FILE 1: {file1_content}
    # FILE 2: {file2_content}
    
    # Provide a summary of removed features, added features, logic changes, and a comparison table in Markdown.
    # """


    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2, # Low temperature for factual comparison
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- UI LAYOUT ---
st.markdown('<div class="centered-block">', unsafe_allow_html=True)
st.title("📂 AI Code Change Analyzer")
# st.write("Upload two versions of a script to see a feature-level diff powered by Groq.")
st.info("Upload two versions of a script to see a feature-level diff powered by Groq.")

uploaded_files = st.file_uploader(
    "Upload two Python files", 
    type=["py"], 
    accept_multiple_files=True
)

st.markdown('</div>', unsafe_allow_html=True)


if len(uploaded_files) == 2:
    file1, file2 = uploaded_files
    
    # Read contents
    code1 = file1.getvalue().decode("utf-8")
    code2 = file2.getvalue().decode("utf-8")

    # st.markdown("---")
    col1, col2 = st.columns(2)
    # with col1:
    #     st.subheader(f"**File 1: {file1.name}**")
    #     st.code(code1, language="python")
    # with col2:
    #     st.subheader(f"**File 2: {file2.name}**")
    #     st.code(code2, language="python")

    # st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Analyze Changes with AI", type="primary", icon="🔍"):
        with st.spinner("Groq is thinking..."):
            analysis = analyze_changes(code1, file1.name, code2, file2.name)
            
            # Lower part
            st.markdown("---")
            st.markdown("## 🤖 AI Analysis Results")
            st.markdown(analysis) # Display the analysis
    
            # Copy Button Logic
            # We escape the backticks and newlines for the JS string
            escaped_analysis = analysis.replace("`", "\\`").replace("\"", "\\\"")
            
            # Custom Copy Button using HTML/JS
            components.html(f"""
                <button onclick="copyToClipboard()" style="
                    background-color: #ff4b4b; color: white; border: none; 
                    padding: 10px 20px; border-radius: 5px; cursor: pointer;
                    font-weight: bold; margin-bottom: 10px;">
                    📋 Copy Report (MD)
                </button>
                <script>
                function copyToClipboard() {{
                    const text = `{escaped_analysis}`;
                    navigator.clipboard.writeText(text).then(() => {{
                        alert('Report copied to clipboard!');
                    }});
                }}
                </script>
            """, height=60)
    
elif len(uploaded_files) > 0:
    st.info("Please upload exactly **two** files to begin comparison.")
