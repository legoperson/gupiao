import plotly.express as px
import streamlit as st
import pandas as pd
import pickle
import plotly.graph_objects as go


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


def plot_histogram_of_columns(df, column_name):
    # 绘制直方图
    # fig = px.histogram(df[column_name], nbins=100)
    fig = px.histogram(df[column_name], x=column_name)

    # 设置 bin 的大小为 0.003
    fig.update_traces(xbins=dict(size=0.003))

    # 使用 Streamlit 显示图像
    st.plotly_chart(fig)


def plot_cumsum(df_in, randf_in, column_name):
    # 假设 df 是你的数据框，column_name 是你要汇总的列名
    # Assume df_in and randf_in are provided DataFrames
    df = df_in.copy()
    ran_df = randf_in.copy()
    
    # Process the first DataFrame
    df[column_name] -= 1
    df_grouped = df.groupby('Date')[column_name].sum().reset_index()
    df_grouped['Accumulated_Sum'] = df_grouped[column_name].cumsum()
    
    # Process the second DataFrame
    ran_df[column_name] -= 1
    ran_df_grouped = ran_df.groupby('Date')[column_name].sum().reset_index()
    ran_df_grouped['Accumulated_Sum'] = ran_df_grouped[column_name].cumsum() / 10
    
    # Create a figure
    fig = go.Figure()
    
    # Add the first line for the original DataFrame
    fig.add_trace(go.Scatter(x=df_grouped['Date'], y=df_grouped['Accumulated_Sum'],
                             mode='lines', name='Original Data'))
    
    # Add the second line for the random DataFrame
    fig.add_trace(go.Scatter(x=ran_df_grouped['Date'], y=ran_df_grouped['Accumulated_Sum'],
                             mode='lines', name='Random Data (Scaled)'))
    
    # Update layout for the figure
    fig.update_layout(title='按日期的累积和对比',
                      xaxis_title='Date',
                      yaxis_title='Accumulated Sum')
    
    # Display the plot using Streamlit
    st.plotly_chart(fig)


def plot_boxplot(df, column_name):
    fig = px.box(df, x='Date', y=column_name, points='all')  # 不显示任何数据点为outliers

    # 更新中位线的颜色
    fig.update_traces(marker=dict(color='blue'),  # 其他数据点的颜色保持默认
                      line=dict(color='red'))  # 中位线的颜色
    fig.update_layout(yaxis=dict(range=[0.5, 1.2]))  # 设置 y 轴范围为 0 到 2
    st.plotly_chart(fig)


# 从 .pk 文件中加载 DataFrame
with open('dataframe_for_steamlit_with_random.pk', 'rb') as file:
    (DF, rand_DF) = pickle.load(file)

# 将 'Date' 列转换为日期格式（如果还没有）
DF['Date'] = pd.to_datetime(DF['Date'])
number = st.number_input('请输入一个浮点数', value=0.0, format="%.2f")

# 创建一个按钮，当按钮被按下时执行绘图操作
if st.button('绘制图表'):
    df = DF.copy()
    rand_df = rand_DF
    df['ActualReturn'] = df.apply(lambda row: number if row['Return_by_10'] > number else row['Return_end_10'], axis=1)
    rand_df['ActualReturn'] = rand_df.apply(lambda row: number if row['Return_by_10'] > number else row['Return_end_10'], axis=1)

    plot_cumsum(df,rand_df, 'ActualReturn')
    plot_boxplot(df, 'ActualReturn')
    plot_histogram_of_columns(df, 'ActualReturn')
    plot_daily_table(df)
