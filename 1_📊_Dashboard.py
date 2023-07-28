#import libraries
import pandas as pd 
import streamlit as st 
import plotly.express as px
import numpy as np 
import module.cleaning as cl

st.set_page_config(page_title= "Amazon_product",
                    page_icon="🏷",
                    layout="wide"
                    )


#data cleaning 
df = pd.read_csv('Amazon-Products.csv')
df = cl.cleaning_data(df)


#title
st.title('📊Dashboard')
st.markdown('##')


#sidebar 
st.sidebar.write('# 🧬Filters')

#dashboard parameter
st.sidebar.write('## Dashboard parameter')
manufactur = st.sidebar.selectbox("Select a manufacturer:", 
                                    options = df['manufacturer'].value_counts().index
                                    )

df_selection = df.query(
    " manufacturer == @manufactur"
)

#subcategory parameter
st.sidebar.write('## Subcategory parameter')
subcategory_parameter = st.sidebar.selectbox('Select a category:',
                                             options = df_selection['main_category'].unique()
                                             )


#KPIs
total_revenue = round(df_selection['discount_price'].sum(),0)
avg_ratings = round(df_selection['ratings'].mean(),1)
star_rating = '⭐'* int(round(avg_ratings,0))
avg_discount = round(df_selection['discount_percentage'].mean()*100,2)

col1, col2, col3  = st.columns(3)
with col1 : 
    st.subheader('Total Sales:')
    st.subheader(f'US $ {total_revenue:,}')
with col2 : 
    st.subheader('Average Rating:')
    st.subheader(f'{avg_ratings} {star_rating} ')
with col3 : 
    st.subheader('Average Discount:')
    st.subheader(f'{avg_discount} %')


st.markdown('---')

# bar chart category sales
sales_by_category = df_selection.groupby('main_category',as_index=False)['discount_price'].sum()
fig_category_sales = px.bar(
    sales_by_category, x='main_category',
      y='discount_price', 
      template='simple_white'
      )
fig_category_sales.update_layout(title = "Sales by category",
                                 xaxis_title = "Category",
                                 yaxis_title = "Sales (US $)",
                                 plot_bgcolor="rgba(0,0,0,0)"
                                 )



# bar chart subcategory sales 
sales_by_subcategory = df.groupby(['main_category','sub_category'],as_index=False)['discount_price'].sum()
fig_subcategory_sales = px.bar(     sales_by_subcategory[sales_by_subcategory['main_category']==subcategory_parameter], 
                                    x='discount_price',
                                    y='sub_category',
                                    orientation = "h", 
                                    template='simple_white'
                                )
fig_subcategory_sales.update_layout(title = "Top subcategory",
                                 xaxis_title = "Sales (US $)",
                                 yaxis_title = "Subcategory",
                                 plot_bgcolor="rgba(0,0,0,0)"
                                 )



left1, right1= st.columns(2)
left1.plotly_chart(fig_category_sales)
right1.plotly_chart(fig_subcategory_sales)


st.markdown('#')


#distribution of price 
fig_distribution_price = px.box(df_selection, 
                                x='discount_price', 
                                template='simple_white',
                                hover_data = ['main_category']
                                )
fig_distribution_price.update_layout(title = 'Distribution of price', 
                                     xaxis_title='Discount price',
                                     plot_bgcolor="rgba(0,0,0,0)"
                                     )




#distribution of reviews
fig_distribution_reviews = px.histogram(df_selection,
                                        x='no_of_ratings',
                                        template = 'simple_white'
                                        )
fig_distribution_reviews.update_layout(title="Distribution of the number of reviews",
                                       xaxis_title = "Number of reviews",
                                       plot_bgcolor="rgba(0,0,0,0)")



left2, right2= st.columns(2)
left2.plotly_chart(fig_distribution_price)
right2.plotly_chart(fig_distribution_reviews)




