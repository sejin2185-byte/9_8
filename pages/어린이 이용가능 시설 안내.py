import streamlit as st
import pandas as pd
import datetime

# -----------------------------------------------------------------------------
# 1단계: 페이지 기본 설정 및 디자인
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="어린이 이용가능 시설 & 안심케어 지도",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 2.1rem;
        color: #FF6B6B;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4ECDC4;
        margin-bottom: 20px;
    }
    .stMetric {
        background-color: #F8F9FA;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #E9ECEF;
    }
    </style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# 데이터 로드 (어린이 시설 데이터 + 위험/흡연구역 데이터)
# -----------------------------------------------------------------------------
@st.cache_data
def load_facility_data():
    """어린이 이용가능 시설 샘플 데이터"""
    data = [
        {
            "시설명": "꿈나무 어린이 도서관",
            "유형": "도서관/문화",
            "주소": "서울특별시 마포구 월드컵북로 21",
            "lat": 37.5568,
            "lon": 126.9238,
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
            "lat": 37.5552,
            "lon": 126.9230,
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
            "lat": 37.5495,
            "lon": 127.0815,
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
            "lat": 37.5559,
            "lon": 126.9368,
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
            "lat": 37.5638,
            "lon": 126.8948,
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
            "lat": 37.5680,
            "lon": 126.9150,
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

@st.cache_data
def load_danger_zone_data():
    """흡연구역 및 위험요소 데이터"""
    danger_data = [
        {
            "시설명": "⚠️ [흡연구역] 홍대입구역 9번 출구",
            "유형": "흡연구역",
            "주소": "서울특별시 마포구 양화로 160 주변",
            "lat": 37.5557,
            "lon": 126.9242,
            "주의사항": "간접흡연 주의 (상시 연기 많음)",
            "반경m": 30
        },
        {
            "시설명": "⚠️ [흡연구역] 신촌 오거리 야외 부스",
            "유형": "흡연구역",
            "주소": "서울특별시 마포구 신촌로 주변",
            "lat": 37.5562,
            "lon": 126.9360,
            "주의사항": "유동인구 많고 간접흡연 노출 위험",
            "반경m": 25
        },
        {
            "시설명": "🚧 [공사장] 성산동 신축 아파트 현장",
            "유형": "공사장/위험지역",
            "주소": "서울특별시 마포구 성산동 주변",
            "lat": 37.5665,
            "lon": 126.9135,
            "주의사항": "낙하물 위험 및 대형 공사차량 이동",
            "반경m": 50
        },
        {
            "시설명": "🚧 [공사장] 상암동 보도 블록 공사구역",
            "유형": "공사장/위험지역",
            "주소": "서울특별시 마포구 상암동 주변",
            "lat": 37.5625,
            "lon": 126.8960,
            "주의사항": "보행로 협소, 유모차 통행 불편",
            "반경m": 40
        }
    ]
    return pd.DataFrame(danger_data)

try:
    df_facility = load_facility_data()
    df_danger = load_danger_zone_data()
except Exception as e:
    st.error(f"데이터 로드 중 오류가 발생했습니다: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 2단계: 사이드바 - 검색 및 필터링 기능
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 맞춤 시설 검색")

search_keyword = st.sidebar.text_input("시설명 또는 주소 검색", placeholder="예: 도서관, 마포구")
age = st.sidebar.slider("아이 연령 선택 (세)", min_value=0, max_value=13, value=3)

all_categories = list(df_facility["유형"].unique())
selected_categories = st.sidebar.multiselect(
    "시설 유형",
    options=all_categories,
    default=all_categories
)

st.sidebar.subheader("✨ 편의시설 조건")
need_nursing = st.sidebar.checkbox("수유실 있음")
need_parking = st.sidebar.checkbox("주차 가능")
need_stroller = st.sidebar.checkbox("유모차 대여 가능")

st.sidebar.subheader("⚠️ 안심/위험 요소 설정")
show_smoking = st.sidebar.checkbox("🚬 흡연구역 표시", value=True)
show_construction = st.sidebar.checkbox("🚧 공사장/위험지역 표시", value=True)

# 어린이 시설 필터링
filtered_facility_df = df_facility[
    (df_facility["최소연령"] <= age) & (df_facility["최대연령"] >= age) &
    (df_facility["유형"].isin(selected_categories))
]

if search_keyword:
    filtered_facility_df = filtered_facility_df[
        filtered_facility_df["시설명"].str.contains(search_keyword, case=False) |
        filtered_facility_df["주소"].str.contains(search_keyword, case=False)
    ]

if need_nursing:
    filtered_facility_df = filtered_facility_df[filtered_facility_df["수유실"] == True]
if need_parking:
    filtered_facility_df = filtered_facility_df[filtered_facility_df["주차"] == True]
if need_stroller:
    filtered_facility_df = filtered_facility_df[filtered_facility_df["유모차대여"] == True]

# 위험구역 필터링
selected_danger_types = []
if show_smoking:
    selected_danger_types.append("흡연구역")
if show_construction:
    selected_danger_types.append("공사장/위험지역")

filtered_danger_df = df_danger[df_danger["유형"].isin(selected_danger_types)]


# -----------------------------------------------------------------------------
# 메인 화면 구성 및 지표
# -----------------------------------------------------------------------------
st.markdown('<p class="main-title">🎈 어린이 이용가능 시설 안내 & 안심 지도</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">아이의 연령에 맞는 시설을 찾고, 주변 흡연구역 및 위험지대를 사전에 확인하세요.</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("안전 추천 시설", f"{len(filtered_facility_df)}개")
col2.metric("선택한 연령", f"만 {age}세")
col3.metric("주변 흡연구역", f"{len(df_danger[df_danger['유형']=='흡연구역'])}곳")
col4.metric("주변 공사/위험구역", f"{len(df_danger[df_danger['유형']=='공사장/위험지역'])}곳")

st.markdown("---")


# -----------------------------------------------------------------------------
# 5단계: 탭(Tab) 구분 구성
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ 안심 지도 보기", 
    "📋 어린이 시설 목록", 
    "⚠️ 위험구역/흡연구역 정보", 
    "📅 방문/체험 신청"
])


# -----------------------------------------------------------------------------
# 3, 4단계: Streamlit 기본 지도 시각화 (Tab 1)
# -----------------------------------------------------------------------------
with tab1:
    st.subheader("📍 어린이 시설 및 위험 요망 구역 위치 지도")
    st.write("아래 지도에서 어린이 이용 시설과 우회해야 할 위험 구역 위치를 한눈에 파악하세요.")

    # 어린이 시설 위치 데이터 + 위험구역 데이터 합치기
    map_data_list = []
    
    if not filtered_facility_df.empty:
        map_data_list.append(filtered_facility_df[["lat", "lon"]])
    if not filtered_danger_df.empty:
        map_data_list.append(filtered_danger_df[["lat", "lon"]])

    if map_data_list:
        combined_map_data = pd.concat(map_data_list, ignore_index=True)
        # 별도 외부 라이브러리 없이 Streamlit 내장 지도로 표시
        st.map(combined_map_data)
    else:
        st.info("선택된 조건에 해당하는 시설이나 위험 지역이 없습니다.")


# -----------------------------------------------------------------------------
# 시설 목록 및 상세 정보 (Tab 2)
# -----------------------------------------------------------------------------
with tab2:
    st.subheader("📋 어린이 시설 상세 정보")
    
    if filtered_facility_df.empty:
        st.warning("조건에 만족하는 어린이 시설이 없습니다.")
    else:
        for idx, row in filtered_facility_df.iterrows():
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


# -----------------------------------------------------------------------------
# 위험구역 / 흡연구역 안내 (Tab 3)
# -----------------------------------------------------------------------------
with tab3:
    st.subheader("⚠️ 주변 주의/위험 요소 상세 안내")
    st.write("아이들과 통행 시 간접흡연 및 안전사고를 예방하기 위해 아래 구역을 우회해 주세요.")

    if filtered_danger_df.empty:
        st.info("현재 선택된 위험 요소가 없습니다. 사이드바의 설정 항목을 확인해주세요.")
    else:
        for idx, row in filtered_danger_df.iterrows():
            badge = "🚬 흡연구역" if row["유형"] == "흡연구역" else "🚧 위험지역"
            st.error(f"**[{badge}] {row['시설명']}**")
            st.write(f"- **위치 주소:** {row['주소']}")
            st.write(f"- **주의 사항:** {row['주의사항']}")
            st.write(f"- **우회 권장 반경:** 약 {row['반경m']}m 이내")
            st.markdown("---")


# -----------------------------------------------------------------------------
# 6단계: 예약 및 상담 신청 폼 (Tab 4)
# -----------------------------------------------------------------------------
with tab4:
    st.subheader("📅 시설 방문 및 프로그램 예약 신청")
    st.write("방문하고 싶은 시설을 선택하여 간편하게 예약 및 상담을 신청해보세요.")

    with st.form("booking_form"):
        selected_facility = st.selectbox(
            "시설 선택", 
            filtered_facility_df["시설명"].tolist() if not filtered_facility_df.empty else ["선택 가능한 시설 없음"]
        )
        parent_name = st.text_input("보호자 성함")
        phone_number = st.text_input("연락처 (예: 010-1234-5678)")
        visit_date = st.date_input("방문 희망일", datetime.date.today())
        num_children = st.number_input("동반 어린이 수", min_value=1, max_value=10, value=1)
        memo = st.text_area("기타 요청사항 (예: 위험지역 우회 경로 안내 요청 등)")

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
