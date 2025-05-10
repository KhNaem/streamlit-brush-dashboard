import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Brush Real Plot (Fixed)", layout="wide")

st.title("📈 พล็อตกราฟตามเวลา (จากข้อมูลจริง Upper และ Lower)")

sheet_url = "https://docs.google.com/spreadsheets/d/1SOkIH9jchaJi_0eck5UeyUR8sTn2arndQofmXv5pTdQ/export?format=xlsx"
xls = pd.ExcelFile(sheet_url)
sheet_names = [s for s in xls.sheet_names if "Sheet" in s]

num_sheets = st.number_input("📌 จำนวน Sheet ที่ใช้พล็อต", min_value=1, max_value=len(sheet_names), value=6)
used_sheets = sheet_names[:num_sheets]

brush_numbers = list(range(1, 33))
upper_data = {n: {'x': [], 'y': []} for n in brush_numbers}
lower_data = {n: {'x': [], 'y': []} for n in brush_numbers}

for sheet in used_sheets:
    df_raw = xls.parse(sheet, header=None)
    try:
        h = float(df_raw.iloc[0, 7])
    except:
        continue

    df = xls.parse(sheet, skiprows=1, header=None).apply(pd.to_numeric, errors='coerce')
    for i in brush_numbers:
        # Upper = column 5 (F), Lower = column 2 (C)
        upper_val = df.iloc[i-1, 5]
        lower_val = df.iloc[i-1, 2]
        if pd.notna(upper_val):
            upper_data[i]['x'].append(h)
            upper_data[i]['y'].append(upper_val)
        if pd.notna(lower_val):
            lower_data[i]['x'].append(h)
            lower_data[i]['y'].append(lower_val)

# plot upper
fig_upper = go.Figure()
for i in brush_numbers:
    x = upper_data[i]['x']
    y = upper_data[i]['y']
    if len(x) >= 2:
        fig_upper.add_trace(go.Scatter(x=x, y=y, name=f"Upper {i}", mode='lines+markers'))
fig_upper.update_layout(title="🔺 ความยาว Upper ตามเวลา", xaxis_title="ชั่วโมง", yaxis_title="mm", xaxis=dict(dtick=10), yaxis=dict(range=[30, 65]))
st.plotly_chart(fig_upper, use_container_width=True)

# plot lower
fig_lower = go.Figure()
for i in brush_numbers:
    x = lower_data[i]['x']
    y = lower_data[i]['y']
    if len(x) >= 2:
        fig_lower.add_trace(go.Scatter(x=x, y=y, name=f"Lower {i}", mode='lines+markers', line=dict(dash='dot')))
fig_lower.update_layout(title="🔻 ความยาว Lower ตามเวลา", xaxis_title="ชั่วโมง", yaxis_title="mm", xaxis=dict(dtick=10), yaxis=dict(range=[30, 65]))
st.plotly_chart(fig_lower, use_container_width=True)
