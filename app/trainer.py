# app/trainer.py

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

DATA_PATH = os.path.join('data', 'creditcard.csv')
MODEL_PATH = os.path.join('model', 'fraud_model.pkl')
SCALER_PATH = os.path.join('model', 'scaler.pkl')

def load_and_prepare_data():
    df = pd.read_csv(DATA_PATH)
    
    # Drop time, scale 'Amount'
    df.drop(['Time'], axis=1, inplace=True)
    df['Amount'] = StandardScaler().fit_transform(df['Amount'].values.reshape(-1, 1))

    X = df.drop('Class', axis=1)
    y = df['Class']
    
    return X, y

def balance_data(X, y):
    # Combine and undersample majority class
    fraud = df[df.Class == 1]
    normal = df[df.Class == 0].sample(n=len(fraud)*5, random_state=42)  # 1:5 ratio

    balanced_df = pd.concat([fraud, normal])
    X_bal = balanced_df.drop('Class', axis=1)
    y_bal = balanced_df['Class']
    
    return X_bal, y_bal

def train_model(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)
    return model

def main():
    print("📊 Loading and preprocessing data...")
    X, y = load_and_prepare_data()

    print("⚖️ Balancing dataset...")
    global df
    df = pd.read_csv(DATA_PATH)
    df.drop(['Time'], axis=1, inplace=True)
    df['Amount'] = StandardScaler().fit_transform(df['Amount'].values.reshape(-1, 1))
    df_balanced = pd.concat([df[df.Class == 1], df[df.Class == 0].sample(n=len(df[df.Class == 1])*5, random_state=42)])
    
    X_bal = df_balanced.drop('Class', axis=1)
    y_bal = df_balanced['Class']

    X_train, X_test, y_train, y_test = train_test_split(X_bal, y_bal, test_size=0.2, random_state=42)

    print("🧠 Training model...")
    model = train_model(X_train, y_train)

    print("💾 Saving model and scaler...")
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    # Save the scaler
    scaler = StandardScaler()
    scaler.fit(X_train)  # Fit the scaler to the training data
    joblib.dump(scaler, SCALER_PATH)

    print("🔎 Evaluating model...")
    y_pred = model.predict(X_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

if __name__ == '__main__':
    main()
