import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import joblib

# =====================================
# LOAD DATASET
# =====================================

data = pd.read_csv(
    "dataset/job_salary_prediction_dataset.csv"
)

# =====================================
# REMOVE NULL VALUES
# =====================================

data.dropna(inplace=True)

# =====================================
# LABEL ENCODING
# =====================================

job_encoder = LabelEncoder()
location_encoder = LabelEncoder()
industry_encoder = LabelEncoder()

data["job_title"] = job_encoder.fit_transform(
    data["job_title"]
)

data["location"] = location_encoder.fit_transform(
    data["location"]
)

data["industry"] = industry_encoder.fit_transform(
    data["industry"]
)

# =====================================
# FEATURES
# =====================================

X = data[
    [
        "job_title",
        "location",
        "industry",
        "experience_years",
        "skills_count"
    ]
]

# =====================================
# TARGET
# =====================================

y = data["salary"]

# =====================================
# TRAIN TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================
# MODEL
# =====================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_train,
    y_train
)

# =====================================
# SAVE MODEL
# =====================================

joblib.dump(
    model,
    "model.pkl"
)

joblib.dump(
    job_encoder,
    "job_encoder.pkl"
)

joblib.dump(
    location_encoder,
    "location_encoder.pkl"
)

joblib.dump(
    industry_encoder,
    "industry_encoder.pkl"
)

print(
    "Model Trained Successfully"
)