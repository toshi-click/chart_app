Next.js

環境構築
# Next.js をセットアップ
# （現在のディレクトリで作成しますが必要に応じて変更）
docker run --rm -it -v $PWD:/tmp/next -w /tmp/next node:latest npx create-next-app chart-app

# pages を src ディレクトリへ移動
$ mkdir src ; mv pages/ src/pages

# Next.js の設定ファイルを作成
$ touch next.config.js


  yarn dev
    Starts the development server.

  yarn build
    Builds the app for production.

  yarn start
    Runs the built app in production mode.

We suggest that you begin by typing:

  cd chart-app
  yarn dev
