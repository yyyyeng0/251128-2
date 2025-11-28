import streamlit as st
import random

st.set_page_config(page_title="나눗셈 학습 (10문제)", page_icon="🍬", layout="centered")

st.title("🍬 초등 4학년 나눗셈 학습")
st.write("성취기준: **[4수01-06] 한 자리 수 나눗셈의 원리를 이해하고, 몫과 나머지를 안다**")


# ------------------------------------
# 🔧 난이도 설정
# ------------------------------------
st.sidebar.header("난이도 선택")

difficulty = st.sidebar.radio(
    "난이도를 선택하세요",
    ["쉬움", "보통", "어려움"],
)

if difficulty == "쉬움":
    A_RANGE = (10, 30)
elif difficulty == "보통":
    A_RANGE = (20, 50)
else:
    A_RANGE = (40, 80)


# ------------------------------------
# 🔧 문제 세트 생성(난이도 변경 시 재생성)
# ------------------------------------
if "problems" not in st.session_state or st.session_state.get("difficulty") != difficulty:
    st.session_state.difficulty = difficulty
    st.session_state.problems = [
        (random.randint(*A_RANGE), random.randint(2, 9))
        for _ in range(10)
    ]
    st.session_state.current = 0
    st.session_state.show_hint = False
    st.session_state.checked = False
    st.session_state.user_q = None
    st.session_state.user_r = None


# 현재 문제
idx = st.session_state.current
a, b = st.session_state.problems[idx]

st.subheader(f"📘 {idx + 1}번째 문제 (총 10문제)")
st.markdown(f"### **{a} ÷ {b}**")


# ------------------------------------
# 🍬 사탕 그림: 묶지 않고 단순 배열
# ------------------------------------
st.markdown("### 🍬 전체 사탕")
st.write("아래 사탕을 보고 직접 **b개씩 묶어보며** 몫과 나머지를 생각해보세요!")

candies_per_row = 10
rows = (a + candies_per_row - 1) // candies_per_row

for r in range(rows):
    row_candies = min(candies_per_row, a - r * candies_per_row)
    cols = st.columns(row_candies)
    for c in cols:
        c.markdown("<div style='font-size:26px; text-align:center;'>🍬</div>", unsafe_allow_html=True)


# ------------------------------------
# 🔍 힌트 버튼 → 묶음 표시 
# ------------------------------------
if st.button("🔍 힌트 보기"):
    st.session_state.show_hint = True

if st.session_state.show_hint:
    st.markdown("### 🔍 힌트: b개씩 묶음 표시")
    st.write("묶음은 초록색, 나머지는 빨간색으로 표시됩니다!")

    groups = a // b
    remainder = a % b

    for g in range(groups):
        cols = st.columns(b)
        for c in cols:
            c.markdown("<div style='font-size:26px; text-align:center; color:green;'>🍬</div>", unsafe_allow_html=True)
        st.write(f"➡️ **{g+1}번째 묶음**")

    if remainder > 0:
        st.write("➡️ **나머지 사탕**")
        cols = st.columns(remainder)
        for c in cols:
            c.markdown("<div style='font-size:26px; text-align:center; color:red;'>🍬</div>", unsafe_allow_html=True)
        st.write(f"👉 남은 사탕: {remainder}개")


# ------------------------------------
# ✏ 정답 입력
# ------------------------------------
st.markdown("### ✏ 몫과 나머지를 입력하세요")

col1, col2 = st.columns(2)

user_q = col1.number_input("몫", min_value=0, step=1, value=st.session_state.user_q or 0)
user_r = col2.number_input("나머지", min_value=0, step=1, value=st.session_state.user_r or 0)

real_q = a // b
real_r = a % b

if st.button("정답 확인"):
    st.session_state.user_q = user_q
    st.session_state.user_r = user_r

    if user_q == real_q and user_r == real_r:
        st.success("🎉 정답입니다! 정말 잘했어요!")
        st.session_state.checked = True
    else:
        st.error("😅 다시 생각해볼까요? 힌트를 참고해보세요!")


# 정답 보기
if st.session_state.checked:
    st.info(f"✔ 정답: 몫 = **{real_q}**, 나머지 = **{real_r}**")


# ------------------------------------
# 다음 문제 버튼
# ------------------------------------
if st.session_state.checked and st.session_state.current < 9:
    if st.button("👉 다음 문제"):
        st.session_state.current += 1
        st.session_state.checked = False
        st.session_state.show_hint = False
        st.session_state.user_q = None
        st.session_state.user_r = None
        st.rerun()   # 🔥 최신 Streamlit용 올바른 rerun


# ------------------------------------
# 10문제 완료
# ------------------------------------
if idx == 9 and st.session_state.checked:
    st.success("🎉 모든 10문제를 완료했습니다! 최고예요!")

    if st.button("🔄 같은 난이도로 다시 시작"):
        st.session_state.problems = [
            (random.randint(*A_RANGE), random.randint(2, 9))
            for _ in range(10)
        ]
        st.session_state.current = 0
        st.session_state.checked = False
        st.session_state.show_hint = False
        st.session_state.user_q = None
        st.session_state.user_r = None
        st.rerun()   # 🔥 최신 Streamlit용 rerun
