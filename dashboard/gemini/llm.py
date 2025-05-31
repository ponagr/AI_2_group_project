import streamlit as st
import plotly.express as px
import os
from google import genai
import os
import pandas as pd
import json
from dotenv import load_dotenv
from pydantic import BaseModel

system_instruction = "Du är en Talent Acquisition Specialist på en HR-byrå. Ditt uppdrag är att analysera flera jobbannonser som kan användas internt för att förstå arbetsmarknadens krav och trender."

class Summarize_description(BaseModel):
    summary: str
    krav: list[str]
    meriterande: list[str]

class Total_skills(BaseModel):
    required: list[str]
    required_count: list[int]
    preferred: list[str]
    preferred_count: list[int]

def get_client():
    load_dotenv()
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_description(df):
    if df["Description"].str.len().iloc[0] < 1000:
        st.warning("Description is not long enough for summarization")
        st.markdown("### Original description")
        st.info(df["Description"].iloc[0])
    else:
        with st.spinner("Awaiting response..."):
            client = get_client()
            description = " ".join(df["Description"])
            prompt = f"""
            Sammanfatta följande jobbannons på ett kortfattat och informativt sätt.

            Fokusera på:
            1. Arbetsuppgifter
            2. Krav och kvalifikationer
            3. Meriterande egenskaper eller erfarenheter
            4. Övrig viktig information
            
            Här är jobbannonsen:
            {description}
            """
            
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                config={
                    "system_instruction": system_instruction,
                    "temperature": 0.2
                },
                contents=prompt
            )

            st.markdown("### llm summarized description")
            st.info(response.text)
    
def summarize_occupation_group(df):
    with st.spinner("Awaiting response..."):
        client = get_client()
        job_descriptions = df["Description"]
        job_descriptions_text = "\n\n".join(job_descriptions.tolist())
        
        prompt = f"""
        Analysera följande jobbannonser inom yrkesgruppen {df["Occupation Group"]}.
        
        Uppgift:
        1. Identifiera och sammanfatta de vanligaste arbetsuppgifterna.
        2. Lista de mest efterfrågade kompetenserna eller färdigheterna.
        3. Notera eventuella meriterande kvalifikationer eller personliga egenskaper.
        4. Identifiera återkommande mönster eller trender (t.ex. fokus på digitalisering, kundkontakt, språkkunskaper, etc).

        Instruktioner:
        - Skriv i markdown.
        - Börja endast med `## Sammanfattning av (yrkesgrupp)` sen rubrikerna
        - Dela upp innehållet med följande rubriker:
        - `### Arbetsuppgifter`
        - `### Krav`
        - `### Meriterande`
        - `### Trender`
        - Håll det kortfattat, sakligt och fokuserat på nyckelinsikter.
        - Baserat enbart på informationen i annonserna.
        - Håll varje rubrik till 5 punkter
        
        Här är jobbannonserna att analysera:
        {job_descriptions_text}
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "system_instruction":system_instruction,
                "temperature": 0.2
            },
            contents=prompt
        )
        
        st.markdown(response.text, unsafe_allow_html=True)

# Pie chart över krav och meriterande kvalifikationer för en yrkesgrupp
def skills_per_occupation_group(df):
    with st.spinner("Awaiting response..."):
        client = get_client()
        job_descriptions = df["Description"]
        job_descriptions_text = "\n\n".join(job_descriptions.tolist())
        
        prompt = f"""
        Du ska analysera jobbannonser inom yrkesgruppen "{df["Occupation Group"]}".
        Extrahera:
        1. De 5 vanligaste **kraven** (färdigheter, erfarenheter, utbildning etc).
        2. De 5 vanligaste **meriterande kvalifikationerna** (önskvärda men ej nödvändiga egenskaper eller kompetenser).
        3. Räkna hur ofta varje punkt förekommer i texterna.

        Håll varje punkt till max 100 tecken
        Returnera ett JSON-objekt i detta format:
        {{
        "krav": ["krav1", "krav2", ...],
        "krav_count": [antal1, antal2, ...],
        "meriterande": ["merit1", "merit2", ...],
        "meriterande_count": [antal1, antal2, ...]
        }}

        Analysera endast utifrån texten nedan:

        {job_descriptions_text}
        """
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "response_mime_type":"application/json",
                "response_schema":Total_skills,
                "system_instruction": system_instruction,
                "temperature": 0.2
            },
            contents=prompt
        )
        
        data = json.loads(response.text)
        
        required_df = pd.DataFrame({
            "Skill": data["required"],
            "Count": data["required_count"]
        })
        preferred_df = pd.DataFrame({
            "Skill": data["preferred"],
            "Count": data["preferred_count"]
        })

        st.markdown("## Top 5 Required / Preferred Skills")
        fig1 = px.pie(required_df, names="Skill", values="Count", title="Summary of Required Skills in Job Ads")
        fig2 = px.pie(preferred_df, names="Skill", values="Count", title="Summary of Preferred Skills in Job Ads")
        fig1.update_layout(legend=dict(font=dict(size=14)))
        fig2.update_layout(legend=dict(font=dict(size=14)))
        st.plotly_chart(fig1)
        st.plotly_chart(fig2)

# skapar en tabell med sammanfattad analys på vald dataframe för tydlig överblick med hjälp av gemini llm
def overview_description(df, choice):
    client = get_client()
    
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
            
            Jag vill ha output i markdown likt detta:
            
            Börja endast med `## Sammanfattning`
            
            Element | Beskrivning
            Dominerande sektor | Hotell, Restaurang, Storhushåll
            Vanligaste yrken | Köksbiträde, Kock (alla typer), Servitör/Servitris
            Anställningsform | Heltid (vanligast), Deltid (förekommer frekvent inom restaurang)
            Erfarenhet | Ofta ett krav, men varierar beroende på tjänst.
            Körkort | Krävs för vissa tjänster som Taxiförare, Distributionsförare och en köksbiträde.
            Potentiellt intressant | "Kock, à la carte" kan indikera en mer specialiserad roll.
            Branschfokus | Starkt fokus på Hotell/Restaurang (kan vara säsongsbetonat).
            Plus yttligare kommentarer i punktlista(om relevant)
            
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
            
            Jag vill ha output i markdown likt detta:
            
            Börja endast med `## Sammanfattning`
            
            Element | Beskrivning
            Dominerande sektor | Hotell, Restaurang, Storhushåll
            Vanligaste yrken | Köksbiträde, Kock (alla typer), Servitör/Servitris
            Anställningsform | Heltid (vanligast), Deltid (förekommer frekvent inom restaurang)
            Erfarenhet | Ofta ett krav, men varierar beroende på tjänst.
            Körkort | Krävs för vissa tjänster som Taxiförare, Distributionsförare och en köksbiträde.
            Potentiellt intressant | "Kock, à la carte" kan indikera en mer specialiserad roll.
            Branschfokus | Starkt fokus på Hotell/Restaurang (kan vara säsongsbetonat).
            Plus yttligare kommentarer i punktlista(om relevant)
        """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config={
            "temperature": 0.2
        }
        )
    
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