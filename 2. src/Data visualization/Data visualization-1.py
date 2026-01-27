import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans', 'Arial Unicode MS', 'SimSun']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['font.family'] = 'sans-serif'

# 设置图形样式
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

print("大气污染可视化分析")

def plot_annual_trend_city_level():
    """绘制城市级别数据的年际变化趋势 - 单独输出每个子图"""
    # 读取所有年份的数据
    years = [2021, 2022, 2023, 2024]
    city_data_list = []
    
    for year in years:
        try:
            df = pd.read_csv(f"珠三角9市大气污染数据_{year}预处理后.csv", encoding='utf-8-sig')
            df['年份'] = year
            
            # 确保每个文件都有季节列
            if '季节' not in df.columns:
                print(f"在{year}年数据中重新生成季节列...")
                df['月份'] = df['时间'].str.split('-').str[1].astype(int)
                
                def get_season(month):
                    if month in [12, 1, 2]:
                        return '冬季'
                    elif month in [3, 4, 5]:
                        return '春季'
                    elif month in [6, 7, 8]:
                        return '夏季'
                    else:
                        return '秋季'
                
                df['季节'] = df['月份'].apply(get_season)
            
            city_data_list.append(df)
            print(f"成功读取{year}年数据，共{len(df)}行")
            
        except FileNotFoundError:
            print(f"警告：{year}年数据文件未找到")
            continue
        except Exception as e:
            print(f"读取{year}年数据时出错：{e}")
            continue
    
    if not city_data_list:
        print("错误：没有找到任何数据文件")
        return None
    
    # 合并所有数据
    city_data = pd.concat(city_data_list, ignore_index=True)
    print(f"合并后总数据量：{len(city_data)}行")
    
    # 确保季节列存在
    if '季节' not in city_data.columns:
        print("在合并数据中重新生成季节列...")
        city_data['月份'] = city_data['时间'].str.split('-').str[1].astype(int)
        
        def get_season(month):
            if month in [12, 1, 2]:
                return '冬季'
            elif month in [3, 4, 5]:
                return '春季'
            elif month in [6, 7, 8]:
                return '夏季'
            else:
                return '秋季'
        
        city_data['季节'] = city_data['月份'].apply(get_season)
    
    # 计算年度平均值
    annual_avg = city_data.groupby(['城市', '年份']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean', 
        'AQI达标率': 'mean'
    }).reset_index()
    
    # 创建专业的颜色方案
    colors = plt.cm.Set3(np.linspace(0, 1, len(annual_avg['城市'].unique())))
    
    # 1. PM2.5年际变化 - 单独图表
    plt.figure(figsize=(14, 8))
    for i, city in enumerate(annual_avg['城市'].unique()):
        city_data_plot = annual_avg[annual_avg['城市'] == city]
        plt.plot(city_data_plot['年份'], city_data_plot['PM2.5'], 
                marker='o', linewidth=3, markersize=8, label=city, color=colors[i])
    
    plt.title('珠三角9市PM2.5浓度年际变化趋势 (2021-2024)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
    plt.xlabel('年份', fontsize=14, fontname='SimHei')
    plt.ylabel('PM2.5浓度 (μg/m3)', fontsize=14, fontname='SimHei')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'family': 'SimHei', 'size': 10})
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks([2021, 2022, 2023, 2024], fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('PM2.5_年际变化趋势.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    # 2. PM10年际变化 - 单独图表
    plt.figure(figsize=(14, 8))
    for i, city in enumerate(annual_avg['城市'].unique()):
        city_data_plot = annual_avg[annual_avg['城市'] == city]
        plt.plot(city_data_plot['年份'], city_data_plot['PM10'], 
                marker='s', linewidth=3, markersize=8, label=city, color=colors[i])
    
    plt.title('珠三角9市PM10浓度年际变化趋势 (2021-2024)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
    plt.xlabel('年份', fontsize=14, fontname='SimHei')
    plt.ylabel('PM10浓度 (μg/m3)', fontsize=14, fontname='SimHei')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'family': 'SimHei', 'size': 10})
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks([2021, 2022, 2023, 2024], fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('PM10_年际变化趋势.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    # 3. AQI达标率年际变化 - 单独图表
    plt.figure(figsize=(14, 8))
    for i, city in enumerate(annual_avg['城市'].unique()):
        city_data_plot = annual_avg[annual_avg['城市'] == city]
        plt.plot(city_data_plot['年份'], city_data_plot['AQI达标率']*100, 
                marker='^', linewidth=3, markersize=8, label=city, color=colors[i])
    
    plt.title('珠三角9市AQI达标率年际变化趋势 (2021-2024)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
    plt.xlabel('年份', fontsize=14, fontname='SimHei')
    plt.ylabel('AQI达标率 (%)', fontsize=14, fontname='SimHei')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'family': 'SimHei', 'size': 10})
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.xticks([2021, 2022, 2023, 2024], fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('AQI达标率_年际变化趋势.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    # 4. PM2.5改善率 - 单独图表
    improvement_data = []
    for city in annual_avg['城市'].unique():
        city_years = annual_avg[annual_avg['城市'] == city].sort_values('年份')
        if len(city_years) >= 2:
            first_pm25 = city_years.iloc[0]['PM2.5']
            last_pm25 = city_years.iloc[-1]['PM2.5']
            improvement_rate = (last_pm25 - first_pm25) / first_pm25 * 100
            improvement_data.append({'城市': city, 'PM2.5改善率(%)': improvement_rate})
    
    if improvement_data:
        improvement = pd.DataFrame(improvement_data)
        plt.figure(figsize=(12, 8))
        colors_bar = ['#2E8B57' if x < 0 else '#CD5C5C' for x in improvement['PM2.5改善率(%)']]
        bars = plt.bar(improvement['城市'], improvement['PM2.5改善率(%)'], 
                      color=colors_bar, alpha=0.8, edgecolor='black', linewidth=0.5)
        
        plt.title('各城市PM2.5浓度改善率 (2021-2024)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
        plt.xlabel('城市', fontsize=14, fontname='SimHei')
        plt.ylabel('PM2.5改善率 (%)', fontsize=14, fontname='SimHei')
        plt.xticks(rotation=45, fontsize=12, fontname='SimHei')
        plt.yticks(fontsize=12)
        plt.grid(True, alpha=0.3, axis='y', linestyle='--')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + (0.5 if height > 0 else -1),
                    f'{height:.1f}%', ha='center', va='bottom' if height > 0 else 'top', 
                    fontsize=10, fontweight='bold', fontname='SimHei')
        
        # 添加零线参考
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('PM2.5改善率分析.png', dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
    
    return city_data

# 执行城市级别年际趋势分析
city_data = plot_annual_trend_city_level()

def plot_spatial_distribution():
    """绘制空间分布特征图 - 单独输出每个子图"""
    if city_data is None:
        print("没有可用的城市数据")
        return
        
    # 计算各城市四年平均浓度
    spatial_avg = city_data.groupby('城市').agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'AQI达标率': 'mean'
    }).reset_index()
    
    # 1. PM2.5空间分布 - 单独图表
    plt.figure(figsize=(14, 8))
    sorted_pm25 = spatial_avg.sort_values('PM2.5', ascending=False)
    colors_pm25 = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(sorted_pm25)))
    bars1 = plt.bar(sorted_pm25['城市'], sorted_pm25['PM2.5'], 
                   color=colors_pm25, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    plt.title('珠三角9市PM2.5浓度空间分布 (2021-2024年平均)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
    plt.xlabel('城市', fontsize=14, fontname='SimHei')
    plt.ylabel('PM2.5浓度 (μg/m3)', fontsize=14, fontname='SimHei')
    plt.xticks(rotation=45, fontsize=12, fontname='SimHei')
    plt.yticks(fontsize=12)
    plt.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    # 添加数值标签
    for bar in bars1:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}', ha='center', va='bottom', 
                fontsize=11, fontweight='bold', fontname='SimHei')
    
    plt.tight_layout()
    plt.savefig('PM2.5_空间分布.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    # 2. PM10空间分布 - 单独图表
    plt.figure(figsize=(14, 8))
    sorted_pm10 = spatial_avg.sort_values('PM10', ascending=False)
    colors_pm10 = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(sorted_pm10)))
    bars2 = plt.bar(sorted_pm10['城市'], sorted_pm10['PM10'],
                   color=colors_pm10, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    plt.title('珠三角9市PM10浓度空间分布 (2021-2024年平均)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
    plt.xlabel('城市', fontsize=14, fontname='SimHei')
    plt.ylabel('PM10浓度 (μg/m3)', fontsize=14, fontname='SimHei')
    plt.xticks(rotation=45, fontsize=12, fontname='SimHei')
    plt.yticks(fontsize=12)
    plt.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    for bar in bars2:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}', ha='center', va='bottom', 
                fontsize=11, fontweight='bold', fontname='SimHei')
    
    plt.tight_layout()
    plt.savefig('PM10_空间分布.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    # 3. AQI达标率空间分布 - 单独图表
    plt.figure(figsize=(14, 8))
    sorted_aqi = spatial_avg.sort_values('AQI达标率', ascending=True)
    colors_aqi = plt.cm.RdYlBu_r(np.linspace(0.8, 0.2, len(sorted_aqi)))
    bars3 = plt.bar(sorted_aqi['城市'], sorted_aqi['AQI达标率']*100,
                   color=colors_aqi, alpha=0.8, edgecolor='black', linewidth=0.5)
    
    plt.title('珠三角9市AQI达标率空间分布 (2021-2024年平均)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
    plt.xlabel('城市', fontsize=14, fontname='SimHei')
    plt.ylabel('AQI达标率 (%)', fontsize=14, fontname='SimHei')
    plt.xticks(rotation=45, fontsize=12, fontname='SimHei')
    plt.yticks(fontsize=12)
    plt.grid(True, alpha=0.3, axis='y', linestyle='--')
    
    for bar in bars3:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%', ha='center', va='bottom', 
                fontsize=11, fontweight='bold', fontname='SimHei')
    
    plt.tight_layout()
    plt.savefig('AQI达标率_空间分布.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()

# 执行空间分布分析
plot_spatial_distribution()

def plot_seasonal_pattern():
    """绘制年份季节分布特征图 - 单独输出每个子图"""
    if city_data is None:
        print("没有可用的城市数据")
        return
        
    # 确保季节列存在
    if '季节' not in city_data.columns:
        print("在city_data中重新生成季节列...")
        city_data['月份'] = city_data['时间'].str.split('-').str[1].astype(int)
        
        def get_season(month):
            if month in [12, 1, 2]:
                return '冬季'
            elif month in [3, 4, 5]:
                return '春季'
            elif month in [6, 7, 8]:
                return '夏季'
            else:
                return '秋季'
        
        city_data['季节'] = city_data['月份'].apply(get_season)
    
    # 只使用2021-2023年的数据进行季节分析
    seasonal_data = city_data[city_data['年份'].isin([2021, 2022, 2023])].copy()
    
    # 创建年份季节列
    seasonal_data['年份季节'] = seasonal_data['年份'].astype(str) + '年' + seasonal_data['季节']
    
    # 定义正确的年份季节顺序
    year_season_order = []
    for year in [2021, 2022, 2023]:
        for season in ['春季', '夏季', '秋季', '冬季']:
            year_season_order.append(f"{year}年{season}")
    
    seasonal_data['年份季节'] = pd.Categorical(seasonal_data['年份季节'], categories=year_season_order, ordered=True)
    
    # 计算年份季节平均值
    year_season_avg = seasonal_data.groupby(['城市', '年份季节']).agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'AQI达标率': 'mean'
    }).reset_index()
    
    print("年份季节数据统计：")
    print(f"城市数量：{year_season_avg['城市'].nunique()}")
    print(f"年份季节类别：{len(year_season_avg['年份季节'].unique())}")
    print(f"数据时间段：{year_season_avg['年份季节'].min()} 到 {year_season_avg['年份季节'].max()}")
    
    # 创建专业的颜色方案
    colors = plt.cm.Set3(np.linspace(0, 1, len(year_season_avg['城市'].unique())))
    
    # 1. PM2.5年份季节变化 - 单独图表
    plt.figure(figsize=(16, 8))
    seasonal_pivot_pm25 = year_season_avg.pivot(index='年份季节', columns='城市', values='PM2.5')
    seasonal_pivot_pm25 = seasonal_pivot_pm25.reindex(year_season_order)
    
    for i, city in enumerate(seasonal_pivot_pm25.columns):
        plt.plot(seasonal_pivot_pm25.index, seasonal_pivot_pm25[city], 
                marker='o', linewidth=2.5, markersize=6, label=city, color=colors[i])
    
    plt.title('珠三角9市PM2.5浓度年份季节变化 (2021-2023年)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
    plt.xlabel('年份季节', fontsize=14, fontname='SimHei')
    plt.ylabel('PM2.5浓度 (μg/m3)', fontsize=14, fontname='SimHei')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'family': 'SimHei', 'size': 10})
    plt.grid(True, alpha=0.3, linestyle='--')
    
    x_positions = range(len(year_season_order))
    plt.xticks(x_positions, year_season_order, rotation=45, fontsize=11, fontname='SimHei')
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('PM2.5_年份季节变化.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    # 2. PM10年份季节变化 - 单独图表
    plt.figure(figsize=(16, 8))
    seasonal_pivot_pm10 = year_season_avg.pivot(index='年份季节', columns='城市', values='PM10')
    seasonal_pivot_pm10 = seasonal_pivot_pm10.reindex(year_season_order)
    
    for i, city in enumerate(seasonal_pivot_pm10.columns):
        plt.plot(seasonal_pivot_pm10.index, seasonal_pivot_pm10[city], 
                marker='s', linewidth=2.5, markersize=6, label=city, color=colors[i])
    
    plt.title('珠三角9市PM10浓度年份季节变化 (2021-2023年)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
    plt.xlabel('年份季节', fontsize=14, fontname='SimHei')
    plt.ylabel('PM10浓度 (μg/m3)', fontsize=14, fontname='SimHei')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'family': 'SimHei', 'size': 10})
    plt.grid(True, alpha=0.3, linestyle='--')
    
    plt.xticks(x_positions, year_season_order, rotation=45, fontsize=11, fontname='SimHei')
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('PM10_年份季节变化.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    # 3. AQI达标率年份季节变化 - 单独图表
    plt.figure(figsize=(16, 8))
    seasonal_pivot_aqi = year_season_avg.pivot(index='年份季节', columns='城市', values='AQI达标率') * 100
    seasonal_pivot_aqi = seasonal_pivot_aqi.reindex(year_season_order)
    
    for i, city in enumerate(seasonal_pivot_aqi.columns):
        plt.plot(seasonal_pivot_aqi.index, seasonal_pivot_aqi[city], 
                marker='^', linewidth=2.5, markersize=6, label=city, color=colors[i])
    
    plt.title('珠三角9市AQI达标率年份季节变化 (2021-2023年)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
    plt.xlabel('年份季节', fontsize=14, fontname='SimHei')
    plt.ylabel('AQI达标率 (%)', fontsize=14, fontname='SimHei')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'family': 'SimHei', 'size': 10})
    plt.grid(True, alpha=0.3, linestyle='--')
    
    plt.xticks(x_positions, year_season_order, rotation=45, fontsize=11, fontname='SimHei')
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.savefig('AQI达标率_年份季节变化.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()
    
    # 4. 污染物浓度季节热力图 - 单独图表
    season_avg = seasonal_data.groupby('季节').mean(numeric_only=True)
    season_order = ['春季', '夏季', '秋季', '冬季']
    season_avg = season_avg.reindex(season_order)
    
    plt.figure(figsize=(10, 8))
    im = plt.imshow(season_avg[['PM2.5', 'PM10']].T, cmap='YlOrRd', aspect='auto')
    
    plt.title('污染物浓度季节热力图 (2021-2023年平均)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
    plt.xticks(range(len(season_order)), season_order, fontsize=12, fontname='SimHei')
    plt.yticks(range(2), ['PM2.5', 'PM10'], fontsize=12, fontname='SimHei')
    
    # 添加颜色条
    cbar = plt.colorbar(im, shrink=0.8)
    cbar.set_label('浓度 (μg/m3)', fontsize=12, fontname='SimHei')  
    
    # 添加数值标注
    for i in range(2):
        for j in range(4):
            plt.text(j, i, f'{season_avg.iloc[j, i]:.1f}', 
                    ha='center', va='center', fontweight='bold', fontsize=14, fontname='SimHei',
                    color='white' if season_avg.iloc[j, i] > season_avg.values.mean() else 'black')
    
    plt.tight_layout()
    plt.savefig('污染物浓度_季节热力图.png', dpi=300, bbox_inches='tight', facecolor='white')
    plt.show()

# 执行季节分布分析
plot_seasonal_pattern()

def analyze_station_data():
    """分析监测子站数据 - 修改为读取所有年份数据"""
    # 读取所有年份的子站数据
    years = [2021, 2022, 2023, 2024]
    station_data_list = []
    
    for year in years:
        try:
            filename = f"六种污染物浓度_{year}预处理后.csv"
            df = pd.read_csv(filename, encoding='utf-8-sig')
            df['年份'] = year
            
            # 确保有季节列
            if '季节' not in df.columns and '时间' in df.columns:
                print(f"在{year}年子站数据中生成季节列...")
                df['月份'] = df['时间'].str.split('-').str[1].astype(int)
                
                def get_season(month):
                    if month in [12, 1, 2]:
                        return '冬季'
                    elif month in [3, 4, 5]:
                        return '春季'
                    elif month in [6, 7, 8]:
                        return '夏季'
                    else:
                        return '秋季'
                
                df['季节'] = df['月份'].apply(get_season)
            
            station_data_list.append(df)
            print(f"成功读取{year}年子站数据，共{len(df)}行")
            
        except FileNotFoundError:
            print(f"警告：{year}年子站数据文件未找到")
            continue
        except Exception as e:
            print(f"读取{year}年子站数据时出错：{e}")
            continue
    
    if not station_data_list:
        print("错误：没有找到任何子站数据文件")
        return None
    
    # 合并所有年份的子站数据
    station_data = pd.concat(station_data_list, ignore_index=True)
    print(f"合并后子站数据总量：{len(station_data)}行")
    
    # 读取子站属性
    try:
        station_info = pd.read_excel("监测子站资料.xlsx")
        print(f"成功读取子站属性数据，共{len(station_info)}个站点")
        station_data = station_data.merge(station_info, left_on='监测子站名称', right_on='监测子站', how='left')
    except FileNotFoundError:
        print("警告：子站属性文件未找到")
        station_info = None
    
    return station_data

# 读取子站数据
station_data = analyze_station_data()

if station_data is not None:
    # 子站数据年际变化趋势 - 单独输出每个污染物图表
    def plot_station_annual_trend():
        """绘制子站年际变化趋势 - 单独输出每个污染物"""
        # 计算各年份平均值
        annual_station_avg = station_data.groupby(['城市', '年份']).agg({
            'SO2': 'mean',
            'NO2': 'mean', 
            'O3': 'mean',
            'PM10': 'mean',
            'PM2.5': 'mean',
            'CO_mg/m3': 'mean',  
            '综合污染指数': 'mean'
        }).reset_index()
        
        pollutants = ['SO2', 'NO2', 'O3', 'PM10', 'PM2.5', 'CO_mg/m3', '综合污染指数']  # 修改为正确的列名
        titles = ['SO2', 'NO2', 'O3', 'PM10', 'PM2.5', 'CO', '综合污染指数']  # CO_mg/m3的显示标题仍用CO
        markers = ['o', 's', '^', 'D', 'v', '*', 'p']  # 为CO添加标记
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(annual_station_avg['城市'].unique())))
        
        for i, (pollutant, title, marker) in enumerate(zip(pollutants, titles, markers)):
            plt.figure(figsize=(14, 8))
            
            for j, city in enumerate(annual_station_avg['城市'].unique()):
                city_data = annual_station_avg[annual_station_avg['城市'] == city].sort_values('年份')
                plt.plot(city_data['年份'], city_data[pollutant], 
                        marker=marker, linewidth=2.5, markersize=7, label=city, color=colors[j])
            
            plt.title(f'监测子站{title}浓度年际变化趋势 (2021-2024)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
            plt.xlabel('年份', fontsize=14, fontname='SimHei')
            if pollutant in ['PM10', 'PM2.5', 'SO2', 'NO2', 'O3']:
                plt.ylabel(f'{title}浓度 (μg/m3)', fontsize=14, fontname='SimHei')
            elif pollutant == 'CO_mg/m3':
                plt.ylabel('CO浓度 (mg/m3)', fontsize=14, fontname='SimHei')  # CO的特殊单位
            else:
                plt.ylabel('综合污染指数', fontsize=14, fontname='SimHei')
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', prop={'family': 'SimHei', 'size': 10})
            plt.grid(True, alpha=0.3, linestyle='--')
            plt.xticks([2021, 2022, 2023, 2024], fontsize=12)
            plt.yticks(fontsize=12)
            plt.tight_layout()
            # 修复文件名中的斜杠问题
            safe_title = title.replace('/', '_')
            plt.savefig(f'子站_{safe_title}_年际变化.png', dpi=300, bbox_inches='tight', facecolor='white')
            plt.show()
    
    # 子站空间分布特征 - 单独输出每个污染物图表
    def plot_station_spatial_distribution():
        """绘制子站空间分布特征 - 单独输出每个污染物"""
        city_station_avg = station_data.groupby('城市').agg({
            'SO2': 'mean',
            'NO2': 'mean',
            'O3': 'mean', 
            'PM10': 'mean',
            'PM2.5': 'mean',
            'CO_mg/m3': 'mean',  
            '综合污染指数': 'mean'
        }).reset_index()
        
        pollutants = ['SO2', 'NO2', 'O3', 'PM10', 'PM2.5', 'CO_mg/m3', '综合污染指数']  
        titles = ['SO2浓度', 'NO2浓度', 'O3浓度', 'PM10浓度', 'PM2.5浓度', 'CO浓度', '综合污染指数']  # CO_mg/m3的显示标题仍用CO浓度
        
        for i, (pollutant, title) in enumerate(zip(pollutants, titles)):
            plt.figure(figsize=(14, 8))
            sorted_data = city_station_avg.sort_values(pollutant, ascending=False)
            colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(sorted_data)))
            bars = plt.bar(sorted_data['城市'], sorted_data[pollutant], 
                          color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
            
            plt.title(f'各城市监测子站{title}对比 (2021-2024年平均)', fontsize=16, fontweight='bold', fontname='SimHei', pad=20)
            plt.xlabel('城市', fontsize=14, fontname='SimHei')
            if pollutant in ['PM10', 'PM2.5', 'SO2', 'NO2', 'O3']:
                plt.ylabel('浓度 (μg/m3)', fontsize=14, fontname='SimHei')
            elif pollutant == 'CO_mg/m3':
                plt.ylabel('CO浓度 (mg/m3)', fontsize=14, fontname='SimHei')  # CO的特殊单位
            else:
                plt.ylabel('综合污染指数', fontsize=14, fontname='SimHei')
            plt.xticks(rotation=45, fontsize=12, fontname='SimHei')
            plt.yticks(fontsize=12)
            plt.grid(True, alpha=0.3, axis='y', linestyle='--')
            
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                       f'{height:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold', fontname='SimHei')
            
            plt.tight_layout()
            # 修复文件名中的斜杠问题
            safe_pollutant = pollutant.replace('/', '_')
            plt.savefig(f'子站_{safe_pollutant}_空间分布.png', dpi=300, bbox_inches='tight', facecolor='white')
            plt.show()
    
    # 执行子站分析
    plot_station_annual_trend()
    plot_station_spatial_distribution()

