import streamlit as st
import plotly.express as px
import os
from google import genai
# from google.generativeai.types import GenerationConfig
# from google import generativeai as oldGenai
import os
import pandas as pd
import json
from dotenv import load_dotenv


# skapar en tabell med sammanfattad analys på vald dataframe för tydlig överblick med hjälp av gemini llm
def overview_description(df, choice):
    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    if choice == "Published today":
        prompt = f"""
            Jag har filtrerat jobbannonser som publicerats idag:
            {df[["Salary Description", "Duration", "Working Hours Type", "Driver License", "Experience Required"]]}

            Analysera dessa annonser och ge mig:
            1. En översikt över dagens trender - vilka yrken, arbetsfält eller sektorer är mest representerade? {df[["Occupation Field", "Occupation Group", "Occupation"]]}
            2. Några arbetsgivare som sticker ut. {df[["Employer Workplace", "Employer Name"]]}
            3. Intressanta formuleringar i rubriker eller beskrivningar som verkar extra engagerande. {df[["Headline", "Description"]]}
            4. Om något sticker ut geografiskt eller branschmässigt. {df[["Workplace City", "Workplace Region"]]}
            5. Övrigt som kan vara intressant(valfritt).
            
            Använd konkreta exempel om möjligt, och håll det lättläst.
            
            Jag vill ha output i tabellformat likt detta:
            
            Panelformat Sammanfattning:
            Element	Beskrivning
            Dominerande sektor	Hotell, Restaurang, Storhushåll
            Vanligaste yrken	Köksbiträde, Kock (alla typer), Servitör/Servitris
            Anställningsform	Heltid (vanligast), Deltid (förekommer frekvent inom restaurang)
            Erfarenhet	Ofta ett krav, men varierar beroende på tjänst.
            Körkort	Krävs för vissa tjänster som Taxiförare, Distributionsförare och en köksbiträde.
            Potentiellt intressant	"Kock, à la carte" kan indikera en mer specialiserad roll.
            Branschfokus	Starkt fokus på Hotell/Restaurang (kan vara säsongsbetonat).
        """
    else:
        prompt = f"""
            Jag har filtrerat ut jobbannonser där sista ansökningsdag är idag: 
            {df[["Description", "Salary Description", "Duration", "Working Hours Type", "Driver License", "Experience Required"]]}

            Ge mig en kort sammanfattning av:
            1. Vilka typer av jobb man bör prioritera att söka idag.
            2. Vilka arbetsgivare som sticker ut. {df[["Employer Workplace", "Employer Name"]]}
            3. Om det finns någon specifik ort eller yrkesgrupp med många annonser. {df["Workplace City"]}
            4. Om det finns någon specifik yrkesgrupp eller yrke med många annonser. {df[["Occupation Field", "Occupation Group", "Occupation"]]}
            5. Några exempel på intressanta annonser (valfritt).

            Använd konkreta exempel om möjligt, och håll det lättläst.
            
            Jag vill ha output i tabellformat likt detta:
            
            Panelformat Sammanfattning:
            Element	Beskrivning
            Dominerande sektor	Hotell, Restaurang, Storhushåll
            Vanligaste yrken	Köksbiträde, Kock (alla typer), Servitör/Servitris
            Anställningsform	Heltid (vanligast), Deltid (förekommer frekvent inom restaurang)
            Erfarenhet	Ofta ett krav, men varierar beroende på tjänst.
            Körkort	Krävs för vissa tjänster som Taxiförare, Distributionsförare och en köksbiträde.
            Potentiellt intressant	"Kock, à la carte" kan indikera en mer specialiserad roll.
            Branschfokus	Starkt fokus på Hotell/Restaurang (kan vara säsongsbetonat).
        """
    
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    
    return response.text


# kladd och potentiella prompts att använda i dashboard
def prompts(df):
    if len(df)>1:
        prompt1 = f"""Vilka kompetenser och färdigheter efterfrågas i annonserna? {df}
        """
    else:
        prompt1 = f"""Vilka kompetenser och färdigheter efterfrågas i annonsen? {df}
        """
    
    # få guidning och rekomendationer av gemini
    skills = "Har C-körkort, är fysiskt stark, bra på motorer, problemlösning"  # från en textbox efter filtrering
    if len(df)>1:
        prompt = f"""Dessa är mina styrkor/färdigheter: {skills}. Hur bra passar dessa jobb mig?
        Rangordna dessa och rekommendera det bästa jobbet enligt {df}.
        """
    else:
        prompt2 = f"""Dessa är mina styrkor/färdigheter: {skills}. Hur bra passar detta jobbet mig {df}?
        """
    
    # välj och filtrera på occupation field och occupation först
    prompt = f"""Skapa en tydlig beskrivning för jobb annonserna baserad på beskrivningen: {df["Description"]}, som beskriver arbetsuppgifter, 
        efterfrågade styrkor, färdigheter, krav, och egenskaper.
        sammanfatta data från {df[['Occupation', 'Headline', 'Required License', 'Required Skills','Experience Required', 'Driver License']]}
        
        Rangordna detta efter mest relevanta och ge mig en sammanfattning
        """
            
    
    # if len(df)>1:
    #     prompt3 = f"""Skapa en tydlig beskrivning för jobb annonserna baserad på beskrivningen: {df["Description"]}, som beskriver arbetsuppgifter, 
    #     efterfrågade styrkor, färdigheter, krav, och egenskaper.
        
    #     Rangordna detta efter mest relevanta och ge mig en sammanfattning på detta sätt:
    #     {{
    #         "sammanfattning av jobb beskrivning": "text",
    #         "efterfrågat(tex "styrkor"/"krav")": ["styrka1", "styrka2"]
    #         "antal för varje efterfrågade styrka/krav": ["antal1", "antal2"]   
    #     }}
        
    #     Plocka ut samma antal för "efterfrågat" och "antal", detta ska enkelt kunna användas till en plot i en dashboard.
    #     """
    # else:
    #     prompt3 = f"""Skapa en tydlig beskrivning för jobb annonsen baserad på beskrivningen: {df["Description"]}, som beskriver arbetsuppgifter, 
    #     efterfrågade styrkor, färdigheter, krav, och egenskaper.
        
    #     Skriv ut på detta sätt:
    #         "sammanfattning av jobb beskrivning"(ny rad)
    #         "arbetsuppgifter"(ny rad)
    #         "efterfrågade styrkor, färdigheter, krav, och egenskaper"  
    #     """
    
    



