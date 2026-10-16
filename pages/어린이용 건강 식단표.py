
import random
import streamlit as st

st.set_page_config(
    page_title="튼튼 키즈 건강 키오스크",
    page_icon="🍎",
    layout="wide",
)

# 요일별 건강 식단
MEALS = {
    "월요일": {
        "🌞 아침": ["현미밥", "달걀찜", "김", "바나나"],
        "☀️ 점심": ["잡곡밥", "닭고기구이", "브로콜리", "미역국"],
        "🌙 저녁": ["두부채소덮밥", "콩나물국", "방울토마토"],
        "🍓 간식": ["플레인 요거트", "사과"],
    },
    "화요일": {
        "🌞 아침": ["통밀 토스트", "우유 또는 두유", "딸기"],
        "☀️ 점심": ["기장밥", "소고기채소볶음", "시금치나물", "된장국"],
        "🌙 저녁": ["고등어구이", "밥", "양배추샐러드", "감자국"],
        "🍓 간식": ["찐 고구마", "귤"],
    },
    "수요일": {
        "🌞 아침": ["오트밀", "우유 또는 두유", "바나나"],
        "☀️ 점심": ["밥", "돼지고기수육", "상추와 오이", "맑은 국"],
        "🌙 저녁": ["채소 달걀볶음밥", "두부구이", "배"],
        "🍓 간식": ["치즈", "방울토마토"],
    },
    "목요일": {
        "🌞 아침": ["밥", "김", "두부부침", "사과"],
        "☀️ 점심": ["잡곡밥", "닭볶음", "당근과 애호박", "미역국"],
        "🌙 저녁": ["잔치국수", "삶은 달걀", "오이무침"],
        "🍓 간식": ["플레인 요거트", "블루베리"],
    },
    "금요일": {
        "🌞 아침": ["통밀 샌드위치", "달걀", "토마토"],
        "☀️ 점심": ["현미밥", "연어구이", "브로콜리", "된장국"],
        "🌙 저녁": ["소고기채소주먹밥", "두부국", "귤"],
        "🍓 간식": ["옥수수", "우유 또는 두유"],
    },
    "토요일": {
        "🌞 아침": ["채소 달걀말이", "밥", "키위"],
        "☀️ 점심": ["닭고기채소볶음밥", "오이와 당근", "과일"],
        "🌙 저녁": ["두부채소전", "밥", "무국"],
        "🍓 간식": ["바나나", "플레인 요거트"],
    },
    "일요일": {
        "🌞 아침": ["고구마", "달걀", "우유 또는 두유", "딸기"],
        "☀️ 점심": ["잡곡밥", "불고기", "상추", "콩나물국"],
        "🌙 저녁": ["채소 카레", "밥", "양배추샐러드"],
        "🍓 간식": ["배", "치즈"],
    },
}

# 어린이 친화적 디자인
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

html, body, [class*="css"] {
    font-family: 'Jua', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #fff7df, #eaffef);
}

