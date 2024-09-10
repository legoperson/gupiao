import plotly.express as px
import streamlit as st
import pandas as pd
import pickle


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
    # fig = px.histogram(df[column_name], nbins=100)
    fig = px.histogram(df[column_name], x=column_name)

    # 设置 bin 的大小为 0.003
    fig.update_traces(xbins=dict(size=0.003))

    # 使用 Streamlit 显示图像
    st.plotly_chart(fig)

def plot_boxplot(df, column_name):
    fig = px.box(df, x='Date', y=column_name, points='all')  # 不显示任何数据点为outliers

    # 更新中位线的颜色
    fig.update_traces(marker=dict(color='blue'),  # 其他数据点的颜色保持默认
                  line=dict(color='red'))    # 中位线的颜色
    fig.update_layout(yaxis=dict(range=[0.5, 1.2]))  # 设置 y 轴范围为 0 到 2
    st.plotly_chart(fig)

# 从 .pk 文件中加载 DataFrame
with open('dataframe_for_steamlit.pk', 'rb') as file:
    df = pickle.load(file)

# 将 'Date' 列转换为日期格式（如果还没有）
df['Date'] = pd.to_datetime(df['Date'])
plot_boxplot(df, 'ActualReturn')
plot_histogram_of_columns(df,'ActualReturn')

plot_daily_table(df)
