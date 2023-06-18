import logging
from typing import Iterable, Iterator, Union

from libnmap.objects import NmapHost, NmapService
from libnmap.parser import NmapParser

from boefjes.job_models import NormalizerMeta
from octopoes.models import OOI, Reference
from octopoes.models.ooi.network import (
    IPAddressV4,
    IPAddressV6,
    Network,
)
from octopoes.models.ooi.service import IPService, Service


def normalize_os(host: NmapHost, network: Network, netblock: Reference) -> Iterator[OOI]:
    """Normalizes OS information if found on the host."""
    os = host.os_fingerprinted
    if os:
        ip = (
            IPAddressV4(network=network.reference, address=host.address, netblock=netblock)
            if host.ipv4
            else IPAddressV6(network=network.reference, address=host.address, netblock=netblock)
        )
        yield ip

        os_name = os.get("osmatch name")[0].get("name") if os.get("osmatch") else None
        os_accuracy = os.get("osmatch name")[0].get("accuracy") if os.get("osmatch") else None

        if os_name:
            os_ooi = OOI(name=os_name, accuracy=os_accuracy)
            yield os_ooi

            ip_os = IPService(ip_port=ip.reference, service=os_ooi.reference)
            yield ip_os

def run(normalizer_meta: NormalizerMeta, raw: Union[bytes, str]) -> Iterable[OOI]:
    """Decouple and parse Nmap XMLs and yield relevant network."""
    # Multiple XMLs are concatenated through "\n\n". XMLs end with "\n"; we split on "\n\n\n".
    raw = raw.decode().split("\n\n\n")

    # Relevant network object is received from the normalizer_meta.
    network = Network(name=normalizer_meta.raw_data.boefje_meta.arguments["input"]["network"]["name"])
    yield network

    netblock_ref = None
    if "NetBlock" in normalizer_meta.raw_data.boefje_meta.arguments["input"]["object_type"]:
        netblock_ref = Reference.from_str(normalizer_meta.raw_data.boefje_meta.input_ooi)

    logging.info("Parsing %d Nmap-xml(s) for %s.", len(raw), network)
    for r in raw:
        for host in NmapParser.parse_fromstring(r).hosts:
            yield from normalize_os(host=host, network=network, netblock=netblock_ref)
