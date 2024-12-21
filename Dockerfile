FROM python:3.12-bullseye

# 作業ディレクトリの設定
WORKDIR /workspace

# プロジェクトに必要なファイルをコピー
COPY ./ /workspace/


# 環境変数の設定
ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME="/root/.local" \
    PYTHONUNBUFFERED=1 \
    PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONPATH=/workspace/src

ENV PATH="$POETRY_HOME/bin:$PATH"


# 必要なツールのインストールとPoetryのインストール
RUN apt-get update \
 && apt-get install -y default-mysql-client vim curl \
 && apt-get upgrade -y \
 && rm -rf /var/lib/apt/lists/* \
 && curl -sSL https://install.python-poetry.org | python3 - \
 && poetry config virtualenvs.create false \
 && poetry install \
 && poetry add "uvicorn[all]" \


