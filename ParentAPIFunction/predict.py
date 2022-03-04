from io import StringIO
import sagemaker
from sagemaker.predictor import Predictor
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import CSVDeserializer
import time
import boto3

import settings
import pandas as pd

def predict_website(possible_urls_with_features, seuil):
    columns = [
       'url_rank', 'url', 'full_url', 'snippet', 'language', 'domain', 'name',
       'isfamilyfriendly', 'isnavigational', 'siren', 'siret',
       'nom_raison_sociale', 'numero_voie', 'type_voie', 'libelle_voie',
       'code_postal', 'libelle_commune', 'departement', 'geo_adresse',
       'activite_principale', 'libelle_activite_principale_entreprise',
       'tranche_effectif_salarie', 'categorie_entreprise', 'latitude',
       'longitude', 'dom_lev_score', 'max_rs_n_gram_matching_dom',
       'max_len_string_match', 'dom_ville_score', 'dom_dep_score',
       'snippet_score', 'lang', 'adresse'
       ]
    df = pd.DataFrame(possible_urls_with_features, columns=columns)
    region = boto3.Session().region_name
    session = sagemaker.Session()
    ep_name = settings.SAGEMAKER_ENDPOINT
    predictor = Predictor(
                        endpoint_name=ep_name,
                        sagemaker_session=session,
                        serializer=CSVSerializer(),
                        deserializer=CSVDeserializer(),
                        )
    test_data_inference = df
    prediction = predictor.predict(test_data_inference.to_csv(sep=",", header=False, index=False))
    prediction_df = pd.DataFrame(prediction)
    prediction_df_labels = prediction_df[0].astype(int)
    prediction_df_probas = prediction_df[1].astype(float)
    idmax = prediction_df_probas.idxmax()
    if prediction_df_probas[idmax] > seuil:
        return df.iloc[idmax].to_dict()