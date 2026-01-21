import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt
import hashlib

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# ---------------- SESSION STATE INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- AUTH DATA ----------------
USERS = {
    "jasmeeta": "expense123",
    "admin": "admin123"
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

HASHED_USERS = {u: hash_password(p) for u, p in USERS.items()}

# ---------------- LOGIN FUNCTION ----------------
def login():
    st.subheader("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in HASHED_USERS and hash_password(password) == HASHED_USERS[username]:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success("Login successful 🎉")
            st.rerun()
        else:
            st.error("Invalid username or password")

# ---------------- LOGIN CHECK ----------------
if not st.session_state.logged_in:
    login()
    st.stop()

# ---------------- FILE SETUP ----------------
DATA_DIR = "data"
FILE_NAME = os.path.join(DATA_DIR, f"expenses_{st.session_state.user}.csv")

if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=["date", "category", "description", "amount"])
    df.to_csv(FILE_NAME, index=False)

# ---------------- SIDEBAR ----------------
st.sidebar.success(f"👋 Logged in as {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# ---------------- MAIN UI ----------------
st.title("💰 Personal Expense Tracker")
st.caption("Built with ❤️ using Python, Pandas & Streamlit by Jasmeeta")
st.markdown("---")

# ---------------- ADD EXPENSE ----------------
st.subheader("➕ Add New Expense")

with st.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Shopping", "Bills", "Entertainment", "Other"]
    )
    description = st.text_input("Description")
    amount = st.number_input("Amount (₹)", min_value=0.0, step=0.01)

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

# ---------------- VIEW EXPENSES ----------------
st.subheader("📄 All Expenses")
df = pd.read_csv(FILE_NAME)

if df.empty:
    st.info("No expenses recorded yet.")
else:
    st.dataframe(df, use_container_width=True)

    # ---------------- ANALYTICS ----------------
    st.subheader("📊 Expense Analytics")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("💸 Total Spending", f"₹ {df['amount'].sum():.2f}")
    with col2:
        st.metric("📦 Total Transactions", len(df))

    st.subheader("📌 Category-wise Spending")
    category_summary = df.groupby("category")["amount"].sum()

    fig, ax = plt.subplots()
    category_summary.plot(kind="bar", ax=ax)
    ax.set_ylabel("Amount (₹)")
    ax.set_xlabel("Category")
    ax.set_title("Category-wise Spending")
    plt.xticks(rotation=45)

    st.pyplot(fig)
