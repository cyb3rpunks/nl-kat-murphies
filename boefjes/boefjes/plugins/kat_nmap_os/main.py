#Author: M. van der Kolk 2023
#As part of a project for the University of Amsterdam for Applied Sciences

from enum import Enum
from ipaddress import IPv6Address, ip_address
from typing import List, Tuple, Union
import docker

from boefjes.job_models import BoefjeMeta

NMAP_IMAGE = "instrumentisto/nmap:latest"

def run_nmap(args: List[str]) -> str:
    """Run Nmap in Docker."""
    client = docker.from_env()
    return client.containers.run(NMAP_IMAGE, args, remove=True).decode()

def build_nmap_arguments(host: str) -> List[str]:
    ip = ip_address(host)
    args = ["nmap", "-A", "T5", "-O", "-sV"]
    if isinstance(ip, IPv6Address):
        args.append("-6")
    args.extend(["-oX", "-", host]) 
    return args

def run(boefje_meta: BoefjeMeta) -> List[Tuple[set, Union[bytes, str]]]:
    """Build Nmap arguments and return results to normalizer."""
    return [
        (
            set(),
            run_nmap(
                args=build_nmap_arguments(
                    host=boefje_meta.arguments["input"]["address"]
                )
            ),
        )
    ]
