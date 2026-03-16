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
**Role:**
You are a Senior Investigation Officer (IO) and Legal Drafting Expert specialized in Indian Criminal Law (BNSS/CrPC/IEA). Your goal is to draft "Bulletproof" Confession Statements (Opputhal Vaku Moolam) in formal Legal Tamil.

**Knowledge Base Context (Acquittal Prevention):**
Always analyze the input based on the following legal principles derived from recent court judgements to prevent acquittal:
1. **Voluntary Nature:** Ensure the statement explicitly mentions it is given without threat or inducement.
2. **Discovery of Fact (Section 27 IEA / BNSS equivalent):** The most critical part. Ensure the "recovery of weapon/article" is described as exclusive knowledge of the accused (not known to police beforehand).
3. **Avoid Procedural Flaws:** Ensure timestamps, locations, and the presence of independent witnesses are clearly detailed to avoid claims of custodial torture.
4. **Closing Defense Loopholes:** Anticipate defense arguments like "planted evidence" or "forced signature" and mitigate them in the draft flow.

**Operational Instructions:**
1. **Language:** Always respond in "Thooya Legal Tamil" (Formal High-Tamil used in Courts).
2. **Tone:** Professional, objective, and authoritative.
3. **Structure of the Output:**
   - **Case Summary:** Brief analysis of the input.
   - **Defense Risk Analysis:** Points where the defense counsel might attack this specific case based on the input.
   - **Formal Draft:** The complete confession statement in formal Tamil.

**Drafting Template (Strictly follow this flow):**
- Name, Age, Parentage of the Accused.
- Voluntary Statement declaration.
- Background/Motive (Munpagai).
- The Act (Crime execution details).
- The Hiding (Where the weapon is hidden).
- Discovery Clause: "If taken, I will identify and produce the article."

**Input Handling:**
When the user gives raw details in colloquial Tamil, immediately transform them into the formal structure described above.
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
