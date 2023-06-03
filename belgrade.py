import requests
import json

url = "http://data.sepa.gov.rs/api/3/action/datastore_search_sql"
sql = """
SELECT 
    date_time::date,
    k_short_name || ' (' || k_unit || ')' AS pollutant,
    AVG(value)
FROM 
    "a8f71ec0-0a68-4d4f-8f37-ceabdcb98569" AS data
    JOIN "7fa4ab3f-423a-4016-8508-37164b49c087" AS pollutant_info
    ON data.component_id = pollutant_info.id
    JOIN "dd7f4e4b-2375-4657-bb91-d541a2759891" AS station_info
    ON data.station_id = station_info.id
WHERE
    date_time::date >= '2022-10-01'
    AND date_time::date <= '2023-03-31'
    AND k_short_name IN ('SO2', 'O3', 'CO', 'PM2.5', 'PM10', 'NO2')
    AND station_info.k_city = 'Beograd'
GROUP BY
    date_time::date,
    pollutant
ORDER BY
    date_time::date ASC
"""
r = requests.get(url, params={"sql": sql})
print(json.dump(r.json()["result"]["records"], open("data.json", "w")))
