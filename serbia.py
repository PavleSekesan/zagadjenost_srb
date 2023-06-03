import requests
import json

url = "http://data.sepa.gov.rs/api/3/action/datastore_search_sql"
sql = """
SELECT 
    date_time::date,
    k_short_name || ' (' || k_unit || ')' AS pollutant,
    AVG(value)
FROM 
    "a8f71ec0-0a68-4d4f-8f37-ceabdcb98569"
    JOIN "7fa4ab3f-423a-4016-8508-37164b49c087"
    ON "a8f71ec0-0a68-4d4f-8f37-ceabdcb98569".component_id = "7fa4ab3f-423a-4016-8508-37164b49c087".id
WHERE
    date_time::date >= '2022-10-01'
    AND date_time::date <= '2023-03-31'
    AND k_short_name IN ('SO2', 'O3', 'CO', 'PM2.5', 'PM10', 'NO2')
GROUP BY
    date_time::date,
    pollutant
ORDER BY
    date_time::date ASC
"""
r = requests.get(url, params={"sql": sql})
json.dump(r.json()["result"]["records"], open("data.json", "w"))
