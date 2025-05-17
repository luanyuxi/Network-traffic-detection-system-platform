import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split

# Load the CSV file into a DataFrame (replace 'file_path' with your actual file location)
file_path = './data/Fin_host_session_submit_S.csv'
df = pd.read_csv(file_path)

# Drop rows with missing values (null values)
df_cleaned = df.dropna()

# Convert 'Timestamp' and 'DLC' to numeric values for feature extraction
df_cleaned['Timestamp'] = pd.to_numeric(df_cleaned['Timestamp'], errors='coerce')
df_cleaned['DLC'] = pd.to_numeric(df_cleaned['DLC'], errors='coerce')

# Label encode the 'Arbitration_ID', 'Class', and 'SubClass' columns
label_encoder = LabelEncoder()
df_cleaned['Arbitration_ID'] = label_encoder.fit_transform(df_cleaned['Arbitration_ID'])
df_cleaned['Class'] = label_encoder.fit_transform(df_cleaned['Class'])
df_cleaned['SubClass'] = label_encoder.fit_transform(df_cleaned['SubClass'])

# Extract features for 'Data' (treating as a single string to encode)
def extract_data_features(row):
    # Split the 'Data' field into separate bytes and convert hex to int
    data_bytes = row.split()
    return [int(byte, 16) for byte in data_bytes]

# Apply the function to the 'Data' column
data_features = df_cleaned['Data'].apply(extract_data_features)

# Concatenate data features back to the dataframe
data_features_df = pd.DataFrame(data_features.tolist(), index=df_cleaned.index)
df_features = pd.concat([df_cleaned[['Timestamp', 'Arbitration_ID', 'DLC', 'Class']], data_features_df], axis=1)

# Drop any remaining rows with null values after feature extraction
df_features = df_features.dropna()

# Split into X (features) and y (target)
X = df_features.drop(columns=['Class'])
y = df_features['Class']

# Convert column names to strings
X.columns = X.columns.astype(str)

# Scale the features
scaler = MinMaxScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Output shapes and sample data for verification
print(f"X_train shape: {X_train.shape}")
print(f"y_train shape: {y_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"y_test shape: {y_test.shape}")
print("Sample of X_train:")
print(X_train.head())
print("Sample of y_train:")
print(y_train.head())

# Save the training and test data to CSV files
X_train.to_csv('train_features.csv', index=False)
y_train.to_csv('train_labels.csv', index=False)
X_test.to_csv('test_features.csv', index=False)
y_test.to_csv('test_labels.csv', index=False)

print(f"Training and test data saved to CSV files.")
