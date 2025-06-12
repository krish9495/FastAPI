from fastapi import FastAPI,Path ,HTTPException,Query
import json

app=FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data =json.load(f)
    return data

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get("/about")

def about():
    return {'message':'A Fully Functional API to maintain your patient record'}

@app.get('/view')
def view():
    data=load_data()
    return data

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str =Path(..., description='ID of the Patient in the DB',example='P001')):
    #load all the patients
    data=load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Data not found')

@app.get('/sort')
def sort_patient(sort_by : str=Query(...,description='Sort on the basis of height,weight or BMI'),order:str=Query('asc',description='Sort in asecending or desending order')):
    valid_field=['height','weight','bmi']

    if sort_by not in valid_field:
        raise HTTPException(status_code=400,detail='invalid field select properly from {valid_field}')
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalidem Order selected !! Select between "ASC","DESC" ')
    

    data = load_data()
    sort_order=True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)

    return sorted_data 
