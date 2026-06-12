import streamlit as st
from asari.api import Sonar

# ページのタイトルやアイコンを設定
st.set_page_config(page_title="感情診断アプリ", page_icon="😊", layout="centered")


# モデルの読み込みをキャッシュ化（ページを開くたびに再読み込みするのを防ぎ、高速化する）
@st.cache_resource
def load_model():
    return Sonar()


# アプリの起動
sonar = load_model()

# 画面のデザイン
st.title("📝 日本語 感情診断アプリ")
st.write("入力された文章がポジティブかネガティブかをAIが判定します。")

# ユーザーからのテキスト入力欄
user_input = st.text_area(
    "文章を入力してください：", placeholder="ここに文章を入力（例：今日は最高の1日だった！）"
)

# 診断ボタン
if st.button("感情を診断する", type="primary"):
    if not user_input.strip():
        st.warning("文章が入力されていません。")
    else:
        try:
            # 感情分析の実行
            res = sonar.ping(text=user_input)
            neg_score = res["classes"][0]["confidence"]
            pos_score = res["classes"][1]["confidence"]

            # 結果の判定と表示
            st.markdown("### 📊 診断結果")

            if pos_score > neg_score:
                # ポジティブな結果を緑色のボックスで表示
                st.success(f"**結果：ポジティブ 😊** (確信度: {pos_score:.2%})")
                # グラフ風のインジケーター（進捗バー）を表示
                st.progress(pos_score)
            else:
                # ネガティブな結果を赤（オレンジ）のボックスで表示
                st.error(f"**結果：ネガティブ 😢** (確信度: {neg_score:.2%})")
                st.progress(neg_score)

        except Exception as e:
            st.error(f"分析中にエラーが発生しました: {e}")