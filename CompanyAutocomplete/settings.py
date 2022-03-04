

URL_BASE_FULL_TEXT = "https://entreprise.data.gouv.fr/api/sirene/v1/full_text/{}"
URL_BASE_SIREN = "https://entreprise.data.gouv.fr/api/sirene/v1/siren/{}"

OUTPUT_COLS = [
    'siret',
    'siren',
    'nom_raison_sociale' ,
    'numero_voie',
    'type_voie',
    'libelle_voie',
    'code_postal',
    'libelle_commune',
    'departement',
    'geo_adresse',
    'activite_principale',
    'libelle_activite_principale_entreprise',
    'tranche_effectif_salarie',
    'categorie_entreprise',
    'latitude',
    'longitude'
    ]

PER_PAGE = 10

PAGE = 1
SUFIXE = "?per_page={}&page={}".format(PER_PAGE,PAGE)


