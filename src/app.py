"""Module to render stock price visualization."""
import altair as alt
import polars as pl
import streamlit as st

import stock_info
import ticker_symbol


def render() -> None:
    st.set_page_config(page_title="米国株価可視化", layout="wide")

    with st.sidebar:
        st.markdown(
            """
            ## はじめに
            株価可視化ツールです。以下のオプションから表示する日数を選択してください。
            """
        )

        st.markdown("## 表示日数の選択")

        selected_days: int = st.slider("日数", 1, 100, 20)

        st.markdown("## 株価の範囲指定")

        selected_range = st.slider("範囲を指定してください", 0.0, 1000.0, (0.0, 500.0))

    st.title("米国株価可視化")

    st.markdown(
        f"""
        ### 過去 **{selected_days}日間** の株価
        """
    )

    stack_price_df = stock_info.get_stack_price_df(selected_days)

    selected_companies = st.multiselect(
        "会社名を選択してください",
        [company.name for company in ticker_symbol.Ticker],
        ("google", "amazon", "meta", "apple", "microsoft"),
    )

    if not selected_companies:
        st.error("少なくとも1社は選択してください。")
    else:
        selected_df = stack_price_df.filter(pl.col("Name").is_in(selected_companies))
        chart = (
            alt.Chart(selected_df.to_pandas())
            .mark_line(opacity=0.8, clip=True)
            .encode(
                x="Date:T",
                y=alt.Y("Stock Price(USD):Q", stack=None, scale=alt.Scale(domain=selected_range)),
                color="Name:N",
            )
        )
        st.markdown("### 株価(USD)")
        st.altair_chart(chart, use_container_width=True)
