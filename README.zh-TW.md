# AI 資料分析助理

[English](README.md) | **繁體中文**

可部署的 Streamlit 分析網站，提供營收、成本、毛利與毛利率 KPI、產品／地區比較、每月趨勢、中英文關鍵字提問、篩選及 CSV 下載。不需要 API 金鑰或資料庫帳密。

## 本機執行

建議 Python 3.12，與 CI、部署設定一致。

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell 改用：.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

網站啟動時自動在記憶體產生 1,800 筆 2025 年合成資料，固定 seed=7，不必事先執行腳本或保存資料檔。若需要額外匯出完整 CSV，可執行 `python src/generate_sales.py`，輸出至 `data/sales.csv`。

## 部署至 Streamlit Community Cloud

1. 開啟 https://share.streamlit.io/ ，登入並連接 GitHub。
2. 選擇 Create app，Repository 填入 `stream6650-arch/ai-data-analytics-assistant`。
3. Branch 選擇包含此版本檔案的分支；合併 PR 後可選 `main`。
4. Main file path 填入 `app.py`，Advanced settings 選 Python **3.12**。
5. 不需要設定 Secrets，按 Deploy，完成後即可分享網站網址。

此專案需要 Python 伺服器，不能直接使用 GitHub Pages 執行。服務配額、可用性與費用以平台當時方案為準。

## 使用方式

左側可篩選產品、地區與月份。輸入「哪個產品營收最高？」、「各地區營收」、「每月銷售趨勢」、「哪個產品毛利最高？」；也支援 README 英文範例。辨識不到問題時會提示支援範圍，並提供手動選擇指標與維度。

- 營收 = 數量 × 單價。
- 成本 = 數量 × 單位成本。
- 毛利 = 營收 − 成本。
- 毛利率 = 總毛利 ÷ 總營收。

所有 KPI、表格、圖表與下載內容都套用篩選。金額為示範貨幣單位。這是關鍵字規則教學版，未串接 LLM，不支援任意 SQL、預測或客戶分析。

## 驗證與檔案

執行 `python -m unittest discover -s tests -v` 可驗證計算、問題辨識、月份排序與 Streamlit 操作。GitHub Actions 也會在 push／PR 自動測試。

`app.py` 是網站入口；`src/generate_sales.py` 產生資料；`src/analytics.py` 定義指標與分析；`.streamlit/config.toml` 設定網站主題。

原文件的歷史圖表數字缺少資料生成程式可供核對，因此此版本移除靜態數字，以隨附程式即時計算結果為準。所有資料都是合成資料，不含企業內部資訊或私人連線。

學習延伸：Deterministic Routing → Semantic Layer → DuckDB → Text-to-SQL → SQL Validation → Execution → Audit。