.hero {
    background: linear-gradient(120deg, #ffe078, #ffb9ce);
    padding: 25px;
    border-radius: 25px;
    text-align: center;
    color: #594333;
    margin-bottom: 20px;
}

.meal-card {
    background: white;
    padding: 20px;
    border-radius: 22px;
    border: 3px solid #dff0d7;
    box-shadow: 0 4px 0 #d0e5c6;
    margin-bottom: 15px;
    min-height: 175px;
}

.meal-card h3 {
    color: #39734b;
}

div.stButton > button {
    border-radius: 15px;
    min-height: 45px;
    background-color: white;
    border: 2px solid #d8ebce;
    color: #315b3a;
}
</style>
""", unsafe_allow_html=True)

if "day" not in st.session_state:
    st.session_state.day = "월요일"

if "checked" not in st.session_state:
    st.session_state.checked = set()

if "menu_version" not in st.session_state:
    st.session_state.menu_version = {}

st.markdown("""
<div class="hero">
    <h1>🍎 튼튼 키즈 건강 키오스크 🥦</h1>
    <h3>골고루 먹고 튼튼하게 자라요!</h3>
    <p>요일을 선택하고 오늘의 맛있는 건강 식단을 확인해 봐요.</p>
</div>
""", unsafe_allow_html=True)

st.subheader("🗓️ 무슨 요일의 식단을 볼까요?")

days = list(MEALS.keys())
cols = st.columns(7)

for i, day in enumerate(days):
    with cols[i]:
        if st.button(day[:1], key=f"day_{day}", help=day,
                     use_container_width=True):
            st.session_state.day = day

day = st.session_state.day

st.markdown(f"## 🌈 {day} 건강 식단")
st.caption("아래 식단은 건강한 식생활을 배우기 위한 예시예요.")

# 식단 변경용 대안 메뉴
ALTERNATIVES = {
    "🌞 아침": [
        ["밥", "두부부침", "김", "귤"],
        ["오트밀", "바나나", "플레인 요거트"],
        ["통밀 토스트", "달걀", "사과"],
    ],
    "☀️ 점심": [
        ["잡곡밥", "닭고기구이", "브로콜리", "맑은 국"],
        ["밥", "두부조림", "시금치나물", "과일"],
        ["현미밥", "생선구이", "채소볶음", "미역국"],
    ],
    "🌙 저녁": [
        ["채소볶음밥", "달걀찜", "방울토마토"],
        ["두부채소덮밥", "맑은 국", "배"],
        ["밥", "닭고기채소볶음", "오이무침"],
    ],
    "🍓 간식": [
        ["사과", "치즈"],
        ["바나나", "플레인 요거트"],
        ["찐 고구마", "귤"],
    ],
}

if day not in st.session_state.menu_version:
    st.session_state.menu_version[day] = MEALS[day].copy()

menu = st.session_state.menu_version[day]

# 아침, 점심, 저녁, 간식 카드
meal_cols = st.columns(2)

for i, (meal, foods) in enumerate(menu.items()):
    with meal_cols[i % 2]:
        food_text = "".join(f"<p>🥗 {food}</p>" for food in foods)

        st.markdown(f"""
        <div class="meal-card">
            <h3>{meal}</h3>
            {food_text}
        </div>
        """, unsafe_allow_html=True)

        check_key = f"{day}_{meal}"
        is_checked = check_key in st.session_state.checked

        checked = st.checkbox(
            f"{meal} 먹었어요!",
            value=is_checked,
            key=f"check_{check_key}",
        )

        if checked:
            st.session_state.checked.add(check_key)
        else:
            st.session_state.checked.discard(check_key)

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("🎲 다른 식단 추천받기", use_container_width=True):
        try:
            st.session_state.menu_version[day] = {
                meal: random.choice(ALTERNATIVES[meal])
                for meal in MEALS[day]
            }
            st.rerun()
        except (KeyError, IndexError, TypeError):
            st.error("식단을 변경하지 못했어요. 다시 눌러 주세요.")

with col2:
    if st.button("🔄 기본 식단으로 돌아가기",
                 use_container_width=True):
        st.session_state.menu_version[day] = MEALS[day].copy()
        st.rerun()

st.divider()

# 식사 체크 현황
st.subheader("⭐ 나의 건강 식사 탐험")

meal_names = list(MEALS[day].keys())
done = sum(
    f"{day}_{meal}" in st.session_state.checked
    for meal in meal_names
)

st.progress(done / len(meal_names))
st.write(f"오늘 식사 체크: **{done}/{len(meal_names)}개**")

if done == len(meal_names):
    st.success("🎉 멋져요! 오늘의 식사 탐험을 모두 완료했어요!")

# 간단한 식품군 교육
st.subheader("🥦 건강 음식 탐험")

st.info(
    "🍚 곡류: 밥, 빵, 국수\n\n"
    "🥚 단백질 식품: 달걀, 고기, 생선, 두부\n\n"
    "🥦 채소: 브로콜리, 당근, 시금치\n\n"
    "🍎 과일: 사과, 바나나, 딸기"
)

with st.expander("⚠️ 알레르기 안전 안내"):
    st.warning(
        "식단에는 달걀, 우유, 콩, 밀, 생선 등 알레르기 유발 식품이 "
        "포함될 수 있어요. 먹기 전에 보호자와 재료 및 제품 표시를 "
        "확인해 주세요. 알레르기가 있다면 해당 식품을 먹지 말고 "
        "보호자나 영양사와 대체 식품을 정해 주세요."
    )

st.markdown("---")
st.markdown(
    "<center>💚 튼튼 키즈 건강 키오스크 · 맛있게 먹고 신나게 놀아요!</center>",
    unsafe_allow_html=True,
)

st.caption(
    "이 앱은 식생활 교육용 예시이며, 개인별 영양 상담이나 "
    "실제 급식 메뉴를 대신하지 않습니다."
)

