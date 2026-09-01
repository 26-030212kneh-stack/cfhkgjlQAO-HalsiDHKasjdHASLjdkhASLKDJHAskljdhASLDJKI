import streamlit as st

# 1. 페이지 기본 설정 및 Custom CSS (카드 스타일링)
st.set_page_config(
    page_title="음식 밸런스 게임 🍔 vs 🍕",
    page_icon="🍔",
    layout="centered"
)

# 카드 형태의 디자인과 호버 효과를 위한 CSS
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #FF4B4B;
    }
    .sub-title {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .card-container {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.2s ease-in-out;
        border: 2px solid #f0f2f6;
    }
    .card-container:hover {
        transform: translateY(-5px);
        border-color: #FF4B4B;
    }
    .food-emoji {
        font-size: 4rem;
        margin-bottom: 10px;
    }
    .food-title {
        font-size: 1.4rem;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .food-desc {
        color: #888;
        font-size: 0.95rem;
        margin-bottom: 15px;
    }
    /* Streamlit 기본 버튼 카드 스타일에 맞춰 커스텀 */
    div.stButton > button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 0;
        font-weight: bold;
        font-size: 1rem;
    }
    div.stButton > button:hover {
        background-color: #D32F2F;
        color: white;
    }
    .vs-badge {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 2rem;
        font-weight: 900;
        color: #FF4B4B;
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 2. 게임 데이터 설정
QUESTIONS = [
    {
        "id": 1,
        "title": "비 오는 날 당신의 선택은?",
        "option_a": {"name": "바삭한 파전 & 막걸리", "emoji": "🥞", "desc": "빗소리 들으며 먹는 겉바속촉 파전"},
        "option_b": {"name": "얼큰한 짬뽕 & 이과두주", "emoji": "🍜", "desc": "칼칼한 국물로 속을 해장하는 짬뽕"}
    },
    {
        "id": 2,
        "title": "평생 한 가지만 먹을 수 있다면?",
        "option_a": {"name": "매일 먹어도 안 질리는 김치찌개", "emoji": "🍲", "desc": "한국인의 소울푸드, 진한 국물과 돼지고기"},
        "option_b": {"name": "육즙 가득한 소고기 스테이크", "emoji": "🥩", "desc": "입에서 녹는 완벽한 미디엄 레어"}
    },
    {
        "id": 3,
        "title": "야식계의 대장, 당신의 पिक은?",
        "option_a": {"name": "바삭하고 고소한 후라이드 치킨", "emoji": "🍗", "desc": "영원한 야식의 왕, 맥주와 완벽 조합"},
        "option_b": {"name": "쫄깃하고 야들야들한 족발", "emoji": "🍖", "desc": "쟁반국수와 함께 싸 먹는 최강 조합"}
    },
    {
        "id": 4,
        "title": "여름철 최애 디저트는?",
        "option_a": {"name": "달콤하고 시원한 팥빙수", "emoji": "🍧", "desc": "고소한 인절미 떡과 클래식한 팥의 조화"},
        "option_b": {"name": "상큼함 폭발 과일 빙수", "emoji": "🍨", "desc": "망고, 딸기가 듬뿍 올라간 프레시 디저트"}
    }
]

# 3. 세션 상태 초기화
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "user_choices" not in st.session_state:
    st.session_state.user_choices = []

# 선택 기록 함수
def select_option(choice):
    st.session_state.user_choices.append({
        "question": QUESTIONS[st.session_state.current_q]["title"],
        "choice": choice
    })
    st.session_state.current_q += 1

# 리셋 함수
def reset_game():
    st.session_state.current_q = 0
    st.session_state.user_choices = []

# 4. 헤더 레이아웃
st.markdown("<h1 class='main-title'>🍕 음식 밸런스 게임 🍔</h1>", unsafe_allow_html=True)

# 5. 게임 진행 로직
if st.session_state.current_q < len(QUESTIONS):
    q = QUESTIONS[st.session_state.current_q]
    
    # 진행률 표시
    progress = (st.session_state.current_q) / len(QUESTIONS)
    st.progress(progress)
    st.markdown(f"<p class='sub-title'>Q{q['id']}. {q['title']} ({st.session_state.current_q + 1}/{len(QUESTIONS)})</p>", unsafe_allow_html=True)

    # 카드 레이아웃 구성 (2개 열 + 중앙 VS)
    col1, col_vs, col2 = st.columns([10, 2, 10])

    # 옵션 A 카드
    with col1:
        opt_a = q["option_a"]
        st.markdown(f"""
            <div class="card-container">
                <div class="food-emoji">{opt_a['emoji']}</div>
                <div class="food-title">{opt_a['name']}</div>
                <div class="food-desc">{opt_a['desc']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("") # 간격 조정
        if st.button("선택하기", key=f"btn_a_{q['id']}"):
            select_option(opt_a['name'])
            st.rerun()

    # VS 표시
    with col_vs:
        st.markdown("<div class='vs-badge'>VS</div>", unsafe_allow_html=True)

    # 옵션 B 카드
    with col2:
        opt_b = q["option_b"]
        st.markdown(f"""
            <div class="card-container">
                <div class="food-emoji">{opt_b['emoji']}</div>
                <div class="food-title">{opt_b['name']}</div>
                <div class="food-desc">{opt_b['desc']}</div>
            </div>
        """, unsafe_allow_html=True)
        st.write("") # 간격 조정
        if st.button("선택하기", key=f"btn_b_{q['id']}"):
            select_option(opt_b['name'])
            st.rerun()

# 6. 결과 페이지
else:
    st.balloons()
    st.success("🎉 모든 밸런스 게임을 완료했습니다!")
    st.subheader("📋 내가 선택한 음식 취향 모아보기")

    for idx, result in enumerate(st.session_state.user_choices, 1):
        st.info(f"**Q{idx}. {result['question']}**\n\n👉 **당신의 선택:** {result['choice']}")

    st.write("---")
    if st.button("🔄 게임 다시 시작하기"):
        reset_game()
        st.rerun()
