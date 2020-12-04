# Frontend
Next.js + TypeScript

[参考](https://zenn.dev/higa/articles/d7bf3460dafb1734ef43)


- フレームワーク： Next.js v10.0.2 (React v17.0.1)
- 静的型付け： TypeScript v4.0.5
- PWA： next-pwa v3.1.5
- スタイリング： CSS Modules + SASS v1.29.0
- 状態管理： Recoil v0.1.2
- 静的解析＆整形： EditorConfig + ESLint v7.14.0 + Prettier v2.2.0
- テスト： Jest v26.6.3 + React Testing Library v11.2.2 + Cypress v6.0.1
- コンポーネントカタログ: Stroybook v6.1.9 (StoryShots v6.1.9 を含む)
- フックスクリプト： lint-staged v10.5.2 + husky v4.3.0


環境構築
# Next.js をセットアップ
# （現在のディレクトリで作成しますが必要に応じて変更）
docker run --rm -it -v $PWD:/tmp/next -w /tmp/next node:latest yarn create next-app .

# pages を src ディレクトリへ移動
# Next.js で v9.1 から src に pages を入れること可能になったので、src に入れる形で進めます。
sudo mkdir -p src && sudo mv pages/ src/pages & sudo mv styles/ src/styles
  
# nodeコンテナを起動しておく
cd ../containers/
docker-compose up -d
cd ../chart-app

# Next.jsで作った環境でTypeScriptを使えるようにする
docker exec -it node yarn add -D typescript @types/react @types/react-dom @types/node

# Next.js を開発モードで起動することで必要なファイルを自動生成
docker exec -it node yarn dev

# src ディレクトリ配下の js と jsx のファイルを ts と tsx に変換
find src/pages -name "_app.js" -or -name "index.js" | sed 'p;s/.js$/.tsx/' | xargs -n2 mv & find src/pages/api -name "*.js" | sed 'p;s/.js$/.ts/' | xargs -n2 mv


# PWA のモジュールをインストール
docker exec -it node yarn add --dev next-offline

  yarn dev
    Starts the development server.

  yarn build
    Builds the app for production.

  yarn start
    Runs the built app in production mode.

We suggest that you begin by typing:

  cd chart-app
  yarn dev
