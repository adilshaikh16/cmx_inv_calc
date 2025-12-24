def calculate_invoice(df, discount=0.16):
    df["Discounted Rate"] = df["Rate"] * (1 - discount)
    df["Paid Amount"] = df["Paid Qty"] * df["Discounted Rate"]
    df["Total Qty"] = df["Paid Qty"] + df["Free Qty"]

    df["Effective Rate"] = df.apply(
        lambda r: round(
            r["Paid Amount"] / r["Total Qty"] if r["Total Qty"] > 0 else 0, 2
        ),
        axis=1
    )

    gross = (df["Rate"] * df["Paid Qty"]).sum()
    discount_amt = gross * discount
    net = df["Paid Amount"].sum()

    return df, gross, discount_amt, net
