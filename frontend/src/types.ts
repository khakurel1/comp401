
export interface Evaluation {
    id: string
    attributes: {
        data: EvaluationData
        created_at: string
        user: string
        tickers: Ticker[]
    }
}

export interface EvaluationData {
    varcovar: number[][]
    efficient_frontier: Map<string, { wts: number[], sd: number }>
    closed_values: Map<string, number>
    optimal_weights: number[]
    max_sharpie_ratio: number
    max_sharpie_ratio_sd: number
    max_sharpie_ratio_risk: number
    max_sharpie_ratio_expected_return: number
    complete_portfolio: { y: number, sd: number, return: number }[]
    price_of_ris: number
    risk_aversion: number
    y: number
    gs1: number
    expected_return: number
    riskiness: number
}

export interface Ticker {
    name: string
    symbol: string
}

export interface Auth {
    id: string,
    type: string,
    attributes: {
        username: string,
        email: string,
    }
}

export interface JobNotifiation {
    id: string,
    type: string,
    attributes: {
        message: string,
        created_at: string,
        read: boolean
    }
}

export interface Notification {
    id: string;
    type: string;
    attributes: {
        message: string;
        created_at: string;
        read: boolean;
        success?: boolean;
    };
}
