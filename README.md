# 双元创新
通过CSMAR数据提取双元创新数据

## 定义：
双元创新分为探索式创新和利用式创新，度量双元创新的方式如下：若一项专利 i 的 IPC 分类号前*4*位在前**3**年(有的学者认为应该采用5年区间)曾出现过至少1 次，则该专利为利用式创新；否则为探索式创新。需要强调的是，大多数专利的 IPC 分类号不止一个，本文在处理过程中进行严格筛选，即当一项专利的所有 IPC 分类号在之前 3 年均未出现过时将其划分为探索式创新，否则均为利用式创新。

## 数据来源：
基于CSMAR中的上市公司及其子公司授权专利被引用信息表进行的双元创新的数据进行提取，其中包含了企业每年申请的专利，可以通过此数据来计算双元创新
