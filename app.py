import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

# Load your dataset
df = pd.read_excel("Modified Coffee Shop Sale.xlsx")

# Create interactive filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df['transaction_date'].min())
end_date = st.sidebar.date_input("End Date", df['transaction_date'].max())
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
store_location = st.sidebar.multiselect("Store Location", df['store_location'].unique())
product_category = st.sidebar.multiselect("Product Category", df['product_category'].unique())
product_type = st.sidebar.multiselect("Product Type", df['product_type'].unique())

# Filter data based on user selections
filtered_df = df[(df['transaction_date'].dt.date >= start_date.date()) & (df['transaction_date'].dt.date <= end_date.date())]
if store_location:
    filtered_df = filtered_df[filtered_df['store_location'].isin(store_location)]
if product_category:
    filtered_df = filtered_df[filtered_df['product_category'].isin(product_category)]
if product_type:
    filtered_df = filtered_df[filtered_df['product_type'].isin(product_type)]



st.sidebar.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #f0f2f6;  
    color: #333;  
    padding: 20px;
}

.sidebar .sidebar-header {
    font-size: 20px;
    font-weight: bold;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)


# Title of the dataset 
st.markdown("<div class='custom-title'>Coffee Shop Sales Dashboard</div>", unsafe_allow_html=True)
# st.title("Coffee Shop Sales Dashboard")

# Display KPIs
# st.header("Key Performance Indicators")
total_sales = filtered_df['total_transaction'].sum()
avg_transaction_value = filtered_df['total_transaction'].mean()
total_transactions = filtered_df.shape[0]
top_products = filtered_df.groupby('product_id')['total_transaction'].sum().sort_values(ascending=False).head(5)
top_stores = filtered_df.groupby('store_id')['total_transaction'].sum().sort_values(ascending=False).head(5)


st.markdown("""
    <style>
    .custom-title {
        font-size: 3em;
        font-weight: bold;
        color: #1F618D;
        text-align: center;
        margin-top: 0;
        margin-bottom: 20px;
    }
    .custom-header {
        font-size: 2.5em;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin-top:20px;
        margin-bottom: 20px;
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
    }
    .custom-subheader {
        font-size: 1.8em;
        color: #6D6D6D;
        text-align: center;
        margin-bottom: 9px;
        font-style: sans serif;
        font-color:#0FECF5;
    }
    .metric-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        background-color: #f7f9fc;
        padding-top: 10px;
        padding-bottom:20px;
        border-radius: 8px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .metric-container:hover {
        transform: scale(1.05);
    }
    .metric-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #333;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #007bff;
    }
    </style>
""", unsafe_allow_html=True)

# Display metrics with style
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-container'><div class='metric-title'>Total Sales</div><div class='metric-value'>${total_sales:.2f}</div></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-container'><div class='metric-title'>Avg Transaction Value</div><div class='metric-value'>${avg_transaction_value:.2f}</div></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-container'><div class='metric-title'>Total Transactions</div><div class='metric-value'>{total_transactions}</div></div>", unsafe_allow_html=True)



# Temporal Trends
st.markdown("<div class='custom-header'>Temporal Trends</div>", unsafe_allow_html=True)
# st.header("Temporal Trends")

# Daily Sales
st.markdown("<div class='custom-subheader'>Daily Sales</div>", unsafe_allow_html=True)

fig = px.line(filtered_df, x="transaction_date", y="total_transaction")
st.plotly_chart(fig)

# weekly Sales
st.markdown("<div class='custom-subheader'>Weekly Sales</div>", unsafe_allow_html=True)
weekly_sales = filtered_df.groupby(pd.Grouper(key='transaction_date', freq='W')).sum()['total_transaction']
fig = px.line(weekly_sales, x=weekly_sales.index, y='total_transaction')
st.plotly_chart(fig)

# Sales by Day of Week

st.markdown("<div class='custom-subheader'>Day of Weeks Sales</div>", unsafe_allow_html=True)
# daily_sales = filtered_df.groupby('day')['total_transaction'].sum()
# fig, ax = plt.subplots(figsize=(10, 5))
# ax.plot(daily_sales.index, daily_sales.values, marker='o', color='b', linestyle='-', linewidth=2)
# ax.set_title("Daily Sales Trend")
# ax.set_xlabel("Date")
# ax.set_ylabel("Total Sales")
# st.pyplot(fig)


# Group the data by day and calculate total transactions
daily_sales = filtered_df.groupby('day')['total_transaction'].sum()
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=daily_sales.index, 
    y=daily_sales.values, 
    mode='lines+markers', 
    line=dict(color='blue', width=2),
    marker=dict(symbol='circle', size=6)
))
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales"
)
st.plotly_chart(fig)

