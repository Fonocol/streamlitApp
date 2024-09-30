import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine='openpyxl',
        sheet_name="Sales",
        skiprows=3,
        usecols='B:R',
        nrows=1000,
    )

    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

# Sidebar filters
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["City"].unique(),
    default=df["City"].unique()[0]
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()[0]
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()[0]
)

df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# Main page
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_raiting = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

left_col, middle_col, right_col = st.columns(3)
with left_col:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_col:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_raiting}")
with right_col:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")

# Plot sales by product line using matplotlib
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum(numeric_only=True)[["Total"]].sort_values(by='Total')
)

# Plot the bar chart using matplotlib
fig, ax = plt.subplots()
ax.barh(sales_by_product_line.index, sales_by_product_line["Total"], color="#0083B8")
ax.set_xlabel("Total Sales")
ax.set_title("Sales by Product Line")
st.pyplot(fig)

# Plot sales per hour using matplotlib
sales_by_hour = df_selection.groupby(by=["hour"]).sum(numeric_only=True)[["Total"]]

# Plot the bar chart using matplotlib
fig, ax = plt.subplots()
ax.bar(sales_by_hour.index, sales_by_hour["Total"], color="#0083B8")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Total Sales")
ax.set_title("Sales by Hour")
st.pyplot(fig)

# Hide streamlit style
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Display data
st.dataframe(df_selection.head(5))
