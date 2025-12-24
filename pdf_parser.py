import pdfplumber
import pandas as pd
import re

def parse_invoice(pdf_file):
    rows = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue

            for row in table:
                try:
                    text = " ".join(row)
                    qty = int(re.search(r"\b\d+\b", text).group())
                    rate = float(re.search(r"\d+\.\d{2}", text).group())

                    description = row[0].strip()

                    if rate > 0:
                        paid_qty = qty
                        free_qty = 0
                    else:
                        paid_qty = 0
                        free_qty = qty

                    rows.append([description, rate, paid_qty, free_qty])

                except:
                    continue

    df = pd.DataFrame(
        rows,
        columns=["Item", "Rate", "Paid Qty", "Free Qty"]
    )

    # Group same items (paid + free merge)
    df = df.groupby(["Item", "Rate"], as_index=False).sum()

    return df
