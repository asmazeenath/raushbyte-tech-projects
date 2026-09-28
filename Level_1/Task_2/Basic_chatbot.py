import streamlit as st
from datetime import datetime
import time
import base64
import os
import re

st.set_page_config(
    page_title="Smart Rule-Based Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "bot_name" not in st.session_state:
    st.session_state.bot_name = "Nova"

if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

if "response_delay" not in st.session_state:
    st.session_state.response_delay = 0.5

if "user_count" not in st.session_state:
    st.session_state.user_count = 0

if "bot_count" not in st.session_state:
    st.session_state.bot_count = 0


def set_background(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image:
            encoded = base64.b64encode(image.read()).decode()

        css = f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
        }}

        .stApp::before {{
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.55);
            z-index: 0;
            pointer-events: none;
        }}

        .main .block-container {{
            position: relative;
            z-index: 1;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}

        .content-frame {{
            background: rgba(10, 15, 30, 0.94);
            border-radius: 25px;
            padding: 30px;
            border: 1px solid rgba(255,255,255,0.18);
            box-shadow: 0 15px 40px rgba(0,0,0,0.45);
            margin-bottom: 20px;
        }}

        .chat-frame {{
            background: rgba(10, 15, 30, 0.96);
            border-radius: 25px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.18);
            box-shadow: 0 20px 50px rgba(0,0,0,0.55);
            margin-bottom: 20px;
        }}

        .chat-header {{
            background: rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px 22px;
            border: 1px solid rgba(255,255,255,0.15);
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .bot-icon {{
            font-size: 45px;
        }}

        .bot-title {{
            font-size: 28px;
            font-weight: 700;
            color: white;
        }}

        .bot-status {{
            font-size: 14px;
            color: #6ee7b7;
            margin-top: 4px;
        }}

        .chat-description {{
            color: #cbd5e1;
            font-size: 16px;
            margin-top: 15px;
        }}

        .stApp p,
        .stApp label,
        .stApp span {{
            color: white;
        }}

        h1, h2, h3, h4 {{
            color: white !important;
        }}

        [data-testid="stSidebar"] {{
            background: rgba(8, 12, 25, 0.98);
            border-right: 1px solid rgba(255,255,255,0.10);
        }}

        [data-testid="stSidebar"] * {{
            color: white !important;
        }}

        [data-testid="stMetric"] {{
            background: rgba(15, 23, 42, 0.96);
            border-radius: 18px;
            padding: 18px;
            border: 1px solid rgba(255,255,255,0.15);
        }}

        [data-testid="stMetricValue"] {{
            color: white !important;
        }}

        [data-testid="stMetricLabel"] {{
            color: #cbd5e1 !important;
        }}

        [data-testid="stChatInput"] {{
            background: rgba(10, 15, 30, 0.98);
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.20);
        }}

        [data-testid="stChatInput"] textarea {{
            color: white !important;
            background: transparent !important;
        }}

        [data-testid="stChatInput"] textarea::placeholder {{
            color: #94a3b8 !important;
        }}

        [data-testid="stChatMessage"] {{
            background: rgba(15, 23, 42, 0.95);
            border-radius: 18px;
            padding: 12px;
            margin-bottom: 10px;
            border: 1px solid rgba(255,255,255,0.10);
        }}

        .stButton > button {{
            background: rgba(30, 41, 59, 0.96);
            color: white !important;
            border: 1px solid rgba(255,255,255,0.20);
            border-radius: 12px;
            min-height: 42px;
        }}

        .stButton > button:hover {{
            background: rgba(51, 65, 85, 1);
        }}

        .stTextInput input {{
            background: rgba(15, 23, 42, 0.96) !important;
            color: white !important;
            border: 1px solid rgba(255,255,255,0.20) !important;
            border-radius: 12px;
        }}

        .stTextInput input::placeholder {{
            color: #94a3b8 !important;
        }}

        [data-baseweb="select"] > div {{
            background: rgba(15, 23, 42, 0.96) !important;
            color: white !important;
            border-radius: 12px;
        }}

        [data-testid="stAlert"] {{
            background: rgba(15, 23, 42, 0.96);
            color: white;
        }}

        hr {{
            border-color: rgba(255,255,255,0.15);
        }}

        .info-card {{
            background: rgba(15, 23, 42, 0.94);
            border-radius: 18px;
            padding: 20px;
            margin: 10px 0;
            border: 1px solid rgba(255,255,255,0.12);
        }}
        </style>
        """

        st.markdown(css, unsafe_allow_html=True)


set_background("image/img.jpeg")


def chatbot_response(user_input):
    text = user_input.lower().strip()

    if any(word in text for word in [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]):
        return (
            f"Hello! 👋 I am {st.session_state.bot_name}. "
            "How can I help you today?"
        )

    elif "your name" in text or "who are you" in text:
        return (
            f"My name is {st.session_state.bot_name}. 🤖 "
            "I am a rule-based chatbot created using Python and Streamlit."
        )

    elif "what is chatbot" in text:
        return (
            "A chatbot is a software application that communicates "
            "with users through text or voice. I use predefined rules "
            "to understand keywords and generate responses."
        )

    elif "how do you work" in text or "how you work" in text:
        return (
            "I work using predefined rules. 🧠\n\n"
            "Your message → Keyword matching → Rule selection → Response"
        )

    elif "artificial intelligence" in text or text == "ai":
        return (
            "Artificial Intelligence is a technology that enables "
            "computers to perform tasks that normally require human "
            "intelligence, such as learning, reasoning and language processing."
        )

    elif "machine learning" in text:
        return (
            "Machine Learning is a branch of AI where computers learn "
            "patterns from data and use those patterns to make predictions "
            "or decisions."
        )

    elif "python" in text:
        return (
            "Python is a popular programming language used in AI, "
            "machine learning, data science, automation and web development."
        )

    elif "streamlit" in text:
        return (
            "Streamlit is a Python framework that makes it easy to build "
            "interactive web applications for data science and machine learning."
        )

    elif "college" in text:
        return (
            "I can help you with basic programming, AI, ML and "
            "computer-science related questions."
        )

    elif "help" in text:
        return (
            "Here are some things you can ask me:\n\n"
            "• What is AI?\n"
            "• What is Machine Learning?\n"
            "• What is Python?\n"
            "• What is Streamlit?\n"
            "• What is a chatbot?\n"
            "• What time is it?\n"
            "• Tell me a joke\n"
            "• Calculate 25 + 50"
        )

    elif "time" in text:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}. ⏰"

    elif "date" in text or "today" in text:
        current_date = datetime.now().strftime("%d %B %Y")
        return f"Today's date is {current_date}. 📅"

    elif "joke" in text:
        return (
            "Why do programmers prefer dark mode? 😄\n\n"
            "Because light attracts bugs! 🐛"
        )

    elif "thank" in text:
        return (
            "You're welcome! 😊 "
            "Let me know if you need anything else."
        )

    elif "bye" in text or "goodbye" in text:
        return "Goodbye! 👋 Have a great day!"

    elif "calculate" in text:
        expression = text.replace("calculate", "").strip()

        try:
            if re.fullmatch(r"[0-9+\-*/(). ]+", expression):
                result = eval(expression)
                return f"The answer is **{result}** 🧮"
        except Exception:
            pass

        return "Please enter a simple calculation such as `calculate 25 + 50`."

    else:
        return (
            "I'm still learning! 🤔\n\n"
            "I don't have a predefined response for that question.\n\n"
            "Try asking:\n"
            "• What is AI?\n"
            "• What is Python?\n"
            "• What is Machine Learning?\n"
            "• Tell me a joke\n"
            "• What time is it?"
        )


st.sidebar.title("🤖 Nova Chatbot")

st.sidebar.write("### Navigation")

page = st.sidebar.radio(
    "Select Page",
    [
        "🏠 Home",
        "💬 Chatbot",
        "✨ Features",
        "⚙️ Settings",
        "ℹ️ About"
    ]
)

st.sidebar.divider()

st.sidebar.write("### Quick Settings")

sidebar_bot_name = st.sidebar.text_input(
    "🤖 Bot Name",
    value=st.session_state.bot_name,
    key="sidebar_bot_name"
)

if st.sidebar.button("💾 Save Name"):

    if sidebar_bot_name.strip():

        st.session_state.bot_name = sidebar_bot_name.strip()

        st.sidebar.success(
            f"Name changed to {st.session_state.bot_name}!"
        )

        st.rerun()

    else:
        st.sidebar.warning("Please enter a chatbot name.")


st.session_state.response_delay = st.sidebar.slider(
    "Response Delay",
    0.0,
    2.0,
    st.session_state.response_delay,
    0.1
)


if st.sidebar.button("🧹 Clear Chat"):

    st.session_state.messages = []
    st.session_state.user_count = 0
    st.session_state.bot_count = 0

    st.rerun()


if page == "🏠 Home":

    st.title(
        f"🤖 Welcome to {st.session_state.bot_name} Chatbot"
    )

    st.subheader(
        "A Simple Rule-Based Chatbot using Python + Streamlit"
    )

    st.markdown(
        """
        <div class="content-frame">
        <p>
        This project demonstrates how a basic chatbot can
        understand predefined user inputs and provide
        appropriate responses.
        </p>

        <p>
        The chatbot uses keyword matching, conditional
        statements and predefined responses to simulate
        a simple conversational AI system.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "User Messages",
            st.session_state.user_count
        )

    with col2:
        st.metric(
            "Bot Responses",
            st.session_state.bot_count
        )

    with col3:
        st.metric(
            "Chatbot Type",
            "Rule-Based"
        )

    st.divider()

    st.subheader("🚀 What Can I Do?")

    st.markdown(
        """
        <div class="info-card">
        <p>💬 Answer predefined questions</p>
        <p>🔎 Recognize common keywords</p>
        <p>😂 Tell jokes</p>
        <p>⏰ Show date and time</p>
        <p>🧮 Perform basic calculations</p>
        <p>🤖 Explain AI concepts</p>
        <p>🐍 Explain Python and Streamlit</p>
        <p>💾 Maintain chat history</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Go to the 💬 Chatbot page from the sidebar to start chatting."
    )


elif page == "💬 Chatbot":

    st.markdown(
        f"""
        <div class="chat-frame">

            <div class="chat-header">

                <div class="bot-icon">
                    🤖
                </div>

                <div>
                    <div class="bot-title">
                        {st.session_state.bot_name} AI Assistant
                    </div>

                    <div class="bot-status">
                        ● Online • Ready to chat
                    </div>
                </div>

            </div>

            <div class="chat-description">
                Ask me something from my predefined knowledge base.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:

        if message["role"] == "user":

            with st.chat_message(
                "user",
                avatar="👤"
            ):
                st.write(message["content"])

        else:

            with st.chat_message(
                "assistant",
                avatar="🤖"
            ):
                st.write(message["content"])


    user_input = st.chat_input(
        "💬 Type your message to "
        + st.session_state.bot_name
        + "..."
    )


    if user_input:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        st.session_state.user_count += 1

        with st.chat_message(
            "user",
            avatar="👤"
        ):
            st.write(user_input)

        response = chatbot_response(user_input)

        with st.chat_message(
            "assistant",
            avatar="🤖"
        ):

            if st.session_state.response_delay > 0:

                with st.spinner(
                    f"{st.session_state.bot_name} is typing..."
                ):
                    time.sleep(
                        st.session_state.response_delay
                    )

            st.write(response)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response
            }
        )

        st.session_state.bot_count += 1


