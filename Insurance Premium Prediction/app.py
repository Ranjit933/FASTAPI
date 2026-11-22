from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import UserInput
from Model.predict import predict_output, model, MODEL_VERSION
from schema.prediction_response import PredictionResponse


app = FastAPI()


# human readable(means human can read it API is running fine)
@app.get('/')
def home():
    return {'message': "Insurance Premium Prediction API"} 

# machine readable(AWS will understand that in claude API is working fine to display the "OK" status)
@app.get('/health')
def health_check():
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):

    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:

        prediction = predict_output(user_input)

        return JSONResponse(status_code=200, content={'response': prediction})
    except Exception as e:

        return JSONResponse(status_code=500, content=str(e))


    # predicted_class = model.predict(input_df)[0]
    # probabilities = model.predict_proba(input_df)[0]

    # class_probs = {
    #     str(cls): round(float(p), 4)
    #     for cls, p in zip(model.classes_, probabilities)
    # }

    # return JSONResponse(
    #     status_code=200,
    #     content={
    #         "response": {
    #             "predicted_category": str(predicted_class),
    #             "confidence": round(float(max(probabilities)), 4),
    #             "class_probabilities": class_probs
    #         }
    #     }
    # )
