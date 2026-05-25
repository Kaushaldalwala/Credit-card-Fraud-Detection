from fastapi import FastAPI, Path, Query, HTTPException
import json
from pydantic import BaseModel, field_validator ,model_validator


class Patient(BaseModel):
    name:str
    age :int = 93
    email : str 
    password: str
    confirm_password: str
    
    @field_validator('age')
    def check_age(cls,value):
        if value < 18:
            raise ValueError("Age can't be less than 18")
        return "doneee "

    @model_validator(mode='after')
    def pass_match(cls,model):
        if model.password != model.confirm_password:
            raise ValueError("Enter the same pass word ")
        return "oyee e "

p1 = Patient(name="Ashok",age=8,email="ssr@kohli.com",password="smdv",confirm_password="smdv")
print(p1)
p1.name = "Jayesh"

p1.email = "kohli@gmail.com"
print(p1)
app = FastAPI()

@app.get("/hello")
def hello():
    return {"message": "Hello World"}

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)
        return data

@app.get("/get_info/{patient_id}")
def load_patient_info(
    patient_id: str = Path(..., description="ID of the patient", example="P001")
):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )

@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort by patient's height, weight or bmi"),
    order_by: str = Query(..., description="Enter asc or desc")
):

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Please select from valid fields: {valid_fields}"
        )

    if order_by not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Please select either 'asc' or 'desc'"
        )

    data = load_data()

    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=True if order_by == "desc" else False
    )

    return sorted_data