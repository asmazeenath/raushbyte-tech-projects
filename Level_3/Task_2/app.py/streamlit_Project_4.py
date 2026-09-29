import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
import base64
import os

# Page configuration
st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load model
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("garbage_model (1).keras",compile=False)

model = load_model()

classes = [
    "cardboard",
    "glass",
    "metal",
    "paper",
    "plastic",
    "trash"
]


# Background image
with open("img.jpg", "rb") as f:
    img = base64.b64encode(f.read()).decode()

st.markdown(f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{img}");
    background-size: cover;
    background-position: center;
}}
</style>
""", unsafe_allow_html=True)
# General styling
st.markdown(
    """
    <style>

    /* Main text */
    h1, h2, h3, h4, p, label {
        color: white !important;
    }

    /* Horizontal navigation */
    .nav-container {
        background: rgba(0, 40, 20, 0.90);
        padding: 12px 20px;
        border-radius: 18px;
        margin-bottom: 25px;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* Hero */
    .hero {
        background: rgba(0, 35, 18, 0.78);
        padding: 35px;
        border-radius: 25px;
        text-align: center;
        margin-bottom: 25px;
        border: 1px solid rgba(255,255,255,0.2);
    }

    .hero h1 {
        font-size: 45px;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 18px;
    }

    /* Cards */
    .card {
        background: rgba(255,255,255,0.14);
        backdrop-filter: blur(10px);
        padding: 22px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.20);
        text-align: center;
        min-height: 130px;
    }

    .card h2 {
        font-size: 30px;
    }

    .card p {
        font-size: 15px;
    }

    /* Result box */
    .result {
        background: rgba(0, 70, 35, 0.85);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        border: 2px solid rgba(255,255,255,0.2);
    }

    /* Info box */
    .info-box {
        background: rgba(255,255,255,0.12);
        padding: 25px;
        border-radius: 20px;
        margin-top: 20px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: bold;
        height: 45px;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.12);
        padding: 15px;
        border-radius: 18px;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.12);
        padding: 15px;
        border-radius: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Session state
if "page" not in st.session_state:
    st.session_state.page = "Home"

if "prediction_count" not in st.session_state:
    st.session_state.prediction_count = 0

if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = "None"


