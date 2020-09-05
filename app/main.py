from typing import Optional, List

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from datetime import datetime
from pytz import timezone
import requests, json, os

from google.cloud import firestore, storage, logging



app = FastAPI()



class Recall(BaseModel):
    id: int
    category: List[int]
    datePublished: Optional[datetime] = None
    title: str
    url: str

recalls = {
    "id" : 73731, 
    "category" : [4, 5],
    "title": "Hi-Lift Storage Hoist Classic and Hi-Lift Storage Hoist Pro recalled due to injury hazard", 
    "url" :"/api/73731/en"
}

# This is to to get the recalls and write to the database everyday
# Cloud function run this once a day
@app.get("/write-recalls")
def write_recalls():
    db = firestore.Client()

    docs = db.collection('recalls').stream()

    recall_ids = set()
    #Store the existing recall ids in the database
    for doc in docs:
        recall_ids.add(doc.id)

    
    r = requests.get('http://healthycanadians.gc.ca/recall-alert-rappel-avis/api/recent/en')
    #Get the newest recall feeds from the API
    if r.status_code == 200:
        data = r.json()
        data_all = data['results']['ALL'] # From the ALL category
        
    
    if len(data_all) > 0: #List is not empty

        for item in data_all:
            # If the recall is not already in the database, store it
            if item['recallId'] not in recall_ids:
                data = {
                    'title': item['title'],
                    'datePublished': datetime.fromtimestamp(int(item['date_published'])),
                    'category': item['category'],
                    'url': item['url'],
                }
                doc_ref = db.collection('recalls').document(item['recallId']).set(data)
                
        return {"Data" : "is sucessfully recorded"}
    
    return {"Data" : "cannot be recorded"}

@app.get("/recalls")
def get_recalls():

   

    print('Inside Get Recalls')
    

    db = firestore.Client()
    #start_date = datetime.datetime(2020, 9, 1, 0, 0)
    #print('Start Date is', start_date)
    #doc_ref = db.collection('recalls').document('73731')
    docs = db.collection('recalls').stream()
    #doc = doc_ref.get()
    #docs = doc_ref
    for doc in docs:
        print(f'{doc.id} => {doc.to_dict()}')
    print("This is the end")
    #if docs.exists:
    #    print(f'Document data: {docs.to_dict()}')
    #else:
    #    print('No Doc Ref')
    #test_recall = Recall(id=73731, category=Category(categoryId=[4]), title="Something", url="/api/73731/en")
    #json_compatible_data = jsonable_encoder(doc.to_dict())
    #return JSONResponse(content=json_compatible_data)
    return {"Completed" : "Request'"}

 

        
# This is to confirm Google Cloud Run is working
@app.get("/")
def read_root():
    print('Testing if Deployment is working')
    return {"Hello": "World3"}

#This is to test if I can use Google Cloud Run to control other Google Services
@app.get("/test-storage")
def test_storage():
    storage_client = storage.Client()
    bucket_name = "my-new-bucket-shlfung8163"
    bucket = storage_client.create_bucket(bucket_name)
    return {"Bucket": bucket_name}

# This is to confirm I can use Cloud Functions on Google Cloud Run
@app.get("/write-time")
def write_time():
    db = firestore.Client()
    vancouver = timezone('America/Vancouver')
    now = datetime.now(vancouver)
    data = {
            'currentDateTime': str(now),

    }
    db.collection('timeRecords').document(str(now)).set(data)
    return {"Data" : "is recorded"}

