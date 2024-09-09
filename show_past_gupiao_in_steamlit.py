import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt

def plot_daily_table(df):
    # 获取唯一的日期列表
    unique_dates = df['Date'].dt.date.unique()

    # Streamlit应用程序标题
    st.title('按日期显示股票数据')

    # 为每个唯一日期创建一个展开项
    for date in unique_dates:
        # 过滤出当前日期的数据
        filtered_df = df[df['Date'].dt.date == date]

        # 使用st.expander为每个日期创建一个可展开的区域
        with st.expander(f"日期: {date}"):
            # 在展开项中显示该日期的数据
            st.dataframe(filtered_df)
            
def plot_histogram_of_columns(df,column_name):
    # 绘制直方图
    fig, ax = plt.subplots()
    ax.hist(df[column_name], bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f'{column_name} Histogram')
    ax.set_xlabel(f'{column_name}')
    ax.set_ylabel('Frequency')

    # 使用 Streamlit 显示图像
    st.pyplot(fig)
            
# 从 .pk 文件中加载 DataFrame
with open('dataframe_for_steamlit.pk', 'rb') as file:
    df = pickle.load(file)

# 将 'Date' 列转换为日期格式（如果还没有）
df['Date'] = pd.to_datetime(df['Date'])
plot_histogram_of_columns(df,'ActualReturn')
plot_daily_table(df)



