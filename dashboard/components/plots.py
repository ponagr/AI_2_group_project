import plotly.express as px

# Enkel barplot med val från selectbox
def barplot_df(df, x_column, y_column="Vacancies", bar_ammount = 5):
    # drop rows with 'Ej Angiven' in column
    df = df[(df[x_column] != "Ej Angiven") & (df[x_column] != "Not Specified") & (df[x_column] != "Undefined")]
    fig = px.bar(df.head(bar_ammount), y=y_column, x=x_column, color=x_column)
    fig.update_layout(showlegend=False)
    if x_column == "Driver License" or x_column == "Experience Required":
        fig.update_layout(yaxis_title="Krav på körkort")
        fig.update_xaxes(tickvals=[True, False], ticktext=["Ja", "Nej"])
    return fig