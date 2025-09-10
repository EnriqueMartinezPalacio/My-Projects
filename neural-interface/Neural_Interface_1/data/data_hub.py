import os
import sys
import pandas as pd
import numpy as np
import sklearn.preprocessing as skp
import sklearn.model_selection as skm
import sklearn.metrics as skme
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

class DataHub:
    def __init__(self):
        self.le = LabelEncoder()
        self.ss_x = StandardScaler()
        self.ss_y = StandardScaler()

    def load_data(self, file):
        ## get the foilder sirectory
        file_route = os.path.join(os.path.dirname(os.path.abspath(__file__)),'database', file)
        data = pd.read_excel(file_route, sheet_name=0)
        print(f'Data shape_load: {data.shape}')

        return data
    
    def preprocess_data(self, data):
        data = data.dropna() # Drop missing values
        data = data.drop_duplicates() # Drop duplicates
        ##apply label encoding and standard scaling only for text columns
        for col in data.columns:
            if data[col].dtype == 'object':
                data[col] = self.le.fit_transform(data[col])

        #print data type
        #print(f'Preprocess data type: {data.dtypes}')
        print(f'Data shape_preprocess: {data.shape}')
        return data
    
    def split_data(self, data, test_size, chk_name, model, label_size):
        ## Split data into features and labels from numpy array
        x = data.iloc[:, :-label_size].values
        y = data.iloc[:, -label_size:].values
        #print(f"Y dimensions: {y.shape}")

        x = self.ss_x.fit_transform(x)
        if label_size == 1:
            y = self.ss_y.fit_transform(y.reshape(-1, 1))
        elif label_size > 1:
            y = self.ss_y.fit_transform(y)

        #save the ss_y model
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'model', 'models', 'scalers', f'{model}_m', f'{model}_{chk_name}_ss_y.pkl')
        
        joblib.dump(self.ss_y, model_path)
        
        
        print(f"Model saved in {model_path}")
       
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)

        return x_train, x_test, y_train, y_test
    
    
    def denorm_data(self, data, model, chk_name):
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'model', 'models', 'scalers', f'{model}_m', f'{model}_{chk_name}_ss_y.pkl')
        self.ss_y = joblib.load(model_path)

        data = data.reshape(-1, 1)
        data = self.ss_y.inverse_transform(data)
        
        return data
    
    def norm_data(self, data):
        data = self.ss_x.fit_transform(data)
        
        return data
    
    def process_timeseries_excel(self, window, horizon, excel_file):
        data = self.load_data(excel_file)
        ts_data = np.zeros((data.shape[0] - window - horizon + 1,((data.shape[1]-1) * window) + horizon))
        
        #full features in the time series data
        for i in range(data.shape[0] - window - horizon + 1):
            for j in range(data.shape[1] - 1):
                for k in range(window):
                    ts_data[i, j * window + k] = data.iloc[i + k, j]

            # Fill in the horizon values from the last column of `data`
            for h in range(horizon):
                ts_data[i, ((data.shape[1]-1) * window) + h] = data.iloc[i + window + h, data.shape[1] - 1]

        #print(ts_data)
        #store to excel
        ts_data = pd.DataFrame(ts_data)
        ts_data.to_excel('timeseries_data_btc.xlsx', index=False)


    def process_timeseries(self, window, horizon, data):
        
        ts_data = np.zeros((data.shape[0] - window - horizon + 1,((data.shape[1]-1) * window) + horizon))
        
        #full features in the time series data
        for i in range(data.shape[0] - window - horizon + 1):
            for j in range(data.shape[1] - 1):
                for k in range(window):
                    ts_data[i, j * window + k] = data.iloc[i + k, j]

            # Fill in the horizon values from the last column of `data`
            for h in range(horizon):
                ts_data[i, ((data.shape[1]-1) * window) + h] = data.iloc[i + window + h, data.shape[1] - 1]
        ##convert ts_data from numpy array to pandas dataframe
        ts_data = pd.DataFrame(ts_data)
        ts_data.to_excel('MASS_DAMPER_TRAIN_DATA_TS.xlsx', index=False)
        #print(f"Timeseries data type: {ts_data.dtypes}")
        return ts_data


    def process_timeseries_dynamic(self, window, horizon, data):
        
        ts_data = np.zeros((data.shape[0] - window - horizon + 1,((data.shape[1]) * window) + horizon))
        
        #full features in the time series data
        for i in range(data.shape[0] - window - horizon + 1):
            for j in range(data.shape[1]):
                for k in range(window):
                    ts_data[i, j * window + k] = data.iloc[i + k, j]

            # Fill in the horizon values from the last column of `data`
            for h in range(horizon):
                ts_data[i, ((data.shape[1]) * window) + h] = data.iloc[i + window + h, data.shape[1]-1]
        ##convert ts_data from numpy array to pandas dataframe
        ts_data = pd.DataFrame(ts_data)
        ts_data.to_excel('MASS_DAMPER_TRAIN_DATA_TS.xlsx', index=False)
        #print(f"Timeseries data type: {ts_data.dtypes}")
        return ts_data


                
            
                 

#D = DataHub()
#D.process_timeseries_excel(4, 3, 'PRECIO_BTC_TRIM.xlsx')


        


