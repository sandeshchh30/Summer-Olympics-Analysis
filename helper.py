def get_list(df, col, isOverall):
    lst = sorted(df[col].dropna().unique())
    if isOverall:
        lst.insert(0, 'Overall')
    return lst

def fetch_medal_tally(country, year, df):
    df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if (country == 'Overall') & (year == 'Overall'):
        temp_df = df
    if (country == 'Overall') & (year != 'Overall'):
        temp_df = df[df['Year'] == year]
    if (country != 'Overall') & (year == 'Overall'):
        flag = 1
        temp_df = df[df['region'] == country]
    if (country != 'Overall') & (year != 'Overall'):
        temp_df = df[(df['region'] == country) & (df['Year'] == year)]

    if flag == 1:
        medal_tally = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze', 'Total']].sort_values('Year', ascending=False).reset_index()
    else:
        medal_tally = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze', 'Total']].sort_values('Gold', ascending=False).reset_index()

    return medal_tally

def get_data_over_time(df, col):
    regions_map = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    regions_map.rename(columns={'Year': 'Year', 'count': col}, inplace=True)

    return regions_map

def get_events_nations_over_time(df):
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pivot_table = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int)
    return pivot_table
    
def get_athlete_performance(df, sport):
    if sport != 'Overall':
        df = df[df['Sport'] == sport]
    df1 = (
        df.groupby(['Name', 'Sport', 'region'], as_index=False)
          .agg({'Total': 'sum'})
          .sort_values('Total', ascending=False)
    )

    df1 = df1.head(50)
    return df1.reset_index().drop('index', axis=1)

def get_country_excels(df, country):
    df = df[df['region'] == country]
    df = df.dropna(subset=['Medal'])
    temp_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'])
    pivot_table = temp_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype(int)
    return pivot_table

def get_top_athletes_country_wise(df, country):
    temp_df = df[df['region'] == country]
    temp_df = temp_df.dropna(subset=['Medal'])
    temp_df = (
        temp_df.groupby(['Name', 'Sport'], as_index=False)
          .agg({'Total': 'sum'})
          .sort_values('Total', ascending=False)
    )

    return temp_df.reset_index().drop('index', axis=1).head(10)

def get_age_kde(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    return [x1, x2, x3, x4]


def get_age_sports(df):
    temp_df = df
    temp_df['Sport'].dropna(inplace=True)
    sport_df = temp_df.groupby('Sport')['Gold'].sum().reset_index().sort_values('Gold', ascending=False).head(20)

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x = []
    name = []
    for sport in sport_df['Sport'].unique():
        x.append(athlete_df[(athlete_df['Sport'] == sport) & (athlete_df['Medal'] == 'Gold')]['Age'].dropna())
        name.append(sport)
    
    return x, name

def get_height_weight(df, sport):
    temp_df = df.drop_duplicates(subset=['Name', 'region'])
    temp_df['Medal'].fillna('No Medal', inplace=True)
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    return temp_df

def get_men_women_participation(df):
    temp_df = df.drop_duplicates(subset=['Name', 'region'])
    male = temp_df[temp_df['Sex'] == 'M'].groupby('Year')['ID'].count().reset_index()
    female = temp_df[temp_df['Sex'] == 'F'].groupby('Year')['ID'].count().reset_index()

    final =  male.merge(female, on='Year')
    final.rename(columns={'ID_x':'Men', 'ID_y':'Women'}, inplace=True)
    return final