st.markdown("<div class='custom-subheader'>Day of Weeks Sales</div>", unsafe_allow_html=True)
fig = px.bar(filtered_df, x="day_of_week", y="total_transaction")
st.plotly_chart(fig)

# Sales by Hour of Day
st.markdown("<div class='custom-subheader'>Hour of Day</div>", unsafe_allow_html=True)

fig = px.histogram(filtered_df, x="transaction_time(hr)")
st.plotly_chart(fig)

# Heatmap of Sales by Day and Hour
st.markdown("<div class='custom-subheader'>Heatmap of Sales by Day and Hour</div>", unsafe_allow_html=True)
heatmap_data = filtered_df.pivot_table(index='day_of_week', columns='transaction_time(hr)', values='total_transaction')
fig = px.imshow(heatmap_data,
                 x=heatmap_data.columns,
                 y=heatmap_data.index,
                 labels=dict(x="Hour", y="Day of Week", color="Total Sales"),
                 color_continuous_scale='RdBu')
st.plotly_chart(fig)

# Calculate total sales per month
st.markdown("<div class='custom-subheader'>Monthly Sales</div>", unsafe_allow_html=True)

monthly_sales = filtered_df.groupby('month_name')['total_transaction'].sum().reset_index()
# Plot line chart for monthly sales trends with month names
fig = px.line(monthly_sales, x='month_name', y='total_transaction',
              title="Monthly Sales Trend",
              labels={'month_name': 'Month', 'total_transaction': 'Total Sales'})

fig.update_xaxes(categoryorder='array', categoryarray=["January", "February", "March", "April", "May", "June",
                                                      "July", "August", "September", "October", "November", "December"])
st.plotly_chart(fig)



st.markdown("<div class='custom-header'>Product Performance</div>", unsafe_allow_html=True)

st.markdown("<div class='custom-subheader'>Top Selling Product</div>", unsafe_allow_html=True)
top_products = filtered_df.groupby('product_id')['total_transaction'].sum().sort_values(ascending=False).head(10)
fig = px.bar(top_products, x=top_products.index, y='total_transaction')
st.plotly_chart(fig)

st.markdown("<div class='custom-subheader'>Product Category Performance</div>", unsafe_allow_html=True)
fig = px.bar(filtered_df, x='product_category', y='total_transaction')
st.plotly_chart(fig)

st.markdown("<div class='custom-subheader'>Popularity of Product Categories</div>", unsafe_allow_html=True)
category_popularity = filtered_df['product_category'].value_counts().reset_index()
category_popularity.columns = ['product_category', 'count']
fig = px.pie(category_popularity, values='count', names='product_category',
             labels={'product_category': 'Product Category', 'count': 'Count'})

fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Popularity of Product Types</div>", unsafe_allow_html=True)
type_popularity = df['product_type'].value_counts().reset_index()
type_popularity.columns = ['product_type', 'count']
fig = px.pie(type_popularity, values='count', names='product_type',
             
             labels={'product_type': 'Product Type', 'count': 'Count'})

fig.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Product Category Distribution</div>", unsafe_allow_html=True)
fig = px.pie(filtered_df, values='total_transaction', names='product_category')
st.plotly_chart(fig)

st.markdown("<div class='custom-subheader'>Product Size Distribution</div>", unsafe_allow_html=True)
fig = px.pie(filtered_df, values='total_transaction', names='size')
st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Product Contribution to Sales</div>", unsafe_allow_html=True)
fig = px.treemap(df, path=['product_category', 'product_type'], values='total_transaction')
st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Unit Price VS Sales Volume</div>", unsafe_allow_html=True)
fig = px.scatter(filtered_df, x='unit_price', y='total_transaction')
st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Sales by Product Size</div>", unsafe_allow_html=True)
size_sales = filtered_df.groupby('size')['total_transaction'].sum()
fig = px.bar(size_sales.reset_index(),
             x='size',
             y='total_transaction',
             text='total_transaction')

fig.update_traces(textposition='outside')  
fig.update_layout(
    xaxis_title='Product Size',
    yaxis_title='Total Sales'
)
st.plotly_chart(fig)


# st.markdown("<div class='custom-subheader'>Total transaction Quantity in each month</div>", unsafe_allow_html=True)
# fig = px.histogram(df, x='month',
#                    title="Number of Transactions in Each Month",
#                    labels={'month': 'Month', 'count': 'Number of Transactions'},  
#                    category_orders={'month': ['January', 'February', 'March', 'April', 'May', 'June',
#                                                    'July', 'August', 'September', 'October', 'November', 'December']},
#                    orientation='h'
#                    )

