import streamlit as st
from automation import automate
import base64
import os

st.set_page_config(
    page_title="AI Automation Assistant",
    page_icon="🤖",
    layout="wide"
)

# Background image
image_path = "image.jpeg"

if os.path.exists(image_path):
    with open(image_path, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(rgba(0,0,0,0.60), rgba(0,0,0,0.60)),
                url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}

        .block-container {{
            max-width: 1100px;
            padding-top: 2rem;
        }}

        .title {{
            text-align: center;
            color: white;
            font-size: 45px;
            font-weight: bold;
            margin-bottom: 5px;
        }}

        .subtitle {{
            text-align: center;
            color: #dddddd;
            font-size: 18px;
            margin-bottom: 30px;
        }}

        .glass {{
            background: rgba(255,255,255,0.12);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.25);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
        }}

        .section-title {{
            color: white;
            font-size: 25px;
            font-weight: bold;
        }}

        .info {{
            color: #eeeeee;
            font-size: 16px;
        }}

        .status {{
            background: rgba(0,200,100,0.20);
            border: 1px solid rgba(0,255,150,0.4);
            border-radius: 12px;
            padding: 12px;
            text-align: center;
            color: white;
            font-weight: bold;
        }}

        h1, h2, h3, p, label {{
            color: white !important;
        }}

        div[data-baseweb="select"] {{
            border-radius: 12px;
        }}

        .stButton > button {{
            width: 100%;
            border-radius: 12px;
            height: 50px;
            font-size: 18px;
            font-weight: bold;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning("Background image 'image.jpeg' was not found.")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

# Header
st.markdown(
    '<div class="title">🤖 AI Automation Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your smart assistant for automating repetitive computer tasks</div>',
    unsafe_allow_html=True
)

# Status
st.markdown(
    '<div class="status">🟢 AI Assistant Ready • Automation System Online</div>',
    unsafe_allow_html=True
)

st.write("")

# Main panel
st.markdown(
    '<div class="glass">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">⚡ Choose an Automation</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="info">Select a task and let Python perform it automatically.</div>',
    unsafe_allow_html=True
)

st.write("")

command = st.selectbox(
    "🎯 Select your command",
    [
        "Open Youtube",
        "Open Google",
        "Open Gmail",
        "Search Google",
        "Create Folder",
        "Take Screenshot",
        "Show Time",
        "Show Date",
        "Open Calculator",
        "Open Notepad",
        "Show Files",
        "Screen size"
    ]
)

st.write("")

# Execute button
if st.button("🚀 Execute Automation"):

    with st.spinner("⚙️ Performing automation..."):
        result = automate(command)

    st.success(result)

    st.session_state.history.append({
        "command": command,
        "result": result
    })

st.markdown("</div>", unsafe_allow_html=True)

# Quick actions
st.markdown(
    '<div class="glass">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">⚡ Quick Actions</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🌐 Google"):
        result = automate("Open Google")
        st.success(result)

with col2:
    if st.button("▶️ YouTube"):
        result = automate("Open Youtube")
        st.success(result)

with col3:
    if st.button("📧 Gmail"):
        result = automate("Open Gmail")
        st.success(result)

with col4:
    if st.button("🕐 Time"):
        result = automate("Show Time")
        st.success(result)

st.markdown("</div>", unsafe_allow_html=True)

# Activity
if st.session_state.history:

    st.markdown(
        '<div class="glass">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">📋 Recent Activity</div>',
        unsafe_allow_html=True
    )

    for item in reversed(st.session_state.history[-5:]):
        st.write(
            f"🤖 **Command:** {item['command']}  \n"
            f"✅ **Result:** {item['result']}"
        )

    if st.button("🗑️ Clear Activity"):
        st.session_state.history = []
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div style="text-align:center; color:white; padding:20px;">
        🤖 AI Automation Assistant | Built with Python + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)