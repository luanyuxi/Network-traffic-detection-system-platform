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


def preprocess_data(pcap_directory="F:/FastAPI/backend/models/cloud_baseline_1/data"):
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
    print("Processing PCAP files and generating new datasets...")

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
            df['Dbytes'] = 0  # 如果不存在，设置为0，避免后续 KeyError

        # 处理协议列和端口列，确保数据类型正确
        df['Proto'] = df['Proto'].fillna('unknown')

        def generate_labels(row):
            try:
                # 获取流量的基本特征
                proto = row.get('Proto', 'unknown').lower()  # 协议
                sport = int(row.get('Sport', -1))  # 源端口
                dport = int(row.get('Dport', -1))  # 目的端口
                dpkts = int(row.get('Dpkts', 0))  # 目的数据包数量
                sbytes = int(row.get('Sbytes', 0))  # 源字节数
                dbytes = int(row.get('Dbytes', 0))  # 目的字节数
                rate = float(row.get('Rate', 0))  # 传输速率
                duration = float(row.get('Dur', 0))  # 持续时间
            except ValueError:
                return 0, "Normal"  # 无法解析的数据直接归类为正常流量

            # 增强判断：如果 DstPkts 很少，但 Rate 或 Sbytes 异常高，可能是恶意流量
            if dpkts < 5 and (rate > 500 or sbytes > 10000):
                return 1, "Potential Small Packet Attack (High Rate or Large Bytes with Few DstPkts)"

            # 检测小包但高频流量
            if dpkts < 4 and (rate > 1000 or sbytes > 5000):  # 结合传输速率和字节数检测小包攻击
                return 1, "Potential Small Packet Attack (High Rate or Large Bytes with Few DstPkts)"

            # 针对 SSH 协议 (SSHv2, SSH) 的规则
            if proto in ['ssh', 'sshv2']:
                if rate > 1000 or sbytes > 10000:  # SSH 暴力破解或劫持
                    return 1, "SSH Brute Force or Hijack"

            # POP 协议 (端口 110)
            if proto == 'pop' or dport == 110:
                if sbytes > 5000 or dpkts > 1000:  # 检测 POP 邮件滥用
                    return 1, "POP Email Abuse or Flood"

            # DNS 协议 (端口 53)
            if proto == 'udp' and dport == 53:
                if dpkts > 1000 or rate > 5000:  # DNS 洪水攻击检测
                    return 1, "DNS Flood Attack"

            # HTTP/HTTPS 协议 (端口 80, 443)
            if proto == 'tcp':
                if dport == 80 and sbytes > 1000000:  # HTTP 洪水攻击
                    return 1, "HTTP Flood Attack (Large Payload)"
                if dport == 443 and dpkts > 1000:  # HTTPS 洪水攻击
                    return 1, "HTTPS Flood Attack"

            # ARP 欺骗攻击 (通过数据包数量检测)
            if proto == 'arp' and dpkts > 100:
                return 1, "ARP Spoofing Attack"

            # SMTP 协议 (端口 25)
            if proto == 'tcp' and dport == 25:  # SMTP 暴力破解或垃圾邮件
                if sbytes > 5000 or dpkts > 500:
                    return 1, "SMTP Attack (Spam or Brute Force)"

            # TLSv1 和 SSLv3 检测
            if proto in ['tlsv1', 'sslv3']:
                if dpkts > 1000 or rate > 5000:  # TLS/SSL 洪水攻击
                    return 1, "TLS/SSL Flood Attack"

            # SIGCOMP 协议检测
            if proto == 'sigcomp':
                if dbytes > 100000:  # 信令压缩滥用
                    return 1, "SIGCOMP Abuse (High Compressed Data)"

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
