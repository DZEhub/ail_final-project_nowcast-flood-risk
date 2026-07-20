# -*- coding=utf-8 -*-
# ============================
# IMPORT LIBRAIRIES
# ============================

# librairie HTTP pour appeler l’API
import requests
# librairie pour manipuler data
import pandas as pd
# numpy pour calculs
import numpy as np
# utilitaires et gestion dossiers et fichiers
import os
from pprint import pprint
from pathlib import Path
import sys
from dotenv import load_dotenv
from pprint import pprint
from datetime import datetime
# librairies pour se connecter à AWS S3 et manipuler les données dans le bucket
import boto3


# Absolute path of this script's folder: .../Dev/python_apps/data_collection
CURRENT_DIR = Path(__file__).resolve().parent.parent
# Add folder to import search path once
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

# 4) Import from files inside CONFIG_DIR
from config.aws_s3 import (api_get_obs_elab_ALL_data,
                            api_get_obs_elab_data, 
                            upload_file_to_s3_bucket
                    )
from config.sites import (SITES, API_BASE_URL, )


# *==========================================================================================
# *1. CONFIGURATION : aws s3
# *==========================================================================================

# ************* ATTENTION : INTERDIRE D'AFFICHER/IMPRIMER LES CREDENTIELS d'AWS S3*************
# 1. get IAM AWS credentials from env variables if they exist, otherwise use the default ones (user_access_key and user_secret_key)
# load_dotenv(dotenv_path=Path.cwd().resolve() / ".env") # load env variables from .env file in the current directory
load_dotenv() # load env variables from .env file in the current directory
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_S3_PROFILE_NAME = os.getenv("AWS_S3_PROFILE_NAME", "default")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "eu-west-3")
EXISTING_BUCKET_MAIN = os.getenv("EXISTING_BUCKET_MAIN")
S3_RESOURCE_ROOT_FOLDER = os.getenv("S3_RESOURCE_ROOT_FOLDER")
# ************* ATTENTION : INTERDIRE D'AFFICHER/IMPRIMER LES CREDENTIELS *************

# Specific folder in your s3 bucket where to store the data inside the root folder, you can change it as you want
# if the root folder <Final_Project_Forecasting> does not exist in your s3 bucket, it will be created automatically when you upload the first file to it, 
# same for the subfolder <Dataset/hubeau_api> 
S3_RESOURCE_DATA_FOLDER = f"{S3_RESOURCE_ROOT_FOLDER}/Dataset/hubeau_api"


# 2. Create an instance of `boto3.Session` that connects with your aws account.
# Create a low-level service client by name using the default session.
# A session stores configuration state and allows you to create service clients and resources
aws_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION,
    profile_name=AWS_S3_PROFILE_NAME
)

# 3. Create a variable called `s3` that connects your session to the s3 ressource.
# Create a resource service client by name: create an S3 resource using the aws session
# The resource provides an object-oriented API as well as low-level access to AWS services. See the documentation for details on the service's resource APIs.
# service_name : string. The name of a service, e.g. 's3' or 'ec2'. You can get a list of available services via get_available_resources.
s3_resource = aws_session.resource("s3")

print("S3 resource service created successfully:", s3_resource)
# Tester la connexion en listant les buckets de votre compte S3 resource
print("\nBuckets in your S3 resource:", s3_resource.buckets.all())
# List all buckets in your S3 ressources service
print("\nBuckets in your S3 resource:")
for bucket in s3_resource.buckets.all():
    print(f" - ressource - Bucket: {bucket.name}")

# 4. Create a variable will connect to an existing bucket in your s3 or to a bucket you are creating now.
# Create a bucket resource object for the existing bucket using the s3 resource
S3_BUCKET_RESOURCE = s3_resource.Bucket(EXISTING_BUCKET_MAIN)

print(f"\nCalling the bucket object: {S3_BUCKET_RESOURCE}")
print(f"Using Bucket Name: {S3_BUCKET_RESOURCE.name}")
print(f"Bucket Creation Date: {S3_BUCKET_RESOURCE.creation_date}")
# print(f"Bucket ACL: {S3_BUCKET_RESOURCE.Acl()}")

# 5. list all objects in the bucket to check if the connection is successful and to see the existing files in the bucket
# Final_Project_Forecasting/Dataset/hubeau_api
print(f"\nObjects in the bucket {S3_BUCKET_RESOURCE.name}:")
# for obj in S3_BUCKET_RESOURCE.objects.all():
#     if obj.key.startswith(S3_RESOURCE_DATA_FOLDER):
#         print(f" - object - Key: {obj.key}, Size: {obj.size} bytes, Last Modified: {obj.last_modified}")
#         print(f"   URI: s3://{S3_BUCKET_RESOURCE.name}/{obj.key}")


# *==========================================================================================
# *2. ETL: Collecte et stockage des données brutes et nettoyées dans AWS S3
# *==========================================================================================

