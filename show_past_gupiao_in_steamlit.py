import streamlit as st
import pandas as pd
import pickle

# 从 .pk 文件中加载 DataFrame
with open('dataframe_for_steamlit.pk', 'rb') as file:
    df = pickle.load(file)

# 确保 'Date' 列为日期格式（如果需要）
df['Date'] = pd.to_datetime(df['Date'])

# 从数据框获取唯一的日期
unique_dates = df['Date'].dt.date.unique()

# Streamlit应用程序标题
st.title('根据日期显示股票数据')

# 日期选择器
selected_date = st.selectbox('选择一个日期:', unique_dates)

# 根据选定日期过滤数据
filtered_df = df[df['Date'].dt.date == selected_date]

# 在页面上显示结果
st.write(f'日期: {selected_date} 的数据如下:')
st.dataframe(filtered_df)
