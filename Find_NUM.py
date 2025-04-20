import streamlit as st
import pandas as pd
import numpy as np

st.title("🎯 로또 번호 추출기 (GitHub 엑셀 기반)")

# ✅ 깃허브 Raw 엑셀 파일 경로 입력
github_url = st.text_input("📂 GitHub 엑셀 파일 Raw URL을 입력하세요",
    value="https://github.com/KIM-JONG-WOON/Randomdice.io/blob/main/NUM_Ro.xlsx")

if github_url:
    try:
        df = pd.read_excel(github_url, usecols="C:I")
        numeric_data = df.select_dtypes(include='number').stack().dropna()
        value_counts = numeric_data.value_counts()
        probabilities = value_counts / value_counts.sum()

        if st.button("✨ 번호 추출하기"):
            selected = np.random.choice(probabilities.index, size=7, replace=False, p=probabilities.values)
            st.success("추출된 번호:")
            st.write("🎱", sorted(selected))
    except Exception as e:
        st.error(f"파일을 불러오는 중 오류 발생: {e}")