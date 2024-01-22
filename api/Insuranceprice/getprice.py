import joblib
import pandas as pd


# if you are getting the error TypeError: __randomstate_ctor() takes from 0 to 1 positional arguments but 2 were given it is because the 
# model was trained with an older version of python. To fix this error, you need to retrain the model ( go into the junpiter notebook 
# and run the code again)
mdl = joblib.load(r'C:\Users\mdame\app-dev\api\Insuranceprice\model.joblib')

columns = ['age','gender','blue collar or white collar','Doing Sports','education','Vacations','phone price']

def getprice(data,price):
    processeddata = pd.DataFrame([data], columns=columns)
    processeddata['gender'] = processeddata['gender'].replace(['Female','Male'],[0,1])
    processeddata['education'] = processeddata['education'].replace(['Associate degree','High school diploma or equivalent','Some college, no degree','Less than high school','Bachelor’s degree','Doctoral degree','Master’s degree'],
[1,0,0,0,1,1,1])
    processeddata = processeddata.values
    factor = mdl.predict(processeddata)
    factor -= 7.48 
    return price * factor

