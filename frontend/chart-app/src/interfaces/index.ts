export type Company = {
  code: number
  name: string
  market_products_kubun: string
  industries_code: number
  industries_kubun: string
  detailed_industries_code: number
  scale_code: number
  scale_kubun: string
}

export type Price = {
  code: number
  date: string
  open_price: number
  close_price: number
  high_price: number
  low_price: number
  volume: bigint
  moving_averages5: number
  moving_averages25: number
  moving_averages75: number
  moving_averages100: number
  moving_averages200: number
}
