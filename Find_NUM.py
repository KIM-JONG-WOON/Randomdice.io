import streamlit as st
import pandas as pd
import numpy as np
import openpyxl

st.title("🎯 로또 번호 추출기 (GitHub 엑셀 기반)")

# GitHub Raw URL 입력
github_url = st.text_input("📂 GitHub 엑셀 파일 Raw URL을 입력하세요",
    value="https://raw.githubusercontent.com/KIM-JONG-WOON/Randomdice.io/main/NUM_Ro.xlsx")

if github_url:
    try:
        # ✅ engine='openpyxl' 명시
        df = pd.read_excel(github_url, usecols="C:I", engine='openpyxl')
        numeric_data = df.select_dtypes(include='number').stack().dropna()
        value_counts = numeric_data.value_counts()
        probabilities = value_counts / value_counts.sum()

        if st.button("✨ 번호 추출하기"):
            selected = np.random.choice(probabilities.index, size=7, replace=False, p=probabilities.values)
            st.success("추출된 번호:")
            st.write("🎱", sorted(selected))

    except Exception as e:
        st.error(f"❌ 파일을 불러오는 중 오류 발생:\n{e}")
        
