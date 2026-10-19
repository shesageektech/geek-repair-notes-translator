import streamlit as st

st.set_page_config(
    page_title="GEEK Repair Notes Translator",
    page_icon="🛠️"
)

st.title("GEEK Repair Notes Translator")
st.write(
    "Turn rough technician notes into clear, accurate documentation."
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

if st.button("Generate"):
    if technician_notes.strip():
        st.subheader("Results")

        st.write(
            f"This is a temporary sample response for: {output_mode}"
        )

        st.info(
            "Temporary version: Gemini has not been connected yet."
        )
    else:
        st.warning("Please paste technician notes before generating an output.")
