import numpy as np
import pandas as pd

def genData(n=30, v=3):
    t = pd.date_range(start='2021-01-01 09:30:00', periods=n, freq='min')
    allRows = []
    for x in range(v):
        mid = [100 + x]
        for i in range(1, n):
            mid.append(mid[-1] + np.random.normal(0, 0.3))
        mid = np.maximum(mid, 1)
        arr = []
        for m in mid:
            sp = np.abs(np.random.normal(0.1, 0.05))
            b = m - sp/2
            a = m + sp/2
            bs = np.random.randint(50, 200)
            az = np.random.randint(50, 200)
            arr.append([b, a, bs, az])
        tmp = pd.DataFrame(arr, columns=['bid', 'ask', 'bSize', 'aSize'])
        tmp['timestamp'] = t
        tmp['venue'] = f"V_{x}"
        allRows.append(tmp)
    df = pd.concat(allRows, ignore_index=True)
    return df

def getVwap(df):
    df['mid'] = (df['bid'] + df['ask']) / 2
    df['vol'] = df['bSize'] + df['aSize']
    gp = df.groupby('timestamp').agg({'mid':'mean','vol':'sum'}).reset_index()
    num = (gp['mid'] * gp['vol']).sum()
    den = gp['vol'].sum()
    return num / den if den != 0 else np.nan

def doTwap(df, qty, startT, endT):
    sel = (df['timestamp'] >= startT) & (df['timestamp'] <= endT)
    z = df[sel].copy()
    z.sort_values(by=['timestamp','ask'], inplace=True)
    times = sorted(z['timestamp'].unique())
    slcs = len(times)
    perSlc = qty / slcs if slcs > 0 else 0
    out = []
    for tm in times:
        r = perSlc
        sd = z[z['timestamp'] == tm].sort_values(by='ask')
        while r > 0 and len(sd) > 0:
            bv = sd.iloc[0]
            bA = bv['ask']
            bASz = bv['aSize']
            exP = bA
            if bASz <= 0:
                sd = sd.iloc[1:]
                if len(sd) == 0:
                    break
                continue
            if bASz >= r:
                act = bA + np.random.normal(0,0.02)
                fQ = r
                r = 0
                sd.at[sd.index[0], 'aSize'] = bASz - fQ
            else:
                act = bA + np.random.normal(0,0.02)
                fQ = bASz
                r -= fQ
                sd.at[sd.index[0], 'aSize'] = 0
            slp = act - exP
            out.append({'timestamp': tm, 'venue': bv['venue'], 
                        'expP': exP, 'actP': act, 'qty': fQ, 'slip': slp})
            sd = sd.sort_values(by='ask')
    return pd.DataFrame(out)

def main():
    dff = genData(n=30, v=3)
    vw = getVwap(dff)
    st = dff['timestamp'].min()
    et = dff['timestamp'].max()
    totalQ = 3000
    fills = doTwap(dff, totalQ, st, et)
    if len(fills) == 0:
        print("No fills.")
        return
    totalFill = fills['qty'].sum()
    wfp = (fills['actP'] * fills['qty']).sum() / totalFill if totalFill else np.nan
    avgSlp = fills['slip'].mean()
    tSlp = (fills['slip'] * fills['qty']).sum()
    exCost = wfp - vw
    fRate = totalFill / totalQ
    print(f"VWAP: {vw:.4f}")
    print(f"FillPrice: {wfp:.4f}")
    print(f"ExecCost: {exCost:.4f}")
    print(f"AvgSlip: {avgSlp:.4f}")
    print(f"Total Slippage (in $): {tSlp:.4f}")
    print(f"FillRate: {fRate:.2%}")
    print("\nFills:\n", fills.head(10))

if __name__ == "__main__":
    main()
