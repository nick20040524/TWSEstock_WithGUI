
# 🇹🇼 台股收盤價預測系統（整合語音輸入輸出 + 跑馬燈動畫版，gTTS 中文語音播報）

🎯 **專案功能總覽**  
✅ 自動擷取 TWSE 上市股票清單  
✅ 更新個股歷史資料（自動補抓缺漏）  
✅ 建立線性回歸模型 ➜ 顯示 R² 決定係數  
✅ 產生預測圖表（`charts/` 資料夾）  
✅ 匯出預測報表（`prediction_report.xlsx`）  
✅ 語音輸入股票代碼（自動偵測 USB 麥克風）  
✅ 中文語音播報預測結果（使用 gTTS，自然發音）  
✅ 狀態即時顯示（跑馬燈動畫顯示「更新中…」）  
✅ 支援 SSL 憑證繞過與 fallback 快取（避免網路錯誤）  
✅ **支援 Raspberry Pi OS Bullseye 上 seeed-2mic 音效卡錄音**  
✅ **Bookworm kernel 6.12.25 上 seeed-2mic 錄音不可用，建議改用 USB 麥克風**

---

## 🔧 安裝與環境配置

1️⃣ 安裝音效播放工具（mpg321）與錄音工具  
```bash
sudo apt update
sudo apt install mpg321 espeak-ng alsa-utils portaudio19-dev
```

2️⃣ 安裝 Python 依賴套件  
```bash
pip install -r requirements.txt
```

---

## ▶️ 執行主程式

啟動（若有虛擬環境可先啟動）：  
```bash
python3 gui_main.py
```

若想隱藏 ALSA / Jack server 等底層雜訊訊息：  
```bash
python3 gui_main.py 2>/dev/null
```

---

## 🎤 語音輸入 + 中文語音播報

- 程式會自動偵測 USB 麥克風或其他可用裝置，無需手動設定 `device_index`  
- 中文語音播報改用 **gTTS（Google TTS API）** ➜ 自然流暢，需要 **網路連線**

---

## 📈 使用方式

1️⃣ 啟動 GUI，選擇股票代碼（或使用語音輸入）  
2️⃣ 點擊「更新資料並預測」  
3️⃣ 系統將：  
   - 更新歷史股價資料  
   - 訓練模型並預測明日收盤價  
   - 顯示圖表、輸出 `prediction_report.xlsx`  
   - 自然語音播報預測結果（中文）  
   - 跑馬燈動畫顯示「更新中…」等狀態  
4️⃣ 下方狀態欄與跑馬燈動畫會即時顯示系統目前狀態

---

## 🟢 音效卡錄音支援說明

✅ **Raspberry Pi OS Bullseye** ➜ 可用 seeed-2mic（安裝 seeed-voicecard 驅動）  
✅ **USB 麥克風** ➜ 標準 UAC 裝置，免驅動，建議首選  
❌ **Bookworm kernel 6.12.25** ➜ seeed-2mic 音效卡錄音不可用，請改用 USB 麥克風

---

## 🟩 參考來源

- Raspberry Pi 官方文件  
- seeed-voicecard GitHub  
- gTTS / speech_recognition 官方文件  
- TWSE 官網

---

✨ 以上即為完整專案文件，歡迎隨時提出 issue、pull request，或需求擴充！
