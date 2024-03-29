import streamlit as st
import time
import pandas as pd
from datetime import datetime
from peoplecounter import count_people

st.set_page_config(layout="wide")

# Initialize a DataFrame to store data
data = pd.DataFrame(columns=['Timestamp', 'People Count', 'Total Time (minutes)', 'Total Cost (€)'])

def reset_data():
    global data
    data = pd.DataFrame(columns=['Timestamp', 'People Count', 'Total Time (minutes)', 'Total Cost (€)'])

def main():
    global data  # Declare data as a global variable

    test = 1
    # Add widgets to the sidebar
    st.sidebar.header("Settings")
    hourly_wage = st.sidebar.number_input(label='Hourly wage', value=50)
    reset_button = st.sidebar.button("Reset Data")

    if reset_button:
        reset_data()


    with st.empty():
        while True:
            # Get current timestamp
            timestamp = datetime.now()

            # Call the function to count people
            people_count = count_people()
            last_three_zeros = data['People Count'].tail(3).eq(0).all()

            if last_three_zeros:
                reset_data()

            # Calculate the total time in meeting per minute
            if not data.empty:
                total_time = (timestamp - data.iloc[0]['Timestamp']).total_seconds() / 60
                total_cost = total_time * (people_count * hourly_wage / 60)
            else:
                total_time = 0
                total_cost = 0

            # Update the title with the dynamic value
            st.title(f"This meeting cost: {round(total_cost, 2)} €")

            # Append data to the DataFrame
            data = data.append({
                'Timestamp': timestamp,
                'People Count': people_count,
                'Total Time (minutes)': total_time,
                'Total Cost (€)': total_cost
            }, ignore_index=True)

            col1, col2, col3 = st.columns(3)

            # Calculate delta based on the previous row
            delta_people_count = data['People Count'].diff().iloc[-1] if len(data) > 1 else 0
            col1.metric("This meeting cost (€)", value=round(total_cost, 2), delta_color='inverse')
            col3.metric("People currently not working efficiently", value=round(people_count), delta=delta_people_count, delta_color='inverse')
            col2.metric("This meeting took (minutes)", value=round(total_time, 2))
            #col4.dataframe(data)

            # Sleep for a minute (adjust as needed)
            time.sleep(5)

if __name__ == "__main__":
    main()
