import streamlit as st
import plotly.express as px
import pandas as pd

@st.cache_data
def get_data_from_excel():
    #path = "c:/Users/user/Downloads/supermarkt_sales.xlsx"
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine= 'openpyxl',
        sheet_name = "Sales",
        skiprows = 3,
        usecols = 'B:R',
        nrows = 1000,
    )

    df["hour"] = pd.to_datetime(df["Time"],format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()

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

#st.dataframe(df_selection)

# Main page
st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(),1)
star_raiting = ":star:" * int(round(average_rating,0))
average_sale_by_transaction = round(df_selection["Total"].mean(),2)


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

# plot the barchart
sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum(numeric_only=True)[["Total"]].sort_values(by='Total')
)


fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation = "h",
    title = "<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"]* len(sales_by_product_line),
    template="plotly_white",
)

#sales per hour
sales_by_hour = df_selection.groupby(by=["hour"]).sum(numeric_only=True)[["Total"]]
fig_hourly_sale = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y='Total',
    title = "<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"]* len(sales_by_hour),
    template="plotly_white",
)

left_plot, right_plot = st.columns(2)
left_plot.plotly_chart(fig_product_sales,use_container_width = True)
right_plot.plotly_chart(fig_hourly_sale, use_container_width = True)

hide_st_style = """ 
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style,unsafe_allow_html=True)

st.dataframe(df_selection.head(5))
