

def parse_cme_row(row):
    (trade_date,product_symbol,C,fut_opt_indicator,exp_month,exp_day,exp_year,strike,I,px_open,K,L,M,px_high,O,px_low,Q,px_close,S,T,U,px_settle,volume,open_interest,Y,imp_volatility,AA) = row.split(",")

    settlement_time = trade_date 
    symbol = product_symbol
    est_vol = volume
    px_last = px_close # really?
    formatted_row = [settlement_time,
                     symbol,
                     fut_opt_indicator,
                     exp_month,
                     exp_day,
                     exp_year,
                     strike,
                     px_open,
                     px_high,
                     px_low,
                     px_last,
                     px_settle,
                     est_vol,
                     imp_volatility,
                     imp_volatility,
                     imp_volatility,
                    ] 
    return ",".join(formatted_row)
    
cme_sample_row = "010311,PY,R,P,12,0,2012,450.0000000,,.0000000,,.0000000,,.00000000,,.00000000,N,501.00000000,,.00000000,,524.00000000,.0000000,108.000000,0,.306303,CBT"

if __name__ == "__main__":
    with open("Corn.csv", "r") as f:
        rows = f.readlines()
        for r in rows:
            print parse_cme_row(r)
