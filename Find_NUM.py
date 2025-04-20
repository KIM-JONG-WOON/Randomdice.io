import streamlit as st
import pandas as pd
import numpy as np

st.title("🎯 로또 번호 추출기 (GitHub 엑셀 기반)")

# ✅ GitHub Raw URL 고정
github_url = "https://raw.githubusercontent.com/KIM-JONG-WOON/Randomdice.io/main/NUM_Ro.xlsx"

try:
    # 엑셀 불러오기 - openpyxl 명시!
    df = pd.read_excel(github_url, usecols="C:I", engine='openpyxl')
    
    # 숫자 데이터 추출 및 전처리
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
    st.error(f"❌ 엑셀 불러오기 실패: {e}")
    st.info("💡 올바른 Raw URL인지 확인하세요.")
