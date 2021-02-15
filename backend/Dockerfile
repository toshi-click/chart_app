FROM python:3.8

# Debian set Locale
RUN apt-get update \
    && apt-get -y install locales task-japanese \
    && locale-gen ja_JP.UTF-8 \
    && rm -rf /var/lib/apt/lists/*
ENV LC_ALL=ja_JP.UTF-8
ENV LC_CTYPE=ja_JP.UTF-8
ENV LANGUAGE=ja_JP:jp
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8

# Debian set TimeZone
ENV TZ=Asia/Tokyo
RUN echo "${TZ}" > /etc/timezone \
    && rm /etc/localtime \
    && ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

# コンテナのデバッグ等で便利なソフト導入しておく
RUN apt-get update \
    && apt-get -y install vim netcat git curl wget zip unzip make sudo gcc libc-dev \
    && rm -rf /var/lib/apt/lists/*

# 環境変数を設定
# Pythonがpyc filesとdiscへ書き込むことを防ぐ
ENV PYTHONDONTWRITEBYTECODE 1
# Pythonが標準入出力をバッファリングすることを防ぐ
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# pipenvのインストール
RUN pip install pipenv

# ローカルマシンののPipfileをコンテナにコピー
COPY Pipfile ./

# Pipfile.lockを無視してPipfileに記載のパッケージをシステムにインストール
RUN pipenv install --system --skip-lock

# シェルスクリプトをコピー
COPY entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

# シェルスクリプトを実行
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
