# app/pages/2_💰_Transactions.py
import streamlit as st
import pandas as pd
from utils.supabase_client import get_data, insert_data, update_data, delete_data

st.title("💰 Transactions")

# Transaction form
with st.form("transaction_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        date = st.date_input("Date")
        code = st.text_input("Code")
        
    with col2:
        description = st.text_input("Description")
        category = st.selectbox("Category", ["Income", "Expense"])
        
    with col3:
        amount_type = st.radio("Type", ["Credit", "Debit"])
        amount = st.number_input("Amount", min_value=0.0, format="%f")
        
    remark = st.text_area("Remark")
    submitted = st.form_submit_button("Save Transaction")
    
    if submitted:
        data = {
            "date": date.isoformat(),
            "code": code,
            "description": description,
            "debit": amount if amount_type == "Debit" else 0,
            "credit": amount if amount_type == "Credit" else 0,
            "remark": remark,
            "category": category
        }
        
        try:
            insert_data("transactions", data)
            st.success("Transaction saved successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"Error saving transaction: {str(e)}")

# Display transactions
try:
    response = get_data("transactions")
    if response.data:
        df = pd.DataFrame(response.data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date', ascending=False)
        
        # Add edit and delete buttons
        def handle_delete(id):
            try:
                delete_data("transactions", id)
                st.success("Transaction deleted successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error deleting transaction: {str(e)}")
        
        for index, row in df.iterrows():
            with st.expander(f"{row['date'].strftime('%Y-%m-%d')} - {row['description']}"):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"Amount: {'Credit' if row['credit'] > 0 else 'Debit'} {max(row['credit'], row['debit']):,.2f}")
                    st.write(f"Category: {row['category']}")
                    if row['remark']:
                        st.write(f"Remark: {row['remark']}")
                with col3:
                    if st.button("Delete", key=f"delete_{row['id']}"):
                        handle_delete(row['id'])
                        
except Exception as e:
    st.error(f"Error loading transactions: {str(e)}")