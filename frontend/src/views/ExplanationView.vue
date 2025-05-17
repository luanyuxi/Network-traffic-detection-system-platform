<template>
  <div class="explanation-view">
    <h2>规则解释 - {{ dataset }}</h2>

    <!-- 根据每个数据集的解释，遍历各个行为（如潜在攻击和非攻击行为） -->
    <el-card
      v-for="(section, index) in explanations[dataset] || []"
      :key="index"
      class="explanation-card"
      shadow="hover"
    >
      <h3>{{ section.title }}</h3>

      <el-collapse>
        <!-- 遍历每个行为下的规则 -->
        <el-collapse-item
          v-for="(rule, ruleIndex) in section.rules"
          :key="ruleIndex"
          :title="'规则 ' + (ruleIndex + 1)"
        >
          <div class="rule-content">
            <p><strong>规则条件：</strong> {{ rule.condition }}</p>
            <p><strong>解释：</strong> {{ rule.explanation }}</p>
          </div>

          <div v-if="rule.significantFeatures.length" class="significant-features">
            <h4>影响较大的特征：</h4>
            <ul>
              <li v-for="feature in rule.significantFeatures" :key="feature.name">
                <strong>{{ feature.name }}</strong>：{{ feature.description }}
              </li>
            </ul>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

export default {
  setup() {
    const route = useRoute();
    const dataset = ref(route.query.dataset || 'car_baseline_1');

    // 规则解释数据框架
    const explanations = ref({
      car_baseline_1: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [0.0, 1.0] AND x2 in [0.0, 0.9302] AND x3 in [-0.001, 0.001] AND x4 in [0.0, 1.0] AND x5 in [0.0, 1.0] AND x6 in [0.0, 1.0] AND x7 in [0.0, 1.0] AND x8 in [0.0, 1.0] AND x9 in [0.0, 1.0] AND x10 in [0.0, 1.0] AND x11 in [0.0, 1.0] THEN y > 0',
              explanation: '此规则表明，当所有特征（时间戳、仲裁ID、DLC和数据字段）处于这些范围时，可能存在潜在的攻击行为。尽管所有特征值都集中在[0.0, 1.0]的范围内，但特征的组合暗示了数据流的某种异常模式，可能与恶意行为相关。',
              significantFeatures: [
                {name: 'x2 (Arbitration_ID)', description: '其范围为[0.0, 0.9302]，表明仲裁ID可能处于特定的控制范围内，攻击者可能通过操纵该ID进行恶意数据注入。'},
                {name: 'x3 (DLC)', description: '数据长度代码（DLC）的变化范围极小（[-0.001, 0.001]），这表明固定的数据长度可能用于某种攻击模式。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0158, 1.0105] AND x2 in [-0.0913, 0.9459] AND x3 in [-0.0704, 0.0158] AND x4 in [-0.0302, 1.0861] AND x5 in [-0.0383, 1.0609] AND x6 in [-0.0278, 1.0452] AND x7 in [-0.0872, 1.0436] AND x8 in [-0.0356, 1.0162] AND x9 in [-0.0803, 1.0683] AND x10 in [-0.0109, 1.0865] AND x11 in [-0.0912, 1.0999] THEN y > 0',
              explanation: '这一规则显示，各特征的取值范围更广，数据的多样性可能更复杂，表明攻击行为更加显著。特征值的波动，尤其是与仲裁ID、数据长度代码和数据字段相关的特征，可能指向更具侵略性的数据注入或欺骗攻击。',
              significantFeatures: [
                {name: 'x2 (Arbitration_ID)', description: '仲裁ID的范围扩大，表明攻击者可能通过多种ID发送恶意信息，扩大攻击覆盖面。'},
                {name: 'x3 (DLC)', description: 'DLC的范围有所扩大，表明数据长度的波动可能暗示数据包结构被篡改，进一步强化了攻击行为的可能性。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0186, 1.0282] AND x2 in [-0.0138, 0.9466] AND x3 in [-0.0511, 0.0926] AND x4 in [-0.0837, 1.0186] AND x5 in [-0.0414, 1.0596] AND x6 in [-0.0328, 1.0276] AND x7 in [-0.0713, 1.0527] AND x8 in [-0.049, 1.0477] AND x9 in [-0.0856, 1.0966] AND x10 in [-0.0722, 1.0198] AND x11 in [-0.0615, 1.0796] THEN y <= 0',
              explanation: '这条规则表明，在较广泛的特征值区间内，网络行为是非攻击行为。虽然特征值波动较大，但总体上这些波动属于正常的数据流动，未显示出攻击行为的特征。',
              significantFeatures: [
                {name: 'x3 (DLC)', description: '数据长度代码（DLC）的波动较为明显（[-0.0511, 0.0926]），表明正常通信中存在一定的数据包长度变化，但这在合法通信中是可以接受的。'},
                {name: 'x9 (Data5)', description: '数据字段的范围较大，表明合法通信中的数据包可能包含更多内容，但这些变化仍未达到攻击的水平。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0561, 1.0672] AND x2 in [-0.0702, 0.976] AND x3 in [-0.0426, 0.0191] AND x4 in [-0.0224, 1.0814] AND x5 in [-0.0521, 1.0376] AND x6 in [-0.0423, 1.0538] AND x7 in [-0.0674, 1.0119] AND x8 in [-0.025, 1.065] AND x9 in [-0.0146, 1.0782] AND x10 in [-0.0491, 1.0871] AND x11 in [-0.0744, 1.0705] THEN y <= 0',
              explanation: '在这条规则中，特征值的区间波动较大，尤其是时间戳和数据字段，但这些变化仍被认为是非攻击行为，可能是由于数据包结构没有明显的异常或恶意操纵。',
              significantFeatures: [
                {name: 'x1 (Timestamp)', description: '时间戳的变化范围较广（[-0.0561, 1.0672]），表明通信在时间上的波动性，可能是由于网络延迟或正常的数据流动引起的，但并未触发攻击的特征。'},
                {name: 'x5 (Data1)', description: 'Data1字段在[-0.0521, 1.0376]范围内，虽然数据值有所波动，但这些变化仍然在合法通信的范围内。'},
              ],
            },
          ],
        },
      ],
      car_baseline_2: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0895, 0.0328] AND x2 in [-0.0388, 0.7431] AND x3 in [-0.0766, 0.6886] AND x4 in [-0.0673, 0.9913] AND x5 in [-0.0298, 0.1788] AND x6 in [-0.059, 0.1431] AND x7 in [-0.0931, 0.0828] AND x8 in [-0.0166, 0.067] AND x9 in [-0.0509, 0.0629] AND x10 in [-0.0723, 0.0439] AND x11 in [-0.0338, 0.0456] AND x12 in [-0.0129, 0.1354] AND x13 in [0.0063, 1.0835] AND x14 in [-0.0497, 0.0776] AND x15 in [-0.0567, 0.057] AND x16 in [-0.0596, 0.0596] THEN y > 0',
              explanation: '此规则指出，当x1至x16的特征值都落在这些区间时，预测为潜在攻击行为。特征显示，攻击者可能通过较长的生存时间（TTL）和适中的数据传输量，试图进行隐蔽的探测或攻击行为。',
              significantFeatures: [
                {name: 'x13（TCP往返时间，TcpRtt）', description: 'TcpRtt较大（[0.0063, 1.0835]），可能意味着数据包往返延迟较长，提示攻击者可能利用复杂网络路径或进行分布式攻击。'},
                {name: 'x3（目标端口，Dport）', description: 'Dport范围较宽，攻击者可能通过多个端口进行攻击或探测，增加其隐蔽性。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0715, 0.0867] AND x2 in [-0.0842, 0.523] AND x3 in [0.4844, 1.0128] AND x4 in [-0.029, 1.0645] AND x5 in [-0.0356, 0.2979] AND x6 in [-0.0801, 0.6407] AND x7 in [-0.0863, 0.0711] AND x8 in [-0.0588, 0.6998] AND x9 in [-0.0347, 0.0408] AND x10 in [-0.0713, 0.0822] AND x11 in [-0.0825, 0.0206] AND x12 in [-0.0807, 0.1852] AND x13 in [0.0027, 0.9627] AND x14 in [-0.0959, 0.1505] AND x15 in [-0.0302, 0.0697] AND x16 in [-0.0212, 0.1] THEN y > 0',
              explanation: '该规则表明，较高的数据传输量和端口特征可能指向潜在的攻击行为，尤其是在x3（Dport）范围较高时。攻击者可能通过大量数据包传输尝试攻击或破坏网络。',
              significantFeatures: [
                {name: 'x3（目标端口，Dport）', description: 'Dport在[0.4844, 1.0128]的范围内，表明攻击者可能通过多个目标端口进行传输，可能是典型的探测或扫描行为。'},
                {name: 'x4（持续时间，Dur）', description: 'Dur的范围较大（[-0.029, 1.0645]），表明攻击者可能在较长时间内持续发送数据包，试图突破防御。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0769, 0.03] AND x2 in [-0.0761, 1.0506] AND x3 in [-0.0542, 0.5801] AND x4 in [-0.0506, 1.012] AND x5 in [-0.0604, 0.1123] AND x6 in [-0.0743, 0.1894] AND x7 in [-0.0854, 0.0692] AND x8 in [-0.0628, 0.094] AND x9 in [-0.0188, 0.0369] AND x10 in [-0.0456, 0.1029] AND x11 in [-0.0597, 0.0928] AND x12 in [-0.0736, 0.1751] AND x13 in [-0.0101, 1.0895] AND x14 in [-0.0369, 0.1448] AND x15 in [-0.0358, 0.0663] AND x16 in [-0.0305, 0.0981] THEN y <= 0',
              explanation: '这条规则表示，当16个特征的值都位于这些范围时，预测为非攻击行为。尽管部分特征，如持续时间（Dur）和目标端口（Dport）范围相对较宽，但其他特征较为稳定且接近中值，表明这些网络通信可能是合法的、正常的数据传输。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '范围较宽（[-0.0761, 1.0506]），源端口的多样性可能表示网络中的常规合法通信。'},
                {name: 'x4（持续时间，Dur）', description: '持续时间范围较大（[-0.0506, 1.012]），表明这些通信在时间上较长，可能代表正常的业务活动或传输。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0213, 0.0533] AND x2 in [0.4066, 1.0179] AND x3 in [-0.0308, 0.6634] AND x4 in [-0.0423, 1.0192] AND x5 in [-0.0947, 0.1519] AND x6 in [-0.0984, 0.184] AND x7 in [-0.0206, 0.0706] AND x8 in [-0.0958, 0.1228] AND x9 in [-0.0123, 0.1013] AND x10 in [-0.0665, 0.0763] AND x11 in [-0.1067, 0.0289] AND x12 in [-0.0248, 0.1461] AND x13 in [0.028, 0.8856] AND x14 in [-0.0607, 0.1092] AND x15 in [-0.0732, 0.0449] AND x16 in [-0.0348, 0.1801] THEN y <= 0',
              explanation: '此规则的特征值范围较大，但并没有指向潜在的攻击行为。数据传输速率和持续时间较高，符合正常的网络通信模式，未出现异常或恶意流量的特征。',
              significantFeatures: [
                {name: 'x4（持续时间，Dur）', description: '持续时间的范围从[-0.0423, 1.0192]，表明正常的业务通信通常会持续较长时间，适合合法的数据传输。'},
                {name: 'x13（TCP往返时间，TcpRtt）', description: '在非攻击行为中，TCP往返时间的范围较大，表明通信可能经过多个网络节点，但属于正常现象。'},
              ],
            },
          ],
        },
      ],
      iot_baseline_1: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.1036, 0.0223] AND x2 in [0.1957, 1.0768] AND x3 in [-0.0894, 0.4612] AND x4 in [-0.0703, 0.3555] AND x5 in [-0.0893, 0.0234] AND x6 in [-0.0381, 0.0558] AND x7 in [-0.0264, 0.0583] AND x8 in [-0.0298, 0.0845] AND x9 in [-0.0361, 0.3437] AND x10 in [-0.0877, 0.33] AND x11 in [0.0691, 0.4555] AND x12 in [-0.0219, 1.0659] AND x13 in [-0.094, 0.5804] AND x14 in [-0.0497, 0.0239] AND x15 in [-0.097, 0.0131] AND x16 in [-0.0114, 0.4088] THEN y > 0',
              explanation: '此规则表明，某些特征如源端口（Sport）、数据包速率（Rate）和TTL等处于较大范围时，网络行为可能为潜在攻击行为。这些特征组合可能代表了恶意流量的行为模式，例如不断变化的数据传输速率和较高的TTL值，这通常是攻击流量的特征。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '范围较大（[0.1957, 1.0768]），显示源设备可能使用了多个端口，这可能暗示攻击者试图通过多个端口进行探测或隐蔽攻击。'},
                {name: 'x12（源窗口大小，SrcWin）', description: '源窗口大小的范围较大（[-0.0219, 1.0659]），表明可能存在较大量的数据传输或非正常的流量模式，进一步提示潜在攻击行为。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0576, 0.053] AND x2 in [0.6068, 0.9399] AND x3 in [0.239, 0.94] AND x4 in [-0.0114, 0.3157] AND x5 in [-0.0105, 0.0235] AND x6 in [-0.089, 0.0936] AND x7 in [-0.0284, 0.064] AND x8 in [-0.0561, 0.063] AND x9 in [-0.0743, 0.2775] AND x10 in [-0.069, 0.3943] AND x11 in [0.0157, 0.4584] AND x12 in [-0.0693, 0.0972] AND x13 in [-0.0717, 0.0669] AND x14 in [-0.0719, 0.0784] AND x15 in [-0.0309, 0.0871] AND x16 in [-0.0693, 0.1955] THEN y > 0',
              explanation: '此规则表明，当数据传输量、源端口、目标端口和TTL等特征值较为波动时，推测为潜在攻击行为。攻击者可能通过调整数据包的TTL或端口分布以绕过检测。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '源端口范围较高，表明可能存在多个源端口的使用，攻击者可能在尝试通过不同端口传输恶意数据。'},
                {name: 'x9（数据传输速率，Rate）', description: '数据传输速率波动较大（[-0.0743, 0.2775]），这可能意味着攻击流量以不规律的速率发送，增加了流量的隐蔽性。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0678, 0.0638] AND x2 in [0.5245, 0.9864] AND x3 in [0.5053, 1.0274] AND x4 in [-0.018, 0.3505] AND x5 in [-0.0519, 0.0854] AND x6 in [-0.0452, 0.0705] AND x7 in [-0.0747, 0.0831] AND x8 in [-0.0222, 0.0516] AND x9 in [-0.0244, 0.2907] AND x10 in [-0.0278, 0.3115] AND x11 in [0.0262, 0.1289] AND x12 in [-0.0201, 0.0353] AND x13 in [-0.0216, 0.0918] AND x14 in [-0.0848, 0.0568] AND x15 in [-0.0439, 0.0261] AND x16 in [-0.0812, 0.2195] THEN y <= 0',
              explanation: '此规则指出，当特征x1到x16处于给定范围时，预测为非攻击行为。虽然目标端口（Dport）和数据包数量（SrcPkts、DstPkts）的值相对较高，但这些通信特征仍然属于正常范围，未显示出恶意流量的特征。',
              significantFeatures: [
                {name: 'x3（目标端口，Dport）', description: '目标端口范围较高（[0.5053, 1.0274]），但这些端口并未呈现异常使用模式，说明此类端口的使用是正常的网络通信。'},
                {name: 'x9（数据传输速率，Rate）', description: '虽然数据速率在[-0.0244, 0.2907]之间有一定波动，但这种变化符合常规网络流量的特征。'},
              ],
            },
            {
              condition: 'If x1 in [-0.1058, 0.1002] AND x2 in [-0.0473, 0.4303] AND x3 in [0.8263, 0.8976] AND x4 in [-0.0233, 0.0888] AND x5 in [-0.1055, 0.0212] AND x6 in [-0.0582, 0.0594] AND x7 in [-0.0995, 0.0309] AND x8 in [-0.0748, 0.026] AND x9 in [-0.0532, 0.0676] AND x10 in [0.2635, 0.3922] AND x11 in [0.3821, 0.5129] AND x12 in [-0.0759, 0.0867] AND x13 in [-0.0225, 0.059] AND x14 in [-0.0227, 0.0228] AND x15 in [-0.0959, 0.1096] AND x16 in [-0.1096, 0.0699] THEN y <= 0',
              explanation: '此规则显示，当特征值大部分落在较低范围内，特别是数据包传输量（SrcPkts、DstPkts）和数据传输持续时间（Dur）较短时，推测为非攻击行为。这些特征均表明网络流量属于普通的短期通信，未表现出异常行为。',
              significantFeatures: [
                {name: 'x3（目标端口，Dport）', description: 'Dport范围相对集中，端口号较高，表明此类网络通信属于稳定的合法通信。'},
                {name: 'x11（目标端TTL，dTtl）', description: '目标设备TTL的值相对较大（[0.3821, 0.5129]），表明数据包经过较多跳数，属于常规网络数据传播。'},
              ],
            },
          ],
        },
      ],
      iot_baseline_2: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.1036, 0.0223] AND x2 in [0.3106, 0.743] AND x3 in [-0.0756, 0.0482] AND x4 in [-0.0703, 0.1022] AND x5 in [-0.0893, 0.0221] AND x6 in [-0.0381, 0.0548] AND x7 in [-0.0264, 0.0617] AND x8 in [-0.0298, 0.0845] AND x9 in [-0.0361, 0.2755] AND x10 in [-0.0823, 0.0553] AND x11 in [0.1929, 0.2553] AND x12 in [-0.0218, 0.0738] AND x13 in [-0.094, 0.0198] AND x14 in [-0.0497, 0.0257] AND x15 in [-0.097, 0.0153] AND x16 in [-0.0114, 0.088] THEN y > 0',
              explanation: '此规则表明，在这些特征范围内，网络行为被判定为潜在攻击行为。数据传输速率和TTL波动较大，特别是在目标端口（Dport）和生存时间（TTL）的较大范围内，显示出可能的异常行为或攻击模式。',
              significantFeatures: [
                {name: 'x9（数据传输速率，Rate）', description: '数据传输速率波动较大，表明可能有不规律的数据包流，提示潜在的攻击流量。'},
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL范围较大，表明数据包可能经过了多次跳跃，攻击者可能试图绕过安全检测。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0576, 0.053] AND x2 in [-0.0639, 0.3041] AND x3 in [-0.028, 0.6154] AND x4 in [-0.0114, 0.6729] AND x5 in [-0.0105, 0.0289] AND x6 in [-0.089, 0.0964] AND x7 in [-0.0284, 0.0721] AND x8 in [-0.0561, 0.0634] AND x9 in [-0.0743, 0.2093] AND x10 in [-0.069, 0.1097] AND x11 in [0.1395, 0.2582] AND x12 in [-0.0692, 0.1467] AND x13 in [-0.0717, 0.0178] AND x14 in [-0.0719, 0.0794] AND x15 in [-0.0309, 0.0882] AND x16 in [-0.0693, 0.0192] THEN y > 0',
              explanation: '此规则指向潜在攻击行为。在源端口（Sport）、数据传输速率（Rate）和TTL的较大范围内，通信显示出异常的流量行为，这可能提示攻击者试图绕过检测，通过不断变化的数据模式进行攻击。',
              significantFeatures: [
                {name: 'x9（数据传输速率，Rate）', description: '数据传输速率的波动范围较大，提示可能存在不规则的流量，增加了潜在攻击的可能性。'},
                {name: 'x4（持续时间，Dur）', description: '持续时间较长，表明数据包可能在网络中停留时间较长，这可能是攻击者进行持续探测或缓慢渗透的行为。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0678, 0.0638] AND x2 in [0.2373, 0.5568] AND x3 in [-0.0794, 0.0619] AND x4 in [-0.018, 0.2809] AND x5 in [-0.0519, 0.0807] AND x6 in [-0.0452, 0.0668] AND x7 in [-0.0747, 0.0828] AND x8 in [-0.0222, 0.0515] AND x9 in [-0.0244, 0.2225] AND x10 in [-0.0224, 0.0369] AND x11 in [0.16, 0.247] AND x12 in [-0.0201, 0.0485] AND x13 in [-0.0216, 0.0426] AND x14 in [-0.0848, 0.0475] AND x15 in [-0.0439, 0.0164] AND x16 in [-0.0812, 0.0698] THEN y <= 0',
              explanation: '此规则表明，在给定的特征值范围内，网络行为被判定为非攻击行为。数据传输量较低，目标端口和数据包特征稳定，表明网络通信是正常的，没有显示异常流量或恶意活动的迹象。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '源端口范围较小，表明通信设备之间的数据传输较为稳定，源端口的波动较少，通常反映合法流量。'},
                {name: 'x11（目标端TTL，dTtl）', description: '目标端TTL的范围相对较大，显示数据包经过多个跳数，属于正常的网络传播。'},
              ],
            },
            {
              condition: 'If x1 in [-0.1058, 0.1002] AND x2 in [0.5016, 0.8734] AND x3 in [-0.0245, 0.07] AND x4 in [-0.025, 0.2905] AND x5 in [-0.0955, 0.014] AND x6 in [-0.0482, 0.0507] AND x7 in [-0.0896, 0.0243] AND x8 in [-0.0648, 0.0162] AND x9 in [-0.0532, 0.2494] AND x10 in [-0.0211, 0.1075] AND x11 in [0.1877, 0.3027] AND x12 in [-0.0659, 0.0846] AND x13 in [-0.0125, 0.0495] AND x14 in [-0.0127, 0.0191] AND x15 in [-0.0859, 0.1008] AND x16 in [-0.0996, 0.0668] THEN y <= 0',
              explanation: '在此规则中，特征显示为非攻击行为。持续时间（Dur）和数据包速率（Rate）表明通信较为正常，虽然存在一些波动，但这些特征表明这是合法的通信活动，而非恶意流量。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '范围在[0.5016, 0.8734]之间，表明源端口较为集中，反映出稳定的数据传输流。'},
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL较高，表明数据包经过多个跳数的传输，符合正常的网络数据传播。'},
              ],
            },
          ],
        },
      ],
      iot_baseline_3: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.1036, 0.0223] AND x2 in [-0.0453, 1.0882] AND x3 in [0.1763, 0.2994] AND x4 in [-0.0262, 1.0526] AND x5 in [0.1754, 0.7242] AND x6 in [0.2266, 0.7586] AND x7 in [0.2408, 0.7672] AND x8 in [0.2043, 0.6998] AND x9 in [-0.036, 0.0973] AND x10 in [0.9023, 1.04] AND x11 in [-0.0332, 0.045] AND x12 in [-0.0318, 0.076] AND x13 in [-0.0415, 0.0918] AND x14 in [-0.0428, 0.0578] AND x15 in [-0.0903, 0.0562] AND x16 in [-0.009, 0.1155] THEN y > 0',
              explanation: '这一规则表明，尽管部分特征如TTL和数据包数量的值处于中等范围，网络行为可能为潜在攻击行为。源端口和数据传输速率的较大波动可能暗示攻击者通过调整传输速率和端口使用进行隐蔽攻击。',
              significantFeatures: [
                {name: 'x5（源数据包数量，SrcPkts）', description: '数据包数量较大，表明可能存在大规模数据传输，攻击者可能在尝试通过大量数据流量进行攻击。'},
                {name: 'x6（目标数据包数量，DstPkts）', description: '目标端的数据包数量较大，显示了潜在攻击者在目标系统上传输大量数据的行为。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0576, 0.053] AND x2 in [-0.0522, 1.0188] AND x3 in [0.2239, 0.3528] AND x4 in [-0.0112, 0.3672] AND x5 in [0.1071, 0.4311] AND x6 in [0.0287, 0.5023] AND x7 in [0.0929, 0.4819] AND x8 in [0.0509, 0.4242] AND x9 in [-0.074, 0.4645] AND x10 in [0.921, 1.1043] AND x11 in [-0.0866, 0.0479] AND x12 in [-0.0693, 0.0972] AND x13 in [-0.0192, 0.0898] AND x14 in [-0.0652, 0.4655] AND x15 in [-0.024, 0.41] AND x16 in [-0.0669, 0.4215] THEN y > 0',
              explanation: '此规则显示的网络行为为潜在攻击行为。特征如TTL和数据包数量的范围较大，且传输速率和目标端口波动较为显著，可能表明攻击者通过增加数据包传输和调整TTL试图进行隐蔽的攻击。',
              significantFeatures: [
                {name: 'x10（生存时间，sTtl）', description: 'TTL高值显示数据包在网络中传输时间较长，可能是攻击者调整TTL以规避检测。'},
                {name: 'x6（目标数据包数量，DstPkts）', description: '数据包数量较大，表明攻击者可能通过目标端传输大量数据进行恶意活动。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0842, 0.0852] AND x2 in [-0.0622, 0.6863] AND x3 in [0.2034, 0.3804] AND x4 in [-0.0925, 0.5665] AND x5 in [0.0722, 0.4404] AND x6 in [0.0888, 0.4489] AND x7 in [0.0836, 0.4517] AND x8 in [0.0892, 0.3763] AND x9 in [-0.0607, 0.5242] AND x10 in [0.9782, 1.1051] AND x11 in [-0.0977, 0.0367] AND x12 in [-0.0439, 0.0147] AND x13 in [0.0157, 0.1214] AND x14 in [-0.0701, 0.4419] AND x15 in [-0.0336, 0.4022] AND x16 in [-0.0165, 0.4706] THEN y <= 0',
              explanation: '此规则表明，在这些特征的取值范围内，网络行为被预测为非攻击行为。特征如数据包数（x5、x6、x7）的中等数值和目标端TTL（x10）的高值显示出正常的通信活动，且没有显示出恶意流量的特征。',
              significantFeatures: [
                {name: 'x10（数据包的生存时间，sTtl）', description: '生存时间在较高范围内（[0.9782, 1.1051]），表明数据包在网络中的传播时间较长，属于正常的网络行为。'},
                {name: 'x9（传输速率，Rate）', description: '速率的中等波动范围显示通信活动稳定，不涉及大规模数据传输，这符合非攻击行为的特征。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0678, 0.0638] AND x2 in [0.2881, 1.0752] AND x3 in [0.1725, 0.3131] AND x4 in [-0.0178, 0.4627] AND x5 in [0.0658, 0.492] AND x6 in [0.0724, 0.4782] AND x7 in [0.0466, 0.4976] AND x8 in [0.0848, 0.4127] AND x9 in [-0.0241, 0.4935] AND x10 in [0.9622, 1.0215] AND x11 in [-0.0661, 0.0366] AND x12 in [-0.0201, 0.0353] AND x13 in [0.0309, 0.1147] AND x14 in [-0.078, 0.4332] AND x15 in [-0.0374, 0.3382] AND x16 in [-0.0787, 0.4715] THEN y <= 0',
              explanation: '该规则预测的网络行为为非攻击行为。多个特征如源端口（x2）和目标端TTL（x10）的高值显示出正常通信特征，特别是数据包传输和TTL显示稳定且无显著异常。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '源端口范围较大，显示了较广泛的端口使用，这通常与合法流量相一致。'},
                {name: 'x10（生存时间，sTtl）', description: 'TTL高值意味着数据包在网络中的存留时间较长，符合普通网络行为的特征。'},
              ],
            },
          ],
        },
      ],
      encrypt_thirdparty_1: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.1036, 0.0223] AND x2 in [-0.0818, 0.093] AND x3 in [-0.0994, 0.0237] AND x4 in [0.3635, 1.0483] AND x5 in [-0.089, 0.2167] AND x6 in [-0.0381, 0.2438] AND x7 in [-0.0263, 0.1179] AND x8 in [-0.0298, 0.2755] AND x9 in [-0.0361, 0.0978] AND x10 in [-0.0977, 0.04] AND x11 in [-0.0332, 0.045] AND x12 in [-0.0183, 0.0699] AND x13 in [0.5898, 0.7231] AND x14 in [-0.0497, 0.0453] AND x15 in [-0.097, 0.0345] AND x16 in [-0.0114, 0.3752] THEN y > 0',
              explanation: '该规则预测网络行为为潜在攻击行为。特征如持续时间（x4）和TCP往返时间（x13）值较高，显示了攻击者可能利用较长时间的持续性流量和不稳定的响应时间进行攻击。',
              significantFeatures: [
                {name: 'x13（TCP往返时间，TcpRtt）', description: 'TCP响应时间较大，表明通信有异常的响应延迟，可能是攻击行为的一部分。'},
                {name: 'x4（持续时间，Dur）', description: '持续时间较长，可能是攻击者通过延长通信时间来渗透网络。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0576, 0.053] AND x2 in [-0.0639, 0.0242] AND x3 in [-0.0518, 0.0771] AND x4 in [-0.0106, 0.5601] AND x5 in [-0.0099, 0.0232] AND x6 in [-0.0885, 0.0931] AND x7 in [-0.0282, 0.07] AND x8 in [-0.0561, 0.0647] AND x9 in [-0.0743, 0.0403] AND x10 in [-0.079, 0.1043] AND x11 in [0.9134, 1.0479] AND x12 in [-0.0654, 0.1012] AND x13 in [0.6121, 0.7212] AND x14 in [-0.0719, 0.0789] AND x15 in [-0.0308, 0.0875] AND x16 in [-0.0649, 0.0493] THEN y > 0',
              explanation: '此规则预测为潜在攻击行为。特征如目标端TTL（x11）和TCP往返时间（x13）较高，表明了攻击者可能通过不正常的TTL和长时间的通信来进行隐蔽攻击。',
              significantFeatures: [
                {name: 'x11（目标端TTL，dTtl）', description: '目标端TTL值较大，可能是攻击者通过调整TTL值绕过检测。'},
                {name: 'x13（TCP往返时间，TcpRtt）', description: 'TCP响应时间较长，显示了不正常的网络延迟，可能与攻击活'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0678, 0.0638] AND x2 in [-0.0137, 0.0795] AND x3 in [-0.1032, 0.0374] AND x4 in [-0.018, 0.354] AND x5 in [-0.0519, 0.1453] AND x6 in [-0.0452, 0.132] AND x7 in [-0.0747, 0.1916] AND x8 in [-0.0222, 0.1171] AND x9 in [-0.0244, 0.0435] AND x10 in [-0.0378, 0.0215] AND x11 in [-0.0661, 0.0366] AND x12 in [-0.02, 0.0393] AND x13 in [0.0802, 0.736] AND x14 in [-0.0848, 0.4561] AND x15 in [-0.0439, 0.4254] AND x16 in [-0.0812, 0.5228] THEN y <= 0',
              explanation: '该规则显示了一个非攻击行为的预测，特征值范围显示网络活动较为平稳，特别是目标端口（x3）、数据传输速率（x9）和数据包数量（x7、x8）都在正常范围内，表明此通信没有异常。',
              significantFeatures: [
                {name: 'x13（TCP往返时间，TcpRtt）', description: '在[0.0802, 0.736]范围内，反映了数据包的响应时间适中，属于正常的网络活动。'},
                {name: 'x15（目标窗口大小，DstWin）', description: '目标窗口大小较大，显示了稳定的连接和传输行为，没有显现攻击迹象。'},
              ],
            },
            {
              condition: 'If x1 in [-0.1058, 0.1002] AND x2 in [-0.0505, 0.8496] AND x3 in [-0.0483, 0.0421] AND x4 in [0.7343, 1.0841] AND x5 in [-0.0951, 0.21] AND x6 in [-0.048, 0.2478] AND x7 in [-0.0895, 0.081] AND x8 in [-0.0648, 0.2146] AND x9 in [-0.0532, 0.0704] AND x10 in [-0.0365, 0.0922] AND x11 in [-0.0384, 0.0924] AND x12 in [-0.0659, 0.0807] AND x13 in [0.6813, 0.7618] AND x14 in [-0.0127, 0.0378] AND x15 in [-0.0859, 0.1246] AND x16 in [-0.0996, 0.3488] THEN y <= 0',
              explanation: '此规则表明当多个特征值，如TCP往返时间（x13）和持续时间（x4）处于较高范围时，预测为非攻击行为。这显示了通信在正常的网络流量和持续时间内，没有表明恶意流量。',
              significantFeatures: [
                {name: 'x4（持续时间，Dur）', description: '持续时间较长，表示这是较为正常的通信流，没有表现出短期异常的特征。'},
                {name: 'x13（TCP往返时间，TcpRtt）', description: 'TCP往返时间的范围较大，表明通信的响应时间属于正常范围。'},
              ],
            },
          ],
        },
      ],
      encrypt_thirdparty_2: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.1036, 0.0223] AND x2 in [0.623, 1.0882] AND x3 in [-0.0994, 0.0237] AND x4 in [0.1733, 1.0581] AND x5 in [-0.0886, 0.3283] AND x6 in [-0.0374, 0.4344] AND x7 in [-0.0264, 0.0973] AND x8 in [-0.0297, 0.7388] AND x9 in [-0.0361, 0.0966] AND x10 in [0.9023, 1.04] AND x11 in [-0.0232, 0.0483] AND x12 in [0.4748, 1.0659] AND x13 in [-0.0862, 0.0512] AND x14 in [0.1484, 0.5132] AND x15 in [0.0998, 0.5007] AND x16 in [0.0827, 1.0863] THEN y > 0',
              explanation: '此规则表明，当多个特征如目标端TTL（x11）、数据包传输量（x6）和TCP往返时间（x12）值较大时，预测为潜在攻击行为。这些特征可能暗示了攻击者利用大量数据包或不稳定的响应时间进行隐蔽攻击。',
              significantFeatures: [
                {name: 'x12（TCP往返时间，TcpRtt）', description: '响应时间的较高值可能反映了通信中的异常延迟，表明潜在的攻击行为。'},
                {name: 'x8（目标数据包数量，DstBytes）', description: '数据包数量的高值显示出攻击者可能在目标设备上传输大量数据，增加了攻击的可能性。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0576, 0.053] AND x2 in [0.6414, 1.0181] AND x3 in [-0.0518, 0.0771] AND x4 in [0.4089, 1.0185] AND x5 in [0.0265, 0.7889] AND x6 in [-0.0524, 0.9145] AND x7 in [-0.0272, 0.1033] AND x8 in [-0.0538, 0.9988] AND x9 in [-0.0742, 0.0309] AND x10 in [0.921, 1.1043] AND x11 in [-0.0766, 0.0512] AND x12 in [-0.0683, 1.0972] AND x13 in [-0.0716, 0.0492] AND x14 in [-0.0719, 0.4548] AND x15 in [-0.0309, 0.4618] AND x16 in [-0.0693, 0.5239] THEN y > 0',
              explanation: '该规则预测为潜在攻击行为。特征如源端口（x2）、数据包传输速率（x8）和目标端TTL（x10）的高值表明攻击者可能利用大量数据包和较长的TTL值进行持续性攻击。',
              significantFeatures: [
                {name: 'x10（生存时间，sTtl）', description: 'TTL的高值表明数据包可能被攻击者通过调整TTL来绕过检测。'},
                {name: 'x6（目标数据包数量，DstPkts）', description: '目标设备接收到的数据包数量较多，提示潜在攻击行为。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0678, 0.0638] AND x2 in [0.6914, 1.0756] AND x3 in [-0.1032, 0.0374] AND x4 in [-0.018, 0.4024] AND x5 in [-0.0519, 0.2572] AND x6 in [-0.0452, 0.269] AND x7 in [-0.0747, 0.0875] AND x8 in [-0.0222, 0.3324] AND x9 in [-0.0244, 0.0501] AND x10 in [0.9622, 1.0215] AND x11 in [-0.0561, 0.0399] AND x12 in [0.4765, 1.0353] AND x13 in [-0.0138, 0.0745] AND x14 in [0.1102, 0.5111] AND x15 in [0.1491, 0.478] AND x16 in [0.0011, 0.6975] THEN y <= 0',
              explanation: '这条规则预测为非攻击行为，特征如目标端口（x3）、数据传输速率（x9）和TCP往返时间（x12）在正常范围内，显示了合法的通信行为，没有异常流量。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '源端口范围较大（[0.6914, 1.0756]），表明通信发生在较高范围的端口，属于正常网络行为。'},
                {name: 'x10（生存时间，sTtl）', description: 'TTL的范围较高，表示数据包在网络中存留时间较长，符合非攻击通信的特征。'},
              ],
            },
            {
              condition: 'If x1 in [-0.1058, 0.1002] AND x2 in [-0.0605, 0.0358] AND x3 in [0.6677, 1.0321] AND x4 in [-0.025, 1.0799] AND x5 in [-0.0955, 0.2506] AND x6 in [-0.0482, 0.2658] AND x7 in [-0.0896, 0.874] AND x8 in [-0.0648, 0.0207] AND x9 in [-0.0532, 0.6131] AND x10 in [-0.0265, 0.0955] AND x11 in [0.9616, 1.0924] AND x12 in [-0.0659, 0.0767] AND x13 in [-0.0124, 0.0491] AND x14 in [-0.0227, 0.0228] AND x15 in [-0.0959, 0.1096] AND x16 in [-0.1096, 0.0699] THEN y <= 0',
              explanation: '此规则预测为非攻击行为。特征如源端口（x2）、目标端TTL（x11）等数值正常，表明数据流量是合法的，通信持续时间较长但符合非攻击行为的特征。',
              significantFeatures: [
                {name: 'x3（目标端口，Dport）', description: 'TTL范围较高，表明数据包在网络中传播时间较长，属于正常的网络传输。'},
                {name: 'x11（目标端TTL，dTtl）', description: '目标端口范围在高值区域，表明目标设备可能是合法通信的接收方。'},
              ],
            },
          ],
        },
      ],
      encrypt_baseline_1: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.1036, 0.0223] AND x2 in [0.3242, 1.087] AND x3 in [0.49, 0.9998] AND x4 in [-0.0703, 0.8109] AND x5 in [-0.0893, 0.0403] AND x6 in [-0.0381, 0.1005] AND x7 in [-0.0264, 0.2042] AND x8 in [-0.0298, 0.1126] AND x9 in [-0.0361, 0.1241] AND x10 in [-0.0877, 0.5223] AND x11 in [0.0115, 1.035] AND x12 in [-0.0219, 1.0659] AND x13 in [-0.094, 0.0412] AND x14 in [-0.0497, 0.4093] AND x15 in [-0.097, 0.3985] AND x16 in [-0.0114, 0.1144] THEN y > 0',
              explanation: '',
              significantFeatures: [
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL较大，表明数据包可能经过多个跳数，提示了潜在的远程攻击。'},
                {name: 'x10（生存时间，sTtl）', description: 'TTL的高值显示数据包在网络中的停留时间较长，可能是攻击者调整TTL进行攻击的一种方式。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0576, 0.053] AND x2 in [-0.0638, 0.4919] AND x3 in [0.031, 1.0364] AND x4 in [-0.0114, 0.0955] AND x5 in [-0.0105, 0.0226] AND x6 in [-0.089, 0.1148] AND x7 in [-0.0284, 0.073] AND x8 in [-0.0561, 0.0785] AND x9 in [-0.0743, 0.09] AND x10 in [-0.069, 0.5867] AND x11 in [-0.042, 0.1374] AND x12 in [-0.0693, 0.1012] AND x13 in [-0.0717, 0.0393] AND x14 in [-0.0719, 0.0782] AND x15 in [-0.0309, 0.0869] AND x16 in [-0.0693, 0.0181] THEN y > 0',
              explanation: '此规则表明，在源端口（x2）、数据包传输速率（x9）和生存时间（x10）的特定区间内，网络行为预测为潜在攻击行为。这些特征可能显示了异常的通信模式，如高TTL和数据包传输速率，提示潜在的恶意攻击。',
              significantFeatures: [
                {name: 'x10（生存时间，sTtl）', description: 'TTL的高值可能是攻击者通过调整TTL来隐藏攻击行为。'},
                {name: 'x9（数据传输速率，Rate）', description: '速率范围较大，表明数据传输量异常，提示了可能的攻击流量。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0678, 0.0638] AND x2 in [-0.0136, 0.4743] AND x3 in [-0.0562, 0.9967] AND x4 in [-0.018, 0.0837] AND x5 in [-0.0519, 0.0835] AND x6 in [-0.0452, 0.0907] AND x7 in [-0.0747, 0.0914] AND x8 in [-0.0222, 0.067] AND x9 in [-0.0244, 0.1032] AND x10 in [-0.0278, 0.5038] AND x11 in [-0.0215, 0.4768] AND x12 in [-0.0201, 0.0393] AND x13 in [-0.0216, 0.0641] AND x14 in [-0.0848, 0.047] AND x15 in [-0.0439, 0.0163] AND x16 in [-0.0812, 0.0681] THEN y <= 0',
              explanation: '该规则表明，当这些特征值在相应区间内时，网络行为被预测为非攻击行为。端口和数据包特征如目标端TTL（x11）和数据包数量（x5、x6）的范围较小，表明通信是正常的，没有攻击行为。',
              significantFeatures: [
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL范围较低，表明数据包的传播距离较短，属于合法的网络流量。'},
                {name: 'x9（数据传输速率，Rate）', description: '速率在正常范围，表明数据传输量稳定，没有异常流量。'},
              ],
            },
            {
              condition: 'If x1 in [-0.1058, 0.1002] AND x2 in [-0.0474, 0.6164] AND x3 in [-0.0012, 0.4232] AND x4 in [-0.025, 0.1225] AND x5 in [-0.0955, 0.0132] AND x6 in [-0.0482, 0.0737] AND x7 in [-0.0896, 0.0217] AND x8 in [-0.0648, 0.0315] AND x9 in [-0.0531, 0.1176] AND x10 in [-0.0265, 0.5745] AND x11 in [0.0062, 0.5326] AND x12 in [-0.0659, 0.0807] AND x13 in [-0.0125, 0.0558] AND x14 in [-0.0127, 0.0139] AND x15 in [-0.0859, 0.1007] AND x16 in [-0.0996, 0.06] THEN y <= 0',
              explanation: '',
              significantFeatures: [
                {name: 'x5（源数据包数量，SrcPkts）', description: '数据包数量较小，表明通信流量没有异常增大，是正常的网络活动。'},
                {name: 'x10（生存时间，sTtl）', description: 'TTL较高，表明数据包在网络中的传播时间较长，符合正常的网络流量模式。'},
              ],
            },
          ],
        },
      ],
      cloud_bupt_1: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.01, 0.01] AND x2 in [0.07, 0.54] AND x3 in [0.89, 0.91] AND x4 in [0.0, 0.0] AND x5 in [-0.01, 0.01] AND x6 in [0.0, 0.0] AND x7 in [-0.01, 0.01] AND x8 in [0.0, 0.0] AND x9 in [0.0, 0.04] AND x10 in [0.1, 0.12] AND x11 in [0.46, 0.94] AND x12 in [0.99, 1.01] AND x13 in [-0.01, 0.01] AND x14 in [-0.01, 0.01] AND x15 in [-0.01, 0.01] AND x16 in [-0.01, 0.01] THEN y > 0',
              explanation: '该规则表明，当这些特征的值落在相应的区间内时，网络行为可能为潜在攻击行为。特征显示了一些微小的波动，特别是在传输速率（x2）和目标TTL（x11）等方面，这可能表明了恶意的、伪装成正常流量的攻击活动。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '虽然端口范围较小，但在攻击行为中，该端口的波动可能是攻击者利用特定端口发起的隐蔽性攻击。'},
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL范围显示数据包可能经历了多个跳数，提示了可能存在的远程攻击。'},
              ],
            },
            {
              condition: 'If x1 in [-0.01, 0.01] AND x2 in [0.61, 0.99] AND x3 in [0.89, 0.91] AND x4 in [0.0, 0.0] AND x5 in [-0.01, 0.01] AND x6 in [0.0, 0.0] AND x7 in [-0.01, 0.01] AND x8 in [0.0, 0.0] AND x9 in [0.0, 0.04] AND x10 in [0.1, 0.12] AND x11 in [0.02, 0.94] AND x12 in [0.99, 1.01] AND x13 in [-0.01, 0.01] AND x14 in [-0.01, 0.01] AND x15 in [-0.01, 0.01] AND x16 in [-0.01, 0.01] THEN y > 0',
              explanation: '此规则表明在特定的端口和传输速率波动范围内，网络行为被预测为潜在攻击行为。源端口（x2）的波动范围较大，可能提示攻击者通过不断变化的端口伪装攻击流量，目标端TTL的较大波动也暗示了远程攻击的可能性。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '源端口的较大范围波动提示了攻击者可能通过多个端口进行隐蔽性攻击。'},
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL值的变化显示了数据包的跳跃次数较多，这表明攻击可能是远程发起的。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.01, 0.01] AND x2 in [0.07, 0.62] AND x3 in [0.89, 0.91] AND x4 in [0.0, 0.01] AND x5 in [-0.01, 0.01] AND x6 in [0.0, 0.0] AND x7 in [-0.01, 0.01] AND x8 in [0.0, 0.0] AND x9 in [0.0, 0.04] AND x10 in [0.1, 0.12] AND x11 in [0.32, 0.94] AND x12 in [0.99, 1.01] AND x13 in [-0.01, 0.01] AND x14 in [-0.01, 0.01] AND x15 in [-0.01, 0.01] AND x16 in [-0.01, 0.01] THEN y <= 0',
              explanation: '该规则显示，当这些特征值落在给定范围时，网络行为被预测为非攻击行为。端口和TTL的波动处于较为稳定的范围，表明此类网络活动是正常的，不存在恶意攻击流量的迹象。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '端口波动范围较小，表明此类网络流量相对稳定，符合合法通信的特征。'},
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL范围相对较低，显示了较少的数据包跳数，表明此通信属于普通的网络行为。'},
              ],
            },
            {
              condition: 'If x1 in [-0.01, 0.01] AND x2 in [0.09, 0.96] AND x3 in [0.89, 0.91] AND x4 in [0.0, 0.01] AND x5 in [-0.01, 0.01] AND x6 in [0.0, 0.0] AND x7 in [-0.01, 0.01] AND x8 in [0.0, 0.0] AND x9 in [0.0, 0.04] AND x10 in [0.1, 0.12] AND x11 in [0.47, 0.94] AND x12 in [0.99, 1.01] AND x13 in [-0.01, 0.01] AND x14 in [-0.01, 0.01] AND x15 in [-0.01, 0.01] AND x16 in [-0.01, 0.01] THEN y <= 0',
              explanation: '此规则表明当源端口和TTL值稳定时，网络行为被预测为非攻击行为。虽然源端口的波动较大，但其他特征如传输速率（x9）和TTL值均显示了合法网络通信的特征。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '源端口波动范围较大，但仍在正常的通信范围内，表明此流量是合法的。'},
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL值保持在正常的范围内，说明数据包的传输是合法的，未显示出异常跳数的特征。'},
              ],
            },
          ],
        },
      ],
      cloud_baseline_1: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0278, 0.0956] AND x2 in [-0.0569, 0.7809] AND x3 in [0.2432, 0.9522] AND x4 in [0.1837, 1.0138] AND x5 in [-0.0706, 0.1924] AND x6 in [-0.0742, 0.2835] AND x7 in [-0.029, 0.2018] AND x8 in [-0.0106, 1.011] AND x9 in [-0.0229, 0.1051] AND x10 in [0.8487, 1.0809] AND x11 in [-0.0752, 1.033] AND x12 in [-0.0938, 0.0795] AND x13 in [-0.0968, 0.3362] AND x14 in [-0.0808, 0.6766] AND x15 in [-0.089, 0.7152] AND x16 in [-0.0268, 0.3617] THEN y > 0',
              explanation: '这一规则显示，尽管数据传输速率和生存时间（TTL）等特征处于相对较高的区间，仍有可能存在潜在攻击行为。攻击者可能利用较长的生存时间和端口特征组合，进行隐蔽的恶意活动。',
              significantFeatures: [
                {name: 'x10（数据包的生存时间，sTtl）', description: '生存时间在[0.8487, 1.0809]范围内，显示数据包在网络中存在的时间较长，这可能是攻击者调节包头信息以混淆来源，逃避检测。'},
                {name: 'x3（目标端口，Dport）', description: '目标端口范围为[0.2432, 0.9522]，表明目标设备可能使用特定端口接受数据，这些端口可能是攻击者选择的目标，尤其是在某些服务端口上进行攻击或试探。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0606, 0.0323] AND x2 in [0.0693, 0.6437] AND x3 in [0.2834, 0.9635] AND x4 in [0.1037, 1.059] AND x5 in [-0.0131, 0.0163] AND x6 in [-0.0473, 0.0933] AND x7 in [-0.0243, 0.0639] AND x8 in [-0.0291, 0.0999] AND x9 in [-0.0416, 0.0482] AND x10 in [0.0431, 0.3252] AND x11 in [0.026, 0.2036] AND x12 in [-0.0192, 0.0254] AND x13 in [-0.0672, 1.0646] AND x14 in [-0.088, 0.4174] AND x15 in [-0.0473, 0.0343] AND x16 in [-0.0571, 0.4796] THEN y > 0',
              explanation: '该规则表明，当部分特征值略有变动但数据包传输量较低时，仍可能存在攻击行为。某些特征表明攻击者可能采用持续性低强度的探测方式，避免引起过多注意。',
              significantFeatures: [
                {name: 'x3（目标端口，Dport）', description: '目标端口在[0.2834, 0.9635]范围内，表明目标设备可能接收到更多数据包，且端口特征提示攻击者可能通过特定端口进行攻击。'},
                {name: 'x10（数据包的生存时间，sTtl）', description: 'sTtl范围较低（[0.0431, 0.3252]），说明攻击者可能故意调整数据包生存时间，发送较短寿命的数据包以尝试不同的攻击方式。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0583, 0.0474] AND x2 in [0.4132, 1.0651] AND x3 in [0.041, 0.9337] AND x4 in [-0.0022, 1.0879] AND x5 in [-0.0166, 0.0908] AND x6 in [-0.0651, 0.0317] AND x7 in [-0.0114, 0.0133] AND x8 in [-0.0931, 0.0485] AND x9 in [-0.0343, 0.0423] AND x10 in [0.8468, 1.0708] AND x11 in [0.0239, 0.1736] AND x12 in [-0.0309, 0.0772] AND x13 in [-0.0215, 0.2781] AND x14 in [-0.0302, 0.5758] AND x15 in [-0.0413, 0.4974] AND x16 in [-0.0158, 0.7026] THEN y <= 0',
              explanation: '此规则显示特征值主要集中在中低范围，表明网络行为正常，未显示出异常数据包传输或端口特征，推测为非攻击行为。',
              significantFeatures: [
                {name: 'x2（源端口，Sport）', description: '源端口在[0.4132, 1.0651]范围内，表明源设备可能通过特定范围的端口进行正常数据传输，这个范围通常与合法流量相关。'},
                {name: 'x10（数据包的生存时间，sTtl）', description: 'sTtl值在较高范围内（[0.8468, 1.0708]），显示包在网络中的生存时间较长，符合正常通信的特征。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0487, 0.0487] AND x2 in [-0.0452, 0.6924] AND x3 in [0.2894, 1.0465] AND x4 in [-0.0837, 0.5554] AND x5 in [-0.0504, 0.1004] AND x6 in [-0.0182, 0.064] AND x7 in [-0.0328, 0.0164] AND x8 in [-0.0502, 0.2365] AND x9 in [-0.0713, 0.4525] AND x10 in [0.9332, 1.0767] AND x11 in [-0.0723, 1.0529] AND x12 in [-0.0565, 0.0668] AND x13 in [-0.0647, 0.3536] AND x14 in [-0.0868, 0.5548] AND x15 in [-0.076, 0.4978] AND x16 in [-0.054, 0.3721] THEN y <= 0',
              explanation: '',
              significantFeatures: [
                {name: 'x4（持续时间，Dur）', description: '持续时间的区间较短（[-0.0837, 0.5554]），表明通信时间较短，符合普通的非攻击行为特征。'},
                {name: 'x9（传输速率，Rate）', description: '速率范围较宽（[-0.0713, 0.4525]），表明速率的变化并没有出现异常波动，符合正常的网络通信特征。'},
              ],
            },
          ],
        },
      ],
      mix_1: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0278, 0.0956] AND x2 in [0.2464, 1.0965] AND x3 in [-0.0872, 0.5733] AND x4 in [-0.0287, 0.6747] AND x5 in [-0.0708, 0.115] AND x6 in [-0.0742, 0.0622] AND x7 in [-0.029, 0.1484] AND x8 in [-0.0106, 0.0464] AND x9 in [-0.0229, 0.0997] AND x10 in [-0.0993, 0.5159] AND x11 in [-0.0771, 1.0521] AND x12 in [-0.0937, 0.1105] AND x13 in [-0.0968, 0.086] AND x14 in [-0.0808, 0.0588] AND x15 in [-0.089, 0.0933] AND x16 in [-0.0268, 0.1176] THEN y > 0',
              explanation: '此规则表明，当这些特征值位于特定范围时，预测网络行为为潜在攻击行为。特征如目标端TTL（x11）和数据传输速率（x9）波动较大，表明网络活动可能存在异常，提示攻击行为的可能性。',
              significantFeatures: [
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL的较高值表明数据包在网络中传播较长时间，可能与攻击行为相关。'},
                {name: 'x9（数据传输速率，Rate）', description: '传输速率的波动显示出网络流量的不规律性，可能暗示攻击者通过改变流量伪装攻击行为。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0606, 0.0323] AND x2 in [-0.0152, 0.9864] AND x3 in [0.4656, 1.0991] AND x4 in [-0.0614, 0.8449] AND x5 in [-0.0131, 0.3457] AND x6 in [-0.0473, 0.3006] AND x7 in [-0.0243, 0.1579] AND x8 in [-0.0291, 0.3131] AND x9 in [-0.0416, 0.1218] AND x10 in [-0.0194, 0.4998] AND x11 in [-0.0754, 0.4682] AND x12 in [-0.0192, 0.1352] AND x13 in [-0.075, 0.0905] AND x14 in [-0.0881, 0.1485] AND x15 in [-0.0473, 0.0984] AND x16 in [-0.0571, 0.3931] THEN y > 0',
              explanation: '该规则表明，当特征如源端口（x2）和目标端口（x3）波动较大时，网络行为可能为潜在攻击行为。特别是数据包的TTL和传输速率的波动范围较大，表明攻击者可能通过调整传输速率和TTL进行隐蔽攻击。',
              significantFeatures: [
                {name: 'x3（目标端口，Dport）', description: '目标端口的高波动性提示了可能的端口扫描或多端口攻击。'},
                {name: 'x10（生存时间，sTtl）', description: 'TTL值的波动表明数据包可能通过调整TTL值绕过防御机制，进行潜在攻击。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0583, 0.0474] AND x2 in [0.215, 1.0645] AND x3 in [0.1486, 1.0669] AND x4 in [-0.024, 0.497] AND x5 in [-0.0169, 0.2023] AND x6 in [-0.0651, 0.1051] AND x7 in [-0.0114, 0.0583] AND x8 in [-0.0932, 0.1004] AND x9 in [-0.0343, 0.0651] AND x10 in [-0.0803, 0.5058] AND x11 in [-0.0113, 0.4964] AND x12 in [-0.0281, 0.1086] AND x13 in [-0.0217, 0.0279] AND x14 in [-0.0302, 0.0213] AND x15 in [-0.0413, 0.08] AND x16 in [-0.0158, 0.0572] THEN y <= 0',
              explanation: '此规则显示，当目标端口（x3）和数据包生存时间（x10）在一定范围内时，网络行为被预测为非攻击行为。这些特征的稳定波动表明通信属于合法流量，没有显现出恶意行为。',
              significantFeatures: [
                {name: 'x3（目标端口，Dport）', description: '目标端口的波动处于较低范围，表明通信是合法的，没有异常的端口扫描行为。'},
                {name: 'x10（生存时间，sTtl）', description: 'TTL的稳定范围显示了数据包的正常传播路径，提示通信没有攻击行为。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0487, 0.0487] AND x2 in [-0.0452, 1.0364] AND x3 in [-0.0631, 0.487] AND x4 in [-0.0837, 0.54] AND x5 in [-0.0504, 0.1546] AND x6 in [-0.0182, 0.0472] AND x7 in [-0.0328, 0.0632] AND x8 in [-0.0502, 0.1084] AND x9 in [-0.0713, 0.0438] AND x10 in [-0.0147, 0.5117] AND x11 in [-0.0694, 1.0815] AND x12 in [-0.0564, 0.1561] AND x13 in [-0.0647, 0.1034] AND x14 in [-0.0868, 0.1043] AND x15 in [-0.076, 0.0427] AND x16 in [-0.054, 0.1323] THEN y <= 0',
              explanation: '该规则显示，当传输速率（x9）和数据包生存时间（x10）在低波动范围内时，网络行为为非攻击行为。特征如数据包的TTL和数据包数量的稳定性表明通信是合法的',
              significantFeatures: [
                {name: 'x9（数据传输速率，Rate）', description: '传输速率较低，表明通信流量没有显现出恶意流量的迹象。'},
                {name: 'x10（生存时间，sTtl）', description: 'TTL的稳定范围表明数据包的正常传播，属于合法通信。'},
              ],
            },
          ],
        },
      ],
      mix_2: [
        {
          title: '潜在攻击行为 (y > 0)',
          rules: [
            {
              condition: 'If x1 in [-0.1036, 0.0223] AND x2 in [0.0738, 0.9921] AND x3 in [0.1763, 0.2994] AND x4 in [-0.0702, 0.3451] AND x5 in [-0.088, 0.0227] AND x6 in [-0.0374, 0.0551] AND x7 in [-0.0248, 0.0633] AND x8 in [-0.0298, 0.0845] AND x9 in [-0.0357, 0.4722] AND x10 in [0.3984, 0.536] AND x11 in [-0.0332, 0.045] AND x12 in [-0.0218, 0.066] AND x13 in [-0.0415, 0.0918] AND x14 in [-0.0497, 0.0239] AND x15 in [-0.097, 0.0131] AND x16 in [-0.009, 0.2948] THEN y > 0',
              explanation: '该规则表明，当数据包的TTL（x10）和数据传输速率（x9）在较高区间时，网络行为可能为潜在攻击行为。这些特征的波动表明，攻击者可能通过调整TTL和流量伪装攻击行为。',
              significantFeatures: [
                {name: 'x9（数据传输速率，Rate）', description: '数据传输速率的较大波动可能提示攻击者通过改变流量来躲避检测。'},
                {name: 'x10（生存时间，sTtl）', description: 'TTL的较高范围表明数据包在网络中传播时间较长，可能暗示攻击者在利用长时间的网络滞留进行攻击。'},
              ],
            },
            {
              condition: 'If x1 in [-0.0576, 0.053] AND x2 in [0.5228, 1.0196] AND x3 in [0.2239, 0.3528] AND x4 in [-0.0113, 0.0189] AND x5 in [-0.0093, 0.0213] AND x6 in [-0.0983, 0.1012] AND x7 in [-0.0268, 0.0668] AND x8 in [-0.0661, 0.073] AND x9 in [0.08, 0.6179] AND x10 in [0.4171, 0.6004] AND x11 in [-0.0866, 0.0479] AND x12 in [-0.0693, 0.0972] AND x13 in [-0.0192, 0.0898] AND x14 in [-0.0719, 0.0784] AND x15 in [-0.0309, 0.0871] AND x16 in [-0.0668, 0.0589] THEN y > 0',
              explanation: '此规则预测的网络行为为潜在攻击行为。特征如数据包传输速率（x9）和TTL（x10）的波动表明攻击者可能通过不规则的传输和较长时间的通信进行恶意攻击。',
              significantFeatures: [
                {name: 'x9（数据传输速率，Rate）', description: '速率的显著波动提示了潜在的攻击流量，攻击者可能调整流量来绕过检测。'},
                {name: 'x10（生存时间，sTtl）', description: 'TTL的较高范围表示通信持续时间较长，这可能是攻击者隐藏活动的策略。'},
              ],
            },
          ],
        },
        {
          title: '非攻击行为 (y <= 0)',
          rules: [
            {
              condition: 'If x1 in [-0.0678, 0.0638] AND x2 in [-0.0074, 1.0719] AND x3 in [-0.0892, 1.0244] AND x4 in [-0.0179, 0.0609] AND x5 in [-0.0519, 0.0847] AND x6 in [-0.0452, 0.0686] AND x7 in [-0.0747, 0.0918] AND x8 in [-0.0222, 0.0517] AND x9 in [-0.0203, 0.4281] AND x10 in [0.2478, 0.4997] AND x11 in [0.9339, 1.0366] AND x12 in [-0.0201, 0.0353] AND x13 in [-0.0216, 1.0422] AND x14 in [-0.0848, 0.0463] AND x15 in [-0.0439, 0.0154] AND x16 in [-0.0812, 0.2828] THEN y <= 0',
              explanation: '该规则表明当数据包的TTL（x11）和传输速率（x9）在一定范围内时，网络行为被预测为非攻击行为。特征表明通信流量较为稳定，没有攻击迹象。',
              significantFeatures: [
                {name: 'x9（数据传输速率，Rate）', description: '数据传输速率较为稳定，表明数据传输正常，没有异常的流量波动。'},
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL的稳定范围表示数据包的正常传播，属于合法的通信流量。'},
              ],
            },
            {
              condition: 'If x1 in [-0.1058, 0.1002] AND x2 in [-0.0485, 0.4324] AND x3 in [0.2274, 0.3178] AND x4 in [-0.0249, 0.0846] AND x5 in [-0.0942, 0.0131] AND x6 in [-0.0575, 0.0601] AND x7 in [-0.088, 0.0238] AND x8 in [-0.0748, 0.026] AND x9 in [0.0944, 0.6402] AND x10 in [0.4596, 0.5882] AND x11 in [-0.0384, 0.0924] AND x12 in [-0.0659, 0.0767] AND x13 in [0.04, 0.1215] AND x14 in [-0.0127, 0.013] AND x15 in [-0.0858, 0.0998] AND x16 in [-0.0972, 0.1043] THEN y <= 0',
              explanation: '此规则预测网络行为为非攻击行为。特征如数据包的TTL（x11）和传输速率（x9）在稳定范围内，显示出正常的网络通信行为。',
              significantFeatures: [
                {name: 'x9（数据传输速率，Rate）', description: '传输速率保持在正常范围，显示出通信流量没有异常波动。'},
                {name: 'x11（目标端TTL，dTtl）', description: 'TTL值显示数据包的传播是正常的，没有表现出攻击特征。'},
              ],
            },
          ],
        },
      ],
    });

    return {dataset, explanations};
  },
};
</script>

<style scoped>
.explanation-view {
  padding: 20px;
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.explanation-card {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.rule-content {
  margin: 10px 0;
}

.significant-features {
  margin-top: 10px;
}

.significant-features h4 {
  font-size: 16px;
}

.el-list-item {
  font-size: 14px;
}
</style>
