import streamlit as st
import pandas as pd
from pdf_parser import parse_invoice
from calculator import calculate_invoice

st.set_page_config("Invoice Auto Calculator", layout="wide")
st.title("🧾 Invoice Auto Calculator (PDF → Auto Scan)")

st.markdown("""
### Logic
- Discount = **16%**
- Discount sirf **Paid Qty**
- Free qty sirf **Effective Rate** me include
""")

uploaded_pdf = st.file_uploader(
    "Upload Invoice PDF (Crystal Reports format)",
    type="pdf"
)

if uploaded_pdf:
    with st.spinner("Scanning PDF..."):
        df = parse_invoice(uploaded_pdf)

    st.subheader("📥 Extracted Data (Auto)")
    st.data_editor(df, use_container_width=True, num_rows="dynamic")

    if st.button("Calculate Invoice"):
        result, gross, discount, net = calculate_invoice(df)

        st.subheader("📊 Final Calculated Invoice")
        st.dataframe(result, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Gross Amount", f"{gross:,.2f}")
        c2.metric("Discount (16%)", f"{discount:,.2f}")
        c3.metric("Net Amount", f"{net:,.2f}")

        st.success("✅ PDF successfully scanned & calculated")
