import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import time
import random

import warnings
warnings.filterwarnings('ignore')

# This must be the first Streamlit command
st.set_page_config(
    page_title="Personal Fitness Tracker",
    page_icon="��",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Then add the custom CSS
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #1a1a1a;
        color: #ffffff;
    }
    
    /* Main title styling */
    .main-title {
        color: #4caf50;
        text-align: center;
        font-size: 3em;
        padding: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Section headers */
    h2 {
        color: #64b5f6;
        padding: 10px 0;
        border-bottom: 2px solid #64b5f6;
        margin-bottom: 20px;
    }
    
    h3 {
        color: #81c784;
        padding: 8px 0;
    }
    
    /* Metrics styling */
    div.stMetric {
        background-color: #2d2d2d;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        color: #ffffff;
    }
    
    /* Table styling */
    div.stTable {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    }
    
    .stTable table {
        background-color: #2d2d2d;
        color: #ffffff;
    }
    
    .stTable th {
        background-color: #1a1a1a;
        color: #4caf50;
    }
    
    /* Progress bar styling */
    div.stProgress > div > div {
        background-color: #4caf50;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #2d2d2d;
        border-right: 1px solid #404040;
    }
    
    /* Activity cards */
    .activity-card {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        margin: 10px 0;
        color: #ffffff;
    }
    
    /* Workout plan styling */
    .workout-plan {
        background-color: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border: 1px solid #404040;
    }
    
    /* Separator styling */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #4caf50, transparent);
        margin: 30px 0;
    }
    
    /* Input fields */
    .stSlider {
        background-color: #2d2d2d;
    }
    
    .stSelectbox {
        background-color: #2d2d2d;
    }
    
    /* Text color for all elements */
    p, span, div {
        color: #ffffff;
    }
    
    /* Links */
    a {
        color: #64b5f6 !important;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #2d2d2d;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #ffffff;
    }
    
    /* BMI status box */
    .bmi-status {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Metrics delta color */
    .stMetric [data-testid="stMetricDelta"] {
        color: #4caf50;
    }
</style>
""", unsafe_allow_html=True)

# Replace the title with styled version
st.markdown("<h1 class='main-title'>🏃‍♂️ Personal Fitness Tracker</h1>", unsafe_allow_html=True)

st.write("## Personal Fitness Tracker")
#st.image("", use_column_width=True)
st.write("In this WebApp you will be able to observe your predicted calories burned in your body. Pass your parameters such as `Age`, `Gender`, `BMI`, etc., into this WebApp and then you will see the predicted value of kilocalories burned.")

st.sidebar.header("User Input Parameters: ")

def user_input_features():
    # Create tabs in sidebar for better organization
    tabs = st.sidebar.tabs(["Basic Info", "Exercise Parameters", "Fitness Goals"])
    
    with tabs[0]:
        st.write("### Physical Information")
        height = st.slider("Height (cm): ", 140, 220, 170)
        weight = st.slider("Weight (kg): ", 40, 160, 70)
        age = st.slider("Age: ", 10, 100, 30)
        
        # Calculate BMI automatically
        bmi = round(weight / ((height/100) ** 2), 2)
        
        # Show BMI status in a colored box
        st.write("### BMI Status")
        status_color = {
            "Underweight": "blue",
            "Normal Weight": "green",
            "Overweight": "orange",
            "Obese": "red"
        }
        
        if bmi < 18.5:
            category, color = "Underweight", "blue"
        elif 18.5 <= bmi < 25:
            category, color = "Normal Weight", "green"
        elif 25 <= bmi < 30:
            category, color = "Overweight", "orange"
        else:
            category, color = "Obese", "red"
            
        st.markdown(
            f"""
            <div style="padding:10px;border-radius:10px;background-color:#2d2d2d;border:1px solid {color};">
                <p style="color:{color};font-weight:bold;">BMI: {bmi}</p>
                <p style="color:{color};">Category: {category}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with tabs[1]:
        st.write("### Exercise Parameters")
        duration = st.slider("Duration (min): ", 10, 120, 30)
        heart_rate = st.slider("Heart Rate: ", 60, 130, 80)
        body_temp = st.slider("Body Temperature (C): ", 36, 42, 38)

    with tabs[2]:
        st.write("### Fitness Goals")
        fitness_goal = st.selectbox("Fitness Goal: ", ["Weight Loss", "Muscle Gain", "Endurance"])
        fitness_level = st.selectbox("Fitness Level: ", ["Beginner", "Intermediate", "Advanced"])

    return {
        "age": age,
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "duration": duration,
        "heart_rate": heart_rate,
        "body_temp": body_temp,
        "fitness_goal": fitness_goal,
        "fitness_level": fitness_level
    }

# Move the user input section before the Health Insights section
user_input = user_input_features()
df = pd.DataFrame(user_input, index=[0])  # Convert the dictionary to a DataFrame

# Now add the Health Insights section
st.write("---")
st.header("Health Insights")

# Create three columns for better layout
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.write("### 📊 BMI Categories")
    bmi_categories = pd.DataFrame({
        "Category": ["Underweight", "Normal Weight", "Overweight", "Obese"],
        "BMI Range": ["< 18.5", "18.5 - 24.9", "25 - 29.9", "≥ 30"],
        "Status": ["🔵", "🟢", "🟡", "🔴"]
    })
    st.table(bmi_categories)

with col2:
    st.write("### 💪 Recommended Activities")
    user_bmi = user_input["bmi"]
    
    if user_bmi < 18.5:
        activities = [
            "🏋️ Strength training exercises",
            "🥩 Protein-rich diet",
            "🍽️ Regular small meals",
            "🥜 Healthy calorie-dense foods"
        ]
    elif 18.5 <= user_bmi < 25:
        activities = [
            "🏃‍♂️ Mix of cardio and strength",
            "🥗 Maintain balanced diet",
            "⏰ Regular exercise routine",
            "💪 Focus on fitness goals"
        ]
    elif 25 <= user_bmi < 30:
        activities = [
            "🚶‍♂️ Regular cardio exercises",
            "🍽️ Portion control",
            "💧 Increased water intake",
            "📝 Food journal tracking"
        ]
    else:
        activities = [
            "🏊‍♂️ Low-impact exercises",
            "🏊‍♀️ Swimming or water aerobics",
            "👨‍⚕️ Consult healthcare provider",
            "📊 Regular health monitoring"
        ]
    
    for activity in activities:
        st.markdown(f"- {activity}")

with col3:
    st.write("### 🎯 Daily Health Goals")
    water_intake = round(user_input["weight"] * 0.033, 1)
    
    # Create a metrics display
    st.metric(
        label="Daily Water Intake",
        value=f"{water_intake}L",
        delta="Target"
    )
    
    # Calculate recommended sleep based on age
    if user_input["age"] < 18:
        sleep_hours = "8-10"
    elif user_input["age"] < 65:
        sleep_hours = "7-9"
    else:
        sleep_hours = "7-8"
    
    st.metric(
        label="Sleep Target",
        value=f"{sleep_hours} hrs",
        delta="Recommended"
    )

# Load workout data
workout_data = pd.read_csv("assets/workouts.csv")  # Assuming you have a CSV with workout data

# Function to recommend workouts
def recommend_workouts(user_input):
    # Filter workouts based on user input
    recommended = workout_data[
        (workout_data['Goal'] == user_input['fitness_goal']) &
        (workout_data['Level'] == user_input['fitness_level'])
    ]
    
    # Drop duplicates to ensure unique workouts
    recommended = recommended.drop_duplicates(subset=['Workout_Name'])
    
    # Limit to a certain number of recommendations if needed
    return recommended.sample(n=min(len(recommended), 5))  # Adjust the number as needed

# Function to create a weekly workout routine
def create_weekly_routine(user_input):
    # Filter workouts based on user input
    filtered_workouts = workout_data[
        (workout_data['Goal'] == user_input['fitness_goal']) &
        (workout_data['Level'] == user_input['fitness_level'])
    ]
    
    # Create a weekly routine
    weekly_routine = {}
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    # Ensure we have enough unique workouts for the week
    if len(filtered_workouts) < len(days_of_week):
        st.warning("Not enough unique workouts available for a full week routine. Some workouts may be repeated.")
    
    # Shuffle the filtered workouts to randomize selection
    unique_workouts = filtered_workouts.sample(n=min(len(filtered_workouts), len(days_of_week))).reset_index(drop=True)
    
    for day, workout in zip(days_of_week, unique_workouts.iterrows()):
        selected_workout = workout[1]  # Get the row data directly
        weekly_routine[day] = {
            "Workout_Name": selected_workout['Workout_Name'],
            "Duration": selected_workout['Duration'],
            "Intensity": selected_workout['Intensity']
        }
    
    return weekly_routine

# Get recommendations
recommended_workouts = recommend_workouts(user_input)

# Create weekly routine
weekly_routine = create_weekly_routine(user_input)

# Display recommendations
st.write("### Recommended Workouts:")
for index, workout in recommended_workouts.iterrows():
    st.write(f"**Workout:** {workout['Workout_Name']}")
    st.write(f"**Duration:** {workout['Duration']} minutes")
    st.write(f"**Intensity:** {workout['Intensity']} intensity")
    st.write("---")  # Add a separator for better visual distinction

# Display weekly routine
st.markdown("<div class='workout-plan'>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>📅 Weekly Workout Plan</h3>", unsafe_allow_html=True)

# Create a DataFrame for the weekly routine
routine_data = {
    "Day": [],
    "Workout": [],
    "Duration": [],
    "Intensity": []
}

for day, workout in weekly_routine.items():
    routine_data["Day"].append(day)
    routine_data["Workout"].append(workout['Workout_Name'])
    routine_data["Duration"].append(f"{workout['Duration']} minutes")
    routine_data["Intensity"].append(f"{workout['Intensity']} intensity")

# Convert to DataFrame
routine_df = pd.DataFrame(routine_data)

# Display the DataFrame as a table
st.table(routine_df)
st.markdown("</div>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    calories = pd.read_csv("assets/calories.csv")
    exercise = pd.read_csv("assets/exercise.csv")
    workout_data = pd.read_csv("assets/workouts.csv")
    return calories, exercise, workout_data
