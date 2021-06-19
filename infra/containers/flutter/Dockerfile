# 参考 https://qiita.com/zigenin/items/b89667c58027f53ec549
# BaseはCircle CI。android sdk, gcloudが導入済み
FROM circleci/android:api-29-node

USER root

RUN apt-get update && \
    apt-get -y install locales task-japanese && \
    locale-gen ja_JP.UTF-8 && \
    rm -rf /var/lib/apt/lists/*
ENV LC_ALL=ja_JP.UTF-8 \
    LC_CTYPE=ja_JP.UTF-8 \
    LANGUAGE=ja_JP:jp
RUN localedef -f UTF-8 -i ja_JP ja_JP.utf8

# tzdataのapt-get時にtimezoneの選択で止まってしまう対策でDEBIAN_FRONTENDを定義する
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Tokyo
RUN echo "${TZ}" > /etc/timezone && \
    rm /etc/localtime && \
    ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# コンテナのデバッグ等で便利なソフト導入しておく
RUN apt-get update \
    && apt-get -y install vim git curl wget zip unzip net-tools iproute2 iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Install firebase tools
RUN curl -sL https://firebase.tools | bash

# Install tools for easylauncher
RUN apt-get update \
    && apt-get install -y fontconfig ttf-dejavu \
    && rm -rf /var/lib/apt/lists/*

USER circleci

# Install Flutter SDK
# see. https://github.com/cirruslabs/docker-images-flutter/blob/master/sdk/Dockerfile
# versionはここ参照 https://flutter.dev/docs/development/tools/sdk/releases?tab=linux
ARG flutter_version=1.20.1
ENV FLUTTER_HOME=${HOME}/sdks/flutter \
    FLUTTER_VERSION=$flutter_version
ENV FLUTTER_ROOT=$FLUTTER_HOME

ENV PATH ${PATH}:${FLUTTER_HOME}/bin:${FLUTTER_HOME}/bin/cache/dart-sdk/bin

RUN git clone --branch ${FLUTTER_VERSION} https://github.com/flutter/flutter.git ${FLUTTER_HOME}

RUN flutter precache

RUN yes | flutter doctor --android-licenses && flutter doctor






# カスタム設定ファイルを設置
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d/nginx.conf
