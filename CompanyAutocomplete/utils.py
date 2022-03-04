
from data import tranche_effectif_dict

def check_if_none(text):
    if not text:
        out = str()
    else:
        out = str(text)
    return out


def clean_data(label, value):
    value = check_if_none(value)
    if label == 'libelle_commune':
        if "paris" in value.lower() and "arrondissement" in value.lower():
            out = 'PARIS'
        elif "lyon" in value.lower() and "arrondissement" in value.lower():
            out = "LYON"
        elif "marseille" in value.lower() and "arrondissement" in value.lower():
            out = "MARSEILLE"
        else:
            out = value
            
    elif label == 'tranche_effectif_salarie':
        out = tranche_effectif_dict[value]
    else:
        out = value
    return out
    