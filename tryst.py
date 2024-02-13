import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

# Predefined list of daily tasks
daily_tasks = [
    "Morning Workout or walk",
    "Deep work learning AI and Data Science",
    "Work",
    "Eat in a calorie deficit/ Nutritional dense",
    "Weight training",
    "Read/ learn something new"
]

# Function to calculate the number of weeks in a month
def get_weeks_in_month(year, month):
    import calendar
    weeks = calendar.monthcalendar(year, month)
    return len(weeks)

# Function to display the page
def display_page(tasks, filename):
    st.title("My Trajectory app")
    st.write("This app is to track your daily objectives and provide your trajectory")

    # Load historical data from CSV file or create new DataFrame if file does not exist
    try:
        historical_data = pd.read_csv(filename)
    except FileNotFoundError:
        historical_data = pd.DataFrame(columns=["Date", "Task"])

    # Initialize a list to store tasks completed for each day
    task_counts = {day: 0 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    st.write("Daily Tasks:")
    for index, task in enumerate(tasks):
        # Display tasks
        if st.checkbox(task, key=f"checkbox_{index}", value=task in historical_data["Task"].values):
            # Record task when checkbox is checked
            today = datetime.now().strftime("%A")
            task_counts[today] += 1

    # Convert task counts dictionary to DataFrame and sort days of the week
    data_agg = pd.DataFrame(list(task_counts.items()), columns=["Date", "Task"])
    custom_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data_agg["Date"] = pd.Categorical(data_agg["Date"], categories=custom_order, ordered=True)
    data_agg = data_agg.sort_values("Date")

    # Save historical data to CSV file
    data_agg.to_csv(filename, index=False)

    # Display bar plot with line
    st.write("Bar plot of task increments:")
    if not data_agg.empty:
        # Create Altair bar chart
        bars = alt.Chart(data_agg).mark_bar(color="#39ff14").encode(
            x=alt.X("Date:O", title="Day of the Week", sort=custom_order),
            y=alt.Y("Task:Q", title="Points", scale=alt.Scale(domain=[0, 6]))
        ).properties(
            width=600,
            height=300
        )

        # Add a line on top of the bars representing the total points
        line = alt.Chart(data_agg).mark_rule(color="red").encode(
            y="sum(Task):Q",
            size=alt.value(2)
        )

        # Display Altair chart with bars and line
        st.altair_chart(bars + line, use_container_width=True)

        # Calculate weekly efficiency
        weekly_points = data_agg["Task"].sum()
        total_possible_points = len(daily_tasks) * 7
        weekly_efficiency = (weekly_points / total_possible_points) * 100
        st.write(f"Weekly Efficiency: {weekly_efficiency:.2f}%")

    # Month selection filter
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    selected_month = st.selectbox("Select Month", months)

    # Week selection filter
    year = datetime.now().year
    month_index = months.index(selected_month) + 1  # Month index starts from 1
    weeks_in_month = get_weeks_in_month(year, month_index)
    weeks = [f"Week {week}" for week in range(1, weeks_in_month + 1)]
    selected_week = st.selectbox("Select Week", weeks)

    # Calculate monthly efficiency based on the selected month
    # Additional logic for month and week selection can be added here

    # Display monthly efficiency graph
    st.write("Monthly Efficiency:")
    # Additional graph for monthly efficiency can be added here

# Display the page
display_page(daily_tasks, "trajectory_data.csv")

































