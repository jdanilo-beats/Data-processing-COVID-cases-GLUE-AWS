import json
import boto3
import sys, os

glue = boto3.client("glue")

def lambda_handler(event, context):
    
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_object = event['Records'][0]['s3']['object']['key']
    
    parse_id_source = s3_object.split('/')[3]
    if parse_id_source == 'casos':
      glue.start_crawler(Name = 'RawCasosCovid')
    elif parse_id_source == 'countries':
      glue.start_crawler(Name = 'RawCountries')   
      
    return {
        'statusCode': 200,
        'body': json.dumps('Crawler en ejecución')
    }
