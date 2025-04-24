# AI_2_group_project

## Setup
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

**Extensions**
För att se filerna i project_descriptions ladda ner:    
Excel Viewer - av MESCIUS   
vscode-pdf - av tomoki1207  

## occupation_fields
***occupation_field__label***       -    ***occupation_field__concept_id***     
Hotell, restaurang, storhushåll     -    ScKy_FHB_7wT   
Installation, drift, underhåll      -    yhCP_AqT_tns   
Transport, distribution, lager      -    ASGV_zcE_bWf   
