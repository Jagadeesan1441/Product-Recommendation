import streamlit as st
import pickle
import pandas as pd

# Load the recommended mobile data
with open('most_recommended_mobile.pkl', 'rb') as file:
    recommended_data = pickle.load(file)

# Mobile data dictionary
mobile_data = {
    "Mobile_brand": ["vivo", "Oneplus", "Motorola-edge", "Samsung", "Redmi", "Apple", "samsung", "ONEPLUS-nord", "Nothingphone"],
    "Model": ["vivo-t3-ultra", "oneplus-12r", "motorola-edge-50-neo", "samsung-galaxy-s24-ultra", "redmi-note-13-pro-5g", "Iphone15-plus", "Samsung Galaxy-s23", "Oneplus-nord-ce-3-lite-5g", "Nothing-phonr-2a-5g"],
    "Price": ["₹24,999", "₹27,999", "₹29,999", "₹1,24,999", "₹21,999", "₹89,999", "₹74,999", "₹19,999", "₹24,999"],
    "Rating": ["4.4", "4.5", "4.3", "4.8", "4.1", "4.7", "4.6", "4.2", "4.5"],
    "Images": [
        r'C:\Users\nsjag\Downloads\FINAL PRO\vivot3ultra.jpeg',
       r'C:\Users\nsjag\Downloads\FINAL PRO\oneplus12r.jpeg',
        r'C:\Users\nsjag\Downloads\FINAL PRO\motorola.jpeg',
        r"C:\Users\nsjag\Downloads\FINAL PRO\s24ultra.jpeg",
       r"C:\Users\nsjag\Downloads\FINAL PRO\redmi13pro.jpeg",
       r"C:\Users\nsjag\Downloads\FINAL PRO\Iphone 15 plus.jpeg",
        r"C:\Users\nsjag\Downloads\FINAL PRO\samsungs23jpeg.jpeg",
        r"C:\Users\nsjag\Downloads\FINAL PRO\oneplus nord.jpeg",
        r"C:\Users\nsjag\Downloads\FINAL PRO\nothing.jpeg"
    ]
}

# Convert the mobile data dictionary into a DataFrame
df1 = pd.DataFrame(mobile_data)

# Clean the 'Price' column by removing the ₹ symbol and commas, then convert to integer
df1['Price'] = df1['Price'].str.replace('₹', '').str.replace(',', '').astype(int)

# Ensure that the 'Rating' column is converted to float for proper comparison
df1['Rating'] = df1['Rating'].astype(float)

# Adjust the merge based on the correct column name (after inspection)
df1 = pd.merge(df1, recommended_data, left_on="Model", right_on="product_name", how="inner")

# Streamlit UI
st.title("Mobile Recommendation System")
st.subheader("Based on Sentiment Analysis from Reviews and Recommendation:")
st.sidebar.header("Filter Options")

# Dropdown for selecting mobile brands (with a unique key to prevent conflicts)
brandoption = df1["Model"].unique().tolist()
selected_brands = st.sidebar.multiselect("Select Brands:", options=brandoption, key="brand_select")

# Slider for price range selection
min_price, max_price = st.sidebar.slider("Price Range:", min_value=20000, max_value=150000, value=(20000, 150000), key="price_range")

# Slider for minimum rating selection
min_rating = st.sidebar.slider("Minimum Rating:", min_value=0.0, max_value=5.0, value=3.0, key="min_rating")

# Apply filters based on user selection
if selected_brands:
    filtered_data = df1[(df1["Price"] >= min_price) & (df1["Price"] <= max_price) & (df1["Rating"] >= min_rating)]
    filtered_data = filtered_data[filtered_data["Model"].isin(selected_brands)]
    st.write(f"Showing products for price between ₹{min_price} and ₹{max_price} with rating above {min_rating}:")

    # If no products match the filters, show a message
    if filtered_data.empty:
        st.write("No products match the criteria.")
    else:
        st.subheader(f"You selected: {', '.join(selected_brands)}")
        
        # Display filtered products
        for _, row in filtered_data.iterrows():
            st.subheader(f"{row['Model']}")
            st.image(row['Images'], width=200)
            st.write(f"Price: ₹{row['Price']}")
            st.write(f"Rating: {row['Rating']}")

            # Display the recommendation prompt based on sentiment analysis with custom color
            prompt = f"""
            <p style="color:#FF6347; font-size:18px;">
            Based on the sentimental analysis, we recommend the following mobile phone:
            <strong>Model</strong>: {row['Model']}<br>
            <strong>Average Compound</strong>: {row['avg_compound']:.2f}<br>
            <strong>Average Compound Sentiment</strong>: {row['avg_compound_sentiment']}<br>
            This mobile phone is highly recommended.
            </p>
            """
            st.markdown(prompt, unsafe_allow_html=True)
else:
    st.write("No brand selected yet.")
