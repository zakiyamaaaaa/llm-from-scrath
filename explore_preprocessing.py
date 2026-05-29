"""前処理のサンプルコードを試すスクリプト。内容は自由に編集して実行してください。"""

import re

from text_preprocessing import SimpleTokenizerV1, download_dataset, load_raw_text

download_dataset()
raw_text = load_raw_text()

# --- ここから下を書籍のサンプルと同じように編集して試せます ---

preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)', raw_text)
preprocessed = [item.strip() for item in preprocessed if item.strip()]
print(len(preprocessed))
print(preprocessed[:30])

all_words = sorted(set(preprocessed))
vocab_size = len(all_words)
print(vocab_size)

# 語彙を作成
vocab = {token:integer for integer,token in enumerate(all_words)}
for i, item in enumerate(vocab.items()):
    print(item)
    if i >= 50:
        break

# tokenizerの作成
tokenizer = SimpleTokenizerV1(vocab)
text = """"It's the last he painted, you know,"
Mrs. Gisburn said with pardonable pride."""
ids = tokenizer.encode(text)
print(ids)
print(tokenizer.decode(ids))