"""Module to get stock price data from yfinance."""
import polars as pl
import streamlit as st
import yfinance as yf

from src import ticker_symbol


@st.cache_data
def get_stack_price_df(displayed_days: int) -> pl.DataFrame:
    stack_price_df = pl.DataFrame()
    for company in ticker_symbol.Ticker:
        tkr = yf.Ticker(company.value)
        hist_df = tkr.history(period=f"{displayed_days}d")
        hist_df = pl.from_pandas(hist_df, include_index=True)
        hist_df = hist_df.select(("Date", "Close")).rename({"Close": "Stock Price(USD)"})
        company_df = pl.DataFrame({"Name": [company.name] * len(hist_df)})
        hist_df = pl.concat((hist_df, company_df), how="horizontal")
        stack_price_df = pl.concat((stack_price_df, hist_df))
    return stack_price_df
