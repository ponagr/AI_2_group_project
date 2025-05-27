# AI_2_group_project

### Project Description
A school group project with the purpose to build and use a pipeline to extract data from arbetsförmedlingen API using dlt, transforming the data with dbt and orchestrating the whole pipeline using dagster.  
And then streaming the transformed data onto a dashboard using streamlit, with implemented LLM, filtering and plots for being able to easier analyze the data in different ways.

### Setup Project 
Start with cloning the repo localy: 
```bash
git clone https://github.com/ponagr/AI_2_group_project.git
```

**Install in terminal:**    
```bash
uv venv 
source .venv/Scripts/activate   
uv pip install -r requirements.txt  
```

**setup dbt profiles:**   
Open profiles.yml
```bash
code ~/.dbt/profiles.yml
```

Paste lines into profiles.yml   
```yml
job_ads_group_project:
  outputs:
    dev:
      type: duckdb
      path: ../job_ads_data_warehouse.duckdb
      threads: 1

    prod:
      type: duckdb
      path: prod.duckdb
      threads: 4

  target: dev
```

**Select python interpreter for project:**    
```bash
Ctrl+Shift+P > Python: Select Interpreter -> python 3.12.8('.venv':venv)

### Run Project

**Run dagster to load and transform data:**    
```bash
dagster dev -f definitions.py
```

In Assets-tab select all assets and click on Materialize selected

**Run streamlit dashboard:**   
```bash
streamlit run dashboard/dashboard.py
```

