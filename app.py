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
import base64
from io import BytesIO
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import tempfile

import warnings
warnings.filterwarnings('ignore')

# This must be the first Streamlit command
st.set_page_config(
    page_title="FitTrack",
    page_icon="🔥",
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
    
    /* Nutrition cards */
    .nutrition-card {
        background-color: #2d2d2d;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #4caf50;
    }
    
    /* Meal plan expander */
    .streamlit-expanderHeader {
        background-color: #2d2d2d;
        border-radius: 10px;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

# Replace the title with styled version
st.markdown("<h1 class='main-title'>🏃‍♂️ FitTrack - Personal Fitness Tracker</h1>", unsafe_allow_html=True)

st.write("## FitTrack")
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
        activity_level = st.selectbox("Activity Level: ", 
                                    ["Sedentary", "Light", "Moderate", "Very Active", "Extra Active"])
        dietary_preference = st.selectbox("Dietary Preference: ", 
                                        ["No Restrictions", "Vegetarian", "Vegan", "Keto", "Mediterranean"])

    return {
        "age": age,
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "duration": duration,
        "heart_rate": heart_rate,
        "body_temp": body_temp,
        "fitness_goal": fitness_goal,
        "fitness_level": fitness_level,
        "activity_level": activity_level,
        "dietary_preference": dietary_preference
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

# Function to calculate daily caloric needs
def calculate_caloric_needs(weight, height, age, activity_level, goal):
    # Basic BMR calculation using Mifflin-St Jeor Equation
    bmr = 10 * weight + 6.25 * height - 5 * age + 5
    
    # Activity multipliers
    activity_multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Very Active": 1.725,
        "Extra Active": 1.9
    }
    
    # Calculate TDEE (Total Daily Energy Expenditure)
    tdee = bmr * activity_multipliers[activity_level]
    
    # Adjust based on fitness goal
    if goal == "Weight Loss":
        return int(tdee - 500)  # 500 calorie deficit
    elif goal == "Muscle Gain":
        return int(tdee + 300)  # 300 calorie surplus
    else:  # Maintenance/Endurance
        return int(tdee)

# Function to generate meal plan
def generate_meal_plan(calories, dietary_preference):
    meal_distribution = {
        "Breakfast": 0.3,
        "Lunch": 0.35,
        "Dinner": 0.25,
        "Snacks": 0.1
    }
    
    meal_plan = {}
    for meal, percentage in meal_distribution.items():
        meal_calories = int(calories * percentage)
        meal_plan[meal] = {
            "Calories": meal_calories,
            "Protein": f"{int(meal_calories * 0.3 / 4)}g",  # 30% from protein
            "Carbs": f"{int(meal_calories * 0.4 / 4)}g",    # 40% from carbs
            "Fats": f"{int(meal_calories * 0.3 / 9)}g"      # 30% from fats
        }
    
    return meal_plan

# Add these functions before the meal plan display section
def load_food_database():
    try:
        food_db = pd.read_csv("assets/food_database.csv")
        return food_db
    except FileNotFoundError:
        st.error("Food database file not found. Please ensure food_database.csv exists in the assets folder.")
        return pd.DataFrame()

def suggest_meals(meal_plan, dietary_preference, goal):
    # Load food database
    food_db = load_food_database()
    
    # Filter foods based on dietary preference
    if dietary_preference != "No Restrictions":
        available_foods = food_db[
            (food_db['dietary_type'] == dietary_preference) | 
            (food_db['dietary_type'] == 'No Restrictions')
        ]
    else:
        available_foods = food_db
    
    suggested_meals = {}
    
    for meal, details in meal_plan.items():
        # Filter for specific meal type
        meal_options = available_foods[available_foods['meal_type'] == meal]
        
        target_calories = details["Calories"]
        
        # Select foods that match caloric needs
        suggested_foods = []
        remaining_calories = target_calories
        
        # Sort by calories to optimize selection
        meal_options = meal_options.sort_values('calories')
        
        for _, food in meal_options.iterrows():
            if food['calories'] <= remaining_calories:
                suggested_foods.append({
                    'name': food['food_name'],
                    'calories': food['calories'],
                    'protein': food['protein'],
                    'carbs': food['carbs'],
                    'fats': food['fats'],
                    'portion': food['portion_size'],
                    'prep_time': food['preparation_time']
                })
                remaining_calories -= food['calories']
                
                if remaining_calories < 100:  # Stop if remaining calories are too low
                    break
        
        suggested_meals[meal] = suggested_foods
    
    return suggested_meals

# Then continue with the meal plan display section
st.write("---")
st.markdown("<h2>🍽️ Nutrition Plan</h2>", unsafe_allow_html=True)

# Calculate daily caloric needs
daily_calories = calculate_caloric_needs(
    user_input["weight"],
    user_input["height"],
    user_input["age"],
    user_input["activity_level"],
    user_input["fitness_goal"]
)

# Generate meal plan
meal_plan = generate_meal_plan(daily_calories, user_input["dietary_preference"])

# Display nutrition information
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<div class='nutrition-card'>", unsafe_allow_html=True)
    st.subheader("Daily Nutrition Targets")
    st.metric("Daily Calories", f"{daily_calories} kcal")
    st.write(f"Based on your {user_input['fitness_goal'].lower()} goal")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='nutrition-card'>", unsafe_allow_html=True)
    st.subheader("Macronutrient Split")
    st.write("- Protein: 30%")
    st.write("- Carbohydrates: 40%")
    st.write("- Fats: 30%")
    st.markdown("</div>", unsafe_allow_html=True)

# Display meal plan
st.subheader("Daily Meal Plan")
suggested_meals = suggest_meals(meal_plan, user_input["dietary_preference"], user_input["fitness_goal"])

for meal, details in meal_plan.items():
    with st.expander(f"{meal} - {details['Calories']} kcal"):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write("**Target Macros:**")
            st.write(f"Protein: {details['Protein']}")
            st.write(f"Carbs: {details['Carbs']}")
            st.write(f"Fats: {details['Fats']}")
        
        with col2:
            st.write("**Suggested Foods:**")
            for food in suggested_meals[meal]:
                st.markdown(
                    f"""
                    <div style="background-color: #2d2d2d; padding: 10px; border-radius: 5px; margin: 5px 0;">
                        <h4>{food['name']}</h4>
                        <p>Calories: {food['calories']} kcal</p>
                        <p>Protein: {food['protein']}g | Carbs: {food['carbs']}g | Fats: {food['fats']}g</p>
                        <p>Portion: {food['portion']}</p>
                        <p>Prep Time: {food['prep_time']} minutes</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

@st.cache_data
def load_data():
    calories = pd.read_csv("assets/calories.csv")
    exercise = pd.read_csv("assets/exercise.csv")
    workout_data = pd.read_csv("assets/workouts.csv")
    return calories, exercise, workout_data

# Add these functions before the display sections

def create_download_link(df, filename, link_text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def create_pdf_report(workout_routine, meal_plan, user_input, suggested_meals):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30
    )
    
    subheader_style = ParagraphStyle(
        'CustomSubHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        textColor=colors.darkgreen
    )
    
    meal_header_style = ParagraphStyle(
        'MealHeader',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.navy
    )
    
    # Title
    elements.append(Paragraph("Your Personal Fitness Plan", header_style))
    elements.append(Spacer(1, 20))
    
    # User Details Section
    elements.append(Paragraph("User Details:", subheader_style))
    user_details = [
        f"Height: {user_input['height']} cm",
        f"Weight: {user_input['weight']} kg",
        f"BMI: {user_input['bmi']}",
        f"Fitness Goal: {user_input['fitness_goal']}",
        f"Activity Level: {user_input['activity_level']}",
        f"Dietary Preference: {user_input['dietary_preference']}"
    ]
    for detail in user_details:
        elements.append(Paragraph(detail, styles['Normal']))
    elements.append(Spacer(1, 20))
    
    # Workout Plan Section
    elements.append(Paragraph("Weekly Workout Plan:", subheader_style))
    workout_data = [[day, details['Workout_Name'], 
                    f"{details['Duration']} minutes", 
                    details['Intensity']] 
                   for day, details in workout_routine.items()]
    workout_data.insert(0, ['Day', 'Workout', 'Duration', 'Intensity'])
    
    workout_table = Table(workout_data)
    workout_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(workout_table)
    elements.append(Spacer(1, 30))
    
    # Nutrition Plan Section
    elements.append(Paragraph("Daily Nutrition Plan:", subheader_style))
    elements.append(Paragraph(f"Total Daily Calories: {sum(details['Calories'] for details in meal_plan.values())} kcal", 
                            styles['Normal']))
    elements.append(Spacer(1, 10))
    
    # Detailed Meal Plan with Suggested Foods
    for meal, details in meal_plan.items():
        # Meal Header
        elements.append(Paragraph(f"{meal} ({details['Calories']} kcal)", meal_header_style))
        
        # Macronutrient Table
        macro_data = [
            ['Nutrient', 'Amount'],
            ['Protein', details['Protein']],
            ['Carbs', details['Carbs']],
            ['Fats', details['Fats']]
        ]
        macro_table = Table(macro_data)
        macro_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(macro_table)
        elements.append(Spacer(1, 10))
        
        # Suggested Foods Section
        elements.append(Paragraph("Suggested Foods:", styles['Heading4']))
        if meal in suggested_meals and suggested_meals[meal]:
            for food in suggested_meals[meal]:
                food_data = [
                    ['Food Item', food['name']],
                    ['Calories', f"{food['calories']} kcal"],
                    ['Protein', f"{food['protein']}g"],
                    ['Carbs', f"{food['carbs']}g"],
                    ['Fats', f"{food['fats']}g"],
                    ['Portion', food['portion']],
                    ['Prep Time', f"{food['prep_time']} minutes"]
                ]
                food_table = Table(food_data)
                food_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey)
                ]))
                elements.append(food_table)
                elements.append(Spacer(1, 5))
        else:
            elements.append(Paragraph("No specific food suggestions available", styles['Normal']))
        
        elements.append(Spacer(1, 15))
    
    # Additional Notes Section
    elements.append(Paragraph("Important Notes:", subheader_style))
    notes = [
        "• Drink plenty of water throughout the day",
        f"• Recommended daily water intake: {round(user_input['weight'] * 0.033, 1)}L",
        "• Eat slowly and mindfully",
        "• Try to have meals at consistent times",
        "• Adjust portions based on hunger and activity level",
        "• Consider food allergies and consult with healthcare provider if needed"
    ]
    for note in notes:
        elements.append(Paragraph(note, styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Add after the workout plan display section:
st.write("### Download Workout Plan")
col1, col2 = st.columns(2)

with col1:
    # CSV download
    csv_workout = create_download_link(routine_df, "weekly_workout_plan.csv", "📥 Download Workout Plan (CSV)")
    st.markdown(csv_workout, unsafe_allow_html=True)

with col2:
    # PDF download
    pdf_buffer = create_pdf_report(weekly_routine, meal_plan, user_input, suggested_meals)
    pdf_bytes = pdf_buffer.getvalue()
    st.download_button(
        label="📑 Download Complete Fitness Plan (PDF)",
        data=pdf_bytes,
        file_name="fitness_plan.pdf",
        mime="application/pdf"
    )

# Add after the meal plan display section:
st.write("### Download Meal Plan")

# Create DataFrame for meal plan
meal_plan_df = pd.DataFrame([
    {
        "Meal": meal,
        "Calories": details["Calories"],
        "Protein": details["Protein"],
        "Carbs": details["Carbs"],
        "Fats": details["Fats"]
    }
    for meal, details in meal_plan.items()
])

# CSV download for meal plan
csv_meal = create_download_link(meal_plan_df, "daily_meal_plan.csv", "📥 Download Meal Plan (CSV)")
st.markdown(csv_meal, unsafe_allow_html=True)
