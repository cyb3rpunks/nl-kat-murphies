# Author: C. Baaij
# As part of a project for Hogeschool van Amsterdam

from typing import List, Tuple, Union
from boefjes.job_models import BoefjeMeta
import requests
import json

def run(boefje_meta: BoefjeMeta) -> List[Tuple[set, Union[bytes, str]]]:
    input_ = boefje_meta.arguments["input"]
    ip = input_["address"]
    url = "https://rdap.arin.net/registry/ip/" + ip
    response = requests.get(url)
    json_data = json.loads(response.text)
    data = {
        "handle": json_data["handle"],
        "startAddress": json_data["startAddress"],
        "endAddress": json_data["endAddress"],
        "name": json_data["name"],
        "eventAction": json_data["events"][0]["eventDate"],
        "registrationDate": json_data["events"][1]["eventDate"],
        "organisation": json_data["entities"][0]["vcardArray"][1][1][3],
        "cidrLength": json_data["cidr0_cidrs"][0]['length'],
        "cidrPrefix": json_data["cidr0_cidrs"][0]['v4prefix']
    }
    return [(set(), json.dumps(data))]