# Nombre de localisations SUDOC
Prends une liste de PPN en entrée et fourni pour chacun le nombre de rcr localisé sous la notice.

## Fonctionnement
Le programme :
1. Dédoublonne la liste 
2. Constitue des lots de 100 PPN
3. Pour chaque lot appel le webservice [Multiwhere](https://documentation.abes.fr/sudoc/manuels/administration/aidewebservices/index.html#multiwhere)  de l'ABES
4. Dans chaque réponse et pour chaque PPN compte le nombre de RCR
5. Ecrit le tout dans un fichier csv

## Piste d'amélioration:
Compter le nombre de rcr pour un même iln