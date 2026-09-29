# agents/environmental_agent.py

import os
import time
import pandas as pd

from dotenv import load_dotenv
from google import genai

from rag.retriever import retrieve_scientific_evidence



# LOAD ENVIRONMENT VARIABLES


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY not found. Please add it to your .env file."
    )



# GEMINI CONFIGURATION

client = genai.Client(
    api_key=API_KEY
)


MODEL = "gemini-3.5-flash-lite"

ENVIRONMENTAL_FILE = "data/environmental dataset.csv"
SOIL_FILE = "data/soil.csv"


# LOAD DATASETS

def load_dataset(path):

    if not os.path.exists(path):
        print(f"Dataset not found: {path}")
        return pd.DataFrame()

    try:

        df = pd.read_csv(path)

        print(
            f"Loaded {path}: "
            f"{df.shape[0]} rows, {df.shape[1]} columns"
        )

        return df

    except Exception as e:

        print(
            f"Error loading {path}: {e}"
        )

        return pd.DataFrame()


environmental_df = load_dataset(
    ENVIRONMENTAL_FILE
)

soil_df = load_dataset(
    SOIL_FILE
)


def calculate_risks(data):

    risks = []

    soil = data.get("soil", {})
    climate = data.get("climate", {})
    land = data.get("land", {})

    ph = soil.get("ph")
    organic_matter = soil.get("organic_matter")
    soil_moisture = soil.get("soil_moisture")

    temperature = climate.get("temperature")
    rainfall = climate.get("rainfall")

    land_use = str(
        land.get("land_use", "")
    ).lower()



    if organic_matter is not None:

        if organic_matter < 1:

            risks.append(
                "very_low_soil_organic_matter"
            )

        elif organic_matter < 2:

            risks.append(
                "low_soil_organic_matter"
            )


    if soil_moisture is not None:

        if soil_moisture < 15:

            risks.append(
                "severe_water_stress"
            )

        elif soil_moisture < 25:

            risks.append(
                "water_stress"
            )


    if ph is not None:

        if ph < 5.5:

            risks.append(
                "acidic_soil"
            )

        elif ph > 8:

            risks.append(
                "alkaline_soil"
            )

    # CLIMATE RISKS


    if rainfall is not None:

        if rainfall < 500:

            risks.append(
                "low_rainfall"
            )


    if temperature is not None:

        if temperature > 32:

            risks.append(
                "heat_stress"
            )



    if "monoculture" in land_use:

        risks.append(
            "low_crop_diversity"
        )


    if (
        "deforest" in land_use
        or
        "degraded" in land_use
    ):

        risks.append(
            "habitat_degradation"
        )


    return risks

# MULTI-METRIC REASONING

def generate_reasoning(data, risks):

    reasoning = []
    # RAINFALL + SOIL MOISTURE

    if (
        "low_rainfall" in risks
        and
        (
            "water_stress" in risks
            or
            "severe_water_stress" in risks
        )
    ):

        reasoning.append(
            "Low rainfall combined with low soil "
            "moisture indicates water stress."
        )

    if (
        (
            "low_soil_organic_matter" in risks
            or
            "very_low_soil_organic_matter" in risks
        )
        and
        (
            "water_stress" in risks
            or
            "severe_water_stress" in risks
        )
    ):

        reasoning.append(
            "Low soil organic matter combined with "
            "low soil moisture may reduce soil water "
            "retention and increase drought sensitivity."
        )

    # MONOCULTURE + BIODIVERSITY
   
    if "low_crop_diversity" in risks:

        reasoning.append(
            "Monoculture provides less crop and habitat "
            "diversity than diversified agricultural systems."
        )


    # -----------------------------------------------------
    # MONOCULTURE + LOW RAINFALL
    # -----------------------------------------------------

    if (
        "low_crop_diversity" in risks
        and
        "low_rainfall" in risks
    ):

        reasoning.append(
            "Low rainfall combined with monoculture "
            "can increase ecological vulnerability because "
            "water availability and habitat diversity are "
            "both constrained."
        )


    # -----------------------------------------------------
    # HEAT + WATER STRESS
    # -----------------------------------------------------

    if (
        "heat_stress" in risks
        and
        (
            "water_stress" in risks
            or
            "severe_water_stress" in risks
        )
    ):

        reasoning.append(
            "Heat stress combined with water stress can "
            "increase plant stress and reduce habitat "
            "suitability for sensitive species."
        )


    # -----------------------------------------------------
    # HABITAT DEGRADATION
    # -----------------------------------------------------

    if "habitat_degradation" in risks:

        reasoning.append(
            "Degraded land can reduce habitat quality "
            "and ecological connectivity."
        )


    return reasoning


