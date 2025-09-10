import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.models.xgboost_m import xgb


import pandas as pd
import random


class MassDamper:
    def __init__(self, window_size):
        self.m = 0.1
        self.k = 3
        self.c = 0.5
        self.x0 = 0
        self.v0 = 0
        self.sim_time = 100
        self.U = 0
        self.step_interval = 3
        self.last_update_time = 0
        self.x_history = np.zeros(window_size)
        self.U_history = np.zeros(window_size)
        self.error = 0
        self.errorI = 0
        self.errorD = 0
        self.previous_error = 0
        self.previous_time = 0
        self.kp = 0.5
        self.ki = 0
        self.kd = 0

    def update_force(self, type, output, t):
        if type == 'ident':
            if t - self.last_update_time >= self.step_interval:
                self.U = random.uniform(-10,10)
                self.last_update_time = t


        return self.U
            
            

    def system_equations(self, t, y):
        x, v = y
        dxdt = v
        dvdt = -(self.k / self.m) * x - (self.c / self.m) * v + self.U / self.m
        return [dxdt, dvdt]
    

    def run_simulation(self, simulation_type, save_to_excel, chk_name, train_model):

        ##Condiciones iniciales 
        y0 = [self.x0, self.v0]
        t_span = [0, self.sim_time]

        ##resolvemos las ecuaciones del sistema
        sol = solve_ivp(self.system_equations, t_span, y0, dense_output=True)

        ##creamos un vector que tenga todos los intervalos de muestreo
        t = np.linspace(0, self.sim_time, num=500)

        x, v = sol.sol(t)

        ##configuramos el plot para mostrar en tiempo real
        plt.figure(figsize=(12,6))
        plt.xlabel('Time (s)')
        plt.ylabel('Value')
        plt.title('Mass Damper Simulation')
        plt.grid(True)

        ##inicializamos lineas para posición, velocidad y entrada del sistema
        position_line, = plt.plot([],[],label='Position(X)')
        velocity_line, = plt.plot([],[],label='Velocity(V)')
        control_input_line, = plt.plot([],[],label='Control Input(U)')
        prediction_line, = plt.plot([],[],label='Network Output(Y)')

        #mostramos leyenda de la grafica
        plt.legend()

        ##inicializamos los vectores x y v para simulación
        x = np.zeros(len(t))
        v = np.zeros(len(t))

        ##colocamos las condiciones iniciales en el primer elemento
        x[0] = self.x0
        v[0] = self.v0

        #inicializamos el vector de entrada
        U = np.zeros(len(t))

        ##configuramos el modelo neuronal a cargar
        if train_model:
            model = xgb()
            model.load_model(chk_name)
            PRED = np.zeros(len(t)) ##vector para guardar predicciones

        ##ventana 6, horizonte 1, 2 datos = 12 entradas contando el tamaño de ventana
        ##corremos la simulación en un ciclo for
        for i in range(1, len(t)):
            
            ##actualizamos entrada del sistema
            self.update_force(type=simulation_type,output=x[i-1], t=t[i-1])


            ##Guardamos historial de lo que le esta entrando al sistema
            U[i-1] = self.U

            ##configuramos las condiciones actuales del sistema
            y = [x[i-1], v[i-1]]
            t_span = [t[i-1], t[i]]

            ##resolvemos ecuaciones del sistema
            sol = solve_ivp(self.system_equations, t_span, y, dense_output=True)

            ##calculamos respuesta del sistema para instante siguiente
            x[i], v[i] = sol.sol(t[i])

            ##guardamos historial de posición del sistema para poder alimentra luego al sistema neuronal
            self.x_history[:-1] = self.x_history[1:]
            self.x_history[-1] = x[i]

            ##Guardamos historial de U para alimentar al sistema neuronal
            self.U_history[:-1] = self.U_history[1:]
            self.U_history[-1] = self.U

            ##calculamos la entrada al sistema neuronal
            #x_input = np.concatenate((self.U_history, self.x_history)).reshape(1,-1)
            x_input = np.concatenate((self.x_history, self.U_history)).reshape(1,-1)

            ##realizamos entrenamiento en tiempo real

            #print(f'Xi: {x_input.shape}')
            if train_model:
                model.train_realtime(x_input, U[i-1].reshape(1,-1),True)

                #realizamos prediccion en tiempo real

                y_pred = model.pred_realtime(x_input)
                PRED[i-1] = y_pred[0]
                prediction_line.set_data(t[:i],PRED[:i])
            #print(f"Prediction dimension: {y_pred.shape}")
            #print(f"Prediction: {y_pred[0]}")


            ##Actualizamos la gráfica
            position_line.set_data(t[:i+1],x[:i+1])
            velocity_line.set_data(t[:i+1], v[:i+1])
            control_input_line.set_data(t[:i],U[:i])
            

            plt.xlim(0, self.sim_time)
            plt.ylim(min(min(x), min(v), min(U)) - 0.5, max(max(x), max(v), max(U)) + 0.5)

            #plt.pause(0.001)
        if save_to_excel:
            # Create a DataFrame to store the simulation results in columns
            data_columns = {'Label': np.arange(1,len(t)+1),
                            'U Input': U,
                            'Position': x}
            df_columns = pd.DataFrame(data_columns)

            # Save the DataFrame with data in columns to an Excel file
            
            current_dir = os.path.abspath(__file__)
            col_file = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'data', 'simulation_results_cols.xlsx')

            df_columns.to_excel(col_file, index=False)

            # Transpose the DataFrame to have data in rows
            df_rows = df_columns.set_index('Label').T.reset_index()

            # Rename the first column to 'Label'
            df_rows.rename(columns={'index': 'Label'}, inplace=True)
             # Remove the 'Label' column
            df_rows.drop(columns=['Label'], inplace=True)

            row_file = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'data', 'simulation_results_rows.xlsx')

            # Save the DataFrame with data in rows to another Excel file
            df_rows.to_excel(row_file, index=False)


        plt.show()




MassDamper(6).run_simulation('ident', True, 'MASS_DAMPER_TEST', train_model=True)



