import { atom } from 'recoil'

import { PriceArticles } from 'types/data/price_articles'

export type PriceState = {
  PriceArticles: PriceArticles
}

const initialState: PriceState = {
  PriceArticles: null
}

export const PriceState = atom({
  key: 'Price',
  default: initialState
})
