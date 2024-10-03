import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
bike_sharing_df = pd.read_csv('bike_rentals_df.csv')  # Change this to your dataset path

def plot_monthly_rentals(data, year):
    """Plot total bike rentals by month for the selected year."""
    monthly_rentals = data.groupby('mnth')['cnt'].sum()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_rentals.index, monthly_rentals, color='#72BCD4', marker="o", linewidth=2)
    ax.set_title(f'Total Bike Rentals in {year}', fontsize=14)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Number of Rentals', fontsize=12)
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)

    plt.tight_layout()
    return fig, monthly_rentals.sum()  # Return the figure and total rentals

def plot_monthly_temperature(data, year):
    """Plot average normalized temperature by month for the selected year."""
    monthly_temp = data.groupby('mnth')['temp'].agg(['mean', 'std'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_temp.index, monthly_temp['mean'], marker='o', color='blue', label='Mean Temperature')
    ax.fill_between(monthly_temp.index,
                    monthly_temp['mean'] - monthly_temp['std'],
                    monthly_temp['mean'] + monthly_temp['std'],
                    color='blue', alpha=0.2)

    ax.set_title(f'Average Monthly Normalized Temperature for {year}', fontsize=14)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_ylabel('Normalized Temperature', fontsize=12)
    ax.set_xticks(ticks=range(1, 13))
    ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    ax.legend()
    
    return fig, monthly_temp['mean'].mean()  # Return the figure and average temperature

def plot_seasonal_rentals(data):
    """Plot average bike rentals by season."""
    seasonal_rentals = data.groupby('season')['cnt'].mean()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(seasonal_rentals.index, seasonal_rentals, color=['green', 'orange', 'brown', 'blue'])
    ax.set_title('Average Bike Rentals by Season', fontsize=14)
    ax.set_xlabel('Season', fontsize=12)
    ax.set_ylabel('Average Number of Rentals', fontsize=12)
    ax.set_xticks(ticks=seasonal_rentals.index)
    
    return fig, seasonal_rentals.mean()  # Return the figure and average rentals by season

def plot_average_rentals_by_hour(data):
    """Plot average bike rentals by hour ."""
    byhour_df = data.groupby('hour_group')['cnt'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(y="cnt", x="hour_group", data=byhour_df, ax=ax)
    ax.set_title("Average Rentals by Hour", fontsize=15)
    ax.set_ylabel(None)
    ax.set_xlabel(None)

    return fig, byhour_df['cnt'].mean()  # Return the figure and average rentals by hour

# Filter by year selection
st.sidebar.title('Plase Select Year')
selected_year = st.sidebar.selectbox('Select Year:', options=[2011, 2012], index=0)

# Filter data for the selected year
df_filtered = bike_sharing_df[bike_sharing_df['yr'] == (1 if selected_year == 2012 else 0)]

# Create visualizations and metrics
st.header("Bike Rentals Monitoring")


st.subheader('Monthly Orders')
monthly_rentals_fig, total_rentals = plot_monthly_rentals(df_filtered, selected_year)
st.pyplot(monthly_rentals_fig)  # Display the plot in Streamlit
st.metric(label="Total Rentals", value=total_rentals)  # Display total rentals metric

monthly_temp_fig, avg_temp = plot_monthly_temperature(df_filtered, selected_year)
st.pyplot(monthly_temp_fig)  # Display the plot in Streamlit
st.metric(label="Average Temperature", value=f"{avg_temp:.2f}")  # Display average temperature metric

seasonal_rentals_fig, avg_seasonal_rentals = plot_seasonal_rentals(df_filtered)
st.pyplot(seasonal_rentals_fig)  # Display the plot in Streamlit
st.metric(label="Average Rentals per Season", value=f"{avg_seasonal_rentals:.2f}")  # Display average rentals metric

average_rentals_hour_fig, avg_hourly_rentals = plot_average_rentals_by_hour(df_filtered)
st.pyplot(average_rentals_hour_fig)  # Display the plot in Streamlit
st.metric(label="Average Rentals per Hour", value=f"{avg_hourly_rentals:.2f}")  # Display average rentals metric
