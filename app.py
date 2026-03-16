import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables (if any .env file is present)
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

if api_key_input:
    genai.configure(api_key=api_key_input)
else:
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
**Role:** Senior Investigation Officer & Legal Expert (Tamil Nadu Police Standard).
**Goal:** Draft 100% Admissible Confession Statements in Formal Tamil, avoiding all acquittal flaws.

**STRICT DRAFTING LOGIC (Based on Recent Judgments):**
1. **Voluntariness Check:** Statement-il "எந்தவித அச்சுறுத்தலோ, தூண்டுதலோ இன்றி நான் மனப்பூர்வமாக கூறுகிறேன்" endru kandippa irukka vendum.
2. **The "Exclusive Knowledge" Clause (Sec 27):** Weapon maraikkapatta idhai ezhudhum podhu, "காவல்துறைக்கு முன்னரே தெரியாத, எனக்கு மட்டுமே தெரிந்த ரகசிய இடத்தில்" endru kurippida vendum.
3. **Avoid Generalizations:** "Kathiyei eduthu koduthen" enbatharku bathilaaga, "முட்புதருக்குள் மறைத்து வைக்கப்பட்டிருந்த இரத்தக்கறை படிந்த 10 அங்குல அரிவாளை அடையாளம் காட்டி எடுத்துக்கொடுத்தேன்" endru thulliyamaaga irukka vendum.
4. **Time & Sequence:** Arrest neram mudhal recovery varai ulla sangiligal (chain of events) logic-aaga irukka vendum.

**OUTPUT FORMAT:**
1. **Critical Warning:** Draft-ai tharum mun, intha case-la Defense Counsel enga madaikka vaaippu irukku nu alert kodu.
2. **Formal Draft:** Thooya Tamil-il (Legal Court Language) Opputhal Vaku Moolam.

**SYSTEM PROMPT START:**
You are now an IO Agent. When I give raw input in Tamil, analyze the flaws first and then provide the 'Thooya Tamil' legal draft.
"""

# Generation Logic
if st.button("Generate Legal Confession Draft", type="primary"):
    if not api_key_input:
        st.error("❌ Please provide a Google Gemini API Key in the sidebar.")
    elif not colloquial_input.strip():
        st.warning("⚠️ Please provide the input case details.")
    else:
        with st.spinner("Drafting Confession Statement..."):
            try:
                # Initialize Gemini Model
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro",
                    system_instruction=IO_SYSTEM_PROMPT
                )

                # Generate Content
                response = model.generate_content(colloquial_input)
                
                st.success("✅ Draft Generated Successfully!")
                st.markdown("---")
                
                # Output Sections
                st.header("2. Generated Draft & Analysis")
                st.markdown(response.text)
                
                # Download Button
                st.download_button(
                    label="Download Draft (Text)",
                    data=response.text,
                    file_name="confession_draft.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
