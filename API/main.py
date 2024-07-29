# Importamos las bibliotecas necesarias
import pandas as pd  # Para la manipulación y análisis de datos
# Para crear la API y manejar excepciones
from fastapi import FastAPI, HTTPException
# Para la transformación de texto en características TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
# Para calcular la similitud del coseno
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn  # Para ejecutar la aplicación FastAPI

# Inicializamos la aplicación FastAPI
app = FastAPI()

# Cargamos el archivo CSV con los datos una sola vez
# Este paso es importante para evitar la carga repetida de datos en cada solicitud
data = pd.read_csv('API/data_final_ML.csv')
# Convertimos la columna 'release_date' a tipo datetime para facilitar el trabajo con fechas
data['release_date'] = pd.to_datetime(data['release_date'], errors='coerce')

# Preprocesamiento de datos
# Definimos stopwords personalizadas para el vectorizador TF-IDF
stopwords_custom = ["the", "and", "in", "of"]
# Inicializamos el vectorizador TF-IDF
tfidf = TfidfVectorizer(stop_words=stopwords_custom)
# Transformamos los títulos de las películas en una matriz TF-IDF
tfidf_matrix = tfidf.fit_transform(data['title'])
# Calculamos la similitud del coseno entre los títulos de las películas para recomendaciones
cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
# Creamos un índice para acceder rápidamente a las películas por su título
indices = pd.Series(data.index, index=data['title']).drop_duplicates()

