import os
import requests
from dotenv import load_dotenv
from keycloak import KeycloakOpenID


load_dotenv()

data = {
  "platform": None,
  "platform_resource_identifier": None,
  "name": "aequitastest",
  "date_published": "2022-01-01T15:15:00.000",
  "same_as": "https://www.example.com/resource/this_resource",
  "is_accessible_for_free": "true",
  "version": "1.1.0",
  "issn": "20493630",
  "measurement_technique": "mass spectrometry",
  "temporal_coverage": "2011/2012",
  "aiod_entry": None,
  "alternate_name": [
    "alias 1",
    "alias 2"
  ],
  "application_area": [
    "Fraud Prevention",
    "Voice Assistance",
    "Disease Classification"
  ],
  "citation": [],
  "contact": [],
  "creator": [],
  "description": None,
  "distribution": [],
  "funder": [],
  "has_part": [],
  "industrial_sector": [
    "Pharmaceuticals",
    "Computer Programming",
    "Cybersecurity"
  ],
  "is_part_of": [],
  "keyword": [
    "keyword1",
    "keyword2"
  ],
  "license": "CC-BY-4.0",
  "media": [],
  "note": [],
  "relevant_link": [
    "https://www.example.com/a_relevant_link",
    "https://www.example.com/another_relevant_link"
  ],
  "relevant_resource": [],
  "relevant_to": [],
  "research_area": [
    "AI Services",
    "Multi-agent Systems"
  ],
  "scientific_domain": [
    "Computer and Information Sciences",
    "Mathematics"
  ],
  "size": None,
  "spatial_coverage": None
}

data_exp = {
  "platform": "aiod",
  "platform_resource_identifier": 1,
  "name": "Use case HC2 bias detection and mitigation",
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
    
    endpoint="v2/datasets"  #or v2/experiments or v2/datasets or v2/models
    identifier="<id>"  #id of the resource to modify (for PUT requests)

    #modify existing resource
    response = requests.put(f"https://api-aiod-dev.iti.es/{endpoint}/{identifier}",
        headers=headers,
        json=data_exp,
    )

    print(response.status_code)
    print(response.text)



if __name__ == "__main__":

    _run_requests(os.getenv("ACCESS_TOKEN"))
   
