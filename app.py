import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# Initialize CSV
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["date", "category", "description", "amount"])
    df.to_csv(FILE_NAME, index=False)

st.set_page_config(page_title="Expense Tracker", layout="centered")

st.title("💰 Personal Expense Tracker")

# ---- Add Expense Form ----
st.subheader("➕ Add New Expense")

with st.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
    )
    description = st.text_input("Description")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)

    submit = st.form_submit_button("Add Expense")

    if submit:
        new_expense = pd.DataFrame([{
            "date": date.strftime("%Y-%m-%d"),
            "category": category,
            "description": description,
            "amount": amount
        }])

        df = pd.read_csv(FILE_NAME)
        df = pd.concat([df, new_expense], ignore_index=True)
        df.to_csv(FILE_NAME, index=False)

        st.success("Expense added successfully 🎉")

# ---- View Expenses ----
st.subheader("📄 All Expenses")
df = pd.read_csv(FILE_NAME)

if df.empty:
    st.info("No expenses recorded yet.")
else:
    st.dataframe(df)

    # ---- Analytics ----
    st.subheader("📊 Expense Analytics")

    total = df["amount"].sum()
    st.metric("Total Spending", f"₹ {total:.2f}")

    # Category-wise spending
    category_summary = df.groupby("category")["amount"].sum()

    st.subheader("📌 Category-wise Spending")
    fig, ax = plt.subplots()
    category_summary.plot(kind="bar", ax=ax)
    ax.set_ylabel("Amount")
    st.pyplot(fig)