else:
    print("子站数据不可用，跳过子站分析部分")

print("已生成以下可视化图表：")
print("\n城市级别分析：")
print("1. PM2.5_年际变化趋势.png")
print("2. PM10_年际变化趋势.png") 
print("3. AQI达标率_年际变化趋势.png")
print("4. PM2.5改善率分析.png")
print("5. PM2.5_空间分布.png")
print("6. PM10_空间分布.png")
print("7. AQI达标率_空间分布.png")
print("8. PM2.5_年份季节变化.png")
print("9. PM10_年份季节变化.png")
print("10. AQI达标率_年份季节变化.png")
print("11. 污染物浓度_季节热力图.png")
print("\n子站级别分析：")
print("12. 子站_SO₂_年际变化.png")
print("13. 子站_NO₂_年际变化.png")
print("14. 子站_O₃_年际变化.png")
print("15. 子站_PM10_年际变化.png")
print("16. 子站_PM2.5_年际变化.png")
print("17. 子站_CO_年际变化.png")  
print("18. 子站_综合污染指数_年际变化.png")
print("19. 子站_SO2_空间分布.png")
print("20. 子站_NO2_空间分布.png")
print("21. 子站_O3_空间分布.png")
print("22. 子站_PM10_空间分布.png")
print("23. 子站_PM2.5_空间分布.png")
print("24. 子站_CO_mg_m3_空间分布.png")  
print("25. 子站_综合污染指数_空间分布.png")