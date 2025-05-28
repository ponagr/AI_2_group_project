import streamlit as st
import os
from google import genai
from dotenv import load_dotenv
import json
from pydantic import BaseModel
import plotly_express as px
import pandas as pd

system_instruction = "Du är en Talent Acquisition Specialist på en HR-byrå. Ditt uppdrag är att analysera flera jobbannonser som kan användas internt för att förstå arbetsmarknadens krav och trender."

class Total_skills(BaseModel):
    required: list[str]
    required_count: list[int]
    preferred: list[str]
    preferred_count: list[int]

def get_client():
    load_dotenv()
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_occupation_group(df):
    client = get_client()

    selected = st.selectbox("Select an occupation group to summarize job roles and requirements", df["Occupation Group"].unique().tolist())
    df = df[df["Occupation Group"] == selected]
    
    if len(df) < 10:
        st.warning("Not enough job ads for analysis")
    else:
        job_descriptions = df["Description"]
        job_descriptions_text = "\n\n".join(job_descriptions.tolist())
        
        prompt = f"""
        Analysera följande jobbannonser inom yrkesgruppen {selected}.
        
        Uppgift:
        1. Identifiera och sammanfatta de vanligaste arbetsuppgifterna.
        2. Lista de mest efterfrågade kompetenserna eller färdigheterna.
        3. Notera eventuella meriterande kvalifikationer eller personliga egenskaper.
        4. Identifiera återkommande mönster eller trender (t.ex. fokus på digitalisering, kundkontakt, språkkunskaper, etc).

        Instruktioner:
        - Skriv i markdown.
        - Börja endast med `## Sammanfattning av (yrkesgrupp)`
        - Dela upp innehållet med följande rubriker:
        - `### Arbetsuppgifter`
        - `### Krav`
        - `### Meriterande`
        - `### Trender`
        - Håll det kortfattat, sakligt och fokuserat på nyckelinsikter.
        - Baserat enbart på informationen i annonserna.
        
        Här är jobbannonserna att analysera:
        {job_descriptions_text}
        """
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config={
                "system_instruction":system_instruction,
            },
            contents=prompt
                
        )
        
        st.markdown(response.text, unsafe_allow_html=True)

# Pie chart över krav och meriterande kvalifikationer för en yrkesgrupp
def skills_per_occupation_group(df):
    client = get_client()
    
    selected = st.selectbox("Select occupation group to analyze required and preferred skills", df["Occupation Group"].unique().tolist())
    df = df[df["Occupation Group"] == selected]
    
    if len(df) < 10:
        st.warning("Not enough job ads for analysis")
    else:
        job_descriptions = df["Description"]
        job_descriptions_text = "\n\n".join(job_descriptions.tolist())
        
        prompt = f"""
        Du ska analysera jobbannonser inom yrkesgruppen "{selected}".
        Extrahera:
        1. De vanligaste **kraven** (färdigheter, erfarenheter, utbildning etc).
        2. De vanligaste **meriterande kvalifikationerna** (önskvärda men ej nödvändiga egenskaper eller kompetenser).
        3. Räkna hur ofta varje punkt förekommer i texterna.

        Returnera ett JSON-objekt i detta format på topp 10:
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
                    "system_instruction": system_instruction
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

        st.markdown("## Top 10 Required / Preferred Skills")
        col1, col2 = st.columns(2)
        fig1 = px.pie(required_df, names="Skill", values="Count", title="Summary of Required Skills in Job Ads")
        fig2 = px.pie(preferred_df, names="Skill", values="Count", title="Summary of Preferred Skills in Job Ads")
        col1.plotly_chart(fig1)
        col2.plotly_chart(fig2)