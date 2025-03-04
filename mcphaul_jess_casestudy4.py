# -*- coding: utf-8 -*-
"""McPhaul_Jess_CaseStudy4.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zLspp1OwLM2oftD7nH22NJDlVv4kagyv
"""

# prompt: mount gopogle drive

from google.colab import drive
drive.mount('/content/drive')

import zipfile
import os

# Define the path to the uploaded zip file
zip_path = "/content/drive/MyDrive/Case Study 4 - Bankruptcy/data.zip"
# Corrected: extract_path should point to a directory
extract_path = "/content/drive/MyDrive/Case Study 4 - Bankruptcy/"

# Extract the contents of the zip file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# List the extracted files to see what we have
extracted_files = os.listdir(extract_path)
extracted_files

!pip install liac-arff

from scipy.io import arff
import pandas as pd
from IPython.display import display

# Load one of the .arff files to inspect the structure
arff_file_path = os.path.join(extract_path, "1year.arff")

# Read the ARFF file
data, meta = arff.loadarff(arff_file_path)

# Convert to DataFrame
df = pd.DataFrame(data)

# Display the first few rows
# Instead of using ace_tools, use IPython.display.display
display(df.head(n=10)) # Displaying the first 10 rows as an example

# Load and preprocess all five years of data
all_data = []

for year in range(1, 6):
    arff_file_path = os.path.join(extract_path, f"{year}year.arff")
    data, meta = arff.loadarff(arff_file_path)
    df = pd.DataFrame(data)

    # Convert class label from bytes to integers
    df['class'] = df['class'].apply(lambda x: int(x.decode('utf-8')))

    # Append to list
    all_data.append(df)

# Combine all years into one DataFrame
df_combined = pd.concat(all_data, ignore_index=True)

# Handle missing values (replace '?' with NaN and fill with median)
df_combined.replace('?', pd.NA, inplace=True)
df_combined = df_combined.apply(pd.to_numeric, errors='coerce')  # Convert all to numeric

# Fill missing values with the median of each column
df_combined.fillna(df_combined.median(), inplace=True)

# Display the cleaned dataset
# Instead of tools.display_dataframe_to_user, use IPython.display.display
from IPython.display import display
display(df_combined)
# You can also print some info about the DataFrame:
print(f"Shape of the cleaned dataset: {df_combined.shape}")
print(f"Data types in the cleaned dataset:\n{df_combined.dtypes}")

from google.colab import drive
import zipfile
import os
from scipy.io import arff
import pandas as pd
from IPython.display import display
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
import matplotlib.pyplot as plt
import seaborn as sns

drive.mount('/content/drive')

# Define the path to the uploaded zip file
zip_path = "/content/drive/MyDrive/Case Study 4 - Bankruptcy/data.zip"
# Corrected: extract_path should point to a directory
extract_path = "/content/drive/MyDrive/Case Study 4 - Bankruptcy/"

# Extract the contents of the zip file
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)

# List the extracted files to see what we have
extracted_files = os.listdir(extract_path)
extracted_files

!pip install liac-arff

# Load and preprocess all five years of data
all_data = []

for year in range(1, 6):
    arff_file_path = os.path.join(extract_path, f"{year}year.arff")
    data, meta = arff.loadarff(arff_file_path)
    df = pd.DataFrame(data)

    # Convert class label from bytes to integers
    df['class'] = df['class'].apply(lambda x: int(x.decode('utf-8')))

    # Append to list
    all_data.append(df)

# Combine all years into one DataFrame
df_combined = pd.concat(all_data, ignore_index=True)

# Handle missing values (replace '?' with NaN and fill with median)
df_combined.replace('?', pd.NA, inplace=True)
df_combined = df_combined.apply(pd.to_numeric, errors='coerce')  # Convert all to numeric

# Fill missing values with the median of each column
df_combined.fillna(df_combined.median(), inplace=True)

# Now use the combined and preprocessed dataframe
data = df_combined

