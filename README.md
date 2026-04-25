# 🌊 sea-bloom-monitor 近海藻华智能监测系统
> 基于FTS-Transformer的近海生态灾害智能预警平台，为海洋生态安全提供科学支撑

---

## 📌 项目简介
近海藻华频发严重威胁海洋生态安全，传统监测方式存在数据孤岛、预警滞后等痛点。本项目依托多源海洋大数据，构建基于FTS-Transformer的近海藻华智能监测与预测系统，实现叶绿素a浓度高精度预测与分级预警，为近海生态治理提供低成本、可落地的智能化解决方案。

- ✅ 模型预测R²达0.9746，RMSE低至0.3137
- ✅ 支持多源数据融合、时序特征增强
- ✅ 提供数据可视化与趋势预测功能

---

## 🛠️ 环境安装
```bash
# 克隆仓库
git clone https://github.com/Chen-cqy/sea-bloom-monitor.git
cd sea-bloom-monitor

# 安装依赖
pip install -r requirements.txt# sea-bloom-monitor

🚀 使用说明
运行数据预处理脚本：python data_preprocess.py
启动模型训练：python train_model.py
生成预测结果与可视化：python predict_visualize.py
📄 开源说明
项目基于 Python 与 PyTorch 开发，使用pandas/numpy等通用开源库
核心 FTS-Transformer 模型为团队独立设计实现
本项目采用 MIT 开源协议，详见 LICENSE
