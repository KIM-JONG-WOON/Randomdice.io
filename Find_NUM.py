import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import BytesIO

# 📱 레이아웃
st.set_page_config(page_title="번호 추출기", layout="centered")
st.title("🎱 번호 추출기 (희귀도 가중)")

# GitHub .xls Raw URL
xls_url = "https://raw.githubusercontent.com/KIM-JONG-WOON/Randomdice.io/main/NUM_Ro.xls"

# ----- 유틸 -----
@st.cache_data(show_spinner=True, ttl=60*30)
def load_excel_from_url(url: str, usecols: str = "C:I") -> pd.DataFrame:
    r = requests.get(url, timeout=20)
    if r.status_code != 200:
        raise ValueError(f"URL 응답 오류: {r.status_code}")
    bio = BytesIO(r.content)
    try:
        df = pd.read_excel(bio, usecols=usecols)  # 엔진 자동
    except Exception:
        df = pd.read_excel(bio, usecols=usecols, engine="xlrd")
    return df

def make_inverse_freq_probabilities(df: pd.DataFrame) -> pd.Series:
    """
    등장 빈도가 낮을수록 높은 가중치.
    가중치 = 1 / freq  → 확률 = 가중치 / 가중치합
    """
    numeric_data = df.select_dtypes(include="number").stack().dropna()
    if numeric_data.empty:
        raise ValueError("숫자 데이터를 찾지 못했습니다. usecols 범위를 확인하세요.")

    counts = numeric_data.value_counts()          # 각 숫자의 등장 빈도
    weights = 1.0 / counts.astype(float)          # 빈도 낮을수록 무거움(=더 높은 확률)
    probs = weights / weights.sum()

    # 안정성: 혹시 NaN/inf가 생기면 방지
    probs = probs.replace([np.inf, -np.inf], np.nan).dropna()
    if probs.empty:
        raise ValueError("가중치 계산 실패: 데이터 확인 필요.")
    return probs

def draw_numbers(probs: pd.Series, k: int = 6) -> np.ndarray:
    unique_n = len(probs)
    if unique_n == 0:
        raise ValueError("추출 가능한 값이 없습니다.")
    draw_n = min(k, unique_n)  # 고유 값 부족 시 가능한 만큼만
    chosen = np.random.choice(
        probs.index,
        size=draw_n,
        replace=False,
        p=probs.values
    )
    return np.sort(chosen)

# ----- 본문 -----
st.caption("엑셀의 숫자 등장 **빈도가 낮은 숫자**일수록 더 잘 뽑히도록 확률을 부여해 6개 번호를 비복원 추출합니다.")

# 버튼
go = st.button("✨ 6개 번호 추출하기", use_container_width=True)

# 상태
if "last_selected" not in st.session_state:
    st.session_state.last_selected = None
if "last_msg" not in st.session_state:
    st.session_state.last_msg = ""

try:
    df = load_excel_from_url(xls_url, usecols="C:I")
    probs = make_inverse_freq_probabilities(df)
except Exception as e:
    st.error(f"❌ 데이터 로딩/계산 실패: {e}")
    st.info("📎 URL / 파일 형식(.xls) / 열 범위(C:I)를 확인하세요.")
else:
    if go:
        try:
            selected = draw_numbers(probs, k=6)   # ✅ 6개 고정
            st.session_state.last_selected = selected
            msg = ""
            if len(probs) < 6:
                msg = f"⚠️ 가능한 고유 값이 {len(probs)}개뿐이라 {len(selected)}개만 추출했습니다."
            st.session_state.last_msg = msg
        except Exception as e:
            st.error(f"❌ 추출 중 오류: {e}")
            st.session_state.last_selected = None
            st.session_state.last_msg = ""

    if st.session_state.last_selected is not None:
        selected = st.session_state.last_selected

        # 원형 뱃지 UI
        circle_html = "".join([
            f"""
            <div style="
                width: 52px; height: 52px; border-radius: 50%;
                background-color: #f7f7f7;
                display: flex; align-items: center; justify-content: center;
                margin: 6px; font-size: 20px; font-weight: 700; color: #000;
                box-shadow: 1px 1px 4px rgba(0,0,0,0.2);
                ">
                {int(num)}
            </div>
            """ for num in selected
        ])

        st.markdown(
            f"""
            <div style="display:flex; justify-content:center; flex-wrap:nowrap; overflow-x:auto; -webkit-overflow-scrolling:touch;">
                {circle_html}
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.last_msg:
            st.info(st.session_state.last_msg)

        # 참고: 희귀(가중치 높음) 상위 10개
        with st.expander("📊 희귀도(가중치) 상위 10개 보기"):
            # 가중치 = 확률 / 최소확률 기준으로 직접 보여줘도 되지만,
            # 여기선 '가중치' 자체를 보여주기 위해 역변환
            weights = probs / probs.min()  # 상대 가중치(최소=1 기준)
            top10 = weights.sort_values(ascending=False).head(10).rename("relative_weight")
            st.dataframe(top10.to_frame())

    else:
        st.info("버튼을 눌러 6개 번호를 뽑아 보세요!")

# 도움말
st.markdown(
    """
    ---
    **도움말**
    - 확률은 **가중치 = 1 / (등장 빈도)** 로 계산합니다.
    - 비복원 추출이라 같은 번호가 중복되지 않습니다.
    - `xlrd`가 필요할 수 있습니다: `pip install xlrd==2.*`
    """
)
