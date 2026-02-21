import streamlit as st
import streamlit.components.v1 as components
import random
import time

# --- ページ設定 (モバイルUXの要) ---
st.set_page_config(
    page_title="元恋人年収予測 | 市場価値を残酷に判定", 
    page_icon="💔", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# GA4 トラッキングコードの埋め込み
ga_code = """
<script async src="https://www.googletagmanager.com/gtag/js?id=G-1NSXSB68RH"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-1NSXSB68RH');
</script>
"""
components.html(ga_code, height=0, width=0)

# --- カスタムCSS (スマホ最適化 & 映え) ---
st.markdown("""
<style>
    /* 全体のフォント・行間調整 */
    html, body, [class*="css"]  {
        font-family: 'Helvetica Neue', Arial, 'Hiragino Kaku Gothic ProN', 'Hiragino Sans', Meiryo, sans-serif;
    }
    
    /* フォーム入力のラベルを太く */
    .stNumberInput label, .stSelectbox label, .stRadio label, .stSlider label {
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }

    /* 巨大判定ボタン (スマホで親指で押しやすい) */
    .stButton > button {
        width: 100%;
        border-radius: 50px;
        height: 4rem;
        font-size: 1.4rem !important;
        background: linear-gradient(135deg, #ff4b4b 0%, #ff8f8f 100%);
        color: white;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
        transition: 0.2s;
        margin-top: 10px;
    }
    .stButton > button:active {
        transform: scale(0.95);
    }

    /* 結果カードの装飾 (スクショ映え用) */
    .result-card {
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 30px;
        border: 4px solid #f0f2f6;
    }
    .win-card { background-color: #e8f5e9; border-color: #4caf50; }
    .loss-card { background-color: #ffebee; border-color: #f44336; }
    .draw-card { background-color: #fff8e1; border-color: #ffc107; }
    
    .status-text { font-size: 1.2rem; font-weight: bold; margin-bottom: 5px; }
    .amount-diff { font-size: 4rem; font-weight: 900; line-height: 1; margin: 10px 0; }
    .unit { font-size: 1.5rem; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 煽りテキスト辞書 (9パターンの刃) ---
persona_texts = {
    "K": {
        "lose": (
            "ファクトベースでお伝えします。対象者の現在の世帯年収ポテンシャルに対し、あなたの生涯賃金は致命的なショートを起こしています。"
            "感情で負けを認めるか、今すぐ市場価値を再定義して数値をひっくり返すか。過去のサンクコスト（埋没費用）に執着する暇があるなら、"
            "戦略的なキャリアピボットを実行してください。"
        ),
        "win": (
            "素晴らしいROI（投資対効果）です。あの時の損切り判断は、金融工学的に見ても大正解でした。"
            "対象者の市場価値が頭打ちになる中、あなたのステータスは上昇気流に乗っています。"
            "次のフェーズは、現在のあなたの高いバリュエーション（企業価値）に相応しい、より上位レイヤーのパートナーとのM&A（結婚）です。"
        ),
        "draw": (
            "完全な均衡状態、つまり『どんぐりの背比べ』です。対象者とあなたは現在、同じコモディティ（代替可能）市場で停滞しています。"
            "このレッドオーシャンから抜け出すためのカタリスト（相場を動かす材料）が欠如しています。市場価値を劇的に上げるか、"
            "より優秀なパートナーを獲得するか、至急アクションを起こしてください。"
        )
    },
    "Reiko": {
        "lose": (
            "ちょっとあんた、いつまでそんな相手の年収引きずってんのよ！"
            "向こうは上層階に上がってんのに、あんたはまだそこでうずくまってる気？悔しくないの？"
            "泣いてる暇があったら、さっさと自分の顔洗って、自分の力で稼ぎなさい！"
            "あんたのポテンシャル、こんな所で腐らせるんじゃないわよ！"
        ),
        "win": (
            "あら、圧勝じゃないの！あの時別れて本当に正解だったわね。"
            "向こうはもうあんたの手の届かない（というか触りたくもない）レベルで燻ってるわよ。"
            "さあ、過去の答え合わせはこれで終わり！今のあんたなら、もっとずっとイイ物件（男/女）が選び放題なんだから、"
            "とっとと次のステージに行きなさい！"
        ),
        "draw": (
            "なーに仲良く同じような底辺這いつくばってんのよ。類は友を呼ぶってやつ？"
            "『あいつも私と同じくらいか、安心♡』じゃないのよ！"
            "そんな低い次元で張り合ってるから、いつまで経っても突き抜けられないの。"
            "過去を気にする前に、自分の未来の心配をしなさいな！"
        )
    },
    "Cassandra": {
        "lose": (
            "解析完了。資本主義社会における明確な劣後が確認されました。"
            "あなたが現在の労働環境に残留した場合、対象者との経済的格差を逆転する確率は0.04%未満です。"
            "警告：このままでは自己実現の維持が困難になります。直ちに現在のエコシステムを放棄し、"
            "上位のハイクラス労働環境（転職）へマイグレーション（移行）することを強く推奨します。"
        ),
        "win": (
            "解析完了。対象者に対する経済的優位性が証明されました。"
            "対象者のスペックは既に陳腐化フェーズに入っています。これ以上の比較演算はリソースの無駄です。"
            "推奨アクション：現在の獲得資本をテコにし、自身のパラメータに合致した上位10%の"
            "ハイクラス・ヒューマンリソース（結婚相手）の確保へリソースを全振りしてください。"
        ),
        "draw": (
            "解析完了。両者のパラメータは統計的誤差の範囲内で一致しています。"
            "双方ともに特筆すべき経済的優位性は認められず、現状維持バイアスに囚われています。"
            "状況を打破するためには、労働市場での急激な価値向上、あるいは上位スペック個体とのマッチングという、"
            "外部からの強烈なパラダイムシフトが必要です。"
        )
    }
}

# --- 判定ロジック (キャッシュ化で計算効率UP) ---
@st.cache_data
def estimate_ex_salary(age, industry, tier):
    # 業界別ベース年収 (万円)
    industry_base = {
        "総合商社": 600, "IT・通信": 480, "金融・保険": 500, 
        "メーカー": 450, "マスコミ・広告": 550, "医療・福祉": 420, 
        "サービス・飲食": 350, "公務員": 400, "その他": 400
    }
    tier_mult = {
        "誰もが知る大企業": 1.3,
        "有名な中堅・メガベンチャー": 1.1,
        "名もなき中小・スタートアップ": 0.9
    }
    
    base = industry_base.get(industry, 400)
    mult = tier_mult.get(tier, 1.0)
    
    # 年齢係数 (25歳を1.0とし、1歳ごとに約4%上昇)
    age_factor = 1.0 + (age - 25) * 0.04
    
    result = base * mult * age_factor
    # 適度な揺らぎ（±3%）
    noise = random.uniform(0.97, 1.03)
    result = result * noise
    
    # 下1桁（10万円単位）で丸める
    return int(round(result, -1))

# --- Session State 初期化 ---
if 'result_ready' not in st.session_state:
    st.session_state.result_ready = False
    st.session_state.user_salary_val = 0
    st.session_state.ex_salary_val = 0
    st.session_state.diff_val = 0

# --- メイン画面 ---
st.title("💔 元恋人・年収エスティメーター")
st.markdown("あの時別れたのは正解だった？ あなたと元恋人の「現在の市場価値」を残酷に比較判定します。")
st.divider()

# --- 入力セクション ---
with st.container():
    st.subheader("👤 あなたの情報")
    u_age = st.slider("あなたの年齢", 20, 50, 28)
    u_salary = st.number_input("現在の年収 (万円)", 200, 3000, 450, step=10)
    u_ind = st.selectbox("あなたの業界", ["IT・通信", "メーカー", "総合商社", "金融・保険", "医療・福祉", "サービス・飲食", "公務員", "その他"])

st.write("") 

with st.container():
    st.subheader("👻 元恋人の情報")
    ex_age = st.slider("元恋人の年齢", 20, 50, 28, key="ex_age_slider")
    ex_ind = st.selectbox("元恋人の業界", ["総合商社", "IT・通信", "金融・保険", "メーカー", "マスコミ・広告", "医療・福祉", "サービス・飲食", "公務員", "その他"])
    ex_tier = st.radio("企業規模感", ["誰もが知る大企業", "有名な中堅・メガベンチャー", "名もなき中小・スタートアップ"], horizontal=True)

st.divider()

persona = st.radio(
    "🗡️ 誰に結果を突きつけられたいですか？",
    ("① 冷徹な戦略コンサル「K」", "② 新宿二丁目のママ「麗子」", "③ 絶望予測AI「カサンドラ」"),
    horizontal=False
)

# --- 判定アクション ---
if st.button("🔥 市場価値を判定する"):
    # エッジケース・エラーハンドリング
    if u_salary >= 3000:
        st.error("【判定不能】年収3000万円以上の富裕層がこんな下世話なアプリで遊んでいるはずがありません。真実を入力してください。")
    elif u_salary <= 100:
        st.error("【警告】現代日本においてその年収は生存危機です。元恋人の心配をしている場合ではありません。")
    elif u_age > 50 and ex_age < 25:
        st.error("【通報】年齢差がありすぎます。それは本当に「元恋人」ですか？")
    else:
        with st.spinner('ビッグデータと市場動向を解析中...'):
            time.sleep(2) 
            ex_estimated = estimate_ex_salary(ex_age, ex_ind, ex_tier)
            st.session_state.user_salary_val = u_salary
            st.session_state.ex_salary_val = ex_estimated
            st.session_state.diff_val = u_salary - ex_estimated
            st.session_state.result_ready = True

# --- 結果表示セクション ---
if st.session_state.result_ready:
    st.divider()
    diff = st.session_state.diff_val
    ex_sal = st.session_state.ex_salary_val
    u_sal = st.session_state.user_salary_val
    
    # 勝敗ステータスの決定（±20万円以内は引き分けとする）
    if diff < -20:
        status_key = "lose"
        status_label = "完全敗北"
        card_class = "loss-card"
        status_color = "#f44336"
        diff_prefix = ""
    elif diff > 20:
        status_key = "win"
        status_label = "圧倒的勝利"
        card_class = "win-card"
        status_color = "#4caf50"
        diff_prefix = "+"
    else:
        status_key = "draw"
        status_label = "引き分け（停滞）"
        card_class = "draw-card"
        status_color = "#ffc107"
        diff_prefix = "±"

    # 映え判定カード (HTML)
    st.markdown(f"""
    <div class="result-card {card_class}">
        <div class="status-text" style="color: {status_color};">ーー 判定結果：{status_label} ーー</div>
        <div class="amount-diff">{diff_prefix}{abs(diff)}<span class="unit"> 万円</span></div>
        <p style="margin: 0; color: #666; font-weight: bold;">（元恋人との推定格差）</p>
    </div>
    """, unsafe_allow_html=True)

    # 補足メトリクス
    c1, c2 = st.columns(2)
    c1.metric("あなたの年収", f"{u_sal} 万円")
    c2.metric("元恋人の推定年収", f"{ex_sal} 万円", delta=f"{diff_prefix}{abs(diff)} 万円" if diff != 0 else "0 万円")

    # キャラクターメッセージの呼び出し
    if "K" in persona:
        char_key = "K"
        char_name = "冷徹な戦略コンサル「K」"
    elif "麗子" in persona:
        char_key = "Reiko"
        char_name = "新宿二丁目のママ「麗子」"
    else:
        char_key = "Cassandra"
        char_name = "絶望予測AI「カサンドラ」"
        
    st.subheader(f"💬 {char_name}からの言葉")
    msg = persona_texts[char_key][status_key]
    st.info(msg)

    # SNSシェア誘導
    st.write("")
    share_msg = f"元恋人との年収差は {diff_prefix}{abs(diff)}万円 でした！ 判定は「{status_label}」。 #元恋人年収予測"
    st.markdown(f"""
    <a href="https://twitter.com/intent/tweet?text={share_msg}" target="_blank">
        <button style="width:100%; border-radius:10px; padding:12px; background-color:#000; color:#fff; border:none; font-weight:bold; cursor:pointer;">
            𝕏 で結果をシェアして見せつける
        </button>
    </a>
    """, unsafe_allow_html=True)

    # --- アフィリエイト導線 (CTR最大化) ---
    st.divider()
    st.subheader("🚀 未来をアップデートする")
    
    if status_key == "lose" or status_key == "draw":
        st.warning("このまま負け組で終わりますか？ 逆転の一手を。")
        st.link_button("🔥 元恋人を見返す『年収100万UP転職』", "https://example.com/career", use_container_width=True)
        st.link_button("💎 格上と出会える『審査制・婚活アプリ』", "https://example.com/konkatsu", use_container_width=True)
    else:
        st.success("勝者の余裕。さらなる高みへ。")
        st.link_button("✨ あなたに相応しい『極上ハイクラス婚活』", "https://example.com/premium", use_container_width=True)
        st.link_button("📈 資産運用で圧倒的な差を広げる", "https://example.com/invest", use_container_width=True)

    st.caption("※判定結果は統計データに基づいた推定であり、実在の人物を特定するものではありません。")
