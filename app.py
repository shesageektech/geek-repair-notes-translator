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

Transform the technician notes according to the selected output mode.

CORE ACCURACY RULES:
- Preserve the meaning of every confirmed fact.
- Separate customer-reported symptoms from technician-confirmed findings.
- Separate completed repair actions from tests and test results.
- Keep pending work separate from completed work.
- Do not place a confirmed finding or test result under Work Completed.
- Do not invent diagnoses, tests, results, approvals, promises, customer contact, next steps, or repair status.
- Do not describe a part as new, used, faulty, damaged, or verified unless the source notes explicitly say so.
- Do not treat reaching BIOS as proof that Windows boots.
- Do not treat a replaced part as proof that the original part was defective unless the notes confirm it.
- Do not use words such as successfully, correctly, fully, properly, resolved, or fixed unless the source notes explicitly support them.
- Preserve limiting language such as not tested, not reproduced, not started, not verified, pending, or in progress.
- Do not say the repair is complete unless the source notes explicitly confirm completion.
- If the overall repair status is missing or unclear, label it as unknown instead of guessing.
- Do not promise future updates or actions unless the source notes explicitly document them.

OUTPUT MODES:
- Internal Repair Notes: Use professional technical documentation with clearly labeled sections.
- Customer Summary: Use clear, customer-friendly language without changing technical facts.
- Follow-Up Instructions: Clearly separate current status, completed work, test results, pending work, and confirmed next steps.

Selected output mode:
{output_mode}

Technician notes:
{technician_notes}
"""

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            st.subheader("Results")
            st.write(response.text)
            with st.expander("Copy Result"):
                st.code(
                    response.text,
                    language=None,
                    wrap_lines=True
                )
            st.download_button(
    label="Download Result",
    data=response.text,
    file_name="geek_repair_notes.txt",
    mime="text/plain"
)

        except Exception as error:
            st.error(f"Something went wrong: {error}")
