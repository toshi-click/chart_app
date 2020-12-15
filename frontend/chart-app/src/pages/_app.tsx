import 'styles/globals.scss'
// sanitize.css を読み込む
import 'sanitize.css'
// React と AppProps を読み込む
import React from 'react'
import { AppProps } from 'next/app'

import { RecoilRoot } from 'recoil'

// 引数に型を追加する
function MyApp({ Component, pageProps }: AppProps): JSX.Element {
  return (
    <RecoilRoot>
      <Component {...pageProps} />
    </RecoilRoot>
  )
}

export default MyApp
