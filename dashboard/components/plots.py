import plotly.express as px

# Enkel barplot med val från selectbox
def barplot_df(df, column, bar_ammount = 5):
    return px.bar(df.head(bar_ammount), y="Vacancies", x=column, color=column)