<template>
  <el-main class="scene-dataset-selection">
        <el-card>
          <h2>场景和数据集选择</h2>

          <!-- 场景和数据集选择在同一行 -->
          <el-form label-width="80px" style="margin-bottom: 20px;">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="选择场景">
                  <el-select v-model="selectedScene" placeholder="选择场景" @change="updateDatasets" style="width: 100%;">
                    <el-option v-for="scene in scenes" :key="scene" :label="scene" :value="scene" />
                  </el-select>
                </el-form-item>
              </el-col>

              <el-col :span="12">
                <el-form-item label="数据集">
                  <el-select v-model="selectedDataset" placeholder="数据集" @change="showDatasetDetails" style="width: 100%;">
                    <el-option v-for="dataset in filteredDatasets" :key="dataset" :label="dataset" :value="dataset" />
                  </el-select>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>

          <!-- 数据集详情 -->
          <div v-if="datasetInfo" class="dataset-details">
            <el-card>
              <h3>数据集的描述</h3>
              <p v-html="datasetInfo.description"></p> <!-- 使用 v-html -->

              <h3>数据集的特征</h3>
              <el-table :data="datasetInfo.features" border style="width: 100%">
                <el-table-column prop="name" label="特征" width="150" />
                <el-table-column prop="description" label="说明" />
              </el-table>

              <h3>数据集标签判定规则</h3>
            <p v-html="datasetInfo.labelRules"></p> <!-- 使用 v-html -->
            </el-card>
          </div>
        </el-card>
      </el-main>
</template>

