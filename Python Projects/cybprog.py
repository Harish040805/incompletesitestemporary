import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import IsolationForest

# Load dataset
data = pd.read_csv('test.csv')

# Encode categorical columns
categorical_columns = ['Source', 'Destination', 'Protocol', 'Info']
label_encoders = {col: LabelEncoder() for col in categorical_columns}

for col in categorical_columns:
    data[col] = label_encoders[col].fit_transform(data[col])

# Features for anomaly detection
features = ['Time', 'Source', 'Destination', 'Protocol', 'Length', 'Info']
X = data[features]

# Scale the data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Isolation Forest model
model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
model.fit(X_scaled)

# Predict anomalies (-1 = anomaly, 1 = normal)
data['anomaly'] = model.predict(X_scaled)

# Extract anomalies
anomalies = data[data['anomaly'] == -1]
print(f"Number of anomalies detected: {len(anomalies)}")

# Visualization
plt.figure(figsize=(10, 6))
plt.scatter(data['Time'], data['Length'], c=data['anomaly'], cmap='coolwarm', marker='o', alpha=0.6)
plt.xlabel("Time")
plt.ylabel("Packet Length")
plt.title("Anomaly Detection in Network Traffic")
plt.colorbar(label="Anomaly (-1) / Normal (1)")
plt.show()
