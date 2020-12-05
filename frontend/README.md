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

# TypeScript に対応
# Next.jsで作った環境でTypeScriptを使えるようにする
docker exec -it node yarn add -D typescript @types/react @types/react-dom @types/node

### Next.js を開発モードで起動することで必要なファイルを自動生成
docker exec -it node yarn dev

### src ディレクトリ配下の js と jsx のファイルを ts と tsx に変換
find src/pages -name "_app.js" -or -name "index.js" | sed 'p;s/.js$/.tsx/' | xargs -n2 mv & find src/pages/api -name "*.js" | sed 'p;s/.js$/.ts/' | xargs -n2 mv

### App コンポーネントを変更
App コンポーネントを TypeScript に対応します。
```src/pages/_app.jsx
// React と AppProps を読み込む
import React from 'react'
import { AppProps } from 'next/app'

// 引数に型を追加する
function MyApp({ Component, pageProps }: AppProps): JSX.Element {
  // 関数の内容はそのまま
}
```

### ページコンポーネントを変更
ページコンポーネントを TypeScript に対応します。
```src/pages/index.jsx
// React と NextPage を読み込む
import React from 'react'
import { NextPage } from 'next'

// 型を追加
const Home: NextPage = () => {
  // 関数の内容はそのまま
}

// export を分離
export default Home
```

### API を変更
API を TypeScript に対応します。
```src/pages/api/hello.ts
// レスポンスの型を追加
type Response = {
  statusCode: number
  json({ name: string }): void
}

// 型を指定＆使用していない引数にアンダースコア接頭詞を追加
export default (_req: void, res: Response): void => {
  // 関数の内容はそのまま
}
```

