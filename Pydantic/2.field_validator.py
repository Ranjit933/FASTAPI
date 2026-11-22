from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: List[str]
    contact_details: Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):

        valid_domins = ['hdfc.com', 'icici.com']
        #abc@gmail.com
        domin_name = value.split('@')[-1]

        if domin_name not in valid_domins:
            raise ValueError('Not a valid domin')

        return value

    @field_validator('name')
    @classmethod
    def transsform_name(cls,value):
        return value.upper()

    @field_validator('age', mode='after')
    @classmethod
    def validate_age(cls,value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be in between 0 and 100')

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print("Update")

patient_info = {'name': 'Ranjit','email': 'abc@hdfc.com','age': '29','weight':75.2,'married':True,'allergies':['Asthma','Dust'],'contact_details':{'phone':'2356478'}}

patient1 = Patient(**patient_info)

update_patient_data(patient1)