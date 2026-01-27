import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')
excel_path = "C:/Users/10944/Desktop/dataset/珠三角9市各监测子站6种污染物浓度/2023.xlsx"
sheet_month_map = {f"Sheet{i}": f"2021-{str(i).zfill(2)}" for i in range(1, 13)}
month_season_map = {
    "01": "冬季", "02": "冬季", "03": "春季",
    "04": "春季", "05": "春季", "06": "夏季",
    "07": "夏季", "08": "夏季", "09": "秋季",
    "10": "秋季", "11": "秋季", "12": "冬季"
}

def read_and_merge_multi_sheets(excel_path, sheet_month_map, month_season_map):
    merged_df = pd.DataFrame()

    for sheet_name, date in sheet_month_map.items():
        try:
            sheet_df = pd.read_excel(excel_path, sheet_name=sheet_name)
            sheet_df["时间"] = date
            sheet_df["季节"] = month_season_map[date.split("-")[1]]
            merged_df = pd.concat([merged_df, sheet_df], ignore_index=True)
            print(f"✅ 成功读取：{sheet_name}（对应时间：{date}）")

        except Exception as e:
            print(f"❌ 读取{sheet_name}失败，原因：{str(e)}")
            return None

    merged_df.rename(columns={
        "监测子站": "监测子站名称",
        "SO2浓度月均值（μg/m3）": "SO2",
        "NO2浓度月均值（μg/m3）": "NO2",
        "O3浓度月均值（μg/m3）": "O3",
        "CO浓度月均值（mg/m3）": "CO_mg/m3",
        "PM10浓度月均值（μg/m3）": "PM10",
        "PM2.5浓度月均值（μg/m3）": "PM2.5"
    }, inplace=True)

    def extract_city(station_name):
        city_keywords = {
            "广州": "广州", "深圳": "深圳", "珠海": "珠海",
            "佛山": "佛山", "东莞": "东莞", "中山": "中山",
            "惠州": "惠州", "江门": "江门", "肇庆": "肇庆"
        }
        for keyword, city in city_keywords.items():
            if keyword in str(station_name):
                return city
        return "其他"

    merged_df["城市"] = merged_df["监测子站名称"].apply(extract_city)

    merged_df.sort_values(by=["城市", "时间", "监测子站名称"], inplace=True)
    return merged_df


def add_fields_with_minmaxscaler(df):
    df_with_fields = df.copy()

    df_with_fields["CO_μg/m3"] = df_with_fields["CO_mg/m3"] * 1000
    print(f"\n✅ CO单位转换完成：新增'CO_μg/m3'字段（原始'CO_mg/m3'保留）")

    pollutant_original_cols = ["SO2", "NO2", "O3", "CO_μg/m3", "PM10", "PM2.5"]
    print(f"✅ 待标准化的原始字段（单位均为μg/m3）：{pollutant_original_cols}")

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df_with_fields[pollutant_original_cols])

    scaled_df = pd.DataFrame(
        scaled_data,
        columns=[f"{col}_标准化" for col in pollutant_original_cols],
        index=df_with_fields.index
    )

    df_with_fields = pd.concat([df_with_fields, scaled_df], axis=1)
    print(f"✅ MinMaxScaler标准化完成：新增{len(scaled_df.columns)}个标准化字段")

    for col in pollutant_original_cols:
        rate_col_name = f"{col}_环比变化率(%)"
        df_with_fields[rate_col_name] = df_with_fields.groupby("城市")[col].pct_change() * 100
        df_with_fields[rate_col_name].fillna(0, inplace=True)

    normalized_cols = [f"{col}_标准化" for col in pollutant_original_cols]
    df_with_fields["综合污染指数"] = df_with_fields[normalized_cols].sum(axis=1)

    return df_with_fields, scaler


def save_data(df,scaler, pollutant_original_cols):
    basic_fields = ["监测子站名称", "城市", "时间", "季节"]
    original_fields = ["SO2", "NO2", "O3", "CO_mg/m3", "CO_μg/m3", "PM10", "PM2.5"]
    normalized_fields = [col for col in df.columns if "_标准化" in col]
    derived_fields = [col for col in df.columns if
                      any(keyword in col for keyword in ["环比变化率", "污染等级", "综合污染指数"])]

    export_fields = basic_fields + original_fields + normalized_fields + derived_fields

    output_path = "六种污染物浓度_2023预处理后.csv"
    df[export_fields].to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n✅ 数据保存成功：{output_path}")


if __name__ == "__main__":
    merged_data = read_and_merge_multi_sheets(excel_path, sheet_month_map, month_season_map)
    if merged_data is None:
        print("\n❌ 多表合并失败，终止数据处理")
        exit()

    final_data, scaler = add_fields_with_minmaxscaler(merged_data)

    pollutant_original_cols = ["SO2", "NO2", "O3", "CO_μg/m3", "PM10", "PM2.5"]
    output_file = save_data(final_data, scaler, pollutant_original_cols)
