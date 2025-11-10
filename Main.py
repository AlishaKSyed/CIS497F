# CIS497F - Group #()
# Author: Alisha Syed 

# Streamlit Banking Dashboard with NVDA Line Chart

import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Skyline Banking", page_icon="💻", layout="wide")

# --- USER CREDENTIALS ---
User_Credentials = {
    "AlishaSyed": "Abcd123!",
    "Kripal": "Efgh456!",
    "Shayne": "Ijkl789!"
}

# --- SESSION STATE ---
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""


# --- LOGIN PAGE ---
def login_page():
    st.title("Skyline Banking ☁️")
    st.text("Where everyday banking is made easier.")

    st.subheader("🔒 Login to access daily banking tools and features!")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

    if login_button:
        if username in User_Credentials and User_Credentials[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("Login successful! Redirecting...")
            st.rerun()
        else:
            st.error("Invalid username or password ❌")


# --- TRANSACTIONS SECTION ---
def init_transactions_simple(username):
    key = f"tx_simple_{username}"
    if key not in st.session_state:
        st.session_state[key] = [
            {"Date": "Today", "Description": "Salary Deposit", "Amount": "+$3,000.00"},
            {"Date": "1 day ago", "Description": "Grocery Store", "Amount": "-$42.50"},
            {"Date": "2 days ago", "Description": "Electric Bill", "Amount": "-$80.00"},
            {"Date": "4 days ago", "Description": "Online Purchase", "Amount": "-$150.00"},
            {"Date": "7 days ago", "Description": "Transfer to Savings", "Amount": "-$200.00"},
        ]


def transactions_simple_section(username):
    init_transactions_simple(username)
    st.subheader("💳 Recent Transactions")
    rows = st.session_state[f"tx_simple_{username}"]
    st.table(rows)


# --- NVDA LINE CHART ---
def nvda_line_chart():
    st.subheader("📈 NVDA Stock Trend")

    try:
        data = yf.download("NVDA", period="3mo", interval="1d", progress=False)

        if data is not None and not data.empty:
            st.line_chart(data["Close"])
        else:
            st.warning("⚠️ Unable to fetch NVDA stock data. Displaying sample data instead.")
            sample_data = pd.DataFrame({
                "Close": [470, 475, 480, 485, 490, 495, 500, 505, 510, 515]
            })
            st.line_chart(sample_data)
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")


# --- DASHBOARD ---
def dashboard():
    st.title(f"🏠 Welcome Back, {st.session_state['username']}!")
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.rerun()

    st.subheader("💼 Account Overview")
    Checking_Account, Savings_Account, Credit_Card_Balance = st.columns(3)
    with Checking_Account:
        st.metric("Checking Account", "$3,420.50")
    with Savings_Account:
        st.metric("Savings Account", "$10,432.00")
    with Credit_Card_Balance:
        st.metric("Credit Card Balance", "-$650.40")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        transactions_simple_section(st.session_state["username"])
    with col2:
        nvda_line_chart()

def transactions_simple_section(username):
    init_transactions_simple(username)
    rows = st.session_state[f"tx_simple_{username}"]
    
    st.subheader("💳 Recent Transactions")
    st.table(rows)

    # --- Calculate total spending ---
    monthly_avg = 500  # Example average spending
    total_spent = sum(float(tx["Amount"].replace("$","").replace(",","")) 
                      for tx in rows if tx["Amount"].startswith("-"))
    
    diff = total_spent - monthly_avg
    st.error(f":warning: You've spent ${abs(diff):.2f} over your monthly average.")


# --- PAGE LOGIC ---
if not st.session_state["logged_in"]:
    login_page()
else:
    dashboard()