# Data Preprocessing
# Splitting features and target variable
target = 'class' # use 'class' column as target variable
X = data.drop(columns=[target])
y = data[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Exploratory Data Analysis (EDA)
plt.figure(figsize=(10,6))
sns.countplot(x=y)
plt.title("Class Distribution")
plt.show()

# Random Forest Model with Hyperparameter Tuning
rf_params = {
    'n_estimators': [100, 300, 500],
    'max_depth': [5, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf = RandomForestClassifier(random_state=42)
rf_random = RandomizedSearchCV(rf, param_distributions=rf_params, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1)
rf_random.fit(X_train, y_train)

# Best model evaluation
y_pred_rf = rf_random.best_estimator_.predict(X_test)
print("Random Forest Model Report:")
print(classification_report(y_test, y_pred_rf))
print("ROC AUC:", roc_auc_score(y_test, rf_random.best_estimator_.predict_proba(X_test)[:, 1]))

# XGBoost Model with Hyperparameter Tuning
xgb_params = {
    'n_estimators': [100, 300, 500],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 6, 10],
    'subsample': [0.8, 1.0]
}
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb_random = RandomizedSearchCV(xgb, param_distributions=xgb_params, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1)
xgb_random.fit(X_train, y_train)

# Best model evaluation
y_pred_xgb = xgb_random.best_estimator_.predict(X_test)
print("XGBoost Model Report:")
print(classification_report(y_test, y_pred_xgb))
print("ROC AUC:", roc_auc_score(y_test, xgb_random.best_estimator_.predict_proba(X_test)[:, 1]))

# Confusion Matrices
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
sns.heatmap(confusion_matrix(y_test, y_pred_rf), annot=True, fmt='d', cmap='Blues', ax=ax[0])
ax[0].set_title("Random Forest Confusion Matrix")
sns.heatmap(confusion_matrix(y_test, y_pred_xgb), annot=True, fmt='d', cmap='Greens', ax=ax[1])
ax[1].set_title("XGBoost Confusion Matrix")
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from google.colab import drive
from scipy.io import arff # Import the arff module

# Mount Google Drive
drive.mount('/content/drive')

# Load Data (Ensure correct path in Google Drive)
data_paths = [
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/1year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/2year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/3year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/4year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/5year.arff'
]

# Use arff.loadarff to load the data, then convert to DataFrame
data_list = []
for path in data_paths:
    data, meta = arff.loadarff(path) # Load using arff.loadarff
    df = pd.DataFrame(data)
    data_list.append(df)


data = pd.concat(data_list, ignore_index=True)  # Adjust the filename and path as needed

# Convert 'class' column to integers (it's likely loaded as bytes)
data['class'] = data['class'].apply(lambda x: int(x.decode()) if isinstance(x, bytes) else int(x))


# Data Preprocessing
# Handling missing values
# Replace '?' with NaN and then fill with median
data.replace('?', pd.NA, inplace=True)
data = data.apply(pd.to_numeric, errors='coerce')  # Convert all to numeric
data.fillna(data.median(), inplace=True)

# # Data Preprocessing
# # Handling missing values
# data.dropna(inplace=True)

# # Splitting features and target variable
# target = 'Bankruptcy'
# X = data.drop(columns=[target])
# y = data[target]

# # Train-test split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# # Exploratory Data Analysis (EDA)
# plt.figure(figsize=(10,6))
# sns.countplot(x=y)
# plt.title("Class Distribution")
# plt.show()

# Random Forest Model with Hyperparameter Tuning
rf_params = {
    'n_estimators': [100, 300, 500],
    'max_depth': [5, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf = RandomForestClassifier(random_state=42)
rf_random = RandomizedSearchCV(rf, param_distributions=rf_params, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1)
rf_random.fit(X_train, y_train)

# Best model evaluation
y_pred_rf = rf_random.best_estimator_.predict(X_test)
print("Random Forest Model Report:")
print(classification_report(y_test, y_pred_rf))
print("ROC AUC:", roc_auc_score(y_test, rf_random.best_estimator_.predict_proba(X_test)[:, 1]))

# XGBoost Model with Hyperparameter Tuning
xgb_params = {
    'n_estimators': [100, 300, 500],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 6, 10],
    'subsample': [0.8, 1.0]
}
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb_random = RandomizedSearchCV(xgb, param_distributions=xgb_params, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1)
xgb_random.fit(X_train, y_train)

# Best model evaluation
y_pred_xgb = xgb_random.best_estimator_.predict(X_test)
print("XGBoost Model Report:")
print(classification_report(y_test, y_pred_xgb))
print("ROC AUC:", roc_auc_score(y_test, xgb_random.best_estimator_.predict_proba(X_test)[:, 1]))

# Confusion Matrices
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
sns.heatmap(confusion_matrix(y_test, y_pred_rf), annot=True, fmt='d', cmap='Blues', ax=ax[0])
ax[0].set_title("Random Forest Confusion Matrix")
sns.heatmap(confusion_matrix(y_test, y_pred_xgb), annot=True, fmt='d', cmap='Greens', ax=ax[1])
ax[1].set_title("XGBoost Confusion Matrix")
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Load Data (Ensure correct path in Google Drive)
data_paths = [
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/1year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/2year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/3year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/4year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/5year.arff'
]

# Read ARFF files
def load_arff_data(path):
    from scipy.io import arff
    data, meta = arff.loadarff(path)
    df = pd.DataFrame(data)
    df.columns = [col.decode('utf-8') if isinstance(col, bytes) else col for col in df.columns]  # Ensure string column names
    return df

data_list = [load_arff_data(path) for path in data_paths]
data = pd.concat(data_list, ignore_index=True)

# Inspect column names to check for issues
print("Available columns:", data.columns.tolist())

# Standardize column names to remove spaces and ensure correct parsing
data.columns = data.columns.str.strip().str.replace(' ', '_').str.lower()

# Ensure target column exists
# Updated target_variations to include 'class' which is likely the actual target column name
target_variations = ['bankruptcy', 'Bankruptcy', 'bankrupt', 'default', 'class']
target = None
for col in target_variations:
    if col.lower() in data.columns:
        target = col.lower()
        break
if not target:
    raise KeyError("Target column not found in dataset. Please verify column names.")

# Splitting features and target variable
X = data.drop(columns=[target])
y = data[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Exploratory Data Analysis (EDA)
plt.figure(figsize=(10,6))
sns.countplot(x=y)
plt.title("Class Distribution")
plt.show()

# Random Forest Model with Hyperparameter Tuning
rf_params = {
    'n_estimators': [100, 300, 500],
    'max_depth': [5, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf = RandomForestClassifier(random_state=42)
rf_random = RandomizedSearchCV(rf, param_distributions=rf_params, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1)
rf_random.fit(X_train, y_train)

# Best model evaluation
y_pred_rf = rf_random.best_estimator_.predict(X_test)
print("Random Forest Model Report:")
print(classification_report(y_test, y_pred_rf))
print("ROC AUC:", roc_auc_score(y_test, rf_random.best_estimator_.predict_proba(X_test)[:, 1]))

# XGBoost Model with Hyperparameter Tuning
xgb_params = {
    'n_estimators': [100, 300, 500],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 6, 10],
    'subsample': [0.8, 1.0]
}
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb_random = RandomizedSearchCV(xgb, param_distributions=xgb_params, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1)
xgb_random.fit(X_train, y_train)

# Best model evaluation
y_pred_xgb = xgb_random.best_estimator_.predict(X_test)
print("XGBoost Model Report:")
print(classification_report(y_test, y_pred_xgb))
print("ROC AUC:", roc_auc_score(y_test, xgb_random.best_estimator_.predict_proba(X_test)[:, 1]))

# Confusion Matrices
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
sns.heatmap(confusion_matrix(y_test, y_pred_rf), annot=True, fmt='d', cmap='Blues', ax=ax[0])
ax[0].set_title("Random Forest Confusion Matrix")
sns.heatmap(confusion_matrix(y_test, y_pred_xgb), annot=True, fmt='d', cmap='Greens', ax=ax[1])
ax[1].set_title("XGBoost Confusion Matrix")
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from google.colab import drive
from scipy.io import arff

# Mount Google Drive
drive.mount('/content/drive')

# Load Data (Ensure correct path in Google Drive)
data_paths = [
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/1year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/2year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/3year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/4year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/5year.arff'
]

# Read ARFF files
def load_arff_data(path):
    data, meta = arff.loadarff(path)
    df = pd.DataFrame(data)
    # Decode byte strings to strings for all columns
    for col in df.columns:
        if df[col].dtype == 'object':  # Check if the column is of object type (likely contains byte strings)
            df[col] = df[col].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)
    return df

data_list = [load_arff_data(path) for path in data_paths]
data = pd.concat(data_list, ignore_index=True)

# Inspect column names to check for issues
print("Available columns:", data.columns.tolist())

# Standardize column names to remove spaces and ensure correct parsing
data.columns = data.columns.str.strip().str.replace(' ', '_').str.lower()

# Ensure target column exists
target_variations = ['bankruptcy', 'bankrupt', 'class']
target = None
for col in target_variations:
    if col in data.columns:
        target = col
        break
if not target:
    raise KeyError("Target column not found in dataset. Available columns: " + str(data.columns.tolist()))

# Convert target variable to numeric if necessary
# Explicitly convert the target column to numeric, handling errors
data[target] = pd.to_numeric(data[target], errors='coerce')
# If any values are not successfully converted, they will be replaced with NaN
# You can drop rows with NaN values in the target or fill them with an appropriate strategy

# Splitting features and target variable
X = data.drop(columns=[target])
y = data[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

y = pd.to_numeric(y, errors='coerce')  # Force numeric conversion, handle errors

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Exploratory Data Analysis (EDA)
plt.figure(figsize=(10,6))
sns.countplot(x=y)
plt.title("Class Distribution")
plt.show()

# Random Forest Model with Hyperparameter Tuning
rf_params = {
    'n_estimators': [100, 300, 500],
    'max_depth': [5, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf = RandomForestClassifier(random_state=42)
rf_random = RandomizedSearchCV(rf, param_distributions=rf_params, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1)
rf_random.fit(X_train, y_train)

# Best model evaluation
y_pred_rf = rf_random.best_estimator_.predict(X_test)
print("Random Forest Model Report:")
print(classification_report(y_test, y_pred_rf))
print("ROC AUC:", roc_auc_score(y_test, rf_random.best_estimator_.predict_proba(X_test)[:, 1]))

# XGBoost Model with Hyperparameter Tuning
xgb_params = {
    'n_estimators': [100, 300, 500],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 6, 10],
    'subsample': [0.8, 1.0]
}
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb_random = RandomizedSearchCV(xgb, param_distributions=xgb_params, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1)
xgb_random.fit(X_train, y_train)

# Best model evaluation
y_pred_xgb = xgb_random.best_estimator_.predict(X_test)
print("XGBoost Model Report:")
print(classification_report(y_test, y_pred_xgb))
print("ROC AUC:", roc_auc_score(y_test, xgb_random.best_estimator_.predict_proba(X_test)[:, 1]))

# Confusion Matrices
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
sns.heatmap(confusion_matrix(y_test, y_pred_rf), annot=True, fmt='d', cmap='Blues', ax=ax[0])
ax[0].set_title("Random Forest Confusion Matrix")
sns.heatmap(confusion_matrix(y_test, y_pred_xgb), annot=True, fmt='d', cmap='Greens', ax=ax[1])
ax[1].set_title("XGBoost Confusion Matrix")
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Load Data (Ensure correct path in Google Drive)
data_paths = [
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/1year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/2year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/3year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/4year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/5year.arff'
]

# Read ARFF files
def load_arff_data(path):
    from scipy.io import arff
    data, meta = arff.loadarff(path)
    df = pd.DataFrame(data)
    df.columns = [col.decode('utf-8') if isinstance(col, bytes) else col for col in df.columns]  # Ensure string column names
    return df

data_list = [load_arff_data(path) for path in data_paths]
data = pd.concat(data_list, ignore_index=True)

# Inspect column names to check for issues
print("Available columns:", data.columns.tolist())

# Standardize column names to remove spaces and ensure correct parsing
data.columns = data.columns.str.strip().str.replace(' ', '_').str.lower()

# Ensure target column exists
# Updated target_variations to include 'class' which is likely the actual target column name
target_variations = ['bankruptcy', 'Bankruptcy', 'bankrupt', 'default', 'class']
target = None
for col in target_variations:
    if col.lower() in data.columns:
        target = col.lower()
        break

# If target is still None, it means none of the expected target columns were found
if not target:
    # Print available columns for debugging
    print("Available columns:", data.columns.tolist())
    raise KeyError("Target column not found in dataset. Please verify column names.")

# Splitting features and target variable
X = data.drop(columns=[target])
y = data[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Exploratory Data Analysis (EDA)
plt.figure(figsize=(10,6))
sns.countplot(x=y)
plt.title("Class Distribution")
plt.show()

# Random Forest Model with Hyperparameter Tuning

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from google.colab import drive
from scipy.io import arff

# Mount Google Drive
drive.mount('/content/drive')

# Load Data (Ensure correct path in Google Drive)
data_paths = [
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/1year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/2year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/3year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/4year.arff',
    '/content/drive/MyDrive/Case Study 4 - Bankruptcy/5year.arff'
]

# Read ARFF files
def load_arff_data(path):
    data, meta = arff.loadarff(path)
    df = pd.DataFrame(data)
    df = df.applymap(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)  # Ensure string column values
    return df

data_list = [load_arff_data(path) for path in data_paths]
data = pd.concat(data_list, ignore_index=True)

# Inspect column names to check for issues
print("Available columns:", data.columns.tolist())

# Standardize column names to remove spaces and ensure correct parsing
data.columns = data.columns.str.strip().str.replace(' ', '_').str.lower()

# Ensure target column exists
target_variations = ['bankruptcy', 'bankrupt', 'class']
target = None
for col in target_variations:
    if col in data.columns:
        target = col
        break
if not target:
    raise KeyError("Target column not found in dataset. Available columns: " + str(data.columns.tolist()))

# Convert target variable to numeric if necessary
data[target] = pd.to_numeric(data[target], errors='coerce')

# Splitting features and target variable
X = data.drop(columns=[target])
y = data[target]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Exploratory Data Analysis (EDA)
plt.figure(figsize=(10,6))
sns.countplot(x=y)
plt.title("Class Distribution")
plt.show()

# Random Forest Model with Hyperparameter Tuning
rf_params = {
    'n_estimators': [100, 300, 500],
    'max_depth': [5, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}
rf = RandomForestClassifier(random_state=42)
rf_random = RandomizedSearchCV(rf, param_distributions=rf_params, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1)
rf_random.fit(X_train, y_train)

# Best model evaluation
y_pred_rf = rf_random.best_estimator_.predict(X_test)
print("Random Forest Model Report:")
print(classification_report(y_test, y_pred_rf))
print("ROC AUC:", roc_auc_score(y_test, rf_random.best_estimator_.predict_proba(X_test)[:, 1]))

# XGBoost Model with Hyperparameter Tuning
xgb_params = {
    'n_estimators': [100, 300, 500],
    'learning_rate': [0.01, 0.1, 0.2],
    'max_depth': [3, 6, 10],
    'subsample': [0.8, 1.0]
}
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
xgb_random = RandomizedSearchCV(xgb, param_distributions=xgb_params, n_iter=10, cv=5, scoring='roc_auc', n_jobs=-1)
xgb_random.fit(X_train, y_train)

# Best model evaluation
y_pred_xgb = xgb_random.best_estimator_.predict(X_test)
print("XGBoost Model Report:")
print(classification_report(y_test, y_pred_xgb))
print("ROC AUC:", roc_auc_score(y_test, xgb_random.best_estimator_.predict_proba(X_test)[:, 1]))

# Confusion Matrices
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
sns.heatmap(confusion_matrix(y_test, y_pred_rf), annot=True, fmt='d', cmap='Blues', ax=ax[0])
ax[0].set_title("Random Forest Confusion Matrix")
sns.heatmap(confusion_matrix(y_test, y_pred_xgb), annot=True, fmt='d', cmap='Greens', ax=ax[1])
ax[1].set_title("XGBoost Confusion Matrix")
plt.show()

import pandas as pd
from scipy.io import arff
from google.colab import drive

# Mount Google Drive (if not already mounted)
drive.mount('/content/drive')

# List of ARFF files with full paths
arff_files = [
    "/content/drive/MyDrive/Case Study 4 - Bankruptcy/1year.arff",
    "/content/drive/MyDrive/Case Study 4 - Bankruptcy/2year.arff",
    "/content/drive/MyDrive/Case Study 4 - Bankruptcy/3year.arff",
    "/content/drive/MyDrive/Case Study 4 - Bankruptcy/4year.arff",
    "/content/drive/MyDrive/Case Study 4 - Bankruptcy/5year.arff"
]

# Convert each ARFF file to CSV
for file in arff_files:
    data, meta = arff.loadarff(file)  # Now using the full path
    df = pd.DataFrame(data)

    # Convert byte columns to string if necessary
    for col in df.select_dtypes([object]):
        df[col] = df[col].apply(lambda x: x.decode('utf-8') if isinstance(x, bytes) else x)

    # Save as CSV
    csv_filename = file.replace(".arff", ".csv")
    df.to_csv(csv_filename, index=False)
    print(f"Converted {file} to {csv_filename}")

# Load CSV files
file_paths = {
    "1year": "/content/drive/MyDrive/Case Study 4 - Bankruptcy/1year.csv", # Change .arff to .csv
    "2year": "/content/drive/MyDrive/Case Study 4 - Bankruptcy/2year.csv", # Change .arff to .csv
    "3year": "/content/drive/MyDrive/Case Study 4 - Bankruptcy/3year.csv", # Change .arff to .csv
    "4year": "/content/drive/MyDrive/Case Study 4 - Bankruptcy/4year.csv", # Change .arff to .csv
    "5year": "/content/drive/MyDrive/Case Study 4 - Bankruptcy/5year.csv"  # Change .arff to .csv
}


# Read and combine data
df = pd.read_csv(file_paths["1year"])
for year, path in file_paths.items():
    if year != "1year":
        df_temp = pd.read_csv(path)
        df = df.merge(df_temp, how='outer')

# Convert class labels to integers if needed
df['class'] = df['class'].replace({b'0': 0, b'1': 1}).astype(int)

# Drop specified columns
df = df.drop(["Attr21", "Attr37"], axis=1, errors='ignore')

# Prepare train/test data
X = df.loc[:, df.columns != 'class'].values
y = df['class'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Impute missing values
imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
X_train = imp_mean.fit_transform(X_train)
X_test = imp_mean.transform(X_test)

# Normalize data
transformer = RobustScaler().fit(X_train)
X_train = transformer.transform(X_train)
X_test = transformer.transform(X_test)

# Build classifier
clf = RandomForestClassifier(n_estimators=20)

# Define hyperparameter search space
param_dist = {
    "max_depth": [3, None],
    "max_features": sp_randint(1, 11),
    "min_samples_split": sp_randint(2, 11),
    "bootstrap": [True, False],+
    "criterion": ["gini", "entropy"]
}

# Run randomized search
n_iter_search = 20
random_search = RandomizedSearchCV(clf, param_distributions=param_dist, n_iter=n_iter_search, random_state=42)
start = time()
random_search.fit(X_train, y_train)
search_time = time() - start

# Evaluate model
y_hat_rf_test = random_search.predict(X_test)
accuracy = accuracy_score(y_hat_rf_test, y_test)
recall = recall_score(y_test, y_hat_rf_test, pos_label=1, average='binary')
precision = precision_score(y_test, y_hat_rf_test, pos_label=1, average='binary')

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_hat_rf_test)

# Display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
disp.plot()

# Show metrics
search_time, accuracy, recall, precision, conf_matrix

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from time import time
from scipy.stats import randint as sp_randint
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, precision_score, confusion_matrix, ConfusionMatrixDisplay

# Load CSV file
file_path = "/content/drive/MyDrive/Case Study 4 - Bankruptcy/merged_data.csv"  # Ensure the file is in your working directory

# Read the dataset
df = pd.read_csv(file_path)

# Convert class labels to integers if needed
df['class'] = df['class'].replace({b'0': 0, b'1': 1}).astype(int)

# Drop specified columns if they exist
df = df.drop(["Attr21", "Attr37"], axis=1, errors='ignore')

# Prepare train/test data
X = df.loc[:, df.columns != 'class'].values
y = df['class'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# Impute missing values
imp_mean = SimpleImputer(missing_values=np.nan, strategy='mean')
X_train = imp_mean.fit_transform(X_train)
X_test = imp_mean.transform(X_test)

# Normalize data
transformer = RobustScaler().fit(X_train)
X_train = transformer.transform(X_train)
X_test = transformer.transform(X_test)

# Build classifier
clf = RandomForestClassifier(n_estimators=20)

# Define hyperparameter search space
param_dist = {
    "max_depth": [3, None],
    "max_features": sp_randint(1, 11),
    "min_samples_split": sp_randint(2, 11),
    "bootstrap": [True, False],
    "criterion": ["gini", "entropy"]
}

# Run randomized search
n_iter_search = 20
random_search = RandomizedSearchCV(clf, param_distributions=param_dist, n_iter=n_iter_search, random_state=42)
start = time()
random_search.fit(X_train, y_train)
search_time = time() - start

# Evaluate model
y_hat_rf_test = random_search.predict(X_test)
accuracy = accuracy_score(y_hat_rf_test, y_test)
recall = recall_score(y_test, y_hat_rf_test, pos_label=1, average='binary')
precision = precision_score(y_test, y_hat_rf_test, pos_label=1, average='binary')

# Confusion matrix
conf_matrix = confusion_matrix(y_test, y_hat_rf_test)

# Display confusion matrix
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
disp.plot()

# Print results
print(f"RandomizedSearchCV Time: {search_time:.2f} seconds")
print(f"Accuracy: {accuracy:.3f}")
print(f"Recall: {recall:.3f}")
print(f"Precision: {precision:.3f}")

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingClassifier # Import GradientBoostingClassifier

#  GBM is GradientBoostingClassifier
GBM = GradientBoostingClassifier() # Create and assign the model to GBM

# Perform 5-fold cross-validation to assess model generalization
cv_scores = cross_val_score(GBM, X_train, y_train, cv=5, scoring="accuracy")

# Print results
print(f"Cross-Validation Accuracy Scores: {cv_scores}")
print(f"Mean CV Accuracy: {np.mean(cv_scores):.3f}")
print(f"Standard Deviation of Accuracy: {np.std(cv_scores):.3f}")

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingClassifier # Import GradientBoostingClassifier

#  GBM is GradientBoostingClassifier
GBM = GradientBoostingClassifier() # Create and assign the model to GBM

# Perform 5-fold cross-validation to assess model generalization
cv_scores = cross_val_score(GBM, X_train, y_train, cv=5, scoring="accuracy")

# Print results
print(f"Cross-Validation Accuracy Scores: {cv_scores}")
print(f"Mean CV Accuracy: {np.mean(cv_scores):.3f}")
print(f"Standard Deviation of Accuracy: {np.std(cv_scores):.3f}")

# Fit the model to the training data before making predictions
GBM.fit(X_train, y_train) # This line is added to fit the model

from sklearn.metrics import precision_recall_curve

# Compute the probability scores for the test set
y_scores_gbm = GBM.predict_proba(X_test)[:, 1]

# Compute precision-recall pairs for different thresholds
precision, recall, thresholds = precision_recall_curve(y_test, y_scores_gbm)

# Plot Precision-Recall Curve
plt.figure(figsize=(8,5))
plt.plot(thresholds, precision[:-1], "b--", label="Precision")
plt.plot(thresholds, recall[:-1], "r--", label="Recall")
plt.xlabel("Decision Threshold")
plt.ylabel("Score")
plt.title("Precision-Recall Tradeoff at Different Thresholds")
plt.legend()
plt.show()

from sklearn.metrics import classification_report

# Choose an alternative threshold
threshold1 = 0.3  # Aggressive (higher recall)
threshold2 = 0.7  # Conservative (higher precision)

# Convert probabilities to binary predictions
y_pred_thresh1 = (y_scores_gbm >= threshold1).astype(int)
y_pred_thresh2 = (y_scores_gbm >= threshold2).astype(int)

# Print classification reports
print("Classification Report at Threshold 0.3:")
print(classification_report(y_test, y_pred_thresh1))

print("\nClassification Report at Threshold 0.7:")
print(classification_report(y_test, y_pred_thresh2))

