# %%
from yahoo_fin.stock_info import get_data
import pandas as pd
import numpy as np
import requests
import io
import json


def run_algorithm(data=[]):
    # symbols = ["AEP", "DFSVX", "DFLVX", "FSAGX"]
    symbols = []
    for entry in data:
        symbols.append(entry["symbol"])

    if len(data) == 0:
        return

    GS1_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?bgcolor=%23e1e9f0&chart_type=line&drp=0&fo=open%20sans&graph_bgcolor=%23ffffff&height=450&mode=fred&recession_bars=on&txtcolor=%23444444&ts=12&tts=12&width=1318&nt=0&thu=0&trc=0&show_legend=yes&show_axis_titles=yes&show_tooltip=yes&id=GS1&scale=left&cosd=1953-04-01&coed=2024-02-01&line_color=%234572a7&link_values=false&line_style=solid&mark_type=none&mw=3&lw=2&ost=-99999&oet=99999&mma=0&fml=a&fq=Monthly&fam=avg&fgst=lin&fgsnd=2020-02-01&line_index=1&transformation=lin&vintage_date=2024-03-11&revision_date=2024-03-11&nd=1953-04-01"

    START_DATE = "01/01/1995"
    END_DATE = "09/01/2023"

    tickers_data = {}
    for t in symbols:
        tickers_data[t] = get_data(
            t, start_date=START_DATE, end_date=END_DATE, index_as_date=False, interval="1mo")

    gs1_data = requests.get(GS1_URL)
    fred = pd.read_csv(io.StringIO(gs1_data.text), parse_dates=["DATE"])
    fred = fred.rename(columns={"DATE": "date"})
    fred = fred.loc[(fred['date'] >= START_DATE) & (fred['date'] < END_DATE)]

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

    print(json.dumps(return_dist))

    # Calulating correlation matrix
    cols = [f"{col}_excess" for col in symbols]
    rename_dict = {}

    for col in cols:
        rename_dict[col] = col.replace("_excess", "")

    corr = merged[cols].corr()
    corr = corr.rename(index=rename_dict, columns=rename_dict)

    print(corr.to_json())

    # Calulating variance-covariance
    var_covar = corr.copy()
    for row_label, row_data in var_covar.iterrows():
        row_std = return_dist[row_label][1]
        for col_label in var_covar.columns:
            col_std = return_dist[col_label][1]
            row_data[col_label] = row_data[col_label]*row_std*col_std

    print(var_covar.to_json())

    wts = [0.36656, 0.32678, 0.15174, 0.15492,]
    weights = np.array(
        [[0.36656],
         [0.32678],
         [0.15174],
         [0.15492]]
    )
    print(wts)


    res = weights.T @ np.power(var_covar.to_numpy() @ weights, 0.5)
    sd = res[0, 0]

    risk_prem = np.dot(weights.T, np.array(
        [[return_dist[r][0]] for r in return_dist.keys()]))[0, 0]

    sharpie_ratio = risk_prem/sd

    # TODO: need to figure out the arbitrary values
    price_of_risk = risk_prem/sd**2
    risk_aver = 4  # this is also an arbitraty value.
    y = price_of_risk/risk_aver

    DGS1 = 5.37/100     # This is the cuurent GS1 value for the current month.
    E_rf = (1-y)*DGS1
    E_rP = y * (DGS1+risk_prem)

    expected_return = E_rf+E_rP
    riskiness = y * sd
