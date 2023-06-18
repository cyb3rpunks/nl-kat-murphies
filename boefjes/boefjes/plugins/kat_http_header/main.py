# Author: C.baaij en buddy R. Visser 2023
# As part of a project for Hogeschool van Amsterdam

from typing import List, Tuple, Union
from boefjes.job_models import BoefjeMeta
import requests
import json

def run_httpheaders(boefje_meta: BoefjeMeta) -> List[Tuple[set, Union[bytes, str]]]:
    #De input van het boefje wordt als variable geset
    input_ = boefje_meta.arguments["input"]
    #De verschillende bouwblokken voor de URI worden in de onderstaande variables gestopt
    netloc = input_["netloc"]["name"]
    path = input_["path"]
    scheme = input_["scheme"]
    Port = input_["port"]
    #De uri is gebouwd op basis van de bouwblokken en wordt gebruikt om doormiddel van de request moduele een HTTP request te maken.
    uri = f"{scheme}://{netloc}:{Port}{path}"
    #De HTTP request wordt gemaakt en wordt opgeslagen in een variable.
    response = requests.get(uri)
    #De headers worden opgeslagen in een dictionary waarin de waardes “kleine” letter hebben. Dit zorgt ervoor dat de format van de headers Case Insensitive is.
    headers = CaseInsensitiveDict(response.headers)
    #Veranderd de CaseInsensitiveDict naar een normale Dict.
    headers_dict = dict(headers)
    #Het resultaat is een JSON file met het object van de url en het tweede object bevat de HTTP headers welke opgeslagen zijn in de headers_dict
    result = {"url": url, "headers": headers_dict}
    #Returned the result als JSON file
    return [(set(), json.dumps(result))]
