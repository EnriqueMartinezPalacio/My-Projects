# Project 2 — Intelligent Prediction Interface (IPI)

This project implements an **Intelligent Prediction Interface (IPI)** to train and evaluate machine learning models (XGBoost, PyTorch MLPs) on structured datasets such as financial or credit risk data.

---

## 📌 Overview
The system is built around two main components:

- **DataHub**  
  - Handles dataset ingestion (`.xlsx`), preprocessing (missing values, duplicates, label encoding), scaling, train/test split.  
  - Stores preprocessing artifacts (`StandardScaler`) for consistent inference.  
  - Provides normalization/denormalization helpers to ensure model predictions are mapped back to the original scale.

- **ModelHub**  
  - Unified interface for model training and prediction.  
  - Supports multiple backends:
    - **XGBoost**: efficient tree-based models with fast training and validation.  
    - **PyTorch**: fully connected neural networks with configurable architecture, GPU support, real-time plotting, and interactive checkpoint saving.  

---

## ⚙️ Features
- Excel data ingestion and preprocessing.  
- Flexible backend choice: `xgboost` or `pytorch`.  
- Train/test split with scaler persistence (`joblib`).  
- Training visualization:
  - Loss curves (PyTorch).  
  - Validation error (XGBoost).  
- Prediction export: appends results into a new Excel file with predicted values.  
- Model checkpointing:
  - PyTorch → `.pth` files.  
  - XGBoost → `.json` models.  

---

## ▶️ Usage
### Training
```python
from model.model_hub import ModelHub

model = ModelHub()

# Train with XGBoost
model.train_model(
    file='DATA_CREDITO_TRIM.xlsx',
    model='xgboost',
    split_size=0.1,
    learning_rate=0.05,
    epochs=1000,
    chk_name='btc_v1'
)

# Train with PyTorch
model.train_model(
    file='DATA_CREDITO_TRIM.xlsx',
    model='pytorch',
    split_size=0.01,
    learning_rate=0.01,
    epochs=100,
    chk_name='income_1'
)
