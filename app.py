import streamlit as st
import datetime as dt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('new.csv')


st.set_page_config(layout="wide")
st.markdown('<style>div.block.container{padding-top:.5rem;}</style>',unsafe_allow_html=True)
html_title  = """
                <style>
                .title-test {
                font-weight : bold;
                padding : 10px;
                border-radius : 6px;
                }
                </style>
                <center><h1 class="title-test">Github Analysis Dashboard Streamlit</h1></center>
              """
st.markdown(html_title, unsafe_allow_html = True)
col1,col2 = st.columns([0.3 , 0.6])

with col1:
    
    df = df.dropna(subset=['primary_language'])  
    languages = df['primary_language'].unique()
    selected_language = st.selectbox("Filter Repository By languages", options=languages)

    filtered_data_language = df[df['primary_language'] == selected_language]

    st.write(f"Repositories filtered by language: **{selected_language}**")
    st.write(filtered_data_language[['name', 'stars_count']])

with col2:
    if not filtered_data_language.empty:
        top_starred = filtered_data_language.nlargest(10, 'stars_count')
        sns.set_theme(style="darkgrid")
        fig, ax = plt.subplots()
        sns.barplot(y='stars_count', x='name', data=top_starred, ax=ax , )
        ax.set_title(f'Top 10 Most Starred Repositories in {selected_language}')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')  # Rotate x labels for better readability
        st.pyplot(fig)
    else:
        st.write("No repositories match the search criteria.")


col3 , col4 = st.columns([0.3 , 0.6])


with col3:
    
    search_name = st.text_input("Search Repository by Name")

    # Filter data based on search query
    filtered_data = filtered_data_language[filtered_data_language['name'].str.contains(search_name, case=False)]
    if not filtered_data.empty :
        top_starred = filtered_data.nlargest(10, 'stars_count')
        st.write(f"Repositories filtered by Name: **{search_name}**")
        st.write(top_starred[['name', 'stars_count' , "commit_count"]])
        
    else:
        st.write("No repositories match the search criteria.")

with col4:
    language_count = df['primary_language'].value_counts().head(10)

    fig, ax = plt.subplots()
    sns.barplot(y=language_count.values, x=language_count.index, ax=ax)
    ax.set_title('Top 10 Primary Languages Used in Repositories')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)


col5 , col6 = st.columns([0.5 , 0.5])

with col5:
    top_starred = df.nlargest(10, 'stars_count')

    fig, ax = plt.subplots()
    sns.barplot(x='stars_count', y='name', data=top_starred, ax=ax)
    ax.set_title('Top 10 Most Starred Repositories')
    st.pyplot(fig)

with col6:
    df['created_at'] = pd.to_datetime(df['created_at'])

    # Repositories Created Over Time
    df['year_created'] = df['created_at'].dt.year
    yearly_creation = df['year_created'].value_counts().sort_index()

    fig, ax = plt.subplots()
    yearly_creation.plot(kind='line', ax=ax)
    ax.set_title('Representation Of Repositories Created Over Time')
    st.pyplot(fig)


