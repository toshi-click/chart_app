Next.js
https://qiita.com/syuji-higa/items/931e44046c17f53b432b
環境構築
# Next.js をセットアップ
# （現在のディレクトリで作成しますが必要に応じて変更）
docker run --rm -it -v $PWD:/tmp/next -w /tmp/next node:latest npx create-next-app chart-app

# pages を src ディレクトリへ移動
# Next.js で v9.1 から src に pages を入れること可能になったので、src に入れる形で進めます。
cd chart-app
mkdir src ; mv pages/ src/pages

# Next.jsで作った環境でTypeScriptを使えるようにする
docker exec -it node yarn add --dev typescript @types/react @types/react-dom @types/node

# Next.js の設定ファイルを作成
touch next.config.js

# Next.js を開発モードで起動することで必要なファイルを自動生成
docker exec -it node yarn dev

# src ディレクトリ配下の js と jsx のファイルを ts と tsx に変換
find src -name "*.js" | sed 'p;s/.js$/.tsx/' | xargs -n2 mv

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
