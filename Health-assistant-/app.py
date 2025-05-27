import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json
import os
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyAdl8m1ff3j1xMQtWjiLGkgNKfXJ5X6JF4")
model = genai.GenerativeModel('gemini-1.5-flash')

# Initialize session state
if 'health_log' not in st.session_state:
    st.session_state.health_log = []
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

# Constants
SERIOUS_SYMPTOMS = [
    "high fever", "chest pain", "difficulty breathing", "severe pain",
    "unconsciousness", "severe bleeding", "stroke", "heart attack"
]

SEASONAL_DISEASES = {
    "Flu": {
        "symptoms": "Fever, cough, sore throat, body aches, fatigue",
        "first_aid": "Rest, stay hydrated, over-the-counter fever reducers",
        "precautions": "Annual flu shot, frequent hand washing, avoid close contact with sick people"
    },
    "Dengue": {
        "symptoms": "High fever, severe headache, joint pain, rash",
        "first_aid": "Rest, stay hydrated, avoid aspirin",
        "precautions": "Use mosquito repellent, eliminate standing water, wear protective clothing"
    },
    "Common Cold": {
        "symptoms": "Runny nose, sore throat, cough, congestion",
        "first_aid": "Rest, stay hydrated, over-the-counter cold medicine",
        "precautions": "Wash hands frequently, avoid close contact with sick people"
    },
    "Allergic Rhinitis": {
        "symptoms": "Sneezing, runny nose, itchy eyes, nasal congestion",
        "first_aid": "Antihistamines, nasal sprays, eye drops",
        "precautions": "Avoid allergens, use air purifiers, keep windows closed during high pollen times"
    },
    "Food Poisoning": {
        "symptoms": "Nausea, vomiting, diarrhea, abdominal pain",
        "first_aid": "Stay hydrated, rest, avoid solid foods initially",
        "precautions": "Practice food safety, wash hands before eating, avoid undercooked food"
    }
}

def save_health_log():
    """Save health log to a CSV file"""
    df = pd.DataFrame(st.session_state.health_log)
    df.to_csv('health_log.csv', index=False)

def load_health_log():
    """Load health log from CSV file"""
    if os.path.exists('health_log.csv'):
        df = pd.read_csv('health_log.csv')
        st.session_state.health_log = df.to_dict('records')

def save_users():
    """Save users to a JSON file"""
    with open('users.json', 'w') as f:
        json.dump(st.session_state.users, f)

def load_users():
    """Load users from JSON file"""
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            st.session_state.users = json.load(f)

