
from model.model_hub import ModelHub as mh


print("IPI - Interface de predicción Inteligente")


## model training
model = mh()
"""
model.train_model(file='MASS_DAMPER_INVERSA.xlsx', 
                    model='xgboost', 
                    split_size=0.1, 
                    learning_rate=0.05, 
                    epochs=100, 
                    chk_name='MASS_DAMPER_INV', 
                    window=6, 
                    horizon=1, 
                    data_process="timeseries") #timeseries - normal

"""
## model prediction

model.predict_model(file='MASS_DAMPER_TEST_INV.xlsx', 
                    model='xgboost', 
                    chk_name='MASS_DAMPER_INV')






print("Progran End")