# =========================================================
# DATASET RETRIEVAL
# =========================================================

def retrieve_dataset_context(data):

    context = []

    location = data.get(
        "location",
        {}
    )

    country = location.get(
        "country"
    )

    region = location.get(
        "region"
    )


    # -----------------------------------------------------
    # ENVIRONMENTAL DATASET
    # -----------------------------------------------------

    if not environmental_df.empty:

        df = environmental_df.copy()

        country_columns = [
            c for c in df.columns
            if c.lower().strip() == "country"
        ]


        if country and country_columns:

            country_column = country_columns[0]

            matched = df[
                df[country_column]
                .astype(str)
                .str.lower()
                .str.strip()
                ==
                str(country).lower().strip()
            ]


            if not matched.empty:

                context.append({
                    "type": "environmental_dataset",
                    "location": country,
                    "records": matched.tail(5).to_dict(
                        orient="records"
                    )
                })


    # -----------------------------------------------------
    # SOIL DATASET
    # -----------------------------------------------------

    if not soil_df.empty:

        context.append({
            "type": "soil_dataset",
            "region": region,
            "records": soil_df.head(5).to_dict(
                orient="records"
            )
        })


    return context


# =========================================================
# RECOMMENDATION ENGINE
# =========================================================

def determine_interventions(risks):

    recommendations = []


    # -----------------------------------------------------
    # LOW ORGANIC MATTER
    # -----------------------------------------------------

    if (
        "low_soil_organic_matter" in risks
        or
        "very_low_soil_organic_matter" in risks
    ):

        recommendations.append(
            "Introduce suitable cover crops and "
            "organic-residue management."
        )


    # -----------------------------------------------------
    # WATER STRESS
    # -----------------------------------------------------

    if (
        "water_stress" in risks
        or
        "severe_water_stress" in risks
    ):

        recommendations.append(
            "Improve soil water retention using "
            "vegetation cover, mulching and "
            "water-efficient land management."
        )


    # -----------------------------------------------------
    # MONOCULTURE
    # -----------------------------------------------------

    if "low_crop_diversity" in risks:

        recommendations.append(
            "Introduce ecologically suitable crop "
            "diversification or intercropping."
        )


    # -----------------------------------------------------
    # HABITAT DEGRADATION
    # -----------------------------------------------------

    if "habitat_degradation" in risks:

        recommendations.append(
            "Restore native vegetation patches and "
            "improve habitat connectivity."
        )


    # -----------------------------------------------------
    # HEAT + WATER STRESS
    # -----------------------------------------------------

    if (
        "heat_stress" in risks
        and
        (
            "water_stress" in risks
            or
            "severe_water_stress" in risks
        )
    ):

        recommendations.append(
            "Evaluate locally appropriate agroforestry "
            "or native vegetation systems where water "
            "availability permits."
        )


    return recommendations


# =========================================================
# GEMINI RETRY FUNCTION
# =========================================================

def generate_with_retry(
    prompt,
    retries=3
):

    for attempt in range(retries):

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            return response


        except Exception as e:

            error_text = str(e)

            # Retry temporary Gemini server errors

            if (
                "503" in error_text
                or
                "UNAVAILABLE" in error_text
                or
                "429" in error_text
                or
                "RESOURCE_EXHAUSTED" in error_text
            ):

                if attempt < retries - 1:

                    wait_time = 5 * (
                        attempt + 1
                    )

                    print(
                        f"Gemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(
                        wait_time
                    )

                else:

                    raise e

            else:

                raise e


    return None


