from model.model_hub import ModelHub as mh
 
print("IPI - Interface de prediccion Inteligente")
model=mh()

#Model training
#model.train_model(file='DATA_CREDITO_TRIM.xlsx', model='xgboost', split_size=0.1, learning_rate=0.05, epochs=1000, chk_name='btc_v1')
#model.train_model(file='DATA_CREDITO_TRIM.xlsx', model='pytorch', split_size=0.01, learning_rate=0.01, epochs=100, chk_name='income_1')



#Model prediction
#model.predict_model(file='PRECIO_BTC_PRED.xlsx',model='xgboost',chk_name='btc_v1')
model.predict_model(file='DATA_CREDITO_PRED.xlsx',model='pytorch',chk_name='income_1')

print("Fin del programa")