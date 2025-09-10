import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import os
import numpy as np
import sklearn.metrics as skme

class pytorch:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        


    def train(self, x_train, y_train, x_test, y_test, learning_rate, epochs, chk_name):
        input_size = x_train.shape[1]
        model, criterion, optimizer = self.build_model(learning_rate, input_size)


        ##convert data from normal arrays to tensor type
        x_train, y_train = torch.tensor(x_train, dtype=torch.float32).to(self.device), torch.tensor(y_train, dtype=torch.float32).to(self.device)
        x_test, y_test = torch.tensor(x_test, dtype=torch.float32).to(self.device), torch.tensor(y_test, dtype=torch.float32).to(self.device)

        print(f"Y Train dimensions: {y_train.shape}")
        ecm = np.zeros(epochs)

        for epoch in range(epochs):
            model.train() ##configure the model for training
            optimizer.zero_grad() ##clear the gradients
            outputs = model(x_train) ##forward pass
            loss = criterion(outputs, y_train) ##calculate the loss
            loss.backward() ##backward pass
            optimizer.step() ##update weights
            ecm[epoch] = loss.item()
            print(f'Epoch {epoch}, Loss: {loss.item()}')

        ##lets plot the training results
        plt.plot(ecm, label='Validation')
        plt.title('Training results')
        plt.xlabel('Epochs')
        plt.ylabel('ECM')
        plt.legend()
        plt.show()
        
        
        
        # Evaluate the model
        model.eval() ##configure the model for evaluation
        print(f"X dimensions: {x_test.shape}")
        y_pred = model(x_test) ##forward pass
        print(f"Y dimensions: {y_pred.shape}")

        ##lets turn the tensors into arrays
        y_pred = y_pred.cpu().detach().numpy()

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
        model = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        ).to(self.device)

        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)

        return model, criterion, optimizer
