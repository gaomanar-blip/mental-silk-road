import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="心理絲路：雲端存檔版", page_icon="🌿", layout="centered")

# --- 2. 連接 Google Sheets ---
# 這裡會讀取你在 Streamlit Secrets 裡面設定的網址
conn = st.connection("gsheets", type=GSheetsConnection)

def load_total_km():
    """從 Google Sheet 讀取目前的總公里數"""
    try:
        # 讀取試算表，預設會讀取第一張工作表
        df = conn.read(spreadsheet=st.secrets["gsheets_url"], usecols=[0])
        # 假設數字存在第一行第一列 (A2，因為 A1 是標題)
        return float(df.iloc[0, 0])
    except Exception:
        # 如果讀取失敗（例如表格是空的），就從 0 開始
        return 0.0

def save_total_km(new_km):
    """將新的總公里數寫回 Google Sheet"""
    # 建立一個簡單的資料表，標題是 total_km
    df = pd.DataFrame({"total_km": [new_km]})
    # 更新回雲端
    conn.update(spreadsheet=st.secrets["gsheets_url"], data=df)

# --- 3. 初始化進度 (只在網頁開啟時執行一次) ---
if 'total_km' not in st.session_state:
    st.session_state.total_km = load_total_km()

# --- 4. 側邊欄：輸入區 ---
with st.sidebar:
    st.header("🏁 每日里程回報")
    st.write("記錄你今天的腳步，同步到雲端記憶。")
    
    add_km = st.number_input("今天跑了幾公里？", min_value=0.0, step=0.1)
    
    if st.button("確認並同步到 Google Sheets"):
        # 更新網頁記憶
        st.session_state.total_km += add_km
        # 同步到雲端試算表
        save_total_km(st.session_state.total_km)
        st.success(f"已存檔！目前累積：{st.session_state.total_km} km")
        st.balloons() # 每次存檔都給你一點小氣球鼓勵

    st.divider()
    if st.button("重置所有進度 (歸零)"):
        st.session_state.total_km = 0
        save_total_km(0)
        st.rerun()

# --- 5. 主畫面：旅程顯示 ---
st.title("🏃‍♀️ 心理絲綢之路：虛擬長跑")
st.markdown("### 這不僅是里程，更是與自己對話的過程。")

# 設定目標公里數
goal_km = 100.0
progress = min(st.session_state.total_km / goal_km, 1.0)

# 視覺化進度條
st.progress(progress)

# 數據儀表板
col1, col2 = st.columns(2)
col1.metric("已完成距離", f"{st.session_state.total_km} km")
col2.metric("剩餘距離", f"{max(goal_km - st.session_state.total_km, 0.0)} km")

# --- 6. 里程碑激勵 (Incentives) ---
st.divider()
st.subheader("🚩 心理里程碑")

if st.session_state.total_km >= 20:
    st.success("✅ **20km：起點的勇氣** — 你已經跨越了最艱難的開始，感受 Grounding 的力量。")

if st.session_state.total_km >= 50:
    st.info("✅ **50km：綠洲的靜謐** — 旅程過半，練習不向外求，在安靜中尋找力量。")

if st.session_state.total_km >= 80:
    st.warning("✅ **80km：終點前的呼吸** — 保持頻率，這段路你走得很漂亮。")

if st.session_state.total_km >= 100:
    st.snow() # 慶祝達成！
    st.header("🏆 恭喜完成心理絲路長跑！")
    st.image("https://images.unsplash.com/photo-1519681393784-d120267933ba", caption="這就是你翻越的高山")
    st.write("這枚獎章代表你對自我修復的承諾。")
