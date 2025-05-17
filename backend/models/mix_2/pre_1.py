import subprocess
import os
import numpy as np
import pandas as pd
from glob import glob
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# 定义PCAP文件所在的目录和输出文件路径
pcap_directory = "./data"  # 存放PCAP文件的目录
output_csv = "./merged_output_with_labels.csv"  # 最终输出的合并文件

# 获取所有PCAP文件的列表
pcap_files = glob(os.path.join(pcap_directory, "*.pcap"))

# 初始化一个空的 DataFrame 来存储所有文件的解析结果
all_data = pd.DataFrame()

# 遍历每个PCAP文件进行解析
for pcap_file in pcap_files:
    pcap_file_wsl = pcap_file.replace("\\", "/")
    print(f"Processing {pcap_file_wsl}...")

    argus_output_bin = "./argus_output.bin"
    argus_output_csv = "./argus_output.csv"

    argus_command = ["wsl", "argus", "-r", pcap_file_wsl, "-w", argus_output_bin]
    subprocess.run(argus_command)

    ra_command = [
        "wsl", "ra", "-r", argus_output_bin, "-c,",
        "-s", "saddr", "daddr", "proto", "sport", "dport", "dur", "spkts", "dpkts",
        "sbytes", "dbytes", "rate", "sttl", "dttl", "swin", "dwin",
        "tcprtt", "synack", "ackdat", "trans_depth", "ct_srv_src", "ct_state_ttl",
        "ct_dst_ltm", "ct_src_dport_ltm", "ct_dst_sport_ltm", "ct_dst_src_ltm",
        "is_sm_ips_ports", "-nn", "-L0"
    ]

    with open(argus_output_csv, "w") as outfile:
        subprocess.run(ra_command, stdout=outfile)

    df = pd.read_csv(argus_output_csv)
    df['Proto'] = df['Proto'].fillna('unknown')

    # 标签生成函数，处理大多数流量为 443 的情况
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

        # 检查是否存在 dbytes 列
        dbytes = row['dbytes'] if 'dbytes' in row else 0  # 如果没有 dbytes 列，默认值设为 0

        # 基于端口和数据包特征判断攻击行为
        if dport == 443:  # HTTPS 流量
            if row['DstPkts'] > 1000 or dbytes > 1000000:  # 大量数据包或传输字节，可能为 DDoS 攻击
                return 1, "DDoS Attack on HTTPS"
            elif row['DstPkts'] > 100:  # 中等数量的数据包，可能为中小型攻击
                return 1, "Potential HTTPS Attack"
            else:
                return 0, "Normal HTTPS Traffic"  # 普通的 HTTPS 流量

        elif proto == 6:  # TCP 协议的其他流量
            if dport == 80 and row['DstPkts'] > 100:  # 可能的DoS攻击
                return 1, "DoS Attack on HTTP"
            elif sport == 21 or dport == 21:  # 针对 FTP 的攻击行为
                return 1, "FTP Attack"
            elif sport > 1024 and dport < 1024:  # 端口扫描，非标准端口到标准端口
                return 1, "Port Scan"
            elif row['DstPkts'] > 500:  # 大流量传输，潜在攻击
                return 1, "Large Packet Flow Attack"
            else:
                return 0, "Normal Traffic"  # 普通的 TCP 流量

        # 增强判断：如果 DstPkts 很少，但 Rate 或 Sbytes 异常高，可能是恶意流量
        if dpkts < 5 and (rate > 500 or sbytes > 10000):
            return 1, "Potential Small Packet Attack (High Rate or Large Bytes with Few DstPkts)"

        # 针对 MQTT 协议的规则 (1883)
        if proto == 'mqtt':
            if dpkts < 4 and sbytes > 5000:  # MQTT 小数据包但字节数较大
                return 1, "MQTT Attack (Small Packets with High Bytes)"

        # DNS 协议 (53)
        if proto == 'udp' and dport == 53:
            if dpkts > 1000 or rate > 5000:  # DNS 洪水攻击检测
                return 1, "DNS Flood Attack"

        # ICMP 协议 (ICMP Flood 检测)
        if proto == 'icmp' and dpkts > 1000:
            return 1, "ICMP Flood Attack"

        # MPEG TS 和 H.264 视频流量检测
        if proto in ['mpeg ts', 'h.264']:
            if rate > 10000:  # 视频传输速率异常高时，可能是流量滥用或攻击
                return 1, "Video Stream Abuse (High Rate)"

        # TCP 协议 (端口扫描或洪水攻击)
        if proto == 'tcp':
            if dpkts < 5 and rate > 1000:  # TCP 小包高频流量
                return 1, "TCP Port Scan or Flood Attack (High Rate)"
            if dport == 80 and sbytes > 1000000:  # HTTP 大流量
                return 1, "HTTP Flood Attack (Large Payload or High Rate)"

        # ARP 欺骗攻击 (通过数据包数量检测)
        if proto == 'arp' and dpkts > 100:
            return 1, "ARP Spoofing Attack"

        # STP 攻击检测 (网络环路攻击)
        if proto == 'stp' and dpkts > 1000:  # STP 网络攻击的高数据包流量
            return 1, "STP Network Attack (High Packet Count)"

        # 默认返回正常流量
        return 0, "Normal"


    # 在读取文件后，强制确保 'Proto' 列为字符串类型
    df['Proto'] = df['Proto'].astype(str)
    df['Proto'] = df['Proto'].fillna('unknown')
    df['label'], df['attack_cat'] = zip(*df.apply(generate_labels, axis=1))

    df['label'], df['attack_cat'] = zip(*df.apply(generate_labels, axis=1))
    all_data = pd.concat([all_data, df], ignore_index=True)

# 输出标签统计信息
print(all_data['label'].value_counts())

# 将带标签的合并特征写入最终的 CSV 文件
all_data.to_csv(output_csv, index=False)

print(f"All PCAP files processed and merged. Final CSV saved to {output_csv}")

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

# 将特征列名重命名为数值索引
X_scaled.columns = range(X_scaled.shape[1])

# 确保所有列名都是数字索引
print("Updated column names to numeric indices:")
print(X_scaled.columns)

# 划分训练集和测试集
y = all_data['label']
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# 输出训练集和测试集的类别分布
def print_class_distribution(y_train, y_test):
    print("训练集类别分布 (0: 正常流量, 1: 异常流量):", np.bincount(y_train))
    print("测试集类别分布 (0: 正常流量, 1: 异常流量):", np.bincount(y_test))

print_class_distribution(y_train, y_test)

# 保存训练集和测试集到 CSV 文件
train_x_file = 'train_features.csv'
train_y_file = 'train_labels.csv'
test_x_file = 'test_features.csv'
test_y_file = 'test_labels.csv'

X_train.to_csv(train_x_file, index=False)
y_train.to_csv(train_y_file, index=False)
X_test.to_csv(test_x_file, index=False)
y_test.to_csv(test_y_file, index=False)

print(f"Training and testing data saved to {train_x_file}, {train_y_file}, {test_x_file}, {test_y_file}")
