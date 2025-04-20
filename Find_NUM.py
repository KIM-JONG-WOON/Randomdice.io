import streamlit as st
import pandas as pd
import numpy as np

st.title("🎯 로또 번호 추출기 (.xls 엑셀 기반)")

# ✅ GitHub에 올린 .xls Raw URL 입력
xls_url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/NUM_Ro.xls"

try:
    df = pd.read_excel(xls_url, usecols="C:I", engine='xlrd')  # .xls는 xlrd 사용

    # 데이터 처리
    numeric_data = df.select_dtypes(include='number').stack().dropna()
    value_counts = numeric_data.value_counts()
    probabilities = value_counts / value_counts.sum()

    st.subheader("📊 번호별 출현 확률")
    st.dataframe(probabilities.mul(100).round(2).rename("출현확률 (%)"))

    if st.button("✨ 번호 7개 추출하기"):
        selected = np.random.choice(
            probabilities.index,
            size=7,
            replace=False,
            p=probabilities.values
        )
        st.success("🎉 추출된 번호:")
        st.write("🎱", sorted(selected))

except Exception as e:
    st.error(f"❌ .xls 불러오기 실패: {e}")
