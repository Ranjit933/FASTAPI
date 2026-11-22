from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json


app = FastAPI()

class Patient(BaseModel):
                            #(... means required)
    id: Annotated[str, Field(..., description= 'ID of the patients', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patients')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patients')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patients')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patients in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patients in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

    @computed_field
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Under Weight'
        elif self.bmi < 25:
            return 'Normal Weight'
        elif self.bmi < 30:
            return 'Normal Weight'
        else:
            return 'Obese'

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[str], Field(default=None)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

# Loading our patients data
def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)

    return data

def save_data(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {'message': "Patient Management System API"}

# To see the about sections
@app.get('/about')
def about():
    return {'message': "A fully functional API to manage your patients records"}

#To get the view of all the users
@app.get('/view')
def view():
    data = load_data()

    return data

#This code is for path parameters
@app.get('/patient/{patient_id}')
def view_patients(patient_id:str = Path(..., description='ID of the patient in the DB', example = 'P001')): #str is used because in json file patients id is in string format
    # load all the patients
    data = load_data()

    if patient_id in data: # checking the condition based on my dictionary based on specific data
        return data[patient_id]
    # return {'Error': 'Patients not found'} # If the condition not full fill then display this
    raise HTTPException(status_code=404, detail = 'Patient not found')

@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='Sort on the basis of height, weight or bmi'),
                  order: str = Query('asc',description='Sort in asc or desc order')):

    valid_fields = ['height', 'weight','bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,details=f"Invalid field select from {valid_fields}")

    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Invalid order select between asc and desc')

    data = load_data()

    sort_order = True if order =='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get('sort_by',0),reverse=sort_order)

    return sorted_data

@app.post('/create')
def create_patient(patient: Patient):

    # load exiting data
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into json file
    save_data(data)

    return JSONResponse(status_code=201, content={'Message': 'Patient created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

        #existing_patient_info -> pydantic object -. update bmi + verdict 
        existing_patient_info['id'] = patient_id
        patient_pydantic_obj = Patient(**existing_patient_info)

        #-> pydantic object -> dict
        existing_patient_info = patient_pydantic_obj.model_dump(exclude='id')

        # add this dict to data
        data[patient_id] = existing_patient_info

        # save data 
        save_data(data)

        return JSONResponse(status_code=200, content={'Message': 'Patient updated'})

@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'Message': 'patient deleted sucessfully'})
