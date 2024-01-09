#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Modules externes
import os
import csv
import re
import logging
import json
import xml.etree.ElementTree as ET
from datetime import datetime,date,timedelta
import requests
#Modules maison 
from SUDOC import Sudoc_api_rcrlist, Sudoc_test_localisation
from logs import logs

SERVICE = "Sudoc_Nb_de_loc_SUDOC"

LOGS_LEVEL = 'DEBUG'
LOGS_DIR = os.getenv('LOGS_PATH')


REGION = 'EU'
API_KEY = os.getenv('PROD_NETWORK_BIB_API')

REP = '/media/sf_LouxBox/Notices_a_fusionner/'


#On initialise le logger
logs.init_logs(LOGS_DIR,SERVICE,LOGS_LEVEL)
log_module = logging.getLogger(SERVICE)
log_module.info("Début du traitement")


def appel_webservice(ids):
    url = "https://www.sudoc.fr/services/multiwhere/{}".format(ids)
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        log_module.error(response.status_code)
        return None

def diviser_en_lots(identifiants, taille_lot):
    for i in range(0, len(identifiants), taille_lot):
        yield identifiants[i:i + taille_lot]

def lire_identifiants_de_fichier(fichier):
    with open(fichier, "r") as file:
        reader = csv.reader(file)
        return list(set(row[0] for row in reader))

def main():
    taille_lot = 100
    fichier_entree = 'Liste_PPN.csv'
    fichier_sortie = "resultats.csv"

    ppn = lire_identifiants_de_fichier(fichier_entree)

    lots_identifiants = list(diviser_en_lots(ppn, taille_lot))
    with open(fichier_sortie, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["PPN", "Nombre de bibliothèques"])
        nb_lots = len(lots_identifiants)
        for lot in lots_identifiants:
            log_module.debug(f"Nb de lots restants {nb_lots}")
            ids_string = ",".join(lot)
            resultat = appel_webservice(ids_string)

            if resultat:
                nb_ppn = len(resultat['sudoc']['query'])
                log_module.debug(f"{nb_ppn} ppn dans le lot {nb_lots}")
                for entry in resultat['sudoc']['query']:
                    ppn = entry['ppn']
                    # log_module.debug(ppn)
                    library_count = len(entry['result']['library'])
                    writer.writerow([ppn, library_count])
            else:
                log_module.error(f"Erreur lors de l'appel pour le lot {ids_string}")
        nb_lots -= 1

if __name__ == "__main__":
    main()