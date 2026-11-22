
#Example.1(It is a lendy process) -> ############################################################################################
# def insert_patient_data(name: str, age: int):

#     if type(name) == str and type(age) == int:
#             if age < 0:
#                   raise ValueError("Age can't be negative")
#             else:
#                   print(name)
#                   print(age)
#                   print("Inserted into database")
#     else:
#           raise TypeError("Incorrect data type")


# insert_patient_data('Ranjit',29)

# def update_patient_data(name: str, age: int):

#       if type(name) == str and type(age) == int:
#             print(name)
#             print(age)
#             print("Updated into database")
#       else:
#             raise TypeError()

############################################################################################

from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50, title='Name of the patient',description='Give the name of a patients in less then 50 characters',example=['Kiwi','Ranjit'])]
    email: EmailStr
    linkedin_url: AnyUrl
    age:  int = Field(gt=0,lt=120)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: Annotated[bool, Field(default=None, description="Is the patients married or not")]
    allergies: Annotated[Optional[List[str]], Field(default = None, max_length=5)] # For optional use
    contact_details: Dict[str,str]

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Inserted")


def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
    print("Update")

#patient_info = {'name': 'Ranjit', 'age': 29,'weight':75.2, 'married':False, 'allergies': ['Asthma','dust'],'contact_details':{'email': 'abc@gmail.com', 'phone':'2356478'}}

patient_info = {'name': 'Ranjit','email': 'abc@gmail.com','linkedin_url':'http://linkedin.com/1111','age': 29,'weight':75.2,'contact_details':{'phone':'2356478'}}

patient1 = Patient(**patient_info)

#insert_patient_data(patient1)

update_patient_data(patient1)


