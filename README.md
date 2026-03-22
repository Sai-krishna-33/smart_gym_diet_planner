# 🚀 Smart Gym Diet Planner

An AI-powered web application that helps fitness enthusiasts plan their nutrition using BMR calculations and real-time Image Recognition to analyze food intake.

---

## 📝 Project Problem Statement
Maintaining a consistent diet is the hardest part of any fitness journey. Users often struggle to:
1.  **Calculate accurate daily caloric needs** based on specific fitness goals (Weight Loss, Gain, or Maintenance).
2.  **Identify nutritional values** of the food they are about to eat instantly.
3.  **Follow a structured meal schedule** that aligns with their metabolic rate.

**The Solution:** An integrated platform where users can calculate their personalized diet plans and use an AI "Food Analyzer" to identify meals and their nutritional content simply by uploading a photo.

---

## 💡 Solution Approach
* **Authentication:** A secure CSV-based login/signup system to manage user sessions.
* **Nutrition Logic:** Implementation of the Mifflin-St Jeor Equation to calculate Basal Metabolic Rate (BMR) and Total Daily Energy Expenditure (TDEE).
* **Deep Learning:** Utilizes the **MobileNetV2** architecture (pre-trained on ImageNet) to classify food images in real-time.
* **Data Matching:** A custom lookup algorithm that matches AI-detected labels with a local nutritional database (`food.csv`).
* **Frontend:** Built with **Streamlit** for a high-performance, responsive, and "Gym-themed" user interface.

---

## ✨ Project Features
* **Ultra-Massive UI:** A bold, high-contrast "Gym-themed" interface with a biscuit-colored background.
* **User Planner:** Calculates personalized calorie targets based on age, height, weight, gender, and activity levels.
* **AI Food Analyzer:** Identify food items via image upload with a built-in safety filter to ensure only food-related images are processed.
* **Dynamic Diet Plan:** Generates a 5-item recommended food list and a 4-meal daily schedule.
* **Responsive Tables:** Dark-themed, high-readability tables for nutritional data.

---
# Screenshots of my Project

<img width="1919" height="831" alt="Screenshot 2026-03-20 131154" src="https://github.com/user-attachments/assets/a3ad70ed-669a-47b2-9cf3-0b273c838ea1" />




<img width="1919" height="829" alt="Screenshot 2026-03-20 131226" src="https://github.com/user-attachments/assets/bfa4146a-67c0-4c18-bbe4-c4f8debf19ef" />





<img width="1919" height="833" alt="Screenshot 2026-03-20 131331" src="https://github.com/user-attachments/assets/a6b0dfc8-ae3e-4140-86e2-20f753d2f928" />





<img width="1917" height="829" alt="Screenshot 2026-03-20 131359" src="https://github.com/user-attachments/assets/bc72158a-4a23-4e77-b313-195b24ea38bc" />






## 📂 Folder Structure
```bash
Smart-Gym-Diet-Planner/
│
├── app.py              # Main Streamlit application code
├── food.csv            # Dataset containing Food Names, Calories, and Macros
├── requirements.txt    # List of Python dependencies
└── README.md           # Project documentation
```

---

## 📄 File Descriptions
* **`app.py`**: The core logic of the application, including the CSS styling, BMR calculation engine, and the TensorFlow model integration.
* **`food.csv`**: The nutritional backbone. *Ensure this file has columns: Food, Calories, Protein, Fat, Carbs.*
* **`users.csv`**: Automatically generated file that stores usernames and passwords.
* **`requirements.txt`**: Contains the necessary libraries (`streamlit`, `pandas`, `tensorflow`, `Pillow`, `numpy`).

---

## 🛠 Steps to Run the Project

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Smart-Gym-Diet-Planner.git
cd Smart-Gym-Diet-Planner
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Prepare your Data
Ensure you have a `food.csv` file in the root directory with the following format:
| Food | Calories | Protein | Fat | Carbs |
| :--- | :--- | :--- | :--- | :--- |
| Banana | 89 | 1.1 | 0.3 | 23 |
| Chicken Breast | 165 | 31 | 3.6 | 0 |

### 5. Launch the App
```bash
streamlit run app.py
```

---


# Video of my Project





https://github.com/user-attachments/assets/3ac6568e-d1ad-450c-815a-cc666b8d6bc8












