streamlit>=1.28.0
pandas>=2.0.0
folium>=0.14.0
streamlit-folium>=0.13.0
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import datetime

# -----------------------------------------------------------------------------
# 1. 페이지 기본 설정 및 스타일링
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="아이플레이그라운드 - 어린이 시설 & 안심케어 지도",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 2.2rem;
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
# 2. 데이터 생성 및 캐싱 (어린이 시설 데이터 + 위험구역/흡연구역 데이터)
# -----------------------------------------------------------------------------
@st.cache_data
def load_facility_data():
    """어린이 이용가능 시설 샘플 데이터"""
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

@st.cache_data
def load_danger_zone_data():
    """흡연구역 및 위험 요소 데이터"""
    danger_data = [
        {
            "명칭": "홍대입구역 9번 출구 지정 흡연구역",
            "유형": "흡연구역",
            "위도": 37.5557,
            "경도": 126.9242,
            "주의사항": "간접흡연 주의 (상시 연기 많음)",
            "반경m": 30
        },
        {
            "명칭": "신촌 오거리 야외 흡연 부스",
            "유형": "흡연구역",
            "위도": 37.5562,
            "경도": 126.9360,
            "주의사항": "유동인구 많고 간접흡연 노출 위험",
            "반경m": 25
        },
        {
            "명칭": "성산동 신축 아파트 건설 공통 현장",
            "유형": "공사장/위험지역",
            "위도": 37.5665,
            "경도": 126.9135,
            "주의사항": "낙하물 위험 및 대형 공사차량 빈번 이동",
            "반경m": 50
        },
        {
            "명칭": "상암동 보도 블록 및 도로 공사구역",
            "유형": "공사장/위험지역",
            "위도": 37.5625,
            "경도": 126.8960,
            "주의사항": "보행로 협소, 유모차 통행 불편",
            "반경m": 40
        }
    ]
    return pd.DataFrame(danger_data)

try:
    df_facility = load_facility_data()
    df_danger = load_danger_zone_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# -----------------------------------------------------------------------------
# 3. 사이드바 - 검색, 시설 필터, 위험요소 설정
# -----------------------------------------------------------------------------
st.sidebar.header("🔍 맞춤 시설 검색")

# 검색어
search_keyword = st.sidebar.text_input("시설명 또는 주소 검색", placeholder="예: 도서관, 마포구")

# 아이 연령 필터
age = st.sidebar.slider("아이 연령 선택 (세)", min_value=0, max_value=13, value=3)

# 시설 유형 필터
all_categories = list(df_facility["유형"].unique())
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

# 🚨 위험구역 표시 옵션
st.sidebar.subheader("⚠️ 안심/위험 요소 표시 설정")
show_smoking = st.sidebar.checkbox("🚬 흡연구역 표시", value=True)
show_construction = st.sidebar.checkbox("🚧 공사장 및 위험구역 표시", value=True)
show_danger_radius = st.sidebar.checkbox("⭕ 위험 영향 반경(원) 표시", value=True)

# 어린이 시설 필터링 적용 Logic
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

# 위험구역 필터링 적용 Logic
selected_danger_types = []
if show_smoking:
    selected_danger_types.append("흡연구역")
if show_construction:
    selected_danger_types.append("공사장/위험지역")

filtered_danger_df = df_danger[df_danger["유형"].isin(selected_danger_types)]


# -----------------------------------------------------------------------------
# 4. 메인 화면 구성
# -----------------------------------------------------------------------------
st.markdown('<p class="main-title">🎈 우리아이 맞춤 시설 & 안심 지도</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">아이의 연령에 맞는 시설을 찾고, 주변 흡연구역 및 위험지대를 사전에 확인하세요.</p>', unsafe_allow_html=True)

# 주요 지표 (Metrics)
col1, col2, col3, col4 = st.columns(4)
col1.metric("안전 추천 시설", f"{len(filtered_facility_df)}개")
col2.metric("선택한 연령", f"만 {age}세")
col3.metric("주변 흡연구역", f"{len(df_danger[df_danger['유형']=='흡연구역'])}곳")
col4.metric("주변 공사/위험구역", f"{len(df_danger[df_danger['유형']=='공사장/위험지역'])}곳")

st.markdown("---")

# 탭 구성 (지도 보기 / 시설 목록 / 위험구역 안내 / 예약 신청)
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ 안심 지도 보기", 
    "📋 어린이 시설 목록", 
    "⚠️ 위험구역/흡연구역 정보", 
    "📅 방문/체험 신청"
])