<script>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export default {
  setup() {
    const router = useRouter();

    const navigateTo = (route) => {
      router.push(route);
    };

    const scenes = ref(["Car", "Encrypt", "Cloud", "IoT", "Mix"]);
    const datasets = ref([
      "car_baseline_1", "car_baseline_2",
      "cloud_baseline_1", "cloud_bupt_1",
      "encrypt_baseline_1", "encrypt_thirdparty_1", "encrypt_thirdparty_2",
      "iot_baseline_1", "iot_baseline_2", "iot_baseline_3",
      "mix_1", "mix_2"
    ]);

    const selectedScene = ref("");
    const selectedDataset = ref("");
    const datasetInfo = ref(null);

    const filteredDatasets = computed(() =>
      datasets.value.filter(dataset =>
        dataset.toLowerCase().startsWith(selectedScene.value.toLowerCase())
      )
    );

    const updateDatasets = () => {
      selectedDataset.value = "";
      datasetInfo.value = null;
    };

    const showDatasetDetails = () => {
      if (selectedDataset.value) {
        loadDatasetInfo(selectedDataset.value);
      }
    };

    const loadDatasetInfo = (datasetName) => {
      if (datasetName === "car_baseline_1") {
        datasetInfo.value = {
          description: "该数据集是在2020年“汽车黑客攻击与防御挑战赛”期间收集并提供的数据集。我们是该竞赛的主要组织者，与Culture Makers和韩国互联网与安全局（KISA）合作。此次比赛的目标是开发针对控制器局域网（CAN）的攻击和检测技术，CAN是车载网络的广泛使用标准。比赛的目标车辆为现代Avante CN7。因此，该数据集包含Avante CN7的CAN网络流量数据，包括正常消息和攻击消息。数据集分为：初赛的训练/测试数据集和决赛的主办方攻击会话数据集，本实验采用的是决赛的主办方攻击会话数据，物联网场景初赛数据集包含两种车辆状态：S（静止）和D（行驶）。决赛数据集仅采集了车辆静止状态下的流量数据，出于安全考虑。<br>" +
              "Class字段的定义如下：<br>" +
              "Normal: CAN总线中的正常流量；Attack: 注入的攻击CAN消息，包含四种类型：Flooding: 通过发送大量消息占用CAN总线带宽。<br>" +
              "Spoofing: 注入伪造消息以控制某些特定功能。<br>" +
              "Replay: 提取特定时间的正常流量并将其重新注入CAN总线。<br>" +
              "Fuzzing: 注入随机消息以导致车辆产生意外行为。\n",
          features: [
            { name: "Timestamp", description: "记录数据帧被捕获的时间" },
            { name: "Arbitration_ID", description: "CAN总线消息的标识符" },
            { name: "DLC", description: "数据长度代码" },
            { name: "Data0 - Data7", description: "数据帧中的具体数据字节" }
          ],
          labelRules: "此数据集为CSV文件，不用生成标签，直接预处理即可"
        };
      } else if (datasetName === "car_baseline_2") {
        datasetInfo.value = {
          description: "实验所采用的基础数据集1为UNSW-NB15数据集，是为评估网络入侵检测系统（NIDS）而创建的。该数据集是在澳大利亚网络安全中心（ACCS）的Cyber Range实验室中，使用IXIA PerfectStorm工具生成的，包含现代网络中正常和异常流量的混合数据。通过IXIA工具模拟了表VIII中列出的九类攻击，IXIA工具能够从CVE网站实时获取最新的攻击信息，该网站是一个公开收录安全漏洞与暴露信息的数据库。\n" +
              "网络流量的捕获是通过tcpdump工具记录下来的数据包完成的。<br>" +
              "整个模拟过程分别在2015年1月22日和2015年2月17日进行，持续时间分别为16小时和15小时，最终捕获了100 GB的网络流量数据。每个pcap文件通过tcpdump工具分割成1000 MB大小的块。为了从这些pcap文件中提取出有效的特征，使用了Argus和Bro-IDS工具。同时，还通过C#语言开发了12种算法，深入分析了网络连接的数据流。数据集的标签来自一个“真实标签表”，该表基于IXIA报告生成，记录了所有模拟的攻击类型。\n" +
              "UNSW-NB15数据集的主要特点是融合了现代真实的正常网络行为与合成的攻击活动，为网络入侵检测的研究提供了可靠的数据基础。\n",
          features: [
            { name: "Proto", description: "协议类型" },
            { name: "Sport", description: "源端口" },
            { name: "Dport", description: "目标端口" },
            { name: "Dur", description: "持续时间" },
            { name: "SrcPkts", description: "源数据包数" },
            { name: "DstPkts", description: "目的数据包数" },
            { name: "SrcBytes", description: "源字节数" },
            { name: "DstBytes", description: "目的字节数" },
            { name: "Rate", description: "传输速率" },
            { name: "sTtl'", description: "源TTL" },
            { name: "dTtl", description: "目的TTL" },
            { name: "SrcWin", description: "源窗口大小" },
            { name: "DstWin", description: "目的窗口大小"},
            { name: "TcpRtt", description: "TCP往返时间"},
            { name: "SynAck", description: "SYN-ACK时间"},
            { name: "AckDat", description: "确认数据量"}

          ],
           labelRules: `标签生成部分通过分析网络流量中的协议类型、端口号、数据包数和字节数等特征，依据预定义的规则判断网络流量是否属于攻击行为，生成相应的标签。具体流程如下：<br>
                        - 协议解析：根据网络流量的协议类型（Proto），识别流量的具体行为，主要包括以下协议：<br>
                        - TCP协议（Proto = 6）：通过分析目的端口和数据包数量，判断是否为DoS攻击、FTP攻击或端口扫描。<br>
                        - UDP协议（Proto = 17）：通过分析目的端口161（SNMP）或数据包数大于1000，识别SNMP Flood或UDP Flood攻击。<br>
                        - ICMP协议（Proto = 1）：通过分析源数据包数，判断是否为ICMP攻击。<br>
                        - GRE协议（Proto = 47）：通过判断目的字节数是否大于100000，检测GRE Tunnel攻击。<br>
                        - OSPF协议（Proto = 89）：直接标记为OSPF攻击。<br>
                        - SCTP协议（Proto = 132）：通过数据包数判断是否为SCTP Flood攻击。<br>
                        - SNMP协议（Proto = 161）：标记为SNMP攻击。<br>
                        - 对每条网络流量记录，首先检查协议类型和相关的流量特征（如数据包数、字节数），如果满足预定条件，则标记为攻击，并为其生成攻击类别标签（attack_cat）；否则，标记为正常流量。`
        };
      } else if (datasetName === "encrypt_thirdparty_1") {
        datasetInfo.value = {
          description: "Jiami2020数据集是一种基于文件划分的网络流量数据集。该数据集将网络流量分为两类：black代表异常流量，" +
                       "表示可能含有恶意行为的流量数据；white代表正常流量，即未检测到攻击或异常行为的常规网络数据。" +
                       "该数据集可以帮助研究人员在正常与异常流量的对比中构建入侵检测系统，检测出潜在的恶意流量模式，从而提高对网络攻击的识别能力。",
          features: [
            { name: "Proto", description: "协议类型" },
            { name: "Sport", description: "源端口" },
            { name: "Dport", description: "目标端口" },
            { name: "Dur", description: "持续时间" },
            { name: "SrcPkts", description: "源数据包数" },
            { name: "DstPkts", description: "目的数据包数" },
            { name: "SrcBytes", description: "源字节数" },
            { name: "DstBytes", description: "目的字节数" },
            { name: "Rate", description: "传输速率" },
            { name: "sTtl'", description: "源TTL" },
            { name: "dTtl", description: "目的TTL" },
            { name: "SrcWin", description: "源窗口大小" },
            { name: "DstWin", description: "目的窗口大小"},
            { name: "TcpRtt", description: "TCP往返时间"},
            { name: "SynAck", description: "SYN-ACK时间"},
            { name: "AckDat", description: "确认数据量"}
          ],
          labelRules: `根据文件划分，black为异常流量，white为正常流量。`
        };
      }else if (datasetName === "encrypt_thirdparty_2") {
        datasetInfo.value = {
          description: "Jiami2021数据集通过解析后的流量数据（df）生成标签，基于协议类型（Proto）、源端口（Sport）、目标端口（Dport）和数据包数量（DstPkts）等" +
                       "多个特征来标识攻击行为。例如，当目标端口为80且数据包数量超过5时，标记为DoS攻击；当源或目标端口为21时，标记为FTP攻击；" +
                       "源端口大于1024且目标端口小于1024时，则标记为端口扫描攻击；而当数据包数量超过10时，则标记为小包攻击。" +
                       "此数据集提供了丰富的网络攻击模式，适用于研究不同类型的网络攻击以及入侵检测算法的性能验证。",
          features: [
            { name: "Proto", description: "协议类型" },
            { name: "Sport", description: "源端口" },
            { name: "Dport", description: "目标端口" },
            { name: "Dur", description: "持续时间" },
            { name: "SrcPkts", description: "源数据包数" },
            { name: "DstPkts", description: "目的数据包数" },
            { name: "SrcBytes", description: "源字节数" },
            { name: "DstBytes", description: "目的字节数" },
            { name: "Rate", description: "传输速率" },
            { name: "sTtl'", description: "源TTL" },
            { name: "dTtl", description: "目的TTL" },
            { name: "SrcWin", description: "源窗口大小" },
            { name: "DstWin", description: "目的窗口大小"},
            { name: "TcpRtt", description: "TCP往返时间"},
            { name: "SynAck", description: "SYN-ACK时间"},
            { name: "AckDat", description: "确认数据量"}
          ],
          labelRules: `解析后的流量数据（df）会根据协议类型（Proto）、源端口（Sport）、目标端口（Dport）及数据包数量（DstPkts）等特征生成标签。
                       特定条件下标记为攻击行为，如：<br>
                       DoS攻击：当目标端口为80，且数据包数量超过5。<br>
                       FTP攻击：当源或目标端口为21。<br>
                       端口扫描：当源端口大于1024且目标端口小于1024。<br>
                       小包攻击：当数据包数量超过10。`
        };
      } else if (datasetName === "encrypt_baseline_1") {
        datasetInfo.value = {
          description: "USTC-TFC2016数据集被描述为一个用于恶意软件流量分类的数据集。该数据集由中国科学技术大学（USTC）开发，" +
              "专门用于网络流量的恶意软件检测和分类研究。USTC-TFC2016数据集包含大量的恶意软件流量样本，涵盖了多种恶意软件家族，" +
              "如病毒、蠕虫、特洛伊木马等，同时也包含了正常的网络流量。数据集的捕获方式通过网络流量抓包工具记录，" +
              "并生成pcap格式文件。每个流量样本对应一个特定的恶意软件家族或正常行为。这些流量样本经过进一步处理和标签化，" +
              "以便为机器学习和深度学习模型提供训练和测试数据。该数据集为研究人员提供了高质量的、可公开使用的恶意软件流量样本，" +
              "广泛用于基于深度学习的流量分类任务中，尤其是在利用卷积神经网络（CNN）进行表示学习的研究中起到了重要作用。",
          features: [
            {name: "Proto", description: "协议类型"},
            {name: "Sport", description: "源端口"},
            {name: "Dport", description: "目标端口"},
            {name: "Dur", description: "持续时间"},
            {name: "SrcPkts", description: "源数据包数"},
            {name: "DstPkts", description: "目的数据包数"},
            {name: "SrcBytes", description: "源字节数"},
            {name: "DstBytes", description: "目的字节数"},
            {name: "Rate", description: "传输速率"},
            {name: "sTtl'", description: "源TTL"},
            {name: "dTtl", description: "目的TTL"},
            {name: "SrcWin", description: "源窗口大小"},
            {name: "DstWin", description: "目的窗口大小"},
            {name: "TcpRtt", description: "TCP往返时间"},
            {name: "SynAck", description: "SYN-ACK时间"},
            {name: "AckDat", description: "确认数据量"}
          ],
          labelRules: `目录如下：<br>
                   Benign/<br>
                       ├── BitTorrent.pcap<br>
                       ├── Facetime.pcap<br>
                       ├── FTP.7z<br>
                       ├── Gmail.pcap<br>
                       ├── MySQL.pcap<br>
                       ├── Outlook.pcap<br>
                       ├── Skype.pcap<br>
                       ├── SMB.7z<br>
                       ├── Weibo.7z<br>
                       └── WorldOfWarcraft.pcap<br>
                   Malware/<br>
                       ├── Cridex.7z<br>
                       ├── Geodo.7z<br>
                       ├── Htbot.7z<br>
                       ├── Miuref.pcap<br>
                       ├── Neris.7z<br>
                       ├── Nsis-ay.7z<br>
                       ├── Shifu.7z<br>
                       ├── Tinba.pcap<br>
                       ├── Virut.7z<br>
                       └── Zeus.pcap`
        };
      } else if (datasetName === "cloud_baseline_1") {
        datasetInfo.value = {
          description: "ISCX 2012入侵评估数据集用于进行实验并评估提出的异常检测方法的性能。该数据集共包含约1,512,000个带有20个特征的标记数据包，" +
                       "覆盖了为期七天的网络活动（包括正常流量和入侵流量）。有关此数据集的详细描述可以参考Shiravi等人在2012年的研究。" +
                       "由于没有现成的训练和测试数据集，且在庞大的数据上进行实验较为困难，研究者选择了特定主机和特定日期的入站数据包来验证其提出的方法，" +
                       "训练数据包含75,372条正常数据和2,154条攻击数据，而测试数据包含19,202条正常数据和37,159条额外的攻击数据。",
          features: [
            { name: "Proto", description: "协议类型" },
            { name: "Sport", description: "源端口" },
            { name: "Dport", description: "目标端口" },
            { name: "Dur", description: "持续时间" },
            { name: "SrcPkts", description: "源数据包数" },
            { name: "DstPkts", description: "目的数据包数" },
            { name: "SrcBytes", description: "源字节数" },
            { name: "DstBytes", description: "目的字节数" },
            { name: "Rate", description: "传输速率" },
            { name: "sTtl'", description: "源TTL" },
            { name: "dTtl", description: "目的TTL" },
            { name: "SrcWin", description: "源窗口大小" },
            { name: "DstWin", description: "目的窗口大小"},
            { name: "TcpRtt", description: "TCP往返时间"},
            { name: "SynAck", description: "SYN-ACK时间"},
            { name: "AckDat", description: "确认数据量"}
          ],
          labelRules: `Friday, 11/6/2010, Normal Activity. No malicious activity, 16.1<br>
                       Saturday, 12/6/2010, Normal Activity. No malicious activity, 4.22<br>
                       Sunday, 13/6/2010, Infiltrating the network from inside + Normal Activity, 3.95<br>
                       Monday, 14/6/2010, HTTP Denial of Service + Normal Activity, 6.85<br>
                       Tuesday, 15/6/2010, Distributed Denial of Service using an IRC Botnet, 23.4<br>
                       Wednesday, 16/6/2010, Normal Activity. No malicious activity, 17.6<br>
                       Thursday, 17/6/2010, Brute Force SSH + Normal Activity, 12.3<br>
                       IDS2012生成标签的方式是基于网络活动的具体描述，对每一天的网络流量进行标记。每个日期对应的活动包含两类：正常活动（Normal Activity）和攻击活动。
                       在有攻击发生的日期，还会进一步标记具体的攻击类型，如HTTP拒绝服务攻击（HTTP Denial of Service）、
                       分布式拒绝服务（Distributed Denial of Service using an IRC Botnet）、SSH暴力破解（Brute Force SSH）等。
                       这种方式通过描述每天的网络流量特征生成标签，便于后续的网络流量分类和检测模型训练。`
        };
      } else if (datasetName === "cloud_bupt_1") {
        datasetInfo.value = {
          description: "Jike数据集是专门为网络安全研究和攻击检测而设计的高质量数据集，通过详细的网络流量分析和协议解析，帮助识别不同类型的网络攻击行为。" +
                       "该数据集的关键特点在于对流量协议（Proto）和端口号的检测，通过端口和流量特征（如数据包数）来推断流量行为，匹配已知的攻击模式。" +
                       "例如，APT_PROMETHIUM攻击假设使用443端口的大量流量进行通信，而Alusinus RAT基于远程访问工具常用的3389端口进行检测。" +
                       "此外，数据集还包括DDoS攻击的检测机制，通过对UDP数据包数量的分析（当目的数据包数大于2000时识别）来判断攻击行为。" +
                       "数据集中的每条流量记录根据事先设定的规则生成二元标签和攻击类别标签。其中，label字段为二元标签，1表示检测到攻击，0表示正常流量； " +
                       "attack_cat字段则具体标明攻击类别，如“APT_PROMETHIUM”、“Emotet”、“DDoS”等。这种设计不仅提高了数据集的精确性和实用性，" +
                       "还为研究人员提供了一个清晰的、标准化的标注体系，方便他们进行模型训练和评估。Jike数据集通过模拟真实网络环境中的攻击场景，" +
                       "为研究人员提供了丰富多样的流量数据，使其能够更好地研究入侵检测系统（IDS）和网络安全防御策略。研究人员可以利用该数据集进行机器学习" +
                       "模型的训练与测试，从而提升对各种已知攻击的检测能力，也可以探索未知攻击模式，推动网络安全领域的技术进步。",
          features: [
            { name: "Proto", description: "协议类型" },
            { name: "Sport", description: "源端口" },
            { name: "Dport", description: "目标端口" },
            { name: "Dur", description: "持续时间" },
            { name: "SrcPkts", description: "源数据包数" },
            { name: "DstPkts", description: "目的数据包数" },
            { name: "SrcBytes", description: "源字节数" },
            { name: "DstBytes", description: "目的字节数" },
            { name: "Rate", description: "传输速率" },
            { name: "sTtl'", description: "源TTL" },
            { name: "dTtl", description: "目的TTL" },
            { name: "SrcWin", description: "源窗口大小" },
            { name: "DstWin", description: "目的窗口大小"},
            { name: "TcpRtt", description: "TCP往返时间"},
            { name: "SynAck", description: "SYN-ACK时间"},
            { name: "AckDat", description: "确认数据量"}
          ],
          labelRules: `根据网络流量的协议类型（Proto），对流量的行为进行解析，并结合端口号和数据包数等特征来匹配不同的攻击模式。<br>
                       •APT_PROMETHIUM：假设使用常见的443端口和大量数据包流量，检测此类攻击。<br>
                       •Alusinus RAT：基于远程访问工具常用的3389端口检测。<br>
                       •Apocalypse：假设使用端口12345检测。<br>
                       •AsyncRAT：假设使用端口8888检测。<br>
                       •Back Connect RAT：使用8080端口的反向连接进行检测。<br>
                       •DDoS：通过大量的UDP数据包进行检测（DstPkts大于2000）。<br>
                       •Covenant：假设使用HTTP流量（80端口）。<br>
                       •Emotet：使用445端口的流量检测此恶意软件。<br>
                       •gcat：检测使用SMTP端口（25）的攻击。<br>
                       •Hancitor、PoshC2、Qakbot等：通过各自假定的端口（如443、8081、2222等）进行识别。<br>
                       •TheFatRAT：使用端口1337的反向连接工具进行检测。<br>
                       •普通HTTP流量：如果检测到正常的HTTP流量（80端口），则标记为正常流量。<br>
                       每条流量记录最终根据上述规则生成两个字段：<br>
                       label：二值标签，1表示攻击，0表示正常；<br>
                       attack_cat：具体的攻击类别，攻击类别的详细名称（如“APT_PROMETHIUM”或“Normal HTTP”）。`
        };
      } else if (datasetName === "iot_baseline_1") {
        datasetInfo.value = {
          description: "本研究使用BoT-IoT数据集进行分析。该数据集由UNSW堪培拉网络安全中心的Cyber Range实验室生成，模拟了一个真实的网络环境，" +
                       "融合了正常流量与僵尸网络攻击流量。数据集包含以下攻击类型：DDoS（分布式拒绝服务攻击）：基于TCP、UDP和HTTP协议的攻击；" +
                       "DoS（拒绝服务攻击）：基于TCP、UDP和HTTP协议；信息收集攻击（服务扫描和操作系统指纹识别）；信息盗窃攻击（键盘记录和数据盗窃）。" +
                       "研究工作包含分析四个文件，涵盖不同类型的DoS和DDoS攻击以及信息收集和信息盗窃攻击。第一个文件包含仅有的DoS攻击，" +
                       "DoS攻击的目的是使授权用户无法访问系统，通常通过向目标发送大量HTTP、UDP和TCP请求来实现。一旦目标被请求淹没，就无法响应正常流量。" +
                       "第二个文件包含DoS和DDoS攻击，DDoS（分布式拒绝服务）攻击通过来自多个来源的流量（包括HTTP、UDP或TCP请求）淹没目标，" +
                       "导致服务或网络的正常流量中断。第三个文件包含两个DDoS攻击，第四个文件包含多种攻击类型。我们之前讨论了几种类型的攻击，" +
                       "其中一种是信息收集攻击，使用工具收集目标信息。该攻击有两种类型：服务扫描和操作系统指纹识别。此外，另一种攻击是信息盗窃攻击，" +
                       "通过窃取目标的个人信息实现。信息可以通过多种方式获取，包括键盘记录器，它会记录目标的按键并发送给第三方。",
          features: [
            { name: "Proto", description: "协议类型" },
            { name: "Sport", description: "源端口" },
            { name: "Dport", description: "目标端口" },
            { name: "Dur", description: "持续时间" },
            { name: "SrcPkts", description: "源数据包数" },
            { name: "DstPkts", description: "目的数据包数" },
            { name: "SrcBytes", description: "源字节数" },
            { name: "DstBytes", description: "目的字节数" },
            { name: "Rate", description: "传输速率" },
            { name: "sTtl'", description: "源TTL" },
            { name: "dTtl", description: "目的TTL" },
            { name: "SrcWin", description: "源窗口大小" },
            { name: "DstWin", description: "目的窗口大小"},
            { name: "TcpRtt", description: "TCP往返时间"},
            { name: "SynAck", description: "SYN-ACK时间"},
            { name: "AckDat", description: "确认数据量"}
          ],
          labelRules: `首先，程序识别每条流量记录中的协议类型（TCP、UDP、ICMP等），并对源端口和目标端口进行解析。如果协议或端口数据不可转换为整数，则赋予默认值-1，表示未知协议或无效端口。<br>
                       根据协议类型和特定的流量特征（如数据包数量、目标端口）生成攻击标签和攻击类别。主要规则如下：<br>
                       •TCP协议（proto=6）：如果目标端口是80且数据包数（DstPkts）超过1000，标记为DoS攻击；如果源或目标端口是21（FTP端口），
                       标记为FTP攻击；源端口大于1024而目标端口小于1024，标记为端口扫描；其他情况下标记为正常流量。<br>
                       •UDP协议（proto=17）：如果目标端口是161（SNMP协议）且数据包数超过500，标记为SNMP Flood；数据包数超过1000，标记为UDP Flood攻击；
                       其他情况下标记为正常流量。<br>
                       •ICMP协议（proto=1）：如果源数据包数（SrcPkts）超过100，标记为ICMP攻击，否则为正常流量。<br>
                       每条流量记录最终根据上述规则生成两个字段：<br>
                       •label：二值标签，1表示攻击，0表示正常；<br>
                       •attack_cat：具体的攻击类别，如“DoS”、“FTP Attack”、“UDP Flood”等。`
        };
      } else if (datasetName === "iot_baseline_2") {
        datasetInfo.value = {
          description: "MedBIoT数据集旨在帮助开发基于机器学习的物联网（IoT）僵尸网络检测系统。该数据集是在一个中型的IoT网络中生成，" +
                       "模拟了包含正常和僵尸网络流量的真实IoT环境。数据集中的流量来自各种IoT设备，如智能家居系统，适用于构建监督学习和无监督学习模型，" +
                       "以检测僵尸网络攻击。数据集中包括多种僵尸网络攻击类型，例如分布式拒绝服务攻击（DDoS）、拒绝服务攻击（DoS）、服务扫描、" +
                       "操作系统指纹识别、以及信息盗窃攻击（如键盘记录攻击）。这些特性使该数据集特别适用于入侵检测系统的研究，帮助研究人员测试和比较不同" +
                       "的检测方法。MedBIoT数据集广泛用于学术研究和实际应用中，尤其是在IoT设备的安全系统开发方面，因为这些设备通常存在被僵尸网络攻击" +
                       "的漏洞。",
          features: [
            { name: "Proto", description: "协议类型" },
            { name: "Sport", description: "源端口" },
            { name: "Dport", description: "目标端口" },
            { name: "Dur", description: "持续时间" },
            { name: "SrcPkts", description: "源数据包数" },
            { name: "DstPkts", description: "目的数据包数" },
            { name: "SrcBytes", description: "源字节数" },
            { name: "DstBytes", description: "目的字节数" },
            { name: "Rate", description: "传输速率" },
            { name: "sTtl'", description: "源TTL" },
            { name: "dTtl", description: "目的TTL" },
            { name: "SrcWin", description: "源窗口大小" },
            { name: "DstWin", description: "目的窗口大小"},
            { name: "TcpRtt", description: "TCP往返时间"},
            { name: "SynAck", description: "SYN-ACK时间"},
            { name: "AckDat", description: "确认数据量"}
          ],
          labelRules: `该数据集已经分好了正常流量和异常流量，根据文件名称即可区分标签。`
        };
      } else if (datasetName === "iot_baseline_3") {
        datasetInfo.value = {
          description: "MQTT数据集包含四种攻击类型：Aggressive scan (Scan A)：激进的扫描攻击；User Datagram Protocol (UDP) scan " +
                       "(Scan sU)：UDP扫描攻击；Sparta SSH brute-force (Sparta)：使用Sparta工具进行的SSH暴力破解攻击；" +
                       "MQTT brute-force attack (MQTT BF)：MQTT协议的暴力破解攻击。数据通过tcpdump工具获取，记录以太网流量并导出为pcap文件。" +
                       "用于攻击模拟的工具包括：虚拟机：用于模拟网络设备；Nmap：用于执行扫描攻击；VLC：用于模拟摄像头视频流；MQTT-PWN：" +
                       "用于执行MQTT暴力破解攻击。网络架构包括12个MQTT传感器、一个MQTT代理、一个用于模拟摄像头视频流的机器和攻击者。在正常操作下，" +
                       "所有12个传感器通过MQTT的“Publish”命令发送随机消息，消息长度和内容不同，以模拟不同的使用场景。摄像头流由VLC媒体播放器通过" +
                       "UDP协议模拟。此外，网络模拟器以不同丢包率（0.2%、1%、0.13%）丢弃部分数据包，以进一步模拟真实场景。在四种攻击场景记录期间，" +
                       "背景中的正常操作仍在继续。不同设备的操作系统如下：传感器使用Tiny Core Linux，摄像头及其服务器使用Ubuntu，" +
                       "攻击者使用Kali Linux。该数据集通过模拟真实的物联网环境，提供了在各种网络攻击场景下的数据，用于研究网络安全防护和检测技术。<br>" +
                       "该数据集具有四个重要意义：模拟真实的MQTT物联网网络正常操作场景：提供了一个逼真的物联网网络环境，用于研究正常和异常情况下的" +
                       "数据流量；涵盖了通用网络扫描攻击和MQTT暴力破解攻击：不仅包括常见的网络扫描攻击，还首次加入了与MQTT协议相关的攻击数据；" +
                       "可用于构建和评估物联网入侵检测系统：研究人员可以利用此数据集开发、测试和优化物联网环境下的入侵检测系统（IDS）；" +
                       "首个包含MQTT场景和攻击数据的数据集：填补了MQTT相关攻击数据的空白，为进一步研究和创新提供了数据基础。该数据集以原始捕获格式" +
                       "（.pcap文件）和处理后的特征集提供。特征集包括以下三种类型：基于数据包的特征；单向流量特征；双向流量特征。其中，" +
                       "双向流量特征的某些特征具有两个值，分别用于记录前向流量（fwd）和后向流量（bwd）。为避免某些特征的影响，" +
                       "特定特征如源和目的IP地址、协议、MQTT标志等被剔除。数据集按75%和25%的比例分为训练集和测试集。",
          features: [
            { name: "Proto", description: "协议类型" },
            { name: "Sport", description: "源端口" },
            { name: "Dport", description: "目标端口" },
            { name: "Dur", description: "持续时间" },
            { name: "SrcPkts", description: "源数据包数" },
            { name: "DstPkts", description: "目的数据包数" },
            { name: "SrcBytes", description: "源字节数" },
            { name: "DstBytes", description: "目的字节数" },
            { name: "Rate", description: "传输速率" },
            { name: "sTtl'", description: "源TTL" },
            { name: "dTtl", description: "目的TTL" },
            { name: "SrcWin", description: "源窗口大小" },
            { name: "DstWin", description: "目的窗口大小"},
            { name: "TcpRtt", description: "TCP往返时间"},
            { name: "SynAck", description: "SYN-ACK时间"},
            { name: "AckDat", description: "确认数据量"}
          ],
          labelRules: `标签生成部分主要通过解析网络流量的协议类型（如TCP、UDP、ICMP等）、端口号、数据包数量、传输速率等特征，来判断流量是否为正常流量或潜在的攻击流量，具体规则如下：<br>
                       •小包攻击检测：如果目的数据包数（dpkts）少于5，且传输速率（rate）大于500或源字节数（sbytes）超过10000，则标记为“小包攻击”。<br>
                       •MQTT协议（端口1883）：若协议为MQTT且目的数据包少于4，源字节数大于5000，则标记为“MQTT攻击”。<br>
                       •DNS协议（UDP协议，端口53）：如果目的数据包数超过1000或传输速率超过5000，则标记为“DNS洪水攻击”。<br>
                       •ICMP协议（ICMP洪水攻击检测）：如果目的数据包数超过1000，标记为“ICMP洪水攻击”。<br>
                       •视频流量滥用（MPEG TS或H.264协议）：若协议为MPEG TS或H.264，且传输速率超过10000，标记为“视频流量滥用”。<br>
                       •TCP协议（端口扫描或洪水攻击）：当目的数据包数少于5且传输速率超过1000，标记为“TCP端口扫描或洪水攻击”。若目的端口为80且源字节数大于1000000，标记为“HTTP洪水攻击”。<br>
                       •ARP欺骗攻击：若协议为ARP且目的数据包数超过100，标记为“ARP欺骗攻击”。<br>
                       •STP网络攻击（网络环路攻击）：若协议为STP且数据包数超过1000，标记为“STP网络攻击”。<br>
                       •默认规则：如果不满足上述条件，则标记为“正常流量”。<br>
                       这些规则通过结合流量特征来生成标签，并根据协议和特定攻击类型对网络流量进行分类。`
        };
      } else if (datasetName === "mix_1") {
        datasetInfo.value = {
          description: "将MedBIoT数据集、UNSW-NB15数据集和USTC-TFC2016数据集相融合。MedBIoT数据集旨在帮助开发基于机器学习的物联网（IoT）僵尸网络检测系统。" +
                       "该数据集是在一个中型的IoT网络中生成，模拟了包含正常和僵尸网络流量的真实IoT环境。数据集中的流量来自各种IoT设备，" +
                       "如智能家居系统，适用于构建监督学习和无监督学习模型，以检测僵尸网络攻击。UNSW-NB15数据集，是为评估网络入侵检测系统（NIDS）" +
                       "而创建的。该数据集是在澳大利亚网络安全中心（ACCS）的Cyber Range实验室中，使用IXIA PerfectStorm工具生成的，" +
                       "包含现代网络中正常和异常流量的混合数据。通过IXIA工具模拟了表VIII中列出的九类攻击，IXIA工具能够从CVE网站实时获取最新的" +
                       "攻击信息，该网站是一个公开收录安全漏洞与暴露信息的数据库。USTC-TFC2016数据集被描述为一个用于恶意软件流量分类的数据集。" +
                       "该数据集由中国科学技术大学（USTC）开发，专门用于网络流量的恶意软件检测和分类研究。" +
                       "USTC-TFC2016数据集包含大量的恶意软件流量样本，涵盖了多种恶意软件家族，如病毒、蠕虫、特洛伊木马等，同时也包含了正常的网络流量。",
          features: [
            { name: "Proto", description: "协议类型" },
            { name: "Sport", description: "源端口" },
            { name: "Dport", description: "目标端口" },
            { name: "Dur", description: "持续时间" },
            { name: "SrcPkts", description: "源数据包数" },
            { name: "DstPkts", description: "目的数据包数" },
            { name: "SrcBytes", description: "源字节数" },
            { name: "DstBytes", description: "目的字节数" },
            { name: "Rate", description: "传输速率" },
            { name: "sTtl'", description: "源TTL" },
            { name: "dTtl", description: "目的TTL" },
            { name: "SrcWin", description: "源窗口大小" },
            { name: "DstWin", description: "目的窗口大小"},
            { name: "TcpRtt", description: "TCP往返时间"},
            { name: "SynAck", description: "SYN-ACK时间"},
            { name: "AckDat", description: "确认数据量"}
          ],
          labelRules: `将MQTT-IoT的数据集与jiami2020数据集混合，规则将两个判断规则相叠加即可。`
        };
      } else if (datasetName === "mix_2") {
        datasetInfo.value = {
          description: "将MQTT数据集和jiami2020数据集相融合。MQTT数据集包含四种攻击类型：Aggressive scan (Scan A)：" +
                       "激进的扫描攻击；User Datagram Protocol (UDP) scan (Scan sU)：UDP扫描攻击；" +
                       "Sparta SSH brute-force (Sparta)：使用Sparta工具进行的SSH暴力破解攻击；" +
                       "MQTT brute-force attack (MQTT BF)：MQTT协议的暴力破解攻击。数据通过tcpdump工具获取，记录以太网流量并导出为pcap文件。" +
                       "Jiami2020数据集是一种基于文件划分的网络流量数据集。该数据集将网络流量分为两类：black代表异常流量，" +
                       "表示可能含有恶意行为的流量数据；white代表正常流量，即未检测到攻击或异常行为的常规网络数据。该数据集可以帮助研究人员在正常" +
                       "与异常流量的对比中构建入侵检测系统，检测出潜在的恶意流量模式，从而提高对网络攻击的识别能力。",
          features: [
            { name: "Proto", description: "协议类型" },
            { name: "Sport", description: "源端口" },
            { name: "Dport", description: "目标端口" },
            { name: "Dur", description: "持续时间" },
            { name: "SrcPkts", description: "源数据包数" },
            { name: "DstPkts", description: "目的数据包数" },
            { name: "SrcBytes", description: "源字节数" },
            { name: "DstBytes", description: "目的字节数" },
            { name: "Rate", description: "传输速率" },
            { name: "sTtl'", description: "源TTL" },
            { name: "dTtl", description: "目的TTL" },
            { name: "SrcWin", description: "源窗口大小" },
            { name: "DstWin", description: "目的窗口大小"},
            { name: "TcpRtt", description: "TCP往返时间"},
            { name: "SynAck", description: "SYN-ACK时间"},
            { name: "AckDat", description: "确认数据量"}
          ],
          labelRules: `将MedBioT数据集与UNSW数据集和USTC数据集相融合，规则将三个判断规则叠加即可。`
        };
      }
    };

    return {
      scenes,
      selectedScene,
      selectedDataset,
      filteredDatasets,
      datasetInfo,
      navigateTo,
      updateDatasets,
      showDatasetDetails,
    };
  },
};
</script>

<style scoped>
.scene-dataset-selection {
  padding: 20px;
}

.dataset-details {
  margin-top: 20px;
}
</style>