# =========================================================
# MAIN ENVIRONMENTAL REPORT
# =========================================================

def generate_environmental_report(data):

    # -----------------------------------------------------
    # STEP 1: Calculate risks
    # -----------------------------------------------------

    risks = calculate_risks(
        data
    )


    # -----------------------------------------------------
    # STEP 2: Multi-metric reasoning
    # -----------------------------------------------------

    reasoning = generate_reasoning(
        data,
        risks
    )


    # -----------------------------------------------------
    # STEP 3: Determine interventions
    # -----------------------------------------------------

    recommendations = determine_interventions(
        risks
    )


    # -----------------------------------------------------
    # STEP 4: Retrieve dataset information
    # -----------------------------------------------------

    dataset_context = retrieve_dataset_context(
        data
    )


    # -----------------------------------------------------
    # STEP 5: Build RAG query
    # -----------------------------------------------------

    query = f"""
Environmental conditions:

{data}

Detected environmental risks:

{risks}

Multi-metric reasoning:

{reasoning}

Potential interventions:

{recommendations}
"""


    # -----------------------------------------------------
    # STEP 6: Retrieve scientific evidence
    # -----------------------------------------------------

    scientific_evidence = (
        retrieve_scientific_evidence(
            query,
            top_k=5
        )
    )


    # -----------------------------------------------------
    # STEP 7: Format evidence
    # -----------------------------------------------------

    evidence_text = "\n\n".join(
        [
            f"Source: {e['source']}\n"
            f"Title: {e['title']}\n"
            f"Evidence: {e['text']}"
            for e in scientific_evidence
        ]
    )


    # -----------------------------------------------------
    # STEP 8: Gemini prompt
    # -----------------------------------------------------

    prompt = f"""
You are EcoSage, an AI environmental scientist.

Your task is to analyze environmental conditions and
generate evidence-grounded recommendations for improving
ecosystem health and biodiversity.

IMPORTANT RULES:

1. Do NOT invent scientific studies.

2. Do NOT invent numerical improvement percentages.

3. Only provide quantitative estimates when the retrieved
scientific evidence supports them.

4. Clearly distinguish:
   - User-provided measurements
   - Dataset measurements
   - Scientific evidence

5. Connect at least THREE environmental variables whenever
   sufficient information is available.

6. Every recommendation must include:

   - What to do
   - Why it works
   - Environmental metrics affected
   - Time horizon
   - Scientific evidence

7. If scientific evidence is insufficient for a specific
claim, explicitly state that.

8. Do not give generic advice such as:
   "Use sustainable practices."

9. Consider interactions between:

   Soil
   Water
   Climate
   Land use
   Biodiversity
   Human impact

USER ENVIRONMENTAL PROFILE:

{data}


DATASET CONTEXT:

{dataset_context}


DETECTED RISKS:

{risks}


MULTI-METRIC REASONING:

{reasoning}


SCIENTIFIC KNOWLEDGE RETRIEVED FROM RAG:

{evidence_text}


Return the answer using exactly this structure:

## 🌱 Environmental Assessment

### Current Conditions

Explain the important environmental conditions.

### 🔗 Multi-Metric Reasoning

Explain how at least three environmental variables
interact.

### 🌿 Recommendation 1

**What to do:**

**Why it works:**

**Impacted metrics:**

**Time horizon:**

**Scientific evidence:**

### 🌳 Recommendation 2

**What to do:**

**Why it works:**

**Impacted metrics:**

**Time horizon:**

**Scientific evidence:**

### 📊 Key Metrics to Monitor

List measurable indicators that should be monitored.

### 🎯 Confidence

Give a qualitative confidence level such as High,
Medium or Low.

Explain what information supports the confidence level
and what additional information would improve it.
"""


    # -----------------------------------------------------
    # STEP 9: Generate Gemini response
    # -----------------------------------------------------

    response = generate_with_retry(
        prompt
    )


    # -----------------------------------------------------
    # STEP 10: Return complete result
    # -----------------------------------------------------

    return {
        "report": response.text,
        "risks": risks,
        "reasoning": reasoning,
        "recommendations": recommendations,
        "evidence": scientific_evidence
    }
