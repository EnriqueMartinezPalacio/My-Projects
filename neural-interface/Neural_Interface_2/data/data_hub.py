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
        self.le = LabelEncoder() # Inicializa un codificador de etiquetas
        self.ss_x = StandardScaler() # Inicializa un escalador estándar para características
        self.ss_y = StandardScaler() # Inicializa un escalador estándar para etiquetas

    def load_data(self, file):
        # Obtener la ruta del archivo en la carpeta de base de datos
        file_route = os.path.join(os.path.dirname(os.path.abspath(__file__)),'database', file)
        # Lee los datos desde el archivo Excel en la ubicación especificada
        data = pd.read_excel(file_route,sheet_name=0)
        return data
    
    def preprocess_data(self, data):
        data = data.dropna() # Elimina filas con valores faltantes
        data = data.drop_duplicates() # Elimina filas duplicadas
        # Aplica codificación de etiquetas y escalado estándar solo para columnas de texto
        for col in data.columns:
            if data[col].dtype == 'object':
                data[col] = self.le.fit_transform(data[col])
        return data
    
    def split_data(self, data, test_size,chk_name,model):
        ## Divide los datos en características y etiquetas como matrices numpy
        x = data.iloc[:, :-1].values # Características
        y = data.iloc[:, -1].values # Etiquetas

        # Escala las características y las etiquetas
        x=self.ss_x.fit_transform(x)
        y=self.ss_y.fit_transform(y.reshape(-1,1))

        # Guarda el modelo de escalado de las etiquetas
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'model','models','scalers', f'{model}_m', f'{model}_{chk_name}_ss_y.pkl')
        joblib.dump(self.ss_y,model_path)
        print(f"Model saved in {model_path}")

        # Divide los datos en conjuntos de entrenamiento y prueba
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, random_state=42)

        return x_train, x_test, y_train, y_test

    def norm_data(self, data):
        # Escala los datos de características
        data = self.ss_x.fit_transform(data)
        return data

    def denorm_data(self,data,model,chk_name):
        # Carga el modelo de escalado de etiquetas
        model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'model', 'models', 'scalers', f'{model}_m', f'{model}_{chk_name}_ss_y.pkl')
        self.ss_y = joblib.load(model_path)

        # Invierte el escalado de las etiquetas
        data=data.reshape(-1,1)
        data=self.ss_y.inverse_transform(data)
        return data
    
    def norm_data(self,data):
        # Escala los datos de características
        data= self.ss_x.fit_transform(data)
        return data
