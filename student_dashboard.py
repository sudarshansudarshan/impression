import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load datasets
file1_path = 'impression1.csv'
file2_path = 'impression2.csv'
file3_path = 'fun_activity_interactive_-_20_12_2024__responses__-_form_responses_1 (1).csv'

df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)
df3 = pd.read_csv(file3_path)

# Combine datasets
df_combined = pd.concat([df1, df2, df3], ignore_index=True)

# Clean data
columns_to_analyze = [col for col in df_combined.columns if 'Choose your pick' in col]
choices_df = df_combined[['Name'] + columns_to_analyze]

# Flatten and count preferences for popularity analysis
popularity_counts = choices_df.melt(id_vars=['Name'], value_name='Choice')['Choice'].value_counts().reset_index()
popularity_counts.columns = ['Choice', 'Count']

# Streamlit App
st.title("Student Preference Dashboard")

# Sidebar for search by name and trends
name_list = df_combined['Name'].dropna().unique()
selected_name = st.sidebar.selectbox("Search by Name:", name_list)

# Filter for trends with inclusion and exclusion
trending_filter_include = st.sidebar.multiselect("Include Choices for Trends:", options=popularity_counts['Choice'], default=None)
trending_filter_exclude = st.sidebar.multiselect("Exclude Choices for Trends:", options=popularity_counts['Choice'], default=None)

filtered_popularity = popularity_counts
if trending_filter_include:
    filtered_popularity = filtered_popularity[filtered_popularity['Choice'].isin(trending_filter_include)]
if trending_filter_exclude:
    filtered_popularity = filtered_popularity[~filtered_popularity['Choice'].isin(trending_filter_exclude)]

# Filter data for selected name
name_data = choices_df[choices_df['Name'] == selected_name]

# Display name-specific choices
st.header(f"Survey Responses for {selected_name}")
if not name_data.empty:
    st.write(name_data)
else:
    st.write("No responses found for this name.")

# Popularity feedback with filters
st.header("Overall Popularity of Choices")
popularity_chart = px.bar(filtered_popularity, x='Choice', y='Count', title="Popularity of Choices", text='Count',
                           color='Count', color_continuous_scale='Viridis')
popularity_chart.update_layout(xaxis_title="Choices", yaxis_title="Number of Students",
                                template='plotly_white', title_x=0.5)
st.plotly_chart(popularity_chart)

# Comparison of student's choices with overall trends
st.header(f"How {selected_name}'s Choices Align with General Trends")
if not name_data.empty:
    student_choices = name_data.melt(id_vars=['Name'], value_name='Choice')['Choice'].dropna()
    student_popularity = filtered_popularity[filtered_popularity['Choice'].isin(student_choices)]

    # Comparison Chart
    comparison_chart = px.bar(student_popularity, x='Choice', y='Count', color='Choice',
                               title=f"Comparison of {selected_name}'s Choices with Popularity", text='Count',
                               color_discrete_sequence=px.colors.qualitative.Bold)
    comparison_chart.update_layout(xaxis_title="Choices", yaxis_title="Number of Students",
                                   template='plotly_white', title_x=0.5)
    st.plotly_chart(comparison_chart)

    # Add Bubble Chart for Trends Comparison
    bubble_chart = px.scatter(filtered_popularity, x='Choice', y='Count', size='Count', color='Choice',
                              title="Bubble Chart of Trends by Choice", size_max=60)
    bubble_chart.update_layout(xaxis_title="Choices", yaxis_title="Count", template='plotly_white', title_x=0.5)
    st.plotly_chart(bubble_chart)

    # Add Line Chart for Trend Alignment
    st.header("Line Chart of Trends")
    trend_line_data = student_popularity.merge(filtered_popularity, on='Choice', suffixes=('_Student', '_Overall'))
    line_chart = px.line(trend_line_data, x='Choice', y=['Count_Student', 'Count_Overall'],
                         title="Line Chart: Student vs Overall Trends", labels={'value': 'Count', 'variable': 'Source'})
    line_chart.update_layout(xaxis_title="Choices", yaxis_title="Popularity", template='plotly_white', title_x=0.5)
    st.plotly_chart(line_chart)

    # Add Heatmap for Choices Comparison
    st.header("Heatmap of Choices Alignment")
    heatmap_data = filtered_popularity.merge(student_popularity, on='Choice', how='outer', suffixes=('_Overall', '_Student')).fillna(0)
    heatmap = go.Figure(data=go.Heatmap(
        z=[heatmap_data['Count_Overall'], heatmap_data['Count_Student']],
        x=heatmap_data['Choice'],
        y=['Overall Popularity', f"{selected_name}'s Popularity"],
        colorscale='Viridis'))
    heatmap.update_layout(title="Heatmap of Overall vs. Student's Popularity", xaxis_title="Choices", yaxis_title="Category")
    st.plotly_chart(heatmap)

    # Add Comparison Table
    st.header("Detailed Comparison Table")
    comparison_table = student_popularity.sort_values(by='Count', ascending=False)
    st.dataframe(comparison_table)
else:
    st.write("No specific comparison available due to missing data.")

# Export Filtered Data
st.sidebar.header("Export Data")
if st.sidebar.button("Export Filtered Data"):
    try:
        filtered_data = filtered_popularity.merge(choices_df.melt(id_vars=['Name'], value_name='Choice'), how='outer', on='Choice')
        filtered_data.to_csv("filtered_data.csv", index=False)
        st.sidebar.success("Filtered data exported as 'filtered_data.csv'.")
    except KeyError as e:
        st.sidebar.error(f"Error exporting data: {e}")

# Enhanced Anomaly Detection
st.header("Enhanced Anomaly Detection")
rare_choices_threshold = st.sidebar.slider("Set Rare Choice Threshold (Count <=):", min_value=1, max_value=5, value=1)
anomalies = popularity_counts[popularity_counts['Count'] <= rare_choices_threshold]
if not anomalies.empty:
    st.write(f"The following choices were selected by {rare_choices_threshold} or fewer students:")
    st.write(anomalies)
    anomaly_chart = px.bar(anomalies, x='Choice', y='Count', title="Anomaly Chart", text='Count',
                            color='Count', color_continuous_scale='Reds')
    anomaly_chart.update_layout(xaxis_title="Choices", yaxis_title="Count", template='plotly_white', title_x=0.5)
    st.plotly_chart(anomaly_chart)
else:
    st.write("No anomalies detected based on the selected threshold.")

# Insights Section
st.header("Insights")
if not name_data.empty:
    top_choice = name_data.melt(id_vars=['Name'], value_name='Choice')['Choice'].dropna().iloc[0]
    st.write(f"- {selected_name}'s top choice: {top_choice}")
    st.write(f"- Most popular choice overall: {popularity_counts.iloc[0]['Choice']} with {popularity_counts.iloc[0]['Count']} votes.")
else:
    st.write("No specific insights available due to missing data.")

# Survey Summary
st.header("Survey Summary")
st.write(f"Total Students: {len(df_combined['Name'].dropna().unique())}")
st.write(f"Total Unique Choices: {len(popularity_counts)}")
st.write(f"Most Popular Choice: {popularity_counts.iloc[0]['Choice']} ({popularity_counts.iloc[0]['Count']} selections)")
