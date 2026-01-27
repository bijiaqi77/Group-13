import pandas as pd
import warnings
warnings.filterwarnings('ignore')
excel_path = "C:/Users/10944/Desktop/dataset/珠三角9市2021-2024年AQI达标率、PM10、PM2.5浓度/2024.xlsx"
sheet_month_map = {f"Sheet{i}": f"2021-{str(i).zfill(2)}" for i in range(1, 7)}
month_season_map = {
    "01": "冬季", "02": "冬季", "03": "春季",
    "04": "春季", "05": "春季", "06": "夏季",
}

def read_and_merge_excel(excel_path, sheet_month_map):
    merged_df = pd.DataFrame()

    for sheet_name, date in sheet_month_map.items():
        try:
            sheet_df = pd.read_excel(excel_path, sheet_name=sheet_name)

            sheet_df["时间"] = date
            sheet_df["季节"] = month_season_map[date.split("-")[1]]

            merged_df = pd.concat([merged_df, sheet_df], ignore_index=True)
        except Exception as e:
            print(f"错误：读取{sheet_name}（{date}）失败，原因：{str(e)}")
            return None

    merged_df.rename(columns={
        "可吸入颗粒物（PM10）月平均浓度(微克/立方米)": "PM10",
        "细颗粒物（PM2.5）月平均浓度（微克/立方米）": "PM2.5",
        "AQI达标率": "AQI达标率"
    }, inplace=True)

    merged_df.sort_values(by=["城市", "时间"], inplace=True)
    return merged_df


def add_visual_fields(df):
    df_with_fields = df.copy()
    df_with_fields["AQI达标率(小数)"] = df_with_fields["AQI达标率"]
    for col in ["PM10", "PM2.5"]:
        df_with_fields[f"{col}环比变化率(%)"] = df_with_fields.groupby("城市")[col].pct_change() * 100
        df_with_fields[f"{col}环比变化率(%)"].fillna(0, inplace=True)
    df_with_fields["AQI达标率环比变化率(%)"] = df_with_fields.groupby("城市")["AQI达标率"].pct_change() * 100
    df_with_fields["AQI达标率环比变化率(%)"].fillna(0, inplace=True)

    def get_pollution_level(aqi_rate):
        if aqi_rate >= 0.95:
            return "优秀"
        elif aqi_rate >= 0.85:
            return "良好"
        elif aqi_rate >= 0.70:
            return "一般"
        else:
            return "较差"

    df_with_fields["污染等级"] = df_with_fields["AQI达标率"].apply(get_pollution_level)

    return df_with_fields

def save_data(df):
    output_path = "珠三角9市大气污染数据_2024预处理后.csv"
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"✅ 保存成功：{output_path}")
    print(f"数据规模：{df.shape[0]}行 × {df.shape[1]}列")

if __name__ == "__main__":
    merged_data = read_and_merge_excel(excel_path, sheet_month_map)
    if merged_data is not None:
        final_data = add_visual_fields(merged_data)
        save_data(final_data)
    else:
        print("❌ 数据处理失败")

