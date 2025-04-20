import streamlit as st
import pandas as pd
import numpy as np
import requests

# 📱 모바일 레이아웃 최적화
st.set_page_config(page_title="추출기", layout="centered")

st.title("🎱🎱🎱")

# GitHub .xls Raw URL 입력
xls_url = "https://raw.githubusercontent.com/KIM-JONG-WOON/Randomdice.io/main/NUM_Ro.xls"

if xls_url:
    try:
        response = requests.get(xls_url)
        if response.status_code != 200:
            raise ValueError(f"⚠️ URL 응답 오류: {response.status_code}")

        df = pd.read_excel(xls_url, usecols="C:I", engine='xlrd')

        # 데이터 처리
        numeric_data = df.select_dtypes(include='number').stack().dropna()
        value_counts = numeric_data.value_counts()
        probabilities = value_counts / value_counts.sum()

        # 번호 추출
        selected = sorted(np.random.choice(
            probabilities.index,
            size=7,
            replace=False,
            p=probabilities.values
        ))

        # ✅ HTML 기반 1줄 7개 가로 정렬 출력
        st.button("✨ 번호 7개 추출하기")
        circle_html = "".join([
            f"""
            <div style='
                width: 50px;
                height: 50px;
                border-radius: 50%;
                background-color: #f0f0f0;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 5px;
                font-size: 20px;
                font-weight: bold;
                color: #000000;
                box-shadow: 1px 1px 4px rgba(0,0,0,0.2);
            '>{int(num)}</div>
            """ for num in selected
        ])

        st.markdown(
            f"""
            <div style='display: flex; justify-content: center; flex-wrap: nowrap;'>
                {circle_html}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"❌ 오류 발생:\n\n{e}")
        st.info("📎 URL과 파일 형식을 다시 확인해주세요.")
else:
    st.info("📥 위에 GitHub .xls 주소를 입력하세요.")
