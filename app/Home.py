# app/Home.py
import streamlit as st
from utils.supabase_client import init_connection

# Page configuration
st.set_page_config(
    page_title="Budget Planner",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Supabase connection
supabase = init_connection()

# Main page content
st.title("💰 Budget Planner")
st.write("Welcome to your personal budget planner!")

# Check database connection
try:
    response = supabase.table('transactions').select("count", count='exact').execute()
    st.success("✅ Connected to database")
except Exception as e:
    st.error(f"❌ Database connection error: {str(e)}")

# Display app information
st.markdown("""
### Features:
- 📊 Track your income and expenses
- 💰 Manage transactions
- 📈 View financial analytics
- ⚙️ Customize settings

Use the sidebar to navigate between different sections of the app.
""")