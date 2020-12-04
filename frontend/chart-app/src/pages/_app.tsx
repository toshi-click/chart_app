import 'styles/globals.scss'
// sanitize.css を読み込む
import 'sanitize.css'
// React と AppProps を読み込む
import React from 'react'
import { AppProps } from 'next/app'

// 引数に型を追加する
function MyApp({ Component, pageProps }: AppProps): JSX.Element {
  return <Component {...pageProps} />
}

export default MyApp
