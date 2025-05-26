import plotly.express as px
import streamlit as st

# Enkel barplot med val från selectbox
def plot_df(df, x_column, y_column="Vacancies"):
    # drop rows with 'Ej Angiven' in column
    df = df[(df[x_column] != "Ej Angiven") & (df[x_column] != "Not Specified") & (df[x_column] != "Undefined")]
    col1, col2 = st.columns(2)
    bar = px.bar(df, y=y_column, x=x_column, color=x_column)
    pie = px.pie(df, values=y_column, names=x_column, color=x_column)
    if x_column == "Driver License" or x_column == "Experience Required":
        bar.update_xaxes(tickvals=[True, False], ticktext=["Krav", "Inte Krav"])
        pie.update_xaxes(tickvals=[True, False], ticktext=["Krav", "Inte Krav"])
    pie.update_layout(showlegend=False)

    col1.plotly_chart(bar, use_container_width=True)
    col2.plotly_chart(pie)


