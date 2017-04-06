# ABOUT
入力に応じて会話を返答するプログラム。返答する内容は2chのログのなかから選ばれる。<br/>
# METHOD
2chのアンカー、被アンカーがセットで格納されたDB(1.db)をコーパスとして使用する。<br/>
1. 前処理として1.dbを形態素解析にかけて各セットの名詞、動詞の総数を記載する（db.py）。<br/>
2. 入力を形態素解析し、名詞と動詞を抜き出す。<br/>
3. 入力がどのセットに一番近いかをナイーブベイズっぽいアルゴリズムで計算する。<br/>
4. 一番近いセットのアンカーレスを出力する。
# USAGE
python conversation.py [input sentense]
# DEMO
