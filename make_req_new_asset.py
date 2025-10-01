import os
import requests
from dotenv import load_dotenv
from keycloak import KeycloakOpenID


load_dotenv()


data_exp = {
  "platform": "aiod",
  "platform_resource_identifier": 2
  ,
  "name": "Use case HC2 bias detection and mitigation_TEST",
  "date_published": "2025-07-07T15:15:00.000",
  "same_as": "https://github.com/aequitas-aod/experiment-hc2-ecg-incartdb",
  "is_accessible_for_free": True,
  "version": "",
  "pid": "",
  "experimental_workflow": "1) process original data set using the R Quarto Markdown file; 2) run analysis code found in the Jupyter notebook; 3) Run R analysis (in incart_repaired.qmd) to complete analysis.",
  "execution_settings": "",
  "reproducibility_explanation": "",
  "aiod_entry": {
    "editor": []
  },
  "alternate_name": [
  ],
  "application_area": [
  ],
  "badge": [
  ],
  "citation": [],
  "contact": [
  ],
  "creator": [
  ],
  "description": {
    "plain": "This repository contains the Jupyter notebook that was used to do a toy world analysis of bias detection and mitigation in the context of use case HC2 ECG data. The approach illustrates in simple ways how to use synthetic data to repair bias observed in a small data set with only few variables."
  },
  "distribution": [],
  "has_part": [],
  "industrial_sector": [
    "Social Security"
  ],
  "is_part_of": [],
  "keyword": [],
  "license": "mit",
  "media": [],
  "note": [],
  "relevant_link": [],
  "relevant_resource": [],
  "relevant_to": [],
  "research_area": [],
  "scientific_domain": []
}


def _run_requests(access_token_value: str) -> None:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token_value}",
        "Content-Type": "application/json",
    }
    
    endpoint="v2/experiments"  #or v2/experiments or v2/datasets or v2/educational_resources

    #create new resource
    response = requests.post(f"https://api-aiod-dev.iti.es/{endpoint}", headers=headers, json=data_exp)



    print(response.status_code)
    print(response.text)



if __name__ == "__main__":

    _run_requests(os.getenv("ACCESS_TOKEN"))
   
