import streamlit as st
from google import genai

st.set_page_config(
    page_title="GEEK Repair Notes Translator",
    page_icon="🛠️",
    layout="centered"
)

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top right, rgba(43, 137, 255, 0.14), transparent 34%),
                linear-gradient(180deg, #07111f 0%, #0b1626 100%);
        }
        .block-container {
            max-width: 860px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }
        .geek-badge {
            display: inline-block;
            padding: 0.38rem 0.75rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(96, 165, 250, 0.45);
            border-radius: 999px;
            background: rgba(37, 99, 235, 0.14);
            color: #93c5fd;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }
        h1 {
            color: #f8fafc;
            font-size: clamp(2.25rem, 6vw, 3.7rem) !important;
            line-height: 1.04 !important;
            letter-spacing: -0.04em;
            margin-bottom: 0.65rem !important;
        }
        .geek-intro {
            color: #cbd5e1;
            font-size: 1.08rem;
            line-height: 1.7;
            margin-bottom: 1.7rem;
        }
        .privacy-note {
            padding: 0.9rem 1rem;
            margin: 0.5rem 0 1.35rem;
            border-left: 4px solid #38bdf8;
            border-radius: 0 10px 10px 0;
            background: rgba(14, 165, 233, 0.09);
            color: #dbeafe;
            font-size: 0.92rem;
        }
        div[data-baseweb="textarea"] textarea,
        div[data-baseweb="select"] > div {
            border-radius: 12px !important;
        }
        .stButton > button {
            width: 100%;
            min-height: 3.15rem;
            border: 0;
            border-radius: 12px;
            background: linear-gradient(90deg, #2563eb, #0ea5e9);
            color: white;
            font-size: 1rem;
            font-weight: 800;
            box-shadow: 0 10px 28px rgba(14, 165, 233, 0.22);
        }
        .stButton > button:hover {
            border: 0;
            color: white;
            transform: translateY(-1px);
            box-shadow: 0 13px 32px rgba(14, 165, 233, 0.3);
        }
        .stDownloadButton > button {
            width: 100%;
            border-radius: 10px;
            font-weight: 700;
        }
        div[data-testid="stExpander"] {
            border-radius: 12px;
            border-color: rgba(148, 163, 184, 0.28);
        }
        .geek-footer {
            margin-top: 2.5rem;
            text-align: center;
            color: #64748b;
            font-size: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="geek-badge">She\'s a Geek AI Project</div>', unsafe_allow_html=True)
st.title("GEEK Repair Notes Translator")
st.markdown(
    '<div class="geek-intro">Turn rough technician notes into clear, accurate documentation without changing the facts.</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="privacy-note">🔒 Portfolio demonstration: Use fictional repair information only. Do not enter customer names, contact details, serial numbers, passwords, or other private data.</div>',
    unsafe_allow_html=True
)

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

if st.button("Generate Documentation", type="primary"):
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

            with st.spinner("Translating repair notes..."):
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt
                )

            plain_text_result = (
                response.text
                .replace("**", "")
                .replace("*", "")
                .replace(chr(96), "")
            )

            st.subheader("Generated Documentation")
            st.markdown(response.text)

            with st.expander("Copy Result"):
                st.code(
                    plain_text_result,
                    language=None,
                    wrap_lines=True
                )

            st.download_button(
                label="Download Result",
                data=plain_text_result,
                file_name="geek_repair_notes.txt",
                mime="text/plain"
            )

        except Exception as error:
            st.error(f"Something went wrong: {error}")

st.markdown(
    '<div class="geek-footer">Built by She\'s a Geek • AI-assisted repair documentation prototype</div>',
    unsafe_allow_html=True
)
