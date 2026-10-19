import streamlit as st
from google import genai

st.set_page_config(
    page_title="GEEK Repair Notes Translator",
    page_icon="🛠️"
)

st.title("GEEK Repair Notes Translator")
st.write("Turn rough technician notes into clear, accurate documentation.")

technician_notes = st.text_area(
    "Paste technician notes here:",
    height=220,
    placeholder="Example: Customer reports that the laptop shuts off when unplugged..."
)

output_mode = st.selectbox(
    "Choose an output mode:",
    [
        "Internal Repair Notes",
        "Customer Summary",
        "Follow-Up Instructions"
    ]
)

if st.button("Generate"):
    if not technician_notes.strip():
        st.warning("Please paste technician notes before generating an output.")
    else:
        try:
            client = genai.Client(
                api_key=st.secrets["GEMINI_API_KEY"]
            )

            prompt = f"""
You are the GEEK Repair Notes Translator.

Rewrite the technician notes using the selected output mode.

Accuracy rules:
- Preserve every confirmed fact.
- Do not invent diagnoses, tests, results, approvals, or repair status.
- Keep completed work separate from pending work.
- If the notes do not establish the overall status, say that the status is unknown.
- Preserve wording such as pending, not tested, not reproduced, or not verified.
- Use clear, professional language.

Selected output mode:
{output_mode}

Technician notes:
{technician_notes}
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            st.subheader("Results")
            st.write(response.text)

        except Exception as error:
            st.error(f"Something went wrong: {error}")
