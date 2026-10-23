import streamlit as st
import json
import os
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="어린이 불편 신문고 🎈",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 데이터 저장 파일 경로 설정
DATA_FILE = "reports_data.json"

# 기본 샘플 데이터 (초기 파일 생성용)
DEFAULT_DATA = [
    {
        "id": 1,
        "title": "학교 앞 신호등 시간이 너무 짧아요!",
        "author": "초등 3학년 민우",
        "category": "🚨 안전/교통",
        "location": "행복초등학교 앞 횡단보도",
        "content": "초록불이 켜지고 건너려고 하면 금방 빨간불로 바뀌어서 위험해요. 다리가 짧은 저학년 친구들은 건너기 힘들어요! 시간을 조금만 더 길게 늘려주세요.",
        "likes": 12,
        "date": "2026-03-20 14:30:00",
        "status": "진행 중 ⏳"
    },
    {
        "id": 2,
        "title": "놀이터 미끄럼틀이 부서져 있어서 위험해요",
        "author": "씩씩한 어린이",
        "category": "🎡 놀이터/공원",
        "location": "무지개공원 놀이터",
        "content": "미끄럼틀 손잡이 부분이 깨져 있어서 손이 긁힐 뻔했어요. 다른 친구들도 다칠 수 있으니까 빨리 고쳐주세요!",
        "likes": 25,
        "date": "2026-03-21 10:15:00",
        "status": "접수 완료 📩"
    }
]

# -------------------------------------------------------------------
# 데이터 로드 & 저장 함수
# -------------------------------------------------------------------
def load_data():
    """JSON 파일에서 제보 글 목록을 불러옵니다."""
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return DEFAULT_DATA

