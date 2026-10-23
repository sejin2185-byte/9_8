import streamlit as st
from datetime import datetime
import random

# 꼬마 상점: 어린이를 위한 가상 주문 키오스크
st.set_page_config(
    page_title="꼬마 상점 🧸",
    page_icon="🧸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- 디자인 ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Jua&display=swap');

    html, body, [class*="css"] {
        font-family: 'Jua', sans-serif;
    }
    .stApp {
        background: linear-gradient(180deg, #fff8e8 0%, #fffdf7 100%);
    }
    .main .block-container {
        max-width: 1100px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }
    .hero {
        background: linear-gradient(120deg, #ffcf70, #ffedaa);
        border: 3px solid #f6b84a;
        border-radius: 26px;
        padding: 1.3rem 1.5rem;
        text-align: center;
        box-shadow: 0 5px 0 #e8a83b;
        margin-bottom: 1.2rem;
    }
    .hero h1 {
        color: #573b25;
        font-size: 2.5rem;
        margin: 0;
    }
    .hero p {
        color: #654b32;
        font-size: 1.15rem;
        margin: .4rem 0 0 0;
    }
    .menu-card {
        background: #ffffff;
        border: 2px solid #f5dfb5;
        border-radius: 22px;
        padding: 1rem .8rem .5rem .8rem;
        text-align: center;
        min-height: 185px;
        box-shadow: 0 4px 0 #f0dfc1;
    }
    .menu-emoji {
        font-size: 3.2rem;
        line-height: 1.3;
    }
    .menu-name {
        font-size: 1.25rem;
        color: #503c2b;
        margin-top: .25rem;
    }
    .menu-price {
        color: #e07835;
        font-size: 1.1rem;
        margin-bottom: .5rem;
    }
    div.stButton > button {
        border-radius: 15px;
        min-height: 2.8rem;
        font-size: 1.05rem;
        font-weight: 700;
        border: 2px solid #f0c16c;
    }
    div.stButton > button[kind="primary"] {
        background: #ffb84d;
        color: #4d321b;
        border: 2px solid #eaa03a;
    }
    .info-pill {
        background: #e8f7df;
        border-radius: 16px;
        padding: .7rem 1rem;
        text-align: center;
        color: #376b31;
        font-size: 1.05rem;
    }
    .total-box {
        background: #fff0cf;
        border: 2px dashed #e9ae4a;
        border-radius: 18px;
        padding: 1rem;
        text-align: center;
        color: #593d22;
        font-size: 1.5rem;
    }
    .small-note {
        color: #766a5d;
        font-size: .9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- 메뉴 데이터 ----------
MENU = [
    {"id": "apple", "name": "사과", "emoji": "🍎", "price": 1000, "category": "간식", "desc": "아삭아삭 과일"},
    {"id": "banana", "name": "바나나", "emoji": "🍌", "price": 800, "category": "간식", "desc": "달콤한 과일"},
    {"id": "cookie", "name": "쿠키", "emoji": "🍪", "price": 1200, "category": "간식", "desc": "바삭바삭 쿠키"},
    {"id": "sandwich", "name": "샌드위치", "emoji": "🥪", "price": 2500, "category": "간식", "desc": "든든한 한입"},
    {"id": "milk", "name": "우유", "emoji": "🥛", "price": 1000, "category": "음료", "desc": "고소한 우유"},
    {"id": "juice", "name": "딸기 주스", "emoji": "🧃", "price": 1500, "category": "음료", "desc": "상큼달콤 주스"},
    {"id": "water", "name": "물", "emoji": "💧", "price": 500, "category": "음료", "desc": "시원한 물"},
    {"id": "yogurt", "name": "요구르트", "emoji": "🥤", "price": 900, "category": "음료", "desc": "새콤달콤 요구르트"},
]

def money(value):
    return f"{value:,}원"

def init_state():
    if "cart" not in st.session_state:
        st.session_state.cart = {}
    if "page" not in st.session_state:
        st.session_state.page = "menu"
    if "last_order" not in st.session_state:
        st.session_state.last_order = None
    if "order_number" not in st.session_state:
        st.session_state.order_number = random.randint(100, 999)

def add_to_cart(item_id):
    st.session_state.cart[item_id] = st.session_state.cart.get(item_id, 0) + 1

def change_quantity(item_id, delta):
    current = st.session_state.cart.get(item_id, 0) + delta
    if current <= 0:
        st.session_state.cart.pop(item_id, None)
    else:
        st.session_state.cart[item_id] = current

def cart_total():
    prices = {item["id"]: item["price"] for item in MENU}
    return sum(prices[item_id] * qty for item_id, qty in st.session_state.cart.items())

init_state()

# ---------- 머리말 ----------
st.markdown(
    """
    <div class="hero">
      <h1>🧸 꼬마 상점에 오신 걸 환영해요!</h1>
      <p>먹고 싶은 것을 골라서 장바구니에 담아 보세요.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

cart_count = sum(st.session_state.cart.values())
top1, top2 = st.columns([3, 1])
with top1:
    st.markdown('<div class="info-pill">🌟 천천히 골라도 괜찮아요. 버튼을 눌러 보세요!</div>', unsafe_allow_html=True)
with top2:
    st.metric("🛒 장바구니", f"{cart_count}개")

# ---------- 화면: 메뉴 ----------
if st.session_state.page == "menu":
    st.subheader("🍓 무엇을 먹고 싶나요?")
    category = st.radio(
        "메뉴 종류",
        ["전체", "간식", "음료"],
        horizontal=True,
        label_visibility="collapsed",
        key="category_choice",
    )
    filtered = [item for item in MENU if category == "전체" or item["category"] == category]

    # 카드 4개씩 표시
    for start in range(0, len(filtered), 4):
        row_items = filtered[start:start + 4]
        cols = st.columns(4)
        for col, item in zip(cols, row_items):
            with col:
                st.markdown(
                    f"""
                    <div class="menu-card">
                      <div class="menu-emoji">{item['emoji']}</div>
                      <div class="menu-name">{item['name']}</div>
                      <div class="menu-price">{money(item['price'])}</div>
                      <div class="small-note">{item['desc']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button(f"➕ 담기", key=f"add_{item['id']}", use_container_width=True):
                    add_to_cart(item["id"])
                    st.toast(f"{item['name']}을(를) 담았어요!", icon="🛒")
                    st.rerun()

    st.divider()
    left, right = st.columns([1, 1])
    with left:
        if st.button("🧺 장바구니 보기", type="primary", use_container_width=True):
            st.session_state.page = "cart"
            st.rerun()
    with right:
        if st.button("🧹 처음부터 다시 고르기", use_container_width=True):
            st.session_state.cart = {}
            st.toast("장바구니를 비웠어요!", icon="✨")
            st.rerun()

# ---------- 화면: 장바구니 ----------
elif st.session_state.page == "cart":
    st.subheader("🧺 장바구니를 확인해요")
    if not st.session_state.cart:
        st.info("아직 담은 메뉴가 없어요. 메뉴를 골라 볼까요?")
        if st.button("🍎 메뉴 고르러 가기", type="primary"):
            st.session_state.page = "menu"
            st.rerun()
    else:
        menu_by_id = {item["id"]: item for item in MENU}
        for item_id in list(st.session_state.cart.keys()):
            item = menu_by_id.get(item_id)
            if item is None:
                st.session_state.cart.pop(item_id, None)
                continue
            qty = st.session_state.cart[item_id]
            c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
            with c1:
                st.markdown(f"### {item['emoji']} {item['name']}")
                st.caption(f"{money(item['price'])} × {qty}개 = **{money(item['price'] * qty)}**")
            with c2:
                if st.button("➖", key=f"minus_{item_id}", use_container_width=True):
                    change_quantity(item_id, -1)
                    st.rerun()
            with c3:
                st.markdown(f"<div style='text-align:center;padding-top:12px;font-size:1.2rem'>{qty}개</div>", unsafe_allow_html=True)
            with c4:
                if st.button("➕", key=f"plus_{item_id}", use_container_width=True):
                    change_quantity(item_id, 1)
                    st.rerun()

        st.divider()
        st.markdown(
            f"<div class='total-box'>✨ 모두 합쳐서 <b>{money(cart_total())}</b> 이에요!</div>",
            unsafe_allow_html=True,
        )
        st.caption("이 앱은 가게 놀이용이에요. 실제 결제는 진행되지 않아요.")
        a, b, c = st.columns(3)
        with a:
            if st.button("⬅️ 메뉴 더 고르기", use_container_width=True):
                st.session_state.page = "menu"
                st.rerun()
        with b:
            if st.button("🗑️ 장바구니 비우기", use_container_width=True):
                st.session_state.cart = {}
                st.toast("장바구니를 비웠어요!")
                st.rerun()
        with c:
            if st.button("🎉 주문하기!", type="primary", use_container_width=True):
                if st.session_state.cart:
                    st.session_state.last_order = {
                        "number": st.session_state.order_number,
                        "items": [
                            {
                                "name": menu_by_id[item_id]["name"],
                                "emoji": menu_by_id[item_id]["emoji"],
                                "qty": qty,
                                "price": menu_by_id[item_id]["price"],
                            }
                            for item_id, qty in st.session_state.cart.items()
                            if item_id in menu_by_id
                        ],
                        "total": cart_total(),
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    st.session_state.cart = {}
                    st.session_state.page = "done"
                    st.rerun()
                else:
                    st.warning("먼저 메뉴를 담아 주세요!")

# ---------- 화면: 주문 완료 ----------
elif st.session_state.page == "done":
    order = st.session_state.last_order
    if not order:
        st.warning("주문 내역을 찾을 수 없어요. 메뉴부터 다시 시작해 주세요.")
        if st.button("🏠 처음으로"):
            st.session_state.page = "menu"
            st.rerun()
    else:
        st.markdown(
            """
            <div class="hero">
              <h1>🎉 주문 완료!</h1>
              <p>멋져요! 주문이 잘 접수되었어요.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='total-box'>내 주문 번호는 <b>#{order['number']}</b> 이에요!</div>",
            unsafe_allow_html=True,
        )
        st.write("")
        st.subheader("🧾 주문한 메뉴")
        for item in order["items"]:
            st.write(f"{item['emoji']} **{item['name']}** × {item['qty']}개 — {money(item['price'] * item['qty'])}")
        st.divider()
        st.markdown(f"## 💰 총 금액: {money(order['total'])}")
        st.success("주문 완료! 실제 결제나 주문 전송은 되지 않는 체험용 앱이에요.")
        if st.button("🌈 새 주문 시작하기", type="primary", use_container_width=True):
            st.session_state.order_number = random.randint(100, 999)
            st.session_state.last_order = None
            st.session_state.cart = {}
            st.session_state.page = "menu"
            st.rerun()

st.divider()
st.markdown(
    "<p style='text-align:center;color:#8a7a68'>💛 꼬마 상점 · 안전한 가게 놀이 키오스크</p>",
    unsafe_allow_html=True,
)
