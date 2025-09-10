import xgboost as xg
import matplotlib.pyplot as plt
import os
import sklearn.metrics as skme
import pandas as pd

class xgb:
    def __init__(self):
        """
        Inicializa la clase XGBoost.

        Establece el modo de depuración como falso por defecto.
        """
        self.debug = False

    def train(self, x_train, y_train, x_test, y_test, learning_rate, n_estimators, chk_name):
        """
        Entrena el modelo XGBoost.

        Args:
            x_train (numpy.ndarray): Datos de entrenamiento.
            y_train (numpy.ndarray): Etiquetas de entrenamiento.
            x_test (numpy.ndarray): Datos de prueba.
            y_test (numpy.ndarray): Etiquetas de prueba.
            learning_rate (float): Tasa de aprendizaje para el modelo.
            n_estimators (int): Número de estimadores (árboles) en el modelo.
            chk_name (str): Nombre del punto de control.

        Returns:
            None
        """
        # Configurar el modelo
        model = self.build_model(learning_rate, n_estimators)

        # Entrenar el modelo
        model.fit(x_train, y_train, eval_metric='mae', eval_set=[(x_test, y_test)])

        # Mostrar los resultados del entrenamiento
        results = model.evals_result()
        data_r = results['validation_0']['mae']
        plt.plot(data_r, label='Validation')
        plt.title('Training results')
        plt.xlabel('Epochs')
        plt.ylabel('ECM')
        plt.legend()
        plt.show()

        # Mostrar los resultados de la validación
        y_pred = model.predict(x_test)
        plt.figure(figsize=(10, 6))
        plt.plot(y_test, label='Real Validation Data', marker='o', linestyle='-', color='blue')
        plt.plot(y_pred, label='Predicted Validation Data', marker='x', linestyle='--', color='red')
        plt.title('Validation Results')
        plt.xlabel('Data Points')
        plt.ylabel('Values')
        plt.legend()
        plt.grid(True)
        plt.show()

        # Calcular y mostrar la precisión del modelo usando MAPE
        mape = 100 - (skme.mean_absolute_percentage_error(y_test, y_pred) * 100)
        print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")

        # Preguntar al usuario si quieren guardar el modelo
        save = input("Do you want to save the model? (y/n): ")
        if save == 'y':
            chkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'checkpoints', 'xgboost_m'))
            chkpoint_name = os.path.join(chkpoint_dir, f'xgboost_{chk_name}.json')
            model.save_model(chkpoint_name)
            print(f"Model saved as: xgboost_{chk_name}.json")
        else:
            print("Model not saved")

    def build_model(self, learning_rate, n_estimators):
        """
        Construye el modelo XGBoost.

        Args:
            learning_rate (float): Tasa de aprendizaje para el modelo.
            n_estimators (int): Número de estimadores (árboles) en el modelo.

        Returns:
            xgboost.core.Booster: El modelo XGBoost construido.
        """
        model = xg.XGBRegressor(
            objective='reg:squarederror',
            device='cpu',
            learning_rate=learning_rate,
            colsample_bytree=0.3,
            max_depth=10,
            n_estimators=n_estimators,
            tree_method='hist',
            updater='grow_quantile_histmaker,prune'
        )
        return model

    def pred(self, x_pred, chk_name):
        """
        Realiza predicciones utilizando el modelo XGBoost cargado desde el punto de control especificado.

        Args:
            x_pred (numpy.ndarray): Datos para realizar predicciones.
            chk_name (str): Nombre del punto de control.

        Returns:
            numpy.ndarray: Las predicciones realizadas por el modelo.
        """
        chkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'checkpoints', 'xgboost_m'))
        chkpoint_name = os.path.join(chkpoint_dir, f'xgboost_{chk_name}.json')

        model = xg.XGBRegressor()
        model.load_model(chkpoint_name)

        print(f'Prediction shape: {x_pred.shape}')
        y_pred = model.predict(x_pred)

        # Plot prediction data
        plt.figure(figsize=(10, 6))
        plt.plot(y_pred, label='Predicted Data', marker='x', linestyle='--', color='red')
        plt.title('Prediction Results')
        plt.xlabel('Data Points')
        plt.ylabel('Values')
        plt.legend()
        plt.grid(True)
        plt.show()

        return y_pred
