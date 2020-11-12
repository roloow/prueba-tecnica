# Prueba de aptitudes

Rolando Javier Casanueva Quezada

## Sección ténica

Implementación de un servicio de procesamiento que genera mensajes ante la llegada de archivos a Cloud Storage. Estos mensajes poseen la ruta del archivo a ser procesado, luego se levanta Cloud Run para el enmascaramiento de columnas `Latitude` y `Longitude` junto al particionamiento del archivo por `Country` para su posterior almacenamiento en un bucket de salida en Cloud Storage.

**Consideraciones:**
Para el desarrollo de lo siguiente se solicito la realización del contenedor y su programación mediante `SpringBoot` para el desarrollo en Java. Debido a la necesidad de afrontar la problemática de una manera efectiva y apropiada se realiza un cambio sobre esta conceptualización, variando el lenguaje de programación a Python y utilizando la librería Flask junto a Docker para levantar la imagen que se utiliza en Cloud Run. Con respecto al desarrollo perse, también existen algunas consideraciones particulares.

- El archivo particular [GlobalLandTemperaturesByCountry.csv](https://www.kaggle.com/sohelranaccselab/global-climate-change?select=GlobalLandTemperaturesByCountry.csv) no posee latitud ni longitud.
- No todos los archivos contienen la columna `Country`

Bajo esos parametros, se decidio generar una función aplicable sobre cualquier estructura de estas mencionadas, sin embargo para avanzar acorde a lo mencionado en el enunciado se procede por la utilización explicita del archivo recien mencionado.

Sobre el código:
```python
_> (...)
1>  df = pd.read_csv(path.format(bucket, key), dtype=str)
2>  for column in set(df.columns).intersection(set(encrypted_columns)):
3>    df[column] = df[column].apply(encrypt)
4>  for country, df_country in df.groupby(group):
5>    df_country.to_csv(path.format(out, country + '.csv'))
_> (...)
```

En la linea (1) se abre el contenido del archivo mediante `pandas`, aunque se comenta que podrían utilizarse opciones como `pyspark` o `dask`. La linea (2) genera un ciclo que recorre la intersección entre las columnas presentes en el archivo y las columnas *predefinidas* para ser enmascaradas, posterior a esto se aplica una función de encriptación simetrica utilizando el servicio de GCP KMS. Finalmente para el particionamiento y almacenamiento de los archivos, se realiza una agrupación por país y se recorren las agrupaciones para luego generar archivos individuales nombrados con respecto al país correspondiente.

## Sección teórica

Para responder esta pregunta podemos subdividir el comportamiento en los diversos servicios y fases que se requieren implementar. 

**Almacenamiento**
Para almacenar el archivo se debe utilizar Cloud Storage. Se considera la utilización de 2 Buckets, para su almacenamiento inicial y su posterior guardado. Considerense estos como bucket `raw` y `analitycs`

**Procesamiento**
Para el procesamiento, el servicio que se plantea utilizar, debido a la cantidad de registros que posee el archivo es GCP Dataproc, debido a sus altas capacidades de procesamiento. En él se utilizaría un ambiente Spark en el cual se utilizaría especificamente Pyspark. Esta decisión basado en la facilidad que otorga para manejar estos tipos de archivos y también las cantidades datos. Por otra parte, para la re-encriptación de columnas, se puede realizar un proceso similar al expuesto en la parte técnica, donde se genera una llave de encriptación simétrica en KMS.

**Orquestación**
Para generar el flujo y levantar los servicios de manera automática, se plantea el uso de eventos gatilladores y el SDK de GCP para el levantamiento mediante las API de los servicios. Esto quiere decir que se puede ajustar un script en GCP Functions que se gatille por la llegada de un archivo a Storage, o bien, agendado mediante algún horario, el cual levantará el servicios de Dataproc.

Otros servicios adicionales a utilizar, corresponden a GCP IAM para la generación de roles, GCP Monitoring para la gestión de recursos y la revisión de salidas.
