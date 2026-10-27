import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import datetime

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 디자인
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="아이플레이그라운드 - 어린이 이용가능 시설 안내",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS (스타일링)
st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
        color: #FF6B6B;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4ECDC4;
        margin-bottom: 20px;
    }
    .stMetric {
        background-color: #F7F9FA;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
""", unsafe_style_kw=True)


# -----------------------------------------------------------------------------
# 2. 데이터로드 및 캐싱 (가상 데이터 생성)
# -----------------------------------------------------------------------------
@st.cache_data
def load_facility_data():
    """어린이 이용가능 시설 관련 샘플 데이터"""
    data = [
        {
            "시설명": "꿈나무 어린이 도서관",
            "유형": "도서관/문화",
            "주소": "서울특별시 마포구 월드컵북로 21",
            "위도": 37.5568,
            "경도": 126.9238,
            "추천연령": "3세~13세",
            "최소연령": 3,
            "최대연령": 13,
            "입장료": "무료",
            "수유실": True,
            "주차": True,
            "유모차대여": True,
            "운영시간": "09:00 - 18:00 (월요일 휴무)",
            "연락처": "02-123-4567",
            "평점": 4.8
        },
        {
            "시설명": "뽀로로 키즈파크 홍대점",
            "유형": "키즈카페",
            "주소": "서울특별시 마포구 양화로 160",
            "위도": 37.5552,
            "경도": 126.9230,
            "추천연령": "1세~7세",
            "최소연령": 1,
            "최대연령": 7,
            "입장료": "유료 (어린이 20,000원)",
            "수유실": True,
            "주차": True,
            "유모차대여": False,
            "운영시간": "10:00 - 20:00 (연중무휴)",
            "연락처": "02-987-6543",
            "평점": 4.5
        },
        {
            "시설명": "서울 어린이 상상나라",
            "유형": "체험/박물관",
            "주소": "서울특별시 광진구 능동로 216",
            "위도": 37.5495,
            "경도": 127.0815,
            "추천연령": "0세~9세",
            "최소연령": 0,
            "최대연령": 9,
            "입장료": "유료 (4,000원)",
            "수유실": True,
            "주차": True,
            "유모차대여": True,
            "운영시간": "10:00 - 18:00 (월요일 휴무)",
            "연락처": "02-432-1004",
            "평점": 4.9
        },
        {
            "시설명": "연세 아이사랑 소아청소년과의원",
            "유형": "의료/병원",
            "주소": "서울특별시 마포구 신촌로 80",
            "위도": 37.5559,
            "경도": 126.9368,
            "추천연령": "0세~18세",
            "최소연령": 0,
            "최대연령": 18,
            "입장료": "진료비 별도",
            "수유실": True,
            "주차": True,
            "유모차대여": False,
            "운영시간": "08:30 - 19:00",
            "연락처": "02-333-7575",
            "평점": 4.6
        },
        {
            "시설명": "월드컵공원 모험놀이터",
            "유형": "공원/놀이터",
            "주소": "서울특별시 마포구 하늘공원로 86",
            "위도": 37.5638,
            "경도": 126.8948,
            "추천연령": "4세~12세",
            "최소연령": 4,
            "최대연령": 12,
            "입장료": "무료",
            "수유실": False,
            "주차": True,
            "유모차대여": False,
            "운영시간": "24시간 열림",
            "연락처": "02-300-5500",
            "평점": 4.7
        },
        {
            "시설명": "햇살아침 어린이집",
            "유형": "어린이집/유치원",
            "주소": "서울특별시 마포구 성산로 4길 12",
            "위도": 37.5680,
            "경도": 126.9150,
            "추천연령": "0세~5세",
            "최소연령": 0,
            "최대연령": 5,
            "입장료": "보육료 지원",
            "수유실": True,
            "주차": False,
            "유모차대여": False,
            "운영시간": "07:30 - 19:30",
            "연락처": "02-555-1234",
            "평점": 4.8
        }
    ]
    return pd.DataFrame(data)

try:
    df = load_facility_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 3. 사이드바 - 검색 및 필터링
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 맞춤 시설 검색")

# 검색어
search_keyword = st.sidebar.text_input("시설명 또는 주소 검색", placeholder="예: 도서관, 마포구")

# 아이 연령 필터
age = st.sidebar.slider("아이 연령 선택 (세)", min_value=0, max_value=13, value=3)

# 시설 유형 필터
all_categories = list(df["유형"].unique())
selected_categories = st.sidebar.multiselect(
    "시설 유형",
    options=all_categories,
    default=all_categories
)

# 편의시설 필터
st.sidebar.subheader("✨ 편의시설 조건")
need_nursing = st.sidebar.checkbox("수유실 있음")
need_parking = st.sidebar.checkbox("주차 가능")
need_stroller = st.sidebar.checkbox("유모차 대여 가능")

# 필터링 적용 Logic
filtered_df = df[
    (df["최소연령"] <= age) & (df["최대연령"] >= age) &
    (df["유형"].isin(selected_categories))
]

if search_keyword:
    filtered_df = filtered_df[
        filtered_df["시설명"].str.contains(search_keyword, case=False) |
        filtered_df["주소"].str.contains(search_keyword, case=False)
    ]

if need_nursing:
    filtered_df = filtered_df[filtered_df["수유실"] == True]
if need_parking:
    filtered_df = filtered_df[filtered_df["주소"] == True] if "주차" not in filtered_df else filtered_df[filtered_df["주차"] == True]
if need_stroller:
    filtered_df = filtered_df[filtered_df["유모차대여"] == True]


# -----------------------------------------------------------------------------
# 4. 메인 화면 구성
# -----------------------------------------------------------------------------
st.markdown('<p class="main-title">🎈 우리아이 맞춤 시설 안내소</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">아이의 연령과 원하는 조건에 맞는 최적의 시설을 찾아보세요!</p>', unsafe_allow_html=True)

# 주요 지표 (Metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("검색된 시설", f"{len(filtered_df)}개")
col2.metric("선택한 연령", f"만 {age}세")
col3.metric("무료 이용 시설", f"{len(filtered_df[filtered_df['입장료'] == '무료'])}개")
col4.metric("수유실 보유 시설", f"{len(filtered_df[filtered_df['수유실'] == True])}개")

st.markdown("---")

# 탭 구성 (지도 보기 / 목록 보기 / 방문/예약 신청)
tab1, tab2, tab3 = st.tabs(["🗺️ 지도 보기", "📋 시설 목록 & 상세정보", "📅 방문/체험 신청"])

# TAB 1: Folium 지도 시각화
with tab1:
    st.subheader("📍 내 주변 시설 위치 보기")
    
    if filtered_df.empty:
        st.info("조건에 맞는 시설이 없습니다. 필터를 조정해 주세요.")
    else:
        # 지도 중심 설정 (데이터의 평균 위도/경도)
        start_lat = filtered_df["위도"].mean()
        start_lng = filtered_df["경도"].mean()
        
        m = folium.Map(location=[start_lat, start_lng], zoom_start=13)
        
        # 마커 아이콘 색상 매핑
        color_dict = {
            "도서관/문화": "blue",
            "키즈카페": "red",
            "체험/박물관": "orange",
            "의료/병원": "green",
            "공원/놀이터": "purple",
            "어린이집/유치원": "cadetblue"
        }

        for _, row in filtered_df.iterrows():
            popup_html = f"""
            <div style="width:180px">
                <b>{row['시설명']}</b><br>
                유형: {row['유형']}<br>
                추천연령: {row['추천연령']}<br>
                평점: ⭐{row['평점']}
            </div>
            """
            folium.Marker(
                location=[row["위도"], row["경도"]],
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=row["시설명"],
                icon=folium.Icon(color=color_dict.get(row["유형"], "gray"), icon="info-sign")
            ).add_to(m)

        # Streamlit에 지도 출력
        st_folium(m, width="100%", height=450)


# TAB 2: 목록 및 상세 정보
with tab2:
    st.subheader("📋 시설 목록")
    
    if filtered_df.empty:
        st.warning("조건에 만족하는 시설이 없습니다.")
    else:
        for idx, row in filtered_df.iterrows():
            with st.expander(f"[{row['유형']}] {row['시설명']} (⭐ {row['평점']})"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.write(f"**📍 주소:** {row['주소']}")
                    st.write(f"**👶 추천 연령:** {row['추천연령']}")
                    st.write(f"**⏰ 운영 시간:** {row['운영시간']}")
                    st.write(f"**📞 연락처:** {row['연락처']}")
                    st.write(f"**💰 입장료/비용:** {row['입장료']}")
                with c2:
                    st.write("**✨ 편의시설 여부**")
                    st.write(f"- 수유실: {'✅ 있음' if row['수유실'] else '❌ 없음'}")
                    st.write(f"- 주차 공간: {'✅ 가능' if row['주차'] else '❌ 불가'}")
                    st.write(f"- 유모차 대여: {'✅ 가능' if row['유모차대여'] else '❌ 불가'}")


# TAB 3: 예약 및 상담 신청 (시뮬레이션 기능)
with tab3:
    st.subheader("📅 시설 방문 및 프로그램 예약 신청")
    st.write("방문하고 싶은 시설을 선택하여 간편하게 상담 및 예약을 신청해보세요.")

    with st.form("booking_form"):
        selected_facility = st.selectbox("시설 선택", filtered_df["시설명"].tolist() if not filtered_df.empty else ["선택 가능한 시설 없음"])
        parent_name = st.text_input("보호자 성함")
        phone_number = st.text_input("연락처 (예: 010-1234-5678)")
        visit_date = st.date_input("방문 희망일", datetime.date.today())
        num_children = st.number_input("동반 어린이 수", min_value=1, max_value=10, value=1)
        memo = st.text_area("기타 요청사항 (예: 유모차 보관 요청 등)")

        submitted = st.form_submit_button("신청하기")

        if submitted:
            if not parent_name or not phone_number:
                st.error("보호자 성함과 연락처를 반드시 입력해주세요.")
            elif selected_facility == "선택 가능한 시설 없음":
                st.error("신청할 시설을 선택해 주세요.")
            else:
                st.success(f"🎉 성공적으로 신청되었습니다!\n\n"
                           f"- **시설:** {selected_facility}\n"
                           f"- **신청자:** {parent_name}님\n"
                           f"- **방문일:** {visit_date}\n"
                           f"- **어린이 수:** {num_children}명\n\n"
                           f"시설 담당자가 입력하신 연락처({phone_number})로 확인 안내를 드릴 예정입니다.")