# TAB 1: Folium 지도 시각화 (시설 + 위험구역)
with tab1:
    st.subheader("📍 어린이 시설 및 회피 요망 구역 지도")
    
    # 범례 안내
    st.markdown("""
    **💡 지도 아이콘 안내:**
    - 🔵/🔴/🟢 **어린이 시설**: 도서관, 키즈카페, 병원, 공원 등
    - 🚬 **검은색 아이콘**: 지정 흡연구역 (간접흡연 주의)
    - 🚧 **주황색 아이콘**: 공사장/위험 요소
    """)

    # 지도 중심 설정
    if not filtered_facility_df.empty:
        start_lat = filtered_facility_df["위도"].mean()
        start_lng = filtered_facility_df["경도"].mean()
    else:
        start_lat, start_lng = 37.5568, 126.9238

    m = folium.Map(location=[start_lat, start_lng], zoom_start=13)

    # 1) 어린이 이용 시설 마커 추가
    color_dict = {
        "도서관/문화": "blue",
        "키즈카페": "red",
        "체험/박물관": "purple",
        "의료/병원": "green",
        "공원/놀이터": "darkgreen",
        "어린이집/유치원": "cadetblue"
    }

    for _, row in filtered_facility_df.iterrows():
        popup_html = f"""
        <div style="width:180px">
            <b style="color:#2B8A3E;">[어린이 시설]</b><br>
            <b>{row['시설명']}</b><br>
            유형: {row['유형']}<br>
            추천연령: {row['추천연령']}<br>
            평점: ⭐{row['평점']}
        </div>
        """
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"🎈 {row['시설명']}",
            icon=folium.Icon(color=color_dict.get(row["유형"], "blue"), icon="info-sign")
        ).add_to(m)

    # 2) 위험 요소 / 흡연구역 마커 및 반경(Circle) 추가
    for _, row in filtered_danger_df.iterrows():
        is_smoking = row["유형"] == "흡연구역"
        icon_name = "ban-circle" if is_smoking else "warning-sign"
        icon_color = "black" if is_smoking else "orange"
        circle_color = "#FF0000" if is_smoking else "#FF8800"

        popup_html = f"""
        <div style="width:190px">
            <b style="color:#C92A2A;">⚠️ {row['유형']}</b><br>
            <b>{row['명칭']}</b><br>
            <span style="color:#E03131; font-size:12px;">{row['주의사항']}</span>
        </div>
        """
        
        # 위험지점 마커
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"⚠️ {row['유형']}: {row['명칭']}",
            icon=folium.Icon(color=icon_color, icon=icon_name)
        ).add_to(m)

        # 위험 영향 반경 (Circle)
        if show_danger_radius:
            folium.Circle(
                location=[row["위도"], row["경도"]],
                radius=row["반경m"],
                color=circle_color,
                fill=True,
                fill_color=circle_color,
                fill_opacity=0.25,
                popup=f"{row['명칭']} 영향 범위 ({row['반경m']}m)"
            ).add_to(m)

    # Streamlit에 지도 출력
    st_folium(m, width="100%", height=480)


# TAB 2: 시설 목록 및 상세 정보
with tab2:
    st.subheader("📋 어린이 시설 목록")
    
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


# TAB 3: 위험구역 / 흡연구역 상세목록
with tab3:
    st.subheader("⚠️ 주변 주의/위험 요소 상세 안내")
    st.write("아이들과 통행 시 간접흡연 및 안전사고를 예방하기 위해 아래 구역을 우회해 주세요.")

    if filtered_danger_df.empty:
        st.info("현재 선택된 위험 요소가 없습니다. 사이드바에서 위험 요소 표시 설정을 확인하세요.")
    else:
        for idx, row in filtered_danger_df.iterrows():
            badge = "🚬 흡연구역" if row["유형"] == "흡연구역" else "🚧 위험지역"
            st.error(f"**[{badge}] {row['명칭']}**")
            st.write(f"- **주의 사항:** {row['주의사항']}")
            st.write(f"- **우회 권장 반경:** 약 {row['반경m']}m 이내")
            st.markdown("---")


# TAB 4: 예약 및 상담 신청 (시뮬레이션)
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
        memo = st.text_area("기타 요청사항 (예: 위험지역 우회 이동 경로 안내 요청 등)")

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
