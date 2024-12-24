# impression
## Student Preference Dashboard

## Overview
The **Student Preference Dashboard** is an interactive web application built with Streamlit to visualize and analyze survey data. It enables users to explore preferences among students, compare individual responses with overall trends, detect anomalies, and export filtered data for further analysis.

## Features

### 1. **Search and Filter**
- **Search by Name:** Quickly view individual student responses by selecting a name from the sidebar.
- **Trend Filters:**
  - Include specific choices to focus the analysis.
  - Exclude specific choices to refine results.

### 2. **Visualizations**
- **Bar Charts:** Display overall popularity of choices and individual comparisons.
- **Bubble Charts:** Show trends with bubble sizes proportional to choice counts.
- **Line Charts:** Compare individual preferences with overall trends dynamically.
- **Heatmaps:** Visualize alignment between individual and overall preferences.

### 3. **Anomaly Detection**
- Detect rare choices based on a customizable threshold (e.g., choices selected by very few students).
- Display anomalies in a bar chart for easy interpretation.

### 4. **Data Export**
- Export filtered data as a CSV file directly from the sidebar for offline analysis.

### 5. **Insights and Summary**
- Display key insights, including:
  - Top choice for the selected student.
  - Most popular choice overall.
- Provide a survey summary with total students, unique choices, and the most popular choice.

## Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Dependencies**
   Ensure you have Python 3.10 or higher and the required libraries:
   ```bash
   pip install streamlit pandas plotly
   ```

3. **Run the Application**
   ```bash
   streamlit run student_dashboard.py
   ```

4. **Place Your Data Files**
   Ensure the following CSV files are in the same directory:
   - `impression1.csv`
   - `impression2.csv`
   - `fun_activity_interactive_-_20_12_2024__responses__-_form_responses_1 (1).csv`

## Usage

1. Open the dashboard in your browser using the URL provided after running the Streamlit app.
2. Use the sidebar to search for a student, apply filters, or export data.
3. View dynamic visualizations and insights for selected preferences.

## Customization

- **Data Columns:** Update the `columns_to_analyze` variable to adjust which columns are included in the analysis.
- **Anomaly Detection Threshold:** Customize the rare choice threshold via the slider in the sidebar.
- **Data Files:** Replace the default CSV files with your own datasets (ensure they have similar structures).

## Contributing
Feel free to fork this repository and submit pull requests to improve the dashboard. Suggestions and feedback are welcome!

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please reach out to the project maintainer.

