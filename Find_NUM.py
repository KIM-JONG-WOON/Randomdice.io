import streamlit as st
import pandas as pd
import numpy as np
import requests

st.title("🎯 로또 번호 추출기 (GitHub .xls 파일 기반)")

# ✅ GitHub .xls 파일 Raw URL 입력
xls_url = st.text_input("📂 GitHub의 .xls 파일 Raw URL을 입력하세요",
    value="https://raw.githubusercontent.com/KIM-JONG-WOON/Randomdice.io/main/NUM_Ro.xls")

if xls_url:
    try:
        # 요청 먼저 확인
        response = requests.get(xls_url)
        if response.status_code != 200:
            raise ValueError(f"📛 URL 응답 오류: {response.status_code}")

        # ✅ .xls 엑셀 파일 읽기
        df = pd.read_excel(xls_url, usecols="C:I", engine='xlrd')

        # 숫자 데이터 추출
        numeric_data = df.select_dtypes(include='number').stack().dropna()
        value_counts = numeric_data.value_counts()
        probabilities = value_counts / value_counts.sum()

        st.subheader("📊 번호별 출현 확률 (%)")
        st.dataframe(probabilities.mul(100).round(2).rename("확률"))

        # 추출 버튼
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
        st.error(f"❌ 오류 발생:\n\n{e}")
        st.info("⚠️ 반드시 GitHub의 Raw URL을 입력했는지, 파일이 .xls 형식인지 확인하세요.")
