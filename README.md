
# 📈 台股收盤價預測系統

🎯 **專案功能總覽**  
✅ 自動擷取台股清單  
✅ 更新個股歷史資料（自動補抓缺漏）  
✅ 建立線性回歸預測模型 ➜ 顯示 R² 決定係數  
✅ 匯出預測報表（`prediction_report.xlsx`）  
✅ 產生預測趨勢圖（`charts/`）  
✅ 語音輸入股票代碼（自動偵測 USB 麥克風）  
✅ 中文語音播報預測結果（使用 gTTS, Google TTS API）  
✅ GUI 操作（tkinter），附狀態顯示（跑馬燈動畫）  
✅ 支援 Raspberry Pi OS Bullseye ➜ 可用 seeed-2mic 音效卡  
✅ **Bookworm kernel 6.12.25 無法錄音，請使用 USB 麥克風**

---

## 🔧 安裝步驟

1️⃣ 安裝必要軟體  
\`\`\`bash
sudo apt update
sudo apt install python3-pip mpg321 espeak-ng alsa-utils portaudio19-dev
pip install -r requirements.txt
\`\`\`

2️⃣ 若使用 seeed-2mic（在 Raspberry Pi OS Bullseye）  
\`\`\`bash
git clone https://github.com/respeaker/seeed-voicecard.git
cd seeed-voicecard
sudo ./install.sh
sudo reboot
\`\`\`

---

## 🟩 執行方式

\`\`\`bash
python3 gui_main.py
\`\`\`

---

## 🟩 重要 Python 相依套件
\`\`\`plaintext
pandas
matplotlib
scikit-learn
joblib
requests
lxml
certifi
tk
Pillow
speechrecognition
gtts
\`\`\`

---

## 🟩 使用注意

✅ 語音輸入使用 \`speech_recognition\` ➜ 自動偵測 USB 麥克風，不需手動設定  
✅ 中文語音播報使用 \`gTTS\` ➜ 需 **網路連線**  
✅ \`mpg321\` 播放語音，若未安裝可改用 \`mplayer\`  

---

## 📸 執行畫面
> 請附上 GUI 介面截圖、圖表範例、報表範例等

---

## 🟩 硬體建議

- Raspberry Pi 4 Model B  
- Raspberry Pi OS Bullseye 64-bit  
- USB 麥克風（或 seeed-2mic）  
- 3.5mm 耳機或喇叭輸出

---

## 🟩 聲音播放測試

若無法聽到語音播報：  
1️⃣ 測試系統音效卡：  
\`\`\`bash
aplay /usr/share/sounds/alsa/Front_Center.wav
\`\`\`
2️⃣ 播放語音檔案：  
\`\`\`bash
mpg321 tts_output.mp3
\`\`\`
3️⃣ 若仍無聲音 ➜ 使用 \`sudo raspi-config\` ➜ Audio ➜ 選擇正確輸出裝置

---

## 🟩 心得

🟩 這個專案整合了資料抓取、模型預測、語音輸入與語音播報。最大的挑戰是音效卡在不同作業系統與驅動下的相容性，最終選擇 USB 麥克風作為穩定的語音輸入方式。系統執行流暢，語音播報與 GUI 整合良好，未來可拓展自動化推播或行動裝置介面。

---

## 🟩 參考來源

- Raspberry Pi 官方文件  
- seeed-voicecard GitHub  
- gTTS / speech_recognition 官方文件  
- TWSE 官網

---

## 🟩 其他

- 程式碼含完整註解、模組化結構  
- 若需要影片示範，請提供錄影畫面（含視窗 + 重要程式片段講解）

---

✨ 以上就是完整的 `README.md`，可直接放到專案目錄！
