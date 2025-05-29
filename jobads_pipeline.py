import dlt
import requests
import json

# getting response from api based on params from dlt resource get_hits-function, returns page of 100 rows each call
def _get_ads(url_for_search, params):
    headers = {"accept": "application/json"}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status()  # check for http errors
    return json.loads(response.content.decode("utf8"))

# this is for removing data in the default staging_staging scheme created by dlt
dlt.config["load.truncate_staging_dataset"] = True

# dlt resource that adds new data for occupation fields ("ScKy_FHB_7wT", "yhCP_AqT_tns", "ASGV_zcE_bWf") into job_ads table
@dlt.resource(
    table_name = "job_ads",
    write_disposition="merge",
    primary_key="id"
)
def get_hits():
    occupation_fields = ("ScKy_FHB_7wT", "yhCP_AqT_tns", "ASGV_zcE_bWf")
    query = ""
    url = "https://jobsearch.api.jobtechdev.se"
    url_for_search = f"{url}/search"
    
    # yields data with max offset limit of 2000 for each occupation field.
    for occupation_field in occupation_fields:
        params = {"q": query, "limit": 100, "occupation-field": occupation_field}
        limit = params.get("limit", 100)
        offset = 0
        while True:
            # build this page’s params
            page_params = dict(params, offset=offset)
            data = _get_ads(url_for_search, page_params)

            hits = data.get("hits", [])
            if not hits:
                # no more results
                break

            # yield each ad on this page
            for ad in hits:
                yield ad

            # if fewer than a full page was returned, we’re done
            if len(hits) < limit or offset > 1900:
                break

            offset += limit # adds 100 each iteration until offset = 2000, then breaks

# to work with dagster, we need to create a dlt source to include the dlt resource
@dlt.source
def jobads_source():
    # return each yielded ad into dlt pipeline used by dagster
    return get_hits()
