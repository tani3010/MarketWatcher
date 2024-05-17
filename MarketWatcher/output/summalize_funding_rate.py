import pandas as pd

file = [
    'TBL_FUNDINGRATE.csv',
    'TBL_FUNDINGRATE_MONTHLY.csv',
    'TBL_FUNDINGRATE_YEARLY.csv'
]

target = [
    ['bybit', 'BTCUSD'],
    ['bybit', 'ETHUSD'],
    ['bybit', 'XRPUSD'],
    ['phemex', 'BTCUSD BTC-Margin'],
    ['phemex', 'ETHUSD ETH-Margin'],
    ['mexc', 'BTC_USD'],
    ['mexc', 'ETH_USD'],
    ['mexc', 'XRP_USD']
]

for fp in file:
    path = r'./' + fp
    df = pd.read_csv(path)
    df['funding_rate'] *= 100
    output_df = pd.DataFrame()
    for iter in target:
        _df = df[(df['exchange'] == iter[0]) & (df['product_code'] == iter[1])]
        output_df = pd.concat([output_df, _df], ignore_index=True)

    df_summ = output_df.pivot_table(index=['timestamp'], columns=['exchange', 'product_code'], values=['funding_rate'])
    output_path = r'./' + fp.replace('.csv', '_summ.csv')
    df_summ.to_csv(output_path)
    print(fp)
    print(df_summ)
