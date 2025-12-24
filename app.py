import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Invoice Discount Calculator",
    layout="wide"
)

st.title("🧾 Invoice Discount Calculator")

st.markdown("""
### Rules
- **Discount:** 16%
- Discount applies **only on Paid Qty**
- **Effective Rate = (Paid Qty × Discounted Rate) / Total Qty**
""")

# Editable input table
df = st.data_editor(
    pd.DataFrame({
        "Item": [""],
        "Rate": [0.0],
        "Paid Qty": [0],
        "Free Qty": [0]
    }),
    num_rows="dynamic",
    use_container_width=True
)

if st.button("Calculate"):
    data = df.copy()

    data["Total Qty"] = data["Paid Qty"] + data["Free Qty"]
    data["Discounted Rate"] = data["Rate"] * 0.84
    data["Paid Amount"] = data["Paid Qty"] * data["Discounted Rate"]

    data["Effective Rate"] = data.apply(
        lambda r: round(
            r["Paid Amount"] / r["Total Qty"]
            if r["Total Qty"] > 0 else 0,
            2
        ),
        axis=1
    )

    gross = (data["Rate"] * data["Paid Qty"]).sum()
    discount = gross * 0.16
    net = data["Paid Amount"].sum()

    st.subheader("📊 Invoice Result")
    st.dataframe(data, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Gross Amount", f"{gross:,.2f}")
    col2.metric("Discount (16%)", f"{discount:,.2f}")
    col3.metric("Net Amount", f"{net:,.2f}")

    st.success("Invoice calculated successfully ✅")
