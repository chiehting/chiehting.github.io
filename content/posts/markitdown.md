---
date: 2025-05-14T00:12:11+08:00
updated: 2025-11-10T12:18:30+08:00
title: Microsoft MarkItDown 工具摘要與使用範例
category: software
tags:
  - software
  - markitdown
type: note
post: true
---

MarkItDown 是由微軟開發的 Python 工具，專門用於將各種文件格式和辦公文檔轉換為 Markdown 格式。這個工具在發布後迅速獲得了廣泛關注。

<!--more-->

## Github

https://github.com/microsoft/markitdown


## 格式轉換

MarkItDown 支援多種文件格式的轉換，包括：
    - PDF
    - PowerPoint
    - Word
    - Excel
    - Images (EXIF metadata and OCR)
    - Audio (EXIF metadata and speech transcription)
    - HTML
    - Text-based formats (CSV, JSON, XML)
    - ZIP files (iterates over contents)
    - Youtube URLs
    - EPubs
    - ... and more!

## 使用範例

### 安裝方法

```bash
pip install markitdown[all]
```

### 使用命令轉換格式

```bash
# 基本轉換
markitdown 1_PDFsam_pool_charlie.pdf -o 1_PDFsam_pool_charlie.md
```

### MarkItDown 將 YouTube 轉換成 Markdown 的範例

沒什麼作用，因為只是提取了字幕文本，但沒任何 Markdown 語法元素，就結果來說只是個純文本。

```python
from markitdown import MarkItDown
import youtube_transcript_api
import os

def youtube_to_markdown(video_id, languages=['en','zh-Hant']):
    # 使用 youtube_transcript_api 獲取字幕
    try:
        transcript = youtube_transcript_api.YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        
        # 將字幕轉換為純文本
        transcript_text = ""
        for line in transcript:
            transcript_text += line['text'] + "\n"
        
        # 保存為臨時文本文件
        temp_file = "temp_transcript.txt"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(transcript_text)
        
        # 使用 MarkItDown 轉換為 Markdown
        md = MarkItDown()
        result = md.convert(temp_file)
        
        # 清理臨時文件
        os.remove(temp_file)
        
        # 從結果對象中提取文本內容
        # 嘗試可能的屬性或方法
        if hasattr(result, 'text'):
            return result.text
        elif hasattr(result, 'content'):
            return result.content
        elif hasattr(result, 'get_text'):
            return result.get_text()
        elif hasattr(result, 'get_content'):
            return result.get_content()
        else:
            # 如果以上都不存在，則嘗試直接將結果轉換為字符串
            return str(result)
    except Exception as e:
        return f"轉換失敗: {str(e)}"

# 使用示例，如果影片本身沒字幕，則會下載失敗
video_id = "TQDHGswF67Q"  # YouTube ID
markdown = youtube_to_markdown(video_id)
print(type(markdown))
print(markdown)

# 保存為 Markdown 文件
with open(f"{video_id}.md", "w", encoding="utf-8") as f:
    f.write(markdown)

```