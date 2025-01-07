import streamlit as st
import pandas as pd
import helper
import preprocessor
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

st.set_page_config(layout="wide")

@st.cache_data
def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

df = load_data('Data/athlete_events.csv')
df = preprocessor.data_preprocessing(df)

st.sidebar.header("Olympics Analysis")
user_menu = st.sidebar.radio('Select an Option', ('Medal Tally', 'Overall Analysis', 'Country wise Analysis', 'Athlete wise Analysis'))

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")

    country = helper.get_list(df, 'region', True)
    years = helper.get_list(df, 'Year', True)
    selected_year = st.sidebar.selectbox('Select Year' , years)
    selected_country = st.sidebar.selectbox('Select Country' , country)

    specific_medal_tally = helper.fetch_medal_tally(selected_country, selected_year, df)
    if (selected_country == 'Overall') & (selected_year == 'Overall'):
        st.title("Overall Tally")
    if (selected_country == 'Overall') & (selected_year != 'Overall'):
        st.title("Overall Tally for year " + str(selected_year))
    if (selected_country != 'Overall') & (selected_year == 'Overall'):
        st.title(selected_country + " Overall Performance")
    if (selected_country != 'Overall') & (selected_year != 'Overall'):
        st.title(selected_country + " Performance in " + str(selected_year))

    st.table(specific_medal_tally)

if user_menu == 'Overall Analysis':
    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(df['Year'].nunique())
    with col2:
        st.header("Sports")
        st.title(df['Sport'].nunique())
    with col3:
        st.header("Hosts")
        st.title(df['City'].nunique())

    col1 , col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(df['Event'].nunique())
    with col2:
        st.header("Nations")
        st.title(df['region'].nunique())
    with col3:
        st.header("Athletes")
        st.title(df['Name'].nunique())


    st.title("Participating Nations Over Time")
    nations_over_time_df = helper.get_data_over_time(df, 'region')
    fig = px.line(nations_over_time_df, x='Year', y= 'region')
    st.plotly_chart(fig)

    st.title("Participating Events Over Time")
    nations_over_time_df = helper.get_data_over_time(df, 'Event')
    fig = px.line(nations_over_time_df, x='Year', y= 'Event')
    st.plotly_chart(fig)

    st.title("Participating Athletes Over Time")
    nations_over_time_df = helper.get_data_over_time(df, 'Name')
    fig = px.line(nations_over_time_df, x='Year', y= 'Name')
    st.plotly_chart(fig)

    st.title("Number of Events Over Time")
    table = helper.get_events_nations_over_time(df)
    fig, ax = plt.subplots(figsize=(20, 20))
    sns.heatmap(table, annot=True,ax=ax)
    st.pyplot(fig)

    st.title("Athletes Performance")
    sports = helper.get_list(df, 'Sport', True)
    selected_sport = st.selectbox("Select Sport", sports)
    perf = helper.get_athlete_performance(df, selected_sport)
    st.table(perf)


if user_menu == 'Country wise Analysis':
    # country_df = df.dropna(subset=['Medal'])
    country_df = df

    country = helper.get_list(country_df, 'region', False)
    selected_country = st.sidebar.selectbox("Select Country", country)


    ## Feature 1
    st.title(selected_country + " Medal Tally over the years")
    country_medal_tally = helper.get_country_medal_tally(country_df, selected_country)
    y = ['Gold', 'Silver', 'Bronze', 'Total']
    selected_y = st.selectbox("Select Y label", y)
    fig = px.line(country_medal_tally, x='Year', y=selected_y)
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title=selected_y + "  Medals",
    )
    st.plotly_chart(fig)


    ## Feature 2
    st.title(selected_country + " Excels in the following sport")
    table = helper.get_country_excels(country_df, selected_country)
    fig, ax = plt.subplots(figsize=(20, 15))
    sns.heatmap(table, annot=True,ax=ax)
    st.pyplot(fig)


    ## Feature 3
    st.title("Detailed Analysis")
    years = helper.get_list(df, 'Year', False)
    col1, col2 = st.columns([3.3, 0.7])
    with col1:
        selected_year = st.selectbox('Select Year', years)
    country_df = helper.get_detailed_country(df, selected_country, selected_year)
    with col2:
        full_table = st.button("Show Full Table", use_container_width=True)
    if full_table == False:
        st.table(country_df.head(15))
    if full_table:
        st.table(country_df)
    country_df = helper.get_detailed_country(df, selected_country, selected_year)


    ## Feature 4
    st.title(selected_country + " top 10 Athletes")
    top_athletes = helper.get_top_athletes_country_wise(df, selected_country)
    st.table(top_athletes.head(10))


    ## Feature 5
    st.title(selected_country + " top 10 Athletes Detailed Analysis")
    selected_athlete = st.selectbox("Select Athlete", top_athletes['Name'])
    temp_df = helper.get_athlete_details(df, selected_country, selected_athlete)
    st.table(temp_df)

if user_menu == 'Athlete wise Analysis':
    st.title("Distribution of Age")
    age_kde = helper.get_age_kde(df)
    fig = ff.create_distplot(age_kde,['Overall Age', 'Gold Medal', 'Silver Medal', 'Bronze Medal'], show_hist=False, show_rug=False)
    fig.update_layout(
        width=900,  # Set the width
        height=600,  # Set the height
        xaxis_title="Age",
        yaxis_title="Density",
    )
    st.plotly_chart(fig)


    st.title("Distribution of Age w.r.t sports (Gold Medalist)")
    lst , name = helper.get_age_sports(df)
    fig = ff.create_distplot(lst, name, show_hist=False, show_rug=False)
    fig.update_layout(
        width=900,  # Set the width
        height=600,  # Set the height
        xaxis_title="Age",
        yaxis_title="Density",
    )
    st.plotly_chart(fig)


    st.title("Height Weight Distribution")
    sports = helper.get_list(df, 'Sport', True)
    selected_sport = st.selectbox("Select Sport", sports)
    hw_df = helper.get_height_weight(df, selected_sport)
    fig = px.scatter(
        hw_df,
        x='Height',
        y='Weight',
        color='Medal',
        symbol='Sex',
        size=None,
        hover_data=['Name', 'region'],
        title='Height vs Weight Distribution'
    )
    st.plotly_chart(fig, use_container_width=True)


    st.title("Men Vs Women participation over the years")
    temp_df = helper.get_men_women_participation(df)
    fig = px.line(temp_df, x='Year', y=['Men', 'Women'])
    fig.update_layout(
        width=900,  # Set the width
        height=600,  # Set the height
        xaxis_title="year",
        yaxis_title="Participation",
    )
    st.plotly_chart(fig)