# get today's date in the format YYYY-MM-DD
DATE_TODAY = datetime.now().strftime("%Y-%m-%d")

# choose the storage folder in your s3 bucket where to upload the json and csv files
S3_STORAGE_ALL = f"{S3_RESOURCE_DATA_FOLDER}/ALL/{DATE_TODAY}"
S3_STORAGE_VARS = f"{S3_RESOURCE_DATA_FOLDER}/VARS/{DATE_TODAY}"

# delete the existing files in the S3 bucket folder if they exist, to avoid duplicates
# delete all objects in the S3 bucket folder for ALL and VARS
for obj in S3_BUCKET_RESOURCE.objects.all():
    if obj.key.startswith(S3_STORAGE_ALL) or obj.key.startswith(S3_STORAGE_VARS):
        S3_BUCKET_RESOURCE.delete_objects(Delete={"Objects": [{"Key": obj.key}]})
        print(f"Deleted object: {obj.key}")

# période souhaitée (historique):  time period
# les formats de date (ISO 8601) supportés : yyyy-MM-dd, yyyy-MM-dd'T'HH:mm:ss, yyyy-MM-dd'T'HH:mm:ssXXX, exemples : 2018-12-01, 2018-12-11T00:00:01, 2018-12-11T00:00:01Z
# DATE_DEBUT_OBS, DATE_FIN_OBS = ("2007-01-01", "2026-06-15")
DATE_DEBUT_OBS, DATE_FIN_OBS = ("2007-01-01", DATE_TODAY)

# créer dossier data en LOCAL pour stocker les données récupérées de l'API en local avant de les uploader dans le bucket s3 --- IGNORE ---
DATA_LOCAL_STORAGE_DIR = None #  "./data", default =None, if None or "" or False or 0, the data will not be stored locally but only uploaded to s3
# if not Path(DATA_LOCAL_STORAGE_DIR).exists():
#     Path(DATA_LOCAL_STORAGE_DIR).mkdir(parents=True, exist_ok=True)

ALL_DATABASE_dict = {"site_name":[], "code_site":[], "code_station":[], "df":[], "csv_file":[], "json_file":[], "s3_csv_uri":[], "s3_json_uri":[]}
VAR_DATABASE_dict = {"site_name":[], "code_site":[], "code_station":[], "Measure":[], "df":[], "csv_file":[], "json_file":[], "s3_csv_uri":[], "s3_json_uri":[]}

