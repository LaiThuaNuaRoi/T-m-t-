import streamlit as st
import random

# Danh sách từ và cụm từ hợp lệ
vietnamese_words = [
    "biển", "báo", "bóng", "bay", "bánh", "bao", "cầu", "vồng", "chân", "trời", "trại", "lửa"
]

valid_phrases = {
    "biển báo", "bóng bay", "bánh bao", "cầu vồng", "chân trời", "trại lửa"
}

st.set_page_config(page_title="🎮 Ghép Từ Có Nghĩa", layout="centered")
st.title("🎮 Game Ghép Từ Có Nghĩa")
st.markdown("Chọn 2 chữ cái. Bạn và máy sẽ lần lượt tạo cụm từ gồm 2 từ bắt đầu bằng 2 chữ cái đó. Ai không nghĩ ra hoặc trùng sẽ thua.")

# Session state
if "used_phrases" not in st.session_state:
    st.session_state.used_phrases = set()
if "prefix" not in st.session_state:
    st.session_state.prefix = ""
if "valid_phrases" not in st.session_state:
    st.session_state.valid_phrases = set()
if "game_started" not in st.session_state:
    st.session_state.game_started = False
if "log" not in st.session_state:
    st.session_state.log = []

def get_valid_phrases(c1, c2):
    first = [w for w in vietnamese_words if w.startswith(c1)]
    second = [w for w in vietnamese_words if w.startswith(c2)]
    return {
        f"{w1} {w2}"
        for w1 in first
        for w2 in second
        if f"{w1} {w2}" in valid_phrases
    }

# Nhập prefix nếu chưa bắt đầu
if not st.session_state.game_started:
    prefix_input = st.text_input("🔡 Nhập 2 chữ cái đầu (VD: 'bb')", max_chars=2)
    if st.button("Bắt đầu"):
        prefix = prefix_input.lower().strip()
        if len(prefix) == 2 and prefix.isalpha():
            st.session_state.prefix = prefix
            c1, c2 = prefix[0], prefix[1]
            vps = get_valid_phrases(c1, c2)
            if not vps:
                st.error("❌ Không tìm thấy cụm từ hợp lệ với 2 chữ cái này.")
            else:
                st.session_state.valid_phrases = vps
                st.session_state.game_started = True
                st.success(f"✅ Bắt đầu! Cụm từ phải có dạng: {c1.upper()}... {c2.upper()}...")
        else:
            st.error("Vui lòng nhập đúng 2 chữ cái.")
else:
    c1, c2 = st.session_state.prefix[0], st.session_state.prefix[1]
    st.info(f"🔤 Cụm từ phải bắt đầu bằng: {c1.upper()}... {c2.upper()}...")

    user_input = st.text_input("👉 Nhập cụm từ (2 từ cách nhau bằng dấu cách):")
    if st.button("Gửi"):
        phrase = user_input.strip().lower()
        if len(phrase.split()) != 2:
            st.error("❌ Phải là 2 từ cách nhau bằng dấu cách.")
        elif phrase in st.session_state.used_phrases:
            st.error("❌ Từ đã dùng.")
        elif phrase not in st.session_state.valid_phrases:
            st.error("❌ Không phải cụm từ hợp lệ.")
        else:
            st.success(f"🧍 Bạn: {phrase}")
            st.session_state.log.append(f"🧍 Bạn: {phrase}")
            st.session_state.used_phrases.add(phrase)

            # Máy phản hồi
            remaining = list(st.session_state.valid_phrases - st.session_state.used_phrases)
            if not remaining:
                st.balloons()
                st.success("🎉 Máy hết từ! Bạn thắng!")
                st.session_state.game_started = False
            else:
                bot_choice = random.choice(remaining)
                st.session_state.used_phrases.add(bot_choice)
                st.session_state.log.append(f"🤖 Máy: {bot_choice}")
                st.success(f"🤖 Máy: {bot_choice}")

    # Hiển thị lịch sử
    st.markdown("### 📜 Lịch sử lượt chơi")
    for line in st.session_state.log:
        st.markdown(line)

    # Nút chơi lại
    if st.button("🔁 Chơi lại"):
        st.session_state.used_phrases = set()
        st.session_state.valid_phrases = set()
        st.session_state.game_started = False
        st.session_state.log = []

