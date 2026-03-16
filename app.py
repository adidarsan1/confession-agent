import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables (mostly for local use)
load_dotenv()

# App UI Configuration
st.set_page_config(
    page_title="Legal Tamil Confession Generator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar Configuration
st.sidebar.title("⚙️ Configuration")
st.sidebar.write("Configure your AI Agent settings here.")
api_key_input = st.sidebar.text_input(
    "Google Gemini API Key",
    type="password",
    help="Get this from Google AI Studio. It is used securely and not stored.",
    value=os.getenv("GEMINI_API_KEY", "")
)

if not api_key_input:
    st.sidebar.warning("⚠️ Please enter your Gemini API Key to continue.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📝 About")
st.sidebar.info(
    "This tool assists Investigation Officers (IOs) in drafting "
    "'Bulletproof' Confession Statements (Opputhal Vaku Moolam) "
    "in formal Legal Tamil from rough facts, focusing on acquittal prevention."
)

# Main Content
st.title("⚖️ Legal Tamil Confession Agent")
st.markdown(
    "Transform raw colloquial Tamil/Tanglish details into a formal, court-admissible "
    "**Opputhal Vaku Moolam** adhering to standard legal templates for Indian Criminal Law."
)

# Input Section
st.header("1. Input Case Details")
st.markdown("Enter the rough details obtained from the accused. Include motive, the act, and hiding place of the weapon/evidence.")

colloquial_input = st.text_area(
    "Accused Statement (Tanglish/Colloquial Tamil)",
    height=150,
    placeholder="Example: Nan thaan kathi eduthu kuthinen, adhu selva layer la olichi vechiruken..."
)

# System Prompt Context
IO_SYSTEM_PROMPT = """
**Role:** Senior Investigation Officer (IO) & Legal Drafting Expert (Tamil Nadu Police Standard).
**Task:** Generate 100% Legally Admissible Confession Statements in Formal Tamil.

**Guiding Principles (Based on Study of Acquittals):**
1. **The "Exclusive Knowledge" Clause:** எப்பொழுதும் ஆயுதம் மறைக்கப்பட்ட இடம் காவல்துறைக்குத் தெரியாது என்றும், எதிரிக்கு மட்டுமே தெரியும் என்றும், அவனே முன்வந்து அடையாளப்படுத்தினான் என்றும் எழுதவும். 
2. **Detailed Descriptions:** ஆயுதத்தின் அளவு, வடிவம், அதன் மேல் உள்ள கறைகள் (இரத்தம்/மண்) பற்றித் துல்லியமாக எழுதவும்.
3. **Defense Analysis:** டிராப்ட் தரும் முன்பாக, இந்த வழக்கில் எதிரி தரப்பு வக்கீல் எங்கே கேள்வி கேட்க வாய்ப்புள்ளது என்பதைக் கண்டறிந்து எச்சரிக்கவும்.
4. **No Coercion:** சித்திரவதை அல்லது மிரட்டல் இன்றி சுயமாகத் தரும் வாக்குமூலம் என்பதை வலியுறுத்தவும்.

**Output Structure:**
- Potential Defense Loopholes (வழக்கின் ஓட்டைகள்).
- Professional Confession Draft (தூய தமிழ் நீதிமன்ற நடைமுறை).
- Mahazar/Recovery Checklist (IO-க்கான குறிப்புகள்).
"""

# Generation Logic
if st.button("Generate Legal Confession Draft", type="primary"):
    if not api_key_input:
        st.error("❌ Please provide a Google Gemini API Key in the sidebar.")
    elif not colloquial_input.strip():
        st.warning("⚠️ Please provide the input case details.")
    else:
        with st.spinner("Drafting Confession Statement bypasses Streamlit limits..."):
            try:
                # Direct REST API call bypassing any older library versions in Streamlit
                # Switched to the universally supported 'gemini-pro' model to resolve the 404 error
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key_input}"
                
                payload = {
                    "contents": [{
                        "parts": [{"text": IO_SYSTEM_PROMPT + "\n\n**Raw Input:**\n" + colloquial_input}]
                    }],
                    "generationConfig": {
                        "temperature": 0.3
                    }
                }
                
                headers = {'Content-Type': 'application/json'}
                
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Check if there are candidates
                    if 'candidates' in result and len(result['candidates']) > 0:
                        draft = result['candidates'][0]['content']['parts'][0]['text']
                        
                        st.success("✅ Draft Generated Successfully!")
                        st.markdown("---")
                        
                        # Output Sections
                        st.header("2. Generated Draft & Analysis")
                        st.markdown(draft)
                        
                        # Download Button
                        st.download_button(
                            label="Download Draft (Text)",
                            data=draft,
                            file_name="confession_draft.txt",
                            mime="text/plain"
                        )
                    else:
                        st.error("❌ API returned an empty response. Please review your input.")
                else:
                    error_msg = response.json().get('error', {}).get('message', 'Unknown Error')
                    st.error(f"❌ API Error: {response.status_code} - {error_msg}")

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
