import streamlit as st
from prediction_helper import predict

# Page config
st.set_page_config(
    page_title="HealthGuard | Cost Predictor",
    page_icon="🛡️",
    layout="centered" # Focused layout feels more professional for forms
)

# Custom CSS for a modern "Card" look
st.markdown("""
    <style>
        /* Main background */
        .stApp {
            background: linear-gradient(to bottom, #ffffff);
        }
        
        /* Highlighting sections */
        div[data-testid="stVerticalBlock"] > div:has(div.stHeader) {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }

        /* Button styling */
        .stButton>button {
            width: 100%;
            border-radius: 25px;
            height: 3em;
            background-color: #007BFF;
            color: white;
            font-weight: bold;
            border: none;
            transition: 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #0056b3;
            border: none;
            color: white;
        }

        /* Metric styling */
        [data-testid="stMetricValue"] {
            font-size: 30px;
            color: #1E88E5;
        }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("🛡️ HealthGuard AI")
st.caption("Advanced Machine Learning for Accurate Premium Estimation")
st.info("Please provide your details below. Our AI model will calculate your estimated annual premium.")

# --- FORM DATA ---
categorical_options = {
    'Gender': ['Male', 'Female'],
    'Marital Status': ['Unmarried', 'Married'],
    'BMI Category': ['Normal', 'Obesity', 'Overweight', 'Underweight'],
    'Smoking Status': ['No Smoking', 'Regular', 'Occasional'],
    'Employment Status': ['Salaried', 'Self-Employed', 'Freelancer'],
    'Region': ['Northwest', 'Southeast', 'Northeast', 'Southwest'],
    'Medical History': [
        'No Disease', 'Diabetes', 'High blood pressure', 'Thyroid', 
        'Heart disease', 'Multi-condition'
    ],
    'Insurance Plan': ['Bronze', 'Silver', 'Gold']
}

# --- INPUT SECTION ---
# Using tabs for a cleaner, less overwhelming interface
tab1, tab2 = st.tabs(["👤 Personal Profile", "🏥 Health & Lifestyle"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input('Age', min_value=18, max_value=100, value=25)
        gender = st.selectbox('Gender', categorical_options['Gender'])
        marital_status = st.selectbox('Marital Status', categorical_options['Marital Status'])
    with col2:
        income_lakhs = st.number_input('Annual Income (in Lakhs)', min_value=0, max_value=200, value=5)
        employment_status = st.selectbox('Employment Status', categorical_options['Employment Status'])
        number_of_dependants = st.number_input('Number of Dependants', min_value=0, max_value=10, value=0)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        bmi_category = st.selectbox('BMI Category', categorical_options['BMI Category'])
        smoking_status = st.selectbox('Smoking Status', categorical_options['Smoking Status'])
        genetical_risk = st.slider('Genetical Risk Score', 0, 5, 1)
    with col2:
        medical_history = st.selectbox('Medical History', categorical_options['Medical History'])
        region = st.selectbox('Region', categorical_options['Region'])
        insurance_plan = st.selectbox('Desired Plan Type', categorical_options['Insurance Plan'])

st.divider()

# --- PREDICTION LOGIC ---
input_dict = {
    'Age': age, 'Number of Dependants': number_of_dependants,
    'Income in Lakhs': income_lakhs, 'Genetical Risk': genetical_risk,
    'Insurance Plan': insurance_plan, 'Employment Status': employment_status,
    'Gender': gender, 'Marital Status': marital_status,
    'BMI Category': bmi_category, 'Smoking Status': smoking_status,
    'Region': region, 'Medical History': medical_history
}

if st.button('Calculate Premium Cost'):
    with st.spinner('Analyzing risk factors...'):
        prediction = predict(input_dict)
        
        # Displaying the result in a modern way
        st.balloons()
        st.subheader("Your Estimated Annual Premium")
        
        c1, c2 = st.columns([1, 1])
        c1.metric(label="Total Cost", value=f"₹{prediction:,.2f}")
        c2.write(f"**Plan Tier:** {insurance_plan}")
        c2.write(f"**Risk Profile:** {'High' if genetical_risk > 3 or smoking_status != 'No Smoking' else 'Standard'}")
        
        st.caption("Note: This is an AI-generated estimate. Actual prices may vary based on policy terms.")

# Footer
st.markdown("---")
st.markdown("<center><small>© 2024 Abhinav Kumar | Secure Prediction Portal</small></center>", unsafe_allow_html=True)