def save_data(data):
    """JSON 파일에 제보 글 목록을 저장합니다."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        st.error(f"데이터 저장 실패: {e}")

# Session State 초기화
if "reports" not in st.session_state:
    st.session_state.reports = load_data()

if "liked_posts" not in st.session_state:
    st.session_state.liked_posts = set()  # 중복 공감 방지용 세션 상태

# -------------------------------------------------------------------
# Custom CSS Style (어린이 친화적 디자인)
# -------------------------------------------------------------------
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #FF5722;
        text-align: center;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .report-card {
        background-color: #FFFDE7;
        border-radius: 12px;
        padding: 18px;
        border-left: 6px solid #FFC107;
        margin-bottom: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    .badge-status {
        background-color: #E1F5FE;
        color: #0288D1;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    .badge-cat {
        background-color: #FFE0B2;
        color: #E65100;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------
# 헤더 영역
# -------------------------------------------------------------------
st.markdown('<div class="main-header">🎈 어린이 마음 소리 (신문고) 🎈</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">학교, 놀이터, 길거리에서 있었던 불편한 점을 이야기해 주세요. 우리가 함께 힘을 모아 바꿔요!</div>', unsafe_allow_html=True)

# -------------------------------------------------------------------
# 사이드바: 통계 & 안내
# -------------------------------------------------------------------
with st.sidebar:
    st.header("📊 우리의 소리 현황")
    total_count = len(st.session_state.reports)
    total_likes = sum(r["likes"] for r in st.session_state.reports)
    
    col1, col2 = st.columns(2)
    col1.metric("총 접수 건수", f"{total_count}건")
    col2.metric("누적 공감 수", f"{total_likes}개")
    
    st.divider()
    
    st.markdown("""
    ### 📢 이용 방법
    1. **글쓰기**: 불편했거나 위험했던 상황을 작성해요.
    2. **공감하기**: 친구들의 글을 읽고 ❤️ **공감하기** 버튼을 눌러 응원해요!
    3. **응원 메세지**: 많은 공감을 받은 이야기는 관련 기관에 전달될 수 있어요!
    """)
    st.info("💡 서로를 존중하며 예쁜 말을 사용해 주세요!")

# -------------------------------------------------------------------
# 메인 탭 구성
# -------------------------------------------------------------------
tab1, tab2 = st.tabs(["📜 어린이들의 이야기 (커뮤니티)", "✍️ 불편사항 제보하기"])

# -------------------------------------------------------------------
# TAB 1: 게시글 목록 & 공감 기능
# -------------------------------------------------------------------
with tab1:
    st.subheader("🗣️ 친구들의 소리를 들어보세요")
    
    # 검색 및 필터링
    c1, c2 = st.columns([2, 1])
    with c1:
        search_kw = st.text_input("🔍 검색어 입력 (제목, 내용, 장소)", placeholder="예: 신호등, 놀이터...")
    with c2:
        sort_option = st.selectbox("정렬 기준", ["최신순 🆕", "공감 많은순 ❤️"])
        
    # 필터링 로직
    filtered_reports = st.session_state.reports.copy()
    if search_kw:
        filtered_reports = [
            r for r in filtered_reports 
            if search_kw.lower() in r["title"].lower() 
            or search_kw.lower() in r["content"].lower() 
            or search_kw.lower() in r["location"].lower()
        ]
        
    # 정렬 로직
    if sort_option == "최신순 🆕":
        filtered_reports.sort(key=lambda x: x["id"], reverse=True)
    else:
        filtered_reports.sort(key=lambda x: x["likes"], reverse=True)

    st.write("")

    if not filtered_reports:
        st.info("아직 등록된 제보가 없거나 검색 결과가 없습니다. 작성 페이지에서 첫 제보를 남겨보세요!")
    else:
        for report in filtered_reports:
            with st.container():
                st.markdown(f"""
                <div class="report-card">
                    <span class="badge-cat">{report['category']}</span> 
                    <span class="badge-status">{report['status']}</span>
                    <h3 style="margin-top: 8px; margin-bottom: 5px; color: #333;">{report['title']}</h3>
                    <p style="color: #666; font-size: 0.9rem; margin-bottom: 8px;">
                        👤 <b>{report['author']}</b> | 📍 장소: {report['location']} | ⏰ 작성일: {report['date'][:10]}
                    </p>
                    <p style="font-size: 1.05rem; line-height: 1.6; color: #222;">{report['content']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # 공감 버튼 및 하트 개수
                col_btn, col_blank = st.columns([1, 4])
                with col_btn:
                    btn_key = f"like_{report['id']}"
                    is_liked = report['id'] in st.session_state.liked_posts
                    
                    btn_label = f"❤️ 공감하기 ({report['likes']})"
                    
                    if st.button(btn_label, key=btn_key, type="primary" if is_liked else "secondary"):
                        if is_liked:
                            # 이미 공감한 경우 취소
                            report['likes'] -= 1
                            st.session_state.liked_posts.remove(report['id'])
                            st.toast("공감을 취소했습니다.", icon="💔")
                        else:
                            # 공감 추가
                            report['likes'] += 1
                            st.session_state.liked_posts.add(report['id'])
                            st.toast("이 글에 공감했습니다!", icon="❤️")
                        
                        save_data(st.session_state.reports)
                        st.rerun()

                st.markdown("<hr style='margin: 15px 0; border: 0.5px solid #eee;'>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# TAB 2: 제보하기 작성 폼
# -------------------------------------------------------------------
with tab2:
    st.subheader("✍️ 내가 겪은 불편한 점을 알려주세요!")
    st.write("어린이 여러분이 느낀 위험하거나 불편한 상황을 자세히 적어주세요.")
    
    with st.form(key="report_form", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            author = st.text_input("닉네임 / 이름", placeholder="예: 무지개초등학교 4학년 김어린이")
            category = st.selectbox("어떤 종류의 불편함인가요?", [
                "🚨 안전/교통 (신호등, 건너목, 위험한 길)",
                "🎡 놀이터/공원 (고장 난 기구, 쓰레기)",
                "🏫 학교/학원 (시설 고장, 위험 요소)",
                "🏬 편의시설/가게 (높은 키오스크, 어린이 이용불가)",
                "💡 기타 자유로운 이야기"
            ])
            
        with col_f2:
            location = st.text_input("어디에서 일어난 일인가요? (장소)", placeholder="예: OO초등학교 앞 문방구 근처")
            title = st.text_input("제목", placeholder="한 줄로 짧게 작성해 주세요")
            
        content = st.text_area("자세한 내용", placeholder="어떤 점이 불편하고 위험했는지, 어떻게 바뀌면 좋을지 적어주세요.", height=150)
        
        submit_button = st.form_submit_button(label="🚀 제보 등록하기")

    if submit_button:
        # 간단한 유효성 검사
        if not author.strip():
            st.warning("닉네임 또는 이름을 입력해 주세요!")
        elif not title.strip():
            st.warning("제목을 입력해 주세요!")
        elif not location.strip():
            st.warning("장소를 입력해 주세요!")
        elif not content.strip():
            st.warning("내용을 작성해 주세요!")
        else:
            try:
                # 새로운 게시글 객체 생성
                new_id = max([r["id"] for r in st.session_state.reports], default=0) + 1
                new_report = {
                    "id": new_id,
                    "title": title.strip(),
                    "author": author.strip(),
                    "category": category,
                    "location": location.strip(),
                    "content": content.strip(),
                    "likes": 0,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "접수 완료 📩"
                }
                
                # 세션 및 파일 저장
                st.session_state.reports.append(new_report)
                save_data(st.session_state.reports)
                
                st.success("🎉 성공적으로 제보가 등록되었습니다! 친구들의 공감을 기다려봐요.")
                st.balloons()
            except Exception as e:
                st.error(f"글을 저장하는 도중 오류가 발생했습니다: {e}")
