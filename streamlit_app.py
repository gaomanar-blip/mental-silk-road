import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from PIL import Image

# --- 0. 用戶頭像設定 (妳需要替換這裡！) ---
# 請按照上面的步驟上傳圖片並獲取 "Raw" URL
# 這裡是佔位符，用戶需要替換為真實 URL
AVATAR_URL = "https://raw.githubusercontent.com/gaomanar-blip/mental-silk-road/refs/heads/data/avatar.png" # 佔位符

# --- 1. 定義行為與獎勵 (Incentive Table) ---
BEHAVIORS = {
    "🌿 練習 Grounding (5-4-3-2-1 法)": 5,
    "😶 練習不過度分享 (內在留白)": 5,
    "📝 撰寫心理自我分析/錄音": 10,
    "💐 進行花藝創作/美肌按摩": 10,
    "🫁 深度「黑暗中的呼吸」冥想": 15,
    "🏥 完成一次 Esketamine 療程回報": 20  # 專為治療設計的里程碑
}

# --- 2. 景觀演變系統 (Visual Evolution) ---
def get_landscape_and_message(km):
    if km < 20:
        return "https://images.unsplash.com/photo-1509316785289-025f5b846b35", "🌵 旅程起點：雖然滿地沙礫，但妳已經出發了。"
    elif km < 50:
        return "https://images.unsplash.com/photo-1534067783941-51c9c23ecefd", "⛰️ 翻越山脈：大起大跌是風景的一部分，呼吸不要停。"
    elif km < 80:
        return "https://images.unsplash.com/photo-1506318137071-a8e063b4b519", "🌌 繁星夜空：在最黑的夜裡，妳最能看清星光。"
    else:
        return "https://images.unsplash.com/photo-1441974231531-c6227db76b6e", "🌳 抵達綠洲：妳親手灌溉了這片森林。"

# --- 3. 雲端連線設定 ---
st.set_page_config(page_title="心理絲路：大轉化記錄", page_icon="🧘‍♀️", layout="wide")
conn = st.connection("gsheets", type=GSheetsConnection)

def load_data():
    try:
        # 假設 A 欄是 total_km, B 欄是 reflections
        df = conn.read(spreadsheet=st.secrets["gsheets_url"])
        return float(df.iloc[0, 0]), df.iloc[1:, 1].tolist() if len(df) > 1 else []
    except:
        return 0.0, []

def save_data(km, reflection):
    # 更新 A2 為總里程，並在 B 欄追加一句話
    new_data = pd.DataFrame({"total_km": [km], "reflections": [reflection]})
    conn.update(spreadsheet=st.secrets["gsheets_url"], data=new_data)

total_km, reflections = load_data()
if 'total_km' not in st.session_state:
    st.session_state.total_km = total_km

# --- 4. 側邊欄：行為與心情輸入 ---
with st.sidebar:
    st.header("✨ 今日心理補給")
    selected_actions = st.multiselect("勾選今日完成的行動：", list(BEHAVIORS.keys()))
    
    daily_gain = sum(BEHAVIORS[action] for action in selected_actions)
    
    st.divider()
    user_note = st.text_area("給未來自己的一句話 (心靈錦囊)：", placeholder="此刻的感覺是...")
    
    if st.button("同步這份進步與心情"):
        if daily_gain > 0 or user_note:
            st.session_state.total_km += daily_gain
            save_data(st.session_state.total_km, user_note)
            st.success(f"同步成功！妳為絲路前進了 {daily_gain} 公里")
            st.balloons()
            st.rerun()

# --- 5. 主畫面：動態獎勵介面 ---
img_url, stage_msg = get_landscape_and_message(st.session_state.total_km)

# 稍微調整右側比例 (1:1.2)，為頭像和指標留出更多空間
col_left, col_right = st.columns([1, 1.2]) 

with col_left:
    st.image(img_url, use_container_width=True, caption="當下的心靈景觀")
    st.info(stage_msg)

with col_right:
    # --- 100% 用戶個性化標頭 (新增) ---
    col_avatar, col_title = st.columns([1, 3])
    with col_avatar:
        # 使用 CSS 圓形頭像
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center; border-radius: 50%; overflow: hidden; width: 120px; height: 120px; border: 4px solid #f0f2f6; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                <img src="{AVATAR_URL}" alt="用戶頭像" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_title:
        st.title("🏃‍♀️ 心理絲綢之路")
        st.markdown("### 用具體行動記錄妳的身心轉化")

    st.divider()

    st.metric("累積成長能量", f"{st.session_state.total_km} km", delta=f"+{daily_gain if 'daily_gain' in locals() else 0}")
    
    progress = min(st.session_state.total_km / 100.0, 1.0)
    st.progress(progress)
    
    # 歷史錦囊回顧 (只顯示最近三句)
    st.subheader("📜 最近的心靈錦囊")
    if reflections:
        for r in reflections[-3:]:
            st.write(f"💬 *「{r}」*")
    else:
        st.write("尚無記錄，開始妳的第一步吧。")

# --- 6. 驚喜里程碑 ---
if st.session_state.total_km >= 100:
    st.snow()
    st.confetti() # 如果環境支援
    st.header("🏆 妳完成了這趟轉化旅程！")
    st.markdown("這份記錄證明了：**妳不只是倖存者，妳是自己生命的創作者。**")
