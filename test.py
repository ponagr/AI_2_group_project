# from pathlib import Path
# import dagster as dg
# from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

# dbt_project_directory = Path(__file__).parent / "job_ads_group_project"
# profiles_dir = "C:/Users/organ/.dbt"#Path.home() / ".dbt"  
# dbt_project = DbtProject( project_dir=dbt_project_directory, profiles_dir=profiles_dir )

# print(profiles_dir)
from pathlib import Path

dbt_project_directory = Path("c:/Users/organ/Repos/python/grupp_projekt/AI_2_group_project/job_ads_group_project")
manifest_path = dbt_project_directory / "target" / "manifest.json"

print("Manifest exists:", manifest_path.exists())
print("Full path:", manifest_path.resolve())