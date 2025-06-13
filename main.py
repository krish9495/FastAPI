from fastapi import FastAPI,Path ,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal
from fastapi.responses import JSONResponse
import json

app=FastAPI()
class Patient(BaseModel):
    id:Annotated[str,Field(...,description='ID of the patient',example='P001')]
    name:Annotated[str,Field(...,description='Name of the Patient')]
    city:Annotated[str,Field(...,description='Name of the City')]
    age:Annotated[int,Field(...,gt=0,lt=100,description='Age of the Patient')]
    gender:Annotated[Literal['male','female','others'],Field(...,description='Enter the gender of the Patient')]
    height:Annotated[float,Field(...,gt=0,description='Height of the Patient in mtrs')]
    weight:Annotated[float,Field(...,gt=0,description='Weight of the Patient in kgs')]

    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:
        if(self.bmi<18.5):
            return 'Underweight'
        elif(self.bmi<35):
            return 'Normal'
        else:
            return 'Obese'




def load_data():
    with open('patients.json','r') as f:
        data =json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)


# Retrieving the data from Json File
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

# Post Inserting the data given by user to json file

@app.post('/create')
def create_patient(patient:Patient):

    #load the data
    data=load_data()

    #check if patient already exist
    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient Already Exist')
    
    #add the new patient to the database
    data[patient.id]=patient.model_dump(exclude=['id'])

    #save into json file with the help a utility function
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created succesfully'})