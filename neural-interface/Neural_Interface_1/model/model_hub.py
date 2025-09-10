
from data.data_hub import DataHub as DH
from model.models.xgboost_m import xgb
from model.models.pytorch_m import pytorch

class ModelHub:
    def __init__(self):
        self.debug = False

    def train_model(self, file, model, split_size, learning_rate, epochs, chk_name, window, horizon, data_process):
        # Load data
        D = DH()
        data = D.load_data(file)
        data = D.preprocess_data(data)


        if data_process == 'normal':
            x_train, x_test, y_train, y_test = D.split_data(data, split_size, chk_name, model, 1)
            #train the model
            if model == 'xgboost':
                model = xgb()
                model.train(x_train, y_train, x_test, y_test, learning_rate, epochs, chk_name)
            elif model == 'pytorch':
                model = pytorch()
                model.train(x_train, y_train, x_test, y_test, learning_rate, epochs, chk_name)
        elif data_process == 'timeseries':
            #data = D.process_timeseries(window, horizon, data)
            print(f"TEST PROCESS TS DYNAMIC")
            data = D.process_timeseries_dynamic(window, horizon, data)
            
            #print(f'Data: {data}')
            x_train, x_test, y_train, y_test = D.split_data(data, split_size, chk_name, model, horizon)
            #train the model
            if model == 'xgboost':
                model = xgb()
                model.train(x_train, y_train, x_test, y_test, learning_rate, epochs, chk_name)
            elif model == 'pytorch':
                model = pytorch()
                model.train(x_train, y_train, x_test, y_test, learning_rate, epochs, chk_name)
            

    def predict_model(self, file, model, chk_name):
        # Load data
        D = DH()
        data = D.load_data(file)
        x_pred = D.preprocess_data(data)
        x_pred = D.norm_data(x_pred)
        print(f'Data shape: {x_pred.shape}')   

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
            
            
        



        