import streamlit as st
import pandas as pd
import numpy as np
import requests

# 💡 모바일에 최적화된 화면 설정
st.set_page_config(page_title="모바일 추출기", layout="centered")

st.title("📱📱📱")

# ✅ GitHub Raw .xls 주소 입력
xls_url = "https://raw.githubusercontent.com/KIM-JONG-WOON/Randomdice.io/main/NUM_Ro.xls"

if xls_url:
    try:
        response = requests.get(xls_url)
        if response.status_code != 200:
            raise ValueError(f"⚠️ URL 응답 오류: {response.status_code}")

        # ✅ .xls 파일 읽기
        df = pd.read_excel(xls_url, usecols="C:I", engine='xlrd')

        # 숫자 데이터 추출 및 확률 계산
        numeric_data = df.select_dtypes(include='number').stack().dropna()
        value_counts = numeric_data.value_counts()
        probabilities = value_counts / value_counts.sum()

        # ✅ 자동 추출
        selected = sorted(np.random.choice(
            probabilities.index,
            size=7,
            replace=False,
            p=probabilities.values
        ))

        st.button("✨ 번호 7개 추출하기")
        # ✅ 번호 출력: 반응형 스타일 (모바일 최적화)
        st.subheader("🎉 자동 추출된 번호")
        for num in selected:
            st.markdown(
                f"""
                <div style='
                    width: 22vw;
                    aspect-ratio: 1 / 1;
                    background-color: #f8f9fa;
                    border-radius: 50%;
                    margin: 10px auto;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 6vw;
                    font-weight: bold;
                    color: #2c3e50;
                    box-shadow: 2px 2px 6px rgba(0,0,0,0.1);
                '>{int(num)}</div>
                """,
                unsafe_allow_html=True
            )

    except Exception as e:
        st.error(f"❌ 오류 발생:\n\n{e}")
        st.info("📎 GitHub Raw URL이 맞는지, 파일이 .xls 형식인지 확인해주세요.")
else:
    st.info("📥 위에 GitHub .xls 주소를 입력하세요.")
