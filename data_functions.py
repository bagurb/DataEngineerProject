from random import randint
from pymongo import MongoClient
import pandas as pd
import json
import datetime
import re
import unicodedata
import os

######## FUNCTIONS FOR MAIN #########
datas_name = ["Apple.csv","Activision_Blizzard.csv","Amazon.csv","Intel.csv","Microsoft.csv","Netflix.csv","NVIDIA.csv","Sanofi.csv","Tesla.csv","Texas_Instruments.csv"]
dataframes = []
### SCRAP FUNCTIONS ###

def scrap():
    try:
        os.remove("Datas/article.json")
    except Exception as e:
        print(e)
    os.system("scrapy crawl article_spider")


### MONGODB FUNCTIONS ###

def new_mongoClient(db_url='localhost',db_port = 27017):
    client = MongoClient(db_url,db_port)
    return client

### DATA TRAITMENT FUNCTIONS ###   

def add_society():
    for csv in datas_name:
        data = pd.read_csv("Datas/Raw_Datas/"+ csv)
        data = data.assign(Society=(csv.replace(".csv","")))
        data["Close/Last"] = data["Close/Last"].str.replace("$","").astype(float)
        dataframes.append(data)

def merge_datas():
    final_data = pd.concat(dataframes)
    final_data = final_data.dropna()
    try:
        os.remove("Datas/data.csv")
    except Exception as e:
        print(e)
    final_data.to_csv("Datas/data.csv")

def data_traitments():
    add_society()
    merge_datas()

def csv_to_mongodb(mongo_Collection,csv_path):
    
    data = pd.read_csv(csv_path)
    data_json = json.loads(data.to_json(orient='records'))
    mongo_Collection.drop()
    mongo_Collection.insert_many(data_json)

def article_traitments(mongo_Collection):
    with open('Datas/article.json', encoding="utf-8") as json_file:
        articles = json.load(json_file)

        for article in articles:
            new_string = ""
            new_title = ""
            new_society = ""
            for chaine in article["text"]:
                new_string = new_string + chaine
            text = ''.join((c for c in unicodedata.normalize('NFKD', new_string) if unicodedata.category(c) != 'Mn'))
            text = re.sub(r'[^A-Za-z0-9\-:&-à ]+', '',text)
            text = re.sub(' +', ' ',text)

            for line in article["title"]:
                new_title = new_title + line
            title = ''.join((c for c in unicodedata.normalize('NFKD', new_title) if unicodedata.category(c) != 'Mn'))
            title = re.sub(r'[^A-Za-z0-9\-:&-à ]+', '',title)
            title = re.sub(' +', ' ',title)

            for line in article["society"]:
                new_society = new_society + line
            society = ''.join((c for c in unicodedata.normalize('NFKD', new_society) if unicodedata.category(c) != 'Mn'))
            society = re.sub(r'[^A-Za-z0-9\-: ]+', '',society)
            if(society[0] == " "):
                society = society[1:]
            society = society.replace(" ","_")

            article.update({'society':society.capitalize(),'title':title,'text':text})
        mongo_Collection.drop()
        mongo_Collection.insert_many(articles)


### DASHBOARD FUNCTIONS ###

def graph_coordinates(society_name,mongo_Collection):
    query = mongo_Collection.find({"Society":society_name}, {"Date":1,"Close/Last":1}).sort([("Date",-1)])
    x = [datetime.datetime.strptime(date["Date"],"%m/%d/%Y").date() for date in query]
    query = query.rewind()
    y = [y["Close/Last"]for y in query]
    query.close()
    return {"x":x,"y":y}

def min_max_history(society_name,mongo_Collection):
    query = mongo_Collection.aggregate([{"$match":{"Society":society_name}},
    {"$group":{"_id":"Close/Last","avg":{"$avg":"$Close/Last"},"min":{"$min":'$Close/Last'},"max":{"$max":"$Close/Last"}}}])
    return next(query)

def recup_article(society_name,mongo_Collection):
    query = mongo_Collection.find({"society":society_name})
    rand = randint(0,len(list(query))-1)
    query.rewind()
    return query[rand]

def mongo_to_df(cursor):
    datas = []
    for data in cursor:
        data.pop('_id')
        data.pop('Unnamed: 0')
        datas.append(data)
    return pd.DataFrame(datas)