for site_name in SITES:
    code_site = SITES[site_name]["code"]
    site_region = SITES[site_name]["region"]
    for station in SITES[site_name]["stations"]:
        code_station = station["code"]
        print(f"============ {site_name} \t: {code_site} \t: {code_station} ============")
        
        # *++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Export toutes les grandeurs hydrométriques élaborées dans un même fichier csv pour chaque station
        # get all data at once:
        # *++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        data1_df, csv_output1_filename, \
            json_output1_filename, s3_csv1_uri, s3_json1_uri = api_get_obs_elab_ALL_data(API_BASE_URL, code_site, code_station, site_name=site_name,
                                                                date_debut_obs=DATE_DEBUT_OBS, date_fin_obs=DATE_FIN_OBS, 
                                                                local_data_dir=DATA_LOCAL_STORAGE_DIR,
                                                                save_in_aws_s3=True, s3_bucket_resource=S3_BUCKET_RESOURCE, s3_storage_vars=S3_STORAGE_ALL)
        # # save to DATABASE dict
        ALL_DATABASE_dict["site_name"].append(site_name)
        ALL_DATABASE_dict["code_site"].append(code_site)
        ALL_DATABASE_dict["code_station"].append(code_station)
        ALL_DATABASE_dict["df"].append(data1_df)
        ALL_DATABASE_dict["csv_file"].append(csv_output1_filename)
        ALL_DATABASE_dict["s3_csv_uri"].append(s3_csv1_uri)
        ALL_DATABASE_dict["json_file"].append(json_output1_filename)
        ALL_DATABASE_dict["s3_json_uri"].append(s3_json1_uri)
        
        # # TRANSFORM the data1_df DataFrame to have a single column for each hydrometric measure, with the date as the index
        # data1_df_pivoted = data1_df.pivot(index="date_obs_elab", columns="grandeur_hydro_elab", values="valeur_obs_elab")
        # # Reset the index to have the date as a column instead of the index
        # data1_df_pivoted.reset_index(inplace=True)
        # # Save the pivoted DataFrame to a CSV file locally and upload it to S3
        # pivoted_csv_filename = f"pivoted_hubeau_obs_elab_{site_name}_{code_site}_{code_station}_ALL_{DATE_DEBUT_OBS}_{DATE_FIN_OBS}.csv"
        # pivoted_csv_filepath = Path(DATA_LOCAL_STORAGE_DIR) / pivoted_csv_filename if DATA_LOCAL_STORAGE_DIR else Path(pivoted_csv_filename)
        # data1_df_pivoted.to_csv(pivoted_csv_filepath, index=False)
        # # UPLOAD the pivoted CSV file to S3
        # s3_pivoted_csv_uri = upload_file_to_s3_bucket(pivoted_csv_filepath, S3_BUCKET_RESOURCE, f"{S3_STORAGE_ALL}/cleaned_pivoted_2")
        # print(f"Pivoted CSV file uploaded to S3: {s3_pivoted_csv_uri}")
        
        # *++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # Exporter chaque grandeur hydrométrique élaborée dans un fichier csv séparé pour chaque station
        # get data by grandeur and merge on date_obs_elab to have a final dataframe with all the hydrometric grandeurs elaborated
        # *++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        for grandeur in ("HIXM", "HIXnJ", "QINM", "QINnJ", "QixM", "QIXnJ", "QmM", "QmnJ"):
            print(f"Récupération données station {site_name} ({code_station}) - grandeur : {grandeur}")
            data2_df, csv_output2_filename, \
                json_output2_filename, s3_csv2_uri, s3_json2_uri = api_get_obs_elab_data(API_BASE_URL, code_site, code_station, site_name=site_name,
                                                                date_debut_obs=DATE_DEBUT_OBS, date_fin_obs=DATE_FIN_OBS, 
                                                                grandeur_hydro_elab=grandeur, local_data_dir=DATA_LOCAL_STORAGE_DIR,
                                                                save_in_aws_s3=True, s3_bucket_resource=S3_BUCKET_RESOURCE, s3_storage_vars=S3_STORAGE_VARS)
            
            # save to DATABASE dict
            VAR_DATABASE_dict["site_name"].append(site_name)
            VAR_DATABASE_dict["code_site"].append(code_site)
            VAR_DATABASE_dict["code_station"].append(code_station)
            VAR_DATABASE_dict["Measure"].append(grandeur)
            VAR_DATABASE_dict["df"].append(data2_df)
            VAR_DATABASE_dict["csv_file"].append(csv_output2_filename)
            VAR_DATABASE_dict["json_file"].append(json_output2_filename)
            VAR_DATABASE_dict["s3_csv_uri"].append(s3_csv2_uri)
            VAR_DATABASE_dict["s3_json_uri"].append(s3_json2_uri)
            
            # # TRANSFORM the data2_df DataFrame to have a single column for each hydrometric measure, with the date as the index
            # data2_df_pivoted = data2_df.pivot(index="date_obs_elab", columns="grandeur_hydro_elab", values="valeur_obs_elab")
            # # Reset the index to have the date as a column instead of the index
            # data2_df_pivoted.reset_index(inplace=True)
            # # Save the pivoted DataFrame to a CSV file locally and upload it to S3
            # pivoted_csv_filename = f"pivoted_hubeau_obs_elab_{site_name}_{code_site}_{code_station}_{grandeur}_{DATE_DEBUT_OBS}_{DATE_FIN_OBS}.csv"
            # pivoted_csv_filepath = Path(DATA_LOCAL_STORAGE_DIR) / pivoted_csv_filename if DATA_LOCAL_STORAGE_DIR else Path(pivoted_csv_filename)
            # data2_df_pivoted.to_csv(pivoted_csv_filepath, index=False)
            # # UPLOAD the pivoted CSV file to S3
            # s3_pivoted_csv_uri = upload_file_to_s3_bucket(pivoted_csv_filepath, S3_BUCKET_RESOURCE, f"{S3_STORAGE_VARS}/cleaned_pivoted_2")
            # print(f"Pivoted CSV file uploaded to S3: {s3_pivoted_csv_uri}")


# check which csv files have been uploaded to the S3 bucket in the ALL and VARS folders
for csv_file1 in ALL_DATABASE_dict["csv_file"]:
    print(f"CSV file uploaded to S3 in ALL folder: {csv_file1}")
    start_date_1, end_date_1 = csv_file1.split("_")[-2], csv_file1.split("_")[-1].split(".")[0]
    site_name_1, code_site_1, code_station_1 = csv_file1.split("_")[4], csv_file1.split("_")[5], csv_file1.split("_")[6]
    print(f"site_name: {site_name_1}, code_site: {code_site_1}, code_station: {code_station_1}, start_date: {start_date_1}, end_date: {end_date_1}: {end_date_1}=={DATE_FIN_OBS}")
    
for csv_file2 in VAR_DATABASE_dict["csv_file"]:
    print(f"CSV file uploaded to S3 in VARS folder: {csv_file2}")
    start_date_2, end_date_2 = csv_file2.split("_")[-2], csv_file2.split("_")[-1].split(".")[0]
    site_name_2, code_site_2, code_station_2 = csv_file2.split("_")[4], csv_file2.split("_")[5], csv_file2.split("_")[6]
    print(f"site_name: {site_name_2}, code_site: {code_site_2}, code_station: {code_station_2}, start_date: {start_date_2}, end_date: {end_date_2}: {end_date_2}=={DATE_FIN_OBS}")
