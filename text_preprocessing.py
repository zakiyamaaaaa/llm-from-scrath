"""テキストデータの取得と前処理。"""

import os
import re
import urllib.request

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATASET_PATH = os.path.join(DATA_DIR, "the-verdict.txt")
DATASET_URL = (
    "https://raw.githubusercontent.com/rasbt/"
    "LLMs-from-scratch/main/ch02/01_main-chapter-code/"
    "the-verdict.txt"
)

TOKEN_SPLIT_PATTERN = r'([,.:;?_!"()\']|--|\s)'


def download_dataset(file_path: str = DATASET_PATH) -> str:
    """データセットをダウンロードする（既に存在する場合はスキップ）。"""
    if os.path.exists(file_path):
        return file_path

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    urllib.request.urlretrieve(DATASET_URL, file_path)
    return file_path


def load_raw_text(file_path: str = DATASET_PATH) -> str:
    """テキストファイルを読み込む。"""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def preprocess_text(text: str) -> list[str]:
    """単語・句読点・空白でテキストをトークン化する。"""
    tokens = re.split(TOKEN_SPLIT_PATTERN, text)
    return [item.strip() for item in tokens if item.strip()]


def build_vocab(tokens: list[str], *, with_special_tokens: bool = False) -> dict[str, int]:
    """ユニークトークンから語彙（token → id）を構築する。"""
    all_tokens = sorted(set(tokens))
    if with_special_tokens:
        all_tokens.extend(["<|endoftext|>", "<|unk|>"])
    return {token: integer for integer, token in enumerate(all_tokens)}


class SimpleTokenizerV1:
    """語彙に含まれるトークンのみを ID に変換するトークナイザ。"""

    def __init__(self, vocab: dict[str, int]) -> None:
        # encodeメソッドとdecodeメソッドでアクセスできるように語彙をクラス属性として格納
        self.str_to_int = vocab
        # トークンIDを元のテキストトークンにマッピングする逆引き語彙を作成
        self.int_to_str = {i: s for s, i in vocab.items()}

    def encode(self, text: str) -> list[int]:
        preprocessed = preprocess_text(text)
        return [self.str_to_int[s] for s in preprocessed]

    def decode(self, ids: list[int]) -> str:
        text = " ".join(self.int_to_str[i] for i in ids)
        text = re.sub(r'\s+([,.?!"\'])', r'\1', text)
        return text


class SimpleTokenizerV2:
    """未知語を <|unk|> に置き換えるトークナイザ。"""

    def __init__(self, vocab: dict[str, int]) -> None:
        self.str_to_int = vocab
        self.int_to_str = {i: s for s, i in vocab.items()}

    def encode(self, text: str) -> list[int]:
        preprocessed = preprocess_text(text)
        preprocessed = [
            item if item in self.str_to_int else "<|unk|>"
            for item in preprocessed
        ]
        return [self.str_to_int[s] for s in preprocessed]

    def decode(self, ids: list[int]) -> str:
        text = " ".join(self.int_to_str[i] for i in ids)
        text = re.sub(r'\s+([,.:;?!"()\'])', r'\1', text)
        return text


def main() -> None:
    file_path = download_dataset()
    raw_text = load_raw_text(file_path)

    print(f"Total number of characters: {len(raw_text)}")
    print(raw_text[:99])

    preprocessed = preprocess_text(raw_text)
    print(preprocessed[:30])
    print(f"Total number of tokens: {len(preprocessed)}")

    vocab = build_vocab(preprocessed)
    print(f"Vocabulary size: {len(vocab)}")

    tokenizer_v1 = SimpleTokenizerV1(vocab)
    sample = (
        '"It\'s the last he painted, you know," '
        "Mrs. Gisburn said with pardonable pride."
    )
    ids = tokenizer_v1.encode(sample)
    print(f"Encoded IDs: {ids}")
    print(f"Decoded: {tokenizer_v1.decode(ids)}")

    vocab_with_special = build_vocab(preprocessed, with_special_tokens=True)
    tokenizer_v2 = SimpleTokenizerV2(vocab_with_special)
    unknown_sample = "Hello, do you like tea. Is this-- a test?"
    ids_v2 = tokenizer_v2.encode(unknown_sample)
    print(f"Unknown-word sample IDs: {ids_v2}")
    print(f"Decoded: {tokenizer_v2.decode(ids_v2)}")


if __name__ == "__main__":
    main()
