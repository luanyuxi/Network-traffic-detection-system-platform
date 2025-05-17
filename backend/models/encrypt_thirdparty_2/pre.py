import subprocess
import os
import pandas as pd
from glob import glob
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
import joblib  # 用于保存和加载数据集

# 数据集文件路径
X_train_file = 'X_train.pkl'
X_test_file = 'X_test.pkl'
y_train_file = 'y_train.pkl'
y_test_file = 'y_test.pkl'

# 采样的数据大小
sample_size = 50000

def preprocess_data(pcap_directory="F:/FastAPI/backend/models/encrypt_thirdparty_2/data"):
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
    #print("Processing PCAP files and generating new datasets...")

    # 获取所有PCAP文件的列表
    pcap_files = glob(os.path.join(pcap_directory, "*.pcap"))

    # 初始化一个空的 DataFrame 来存储所有文件的解析结果
    all_data = pd.DataFrame()

    # 遍历每个PCAP文件进行解析
    for pcap_file in pcap_files:
        pcap_file_wsl = pcap_file.replace("\\", "/")

        print(f"Processing {pcap_file_wsl}...")

        # 定义每个文件的输出路径（临时文件）
        argus_output_bin = "./argus_output.bin"
        argus_output_csv = "./argus_output.csv"

        # 通过 WSL 运行 Argus 命令，生成二进制流记录
        argus_command = ["wsl", "argus", "-r", pcap_file_wsl, "-w", argus_output_bin]
        subprocess.run(argus_command)

        # 使用 ra 命令提取特征并输出为 CSV 文件
        ra_command = [
            "wsl", "ra", "-r", argus_output_bin, "-c,",
            "-s", "saddr", "daddr", "proto", "sport", "dport", "dur", "spkts", "dpkts",
            "sbytes", "dbytes", "rate", "sttl", "dttl", "swin", "dwin",
            "tcprtt", "synack", "ackdat", "trans_depth", "ct_srv_src", "ct_state_ttl",
            "ct_dst_ltm", "ct_src_dport_ltm", "ct_dst_sport_ltm", "ct_dst_src_ltm",
            "is_sm_ips_ports", "-nn", "-L0"
        ]

        # 将 Argus 输出写入 CSV 文件
        with open(argus_output_csv, "w") as outfile:
            subprocess.run(ra_command, stdout=outfile)

        # 加载当前文件的 CSV 结果，并设置 low_memory=False 以避免分块读取
        df = pd.read_csv(argus_output_csv, low_memory=False)

        # 检查是否存在 'Dbytes' 列
        if 'Dbytes' not in df.columns:
            #print(f"'Dbytes' column not found in {pcap_file_wsl}. Skipping this column for data analysis.")
            df['Dbytes'] = 0  # 如果不存在，设置为0，避免后续 KeyError

        # 处理协议列和端口列，确保数据类型正确
        df['Proto'] = df['Proto'].fillna('unknown')

        def generate_labels(row):
            try:
                proto = int(row['Proto'])  # 尝试将 Proto 转换为整数
            except ValueError:
                proto = -1  # 如果不能转换，设置为 -1 表示未知协议

            # 尝试将 Sport 和 Dport 转换为整数，如果失败则设为 -1
            try:
                sport = int(row['Sport'])
            except ValueError:
                sport = -1  # 设置无效端口为 -1

            try:
                dport = int(row['Dport'])
            except ValueError:
                dport = -1  # 设置无效端口为 -1

            # 打印调试信息以检查特征值
            #print(f"Sport: {sport}, Dport: {dport}, DstPkts: {row['DstPkts']}")

            # 基于端口和数据包特征判断攻击行为
            if proto == 6:  # TCP 协议
                if dport == 443 or sport == 443:  # HTTPS 流量
                    return 0, "Encrypted Traffic (HTTPS)"
                elif dport == 80 and row['DstPkts'] > 5:  # 降低阈值，检测DoS攻击
                    return 1, "DoS Attack"
                elif sport == 21 or dport == 21:  # 针对 FTP 的攻击行为
                    return 1, "FTP Attack"
                elif sport > 1024 and dport < 1024:  # 端口扫描，非标准端口到标准端口
                    return 1, "Port Scan"
                elif row['DstPkts'] > 10:  # 如果数据包数量超过10，可以假设这是一个潜在攻击
                    return 1, "Potential Small Packet Flood Attack"
                else:
                    return 0, "Normal Traffic"  # 普通的 TCP 流量

            # 默认返回正常流量
            return 0, "Normal"

        # 应用规则生成标签
        df['label'], df['attack_cat'] = zip(*df.apply(generate_labels, axis=1))

        # 将当前文件的数据追加到总的 DataFrame 中
        all_data = pd.concat([all_data, df], ignore_index=True)

    # 删除 'SrcAddr' 和 'DstAddr' 列（避免处理大量类别值）
    all_data = all_data.drop(columns=['SrcAddr', 'DstAddr'])

    # 删除包含空值的行
    all_data = all_data.dropna()

    # 将 'Proto' 列中的非数值协议转换为一个默认的值（如 'unknown'），保留数值协议
    all_data['Proto'] = pd.to_numeric(all_data['Proto'], errors='coerce').fillna(-1)

    # 对 Proto 列进行编码
    encoder = LabelEncoder()
    all_data['Proto'] = encoder.fit_transform(all_data['Proto'])

    # 获取字符类型特征列，不包括 'Proto'
    categorical_mask = (all_data.dtypes == object)
    categorical_columns = [col for col in all_data.columns[categorical_mask] if col != 'Proto']

    # 强制将所有类别列转换为字符串类型，以防止混合数据类型
    for col in categorical_columns:
        all_data[col] = all_data[col].astype(str)

    # 对字符变量进行标签编码
    def label_encoding(data, columns):
        encoder = LabelEncoder()
        for col in columns:
            data[col] = encoder.fit_transform(data[col])
        return data

    all_data = label_encoding(all_data, categorical_columns)

    # 确保所有列名都是字符串类型
    all_data.columns = all_data.columns.astype(str)

    # 对其他特征进行缩放
    X = all_data.drop(columns=['label', 'attack_cat'])
    scaler = MinMaxScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    # 应用 ADASYN 进行重采样
    y = all_data['label']

    # ---- 采样部分 ----
    if len(X_scaled) > sample_size:
        X_scaled, _, y, _ = train_test_split(
            X_scaled, y, train_size=50000, random_state=42, stratify=y
        )
    # ----------------

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    # 保存数据集
    joblib.dump(X_train, X_train_file)
    joblib.dump(X_test, X_test_file)
    joblib.dump(y_train, y_train_file)
    joblib.dump(y_test, y_test_file)

    return X_train, X_test, y_train, y_test


