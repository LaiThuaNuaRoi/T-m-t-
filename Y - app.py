import streamlit as st
import random
import time

# Mở rộng từ điển với danh sách từ tiế vọn thực tế
with open("vietnamese_words.txt", encoding="utf-8") as f:
    vietnamese_words = [line.strip().lower() for line in f if line.strip()]

# Đổi từ mẫu cụm từ
valid_phrases = set()
for w1 in vietnamese_words:
    for w2 in vietnamese_words:
        valid_phrases.add(f"{w1} {w2}")

st.set_page_config(page_title="🎮 Ghép Từ Có Nghĩa", layout="centered")
st.title("🎮 Game Ghép Từ Có Nghĩa")

# Thiết lập session state
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
if "player_mode" not in st.session_state:
    st.session_state.player_mode = "1P"
if "timer" not in st.session_state:
    st.session_state.timer = 10
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "player_turn" not in st.session_state:
    st.session_state.player_turn = True

def get_valid_phrases(c1, c2):
    first = [w for w in vietnamese_words if w.startswith(c1)]
    second = [w for w in vietnamese_words if w.startswith(c2)]
    return {
        f"{w1} {w2}"
        for w1 in first
        for w2 in second
        if f"{w1} {w2}" in valid_phrases
    }

# Cài đặt
with st.sidebar:
    st.header("⚙️ Cài Đặt")
    st.session_state.timer = st.slider("⏱️ Thời gian cho mỗi lượt (giây)", 5, 30, 10)
    st.session_state.player_mode = st.selectbox("🔹 Chế độ", ["1P (với máy)", "2P (người với người)"])

# Nhập prefix
if not st.session_state.game_started:
    prefix_input = st.text_input("🔡 Nhập 2 chữ cái đầu (VD: 'bb')", max_chars=2)
    if st.button("Bắt đầu"):
        prefix = prefix_input.lower().strip()
        if len(prefix) == 2 and prefix.isalpha():
            c1, c2 = prefix[0], prefix[1]
            vps = get_valid_phrases(c1, c2)
            if not vps:
                st.error("❌ Không tìm thấy cụm từ hợp lệ.")
            else:
                st.session_state.prefix = prefix
                st.session_state.valid_phrases = vps
                st.session_state.game_started = True
                st.session_state.used_phrases = set()
                st.session_state.log = []
                st.session_state.player_turn = True
                st.session_state.start_time = time.time()
                st.success(f"✅ Bắt đầu! Cụm từ: {c1.upper()}... {c2.upper()}...")
        else:
            st.error("Nhập đúng 2 chữ cái.")
else:
    c1, c2 = st.session_state.prefix[0], st.session_state.prefix[1]
    st.info(f"🔤 Cụm từ phải bắt đầu: {c1.upper()}... {c2.upper()}...")
    remaining = st.session_state.timer - int(time.time() - st.session_state.start_time)
    st.warning(f"⏳ Thời gian còn: {remaining} giây")

    if remaining <= 0:
        st.error("⏱️ Hết giờ! Người chơi " + ("1" if st.session_state.player_turn else "2/Máy") + " thua.")
        st.session_state.game_started = False
    else:
        user_input = st.text_input("👉 Nhập cụm từ (2 từ, cách nhau bằng dấu cách):")
        if st.button("Gửi"):
            phrase = user_input.strip().lower()
            if len(phrase.split()) != 2:
                st.error("❌ Phải là 2 từ.")
            elif phrase in st.session_state.used_phrases:
                st.error("❌ Từ đã dùng.")
            elif phrase not in st.session_state.valid_phrases:
                st.error("❌ Cụm từ không hợp lệ.")
            else:
                p = "Người chơi 1" if st.session_state.player_turn else ("Người chơi 2" if st.session_state.player_mode == "2P (người với người)" else "Máy")
                st.session_state.used_phrases.add(phrase)
                st.session_state.log.append(f"✅ {p}: {phrase}")
                st.session_state.player_turn = not st.session_state.player_turn
                st.session_state.start_time = time.time()

                # Lượt của máy (nếu chơi 1P)
                if not st.session_state.player_turn and st.session_state.player_mode.startswith("1P"):
                    bot_choices = list(st.session_state.valid_phrases - st.session_state.used_phrases)
                    if not bot_choices:
                        st.balloons()
                        st.success("🎉 Bạn thắng! Máy hết từ.")
                        st.session_state.game_started = False
                    else:
                        bot_choice = random.choice(bot_choices)
                        st.session_state.used_phrases.add(bot_choice)
                        st.session_state.log.append(f"🤖 Máy: {bot_choice}")
                        st.session_state.player_turn = True
                        st.session_state.start_time = time.time()

    st.markdown("### 📜 Lịch sử")
    for line in st.session_state.log:
        st.markdown(line)

    if st.button("🔁 Chơi lại"):
        for key in ["used_phrases", "valid_phrases", "game_started", "log", "prefix"]:
            st.session_state[key] = set() if isinstance(st.session_state[key], set) else False
