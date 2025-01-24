import streamlit as st
import plotly.express as px
import pandas as pd
from openai import OpenAI

# OpenAI API Key (set this in Streamlit's Secrets Manager for security)
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Sample data creation
data = {
    'Customer ID': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007', 'C008', 'C009'],
    'Call Date': ['2025-01-01', '2025-01-02', '2025-01-03', '2025-01-04', '2025-01-05', '2025-01-06', '2025-01-07', '2025-01-08', '2025-01-09'],
    'Sentiment Score': [0.5, 0.55, 0.6, 0.58, 0.65, 0.6, 0.55, 0.5, 0.48],
    'Churn Likelihood': [0.2, 0.4, 0.3, 0.6, 0.1, 0.3, 0.5, 0.7, 0.9],
    'Follow-Up Required': ['Yes', 'No', 'Yes', 'Yes', 'No', 'No', 'Yes', 'No', 'Yes'],
    'Call Duration Minutes': [8, 10, 12, 9, 11, 13, 10, 9, 8],
    'Customer Wait Time Minutes': [3, 5, 4, 6, 3, 5, 4, 6, 3],
    'Issue Type': ['Ride Cancellation', 'Driver Complaint', 'App Bug', 'Payment Issue', 'General Inquiry', 'Ride Cancellation', 'Driver Complaint', 'App Bug', 'Payment Issue']
}
df = pd.DataFrame(data)

# Simulated data for the new tab (Customer Service Issue Types)
issue_data = {
    'Issue Type': ['Ride Cancellation', 'Driver Complaint', 'App Bug', 'Payment Issue', 'General Inquiry'],
    'Count': [45, 30, 15, 10, 20]
}
issue_df = pd.DataFrame(issue_data)

call_duration_data = {
    'Issue Type': ['Ride Cancellation', 'Driver Complaint', 'App Bug', 'Payment Issue', 'General Inquiry'],
    'Average Call Duration': [12, 15, 10, 14, 8]
}
call_duration_df = pd.DataFrame(call_duration_data)

# Define the function to generate AI insights
def explain_with_ai(data, title):
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = f"Analyze the following data for the chart titled '{title}':\n{data}\nProvide a summary, insights, prediction and recommended actions."
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant analyzing data for insights, predictions and recommendations for an e-hailing company named TADA."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4",
        )
        explanation = response.choices[0].message.content
        return explanation
    except Exception as e:
        return f"An error occurred while generating insights: {e}"

# Sidebar for navigation
st.sidebar.title("Customer Insights Dashboard")
tab = st.sidebar.radio("Select Tab", ["Main", "Sentiment Score", "Churn Prediction", "Follow-Up Analysis", "Call Metrics", "Issue Types Breakdown", "Call Duration by Issue"])

# Custom color palettes
custom_colors = px.colors.qualitative.Set3

# Display corresponding figures based on selected tab
if tab == "Main":
    st.subheader("Main Dashboard Overview")
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            px.line(
                df,
                x='Call Date',
                y='Sentiment Score',
                title='Average Sentiment Score by Call Date',
                color_discrete_sequence=custom_colors
            ),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            px.bar(
                df,
                x='Customer ID',
                y='Churn Likelihood',
                title='Churn Prediction by Customer ID',
                color='Customer ID',
                color_discrete_sequence=custom_colors
            ),
            use_container_width=True
        )
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            px.pie(
                df,
                names='Follow-Up Required',
                title='Follow-Up Analysis by Issue Types',
                color_discrete_sequence=custom_colors,
                hole=0.4
            ),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            px.bar(
                df,
                x='Call Date',
                y=['Call Duration Minutes', 'Customer Wait Time Minutes'],
                title='Call Metrics',
                barmode='group',
                color_discrete_sequence=custom_colors
            ),
            use_container_width=True
        )
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            px.pie(
                issue_df,
                values='Count',
                names='Issue Type',
                title='Customer Service Issue Types Breakdown (TADA)',
                color_discrete_sequence=custom_colors
            ),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            px.bar(
                call_duration_df,
                x='Issue Type',
                y='Average Call Duration',
                title='Average Call Duration by Issue Type',
                color='Issue Type',
                color_discrete_sequence=custom_colors
            ),
            use_container_width=True
        )

elif tab == "Sentiment Score":
    st.plotly_chart(
        px.line(
            df,
            x='Call Date',
            y='Sentiment Score',
            title='Average Sentiment Score by Call Date',
            color_discrete_sequence=custom_colors
        )
    )

elif tab == "Churn Prediction":
    st.plotly_chart(
        px.bar(
            df,
            x='Customer ID',
            y='Churn Likelihood',
            title='Churn Prediction by Customer ID',
            color='Customer ID',
            color_discrete_sequence=custom_colors
        )
    )

elif tab == "Follow-Up Analysis":
    st.plotly_chart(
        px.pie(
            df,
            names='Follow-Up Required',
            title='Follow-Up Analysis by Issue Types',
            color_discrete_sequence=custom_colors,
            hole=0.4
        )
    )

elif tab == "Call Metrics":
    st.plotly_chart(
        px.bar(
            df,
            x='Call Date',
            y=['Call Duration Minutes', 'Customer Wait Time Minutes'],
            title='Call Metrics',
            barmode='group',
            color_discrete_sequence=custom_colors
        )
    )

elif tab == "Issue Types Breakdown":
    st.plotly_chart(
        px.pie(
            issue_df,
            values='Count',
            names='Issue Type',
            title='Customer Service Issue Types Breakdown (TADA)',
            color_discrete_sequence=custom_colors
        )
    )

elif tab == "Call Duration by Issue":
    st.plotly_chart(
        px.bar(
            call_duration_df,
            x='Issue Type',
            y='Average Call Duration',
            title='Average Call Duration by Issue Type',
            color='Issue Type',
            color_discrete_sequence=custom_colors
        )
    )

# AI Insights Button
if st.button("Ask AI"):
    combined_data = {
        "Sentiment Data": df.to_dict(),
        "Issue Type Data": issue_df.to_dict(),
        "Call Duration Data": call_duration_df.to_dict()
    }
    st.subheader("AI Insights")
    explanation = explain_with_ai(combined_data, f"{tab} Dashboard")
    st.write(explanation)
