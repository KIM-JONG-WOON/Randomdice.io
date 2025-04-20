import streamlit as st
import pandas as pd
import numpy as np
import requests

st.title("🎯🎯🎯")

# ✅ GitHub .xls 파일 Raw URL 입력
xls_url = "https://raw.githubusercontent.com/KIM-JONG-WOON/Randomdice.io/main/NUM_Ro.xls"

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

        # 추출 버튼
        selected = np.random.choice(
            probabilities.index,
            size=7,
            replace=False,
            p=probabilities.values
        )
        selected = sorted(selected)

        # ✅ 시각적으로 강조된 출력
        st.subheader("🎉 추출된 번호")

        st.button("✨ 번호 7개 추출하기")
        cols = st.columns(7)
        for i, num in enumerate(selected):
            with cols[i]:
                st.markdown(
                    f"""
                    <div style='
                        width: 16vw;
                        aspect-ratio: 1 / 1;
                        background: #f0f0f0;
                        border-radius: 50%;
                        text-align: center;
                        font-size: 6vw;
                        font-weight: bold;
                        margin: auto;
                        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        '>
                        {int(num)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
    except Exception as e:
        st.error(f"❌ 오류 발생:\n\n{e}")
        st.info("⚠️ 반드시 GitHub의 Raw URL을 입력했는지, 파일이 .xls 형식인지 확인하세요.")
