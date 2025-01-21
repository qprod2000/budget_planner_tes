# app/utils/supabase_client.py
import streamlit as st
from supabase import create_client

@st.cache_resource
def init_connection():
    """Initialize connection to Supabase"""
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )

def get_data(table_name, query=None):
    """Fetch data from Supabase table"""
    supabase = init_connection()
    if query:
        return supabase.table(table_name).select(query).execute()
    return supabase.table(table_name).select("*").execute()

def insert_data(table_name, data):
    """Insert data into Supabase table"""
    supabase = init_connection()
    return supabase.table(table_name).insert(data).execute()

def update_data(table_name, id, data):
    """Update data in Supabase table"""
    supabase = init_connection()
    return supabase.table(table_name).update(data).eq('id', id).execute()

def delete_data(table_name, id):
    """Delete data from Supabase table"""
    supabase = init_connection()
    return supabase.table(table_name).delete().eq('id', id).execute()