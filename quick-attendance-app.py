import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Display Title and Description
st.title("Vendor Management Portal")
st.markdown("Enter the details of the new vendor below.")

# Establishing a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read(worksheet="Vendors", usecols=list(range(6)), ttl=3)
existing_data = existing_data.dropna(how="all")

# List of Business Types and Products
BUSINESS_TYPES = [
    "BSIS",
    "BSCS",
    "BSIT",
    "BSCA",
]
PRODUCTS = [
    "IT",
    "ESET",
    "CSC",
]

action = st.selectbox(
    "Choose an Action",
    [
        "Magpa Attendance",
        "Mo lantaw sa naka Attendance"
    ],
)

# Check the action selected
if action == "Magpa Attendance":
    with st.form(key="vendor_form"):
        student_name = st.text_input(label="Name*")
        company_name = st.text_input(label="ID Number*")
        business_type = st.selectbox("Major*", options=BUSINESS_TYPES, index=None)
        products = st.selectbox("Department (note: IT: for BSIS and BSIT, ESET: for BSCA, CSC: for BSCS)", options=PRODUCTS)
        years_in_business = st.slider("Years", 1, 15, 5)
        onboarding_date = st.date_input(label="Current Date")

        st.markdown("**required*")
        submit_button = st.form_submit_button(label="Submit Details")

        if submit_button:
            if not company_name or not business_type:
                st.warning("Ensure all mandatory fields are filled.")
            elif existing_data["ID"].astype(str).str.contains(company_name).any():
                st.warning("A student with this ID already exists.")
            else:
                vendor_data = pd.DataFrame([
                    {
                        "Name": student_name,
                        "ID": company_name,
                        "Major": business_type,
                        "Department": products,
                        "Year": years_in_business,
                        "Date": onboarding_date.strftime("%Y-%m-%d"),
                
                    }
                ])
                updated_df = pd.concat([existing_data, vendor_data], ignore_index=True)
                conn.update(worksheet="Vendors", data=updated_df)
                st.success("Attendance Submitted!")

elif action == "Mo lantaw sa naka Attendance":
    st.dataframe(existing_data)
