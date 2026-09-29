# app.py

import os
import json
import streamlit as st

from dotenv import load_dotenv

from agents.environmental_agent import (
    generate_environmental_report
)

from utils.validators import (
    validate_environment_data,
    parse_json_input
)


# -------------------------------------------------
# Configuration
# -------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="EcoSage",
    page_icon="🌱",
    layout="wide"
)


# -------------------------------------------------
# Session memory
# -------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


if "environment" not in st.session_state:

    st.session_state.environment = {}


# -------------------------------------------------
# Header
# -------------------------------------------------

st.title("🌱 EcoSage")

st.subheader(
    "AI-Powered Environmental Scientist"
)

st.write(
    """
EcoSage combines environmental datasets,
scientific knowledge retrieval and multi-metric
reasoning to generate evidence-backed
biodiversity recommendations.
"""
)


# -------------------------------------------------
# Sidebar
# -------------------------------------------------

with st.sidebar:

    st.header("Environmental Profile")

    country = st.text_input(
        "Country",
        value="India"
    )

    region = st.text_input(
        "Region"
    )

    st.subheader("Soil")

    ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=6.5
    )

    organic_matter = st.number_input(
        "Organic Matter (%)",
        min_value=0.0,
        value=1.0
    )

    soil_moisture = st.number_input(
        "Soil Moisture (%)",
        min_value=0.0,
        max_value=100.0,
        value=20.0
    )

    st.subheader("Climate")

    temperature = st.number_input(
        "Temperature (°C)",
        value=28.0
    )

    rainfall = st.number_input(
        "Annual Rainfall (mm)",
        min_value=0.0,
        value=600.0
    )

    st.subheader("Land")

    crop = st.text_input(
        "Crop",
        value="Wheat"
    )

    land_use = st.selectbox(
        "Land Use",
        [
            "Monoculture",
            "Mixed cropping",
            "Agroforestry",
            "Forest",
            "Degraded land",
            "Other"
        ]
    )

    analyze_button = st.button(
        "🔍 Analyze Environment",
        use_container_width=True
    )


# -------------------------------------------------
# Structured profile
# -------------------------------------------------

environment = {

    "location": {
        "country": country,
        "region": region
    },

    "soil": {
        "ph": ph,
        "organic_matter": organic_matter,
        "soil_moisture": soil_moisture
    },

    "climate": {
        "temperature": temperature,
        "rainfall": rainfall
    },

    "land": {
        "crop": crop,
        "land_use": land_use
    }
}


# -------------------------------------------------
# Analysis
# -------------------------------------------------

if analyze_button:

    missing = validate_environment_data(
        environment
    )

    if missing:

        st.warning(
            "Some environmental information is missing: "
            + ", ".join(missing)
        )

    else:

        with st.spinner(
            "Analyzing environmental conditions..."
        ):

            result = generate_environmental_report(
                environment
            )

        st.session_state.environment = environment

        st.session_state.messages.append({
            "role": "user",
            "content": environment
        })

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["report"]
        })

        st.success(
            "Environmental analysis completed."
        )


# -------------------------------------------------
# Display result
# -------------------------------------------------

if st.session_state.messages:

    for message in st.session_state.messages:

        if message["role"] == "user":

            with st.chat_message("user"):

                st.json(
                    message["content"]
                )

        else:

            with st.chat_message("assistant"):

                st.markdown(
                    message["content"]
                )


# -------------------------------------------------
# Chat input
# -------------------------------------------------

user_question = st.chat_input(
    "Ask about your ecosystem..."
)


if user_question:

    st.chat_message(
        "user"
    ).write(
        user_question
    )

    previous_environment = (
        st.session_state.environment
    )

    if not previous_environment:

        st.warning(
            "Please provide an environmental profile "
            "using the sidebar first."
        )

    else:

        updated_prompt = f"""

Previous environmental profile:

{json.dumps(
    previous_environment,
    indent=2
)}

User question:

{user_question}

Use the previous environmental context when
answering. Connect soil, climate, land-use and
biodiversity variables whenever relevant.

Do not invent scientific evidence.
"""

        with st.spinner(
            "Reasoning from environmental context..."
        ):

            from agents.environmental_agent import client, MODEL

            response = client.models.generate_content(
                model=MODEL,
                contents=updated_prompt
            )

        st.chat_message(
            "assistant"
        ).markdown(
            response.text
        )