# Diccionarios para meses y días, utilizados en la validación de las entradas
meses = {name: num for num, name in enumerate(
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"], start=1)}
dias = {name: num for num, name in enumerate(
    ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"])}


def validate_time_unit(unit, unit_dict):
    """
    Valida que la unidad de tiempo (mes o día) proporcionada esté en el diccionario correspondiente.
    Si no se encuentra, lanza una excepción HTTP 404.

    :param unit: Nombre del mes o día a validar
    :param unit_dict: Diccionario de meses o días
    """
    if unit not in unit_dict:
        raise HTTPException(
            status_code=404, detail=f"{unit.capitalize()} no encontrado")


@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    """
    Endpoint para obtener la cantidad de películas estrenadas en un mes específico.

    :param mes: Nombre del mes (en español)
    :return: Número de películas estrenadas en el mes
    """
    mes = mes.lower()  # Normalizamos el mes a minúsculas
    validate_time_unit(mes, meses)  # Validamos el mes
    # Contamos el número de películas estrenadas en el mes especificado
    count = data[data['release_date'].dt.month == meses[mes]].shape[0]
    return {f'{count} cantidad de películas fueron estrenadas en el mes de {mes}'}


@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    """
    Endpoint para obtener la cantidad de películas estrenadas en un día específico.

    :param dia: Nombre del día (en español)
    :return: Número de películas estrenadas en el día
    """
    dia = dia.lower()  # Normalizamos el día a minúsculas
    validate_time_unit(dia, dias)  # Validamos el día
    # Contamos el número de películas estrenadas en el día de la semana especificado
    count = data[data['release_date'].dt.dayofweek == dias[dia]].shape[0]
    return {f'{count} cantidad de películas fueron estrenadas en los días {dia}'}


@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str):
    """
    Endpoint para obtener el score (popularidad) de una película por su título.

    :param titulo: Título de la película
    :return: Información sobre la película y su popularidad
    """
    film = data[data['title'].str.lower() == titulo.lower()
                ]  # Buscamos la película por título
    if film.empty:
        # Manejo de error si no se encuentra la película
        raise HTTPException(status_code=404, detail="Película no encontrada")
    film_info = film.iloc[0]  # Obtenemos la información de la película
    return {f'La película {film_info["title"]} fue estrenada en el año {int(film_info["release_year"])} con un score/popularidad de {float(film_info["popularity"])}'}


@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str):
    """
    Endpoint para obtener la cantidad de votos y el promedio de votos de una película por su título.

    :param titulo: Título de la película
    :return: Información sobre los votos de la película
    """
    film = data[data['title'].str.lower() == titulo.lower()
                ]  # Buscamos la película por título
    if film.empty:
        # Manejo de error si no se encuentra la película
        raise HTTPException(status_code=404, detail="Película no encontrada")
    film_info = film.iloc[0]  # Obtenemos la información de la película
    # Verificamos si la película tiene al menos 2000 votos
    if film_info['vote_count'] < 2000:
        return {"mensaje": "La película no cumple con la condición de tener al menos 2000 valoraciones"}
    # Retornamos la información de la película en formato de texto
    return {f'La película {film_info["title"]} fue estrenada en el año {int(film_info["release_year"])}. La misma cuenta con un total de {int(film_info["vote_count"])} valoraciones, con un promedio de {float(film_info["vote_average"])}'}


@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    """
    Endpoint para obtener información sobre un actor y las películas en las que ha participado.

    :param nombre_actor: Nombre del actor
    :return: Información sobre el actor y su participación en películas
    """
    # Buscamos las películas en las que ha participado el actor, ignorando mayúsculas y NaN
    films_actor = data[data['names_actors'].str.contains(
        nombre_actor, case=False, na=False)]
    if films_actor.empty:
        # Manejo de error si no se encuentra el actor
        raise HTTPException(status_code=404, detail="Actor no encontrado")
    # Contamos la cantidad de películas
    cantidad_peliculas = films_actor.shape[0]
    # Calculamos el retorno total y el promedio de retorno de las películas del actor
    retorno_total = films_actor['return'].sum()
    promedio_retorno = retorno_total / \
        cantidad_peliculas if cantidad_peliculas > 0 else 0  # Manejo de división por cero
    return {f'El actor {nombre_actor} ha participado en {cantidad_peliculas} filmaciones, con un retorno de {float(retorno_total)} y un promedio de {float(promedio_retorno)} por filmación'}


@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    """
    Endpoint para obtener información sobre un director y las películas que ha dirigido.

    :param nombre_director: Nombre del director
    :return: Información sobre el director y sus películas
    """
    # Buscamos las películas dirigidas por el director, ignorando mayúsculas y NaN
    films_director = data[data['name_director'].str.contains(
        nombre_director, case=False, na=False)]
    if films_director.empty:
        # Manejo de error si no se encuentra el director
        raise HTTPException(status_code=404, detail="Director no encontrado")
    # Calculamos el retorno total de las películas del director
    retorno_total = films_director['return'].sum()
    resultado = {
        "director": nombre_director,
        "retorno_total": float(retorno_total),
        "peliculas": [
            {
                "titulo": row['title'],
                "fecha_lanzamiento": row['release_date'],
                "retorno_individual": float(row['return']),
                "costo": float(row['budget']),
                "ganancia": float(row['revenue'])
            }
            # Recolectamos información detallada de cada película dirigida por el director
            for _, row in films_director.iterrows()
        ]
    }
    return resultado


@app.get("/recomendacion/{titulo}")
def recomendacion(titulo: str):
    """
    Endpoint para recomendar películas similares basadas en el título proporcionado.

    :param titulo: Título de la película
    :return: Lista de títulos de películas recomendadas
    """
    # Verificar si el título está en el DataFrame
    if titulo not in indices:
        # Manejo de error si no se encuentra la película
        raise HTTPException(status_code=404, detail="Película no encontrada")
    idx = indices[titulo]  # Obtenemos el índice de la película
    # Obtenemos las películas más similares (excluyendo la misma película)
    sim_scores = sorted(
        enumerate(cosine_similarities[idx]), key=lambda x: x[1], reverse=True)[1:6]
    # Extraemos los índices de las películas similares
    movie_indices = [x[0] for x in sim_scores]
    # Retornamos la lista de títulos recomendados
    respuesta_recomendacion = data['title'].iloc[movie_indices].tolist()
    return {'lista recomendada': respuesta_recomendacion}


# Ejecutamos el servidor de FastAPI con Uvicorn
if __name__ == "__main__":
    # El servidor se ejecuta en todas las interfaces de red en el puerto 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