# st.plotly_chart(fig)

st.markdown("<div class='custom-subheader'>Total Transaction Quantity each day of Month</div>", unsafe_allow_html=True)
fig = px.histogram(filtered_df, x='day',
                   
                   labels={'day': 'Day of the Month', 'count': 'Number of Transactions'},
                   nbins=31)  

st.plotly_chart(fig)



st.markdown("<div class='custom-header'>Store Performance</div>", unsafe_allow_html=True)


st.markdown("<div class='custom-subheader'>Sales By Store Location</div>", unsafe_allow_html=True)
fig = px.bar(filtered_df, x='store_location', y='total_transaction')
st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Percentage of Sales in Each Store</div>", unsafe_allow_html=True)
store_sales = filtered_df['store_location'].value_counts().reset_index()
store_sales.columns = ['store_location', 'num_sales']  
fig = px.pie(store_sales, values='num_sales', names='store_location',
             
             labels={'store_location': 'Store Location', 'num_sales': 'Number of Sales'},
             hole=0.3)  

st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Most Transaction Occure Time</div>", unsafe_allow_html=True)
# fig, ax = plt.subplots()
# sns.kdeplot(filtered_df['transaction_time(hr)'])
# st.pyplot(fig)


kde_data = filtered_df['transaction_time(hr)']
fig = ff.create_distplot([kde_data], group_labels=['Transaction Time (hr)'], show_hist=False, show_rug=False)
fig.update_layout(
    xaxis_title="Transaction Time (hr)",
    yaxis_title="Density"
)
st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Number of transaction by store location</div>", unsafe_allow_html=True)
fig = px.bar(filtered_df, x='store_location', y='transaction_qty')
st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Average Transaction Value by Store Location</div>", unsafe_allow_html=True)
avg_transaction_by_store = filtered_df.groupby('store_location')['total_transaction'].mean()
fig = px.bar(avg_transaction_by_store, x=avg_transaction_by_store.index, y='total_transaction')
st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Distribution of Product Categories Across Stores</div>", unsafe_allow_html=True)
store_category_count = filtered_df.groupby(['store_location', 'product_category']).size().reset_index(name='count')
fig = px.bar(store_category_count, x='store_location', y='count', color='product_category',
             labels={'store_location': 'Store Location', 'count': 'Number of Products Sold', 'product_category': 'Product Category'},
             barmode='stack')  
st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Transaction Quantity by Store and Product Category</div>", unsafe_allow_html=True)
store_transaction_qty = filtered_df.groupby(['store_location', 'product_category'])['transaction_qty'].sum().reset_index()
fig = px.bar(store_transaction_qty, y='store_location', x='transaction_qty', color='product_category',
             labels={'store_location': 'Store Location', 'transaction_qty': 'Transaction Quantity', 'product_category': 'Product Category'},
             orientation='h', 
             barmode='stack')
st.plotly_chart(fig)




st.markdown("<div class='custom-header'>Additional Insights and Visualization</div>", unsafe_allow_html=True)

st.markdown("<div class='custom-subheader'>Distribution of Total Transaction</div>", unsafe_allow_html=True)
fig = px.histogram(filtered_df, x='total_transaction', nbins=30,
                   color_discrete_sequence=['skyblue'])

fig.update_layout(
    xaxis_title='Transaction Total',
    yaxis_title='Frequency',
    bargap=0.1  
)
st.plotly_chart(fig)

st.markdown("<div class='custom-subheader'>Five Number Summary of Unit Price to check outlier</div>", unsafe_allow_html=True)
fig = px.box(filtered_df, y='unit_price',
             title="Five-Number Summary for Unit Price",
             labels={'unit_price': 'Unit Price'})

st.plotly_chart(fig)


st.markdown("<div class='custom-subheader'>Distribution of Unit Price</div>", unsafe_allow_html=True)
# fig, ax = plt.subplots(figsize=(10, 6))
# sns.kdeplot(filtered_df['unit_price'], shade=True, color="blue", ax=ax)
# ax.set_xlabel("Unit Price")
# ax.set_ylabel("Density")
# st.pyplot(fig)

kde_data = filtered_df['unit_price']
fig = ff.create_distplot([kde_data], group_labels=['Unit Price'], show_hist=False, colors=['blue'])
fig.update_layout(
    xaxis_title="Unit Price",
    yaxis_title="Density"
)

st.plotly_chart(fig)

