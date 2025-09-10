import xgboost as xg
import matplotlib.pyplot as plt
import os
import sklearn.metrics as skme
import pandas as pd

class xgb:
    def __init__(self):
        self.debug = False
        self.model = None 
        self.chk_name=None  

    def train(self, x_train, y_train, x_test, y_test, learning_rate, epoch, chk_name):
        # Lets configure the model
        model = self.build_model(learning_rate, epoch)

        # Train the model
        model.fit(x_train, y_train, eval_metric = 'mae', eval_set = [(x_test, y_test)])

        ##lets show the results
        results = model.evals_result()

        #lets plot the training results

        data_r = results['validation_0']['mae']
        plt.plot(data_r, label='Validation')
        plt.title('Training results')
        plt.xlabel('Epochs')
        plt.ylabel('ECM')
        plt.legend()
        plt.show()

        ##lets show the validation results
        y_pred = model.predict(x_test)

        plt.figure(figsize=(10,6))
        plt.plot(y_test, label='Real Validation Data', marker='o', linestyle='-', color='blue')
        plt.plot(y_pred, label='Predicted Validation Data', marker='x', linestyle='--', color='red')
        plt.title('Validation Results')
        plt.xlabel('Data Points')
        plt.ylabel('Values')
        plt.legend()
        plt.grid(True)
        plt.show()

        #lets show the model accuracy using MAPE (Mean Absolute Percentage Error)
        mape = 100 - (skme.mean_absolute_percentage_error(y_test, y_pred) * 100)  
        

        print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")

        ##lest ask the user if he wants to save the model
        save = input("Do you want to save the model? (y/n): ")
        if save == 'y':
            name = chk_name
            chkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'checkpoints','xgboost_m'))
            chkpoint_name = os.path.join(chkpoint_dir, f'xgboost_{name}.json')
            model.save_model(chkpoint_name)
            print(f"Model saved as: xgboost_{name}.json")
        else:
            print("Model not saved")


    def build_model(self, learning_rate, n_estimators):
        model = xg.XGBRegressor(
            objective ='reg:squarederror',
            device = 'cpu',
            learning_rate = learning_rate,
            colsample_bytree = 0.3,
            max_depth = 10,
            n_estimators = n_estimators, 
            tree_method = 'hist',
            updater = 'grow_quantile_histmaker,prune'
        )
        return model

    def pred(self, x_pred, chk_name):

        chkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'checkpoints','xgboost_m'))
        chkpoint_name = os.path.join(chkpoint_dir, f'xgboost_{chk_name}.json')


        model = xg.XGBRegressor()
        model.load_model(chkpoint_name)

        print(f'Prediction shape: {x_pred.shape}')
        y_pred = model.predict(x_pred)

        #plot prediction data
        plt.figure(figsize=(10,6))
        plt.plot(y_pred, label='Predicted Data', marker='x', linestyle='--', color='red')
        plt.title('Prediction Results')
        plt.xlabel('Data Points')
        plt.ylabel('Values')
        plt.legend()
        plt.grid(True)
        plt.show()

        return y_pred
    
    def load_model(self, chk_name):
        self.chk_name=chk_name
        chkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'checkpoints','xgboost_m'))
        chkpoint_name = os.path.join(chkpoint_dir, f'xgboost_{chk_name}.json')
        self.model = xg.XGBRegressor()
        self.model.load_model(chkpoint_name)
        print(f"Model {chk_name} loaded")

    def pred_realtime(self, x_pred):

        y_pred = self.model.predict(x_pred)
        return y_pred
    

    def train_realtime(self, x_train, y_train,store_model):
        self.model.fit(x_train,y_train)
        if store_model:
            name = self.chk_name
            chkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'checkpoints','xgboost_m'))
            chkpoint_name = os.path.join(chkpoint_dir, f'xgboost_{name}.json')
            self.model.save_model(chkpoint_name)
            print(f"Model{name} saved")
            #print("Model trained for this iter")
    
    
    

        

