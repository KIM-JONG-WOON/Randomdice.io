import streamlit as st
import pandas as pd
import numpy as np

st.title("🎯 로또 번호 추출기 (확률 기반)")

uploaded_file = st.file_uploader("📂 엑셀 업로드", type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, usecols="C:I")
    numeric_data = df.select_dtypes(include='number').stack().dropna()
    value_counts = numeric_data.value_counts()
    probabilities = value_counts / value_counts.sum()

    if st.button("✨ 번호 추출하기"):
        selected = np.random.choice(probabilities.index, size=7, replace=False, p=probabilities.values)
        st.success("추출된 번호:")
        st.write("🎱", sorted(selected))
else:
    st.info("왼쪽 사이드바에서 엑셀 파일을 업로드하세요.")