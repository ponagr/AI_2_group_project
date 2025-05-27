import streamlit as st
import plotly.express as px
import os
from google import genai
from google.generativeai.types import GenerationConfig
from google import generativeai as oldGenai
import os
import pandas as pd
import json
from dotenv import load_dotenv


load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_description(df):
    load_dotenv()
    oldGenai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    # current_df = df[["Occupation Field", "Headline", "Description"]] #.iloc[:10]

    # lägg in info till prompt för generell sammanställning för översikt
    prompt = f"""Skapa en tydlig beskrivning för jobb annonsen baserad på beskrivningen: {df["Description"]}, som beskriver arbetsuppgifter, krav, meriter och egenskaper.
    
    Plocka ut max 5 av dom nämnda krav och max 5 av nämnda meriterade/eftertraktade färdigheterna(om färre, se till att ta samma antal för båda),
    och ett sammanställt antal av dessa som efterfrågas i annonsen, detta ska enkelt kunna användas till en plot i en dashboard.
    
    Output ska vara i detta formatet enbart: 
    {{
        "sammanfattning": "sammanfattnings text",
        "krav": [erfarenhet1, erfarenhet2, ...],
        "antal krav": [summa erfarenhet1, erfarenhet2..],
        "meriterande": [meriterande1,meriterande2, ... ],
        "antal meriterande": [summa meriterande1,meriterande2..]
        
    }}
    """
    # prompt = f"""Du är en rekryterare inom {current_df["Occupation Field"]}.
    # Plocka ut max 5 av dom vanligast nämnda kraven och max 5 av dom vanligast nämnda meriterade/eftertraktade färdigheterna(annars samma antal för båda),
    # och ett sammanställt antal av dessa som efterfrågas i dessa jobbannonser {current_df["Description"]}, detta ska enkelt kunna användas till en plot i en dashboard
    # skriv även en sammanfattning av krav och meriter som du skriver ut för jobb fältet för att tydligt beskriva vad som sökt och är mest eftertraktat just nu enligt annonserna:

    # Output ska vara i detta formatet enbart: 

    # {{
    #     "sammanfattning": "sammanfattnings text",
    #     "krav": [erfarenhet1, erfarenhet2, ...],
    #     "antal krav": [summa erfarenhet1, erfarenhet2..],
    #     "meriterande": [meriterande1,meriterande2, ... ],
    #     "antal meriterande": [summa meriterande1,meriterande2..]
        
    # }}
    # """
    # skicka in prompt till gemini
    model = oldGenai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=GenerationConfig(
                temperature=0.0,         
                top_p=1.0,  # Säkerställer att sampling inte påverkas   #verkar inte göra skillnad
                top_k=1     # Tar bort variation)                       #verkar inte göra skillnad    
            )
        )
    response = model.generate_content(prompt)

    # städa response text från gemini
    cleaned = response.text.replace("\n", "").replace("```json", "")
    data = json.loads(cleaned)

    # strukturera upp datan i dfs för plots och en text-string för sammanfattning
    krav_df = pd.DataFrame({
        "Krav": data["krav"],
        "Antal": data["antal krav"]
    })
    merit_df = pd.DataFrame({
        "Krav": data["meriterande"],
        "Antal": data["antal meriterande"]
    })
    summary = data["sammanfattning"]

    # skriv ut sammanfattning och plots
    # print(summary)
    st.info(summary)
    col1,col2 = st.columns(2)
    fig1 = px.pie(krav_df, names="Krav", values="Antal", title="Sammanställning av krav på färdigheter för annonser")
    fig2 = px.pie(merit_df, names="Krav", values="Antal", title="Sammanställning av meriterande färdigheter för annonser")
    col1.plotly_chart(fig1)
    col2.plotly_chart(fig2)