
import random
import streamlit as st

# ---------------------------------
# 기본 설정
# ---------------------------------
st.set_page_config(
    page_title="몽글몽글 놀이터 ☁️",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------
# 스타일
# ---------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&family=Noto+Sans+KR:wght@400;500;700&display=swap');

    :root {
        --ink: #554F70;
        --pink: #FFE5F0;
        --blue: #E5F2FF;
        --yellow: #FFF5CF;
        --green: #E8F7E7;
        --purple: #F0E8FF;
    }

    html, body, [class*="css"] {
        font-family: 'Noto Sans KR', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 5% 5%, #FFF0F6 0, transparent 30%),
            radial-gradient(ellipse at 95% 20%, #E7F4FF 0, transparent 30%),
            linear-gradient(180deg, #FFFCFF 0%, #F7F7FF 55%, #FFFDF5 100%);
        color: var(--ink);
    }

    .block-container {
        max-width: 1050px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3 {
        font-family: 'Jua', sans-serif !important;
        color: var(--ink) !important;
    }

    .hero {
        background: linear-gradient(135deg, #FFE8F2, #E9E9FF 55%, #E2F6FF);
        border: 2px solid rgba(255,255,255,.9);
        border-radius: 32px;
        padding: 34px 28px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(117, 104, 161, .09);
        position: relative;
        overflow: hidden;
    }

    .hero-bubble {
        display: inline-block;
        background: rgba(255,255,255,.78);
        border-radius: 30px;
        padding: 7px 15px;
        color: #8276A7;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero-title {
        font-family: 'Jua', sans-serif;
        font-size: clamp(34px, 6vw, 54px);
        line-height: 1.3;
        color: #665781;
        margin: 5px 0 10px;
    }

    .hero-desc {
        color: #776E91;
        font-size: 16px;
        line-height: 1.8;
        margin-bottom: 10px;
    }

    .cloud-deco {
        font-size: 25px;
        letter-spacing: 8px;
        margin: 8px 0;
    }

    .section-label {
        color: #9A8BB7;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 2px;
        margin-bottom: 3px;
    }

    .soft-card {
        height: 100%;
        border-radius: 24px;
        padding: 22px 20px;
        border: 2px solid rgba(255,255,255,.95);
        box-shadow: 0 7px 22px rgba(100, 90, 140, .06);
        color: #5E5878;
    }

    .soft-card .emoji {
        font-size: 38px;
        margin-bottom: 10px;
    }

    .soft-card .card-title {
        font-family: 'Jua', sans-serif;
        font-size: 22px;
        margin-bottom: 8px;
    }

    .soft-card .card-desc {
        font-size: 14px;
        line-height: 1.75;
    }

    .pink { background: #FFF0F5; }
    .blue { background: #EDF6FF; }
    .yellow { background: #FFF8DF; }
    .green { background: #EDF8E9; }
    .purple { background: #F2ECFF; }

    .mini-pill {
        display: inline-block;
        background: rgba(255,255,255,.8);
        border-radius: 20px;
        padding: 5px 11px;
        font-size: 12px;
        color: #85769F;
        margin-top: 12px;
    }

    .mission-box {
        background: linear-gradient(120deg, #FFF4D9, #FFF0F6);
        border: 2px dashed #F2C9D9;
        border-radius: 25px;
        padding: 24px;
        text-align: center;
    }

    .mission-text {
        font-family: 'Jua', sans-serif;
        font-size: 24px;
        color: #756183;
        line-height: 1.6;
    }

    .result-box {
        background: #FFFFFF;
        border: 2px solid #EEE5FF;
        border-radius: 20px;
        padding: 18px;
        text-align: center;
        margin-top: 12px;
        color: #665B82;
        line-height: 1.8;
    }

    div.stButton > button {
        border: 0;
        border-radius: 18px;
        background: linear-gradient(100deg, #F5D9EC, #E5DFFF);
        color: #66577D;
        font-weight: 700;
        min-height: 45px;
        transition: transform .15s ease;
    }

    div.stButton > button:hover {
        border: 0;
        color: #514466;
        transform: translateY(-2px);
        background: linear-gradient(100deg, #FBE0F0, #E9E2FF);
    }

    div[data-baseweb="select"] > div {
        border-radius: 15px;
        border-color: #E8DFF6;
        background: rgba(255,255,255,.8);
    }

    div[data-testid="stAlert"] {
        border-radius: 16px;
    }

    .footer {
        text-align: center;
        color: #A49AB7;
        font-size: 13px;
        line-height: 2;
        padding: 25px 10px 5px;
    }

    @media (max-width: 600px) {
        .hero {
            padding: 26px 16px;
            border-radius: 25px;
        }
        .soft-card {
            padding: 17px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------
# 데이터
# ---------------------------------
MISSIONS = [
    "주변에서 동그란 물건 3개를 찾아봐요! 🔵",
    "하늘을 보고 구름 모양을 상상해 봐요! ☁️",
    "가족이나 친구에게 고마운 말을 전해요! 💗",
    "좋아하는 색으로 작은 그림을 그려봐요! 🎨",
    "동물처럼 움직이며 10초 동안 놀아봐요! 🐰",
    "오늘 재미있었던 일을 한 가지 떠올려 봐요! 🌷",
    "눈을 감고 들리는 소리 3가지를 찾아봐요! 👂",
    "종이 위에 나만의 상상 속 친구를 그려봐요! 🦄",
    "기지개를 쭉 펴고 깊게 숨을 쉬어봐요! 🌈",
    "주변에 있는 작은 친절 한 가지를 실천해 봐요! ✨",
]

MOOD_ACTIVITIES = {
    "😊 신나요": (
        "🎈 신나는 몸놀이",
        "좋아하는 노래에 맞춰 춤을 추거나 동물 흉내를 내봐요!"
    ),
    "😴 졸려요": (
        "🌙 구름 휴식 시간",
        "편안하게 앉아서 천천히 숨을 쉬고 포근한 구름을 상상해 봐요."
    ),
    "🥺 조금 속상해요": (
        "🧸 마음 토닥토닥",
        "지금 마음을 색깔로 표현해 보거나 믿을 수 있는 어른에게 이야기해 봐요."
    ),
    "🤔 궁금해요": (
        "🔎 꼬마 탐험가",
        "주변에서 처음 보는 물건 하나를 찾아 모양과 쓰임을 관찰해 봐요!"
    ),
    "🥰 행복해요": (
        "💌 행복 나누기",
        "오늘 행복했던 순간을 떠올리고 누군가에게 따뜻한 말을 건네봐요."
    ),
}

WORLDS = [
    {
        "emoji": "🌈",
        "title": "무지개 구름섬",
        "desc": "알록달록한 색깔을 찾아보고 나만의 무지개를 상상해요.",
        "tag": "상상력 쑥쑥",
        "color": "pink",
    },
    {
        "emoji": "🔭",
        "title": "반짝 별나라",
        "desc": "별과 달, 신기한 우주에 대해 궁금한 것을 생각해 봐요.",
        "tag": "호기심 반짝",
        "color": "blue",
    },
    {
        "emoji": "🐰",
        "title": "토끼 풀밭",
        "desc": "작은 생명과 자연을 관찰하고 다정한 마음을 키워요.",
        "tag": "자연과 친구",
        "color": "green",
    },
    {
        "emoji": "🎨",
        "title": "말랑 미술방",
        "desc": "색칠하고 그리고 새로운 이야기를 마음껏 만들어 봐요.",
        "tag": "창의력 몽글",
        "color": "purple",
    },
]

# ---------------------------------
# 세션 상태 초기화
# ---------------------------------
if "mission" not in st.session_state:
    st.session_state.mission = random.choice(MISSIONS)

if "completed_missions" not in st.session_state:
    st.session_state.completed_missions = 0

if "favorite_worlds" not in st.session_state:
    st.session_state.favorite_worlds = []

if "last_mission" not in st.session_state:
    st.session_state.last_mission = ""

# ---------------------------------
# 헤더
# ---------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="cloud-deco">☁️ ✨ ☁️</div>
        <div class="hero-bubble">WELCOME TO MONGLE WORLD</div>
        <div class="hero-title">몽글몽글 놀이터</div>
        <div class="hero-desc">
            작은 상상이 커다란 모험이 되는 곳!<br>
            오늘은 어떤 즐거운 일이 기다리고 있을까요?
        </div>
        <div class="cloud-deco">🌈 ⭐ 🦄 ⭐ 🌈</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# ---------------------------------
# 오늘의 인사
# ---------------------------------
st.markdown(
    '<div class="section-label">TODAY\'S LITTLE MOMENT</div>',
    unsafe_allow_html=True,
)
st.subheader("안녕, 꼬마 친구! 💗")
st.write("오늘의 마음을 살짝 알려주면 어울리는 놀이를 추천해 줄게요.")

mood = st.selectbox(
    "지금 어떤 기분인가요?",
    options=list(MOOD_ACTIVITIES.keys()),
    index=0,
    key="today_mood",
)

activity_title, activity_desc = MOOD_ACTIVITIES[mood]

st.markdown(
    f"""
    <div class="result-box">
        <div style="font-size:35px;">💌</div>
        <div style="font-size:21px;font-weight:700;">{activity_title}</div>
        <div>{activity_desc}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.divider()

# ---------------------------------
# 놀이 세계
# ---------------------------------
st.markdown(
    '<div class="section-label">LITTLE DREAM WORLDS</div>',
    unsafe_allow_html=True,
)
st.subheader("어디로 놀러 갈까요? 🧸")
st.write("마음에 드는 세계를 골라 나만의 작은 모험을 시작해요.")

columns = st.columns(2, gap="medium")

for index, world in enumerate(WORLDS):
    with columns[index % 2]:
        st.markdown(
            f"""
            <div class="soft-card {world['color']}">
                <div class="emoji">{world['emoji']}</div>
                <div class="card-title">{world['title']}</div>
                <div class="card-desc">{world['desc']}</div>
                <div class="mini-pill">{world['tag']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        world_name = world["title"]
        is_favorite = world_name in st.session_state.favorite_worlds
        button_label = (
            f"💖 {world_name} 찜 해제"
            if is_favorite
            else f"✨ {world_name} 찜하기"
        )

        if st.button(
            button_label,
            key=f"world_{index}",
            use_container_width=True,
        ):
            if is_favorite:
                st.session_state.favorite_worlds.remove(world_name)
                st.toast("찜 목록에서 뺐어요!")
            else:
                st.session_state.favorite_worlds.append(world_name)
                st.toast("좋아하는 세계에 추가했어요! 💗")

            st.rerun()

        st.write("")

# ---------------------------------
# 오늘의 몽글 미션
# ---------------------------------
st.divider()
st.markdown(
    '<div class="section-label">TODAY\'S CLOUD MISSION</div>',
    unsafe_allow_html=True,
)
st.subheader("몽글 미션에 도전해 봐요! ☁️")

st.markdown(
    f"""
    <div class="mission-box">
        <div style="font-size:40px;">🪄</div>
        <div class="mission-text">{st.session_state.mission}</div>
        <div style="color:#A28EA9;font-size:13px;margin-top:8px;">
            천천히 해도 괜찮아요. 즐겁게 도전해 봐요!
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2 = st.columns(2)

with col1:
    if st.button("🎲 새 미션 뽑기", use_container_width=True):
        try:
            choices = [
                mission
                for mission in MISSIONS
                if mission != st.session_state.mission
            ]
            st.session_state.mission = random.choice(
                choices if choices else MISSIONS
            )
            st.rerun()
        except (IndexError, ValueError):
            st.warning("미션을 다시 준비하고 있어요. 한 번 더 눌러주세요.")

with col2:
    if st.button("🌟 미션 완료!", use_container_width=True):
        st.session_state.completed_missions += 1
        st.balloons()
        st.success("참 잘했어요! 오늘도 멋진 도전을 해냈어요! 💖")

st.write("")

# ---------------------------------
# 나의 작은 기록
# ---------------------------------
st.markdown(
    '<div class="section-label">MY LITTLE COLLECTION</div>',
    unsafe_allow_html=True,
)
st.subheader("나의 몽글 기록 📒")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="soft-card yellow" style="text-align:center;">
            <div class="emoji">🏆</div>
            <div class="card-title">완료한 미션</div>
            <div style="font-size:34px;font-weight:700;">
                {st.session_state.completed_missions}
            </div>
            <div class="card-desc">작은 도전도 멋진 일이에요!</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    favorite_count = len(st.session_state.favorite_worlds)
    st.markdown(
        f"""
        <div class="soft-card pink" style="text-align:center;">
            <div class="emoji">💝</div>
            <div class="card-title">좋아하는 세계</div>
            <div style="font-size:34px;font-weight:700;">
                {favorite_count}
            </div>
            <div class="card-desc">내가 고른 특별한 놀이터</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if st.session_state.favorite_worlds:
    st.write("내가 찜한 세계:")
    st.write(" · ".join(st.session_state.favorite_worlds))
else:
    st.info("마음에 드는 놀이 세계를 찜하면 여기에 모여요!")

# ---------------------------------
# 푸터
# ---------------------------------
st.markdown(
    """
    <div class="footer">
        ☁️ 몽글몽글 놀이터 ☁️<br>
        작은 꿈도 소중하게, 매일매일 행복하게!<br>
        <span style="font-size:11px;">
            안전하고 즐거운 어린이의 상상 공간
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
