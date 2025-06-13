from fastapi import FastAPI,Path ,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
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

class Patient_Update(BaseModel):
        name:Annotated[Optional[str],Field(default=None)]
        city:Annotated[Optional[str],Field(default=None)]
        age:Annotated[Optional[int],Field(default=None,gt=0)]
        gender:Annotated[Optional[Literal['Male','Female']],Field(default=None)]
        height:Annotated[Optional[float],Field(default=None,gt=0)]
        weight:Annotated[Optional[float],Field(default=None,gt=0)]



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


# END POINT FOR UPDATING PATIENT DETAIL
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:Patient_Update):
    data=load_data()
    if patient_id not in data :
        raise HTTPException(status_code=404,detail='Patient not found')
    
    exisiting_patient_info=data[patient_id]

    # converting the pydantic model Patient_update into dictonary and will use model_dump(exclude_unset=True) because of this only which user want to update that will include in the list otherwise all with the default none value would be included
    updated_patient_info= patient_update.model_dump(exclude_unset=True)
    for key,value in updated_patient_info.items():
        exisiting_patient_info[key]=value
    
    # data[patient_id]=exisiting_patient_info (but with this BMI and Verdict wont be getting updated so...)
    # how to solve that problem 
    # exisiting_patient_info -> pydantic object ->update bmi and verdict -> pydantic object ->dict


    # exisiting_patient_info -> pydantic object
    exisiting_patient_info['id']=patient_id
    patient_pydantic_obj=Patient(**exisiting_patient_info)
    # pydantic obj to DICT
    exisiting_patient_info=patient_pydantic_obj.model_dump(exclude='id')

    # add this dict to ada
    data[patient_id]=exisiting_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient updated'})



    

# Delete Endpoint
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id:str):
    data =load_data()

    if patient_id  not in data:
        raise HTTPException(status_code=404,detail='Patient id is not valid')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'Patient deleted'})