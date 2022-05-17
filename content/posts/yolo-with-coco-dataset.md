---
date: 2025-05-18T23:28:07+08:00
updated: 2025-06-05T22:13:08+08:00
title: 使用 coco 2017 dataset 做 yolo11 訓練
category: machine-learning
tags:
  - machine-learning
  - yolo
  - coco
type: note
post: true
---

## 使用 COCO 2017 Dataset 訓練 YOLO11

<!--more-->

### 專案流程總覽

[github: yolo-with-coco-dataset](https://github.com/chiehting/yolo-with-coco-dataset)

1. **資料集準備**
    
    - 從 COCO 官方網站下載 2017 年版的訓練集、驗證集圖片及標註檔案。
    - 將資料分別放在 `coco2017/annotations`、`coco2017/train2017`、`coco2017/val2017` 目錄下。
2. **資料格式轉換**
    
    - 使用 `1_convert_to_yolo11.py` 進行 COCO → YOLO 格式轉換，並可過濾所需的類別（categories）。
    - COCO bbox 格式為 `[x_min, y_min, width, height]`，需轉成 YOLO 格式 `[class_id, x_center, y_center, width, height]`，且所有值需歸一化到 [0, 1]。
    - 需自行設計類別對應（category mapping）。
3. **訓練流程**
    
    - 執行 `2_train.py` 進行模型訓練。
4. **推論預測**
    
    - 執行 `3_predict.py` 進行圖片預測。

### 1. 準備資料集

這是最關鍵的步驟之一：

- **收集圖片**：收集包含您想要偵測物件的圖片
- **標註資料**：為每張圖片中的目標物件創建標註（邊界框和類別）
- **資料集分割**：將資料集分為訓練集、驗證集和測試集（通常比例為 70%/20%/10%）

YOLO 格式

```txt
<class_id> <x_center> <y_center> <width> <height>
```

COCO 的邊界框格式 `[x_min, y_min, width, height]` 轉換為 YOLO 的 `[x_center, y_center, width, height]` 格式

```python
# COCO 格式邊界框
x_min = 433.61
y_min = 213.88
width = 39.67
height = 112.56
category_id = 16

# 圖片尺寸
image_width = 640
image_height = 480

# 計算 YOLO 格式的中心點座標
x_center = (x_min + width/2) / image_width
y_center = (y_min + height/2) / image_height

# 計算 YOLO 格式的寬高（歸一化）
yolo_width = width / image_width
yolo_height = height / image_height

# 假設我們將 COCO 類別 ID 16 映射到 YOLO 類別 ID 5
yolo_class_id = 5  # 這取決於您的類別映射

# 生成 YOLO 格式的字串
yolo_format = f"{yolo_class_id} {x_center:.6f} {y_center:.6f} {yolo_width:.6f} {yolo_height:.6f}"
print(yolo_format)
```