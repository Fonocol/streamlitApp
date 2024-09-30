import streamlit as st
import plotly.express as px
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
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

# Filter the DataFrame based on the selections
df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender"
)

# Main page layout
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

# KPIs (Key Performance Indicators)
total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_raiting = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Total"].mean(), 2)

# Display KPIs
left_col, middle_col, right_col = st.columns(3)
with left_col:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_col:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_raiting}")
with right_col:
    st.subheader("Avg Sale per Transaction:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("---")

# Visualization 1: Sales by Product Line
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum(numeric_only=True)[["Total"]].sort_values(by="Total")
)

fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)

# Visualization 2: Sales by Hour
sales_by_hour = df_selection.groupby(by=["hour"]).sum(numeric_only=True)[["Total"]]

fig_hourly_sale = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)

# Layout for the charts
left_plot, right_plot = st.columns(2)
left_plot.plotly_chart(fig_product_sales, use_container_width=True)
right_plot.plotly_chart(fig_hourly_sale, use_container_width=True)

# Add a map of sales per city (Optional improvement)
if st.sidebar.checkbox("Show Sales Map by City"):
    sales_by_city = df_selection.groupby(by="City").sum(numeric_only=True)[["Total"]]
    
    # Adding a dummy latitude and longitude for demonstration
    city_coords = {
        'Yangon': [16.8661, 96.1951],
        'Mandalay': [21.9162, 96.0844],
        'Naypyitaw': [19.7633, 96.0785]
    }
    
    sales_by_city["lat"] = sales_by_city.index.map(lambda city: city_coords[city][0])
    sales_by_city["lon"] = sales_by_city.index.map(lambda city: city_coords[city][1])

    fig_map = px.scatter_mapbox(
        sales_by_city,
        lat="lat",
        lon="lon",
        size="Total",
        zoom=5,
        mapbox_style="carto-positron",
        title="<b>Sales by City</b>",
        size_max=15,
    )
    st.plotly_chart(fig_map, use_container_width=True)

# Hide Streamlit style
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Display filtered data (Optional)
if st.sidebar.checkbox("Show Data Table"):
    st.dataframe(df_selection.head(10))
