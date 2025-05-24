import plotly.express as px
import streamlit as st

# Enkel barplot med val från selectbox
def barplot_df(df, x_column, y_column="Vacancies", bar_ammount = 5):
    # drop rows with 'Ej Angiven' in column
    df = df[(df[x_column] != "Ej Angiven") & (df[x_column] != "Not Specified") & (df[x_column] != "Undefined")]
    fig = px.bar(df.head(bar_ammount), y=y_column, x=x_column, color=x_column)
    fig.update_layout(showlegend=False)
    if x_column == "Driver License" or x_column == "Experience Required":
        fig.update_layout(yaxis_title="Krav på körkort")
        fig.update_xaxes(tickvals=[True, False], ticktext=["Ja", "Nej"])
    st.plotly_chart(fig)

def lineplot_df(df, x_column="Publication Date", y_column="Vacancies", bar_ammount = 5, color_column=None):
    if color_column:
        # drop rows with 'Ej Angiven' in column
        df = df[(df[x_column] != "Ej Angiven") & (df[x_column] != "Not Specified") & (df[x_column] != "Undefined")]
        
        top_categories = df[color_column].value_counts().nlargest(bar_ammount).index
        df = df[df[color_column].isin(top_categories)]

    fig = px.line(df, x=x_column, y=y_column, color=color_column)
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig)

def pieplot_df(df, x_column, y_column="Vacancies", bar_ammount = 5):
    # drop rows with 'Ej Angiven' in column
    df = df[(df[x_column] != "Ej Angiven") & (df[x_column] != "Not Specified") & (df[x_column] != "Undefined")]
    fig = px.pie(df.head(bar_ammount), values=y_column, names=x_column)
    fig.update_traces(textposition='inside', textinfo='percent')
    st.plotly_chart(fig)