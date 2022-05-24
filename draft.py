import pandas as pd
import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Finance Dashboard", page_icon=":bar_chart:", layout="wide")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_excel(
        io=uploaded_file,
        engine="openpyxl",
        sheet_name="BMO",
    )
else:
    columns = ['Account', 'Type', 'Date', 'Value', 'Description']
    df = pd.DataFrame(columns=columns)

df['Date'] = pd.to_datetime(df['Date']).dt.date

print(df.dtypes)

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
        "Category != 'Transfer'"
    )

# --------- MAIN ------------
totalAllTime = float(df["Value"].sum())
totalPeriod = float(df_selection["Value"].sum())

with st.container():
    left, middle, right = st.columns(3)
    with left:
        st.subheader("Overall Balance:")
        st.subheader(f"CAD {totalAllTime:,.2f}")

    with middle:
        st.subheader("Balance over period:")
        st.subheader(f"CAD {totalPeriod:,.2f}")

with st.container():
    st.write("Transactions")
    st.table(df_selection)

hide_table_row_index = """
            <style>
            tbody th {display:none}
            .blank {display:none}
            </style>
            """
st.markdown(hide_table_row_index, unsafe_allow_html=True)
