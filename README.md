# LLMs from Scratch — 環境構築

[Build a Large Language Model (From Scratch)](https://github.com/rasbt/LLMs-from-scratch) のハンズオン用 Python 環境です。

原典のコードは別リポジトリで clone し、このリポジトリでは **uv + uv pip** による依存関係管理のみを行います。

## 前提

- macOS / Linux（Windows でも動作する想定だが、原典の platform 条件に従う）
- Python **3.10–3.12**（本リポジトリは **3.11** 固定）
- [uv](https://docs.astral.sh/uv/) が未インストールの場合は下記手順で導入

## 1. uv のインストール

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

インストール後、シェルを再起動するか `source ~/.local/bin/env`（インストーラの案内に従う）を実行してください。

## 2. 仮想環境の作成

```bash
cd /path/to/llm-from-scratch
uv venv --python 3.11
source .venv/bin/activate
```

Python 3.11 がシステムに無い場合、uv が自動でダウンロードします。

- オプションは **`--python`**（`--pyhon` などの typo だとコマンドは失敗します）
- 既存の `.venv` を作り直す場合: `uv venv --python 3.11 --clear`
- 本リポジトリは **uv + `.venv`** を使います。**pyenv は使いません**（`.python-version` は uv 向けの 3.11 指定です）

## 3. 依存関係のインストール

```bash
uv pip install -r requirements.txt
```

主要パッケージ:

| パッケージ | 用途 |
|-----------|------|
| torch | 全章（PyTorch 実装） |
| jupyterlab | ノートブック実行 |
| tiktoken | ch02, ch04, ch05 |
| matplotlib | ch04, ch06, ch07 |
| tensorflow | ch05, ch06, ch07 |
| pandas | ch06 |
| tqdm, numpy, psutil | 各章 |

## 4. 動作確認

### 最小確認

```bash
python -c "import torch; print(torch.__version__, torch.backends.mps.is_available())"
```

Apple Silicon Mac では MPS が `True` なら GPU 加速が利用可能です。

### 原典の環境チェックスクリプト

原典を clone したうえで:

```bash
git clone --depth 1 https://github.com/rasbt/LLMs-from-scratch.git
python /path/to/LLMs-from-scratch/setup/02_installing-python-libraries/python_environment_check.py
```

## 5. 原典ノートブックとの接続

コードは別ディレクトリのため、Jupyter がこの `.venv` を使う設定が必要です。

### 方法 A（推奨）: カーネル登録

```bash
source .venv/bin/activate
python -m ipykernel install --user --name llms-from-scratch --display-name "LLMs (uv)"
```

原典ノートブックを開いたら、カーネル **LLMs (uv)** を選択してください。

### 方法 B: 原典ディレクトリから直接起動

```bash
source /path/to/llm-from-scratch/.venv/bin/activate
cd /path/to/LLMs-from-scratch
jupyter lab
```

## 6. Cursor / VS Code の設定

このリポジトリには `.vscode/settings.json` があり、次をワークスペース単位で指定しています。

- Python インタープリター: **`.venv/bin/python`**（3.11）
- ターミナル起動時の仮想環境の自動有効化
- 言語サーバー: **Pylance**
- スペルチェック: **Code Spell Checker**（辞書は `cspell.json` の `words`）

**Unknown word** が出たら、`cspell.json` の `words` に単語を追加するか、Quick Fix で追加してください。

初回または venv 作り直し後は、次も実行してください。

1. `Cmd + Shift + P` → **「Python: インタープリターを選択」**
2. **`.venv (Python 3.11.x)`** を選ぶ
3. 警告が残る場合: **「Developer: Reload Window」** でウィンドウをリロード

グローバル設定で pyenv 3.8 などが選ばれていると、このプロジェクトでも誤ったインタープリターが使われることがあります。ステータスバー左下の Python バージョン表示が **3.11** か確認してください。

## トラブルシューティング

### ターミナルで `yenv: command not found`

```
yenv shell 3.8.0
zsh: command not found: yenv
```

`yenv` は **`pyenv` の先頭 `p` が欠けたもの**です。Cursor の Python 拡張が、グローバル設定の pyenv 向けに `pyenv shell 3.8.0` をターミナルへ送る際、シェル初期化とタイミングが重なると起きることがあります。

**対処:** 上記 [§6](#6-cursor--vs-code-の設定) のとおり `.venv` をインタープリターに選ぶ。pyenv を使わないなら、ユーザー設定の `python.defaultInterpreterPath` を pyenv から外すか、`"python.terminal.activateEnvironment": false` を検討してください。

### 「無効な Python インタープリターが選択されています」

よくある原因:

| 原因 | 対処 |
|------|------|
| `uv venv --pyhon` など typo で venv が未作成 | `uv venv --python 3.11` を実行 |
| venv 再作成直後に IDE が古いパスを参照 | インタープリター再選択 → Reload Window |
| グローバル設定が pyenv 3.8 のまま | ワークスペースで `.venv` を選択（§6） |
| `.python-version` の 3.11 を pyenv が解決できない | pyenv は無視し、uv の `.venv` を使う |

venv が存在するか確認:

```bash
.venv/bin/python --version   # Python 3.11.x と表示されれば OK
```

## 注意事項

1. **Python 3.13 は非推奨** — PyTorch 互換のため 3.10–3.12 を使用
2. **TensorFlow も必要** — ch05 以降で使用（PyTorch のみでは不足）
3. **bonus 依存は後回し** — Hugging Face 連携などは必要な章で個別に追加:
   ```bash
   uv pip install transformers huggingface_hub
   ```
4. 作業時は `source .venv/bin/activate`、IDE では `.venv` インタープリター、Jupyter ではカーネル選択を忘れないこと
5. **pyenv / グローバル Python 3.8 設定と混在しない** — 本リポジトリは 3.11 の `.venv` に統一する

## 参考リンク

- [原典リポジトリ](https://github.com/rasbt/LLMs-from-scratch)
- [原典セットアップガイド](https://github.com/rasbt/LLMs-from-scratch/tree/main/setup)
- [uv ドキュメント](https://docs.astral.sh/uv/)
