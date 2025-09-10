from data.data_hub import DataHub as DH
from model.models.xgboost_m import xgb
from model.models.pytorch_m import pytorch

class ModelHub:
    def __init__(self):
        self.debug = False

    def train_model(self,file,model,split_size,learning_rate,epochs,chk_name):
        # Carga de datos
        D = DH()
        data = D.load_data(file) # Carga los datos desde el archivo especificado
        data = D.preprocess_data(data) # Preprocesa los datos

        # División de datos en conjuntos de entrenamiento y prueba
        x_train, x_test, y_train, y_test = D.split_data(data, split_size, chk_name, model)

        # Entrenamiento del modelo
        if model == 'xgboost':
            model = xgb()
            model.train(x_train, y_train, x_test, y_test, learning_rate, epochs, chk_name) # Entrena el modelo XGBoost
        elif model == 'pytorch':
            model = pytorch()
            model.train(x_train, y_train, x_test, y_test, learning_rate, epochs, chk_name) # Entrena el modelo PyTorch


    def predict_model(self, file, model, chk_name):
        # Load data
        D = DH()
        data = D.load_data(file)
        x_pred = D.preprocess_data(data)
        x_pred = D.norm_data(x_pred)

        #predict the data
        if model == 'xgboost':
            model_o = xgb()
            y_pred = model_o.pred(x_pred, chk_name)
            y_pred_denorm = D.denorm_data(y_pred, model, chk_name)

            ##store the predicted data wlong the original data in an excel file
            data['Predicted'] = y_pred_denorm
            data.to_excel(f'PRED_{model}_{chk_name}_FILE.xlsx', index=False)

        elif model == 'pytorch':
            model_o = pytorch()
            y_pred = model_o.pred(x_pred, chk_name)
            y_pred_denorm = D.denorm_data(y_pred, model, chk_name)

            ##store the predicted data wlong the original data in an excel file
            data['Predicted'] = y_pred_denorm
            data.to_excel(f'PRED_{model}_{chk_name}_FILE.xlsx', index=False)