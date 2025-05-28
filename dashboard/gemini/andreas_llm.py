import streamlit as st
import os
from google import genai
from dotenv import load_dotenv

system_instruction = "Du är en Talent Acquisition Specialist på en HR-byrå. Ditt uppdrag är att analysera flera jobbannonser som kan användas internt för att förstå arbetsmarknadens krav och trender."

def get_client():
    load_dotenv()
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_occupation_group(df):
    client = get_client()

    selected = st.selectbox("Välj en yrkesgrupp att sammanfatta:", df["Occupation Group"].unique().tolist())
    df = df[df["Occupation Group"] == selected]
    job_descriptions = df["Description"]
    
    prompt = f"""
    Analysera följande jobbannonser inom yrkesgruppen {df['Occupation Group']}.
    
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
    {job_descriptions}
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config={
            "system_instruction":system_instruction,
        },
        contents=prompt
            
    )
    
    st.markdown(response.text, unsafe_allow_html=True)