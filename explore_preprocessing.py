"""前処理のサンプルコードを試すスクリプト。内容は自由に編集して実行してください。"""

import re

from text_preprocessing import download_dataset, load_raw_text

download_dataset()
raw_text = load_raw_text()

# --- ここから下を書籍のサンプルと同じように編集して試せます ---

preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
print(len(preprocessed))
print(preprocessed[:30])
