import streamlit as st
from google import genai
import json

# Page Configuration
st.set_page_config(page_title="AI Vibe Generator", page_icon="✨", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main { background-color: #0f1116; color: #ffffff; }
    .vibe-card { padding: 20px; border-radius: 15px; border: 1px solid #30363d; background-color: #161b22; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# 🔒 SECURITY FIXED: Ab key direct Streamlit Secrets se load hogi
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    st.error("⚠️ Streamlit Cloud Secrets mein GOOGLE_API_KEY nahi mili!")
    st.stop()

# Initialize the Gemini Client
client = genai.Client(api_key=GOOGLE_API_KEY)

st.title("✨ AI Vibe Check Generator")
st.write("Apna current mood ya thought likho, aur AI aapko uski puri aesthetic vibe generate karke dega!")

# User Input
user_input = st.text_input("Aapki vibe kya hai aaj?", placeholder="e.g., Cyberpunk neon night, peaceful mountain rain...")

if st.button("Generate Vibe 🔮"):
    if user_input:
        with st.spinner("Decoding your vibe... 🌌"):
            try:
                # System prompt for Hinglish JSON output
                prompt = f"""
                Analyze the following mood/text and return a JSON object representing its aesthetic 'vibe'.
                Text: "{user_input}"
                
                Respond ONLY with a JSON object in this exact format. The values should be short and in easy Hinglish (Hindi + English mix):
                {{
                    "vibe_name": "Name of the vibe",
                    "dominant_color": "#HEXCODE",
                    "secondary_color": "#HEXCODE",
                    "description": "A very short poetic description in easy Hinglish explaining the mood",
                    "music_genre": "Specific music style or best song type to listen in Hinglish",
                    "outfit_idea": "Quick description of what to wear matching this vibe in Hinglish"
                }}
                """
                
                # Using the updated model
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=prompt,
                )
                
                # Clean up markdown code blocks if any
                clean_text = response.text.replace("```json", "").replace("```", "").strip()
                vibe_data = json.loads(clean_text)
                
                # Display Results
                st.balloons()
                st.markdown(f"### 🎯 Your Vibe: **{vibe_data['vibe_name']}**")
                
                # Color Palette Preview
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"<div style='background-color:{vibe_data['dominant_color']}; height:100px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:bold;'>Primary: {vibe_data['dominant_color']}</div>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<div style='background-color:{vibe_data['secondary_color']}; height:100px; border-radius:10px; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:bold;'>Secondary: {vibe_data['secondary_color']}</div>", unsafe_allow_html=True)
                
                # Detailed Info Card with Easy Labels
                st.markdown(f"""
                <div class="vibe-card" style="color: #ffffff;">
                    <h4 style="color: #00f3ff;">📖 Yeh Vibe Kaisi Hai? (Mood Vibes)</h4>
                    <p style="color: #ffffff;">{vibe_data['description']}</p>
                    <h4 style="color: #ff007f;">🎵 Kaun Sa Gaana Sunein? (Songs Match)</h4>
                    <p style="color: #ffffff;">{vibe_data['music_genre']}</p>
                    <h4 style="color: #00f3ff;">🧥 Aaj Kya Pehnein? (Outfit Idea)</h4>
                    <p style="color: #ffffff;">{vibe_data['outfit_idea']}</p>
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Kuch galat hua! Error: {e}")
    else:
        st.error("Please enter some text first!")