## Document コンポーネントを追加
[Document コンポーネント](https://nextjs.org/docs/advanced-features/custom-document) を使うと、初期状態だと自動で追加される <html> や <body> に変更を加えることができます。

### Document コンポーネントを作成
```
touch src/pages/_document.jsx
```

### 作成した Document コンポーネントに以下を記述します。
```
import React from 'react'
import Document, { Html, Head, Main, NextScript } from 'next/document'

interface MyDocumentInterface {
  url: string
  title: string
  description: string
}

class MyDocument extends Document implements MyDocumentInterface {
  url = 'https://example.com'
  title = 'Demo Next.js'
  description = 'Demo of Next.js'

  render(): JSX.Element {
    return (
      <Html lang="ja-JP">
        <Head>
          {/* `<Head>` の内容は必要に応じて変更 */}
          <meta name="description" content={this.description} />
          <meta name="theme-color" content="#333" />
          <meta property="og:type" content="website" />
          <meta property="og:title" content={this.title} />
          <meta property="og:url" content={this.url} />
          <meta property="og:description" content={this.description} />
          <meta property="og:site_name" content={this.title} />
          <meta property="og:image" content={`${this.url}/ogp.png`} />
          <meta name="format-detection" content="telephone=no" />
          <meta name="twitter:card" content="summary_large_image" />
          <meta name="twitter:title" content={this.title} />
          <meta name="twitter:description" content={this.description} />
          <meta name="twitter:image" content={`${this.url}/ogp.png`} />
          <link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        </Head>
        <body>
          <Main />
          <NextScript />
        </body>
      </Html>
    )
  }
}

export default MyDocument
```

## ベース URL を設定
### TypeScript の設定を変更
TypeScript の設定にモジュールインポートのベース URL を追記します。
```tsconfig.json
{
  "compilerOptions": {
    // ベース URL を追加
    "baseUrl": "src"
  }
}
```

### 各コンポーネントを変更
各コンポーネントのモジュールインポートの指定を、ベース URL 指定に変更します。
```
sed -i '' -e 's/..\/styles/styles/' src/pages/_app.tsx & sed -i '' -e 's/..\/styles/styles/' src/pages/index.tsx
```

## PWA に対応
### インストール
PWA のモジュールをインストールします。
```
docker exec -it node yarn add next-pwa
```

### 設定ファイルの追加
touch next.config.js
```next.config.js
const withPWA = require('next-pwa')

module.exports = withPWA({
  pwa: {
    dest: 'public'
  }
})
```

### ウェブアプリマニフェストを追加
1. [Web App Manifest Generator ](https://app-manifest.firebaseapp.com/) でウェブアプリマニフェスト関連のファイルを作成します
1. 作成した manifest.json と images フォルダを public 直下に設置します

### Document コンポーネントを変更
Document コンポーネントにマニュフェストへのリンクを追記します。
```src/pages/_document.tsx
<Head>
  <link rel="manifest" href="/manifest.json" />
</Head>
```

### 無視ファイルを追加
```.gitignore
**/public/precache.*.*.js
**/public/sw.js
**/public/workbox-*.js
**/public/worker-*.js
**/public/precache.*.*.js.map
**/public/sw.js.map
**/public/workbox-*.js.map
**/public/worker-*.js.map
```

## 状態管理ライブラリを追加
### Recoil のインストール
```
docker exec -it node yarn add recoil
```
使い方は[ドキュメント](https://recoiljs.org/docs/basic-tutorial/intro/) を確認してください。

## スタイルの設定
### SASS のインストール
```
docker exec -it node yarn add -D sass
```

### SASS ファイルに変換
src/styles ディレクトリ内の CSS ファイルを SASS ファイルに変換します
```
find src/styles -name "*.css" | sed 'p;s/.css$/.scss/' | xargs -n2 mv
```

### SASS ファイルを読み込むように変更
CSS ファイルを SASS ファイルに変換しましたので、正しく読み込めるようにコンポーネントを変更します。
```
sed -i '' -e 's/\.css/\.scss/' src/pages/_app.tsx && sed -i '' -e 's/\.css/\.scss/' src/pages/index.tsx
```

## デフォルト CSS の追加
### インストール
sanitize.css をインストールします
```
docker exec -it node yarn add -D sanitize.css
```
### App コンポーネントを変更
デフォルト CSS を全体に適応する為に、App コンポーネントで sanitize.css を読み込みます。
```src/pages/_app.tsx
// sanitize.css を読み込む
import 'sanitize.css'
```

## 静的解析と整形のツールを追加
### EditorConfig の追加
```.editorconfig
# editorconfig.org
root = true

[*]
indent_style = space
indent_size = 2
end_of_line = lf
charset = utf-8
trim_trailing_whitespace = true
insert_final_newline = true

[*.md]
trim_trailing_whitespace = false
```

### Prettier の追加
インストール
```
docker exec -it node yarn add -D prettier
```
### 設定ファイルの追加
```.prettierrc.js
module.exports = {
  semi: false,
  arrowParens: 'always',
  singleQuote: true,
}
```

### ESLint の追加
ESLint の関連モジュールをインストールします。
```
docker exec -it node yarn add -D eslint eslint-plugin-react \
                                 eslint-config-prettier eslint-plugin-prettier \
                                 @typescript-eslint/parser @typescript-eslint/eslint-plugin
```
### 設定ファイルの追加
```.eslintrc.js
module.exports = {
  ignorePatterns: ['!.eslintrc.js', '!.prettierrc.js'],
  extends: [
    'eslint:recommended',
    'plugin:react/recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/eslint-recommended',
    'plugin:prettier/recommended',
    'prettier/@typescript-eslint'
  ],
  plugins: ['@typescript-eslint', 'react'],
  parser: '@typescript-eslint/parser',
  env: {
    browser: true,
    node: true,
    es6: true,
    jest: true
  },
  parserOptions: {
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true
    }
  },
  settings: {
    react: {
      version: 'detect'
    }
  },
  rules: {
    // 必要に応じてルールを追加
    'react/prop-types': 'off',
    'react/react-in-jsx-scope': 'off',
    '@typescript-eslint/no-explicit-any': 'off'
  }
}
```

### Next.js の設定ファイルを修正
Next.js の設定ファイルの先頭に eslint-disable を設定する。
```next.config.js
/* eslint-disable
   @typescript-eslint/no-var-requires
*/
```

### NPM スクリプトの追加
ESLint を実行する NPM スクリプトを追記します。
```package.json
{
  "scripts": {
    "lint": "eslint --ext .js,.jsx,.ts,.tsx --ignore-path .gitignore ."
  }
}
```
Lint実行テスト
```
docker exec -it node yarn lint
# 自動整形
docker exec -it node yarn lint --fix
```

### VSCode の設定
```.vscode/settings.json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ]
}
```

### 無視ファイルを追加
```.gitignore
# ESLint のキャッシュファイルを追加
.eslintcache
```

## テストの追加
### Jest を追加
```
# Jest 関連モジュールをインストール
docker exec -it node yarn add -D jest identity-obj-proxy

# Jest の TypeScript に関するモジュールをインストール
docker exec -it node yarn add -D ts-jest @types/jest
```
### 設定ファイルの追加
```jest.config.js
module.exports = {
  preset: 'ts-jest',
  roots: ['<rootDir>/src'],
  moduleNameMapper: {
    // CSS モックをモックする設定
    '\\.(css|scss)$': 'identity-obj-proxy',
    // pages と components ディレクトリのエイリアスを設定（必要であれば他のディレクトリも追加）
    '^(pages|components)/(.+)': '<rootDir>/src/$1/$2',
  },
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json'],
  globals: {
    'ts-jest': {
      tsconfig: {
        jsx: 'react',
      },
    },
  },
}
```

### NPM スクリプトの追加
```package.json
{
  "scripts": {
    "test": "jest src/__tests__/.*/*.test.tsx?$",
  }
}
```
### テストの追加
テストファイルを置くフォルダと、サンプルのテストファイルを作成します。
```
mkdir src/__tests__ && touch src/__tests__/Sample.test.tsx
```

```src/__tests__/Smaple.test.tsx
/// <reference types="jest" />

import React from 'react'
import Home from 'pages/index'

it('Home ページコンポーネントが存在している', () => {
  expect(Home).toBeTruthy()
})
```

### テストのテスト
```
docker exec -it node yarn test
```

### React Testing Library を追加
React Testing Library をインストールします。
```
docker exec -it node yarn add -D @testing-library/react
```
適当なテストを追記してみます。
```src/__tests__/Smaple.test.tsx
// React と React Testing Library を読み込みます
import React from 'react'
import { cleanup, render, screen } from '@testing-library/react'

// 各テスト実行後にレンダーしたコンポーネントをアンマウントする
afterEach(cleanup)

it('「Next.js!」のリンクが Next.js の公式サイトのトップページである', () => {
  render(<Home />)
  expect(screen.getByText('Next.js!').getAttribute('href')).toBe(
    'https://nextjs.org'
  )
})
```
## コンポーネントカタログの追加
コンポーネントを元にそれを組みわせてアプリケーションを作り上げていく形では、コンポーネントの一覧や状態を確認できるコンポーネントカタログはとても便利です。

### Storybook のインストール
```
docker exec -it node npx sb init
```
セットアップが終わると以下が対応されています。
- 関連ファイルのインスール
- 設定ファイルの追加
- サンプルファイルの追加
- NPM スクリプトの追記

### ESLint の設定を変更
ESLint の設定ファイルに Storybook の設定ファイルを無視しないように追記します。
```.eslintrc.js
module.exports = {
  ignorePatterns: [
    // Storybook の設定フォルダを追加する
    '!.storybook'
  ],
}
```
一度、自動整形を実行します。
```
docker exec -it node yarn lint --fix
```
いくつかのサンプルファイルでエラーがでているので修正します。
```src/stories/Header.tsx
export interface HeaderProps {
  // `{}` の型を変更する
  user?: Record<string, unknown>
}
```
```src/stories/Page.tsx
export interface PageProps {
  // `{}` の型を変更する
  user?: Record<string, unknown>
}

export const Page: React.FC<PageProps> = () => (
  <li>
    Use a higher-level connected component. Storybook helps you compose
    {/* `"` を実体参照に変更する */}
    such data from the &quot;args&quot; of child component stories
  </li>
)
```

### sass-loader をインストール
SASS を使っていれば　sass-loader をインスールします。
```
docker exec -it node yarn add -D sass-loader
```

### Storybook の設定を変更
設定ファイルにエイリアスと SASS の設定を追記します。
```.storybook/main.js
// ESLint のエラーを回避する
/* eslint-disable
    @typescript-eslint/no-var-requires
*/

const { resolve } = require('path')

module.exports = {
  webpackFinal: async (config) => {
    // SASS ファイルを読み込みるように設定する
    config.module.rules.push({
      test: /\.scss$/,
      use: ['style-loader', 'css-loader', 'sass-loader'],
      include: resolve(__dirname, '../'),
    })
    // エイリアスを設定する
    config.resolve.alias = {
      ...config.resolve.alias,
      components: resolve(__dirname, '../src/components'),
      styles: resolve(__dirname, '../src/styles'),
    }
    return config
  },
}
```
### 無視ファイルを追加
```.gitignore
# Storybook のビルドディレクトリを追加
storybook-static
```

### デフォルト CSS を追加
Storybook で表示されるコンポーネント自体に、デフォルト CSS を効かせる為に以下を追記します。
```storybook/preview.js
// デフォルト CSS を読み込む
import 'sanitize.css'
```

## コンポーネントカタログのスナップショットの追加

### StoryShots の追加
スナップショットのテストをすることで、機能追加などの際に意図しない変更が起きていないかを確認することができます。
共通コンポーネントの変更は影響範囲が大きいですので、明確に差分を確認させることでリスクを減らすことができるかと思います。

#### インストール
```
docker exec -it node yarn add -D @storybook/addon-storyshots
```
#### 設定の追加
Storybook の設定ファイルを作成します。
```
mkdir storyshots && touch storyshots/storybook.test.ts
```

```src/storybook.test.ts
import initStoryshots from '@storybook/addon-storyshots'

initStoryshots()
```
#### TS ファイルに変換
JS ファイルのままだと tsconfig.json の設定を使えずに、ファイルの読み込みエラーなどがおきるので preview.js を TS ファイルに変換します。
```
mv .storybook/preview.js .storybook/preview.ts
```
#### ファイルの読み込みに対応
サンプルのストーリーファイルで DMX と SVG のファイルを読み込んでいる為、スナップショット時にエラーがでてしまいます。

SVG の変換をするモジュールを追加します。
```
docker exec -it node yarn add -D jest-svg-transformer
```
テストの設定ファイルに MDX の変換処理 と SVG の変換処理を追加します。
```jest.config.js
module.exports = {
  // DMX と SVG の変換処理を追加
  transform: {
    '^.+\\.svg$': 'jest-svg-transformer',
    '^.+\\.jsx?$': 'ts-jest',
    '^.+\\.mdx$': '@storybook/addon-docs/jest-transform-mdx',
  },
}
```
#### NPM スクリプトの追加
スナップショットテストを実行する NPM スクリプトを追記します。
```package.json
{
  "scripts": {
    "storyshots": "jest src/storybook.test.ts",
  }
}
```
### Puppeteer storyshots の追加
Puppeteer を使いスクレイピングすることで、ストーリーごとの画像キャプチャを撮り見た目の差分を検知することができます。
#### インストール
```
docker exec -it node yarn add -D @storybook/addon-storyshots-puppeteer puppeteer
```
#### 設定の追加
Storybook の設定ファイルを作成します。
```
# 基本（PC用）の設定ファイルを作成
touch storyshots/puppeteer-storyshots.test.ts

# タブレット用の設定ファイルを作成
touch storyshots/puppeteer-storyshots-ipad.test.ts

# スマホ用の設定ファイルを作成
touch storyshots/puppeteer-storyshots-iphone8.test.ts
```
基本（PC用）の設定ファイルに以下を記述します。
```storyshots/puppeteer-storyshots.test.ts
import initStoryshots from '@storybook/addon-storyshots'
import { imageSnapshot } from '@storybook/addon-storyshots-puppeteer'

initStoryshots({
  test: imageSnapshot(),
})
```
タブレット用の設定ファイルに以下を記述します。
```storyshots/puppeteer-storyshots-ipad.test.ts
import initStoryshots from '@storybook/addon-storyshots'
import { imageSnapshot } from '@storybook/addon-storyshots-puppeteer'
import { devices } from 'puppeteer'

const customizePage = (page) => page.emulate(devices['iPad'])

initStoryshots({
  suite: 'Image storyshots: iPad',
  test: imageSnapshot({ customizePage }),
})
```
スマホ用の設定ファイルに以下を記述します。
```storyshots/puppeteer-storyshots-iphone8.test.ts
import initStoryshots from '@storybook/addon-storyshots'
import { imageSnapshot } from '@storybook/addon-storyshots-puppeteer'
import { devices } from 'puppeteer'

const customizePage = (page) => page.emulate(devices['iPhone 8'])

initStoryshots({
  suite: 'Image storyshots: iPhone 8',
  test: imageSnapshot({ customizePage }),
})
```
#### 無視ファイルを追加
```.gitignore
# Storyshots の差分ディレクトリを追加
src/storyshots/__snapshots__/__diff_output__
```
#### NPM スクリプトの追加
```package.json
{
  "scripts": {
    "puppeteer-storyshots": "jest storyshots/puppeteer-storyshots*.test.ts",
  }
}
```

## フックスクリプトの追加
TODO WSL-Docker環境で動かすために若干修正が必要なのでここは未実施

リポジトリへのコミットやプッシュの際に、事前に Lint やテストを自動実行できるようにします。
これによりプロジェクトを健全に保つことができます。
### lint-staged の追加
lint-staged は Git のステージに上っているファイルだけを Lint の対象にすることができるツールです。

#### lint-staged をインストール
```
npx mrm lint-staged
```
#### NPM スクリプトに追加
```package.json
{
  "scripts": {
    "lint-staged": "lint-staged"
  }
}
```
### husky の追加
#### husky のインストール
```
yarn add -D  husky@next
```
#### Git hooks の有効化
以下のコマンドで Git hooks を有効化します。
```
yarn husky install
```
#### フックスクリプトを追加
Git コマンド実行時に以下の処理を実行するようにします。

- コミット前にステージにあるファイルを対象に ESLint の実行
- プッシュ前にすべてのテストの実行
```
yarn husky add pre-commit "yarn lint-staged" & \
  yarn husky add pre-push "yarn test && yarn storyshots && yarn puppeteer-storyshots"
```
## 環境変数の追加
開発環境や本番環境ごとなどに、違った変数を用意することができます。それを環境変数といいます。Next.js では環境変数をデフォルトで設定できるようになっています。

### 環境変数ファイルを追加
開発環境と本番環境の環境変数ファイルを作成する。
```
touch .env.development & touch .env.production
```
作成した開発環境の環境変数ファイルに、開発サーバの URL を環境変数として用意する。
```.env.development
NEXT_PUBLIC_SITE_URL=http://localhost:3000
```
作成した本番環境の環境変数ファイルに、本番サーバの URL を環境変数として用意する。
```.env.production
NEXT_PUBLIC_SITE_URL=https://example.com
```
### 環境変数を使用する
Document コンポーネントのサイト URL に環境変数を設定します。
```src/pages/_document.tsx
class MyDocument extends Document implements MyDocumentInterface {
  // 環境変数を追加
  url = process.env.NEXT_PUBLIC_SITE_URL
}
```
