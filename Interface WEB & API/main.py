#imports
import fastapi
from fastapi import FastAPI, Request
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


data_joueurs = pd.read_csv("data_joueurs_complet.csv")

#Preprocessing
#one hot encoder sur le poste 
one_hot = pd.get_dummies(data_joueurs['poste'])
# Join the encoded df
data_joueurs = data_joueurs.join(one_hot)

data_joueurs.drop(columns='Unnamed: 0',inplace=True)
data_joueurs["taille"] = data_joueurs["taille"].str.replace("\xa0m", "")
data_joueurs["taille"] = data_joueurs["taille"].str.replace(",", ".")

def value_to_float(x):
    if 'K' in x:
        return float(x.replace(' K €', '')) * 0.001
    if 'mio.' in x:
        return float(x.replace(' mio. €', ''))



data_joueurs["valeur"] = data_joueurs["valeur_marchande"].str.replace(",", ".")
data_joueurs["valeur"] = data_joueurs["valeur"].apply(value_to_float)
data_joueurs["valeur"] = data_joueurs["valeur"].apply(pd.to_numeric)
column_to_move = data_joueurs.pop("valeur")
data_joueurs.insert(10, "valeur", column_to_move)

data_joueurs["age_normalized"] = MinMaxScaler().fit_transform(np.array(data_joueurs["age"]).reshape(-1,1))
data_joueurs["taille_normalized"] = MinMaxScaler().fit_transform(np.array(data_joueurs["taille"]).reshape(-1,1))

X = data_joueurs.iloc[:, 11:].to_numpy()
cosine_sim = cosine_similarity(X)

#functions
def get_index_from_name(name):
    return data_joueurs[data_joueurs.nom_joueur == name].index.values[0]

def get_list_of_indexes(sorted_similar_players, nb_joueurs, valeur_max):
    i=1
    j=1
    liste_index_finale = []
    while(i<nb_joueurs+1):
        if data_joueurs.iloc[sorted_similar_players[j][0]].valeur<=valeur_max:
            liste_index_finale.append(sorted_similar_players[j][0])
            i+=1
        j+=1
    return liste_index_finale

def create_finale_df(sorted_similar_players, nb_joueurs, valeur_max):
    liste_index_finale = get_list_of_indexes(sorted_similar_players, nb_joueurs, valeur_max)
    res = data_joueurs.iloc[liste_index_finale]
    return res.iloc[:,:10]

def select_similar_players(cosine_matrix, player_name,nb_joueurs,valeur_max=300):
    player_index = get_index_from_name(player_name)
    similar_players = list(enumerate(cosine_matrix[player_index]))
    sorted_similar_players = sorted(similar_players, key=lambda x:x[1], reverse=True)
    return create_finale_df(sorted_similar_players, nb_joueurs, valeur_max)


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root():
    return {"message": "Bienvenue sur le site de recherche de joueur"}

@app.get("/home")
def home():
    return HTMLResponse(content=open("templates/home.html", "r").read())

@app.get("/model")
def home():
    return HTMLResponse(content=open("templates/model.html", "r").read())


@app.get("/joueur/{joueur_nom}/nombre/{nombre}/prix_max/{prix_max}")
async def read_joueur_solo(joueur_nom,nombre=10,prix_max=300):
    df_res = select_similar_players(cosine_sim,joueur_nom,int(nombre),float(prix_max))
    df_res = df_res.fillna('NA')
    return df_res.values.tolist()

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})
