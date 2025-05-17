import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
import joblib  # 用于保存和加载数据集
import os

# 数据集文件路径
X_train_file = 'X_train.pkl'
X_test_file = 'X_test.pkl'
y_train_file = 'y_train.pkl'
y_test_file = 'y_test.pkl'

# 采样的数据大小
sample_size = 100000


def preprocess_data(file_path='F:/FastAPI/backend/models/car_baseline_1/data/Fin_host_session_submit_S.csv'):
    # 检查是否已存在保存的训练和测试集，如果存在则直接加载
    if os.path.exists(X_train_file) and os.path.exists(X_test_file) and \
            os.path.exists(y_train_file) and os.path.exists(y_test_file):
        print("Loading existing datasets...")
        X_train = joblib.load(X_train_file)
        X_test = joblib.load(X_test_file)
        y_train = joblib.load(y_train_file)
        y_test = joblib.load(y_test_file)
        return X_train, X_test, y_train, y_test

    # 否则生成数据集
    print("Processing dataset and generating new datasets...")

    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # **保留前 50000 行**
    df_sampled = df.head(sample_size)

    # Drop rows with missing values (if any)
    df_cleaned = df_sampled.dropna()

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

    # 保存数据集到文件
    joblib.dump(X_train, X_train_file)
    joblib.dump(X_test, X_test_file)
    joblib.dump(y_train, y_train_file)
    joblib.dump(y_test, y_test_file)

    print("Datasets saved successfully.")

    return X_train, X_test, y_train, y_test
