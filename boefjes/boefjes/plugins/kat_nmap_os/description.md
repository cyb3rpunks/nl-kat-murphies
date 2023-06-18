# Nmap

Nmap is a powerful network scanning tool that utilizes IP packets to identify and gather information about devices connected to a network. It provides detailed insights into the services and operating systems running on those devices. In KAT, a Python wrapper is utilized to leverage the capabilities of Nmap for discovering Operating Systems. Nmap is executed within a temporary Docker container, ensuring a controlled and isolated environment for the scanning process.

### Options

This Nmap has the following hardcoded options for an OS scan:

| Option | Function |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| `-A` | enables aggressive scanning incl. various advanced scan options                    
| `T5` |  sets the timing template to the highest speed, increasing the scanning speed but potentially raising the chance of detection                          
| `-O` | enables OS detection, allowing Nmap to attempt to determine the operating system of the target host                
| `-sV` | performs version detection, actively identifying the software and services running on open ports of the target host.  
|`-oX` | Output in XML                                                

### Input OOIs

Nmap expects an IpAddress as input which can be of type IpAddressV4 or IpAddressV6.

### Output OOIs

Nmap outputs the following OOIs:

|OOI type|Description|
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
|osmatch name|: A list of detected operating systems that match the scanned device
|accuracy|: The accuracy of the detected match with the operating system
|line|: The line number where the match is displayed in the scan output
|osclass type|: A more detailed classification of the detected operating system
|vendor|: The name of the vendor or developer of the detected operating system
|osfamily|: The general category or family to which the detected operating system belongs
|cpe|: The Common Platform Enumeration (CPE) of the detected operating system

### Running Boefje

```json
{
  "id": "nmap-scan-job",
  "organization": "_dev",
  "arguments": {
    "host": "1.1.1.1"
  },
  "dispatches": {
    "normalizers": [
      "kat_nmap.normalize"
    ],
    "boefjes": []
  }
}
```

### Boefje structure

```
boefjes/tools/kat_nmap_os
├── normalize.py
├── main.py
```

**Cat name**: Tijger en Macy
