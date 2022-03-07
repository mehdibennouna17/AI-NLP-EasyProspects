import plotly.express as px
from sklearn.decomposition import PCA
import pandas as pd

df = pd.read_excel("dataset.xlsx")
X = df[[
       # 'lang_id',
       # 'url_rank',	
        'snippet_score',	
        'dom_lev_score',	
        'max_rs_n_gram_matching_dom',	
        'max_len_string_match',	
       # 'dom_ville_scores',
       # 'dom_dep_scores'
        ]]

pca = PCA(n_components=2)
components = pca.fit_transform(X)

fig = px.scatter(components, x=0, y=1, color=df['target'])
fig.show()