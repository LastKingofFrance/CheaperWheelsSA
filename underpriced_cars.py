import pandas as pd
import streamlit as st

# Load dataset
df = pd.read_csv('webuycar.csv')

# Data preprocessing to calculate average price per make, model, year
avg_price = df.groupby(['Make', 'Model', 'Year'])['Price'].mean().reset_index()
avg_price.rename(columns={'Price': 'Avg_Price'}, inplace=True)

# Merge with the original dataframe to get the average price for each car
df = df.merge(avg_price, on=['Make', 'Model', 'Year'], how='left')

# Calculate the deviation from the average price
df['Price_Deviation'] = df['Avg_Price'] - df['Price']

# Filter underpriced cars
df['Underpriced'] = df['Price'] < df['Avg_Price']

# Streamlit UI
st.set_page_config(page_title="Cheaper Wheels SA: Finding the Best Deals for You", layout="wide")

# Custom CSS for better look
st.markdown("""
    <style>
    body {
        background-color: #1a1a1a;  /* Dark background */
        color: #e6e6e6;  /* Light text color for contrast */
        font-family: 'Arial', sans-serif;
    }
    .title {
        font-size: 2.5em;
        font-weight: bold;
        color: #f5a623; /* Animated color */
        text-align: center;
        padding: 20px;
        animation: color-change 5s infinite alternate;
    }
    @keyframes color-change {
        0% { color: #f5a623; }
        50% { color: #d4af37; }
        100% { color: #8e44ad; }
    }
    .container {
        text-align: center;
    }
    .logo {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 150px;
        margin-top: 20px;
    }
    .car-image {
        width: 180px;  /* Reduced size by 40% */
        border-radius: 10px;
    }
    .car-card {
        padding: 15px;
        margin: 10px;
        border: 1px solid #ddd;
        border-radius: 5px;
        background-color: #ffffff;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        color: #333; /* Darker text for the grid */
        transition: transform 0.3s ease-in-out;
    }
    .car-card:hover {
        transform: scale(1.05);
    }
    .car-card h4 {
        font-size: 1.1em;
        color: #ff7f50; /* A lively color for the car title */
    }
    .car-card p {
        font-size: 0.9em;
        color: #555;  /* Dark text color for description */
    }
    .button {
        margin-top: 20px;
        background-color: #1f77b4;  /* Button color */
        color: white;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        font-size: 1em;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .button:hover {
        background-color: #0d5b9f;
    }
    </style>
""", unsafe_allow_html=True)

# Display Logo
st.image(r"C:\Users\HP\Downloads\PythonProjects\CarPricing\carproject\carproject\spiders\logo.jpg", width=150)


# Title with a better description
st.markdown('<div class="title">Cheaper Wheels SA: Finding the Best Deals for You</div>', unsafe_allow_html=True)

# Filters
make_filter = st.selectbox('Select Make', ['All'] + list(df['Make'].unique()))
model_filter = st.selectbox('Select Model', ['All'] + list(df[df['Make'] == make_filter]['Model'].unique()))
condition_filter = st.selectbox('Select Condition', ['All', 'Vehicle in excellent condition', 'Vehicle is better than average', 'Normal wear and tear'])
location_filter = st.selectbox('Select Location', ['All'] + list(df['Dealer'].unique()))

# Filter the dataframe based on user input
filtered_df = df
if make_filter != 'All':
    filtered_df = filtered_df[filtered_df['Make'] == make_filter]
if model_filter != 'All':
    filtered_df = filtered_df[filtered_df['Model'] == model_filter]
if condition_filter != 'All':
    filtered_df = filtered_df[filtered_df['Condition'] == condition_filter]
if location_filter != 'All':
    filtered_df = filtered_df[filtered_df['Dealer'] == location_filter]

# Show underpriced cars (sorted by price deviation and limited to 36 per page)
underpriced_cars = filtered_df[filtered_df['Underpriced'] == True].sort_values(by='Price_Deviation', ascending=False)
underpriced_cars = underpriced_cars.head(36)

# Pagination for cars (12 cars per page)
page_size = 12
total_pages = len(underpriced_cars) // page_size + (1 if len(underpriced_cars) % page_size != 0 else 0)

# Select page (with Next Page button)
if 'page' not in st.session_state:
    st.session_state.page = 0

def next_page():
    if st.session_state.page < total_pages - 1:
        st.session_state.page += 1

# Show the "Next Page" button
st.button("Next Page", on_click=next_page, key="next_page_button")

# Slice cars based on the selected page
start_idx = st.session_state.page * page_size
end_idx = start_idx + page_size
cars_to_display = underpriced_cars.iloc[start_idx:end_idx]

# Display cars in a grid (4x3 layout)
columns = st.columns(4)

for i, car in cars_to_display.iterrows():
    with columns[i % 4]:
        st.markdown(f"""
        <div class="car-card">
            <img src="{car['Image Link']}" class="car-image"/>
            <h4>{car['Make']} {car['Model']} {car['Year']}</h4>
            <p>Mileage: {car['Mileage']} km</p>
            <p>Price: R{car['Price']}</p>
            <p>Condition: {car['Condition']}</p>
            <p>Price Deviation: R{car['Price_Deviation']:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
