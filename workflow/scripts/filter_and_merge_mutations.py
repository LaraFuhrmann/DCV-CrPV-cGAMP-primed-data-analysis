#!/usr/bin/env python3

import pandas as pd
import math

def f_windows_covering_positions(row):
    return len([0 for x in [row['Frq1'], row['Frq2'], row['Frq3']] if not math.isnan(x)])

def f_windows_pass_posterior(row):
    posterior_threshold = 0.8
    return len([0 for x in [row['Pst1'], row['Pst2'], row['Pst3']] if x>=posterior_threshold])

def main(fname_crpv, fname_dcv, fname_crpv_p0, fname_out):

    # load dataframes
    # load dataframes
    df_crpv = pd.read_csv(fname_crpv)
    df_crpv = df_crpv[~df_crpv["file"].str.contains("parental")] # no parental

    df_dcv = pd.read_csv(fname_dcv)

    df_crpv_p0 = pd.read_csv(fname_crpv_p0)
    df_crpv_p0 = df_crpv_p0[df_crpv_p0["file"].str.contains("parental")] # only parental

    df = pd.concat([df_crpv_p0,df_dcv,df_crpv] ).reset_index()

    # convert columns to float
    columns_to_float = ['Frq1', 'Pst1','Frq2', 'Pst2', 'Frq3', 'Pst3', 'Fvar', 'Rvar', 'Ftot', 'Rtot']
    for col in columns_to_float:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df['coverage'] = df['Ftot'] + df['Rtot']
    df['n_var'] = df['Rvar'] + df['Fvar']
    df['freq'] = df['n_var'] / df['coverage']
    df['sample']=df['file'].str.split('/').str[-2]

    df['windows_pass_posterior'] = df.apply(f_windows_pass_posterior, axis=1).astype(float)
    df['windows_covering_positions'] = df.apply(f_windows_covering_positions, axis=1)

    # filtering
    df = df[(df['windows_covering_positions']>1)  & (df['windows_pass_posterior']>1)]

    # write to csv
    df.to_csv(fname_out)



if __name__ == "__main__":
    main(
        snakemake.input.fname_crpv,
        snakemake.input.fname_dcv,
        snakemake.input.fname_crpv_p0,
        snakemake.output.fname_out,
    )
