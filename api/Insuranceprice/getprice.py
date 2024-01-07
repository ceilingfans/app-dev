import joblib
import pandas as pd

mdl = joblib.load('api/Insuranceprice/model.joblib')

columns = ['age','gender','blue collar or white collar','Doing Sports','education','Vacations','phone price']

def getprice(data,price):
    processeddata = pd.DataFrame([data], columns=columns)
    processeddata['gender'] = processeddata['gender'].replace(['Female','Male'],[0,1])
    processeddata['education'] = processeddata['education'].replace(['Associate degree','High school diploma or equivalent','Some college, no degree','Less than high school','Bachelor’s degree','Doctoral degree','Master’s degree'],
[1,0,0,0,1,1,1])
    processeddata = processeddata.values
    factor = mdl.predict(processeddata)
    factor -= 6.48 
    return price * factor

