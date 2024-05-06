import math
from yahoo_fin.stock_info import get_data
import pandas as pd
import numpy as np
import requests
import io
import scipy
import json


def extend_x(x):
    return [x[0], x[1], x[2], 1-x[0]-x[1]-x[2]]


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def calc_risk_premium(wts, return_distr_risk_prem):
    risk_prem = (wts @ return_distr_risk_prem).item()
    return risk_prem


def get_ticker_data(
        symbol: str,
        start_date: str = "01/01/1995",
        end_date: str = "09/01/2023",
        index_as_date: bool = False,
        interval: str = "1mo"
):
    ''' date_format:"01/01/1995" '''
    return get_data(
        symbol,
        start_date=start_date,
        end_date=end_date,
        index_as_date=index_as_date,
        interval=interval
    )


def run_algorithm(data=[]):
    symbols = ["AEP", "DFSVX", "DFLVX", "FSAGX"]
    # if len(data) == 0:
    #     return
    # symbols = [entry["symbol"] for entry in data]

    GS1_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GS1&scale=left&cosd=1953-04-01&coed=2024-02-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-03-11&revision_date=2024-03-11&nd=1953-04-01"
    START_DATE = "01/01/1995"
    END_DATE = "09/01/2023"

    tickers_data = {}
    closed_values = {}
    for s in symbols:
        tickers_data[s] = get_ticker_data(s)
        closed_values[s] = tickers_data[s].iloc[-1]["adjclose"]

    gs1_data = requests.get(GS1_URL)
    fred = pd.read_csv(io.StringIO(gs1_data.text), parse_dates=["DATE"])
    fred = fred.rename(columns={"DATE": "date"})
    fred = fred.loc[(fred['date'] >= START_DATE) & (fred['date'] < END_DATE)]

    gs1_val = fred.iloc[-1]["GS1"]

    merged = fred
    for t in tickers_data:
        df = tickers_data[t]
        merged = pd.merge(
            merged, df[["date", "adjclose"]], on="date", how="inner")
        merged = merged.rename(columns={"adjclose": f"{t}_Adjusted"})

    shifted = merged.shift(12)
    for t in symbols:
        col_to_substract = f"{t}_Adjusted"
        merged[f"{t}_annual"] = (merged[col_to_substract] -
                                 shifted[col_to_substract]) / shifted[col_to_substract]
        merged[f"{t}_excess"] = merged[f"{t}_annual"] - \
            merged.shift(12)["GS1"]/100

    return_dist = {}
    for t in symbols:
        cleaned = merged[merged[f"{t}_excess"].notna()]
        return_dist[t] = (cleaned[f"{t}_excess"].mean(),
                          cleaned[f"{t}_excess"].std())

    # Calulating correlation matrix
    cols = [f"{col}_excess" for col in symbols]
    rename_dict = {}

    for col in cols:
        rename_dict[col] = col.replace("_excess", "")

    corr = merged[cols].corr()
    corr = corr.rename(index=rename_dict, columns=rename_dict)

    # Calulating variance-covariance
    var_covar = corr.copy()
    for row_label, row_data in var_covar.iterrows():
        row_std = return_dist[row_label][1]
        for col_label in var_covar.columns:
            col_std = return_dist[col_label][1]
            row_data[col_label] = row_data[col_label]*row_std*col_std

    ''' Tables, Optimization and other calculations start here! '''
    # Here we do the optimization operations.

    # Calulcate the min variance portfolio for effecient frontier's SD and riskpremium

    covar = var_covar.to_numpy()

    def objective_function(x):
        iter_weights = np.array(extend_x(x))
        return np.power((iter_weights @ covar) @ iter_weights.T, 0.5).item()

    def constraint_risk_prem(x, target):
        iter_weights = np.array(extend_x(x))
        return_distr_risk_premium = np.array(
            [[return_dist[r][0]] for r in return_dist.keys()])
        risk_prem = calc_risk_premium(iter_weights, return_distr_risk_premium)
        # print(target, risk_prem)
        return risk_prem - target

    def total_one(x):
        return (x[0] + x[1] + x[2]) - 1

    # Create the constraint object
    bounds = [(0, None), (0, None), (0, None)]

    weights_map = {}
    # Initial guess
    initial_values = np.array([0.12, 0.43, 0.23])

    # Call the minimize function
    result = scipy.optimize.minimize(
        objective_function,
        initial_values,
        method='SLSQP',
        constraints=[],
        bounds=bounds
    )

    risk_prem = np.array(extend_x(
        result.x)) @ np.array([[return_dist[r][0]] for r in return_dist.keys()])

    changing_wts = result.x

    weights_map[f"{risk_prem.item() * 100}"] = {
        "wts": result.x,
        "sd": result.fun
    }

    # print(np.array(extend_x(result.x)), np.array([[return_dist[r][0]] for r in return_dist.keys()]), )
    next_risk_prem = math.ceil(risk_prem.item() * 100)
    for val in range(next_risk_prem, next_risk_prem + 8):
        target_risk_prem = val * 0.01
        # print(target_risk_prem)
        risk_prem_eq_val = scipy.optimize.NonlinearConstraint(
            lambda x: constraint_risk_prem(x, target_risk_prem), 0, 0)
        result = scipy.optimize.minimize(
            objective_function,
            changing_wts,
            method='SLSQP',
            constraints=[risk_prem_eq_val],
            bounds=bounds,
            tol=1e-6,
            options={'maxiter': 1000})
        changing_wts = result.x
        # print("min sd:", result.fun, result.x)

        weights_map[f"{val}"] = {
            "sd": result.fun,
            "wts": result.x.tolist()
        }

        risk_prem = np.array(
            extend_x(changing_wts)
        ) @ np.array([[return_dist[r][0]] for r in return_dist.keys()])
        # print(risk_prem[0])

    data = {
        "varcovar": var_covar.to_numpy().tolist(),
        "efficient_frontier": weights_map,
        "return_distribution": np.array([[return_dist[r][0]] for r in return_dist.keys()]).tolist(),
        "closed_values": closed_values,
    }

    # print(json.dumps(data["efficient_frontier"],cls=NumpyEncoder))

    # Getting value for maximum sharpie ratio

    covar = var_covar.to_numpy()

    def objective_function(x):
        iter_weights = np.array(extend_x(x))
        return_distr_risk_premium = np.array(
            [[return_dist[r][0]] for r in return_dist.keys()])
        risk_prem = calc_risk_premium(iter_weights, return_distr_risk_premium)
        sd = np.power((iter_weights @ covar) @ iter_weights.T, 0.5).item()
        return sd/risk_prem

    # Create the constraint object
    bounds = [(0, None), (0, None), (0, None)]
    # Initial guess
    initial_values = np.array([0.12, 0.43, 0.23])

    # Call the minimize function
    result = scipy.optimize.minimize(
        objective_function, initial_values, method='SLSQP', constraints=[], bounds=bounds)

    risk_prem = np.array(extend_x(
        result.x)) @ np.array([[return_dist[r][0]] for r in return_dist.keys()])
    # print("risk prem for efficient frontier 1st line.", risk_prem)
    efficient_sd = result.fun * risk_prem
    # print("sd.", efficient_sd)
    data["optimal_weights"] = result.x
    data["max_sharpie_ratio"] = 1/result.fun
    data["max_sharpie_ratio_sd"] = efficient_sd.item()
    data["max_sharpie_ratio_risk"] = risk_prem.item()
    data["max_sharpie_ratio_expected_return"] = risk_prem.item() + gs1_val * 0.01
    # Getting values for complete portfolio

    # y, sd, return

    complete_portfolio = []
    for i in range(0, 12):
        sd = i * 0.1 * efficient_sd

        if i == 0:
            ex_return = gs1_val * 0.01
        else:
            ex_return = i * 0.1 * risk_prem + gs1_val * 0.01

        complete_portfolio.append({
            "y": i * 0.1,
            "sd": sd.item(),
            "return": ex_return.item(),
        })

    # print(complete_portfolio)

    data["complete_portfolio"] = complete_portfolio

    price_of_risk = risk_prem/efficient_sd**2
    risk_aver = 4  # this is also an arbitraty value.
    y = price_of_risk/risk_aver

    # This is the cuurent GS1 value for the current month.
    DGS1 = gs1_val*0.01
    E_rf = (1-y)*DGS1
    E_rP = y * (DGS1+risk_prem)

    expected_return = E_rf+E_rP
    riskiness = y * efficient_sd

    data["price_of_ris"] = price_of_risk.item()
    data["risk_aversion"] = risk_aver
    data["y"] = y.item()
    data["gs1"] = DGS1
    data["expected_return"] = expected_return.item()
    data["riskiness"] = riskiness.item()
    return data


data = run_algorithm([])
for key in data:
    print(key, data[key], "\n")
