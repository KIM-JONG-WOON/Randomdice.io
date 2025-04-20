import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 엑셀 파일 읽기 (시트 이름이 없으면 첫 번째 시트를 읽음)
df = pd.read_excel('NUM_Ro.xlsx', usecols="C:I")  # 엑셀 파일명 변경 필요


# 2. 숫자 데이터만 추출하고 1차원으로 변환
numeric_data = df.select_dtypes(include='number').stack().dropna()

# 3. 숫자별 빈도수 → 퍼센트 비율
value_counts = numeric_data.value_counts()
percentages = (value_counts / value_counts.sum()) * 100

# 4. 확률 분포로 변환 (합이 1이 되도록)
probabilities = percentages / 100

# 5. 확률 기반으로 7개 번호 추출 (중복 없이)
selected_numbers = np.random.choice(
    probabilities.index,       # 후보 숫자들
    size=7,                    # 7개 추출
    replace=False,             # 중복 없이
    p=probabilities.values     # 확률 분포 적용
)

# 6. 결과 출력
print("빈도 비율 기반으로 추출된 7개 번호:")
print(selected_numbers)