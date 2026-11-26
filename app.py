
import streamlit as st

st.set_page_config(
    page_title="태양전지 발전량 시뮬레이터",
    page_icon="☀️",
    layout="centered"
)

# 1. 리스트 자료구조 사용
materials = [
    ["단결정 실리콘", 22.0],
    ["다결정 실리콘", 18.0],
    ["비정질 실리콘", 10.0],
    ["페로브스카이트", 25.0],
    ["CdTe (카드뮴 텔루라이드)", 19.0],
    ["CIGS", 18.0]
]

# 2. 함수 사용: 발전량 계산
def calculate_energy(area, irradiance, hours, efficiency):
    energy = area * irradiance * hours * efficiency / 100 / 1000
    return energy

# 3. 함수 사용: 효율 등급 판정
def get_grade(efficiency):
    if efficiency < 10:
        return "낮음", "#ff4b4b"
    elif efficiency < 15:
        return "보통", "#ff914d"
    elif efficiency < 20:
        return "양호", "#e6c229"
    elif efficiency < 25:
        return "높음", "#21a366"
    else:
        return "매우 높음", "#3186e8"

# 제목
st.title("☀️ 태양전지 발전량 시뮬레이터")
st.write("소재에 따른 태양전지의 전기 생산량을 확인해 보세요.")

st.divider()

# 4. for 반복문 사용: 소재 목록 만들기
st.subheader("① 소재 선택")

options = []

for material in materials:
    options.append(material[0])

options.append("나만의 소재 만들기")

selected = st.selectbox(
    "태양전지 소재를 선택하세요.",
    options
)

# 5. if 조건문 사용: 소재에 따른 입력
if selected == "나만의 소재 만들기":

    material_name = st.text_input(
        "새로운 소재 이름",
        "나만의 태양전지"
    )

    efficiency = st.slider(
        "발전 효율 (%)",
        0.1, 40.0, 20.0, 0.1
    )

    description = st.text_input(
        "소재 특징",
        "직접 설계한 가상의 태양전지 소재"
    )

else:
    material_name = selected

    # for문을 이용해 선택한 소재의 효율 찾기
    for material in materials:
        if material[0] == selected:
            efficiency = material[1]

st.divider()

# 태양전지 면적
st.subheader("② 태양전지 면적 선택")

area = st.slider(
    "태양전지 면적 (㎡)",
    0.1, 10.0, 1.0, 0.1
)

st.divider()

# 일사량
st.subheader("③ 일사량 선택")

irradiance = st.slider(
    "태양광 일사량 (W/㎡)",
    100, 1200, 800, 50
)

sun_hours = 5

st.info("하루 유효 발전 시간은 5시간으로 설정했습니다.")

st.divider()

# 결과 확인
if st.button("📊 결과 확인하기", use_container_width=True):

    # 함수 호출
    energy = calculate_energy(
        area, irradiance, sun_hours, efficiency
    )

    st.session_state.result = {
        "name": material_name,
        "efficiency": efficiency,
        "energy": energy,
        "area": area,
        "irradiance": irradiance
    }

# 결과 출력
if "result" in st.session_state:

    r = st.session_state.result

    st.divider()
    st.header("📊 분석 결과")

    st.write(f"**선택한 소재: {r['name']}**")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "하루 에너지 생산량",
            f"{r['energy']:.3f} kWh"
        )

    with col2:
        st.metric(
            "태양광-전기 변환 효율",
            f"{r['efficiency']:.1f}%"
        )

    # 함수 호출: 효율 등급 확인
    grade, color = get_grade(r["efficiency"])

    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:25px;
            border-radius:15px;
            text-align:center;
            color:white;
        ">
            <h1 style="color:white;">
                {r['efficiency']:.1f}%
            </h1>
            <h3 style="color:white;">
                {grade}
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🔎 계산 조건")

    st.write(f"- 소재: {r['name']}")
    st.write(f"- 면적: {r['area']}㎡")
    st.write(f"- 일사량: {r['irradiance']}W/㎡")
    st.write(f"- 하루 유효 발전 시간: {sun_hours}시간")

    st.subheader("🧮 계산 공식")

    st.latex(
        r"E = \frac{A \times I \times T \times \eta}{1000}"
    )

    st.caption(
        "※ 소재별 발전 효율은 비교를 위한 예시값입니다. "
        "실제 발전량은 날씨, 온도, 설치 방향 및 발전 손실에 따라 달라집니다."
    )
