#!/usr/bin/env python
# coding: utf-8

# # Libraries

import requests
import pandas as pd
import json
from datetime import datetime as dt


# # Actividad 1: Conectarse al enlace

# Hago el request con la url del ejercicio

url_request = 'https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle=perl&site=stackoverflow'
resp = requests.get(url_request)


# Acá reviso que se haya obtenido correctamente la información

print(resp.status_code)


# Guardo el contenido del request como un diccionario

dict_posts = json.loads(resp.text)


# # Data Exploration

# Los datos que nos importan se encuentran dentro de *'items'*

dict_posts.keys()


# Para un mejor manejo de datos transformo el diccionario a un dataframe:

dposts = pd.DataFrame(dict_posts['items'])


# **NOTA:** Le agrego una "d" al inicio de la variable *posts* porque así sé que es un dataframe.

# Veo el número total de posts:

total = dposts.shape[0]
print('Total de posts:', total)


# ## Actividad 2: Obtener el número de respuestas contestadas y no contestadas

# En esta parte no estaba seguro si utilizar la columna *'is_answered'* o *'answer_count'*, ya que al contar los True que contiene *'answer_count'* vienen 18 registros pero si cuento los *'answer_count'* diferentes de 0 son 23. 
# 
# Por lo que fui a ver el link de los post que tienen 'answer_count': False y 'answer_count' diferentes de 0 y resulta que estos en estos posts sí recibieron respuestas, por lo que decidí contar respecto a la columna *'answer_count'*.

answered = dposts['answer_count'].apply(lambda x: x!=0).sum()
not_answered = dposts['answer_count'].apply(lambda x: x==0).sum()


print(' Número de posts que recibieron respuesta:', answered, '\n Número de posts que no recibieron respuesta', not_answered)


# # Actividad 3: Obtener la respuesta con menor número de vistas

# Ahora obtenemos el post con menor número de respuestas, acá omitiré los que no recibieron respuestas:

min_answers = dposts['answer_count'][dposts['answer_count']!=0].min()


dposts[dposts['answer_count']==min_answers].shape[0]


dposts[dposts['answer_count']==min_answers]


# # Actividad 4: Obtener la respuesta más vieja y más actual

# Transformamos la columna 'creation_date' que está en formato timestamp a un formato más amigable: "AAAA-MM-DD HH:MM:SS"

dposts['creation_date_fix'] = dposts['creation_date'].map(dt.fromtimestamp)


# Obtenemos el post más antiguo:

oldest_date = dposts['creation_date_fix'].min()

dposts[dposts['creation_date_fix'] == oldest_date]


# Y el más reciente:

most_recent_date = dposts['creation_date_fix'].max()
dposts[dposts['creation_date_fix'] == most_recent_date]


# # Actividad 5: Obtener la respuesta del owner que tenga una mayor reputación

# **NOTA**: Esta actividad no le entendí del todo, porque me pide la respuesta del owner con mayor reputación pero entiendo que solo viene el post del owner.

# Para tomar la información del owner, crearé un dataframe nuevo:

downer = pd.DataFrame(dposts['owner'].tolist())


# **NOTA:** Le agrego una "d" al inicio de la variable *owner* porque así sé que es un dataframe.

# Y este es el owner con mejor reputación:

max_reputation = downer['reputation'].max()
downer[downer['reputation'] == max_reputation]


# De acá tomaré su nombre para obtener los posts relacionados con el owner:

owner_max_reputation = downer['display_name'][downer['reputation'] == max_reputation].squeeze()


dposts[dposts['owner'].apply(lambda x: x['display_name']==owner_max_reputation)]


# # Actividad 6: Imprimir en consola del punto 2 al 5

print('2. Obtener el número de respuestas contestadas y no contestadas.')
print('\n\t- Número de posts que recibieron respuesta:', answered, '\n\t- Número de posts que no recibieron respuesta', not_answered)
print('\n','*'*66, '\n')

print('3. Obtener la respuesta con menor número de vistas.')
print('\n\t El menor número de respuestas obtenidas (omitiendo el cero) es:', min_answers)
print('\n\t Provenientes de los siguientes posts:')
[print('\t\t- ' + t) for t in dposts['title'][dposts['answer_count']==min_answers].values]
print('\n','*'*66, '\n')

print('4. Obtener la respuesta más vieja y más actual.\n')
[print('\t- ' + dt.strftime(r[1], '%d/%m/%Y-%H:%M') + ' - ' + r[2]) for r in dposts[['creation_date_fix', 'title']][dposts['creation_date_fix'] == oldest_date].itertuples()]
[print('\t- ' + dt.strftime(r[1], '%d/%m/%Y-%H:%M') + ' - ' + r[2]) for r in dposts[['creation_date_fix', 'title']][dposts['creation_date_fix'] == most_recent_date].itertuples()]
print('\n','*'*66, '\n')

print('5. Obtener la respuesta del owner que tenga una mayor reputación.\n')
print('\t- ' + owner_max_reputation + ': ' + dposts['title'][dposts['owner'].apply(lambda x: x['display_name']==owner_max_reputation)].squeeze())