# Horizontal Navigation
st.markdown(
    """
    <div class="nav-container">
        <h3 style="text-align:center;">
            ♻️ EcoSort AI &nbsp;&nbsp; | &nbsp;&nbsp;
            🤖 AI Waste Classification &nbsp;&nbsp; | &nbsp;&nbsp;
            🌱 Smart Recycling
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

nav1, nav2, nav3, nav4, nav5 = st.columns(5)

with nav1:
    if st.button("🏠 Home"):
        st.session_state.page = "Home"

with nav2:
    if st.button("🔍 Classify"):
        st.session_state.page = "Classify"

with nav3:
    if st.button("📊 Dashboard"):
        st.session_state.page = "Dashboard"

with nav4:
    if st.button("📚 Learn"):
        st.session_state.page = "Learn"

with nav5:
    if st.button("⚙️ Settings"):
        st.session_state.page = "Settings"


# HOME PAGE
if st.session_state.page == "Home":

    st.markdown(
        """
        <div class="hero">
            <h1>♻️ EcoSort AI</h1>
            <p>
            Intelligent Waste Classification Using Deep Learning
            </p>
            <p>
            Upload a waste image and let Artificial Intelligence
            identify the waste category instantly.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            """
            <div class="card">
                <h2>🤖 AI</h2>
                <p>Deep Learning Classification</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="card">
                <h2>♻️ 6</h2>
                <p>Waste Categories</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="card">
                <h2>⚡ Fast</h2>
                <p>Instant Prediction</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div class="card">
                <h2>🌍 Eco</h2>
                <p>Better Waste Segregation</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("🌱 How EcoSort AI Works")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.info("📤 **1. Upload**\n\nUpload an image of waste.")

    with c2:
        st.info("🧠 **2. Analyze**\n\nThe MobileNetV2 model analyzes the image.")

    with c3:
        st.success("♻️ **3. Classify**\n\nAI predicts the waste category.")


# CLASSIFICATION PAGE
elif st.session_state.page == "Classify":

    st.markdown(
        """
        <div class="hero">
            <h1>🔍 AI Waste Classifier</h1>
            <p>Upload an image to identify the type of waste.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("📌 For better results, upload a clear image containing one main waste object.")

    file = st.file_uploader(
        "📤 Upload Waste Image",
        type=["jpg", "jpeg", "png"],
        help="Supported formats: JPG, JPEG and PNG"
    )

    if file:

        img = Image.open(file).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("🖼️ Uploaded Image")
            st.image(
                img
            )

        # Preprocessing
        resized = img.resize((224, 224))
        img_array = np.array(resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        with st.spinner("🤖 AI is analyzing the image..."):

            prediction = model.predict(img_array, verbose=0)

        predicted_index = np.argmax(prediction[0])
        confidence = float(np.max(prediction[0]))

        predicted_class = classes[predicted_index]

        st.session_state.prediction_count += 1
        st.session_state.last_prediction = predicted_class

        with col2:

            st.subheader("🤖 AI Prediction")

            st.markdown(
                f"""
                <div class="result">
                    <h2>♻️ {predicted_class.upper()}</h2>
                    <h3>{confidence * 100:.2f}% Confidence</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                min(int(confidence * 100), 100)
            )

            if confidence >= 0.80:
                st.success("🟢 High confidence prediction")

            elif confidence >= 0.50:
                st.warning("🟡 Moderate confidence prediction")

            else:
                st.error("🔴 Low confidence prediction")

        st.markdown("---")

        st.subheader("🏆 Top 3 Predictions")

        top3 = prediction[0].argsort()[-3:][::-1]

        for rank, index in enumerate(top3, start=1):

            probability = float(prediction[0][index])

            col_a, col_b, col_c = st.columns([1, 4, 2])

            with col_a:
                st.write(f"**#{rank}**")

            with col_b:
                st.write(classes[index].upper())

            with col_c:
                st.write(f"**{probability * 100:.2f}%**")

            st.progress(
                min(int(probability * 100), 100)
            )

        st.markdown("---")

        # Recycling information
        recycling_info = {
            "cardboard": "📦 Cardboard can usually be recycled. Keep it clean and dry.",
            "glass": "🍾 Glass containers can generally be recycled. Separate them from other waste.",
            "metal": "🥫 Metals such as cans can often be recycled and reused.",
            "paper": "📄 Clean paper can usually enter paper recycling streams.",
            "plastic": "🧴 Check local recycling rules because different plastics have different recycling requirements.",
            "trash": "🗑️ General trash should be disposed of according to local waste-management rules."
        }

        st.subheader("🌱 Smart Recycling Tip")

        st.success(
            recycling_info[predicted_class]
        )


# DASHBOARD PAGE
elif st.session_state.page == "Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>📊 EcoSort Dashboard</h1>
            <p>Monitor your AI waste classification activity.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "🔍 Images Classified",
            st.session_state.prediction_count
        )

    with col2:
        st.metric(
            "♻️ Waste Classes",
            len(classes)
        )

    with col3:
        st.metric(
            "🧠 AI Model",
            "MobileNetV2"
        )

    st.markdown("---")

    st.subheader("🗂️ Supported Waste Categories")

    cols = st.columns(3)

    icons = {
        "cardboard": "📦",
        "glass": "🍾",
        "metal": "🥫",
        "paper": "📄",
        "plastic": "🧴",
        "trash": "🗑️"
    }

    for i, waste in enumerate(classes):

        with cols[i % 3]:

            st.markdown(
                f"""
                <div class="card">
                    <h2>{icons[waste]}</h2>
                    <h3>{waste.upper()}</h3>
                    <p>AI Classification Category</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("🧠 Latest Prediction")

    st.info(
        f"Last detected waste: **{st.session_state.last_prediction.upper()}**"
    )


# LEARN PAGE
elif st.session_state.page == "Learn":

    st.markdown(
        """
        <div class="hero">
            <h1>📚 Learn About Waste</h1>
            <p>Understanding waste classification and recycling.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("♻️ Why Waste Classification Matters")

    st.write(
        """
        Waste classification helps separate different materials so that
        suitable materials can be reused, recycled, processed or disposed
        of appropriately.
        """
    )

    st.markdown("---")
    icons = {
    "cardboard": "📦",
    "glass": "🍾",
    "metal": "🥫",
    "paper": "📄",
    "plastic": "🧴",
    "trash": "🗑️"
}
    for waste in classes:

        with st.expander(
            f"{icons[waste]} {waste.upper()}"
        ):

            if waste == "cardboard":
                st.write(
                    "Cardboard is commonly used for boxes and packaging. "
                    "Clean cardboard can often be recycled."
                )

            elif waste == "glass":
                st.write(
                    "Glass is commonly used for bottles and containers. "
                    "Recycling requirements depend on the local waste system."
                )

            elif waste == "metal":
                st.write(
                    "Metal waste includes materials such as cans and metal containers. "
                    "Many metals can be recovered and recycled."
                )

            elif waste == "paper":
                st.write(
                    "Paper is widely used for documents, newspapers and packaging. "
                    "Clean paper is commonly recyclable."
                )

            elif waste == "plastic":
                st.write(
                    "Plastic includes many different resin types. "
                    "Recycling availability varies by material and location."
                )

            else:
                st.write(
                    "Trash represents waste that does not belong to the "
                    "specific recyclable categories detected by this model."
                )


# SETTINGS PAGE
elif st.session_state.page == "Settings":

    st.markdown(
        """
        <div class="hero">
            <h1>⚙️ Settings</h1>
            <p>Customize your EcoSort AI experience.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🎨 Interface Settings")

    show_tips = st.toggle(
        "🌱 Show recycling tips",
        value=True
    )

    show_confidence = st.toggle(
        "📊 Show confidence score",
        value=True
    )

    st.markdown("---")

    st.subheader("🧠 Model Information")

    st.write("**Model:** MobileNetV2")
    st.write("**Framework:** TensorFlow / Keras")
    st.write("**Input Size:** 224 × 224 pixels")
    st.write("**Number of Classes:** 6")

    st.markdown("---")

    if st.button("🗑️ Reset Dashboard"):

        st.session_state.prediction_count = 0
        st.session_state.last_prediction = "None"

        st.success("Dashboard reset successfully!")


# Footer
st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;">
        <p>♻️ <b>EcoSort AI</b> | Deep Learning Waste Classification</p>
        <p>🌱 Building smarter and cleaner waste-management solutions</p>
    </div>
    """,
    unsafe_allow_html=True
)