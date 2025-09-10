import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import os
import numpy as np
import sklearn.metrics as skme


class pytorch:
    def __init__(self):
        """
        Inicializa la clase PyTorch.

        Determina el dispositivo de ejecución (CPU o GPU) disponible.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


    def train(self, x_train, y_train, x_test, y_test, learning_rate, epochs, chk_name):
        """
        Entrena el modelo PyTorch.

        Args:
            x_train (torch.Tensor): Datos de entrada de entrenamiento.
            y_train (torch.Tensor): Etiquetas de entrenamiento.
            x_test (torch.Tensor): Datos de entrada de prueba.
            y_test (torch.Tensor): Etiquetas de prueba.
            learning_rate (float): Tasa de aprendizaje para el optimizador.
            epochs (int): Número de épocas de entrenamiento.
            chk_name (str): Nombre del punto de control.

        Returns:
            None
        """
        input_size = x_train.shape[1]  # Tamaño de la capa de entrada
        model, criterion, optimizer = self.build_model(learning_rate, input_size)  # Construye el modelo, define la función de pérdida y el optimizador

        ## convertir datos de listas a tensores y enviarlos al dispositivo
        x_train, y_train = torch.tensor(x_train, dtype=torch.float32).to(self.device), torch.tensor(y_train, dtype=torch.float32).to(self.device)
        x_test, y_test = torch.tensor(x_test, dtype=torch.float32).to(self.device), torch.tensor(y_test, dtype=torch.float32).to(self.device)

        ecm= np.zeros(epochs)
        # Bucle de entrenamiento a través de las épocas
        for epoch in range(epochs):
            model.train()  # Configura el modelo para el modo de entrenamiento
            optimizer.zero_grad()  # Reinicia los gradientes de los parámetros del modelo
            outputs = model(x_train)  # Realiza una pasada hacia adelante (forward pass) del modelo
            loss = criterion(outputs, y_train)  # Calcula la pérdida entre las salidas del modelo y las etiquetas de entrenamiento
            loss.backward()  # Realiza la retropropagación del gradiente
            optimizer.step()  # Actualiza los pesos del modelo basado en el gradiente calculado
            ecm[epoch]=loss.item()

            print(f'Epoch {epoch}, Loss: {loss.item()}')  # Imprime el valor de la pérdida en cada época

        plt.plot(ecm,label="Validation")
        plt.title('Training Results')
        plt.xlabel('Epochs')
        plt.ylabel('ECM')
        plt.legend()
        plt.show()

        #Evaluate the model
        model.eval()## Configure the model for evaluation
        y_pred=model(x_test)## forward pass

        ## Lests turn the tensors into arrays
        y_pred=y_pred.cpu().detach().numpy()
        plt.figure(figsize=(10,6))
        plt.plot(y_test, label='Real Validation Data', marker='o', linestyle='-', color='blue')
        plt.plot(y_pred, label='Predicted Validation Data', marker='x', linestyle='--', color='red')
        plt.title('Validation Results')
        plt.xlabel('Data Points')
        plt.ylabel('Values')
        plt.legend()
        plt.grid(True)
        plt.show()

        ##lets show the model accuracy using MAPE (Mean Absolute Percentage Error)
        #lets show the model accuracy using MAPE (Mean Absolute Percentage Error)
        mape = 100 - (skme.mean_absolute_percentage_error(y_test, y_pred) * 100)  
        print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")

        ##lest ask the user if he wants to save the model
        save = input("Do you want to save the model? (y/n): ")
        if save == 'y':
            name = chk_name
            chkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'checkpoints','pytorch_m'))
            chkpoint_name = os.path.join(chkpoint_dir, f'pytorch_{name}.pth')
            torch.save(model, chkpoint_name)
            print(f"Model saved as: pytorch_{name}.pth")
        else:
            print("Model not saved")



    def pred(self, x_pred, chk_name):
        ##load the model
        chkpoint_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'checkpoints','pytorch_m'))
        chkpoint_name = os.path.join(chkpoint_dir, f'pytorch_{chk_name}.pth')
        model = torch.load(chkpoint_name)

        model.eval() ##configure the model for evaluation

        ##convert data from normal arrays to tensor type
        x_pred = torch.tensor(x_pred, dtype=torch.float32).to(self.device)

        y_pred = model(x_pred) ##forward pass
        
        ##lets turn the tensors into arrays
        y_pred = y_pred.cpu().detach().numpy()

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

    def build_model(self, learning_rate, input_size):
        """
        Construye el modelo PyTorch.

        Args:
            learning_rate (float): Tasa de aprendizaje para el optimizador.
            input_size (int): Tamaño de la capa de entrada.

        Returns:
            torch.nn.Module, torch.nn._Loss, torch.optim.Optimizer: El modelo construido, la función de pérdida y el optimizador.
        """
        # Define la arquitectura del modelo
        model = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        ).to(self.device)

        criterion = nn.MSELoss()  # Define la función de pérdida
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)  # Define el optimizador

        return model, criterion, optimizer
