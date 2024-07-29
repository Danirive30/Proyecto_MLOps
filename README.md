# Proyecto: Machine Learning Operations (MLOps)

<p align="center">
  <img src="image.png" alt="alt text" width="400"/>
</p>

## Descripción del Proyecto

Este proyecto se centra en el ciclo de vida completo de un sistema de recomendación de películas, desde el procesamiento de datos hasta el despliegue de un modelo de Machine Learning en producción. Se desempeñará en el rol de un MLOps Engineer, encargado de transformar datos, desarrollar una API para consulta de datos, y entrenar un modelo de recomendación.

## Contexto

Has desarrollado un modelo de recomendación con buenas métricas, y ahora necesitas llevarlo al mundo real. El ciclo de vida de un proyecto de Machine Learning abarca desde la recolección y tratamiento de datos hasta el entrenamiento y mantenimiento del modelo a medida que llegan nuevos datos.

## Rol a Desarrollar

Trabajas como Data Scientist en una start-up de agregación de plataformas de streaming. Tu tarea es desarrollar un sistema de recomendación desde cero, enfrentándote a datos inmaduros y procesos desorganizados. Necesitas crear un MVP (Minimum Viable Product) en las próximas semanas, resolviendo problemas como datos anidados y ausencia de procesos automatizados.

## Requerimientos de Trabajo

### Transformaciones de Datos

Para el MVP, se realizaron las siguientes transformaciones en los datos:

- Desanidar campos como `belongs_to_collection`, `production_companies`, etc.
- Rellenar los valores nulos de `revenue` y `budget` con `0`.
- Eliminar las filas con valores nulos en `release_date`.
- Asegurar que las fechas estén en formato `AAAA-mm-dd` y crear una columna `release_year`.
- Crear una columna `return` calculando `revenue / budget` y asignar `0` cuando no hay datos disponibles.
- Eliminar las columnas `video`, `imdb_id`, `adult`, `original_title`, `poster_path`, y `homepage`.
- Filtar data para reducir el tamaño del archivo `data_final_ML.csv` (con el que se trabajaron los endpoints de la API).

### Desarrollo de la API

Se utilizó FastAPI para desarrollar una API con los siguientes endpoints:

1. **`/cantidad_filmaciones_mes/{Mes}`**: Devuelve la cantidad de películas estrenadas en un mes específico.
2. **`/cantidad_filmaciones_dia/{Dia}`**: Devuelve la cantidad de películas estrenadas en un día específico.
3. **`/score_titulo/{titulo_de_la_filmacion}`**: Devuelve el título, año de estreno y score de una película.
4. **`/votos_titulo/{titulo_de_la_filmacion}`**: Devuelve el título, cantidad de votos y valor promedio de votaciones para una película con al menos 2000 valoraciones.
5. **`/get_actor/{nombre_actor}`**: Devuelve el éxito de un actor, la cantidad de películas en las que ha participado y el promedio de retorno.
6. **`/get_director/{nombre_director}`**: Devuelve el éxito de un director, las películas que ha dirigido y detalles de cada una.

### Despliegue

El despliegue se realizó utilizando Render para que la API sea accesible desde la web.
- **URL Render**: 

### Análisis Exploratorio de los Datos (EDA)

Después de limpiar los datos, se realiza un análisis exploratorio para investigar relaciones entre variables, detectar outliers, y descubrir patrones interesantes. Incluye nubes de palabras para identificar términos frecuentes en los títulos.

### Sistema de Recomendación

Se entrena un modelo de recomendación que sugiera películas similares basándose en la similitud de puntuación. Implementar esta función adicional en la API:

- **`/recomendacion/{titulo}`**: Devuelve una lista de 5 películas similares a la proporcionada.

### Video de Demostración

Grabar un video de máximo 7 minutos mostrando:

- Resultados de las consultas API.
- Explicación breve del modelo de recomendación.
- Explicación de EDA, ETL y desarrollo de la API.

- **URL YouTube**: 

## Criterios de Evaluación

- **Código**: Claridad y estructura del código, uso adecuado de clases y funciones, y comentarios necesarios.
- **Repositorio**: Organización adecuada de archivos y carpetas, y un `README.md` claro y detallado.
- **Cumplimiento de Requerimientos**: Adherencia a los requisitos y propuestas del proyecto.

## Fuente de Datos

- **Dataset**: `movies_dataset.csv` y `credits.csv`.
- **Diccionario de Datos**: Descripciones de las columnas disponibles en el dataset.
- **URL Data**: https://drive.google.com/drive/folders/1_Mre-XI31f1whYUZaBF5-RnOGashkuH4?usp=drive_link

## Autor

Este proyecto fue realizado por: José Daniel Rivera Hernández. (Daniel.rivera.30@outlook.com)

---

¡Saludos! 🚀
# Proyecto_MLOps
