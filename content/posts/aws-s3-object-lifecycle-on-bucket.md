---
date: 2023-09-11T16:35:02+08:00
updated: 2025-02-27T08:46:36+08:00
title: Managing the lifecycle of the objects on AWS S3
category: cloud
tags:
  - cloud
  - aws
  - s3
type: note
post: true
---

如何管理 S3 上的物件生命週期？

在做 S3 物件的管理時，若使用 HTTP request 做操作，會造成成本增加。所以若是物件有**轉換**或是**過期**的操作時，就可以考慮使用 S3 生命週期來做管理。

<!--more-->

### Managing your storage lifecycle

為管理您的物件，使其整個生命週期以更符合成本效益的方式儲存，請配置 _Amazon S3 生命週期_。_S3 生命週期組態_是一組定義 Amazon S3 動作的規則，適用於一組物件。有兩種類型的動作：

- **轉換動作** – 定義物件何時轉換成另一個儲存類別。例如，您可以選擇在建立物件後的 30 天，將物件轉換為 S3 標準 – IA 儲存類別，或者在建立物件一年後，將物件封存到 S3 Glacier Flexible Retrieval 儲存類別。如需詳細資訊，請參閱 [使用 Amazon S3 儲存體方案](https://docs.aws.amazon.com/zh_tw/AmazonS3/latest/userguide/storage-class-intro.html)。
    
    這些是與生命週期轉換請求相關聯的成本。如需定價資訊，請參閱 [Amazon S3 定價](https://aws.amazon.com/s3/pricing/)。
    
- **過期動作** – 這些動作會定義物件何時過期。Amazon S3 會為您刪除已過期的物件。
    
    生命週期過期成本，取決於您選擇物件的過期時間。如需詳細資訊，請參閱 [即將到期的物件](https://docs.aws.amazon.com/zh_tw/AmazonS3/latest/userguide/lifecycle-expire-general-considerations.html)。

為已妥善定義生命週期的物件，定義 S3 生命週期組態規則。例如：

- 如果您將定期日誌上傳到儲存貯體，您的應用程式可能需要使用它們一週或一個月。之後，您可能會想刪除它們。
- 某些文件在一段有限的期間內會經常受到存取。而在該期間之後，存取它們的頻率很低。在某些時候，您可能不需要即時存取它們，但您的組織或法規可能要求您將其封存一段特定時間。之後，您可以刪除它們。
- 您可能會將某些類型的資料上傳到 Amazon S3，主要為目的檔案用。例如，您可以使用它來封存數位媒體、財務及醫療保健記錄、原始基因序列資料、長期資料庫備份，以及為遵守法規而所必須保留的資料。

使用 S3 生命週期組態規則，您可以指示 Amazon S3 將物件轉換為較便宜的儲存體類別、封存或刪除物件。

### 指定篩選條件

每個 S3 生命週期規則都包含篩選條件，您可用於找出儲存貯體中將套用 S3 生命週期規則的一組物件。下列 S3 生命週期組態說明如何指定篩選條件的範例。

- 在此 S3 生命週期組態規則中，https://docs.aws.amazon.com/zh_tw/AmazonS3/latest/userguide/object-keys.html
   - 篩選條件指定了一個金鑰字首 (key prefix) (`tax/`)。因此，規則將會套用至其金鑰名稱字首為 `tax/` 的物件，例如 `tax/doc1.txt` 與 `tax/doc2.txt`。
   - 若篩選條件指定了一個金鑰字首`1d`，**不會**套用規則至物件 `1d-doc1.txt`。

- 您可以僅根據標籤來篩選物件。