elif page == "✨ Features":

    st.title("✨ Chatbot Features")

    st.markdown(
        """
        <div class="content-frame">

        <h3>🤖 Rule-Based Conversation</h3>
        <p>
        The chatbot uses predefined conditions and keyword
        matching to determine the appropriate response.
        </p>

        <h3>💬 Natural Chat Interface</h3>
        <p>
        Users can communicate with the chatbot using
        Streamlit's interactive chat interface.
        </p>

        <h3>🧮 Calculator</h3>
        <p>
        The chatbot can perform simple mathematical calculations.
        </p>

        <h3>⏰ Date and Time</h3>
        <p>
        Ask the chatbot for the current date or time.
        </p>

        <h3>😂 Entertainment</h3>
        <p>
        Ask the chatbot to tell you a joke.
        </p>

        <h3>📚 AI Knowledge</h3>
        <p>
        The chatbot provides predefined explanations about
        Artificial Intelligence, Machine Learning, Python,
        Streamlit and Chatbots.
        </p>

        <h3>💾 Chat History</h3>
        <p>
        Conversation messages are maintained during the
        current Streamlit session.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


elif page == "⚙️ Settings":

    st.title("⚙️ Chatbot Settings")

    st.subheader("🤖 Bot Configuration")

    new_name = st.text_input(
        "Change chatbot name",
        value=st.session_state.bot_name,
        key="settings_bot_name"
    )

    if st.button("💾 Save Bot Name"):

        if new_name.strip():

            st.session_state.bot_name = new_name.strip()

            st.success(
                f"Bot name changed to {st.session_state.bot_name}! 🎉"
            )

            st.rerun()

        else:
            st.warning("Please enter a chatbot name.")


    st.subheader("⏱️ Response Settings")

    delay = st.slider(
        "Response delay",
        0.0,
        3.0,
        st.session_state.response_delay,
        0.1
    )

    st.session_state.response_delay = delay


    st.subheader("🎨 Appearance")

    theme = st.selectbox(
        "Select theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1
    )

    st.session_state.theme = theme

    st.divider()

    st.write("### Current Configuration")

    st.markdown(
        f"""
        <div class="info-card">

        <p>
        🤖 <b>Bot Name:</b>
        {st.session_state.bot_name}
        </p>

        <p>
        ⏱️ <b>Response Delay:</b>
        {st.session_state.response_delay} seconds
        </p>

        <p>
        🎨 <b>Theme:</b>
        {st.session_state.theme}
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button("🔄 Reset Settings"):

        st.session_state.bot_name = "Nova"
        st.session_state.response_delay = 0.5
        st.session_state.theme = "Dark"

        st.success("Settings reset successfully!")

        st.rerun()


elif page == "ℹ️ About":

    st.title("ℹ️ About This Project")

    st.markdown(
        """
        <div class="content-frame">

        <h3>🤖 Basic Rule-Based Chatbot</h3>

        <p>
        This project was developed as an introductory
        Artificial Intelligence project.
        </p>

        <p>
        The chatbot does not use a large language model
        or external API. Instead, it uses predefined rules,
        keyword matching and conditional statements.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🛠️ Technologies Used")

    st.markdown(
        """
        <div class="info-card">

        <p>🐍 Python</p>
        <p>🎈 Streamlit</p>
        <p>🔀 Conditional Statements</p>
        <p>🔤 String Processing</p>
        <p>💾 Session State</p>
        <p>🧠 Rule-Based Logic</p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🔄 How It Works")

    st.markdown(
        """
        <div class="content-frame">

        <p>👤 <b>User Input</b></p>
        <p>⬇️</p>
        <p>🔤 <b>Text Processing</b></p>
        <p>⬇️</p>
        <p>🔎 <b>Keyword Matching</b></p>
        <p>⬇️</p>
        <p>⚙️ <b>Rule Selection</b></p>
        <p>⬇️</p>
        <p>💬 <b>Predefined Response</b></p>
        <p>⬇️</p>
        <p>🖥️ <b>Display Response</b></p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.success(
        "This project was done by Zeenath Asma."
    )