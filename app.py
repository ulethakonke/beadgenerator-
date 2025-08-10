import streamlit as st
from pathlib import Path
import subprocess, tempfile, time, os
st.set_page_config(page_title="SoulGenesis v2 — Fixed", layout="wide")
st.markdown("<h1 style='text-align:center;color:#7C3AED;'>SoulGenesis v2 — Fixed & Polished</h1>", unsafe_allow_html=True)
st.write("Lossless binary .genesis compressor. Upload images, download .genesis; upload .genesis, reconstruct image.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Compress Image")
    uploaded = st.file_uploader("Upload image (PNG/JPG)", type=['png','jpg','jpeg'], key="compress_uploader")
    if uploaded:
        tmp_in = Path(tempfile.gettempdir()) / f"sg_in_{int(time.time())}.png"
        tmp_out = Path("tests") / (uploaded.name.rsplit('.',1)[0] + f"_{int(time.time())}.genesis")
        tmp_in.write_bytes(uploaded.read())
        subprocess.run(["python3","compress_v2.py", str(tmp_in), str(tmp_out)])
        st.success("Compressed!")
        with open(tmp_out, "rb") as f:
            st.download_button("Download .genesis", f, file_name=tmp_out.name)

with col2:
    st.subheader("Decompress .genesis")
    uploaded_g = st.file_uploader("Upload .genesis file", type=['genesis'], key="decompress_uploader")
    if uploaded_g:
        tmp_gen = Path(tempfile.gettempdir()) / f"sg_in_{int(time.time())}.genesis"
        tmp_recon = Path("tests") / (uploaded_g.name.rsplit('.',1)[0] + f"_{int(time.time())}.recon.png")
        tmp_gen.write_bytes(uploaded_g.read())
        subprocess.run(["python3","decompress_v2.py", str(tmp_gen), str(tmp_recon)])
        st.success("Reconstructed!")
        st.image(str(tmp_recon), caption="Reconstructed Image", use_column_width=True)
        with open(tmp_recon,"rb") as f:
            st.download_button("Download Reconstructed Image", f, file_name=tmp_recon.name)

st.write("---")
st.write("Notes: This is a prototype. Keep originals backed up. For photos with many unique colors, .genesis file may still be large.")