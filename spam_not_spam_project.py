from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel,Field
import streamlit as st
import os

key=os.getenv('gemini_key')

llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash',api_key=key)

class Spamcheck(BaseModel):
    message:str=Field(description="actual review given as prompt")
    result:str=Field(description="Spam or Not Spam")

llm_structure=llm.with_structured_output(Spamcheck)

st.set_page_config(page_title="Spam Detector", layout="wide")

st.markdown("""
<style>
:root{
  --bg:#071026;
  --card:#0b1220;
  --muted:#9aa6b2;
  --accent:#08c8ff;
  --glass: rgba(255,255,255,0.03);
}
body {
  background: radial-gradient(circle at 10% 10%, rgba(8,200,255,0.02), transparent 20%),
              linear-gradient(180deg, #04060a 0%, #071026 100%);
  color: #e6f0f6;
}
header, footer {visibility: hidden;}
.stApp > header {display: none;}

.viewerBadge_link__1S137 {display:none;}

.css-1d391kg {padding-top:0rem;} /* reduce top padding on some streamlit versions */

section.main > div.block-container {
    padding-top: 1.2rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* neon title box */
.neon-box {
  border-radius:14px;
  padding:22px;
  background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
  border: 1px solid rgba(255,255,255,0.04);
  box-shadow: 0 0 40px rgba(8,200,255,0.06), inset 0 0 2px rgba(255,255,255,0.02);
}
.neon-title {
  font-size:32px;
  font-weight:700;
  color: #f2fbff;
  padding:12px;
  border-radius:10px;
  border: 2px solid rgba(8,200,255,0.12);
  box-shadow: 0 6px 40px rgba(8,200,255,0.16);
}

/* text area */
textarea, .stTextArea>div>textarea {
  background: rgba(255,255,255,0.02) !important;
  color: #e6f0f6 !important;
  border-radius:10px !important;
  border: 1px solid rgba(255,255,255,0.03) !important;
  padding:14px !important;
  min-height:110px;
}

/* button */
.stButton>button {
  background: linear-gradient(90deg, rgba(8,200,255,0.14), rgba(10,120,255,0.08));
  color: #dff7ff;
  border-radius:12px;
  padding:12px 22px;
  border: 1px solid rgba(8,200,255,0.18);
  font-weight:600;
  box-shadow: 0 8px 30px rgba(8,200,255,0.06);
}
.stButton>button:hover { transform: translateY(-2px); }

/* result cards */
.result-card {
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.02));
  border-radius:12px;
  padding:18px;
  border: 1px solid rgba(255,255,255,0.03);
  box-shadow: 0 8px 30px rgba(2,6,12,0.6);
  margin-bottom:12px;
}

/* sidebar tweaks */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.02));
  border-right: 1px solid rgba(255,255,255,0.02);
}
.stSidebar .stButton>button { width:100%; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("D:/Gen AI/Gen AI/image2.webp")
    st.markdown("**About Spam Detector**")
    st.write("This app uses an advanced AI model classify messages as **Spam** or **Not Spam**.")

    st.markdown("💡 Why Spam Check?")
    st.write("""
    - Detects fraud messages
    - Prevents phishing attacks
    - Protects users from scam
    """)    

    st.markdown("📞 Contact Us")
    st.write("support@example.com\n+91 9876543210")

    st.markdown("🆘 Help")
    st.write("Enter a message and click *Check Spam*. The AI will classify it instantly.")

st.markdown(
    """
    <div class="neon-box"><div class="neon-title">
        🛡️ Spam / Not-Spam Classifier
    </div></div>
    """,
    unsafe_allow_html=True
)

st.write("Enter a message below and click **Check Spam**.")

message=st.text_area(
    "Enetr Message:",
    height=150,
    placeholder="Type your message here..."
)

if st.button("🔍 Check Spam", use_container_width=True):
    if message.strip() == "":
        st.warning("⚠️ Please enter a message!")
    else:
        with st.spinner("Analyzing with AI..."):
            res=llm_structure.invoke(
                f"""
                Classify the following message strictly as Spam or Not Spam.
                Message: {message}
                """
            )

        st.markdown("## 🔎 Result")
        st.write("**Message:**", res.message)

        if res.result.lower() == "spam":
            st.error("🚫 **Spam — This message looks suspicious!**")
        else:
            st.success("✅ **Not Spam — This message looks safe.**")