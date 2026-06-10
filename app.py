import streamlit as st
import tempfile
import os
import py3Dmol
from stmol import showmol

from RNA2DNA import convert_rna_to_dna


# ----------------------------
# PDB Visualization Function
# ----------------------------

def visualize_pdb(pdb_file, label, style_color):

    with open(pdb_file, "r") as f:
        pdb_data = f.read()

    view = py3Dmol.view(
        width=500,
        height=500
    )

    view.addModel(
        pdb_data,
        "pdb"
    )

    view.setStyle(
        {
            "stick": {
                "color": style_color
            }
        }
    )

    view.zoomTo()

    st.subheader(label)

    showmol(
        view,
        height=500,
        width=500
    )


# ----------------------------
# Streamlit Page Configuration
# ----------------------------

st.set_page_config(
    page_title="RNA2DNA Dashboard",
    page_icon="🧬",
    layout="wide"
)


# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.header("About RNA2DNA")

    st.markdown(
        """
RNA2DNA is a structural bioinformatics tool designed to convert **single-stranded RNA (ssRNA)** structures into **single-stranded DNA (ssDNA)** structures.

### Features

- RNA PDB upload
- Automated RNA → DNA conversion
- Interactive 3D visualization
- Download converted DNA structures

### Technologies Used

- Python
- Streamlit
- BioPandas
- py3Dmol
- Structural Bioinformatics
"""
    )


# ----------------------------
# Main Page
# ----------------------------

st.title("🧬 RNA2DNA Dashboard")

st.markdown(
    """
Convert **single-stranded RNA (ssRNA)** 3D structures into **single-stranded DNA (ssDNA)** structures.

Upload an RNA structure in **PDB format** to begin.
"""
)


# ----------------------------
# File Upload
# ----------------------------

uploaded_file = st.file_uploader(
    "Upload RNA PDB File",
    type=["pdb"]
)


# ----------------------------
# File Information
# ----------------------------

if uploaded_file:

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "File Size",
            f"{uploaded_file.size / 1024:.2f} KB"
        )

    with col2:
        st.metric(
            "File Type",
            "PDB"
        )


# ----------------------------
# Conversion
# ----------------------------

if uploaded_file:

    if st.button("Convert RNA → DNA"):

        with st.spinner(
            "Converting RNA structure..."
        ):

            with tempfile.TemporaryDirectory() as temp_dir:

                input_file = os.path.join(
                    temp_dir,
                    uploaded_file.name
                )

                with open(
                    input_file,
                    "wb"
                ) as f:

                    f.write(
                        uploaded_file.getbuffer()
                    )

                output_file = os.path.join(
                    temp_dir,
                    "DNA.pdb"
                )

                try:

                    convert_rna_to_dna(
                        input_file,
                        output_file
                    )

                    st.success(
                        "Conversion successful!"
                    )

                    st.balloons()

                    st.header(
                        "Structure Comparison"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        visualize_pdb(
                            input_file,
                            "Original RNA Structure",
                            "blue"
                        )

                    with col2:

                        visualize_pdb(
                            output_file,
                            "Converted DNA Structure",
                            "green"
                        )

                    st.divider()

                    with open(
                        output_file,
                        "rb"
                    ) as f:

                        st.download_button(
                            label="Download DNA Structure",
                            data=f,
                            file_name="DNA.pdb",
                            mime="chemical/x-pdb"
                        )

                except Exception as e:

                    st.error(
                        f"Conversion failed:\n{e}"
                    )