def create_user(username, password, age, sex, weight=None, height=None):
    """Create a new user"""
    if username in st.session_state.users:
        return False, "Username already exists"
    
    st.session_state.users[username] = {
        'password': password,
        'age': age,
        'sex': sex,
        'weight': weight,
        'height': height,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    save_users()
    return True, f"""✅ Registration Successful!

Welcome to Hospital Health Assistant, {username}!

Your patient account has been created successfully with the following details:
- Age: {age} years
- Sex: {sex}
{f"- Weight: {weight} kg" if weight else ""}
{f"- Height: {height} cm" if height else ""}

You can now:
1. Log in to your account
2. Start tracking your health symptoms
3. Receive personalized medical advice
4. Access your health history

Please login to continue."""

def login_user(username, password):
    """Login a user"""
    if username not in st.session_state.users:
        return False, "User not found"
    
    if st.session_state.users[username]['password'] != password:
        return False, "Incorrect password"
    
    st.session_state.current_user = username
    return True, "Login successful"

def logout_user():
    """Logout current user"""
    st.session_state.current_user = None

def analyze_symptoms(symptoms, age=None, sex=None):
    """Analyze symptoms using Gemini API with age and sex-specific considerations"""
    if age is None or sex is None:
        user_info = st.session_state.users[st.session_state.current_user]
        age = user_info['age']
        sex = user_info['sex']
    
    # Age group categorization
    age_group = "child" if age < 18 else "adult" if age < 65 else "elderly"
    
    prompt = f"""As a medical assistant, analyze these symptoms for a {age_group} {sex.lower()} patient aged {age} years and provide:
    1. Possible conditions (considering age and sex-specific factors)
    2. Home remedies (appropriate for the patient's age group)
    3. When to seek medical attention
    4. Age and sex-specific recommendations
    
    Patient Information:
    - Age: {age} years
    - Sex: {sex}
    - Age Group: {age_group}
    
    Symptoms: {symptoms}
    
    Keep the response concise and focused on immediate actions. Consider age-appropriate medications and treatments.
    For {age_group}s, pay special attention to:
    - Dosage recommendations based on age
    - Age-specific warning signs
    - Sex-specific health considerations
    - Appropriate lifestyle recommendations"""
    
    response = model.generate_content(prompt)
    return response.text

def check_serious_symptoms(symptoms):
    """Check if any serious symptoms are present"""
    return any(symptom.lower() in symptoms.lower() for symptom in SERIOUS_SYMPTOMS)

def get_symptom_trends():
    """Analyze symptom trends from health log"""
    if not st.session_state.health_log:
        return None
    
    df = pd.DataFrame(st.session_state.health_log)
    symptom_counts = df['symptoms'].value_counts().head(5)
    return symptom_counts

def get_customized_advice():
    """Generate customized advice based on user's symptom history and demographics"""
    if not st.session_state.health_log:
        return "No health history available for personalized advice."
    
    user_info = st.session_state.users[st.session_state.current_user]
    age = user_info['age']
    sex = user_info['sex']
    age_group = "child" if age < 18 else "adult" if age < 65 else "elderly"
    
    df = pd.DataFrame(st.session_state.health_log)
    df['date'] = pd.to_datetime(df['date'])
    
    # Get last 7 days of logs
    last_week = datetime.now() - timedelta(days=7)
    recent_logs = df[df['date'] >= last_week]
    
    if recent_logs.empty:
        return "No recent symptoms recorded in the last 7 days."
    
    # Analyze patterns
    symptoms_text = "\n".join(recent_logs['symptoms'].tolist())
    
    prompt = f"""Based on the patient's health history and demographics, provide personalized advice:
    
    Patient Information:
    - Age: {age} years
    - Sex: {sex}
    - Age Group: {age_group}
    
    Recent Symptoms (Last 7 Days):
    {symptoms_text}
    
    Please provide:
    1. Pattern Analysis: Identify any recurring symptoms or patterns, considering age and sex-specific factors
    2. Lifestyle Recommendations: Suggest age and sex-appropriate lifestyle changes
    3. Preventive Measures: Recommend preventive steps based on the patient's demographics and symptom patterns
    4. Follow-up Actions: Suggest when to monitor or seek medical attention, with age-specific considerations
    
    Keep the advice practical and focused on the specific symptoms shown, while considering the patient's age group and sex."""
    
    response = model.generate_content(prompt)
    return response.text

# Custom CSS for hospital theme
def load_css():
    st.markdown("""
    <style>
    /* Hospital theme colors */
    :root {
        --hospital-blue: #0078D7;
        --hospital-light-blue: #E6F3FF;
        --hospital-white: #FFFFFF;
        --hospital-gray: #F5F5F5;
    }
    
    /* Main container styling */
    .main {
        background-color: var(--hospital-light-blue);
    }
    
    /* Header styling */
    .stApp header {
        background-color: var(--hospital-blue);
        color: white;
    }
    
    /* Header icons styling */
    .header-icons {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    .heart-icon {
        font-size: 3rem;
        color: #FF4B4B;
        margin: 0 1rem;
        animation: pulse 2s infinite;
    }
    
    .stethoscope-icon {
        font-size: 2.5rem;
        color: #FFFFFF;
        margin: 0 1rem;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--hospital-white);
        padding: 2rem 1rem;
    }
    
    /* Button styling */
    .stButton button {
        background-color: var(--hospital-blue);
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #005A9E;
    }
    
    /* Card styling */
    .card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Analysis Results card styling */
    .analysis-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid var(--hospital-blue);
    }
    
    .analysis-card h3 {
        color: var(--hospital-blue);
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    .analysis-card p {
        color: #333333;
        line-height: 1.6;
        margin: 0.5rem 0;
    }
    
    /* Health Advice card styling */
    .advice-card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #4CAF50;
    }
    
    .advice-card h3 {
        color: #4CAF50;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    .advice-card p {
        color: #333333;
        line-height: 1.6;
        margin: 0.5rem 0;
    }
    
    /* Input field styling */
    .stTextInput input, .stTextArea textarea {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 0.5rem;
    }
    
    /* Success message styling */
    .stSuccess {
        background-color: #E6FFE6;
        border-left: 4px solid #00CC00;
        padding: 1rem;
        border-radius: 5px;
    }
    
    /* Error message styling */
    .stError {
        background-color: #FFE6E6;
        border-left: 4px solid #FF0000;
        padding: 1rem;
        border-radius: 5px;
    }
    
    /* Warning message styling */
    .stWarning {
        background-color: #FFF2E6;
        border-left: 4px solid #FFA500;
        padding: 1rem;
        border-radius: 5px;
    }
    
    /* Hospital icon styling */
    .hospital-icon {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    
    /* User info card */
    .user-info {
        background-color: var(--hospital-light-blue);
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
    }
    
    /* Navigation styling */
    .nav-item {
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .nav-item:hover {
        background-color: var(--hospital-light-blue);
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Hospital Health Assistant",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_css()
    
    # Main title with hospital icon and animated heart
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div class='header-icons'>
                <span class='stethoscope-icon'>🩺</span>
                <span class='heart-icon'>❤️</span>
                <span class='stethoscope-icon'>🩺</span>
            </div>
            <h1 style='margin: 0; color: var(--hospital-blue);'>Hospital Health Assistant</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # User authentication
    if st.session_state.current_user is None:
        auth_page = st.sidebar.selectbox(
            "Authentication",
            ["Login", "Register"]
        )
        
        if auth_page == "Login":
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.header("👤 Patient Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.button("Login", key="login_btn"):
                success, message = login_user(username, password)
                if success:
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            st.markdown("</div>", unsafe_allow_html=True)
        
        else:  # Register
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.header("📝 New Patient Registration")
            
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                age = st.number_input("Age", min_value=1, max_value=120, step=1)
                sex = st.selectbox("Sex", ["Male", "Female", "Other"])
            
            with col2:
                weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, step=0.1, format="%.1f")
                height = st.number_input("Height (cm)", min_value=0.0, max_value=300.0, step=0.1, format="%.1f")
            
            if st.button("Register", key="register_btn"):
                if not username or not password or not age or not sex:
                    st.error("Please fill in all required fields")
                else:
                    success, message = create_user(username, password, age, sex, weight, height)
                    if success:
                        st.markdown(f"""
                            <div style='background-color: #E6FFE6; padding: 20px; border-radius: 10px; margin: 20px 0;'>
                                {message.replace(chr(10), '<br>')}
                            </div>
                        """, unsafe_allow_html=True)
                        st.info("Please switch to the Login page to access your account.")
                    else:
                        st.error(message)
            st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Show logout button in sidebar
    if st.sidebar.button("Logout", key="logout_btn"):
        logout_user()
        st.rerun()
    
    # Display current user info in a card
    st.sidebar.markdown("<div class='user-info'>", unsafe_allow_html=True)
    st.sidebar.markdown(f"### 👤 Patient Information")
    st.sidebar.write(f"**Name:** {st.session_state.current_user}")
    user_info = st.session_state.users[st.session_state.current_user]
    st.sidebar.write(f"**Age:** {user_info['age']}")
    st.sidebar.write(f"**Sex:** {user_info['sex']}")
    if user_info['weight']:
        st.sidebar.write(f"**Weight:** {user_info['weight']} kg")
    if user_info['height']:
        st.sidebar.write(f"**Height:** {user_info['height']} cm")
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    # Sidebar navigation with icons
    st.sidebar.markdown("### 🏥 Navigation")
    page = st.sidebar.selectbox(
        "",
        ["Log Symptoms", "View Health Log", "Customized Advice", "Seasonal Disease Info"],
        format_func=lambda x: {
            "Log Symptoms": "📝 Log Symptoms",
            "View Health Log": "📊 Health Log",
            "Customized Advice": "💡 Health Advice",
            "Seasonal Disease Info": "🌡️ Disease Information"
        }[x]
    )
    
    if page == "Log Symptoms":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.header("📝 Symptom Logging")
        
        symptoms = st.text_area("Describe your symptoms:", height=100, 
                              placeholder="Please describe your symptoms in detail...")
        
        # Add checkbox for using registration details
        use_registration_details = st.checkbox("Use my registration details for age and sex", value=True)
        
        if use_registration_details:
            user_info = st.session_state.users[st.session_state.current_user]
            st.info(f"Using your registration details: Age {user_info['age']} years, Sex: {user_info['sex']}")
            age = user_info['age']
            sex = user_info['sex']
        else:
            col1, col2 = st.columns(2)
            with col1:
                age = st.number_input("Age", min_value=1, max_value=120, step=1, 
                                    value=st.session_state.users[st.session_state.current_user]['age'])
            with col2:
                sex = st.selectbox("Sex", ["Male", "Female", "Other"], 
                                 index=["Male", "Female", "Other"].index(st.session_state.users[st.session_state.current_user]['sex']))
        
        if st.button("Analyze Symptoms", key="analyze_btn"):
            if not symptoms.strip():
                st.warning("Please enter your symptoms before proceeding.")
            else:
                with st.spinner("🔍 Analyzing symptoms..."):
                    # Get AI analysis with current age and sex
                    analysis = analyze_symptoms(symptoms, age, sex)
                    
                    # Check for serious symptoms
                    if check_serious_symptoms(symptoms):
                        st.error("⚠️ Serious symptoms detected! Please seek medical attention immediately.")
                    
                    # Display analysis with improved styling
                    st.markdown("""
                        <div class='analysis-card'>
                            <h3>📋 Analysis Results</h3>
                            <div style='color: #333333;'>
                                {}
                            </div>
                        </div>
                    """.format(analysis.replace('\n', '<br>')), unsafe_allow_html=True)
                    
                    # Log the entry with current age and sex
                    log_entry = {
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'username': st.session_state.current_user,
                        'symptoms': symptoms,
                        'analysis': analysis,
                        'age_at_log': age,
                        'sex_at_log': sex
                    }
                    st.session_state.health_log.append(log_entry)
                    save_health_log()
                    
                    st.success("✅ Symptoms logged successfully!")
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif page == "View Health Log":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.header("📊 Health Records")
        
        if not st.session_state.health_log:
            st.info("No health records found.")
        else:
            # Display health log for current user only
            df = pd.DataFrame(st.session_state.health_log)
            user_logs = df[df['username'] == st.session_state.current_user]
            
            # Format the dataframe
            user_logs['date'] = pd.to_datetime(user_logs['date']).dt.strftime('%Y-%m-%d %H:%M')
            user_logs = user_logs.rename(columns={
                'date': 'Date',
                'symptoms': 'Symptoms',
                'analysis': 'Analysis'
            })
            
            st.dataframe(user_logs, use_container_width=True)
            
            # Display symptom trends
            st.subheader("📈 Symptom Trends")
            trends = get_symptom_trends()
            if trends is not None:
                fig = px.bar(trends, title="Most Common Symptoms")
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    title_x=0.5,
                    title_font_size=20
                )
                st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif page == "Customized Advice":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.header("💡 Personalized Health Advice")
        
        if st.button("Generate Health Advice", key="advice_btn"):
            with st.spinner("🔍 Analyzing your health history..."):
                advice = get_customized_advice()
                
                # Display advice with improved styling
                st.markdown("""
                    <div class='advice-card'>
                        <h3>💡 Your Personalized Health Insights</h3>
                        <div style='color: #333333;'>
                            {}
                        </div>
                    </div>
                """.format(advice.replace('\n', '<br>')), unsafe_allow_html=True)
                
                # Display recent symptoms if available
                if st.session_state.health_log:
                    df = pd.DataFrame(st.session_state.health_log)
                    df['date'] = pd.to_datetime(df['date'])
                    user_logs = df[df['username'] == st.session_state.current_user]
                    recent_logs = user_logs[user_logs['date'] >= datetime.now() - timedelta(days=7)]
                    
                    if not recent_logs.empty:
                        st.markdown("""
                            <div class='card'>
                                <h3>📊 Recent Symptoms (Last 7 Days)</h3>
                            </div>
                        """, unsafe_allow_html=True)
                        recent_logs['date'] = recent_logs['date'].dt.strftime('%Y-%m-%d %H:%M')
                        recent_logs = recent_logs.rename(columns={
                            'date': 'Date',
                            'symptoms': 'Symptoms'
                        })
                        st.dataframe(recent_logs[['Date', 'Symptoms']], use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:  # Seasonal Disease Info
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.header("🌡️ Seasonal Disease Information")
        
        for disease, info in SEASONAL_DISEASES.items():
            with st.expander(f"📋 {disease}"):
                st.markdown(f"""
                    <div style='padding: 1rem;'>
                        <h4>Symptoms:</h4>
                        <p>{info['symptoms']}</p>
                        <h4>First Aid:</h4>
                        <p>{info['first_aid']}</p>
                        <h4>Precautions:</h4>
                        <p>{info['precautions']}</p>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    load_health_log()
    load_users()
    main() 