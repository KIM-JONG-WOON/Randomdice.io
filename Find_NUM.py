import streamlit as st
import pandas as pd
import numpy as np
import requests

# ✅ 모바일 대응 레이아웃
st.set_page_config(page_title="로또 번호 추출기", layout="centered")

st.title("📱 로또 번호 추출기 (한 줄 7개 가로 배치)")

# ✅ GitHub .xls 파일 Raw URL
xls_url = "https://raw.githubusercontent.com/KIM-JONG-WOON/Randomdice.io/main/NUM_Ro.xls"

if xls_url:
    try:
        # URL 확인
        response = requests.get(xls_url)
        if response.status_code != 200:
            raise ValueError(f"⚠️ URL 응답 오류: {response.status_code}")

        # .xls 파일 읽기
        df = pd.read_excel(xls_url, usecols="C:I", engine='xlrd')

        # 숫자 추출 및 확률 계산
        numeric_data = df.select_dtypes(include='number').stack().dropna()
        value_counts = numeric_data.value_counts()
        probabilities = value_counts / value_counts.sum()
        
        # 번호 자동 추출
        selected = sorted(np.random.choice(
            probabilities.index,
            size=7,
            replace=False,
            p=probabilities.values
        ))

        st.button("✨ 번호 7개 추출하기")
        # ✅ 가로 한 줄에 7개, 모바일에서도 잘 보이게
        st.subheader("🎉 자동 추출된 번호")
        cols = st.columns(7)
        for i, num in enumerate(selected):
            with cols[i]:
                st.markdown(
                    f"""
                    <div style='
                        width: 11vw;
                        aspect-ratio: 1 / 1;
                        background-color: #f0f0f0;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 4vw;
                        font-weight: bold;
                        color: #000000;
                        box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
                        margin: auto;
                    '>{int(num)}</div>
                    """,
                    unsafe_allow_html=True
                )

    except Exception as e:
        st.error(f"❌ 오류 발생:\n\n{e}")
        st.info("📎 올바른 GitHub Raw URL인지, 파일이 .xls 형식인지 확인해주세요.")
else:
    st.info("📥 위에 GitHub .xls 주소를 입력하세요.")
