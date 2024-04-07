import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px


# Display Title and Description
st.title("CCS Quick Attendance Portal")
st.markdown("enter your sins below")

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
        years_in_business = st.slider("Year Level (if extended, slide to year 5)", 1, 5, 3)
        onboarding_date = st.date_input(label="Current Date")

        st.markdown("**required*")
        submit_button = st.form_submit_button(label="Submit Details")

        if submit_button:
            if not company_name or not business_type:
                st.warning("Ensure all mandatory fields are filled.")
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
     # Count the occurrences of each "Year" in the "Year" column
    year_counts = existing_data["Year"].value_counts().reset_index()
    year_counts.columns = ['Year', 'Count']  # Renaming columns for clarity
    
    # Create a bar chart using Plotly
    fig = px.bar(year_counts, x='Year', y='Count', title='Attendance by Year')
    st.plotly_chart(fig)  # Display the figure in the Streamlit app

    
     # For Pie Chart of Majors
    major_counts = existing_data["Major"].value_counts().reset_index()
    major_counts.columns = ['Major', 'Count']  # Renaming columns for clarity
    
    # Create a pie chart using Plotly
    pie_fig = px.pie(major_counts, values='Count', names='Major', title='Distribution of Majors')
    st.plotly_chart(pie_fig)  # Display the pie chart in the Streamlit app
