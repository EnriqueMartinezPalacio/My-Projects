import numpy as np
import xlrd #Read excel file

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,confusion_matrix
import joblib

#workbook= xlrd.open_workbook('dataNumbers.xlsx')
workbook= xlrd.open_workbook('dataTodo.xlsx')


def load_workbook(file):
    sheet= file.sheet_by_index(0)
    x= np.zeros((sheet.nrows,sheet.ncols-1))
    y=[]
    for i in range(0, sheet.nrows):
        for j in range(0,sheet.ncols-1):
            cell_value = sheet.cell_value(rowx=i,colx=j+1)
            if cell_value == '':
                x[i,j]=0
            else:
                x[i,j]=sheet.cell_value(rowx=i,colx=j+1)
        y.append(sheet.cell_value(rowx=i,colx=0))
    y=np.array(y,np.float32)
    return x,y

if __name__ == '__main__':
    x,y=load_workbook(workbook)
    modelScaler = StandardScaler()
    modelScaler.fit(x)
    Xscaled= modelScaler.transform(x)

    X_train,X_test,Y_train,Y_test= train_test_split(Xscaled,y,test_size=0.1,random_state=42)
    #Todos:
    modelMLP = MLPClassifier(hidden_layer_sizes=(
        100,100 ), max_iter=2000, activation='relu',learning_rate_init=0.001, alpha=0.001, random_state=42)



    #Centrales
    # modelMLP = MLPClassifier(hidden_layer_sizes=(
    #     50,60 ), max_iter=2000, activation='relu',learning_rate_init=0.01, alpha=0.001, random_state=42)
    # modelMLP.fit(X_train,Y_train)

    # modelMLP= KNeighborsClassifier(algorithm='auto',metric='manhattan',n_neighbors=32,weights='distance')
    # modelMLP.fit(X_train,Y_train)
    modelMLP.fit(X_train, Y_train)

    accuracy=modelMLP.score(X_test,Y_test)
    accuracy=round(accuracy*100,3)
    print(f'Acurracy:{accuracy}%')

    joblib.dump(modelScaler,'modelScaler_Todo.joblib')
    joblib.dump(modelMLP,'modelMLP_Todo.joblib')