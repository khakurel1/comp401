export interface Evaluation {
    id: string
    data: any
    createdAt: string
    user: string
    tickers: Ticker[]
}

export interface Ticker {
    name: string
    symbol: string
}
