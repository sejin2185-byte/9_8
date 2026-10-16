
import random
import streamlit as st

st.set_page_config(
    page_title="튼튼 키즈 건강 키오스크",
    page_icon="🍎",
    layout="wide",
)

# 건강식 메뉴 목록
FOOD_OPTIONS = {
    "🌞 아침": [
        ["현미밥", "달걀찜", "바나나"],
        ["통밀 토스트", "삶은 달걀", "딸기"],
        ["오트밀", "우유 또는 두유", "사과"],
        ["고구마", "두부부침", "귤"],
        ["채소달걀말이", "밥", "키위"],
        ["통밀 샌드위치", "토마토", "우유 또는 두유"],
        ["밥", "김", "두부", "배"],
    ],
    "☀️ 점심": [
        ["닭고기구이", "잡곡밥", "브로콜리", "미역국"],
        ["소고기채소볶음", "기장밥", "된장국"],
        ["돼지고기수육", "밥", "상추", "오이"],
        ["닭고기채소볶음밥", "당근", "오이"],
        ["연어구이", "현미밥", "브로콜리"],
        ["불고기", "잡곡밥", "상추", "콩나물국"],
        ["두부조림", "밥", "시금치나물", "맑은 국"],
    ],
    "🌙 저녁": [
        ["두부채소덮밥", "콩나물국"],
        ["고등어구이", "밥", "양배추샐러드"],
        ["채소달걀볶음밥", "두부구이"],
        ["잔치국수", "삶은 달걀", "오이무침"],
        ["소고기채소주먹밥", "두부국"],
        ["두부채소전", "밥", "무국"],
        ["채소카레", "밥", "양배추샐러드"],
    ],
    "🍓 간식": [
        ["사과", "플레인 요거트"],
        ["찐 고구마", "귤"],
        ["치즈", "방울토마토"],
        ["플레인 요거트", "블루베리"],
        ["옥수수", "바나나"],
        ["배", "치즈"],
        ["바나나", "플레인 요거트"],
        ["딸기", "우유 또는 두유"],
    ],
}

# 디자인
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

html, body, [class*="css"] {
    font-family: 'Jua', sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #fff8df, #eaffef);
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

# 상태 초기화
if "day" not in st.session_state:
    st.session_state.day = "월요일"

if "menus" not in st.session_state:
    st.session_state.menus = {}

if "checked" not in st.session_state:
    st.session_state.checked = set()

# 랜덤 식단 생성
def make_random_menu():
    return {
        meal: random.choice(options).copy()
        for meal, options in FOOD_OPTIONS.items()
    }

# 처음 실행할 때 요일별 식단 생성
for day_name in [
    "월요일", "화요일", "수요일", "목요일",
    "금요일", "토요일", "일요일"
]:
    if day_name not in st.session_state.menus:
        st.session_state.menus[day_name] = make_random_menu()

# 제목
st.markdown("""
<div class="hero">
    <h1>🍎 튼튼 키즈 건강 키오스크 🥦</h1>
    <h3>오늘은 어떤 건강 음식이 나올까요?</h3>
    <p>요일을 고르고 나만의 건강 식단을 확인해 봐요!</p>
</div>
""", unsafe_allow_html=True)

# 요일 선택
st.subheader("🗓️ 요일을 선택하세요!")

days = [
    "월요일", "화요일", "수요일", "목요일",
    "금요일", "토요일", "일요일"
]

cols = st.columns(7)

for i, day_name in enumerate(days):
    with cols[i]:
        if st.button(
            day_name[:1],
            key=f"day_{day_name}",
            help=day_name,
            use_container_width=True,
        ):
            st.session_state.day = day_name

day = st.session_state.day
menu = st.session_state.menus[day]

st.markdown(f"## 🌈 {day} 랜덤 건강 식단")
st.caption("매일 새로운 건강 메뉴를 추천받을 수 있어요!")

# 식단 카드 표시
meal_cols = st.columns(2)

for i, (meal_name, foods) in enumerate(menu.items()):
    with meal_cols[i % 2]:
        food_text = "".join(
            f"<p>🥗 {food}</p>" for food in foods
        )

        st.markdown(
            f"""
            <div class="meal-card">
                <h3>{meal_name}</h3>
                {food_text}
            </div>
            """,
            unsafe_allow_html=True,
        )

        check_key = f"{day}_{meal_name}"

        checked = st.checkbox(
            f"{meal_name} 먹었어요!",
            value=check_key in st.session_state.checked,
            key=f"check_{check_key}",
        )

        if checked:
            st.session_state.checked.add(check_key)
        else:
            st.session_state.checked.discard(check_key)

st.divider()

# 랜덤 추천 버튼
if st.button("🎲 새로운 건강 식단 뽑기!", use_container_width=True):
    try:
        st.session_state.menus[day] = make_random_menu()

        # 새 식단을 뽑으면 해당 요일의 체크 초기화
        for meal_name in FOOD_OPTIONS:
            st.session_state.checked.discard(
                f"{day}_{meal_name}"
            )

        st.rerun()

    except (KeyError, IndexError, TypeError):
        st.error("식단을 만들지 못했어요. 다시 시도해 주세요.")

# 건강 음식 안내
st.divider()
st.subheader("🥦 건강 음식 탐험")

food_cols = st.columns(4)

food_groups = [
    ("🍚 곡류", "밥, 빵, 국수"),
    ("🥚 단백질", "달걀, 고기, 생선, 두부"),
    ("🥦 채소", "브로콜리, 당근, 시금치"),
    ("🍎 과일", "사과, 바나나, 딸기"),
]

for i, (title, description) in enumerate(food_groups):
    with food_cols[i]:
        st.markdown(f"### {title}")
        st.write(description)

with st.expander("⚠️ 알레르기 안전 안내"):
    st.warning(
        "메뉴에는 달걀, 우유, 콩, 밀, 생선 등 알레르기 유발 식품이 "
        "포함될 수 있어요. 먹기 전에 보호자와 재료 및 제품 표시를 "
        "확인해 주세요."
    )

st.markdown("---")
st.markdown(
    "<center>💚 튼튼 키즈 건강 키오스크 · 골고루 먹고 튼튼하게!</center>",
    unsafe_allow_html=True,
)

st.caption(
    "이 식단은 교육용 예시입니다. 실제 영양 상태와 알레르기에 맞게 "
    "보호자 또는 영양사와 메뉴를 조정해 주세요."
)


