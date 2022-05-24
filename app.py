import pandas as pd
import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Finance Dashboard", page_icon=":bar_chart:", layout="wide")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(
        io=uploaded_file,
        engine="openpyxl",
        sheet_name="TRANSACTIONS",
    )
else:
    columns = ['Account', 'Type', 'Date', 'Value', 'Description']
    df = pd.DataFrame(columns=columns)

df.Date = pd.to_datetime(df.Date, format='%Y%m%d')
df.Date = pd.to_datetime(df.Date).dt.date

# --------- SIDEBAR ------------
st.sidebar.header("Filter Options")
account = st.sidebar.multiselect(
    "Filter by account:",
    options=df["Account"].unique(),
    default=df["Account"].unique()
)

hideTransfer = st.sidebar.checkbox(
    'Hide transfers',
    value=True
)

date = st.sidebar.date_input(
    "Filter by date",
    (date.today() - timedelta(days=30), date.today())
)

df_selection = df.query(
    "Account == @account & Date >= @date[0] & Date <= @date[1]"
)
if hideTransfer:
    df_selection = df_selection.query(
        "~Description.str.startswith('[CW] TF 0836#')"
    )

totalAllTime = float(df["Value"].sum())
totalPeriod = float(df_selection["Value"].sum())
incomePeriod = float(df_selection.loc[(df_selection.Type == 'CREDIT') & (~df_selection.Description.str.startswith('[CW] TF 0836#')), 'Value'].sum())
expensesPeriod = abs(float(df_selection.loc[(df_selection.Type == 'DEBIT') & (~df_selection.Description.str.startswith('[CW] TF 0836#')), 'Value'].sum()))

with st.container():
    left, middle, right = st.columns(3)
    with left:
        st.subheader("Balance")
        st.write(f"CAD {totalAllTime:,.2f}")
    with middle:
        st.subheader("Balance for period")
        st.write(f"CAD {totalPeriod:,.2f}")
    with right:
        st.subheader("Income x Expenses")
        st.write(f"Income:   CAD {incomePeriod:,.2f}")
        st.write(f"Expenses: CAD {expensesPeriod:,.2f}")

with st.container():
    st.write("Transactions")
    st.dataframe(df_selection)
