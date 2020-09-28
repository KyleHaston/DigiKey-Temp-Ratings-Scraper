# ----------------------------------------------------------------------------------------------------------------------
# Kyle Haston
# Sept 2020
# Need to check temperature rating for circuit components. Going to scrape the info. from Digikey.
# ----------------------------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import urllib
import time
import os

# use requests to get a text version of the webpage we want.
# feed it into BeautifulSoup and specify an HTML parser

# Base Board
# mfg_PNs = ['CGA3E2X7R1H104K080AA', 'CL10A475MQ8NNNC', 'GRM188R71H103KA01', 'VY1222M47Y5UQ63V0', 'TMK212BBJ106KG-T',
#           'CL10A474KA8NNNC', 'EEE1HA101UP', 'UWT0J101MCL1GB', 'UVK2V680MHD', 'CC0603KRX7R6BB334', 'EEE-FK1H220P',
#           'CL10C120JB8NNNC', 'CL10B222KB8NFNC', 'CC0603JRNPO0BN270', 'P6SMB47CA', 'SM712-02HTG', 'SMAJ5.0CA-13-F',
#           'RS1MTR', '1SMA200Z R3G', 'S3M', 'SF-3812TM050T-2', 'BC-508X14-7 BK', 'SFV30R-4STBE1HLF', 'EK508V-09P-BK',
#           'MLZ1608N100L', 'SCT2H12NYTB', 'ERJ3EKF5110V', 'RC0603JR-070RL', 'EP1WS10RJ', 'CRCW060344K2FKEA',
#           'ERJ3EKF1431V', 'RT0603BRD071K43L', 'RT0603DRD074K99L', 'RT1206DRD071ML', 'RC0603FR-07240RL',
#           'CRCW060375K0FKEA', 'RMCF1206FT100K', 'RC0603FR-07390RL', 'CRCW08054R70FKEA', '20050 Rev 3', 'LAA108STR',
#           'MSP430F67671AIPZR', 'ISO1410BDWR', 'AS78L05RTR-E1', 'LM317LDR2G', 'UCC28730DR', 'LTV-826S',
#           'CM7V-T1A-32.768KHZ-12.5PF-20PPM-TA-QC']

# test case
# mfg_PNs = ['CGA3E2X7R1H104K080AA', 'CL10A475MQ8NNNC', 'GRM188R71H103GARBAGE']  # for testing. last PN should err out.

# Display Board
mfg_PNs = ['3030TR', 'TAJA475K025RNJ', 'GRT188R61H105ME13D', 'CGA3E2X7R1H104K080AA', 'TMK212BBJ106KG-T', '1N4148W-TP',
           'BAT46GWX', 'MLZ1608N100L', 'SFV30R-3STBE1HLF', 'ERJ3EKF1000V', 'ERJ3EKF6343V', 'ERJ-3EKF2321V',
           'ERJ3EKF2490V', 'FSM8JSMA', 'ST25DV04K-IER6S3', 'PCF85263ATT/AJ', 'LM317LDR2G', 'CAT24M01WI-GT3',
           'CM7V-T1A-32.768KHZ-12.5PF-20PPM-TA-QC']

ratings = []  # placeholder for the temp. ratings we're about to scrape
missing = []  # placeholder for part numbers that didn't turn up any ratings.

for pn in mfg_PNs:

    print('\tGathering info: ' + pn)
    URL = 'https://www.digikey.com/products/en?keywords=' + pn

    soup = BeautifulSoup(requests.get(URL).text, 'html.parser')

    found = False
    # find all anchors (links)
    # tags = soup.find_all('a')
    tags = soup.find_all('td')

    for tag in tags:
        if '°' in tag.text and '/°C' not in tag.text and '@' not in tag.text:
            # print('        ' + pn + ': ' + tag.text.strip('\n\r\t '))
            ratings.append(pn + '\t' + tag.text.strip('\n\r\t '))
            found = True

    if not found:
        print('\t\tWARNING: Could not find rating for PN: ' + pn)
        missing.append(pn)

ratings = list(dict.fromkeys(ratings))  # remove duplicate entries

print('\n\tTemperature Ratings:')
for r in ratings:
    print('\t\t' + r)

print('\n\tMissing:')
for m in missing:
    print('\t\t' + m)
