# ベースイメージとして公式のPythonイメージを使用
FROM python:3.9-bullseye

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係のリストをコピーし、インストール
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# アプリケーションのコードをコピー
COPY . .

# Flaskサーバーを起動
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
