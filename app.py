import streamlit as st
import pandas as pd
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Smart Gym Diet Planner",
    page_icon="🏋",
    layout="wide"
)

# ---------------------------------------------------
# USER STORAGE & MODEL CACHE
# ---------------------------------------------------
USER_FILE = "users.csv"

def load_users():
    if not os.path.exists(USER_FILE):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USER_FILE, index=False)
        return df
    return pd.read_csv(USER_FILE)

def save_user(username, password):
    df = load_users()
    username = username.strip().lower()
    password = password.strip()
    new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)

def check_login(username, password):
    df = load_users()
    username = username.strip().lower()
    password = password.strip()
    return not df[(df["username"].str.lower() == username) & (df["password"] == password)].empty

@st.cache_resource
def load_food_model():
    return tf.keras.applications.MobileNetV2(weights="imagenet")

# ---------------------------------------------------
# STYLING
# ---------------------------------------------------
st.markdown("""
<style>
/* GLOBAL BACKGROUND */
.stApp {
    background-color: #f5deb3; 
}

/* TAB BAR STYLING - Titles always RED */
button[data-baseweb="tab"] p {
    color: red !important;
    font-weight: bold;
    font-size: 22px; 
}

/* SPECIFIC STYLE FOR LOGIN/SIGNUP TABS (Smaller size) */
[data-testid="stExpander"] button[data-baseweb="tab"] p, 
.stTabs button[data-baseweb="tab"] p {
    font-size: 16px !important; 
}

/* MAIN TITLE - MASSIVE SIZE & NO SHADOW */
.main-title { 
    font-size: 150px; 
    font-weight: 950; 
    text-align: center; 
    color: red;
    margin-bottom: 0px;
    line-height: 1;
    text-transform: uppercase;
    text-shadow: none !important; /* Explicitly removed shadow */
}

.sub-title { 
    font-size: 26px; 
    text-align: center; 
    color: #5d4037;
    font-weight: bold;
    margin-bottom: 30px;
}

/* BLACK INPUT LABELS */
label, .stTextInput label, .stNumberInput label, .stSelectbox label {
    color: black !important;
    font-weight: bold;
    font-size: 18px;
}

/* HEADINGS */
.red-heading {
    color: red !important;
    font-size: 30px;
    font-weight: 700;
}

/* DARK GREEN SUCCESS THEME */
.stAlert, div[data-testid="stNotificationContentSuccess"] {
    background-color: #006400 !important; 
    color: white !important;
}

/* DETECTION TEXT */
.detection-result {
    color: #006400; 
    font-size: 35px;
    font-weight: bold;
}

/* TABLE STYLING */
.stDataFrame, div[data-testid="stTable"] {
    background-color: #1e1e1e;
    border-radius: 12px;
}
table {
    color: white !important;
    background-color: #1e1e1e !important;
}

/* BOXES */
.custom-box {
    background-color: #1e1e1e;
    color: white !important;
    padding: 25px;
    border-radius: 15px;
    margin-bottom: 20px;
    border-left: 10px solid red;
}

/* BUTTONS */
.stButton button {
    background-color: red !important;
    color: white !important;
    font-size: 18px;
    padding: 10px 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------------------------------------------
# MAIN APP
# ---------------------------------------------------
if not st.session_state.logged_in:
    st.markdown('<p class="main-title">SMART GYM DIET PLANNER</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">AI Diet + Food Analyzer</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        t1, t2 = st.tabs(["🔐 Login", "📝 Signup"])
        with t1:
            with st.form("login"):
                u = st.text_input("Username")
                p = st.text_input("Password", type="password")
                if st.form_submit_button("Login"):
                    if check_login(u, p):
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Invalid Credentials ❌")
        with t2:
            with st.form("signup"):
                nu = st.text_input("New Username")
                np = st.text_input("New Password", type="password")
                if st.form_submit_button("Signup"):
                    save_user(nu, np)
                    st.success("Account Created! ✅")

else:
    st.markdown('<p class="main-title">SMART GYM DIET PLANNER</p>', unsafe_allow_html=True)
    
    try:
        food_df = pd.read_csv("food.csv")
    except:
        st.error("Missing food.csv file!")
        st.stop()

    tab1, tab2, tab3 = st.tabs(["👤 User Planner", "🥗 Diet Plan", "📷 Food Analyzer"])

    # --- TAB 1: PLANNER ---
    with tab1:
        with st.form("user"):
            c1, c2 = st.columns(2)
            with c1:
                age = st.number_input("Age", 10, 80, 25)
                h = st.number_input("Height (cm)", 120, 230, 170)
                w = st.number_input("Weight (kg)", 30, 200, 70)
            with c2:
                gender = st.selectbox("Gender", ["Male", "Female"])
                goal = st.selectbox("Goal", ["Weight Loss", "Maintenance", "Weight Gain"])
                activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])
            
            if st.form_submit_button("Generate Plan"):
                bmr = (10*w + 6.25*h - 5*age + (5 if gender=="Male" else -161))
                mult = {"Low": 1.2, "Moderate": 1.55, "High": 1.9}
                t_cal = int(bmr * mult[activity])
                if goal == "Weight Loss": t_cal -= 500
                elif goal == "Weight Gain": t_cal += 500
                
                st.session_state.calories = t_cal
                st.session_state.goal = goal
                st.success(f"Target: {t_cal} kcal per day ✅")

    # --- TAB 2: DIET PLAN ---
    with tab2:
        if "calories" in st.session_state:
            st.markdown('<p class="red-heading">Recommended Foods</p>', unsafe_allow_html=True)
            data = food_df.sample(min(len(food_df), 5)).reset_index(drop=True)
            data.index += 1 
            st.table(data)

            st.markdown('<p class="red-heading">Daily Meal Schedule</p>', unsafe_allow_html=True)
            meals = pd.DataFrame({
                "S.No": [1, 2, 3, 4],
                "Time": ["08:30 AM", "01:30 PM", "05:30 PM", "08:30 PM"],
                "Meal": ["Breakfast", "Lunch", "Snacks", "Dinner"],
                "Suggested Food": food_df["Food"].sample(min(len(food_df), 4)).values
            }).set_index("S.No")
            st.table(meals)
        else:
            st.warning("Please complete Tab 1 first.")

    # --- TAB 3: FOOD ANALYZER ---
    with tab3:
        st.markdown('<p class="red-heading">AI Food Recognition</p>', unsafe_allow_html=True)
        file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
        
        if file:
            img = Image.open(file)
            st.image(img, width=350)
            
            with st.spinner("Analyzing Image..."):
                model = load_food_model()
                img_prep = img.resize((224,224))
                arr = preprocess_input(np.expand_dims(image.img_to_array(img_prep), axis=0))
                preds = decode_predictions(model.predict(arr), top=5)[0]
                
                # FOOD VALIDATION LIST
                food_keywords = ['food', 'fruit', 'vegetable', 'meat', 'dish', 'meal', 'bread', 'soup', 'pizza', 'burger', 'apple', 'banana', 'custard', 'carbonara', 'egg', 'hotdog']
                is_food = any(any(key in p[1].lower() for key in food_keywords) for p in preds)
                
                if not is_food:
                    st.error("⚠️ Please upload the food images only!")
                else:
                    label = preds[0][1].replace("_", " ").title()
                    st.markdown(f'<p class="detection-result">🔍 Detected: {label}</p>', unsafe_allow_html=True)
                    
                    match = food_df[food_df["Food"].str.contains(label, case=False, na=False)]
                    if not match.empty:
                        row = match.iloc[0]
                        st.markdown(f"""
                        <div class="custom-box">
                        <h3>Detailed Analysis</h3>
                        <p><b>Item:</b> {label}</p>
                        <p><b>Calories:</b> {row['Calories']} kcal</p>
                        <p><b>Protein:</b> {row['Protein']}g</p>
                        <p><b>Status:</b> Fit for your {st.session_state.get('goal', 'plan')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info(f"Detected {label}, but detailed nutrition is missing from our current database.")

    st.markdown("---")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
