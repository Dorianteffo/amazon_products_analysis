import streamlit as st 

st.set_page_config(page_title= "Amazon_product",
                    page_icon="🏷",
                    layout="wide")

st.title('📕About')
st.markdown('#')

st.markdown('### 💡Goal')
st.markdown("""
            The main objective of this project was to advise someone who wanted to start selling products on Amazon's E-commerce platform.                                                                                                            
            To do this, we have created this web application, to display the top 10 manufacturers on Amazon and their statistics: average rating, discount percentage, number of reviews, and main categories of products sold."""
            )


st.markdown('##')
st.markdown('### 🔎Methodology')
st.markdown(f"""
            This app uses a dataset from [kaggle](https://www.kaggle.com/datasets/lokeshparab/amazon-products-dataset) (updated 4 months ago).
            Since I don't have any skills in web scraping and data pipeline implementation yet, I couldn't build this app with real-time data. That's why I used the latest Amazon product data set available on Kaggle. 
            """)


st.markdown('##')
st.markdown("### ❓What's next")
st.markdown("""
            I will definitely go further with this project using real time data in the next months.
            """)


st.markdown('##')
st.markdown('### 🔗Links')
col1,col2,col3 = st.columns(3)
with col1 : 
    st.markdown(f'### 🐈[Github](https://github.com/Dorianteffo/amazon_products_analysis/tree/master)')
    st.write('Source code for project')

with col2 : 
    st.markdown(f'### 💹[Kaggle](https://www.kaggle.com/code/doriancurtis/amazon-products-analysis)')
    st.write('Notebook (EDA) and dataset')

with col3 : 
    st.markdown(f'### 🗞[Medium](https://medium.com/@dorianteffo)')
    st.write('For tips in data analysis')
