# workflow.py
# -*- coding: utf-8 -*-
from .twse_stock_info import twse_stock_info
from .update_module import update_stock_data_incrementally, check_fallback_csvs
from .predict_and_export import (
    predict_multiple_stocks,
    plot_predictions_ten,
    plot_predictions_all,
    export_prediction_summary,
    train_and_predict,
    build_features
)
import pandas as pd
import os
from stock.setup_chinese_font import setup_chinese_font

# 將完整預測輸出流程整合成一個函式執行
def update_and_predict_workflow(stock_code, verify_ssl=False):
    # 🟩 檢查 twse_stock.csv 是否存在
    if os.path.exists("twse_stock.csv"):
        stock_info_df = twse_stock_info(use_cache=True, verify_ssl=verify_ssl)
    else:
        stock_info_df = twse_stock_info(use_cache=False, verify_ssl=verify_ssl)

    stock_df = stock_info_df[stock_info_df["有價證券代號代碼"] == stock_code].copy()
    stock_df["上市日"] = pd.to_datetime(stock_df["上市日"], errors="coerce")
    if stock_df.empty:
        raise ValueError(f"❌ 找不到股票代碼：{stock_code}")

    stock_name = stock_df.iloc[0]["有價證券代號名稱"]
    listed_date = stock_df.iloc[0]["上市日"]

    # 🟩 更新歷史資料（增量更新）
    update_stock_data_incrementally(
        stock_code=stock_code,
        stock_name=stock_name,
        listed_date=listed_date,
        verify_ssl=verify_ssl
    )

    # 🟩 確認 fallback CSV
    valid_codes, summary = check_fallback_csvs([stock_code])
    if not valid_codes:
        raise ValueError("❌ fallback CSV 無效或無資料")

    # 🟩 載入 fallback 檔案，並做特徵工程
    df = pd.read_csv(f"fallback_{stock_code}.csv", parse_dates=["日期"])
    df_feat = build_features(df)  # 🔧 特徵工程

    # 🟩 執行預測（取得 df_result & 模型 R²）
    result_df, model_r2 = train_and_predict(df_feat, stock_code)
    if result_df.empty:
        raise ValueError("⚠️ 預測失敗或無資料")

    # 🟩 新增股票代號欄位（避免 GUI 出錯）
    result_df["股票代號"] = stock_code
    result_df["股票代碼"] = stock_code

    # 🟩 將模型 R² 直接作為信心度（整體模型可信度）
    result_df["信心度"] = model_r2

    # 🟩 產出圖表（自動建立 charts 目錄）
    prop = setup_chinese_font()
    plot_predictions_ten(result_df, output_dir="charts", prop=prop)
    plot_predictions_all(result_df, output_dir="charts", prop=prop)

    # 🟩 匯出預測摘要報表
    export_prediction_summary(result_df, output_path="prediction_report.xlsx")

    return result_df, stock_name, model_r2
