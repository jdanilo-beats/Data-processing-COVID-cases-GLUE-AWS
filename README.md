# Data-processing-COVID-cases-GLUE-AWS

En este proyecto se hara el procesamiento de datos por capas de casos de COVID por paises, se tiene archivos .csv de casos y countries que se ingestaran en la capa RAW de un bucket de S3 activando el trigger para ejecutar la funcion lambda y crear las tablas logicas "casos" y "countries" en Glue Data Catalog mediante los CRAWLER creados. Seguidamente mediante un JOB creado en Glue Studio se procedera a enviar las tablas de "casos" y "countries" a la capa STAGE en formato PARQUET, posteriormente con ATHENA se procedera a realizar transformaciones para crear un solo TABLON de las 2 tablas de las variables de interes llamado "casos_countries" y se enviara a la capa ANALYTICS para su posterior analisis, para la creacion de dashboards e identificar insights de valor.


## Arquitectura realizada
<p align="center">
  <img width="1000" height="650" src="Images/architecture.jpg">
</p>


##  PROCEDIMIENTO

## Creacion de recursos con CLOUDFORMATION con la plantilla YAML

 - Se procede a crear los buckets para las capas RAW, STAGE, ANALYTICS, así como un 4to bucket para guardar los logs de Athena.
 - Se crea las bases de datos RAW,STAGE,ANALYTICS en GLUE
 - Se crea tambien el rol para que el Crawler de GLUE pueda tener acceso a los servicios
 - Tambien se le da permisos para invocar funciones lambda en el bucket raw donde se almacenará la informacion primero. Para transformar la informacion de formato .csv    a formato parquet.   Tambien se coloca el rol que necesita lambda para funcionar sobre GLUE y S3. 

<p align="center">
  <img width="460" height="580" src="Images/yaml.jpg">
</p>

- Se indica la funcion de lambda en formato zip, donde se encuentra el script en Python que permite ver los eventos o triggers en el bucket, si el archivo que se         ingeste en “casos” iniciará el crawler  RAWCasosCovid o si el archivo es ingestado en “countries” llamara al crawler RawCountries.
- Finalmente se crean los crawler y se define los permisos para que se pueda escribir en las capas RAW, STAGE y ANALYTICS

<p align="center">
  <img width="460" height="580" src="Images/yaml2.jpg">
</p>

## EJECUCION
Se ejecuta la plantilla yaml
aws cloudformation create-stack --stack-name StackDatalake --template-body file://Datalake.yaml --capabilities CAPABILITY_NAMED_IAM

##  Crawlers creados

<p align="center">
  <img width="650" height="350" src="Images/crawlerscreados.jpg">
</p>

##  Buckets creados

<p align="center">
  <img width="750" height="450" src="Images/bucketscreadoss3.jpg">
</p>

##  Funcion Lambda creada

<p align="center">
  <img width="650" height="740" src="Images/lambdafunction.jpg">
</p>

## Trigger de la funcion
Esta se activara cuando el archivo que se ingeste un archivo en la carpeta “casos” iniciará el crawler  RAWCasosCovid o si se ingesta un archivo en la carpeta “countries” llamara al crawler RawCountries.
<p align="center">
  <img width="650" height="350" src="Images/triggerS3.jpg">
</p>

##  Se realiza la Carga de CSV
Una vez ingestados los archivos csv se procede a activar el trigger y se ejecuta la funcion lambda y los crawler de GLUE

<p align="center">
  <img width="650" height="350" src="Images/casos.csv.jpg">
</p>
<p align="center">
  <img width="650" height="350" src="Images/countries.csv.jpg">
</p>

##  CREACION DE TABLAS LOGICAS
Al iniciarse los CRAWLERS analizan la metadata y el esquema de los archivos  para crear las tablas logicas "casos" y "countries" en GLUE en la ubicacion de la capa RAW en S3

<p align="center">
  <img width="650" height="350" src="Images/tablascreadasGlue.jpg">
</p>


## Creacion y Ejecucion de JOB en GLUE STUDIO
Se crea un JOB en Glue Studio para realizar la transformacion de las tablas de la capa RAW a formato PARQUET y almacenarlos en el bucket de destino de la capa STAGE en S3.
<p align="center">
  <img width="750" height="600" src="Images/jobsGluetoS3.jpg">
</p>

## Archivo PARQUET en la capa STAGE

<p align="center">
  <img width="650" height="350" src="Images/S3stageparquet.jpg">
</p>


## Ejecucion de CRAWLER STAGE
Este Crawler se ejecuta para poder analizar la metadata de los archivos PARQUET en la capa STAGE de S3 para luego crear las tablas logicas en el Data Catalog de Glue.

<p align="center">
  <img width="650" height="350" src="Images/Crawlerstage.jpg">
</p>


## Configuracion de ubicacion de LOGS en ATHENA
Se tiene que indicar el bucket donde ATHENA almacenará los logs por cada consulta

<p align="center">
  <img width="600" height="400" src="Images/athenabucket.jpg">
</p>

## Creacion de Queries en ATHENA
Se abre el servicio ATHENA donde se observa como Data Source el "DataCatalog de GLUE" y en bases de datos estan las 3 bases de datos para cada capa RAW, STAGE y ANALYTICS en la cual se pueden realizar consultas

<p align="center">
  <img width="300" height="300" src="https://user-images.githubusercontent.com/105177541/210435082-f2bda77d-1c06-49ef-a3eb-1faa24483215.png">
</p>

Se procede a realizar una query en la capa STAGE de la tabla CASOS

<p align="center">
  <img width="750" height="650" src="Images/queryathena.jpg">
</p>

## Creacion de tabla analitica en CAPA ANALYTICS

En ATHENA se realiza la creacion de un TABLON "casos_countries" en formato PARQUET que viene de la union (inner join) de las 2 tablas logicas "casos" y "countries" seleccionando las variables de interes, el cual se envia a la CAPA ANALYTICS para su consumo en la creacion de DASHBOARDS o de Modelos Predictivos.

<p align="center">
  <img width="820" height="670" src="Images/analyticstable.jpg">
</p>


## Se muestran las tablas logicas creadas en GLUE

<p align="center">
  <img width="850" height="400" src="https://user-images.githubusercontent.com/105177541/210439747-096f5fe1-0de6-4542-b2a2-67a7be659855.png">
</p>


## Bucket de la capa ANALYTICS en S3
Se muestra la tabla "casos_countries" almacenada en formato PARQUET

<p align="center">
  <img width="800" height="550" src="Images/analyticsparquet.jpg">
</p>


## Query en la tabla "casos_countries"

<p align="center">
  <img width="750" height="650" src="Images/queryathenaanalytics.jpg">
</p>

## Creacion de DASHBOARD en POWER BI
Se realiza la conexion de ATHENA con POWER BI para exportar la tabla "casos_countries" y poder realizar un DASHBOARD y analizar indicadores clave.

<p align="center">
  <img width="1050" height="450" src="Images/powerbi1.jpg">
</p>

## DASHBOARD CASOS COVID-19 en el MUNDO en 2020-2021
Se muestra informacion relacionada al covid en el mundo, obteniendo datos sobre el total de casos por trimestre, el total de muertes por año, el total de nuevos casos por pais en estos 2 ultimos años.

<p align="center">
  <img width="1200" height="750" src="CASOS_COVID_DASHBOARD.jpg">
</p>























