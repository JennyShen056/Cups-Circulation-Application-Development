import mysql.connector
from mysql.connector import Error
import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import altair as alt
import datetime


def create_db_connection(host_name, user_name, user_password, user_port, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port=user_port,
            database=db_name,
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


connection = create_db_connection(
    os.getenv("AWS_CUPADVENTURE_HOSTNAME"),
    os.getenv("AWS_CUPADVENTURE_USERNAME"),
    os.getenv("AWS_CUPADVENTURE_PASSWORD"),
    os.getenv("AWS_CUPADVENTURE_PORT"),
    "cup_adventure",
)

# fetch the table names from the database
cursor = connection.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
tables = [table[0] for table in tables]



st.header("Customer Analytics for 2022")

st.subheader("Active Users by Month")
query_customer_2 = "SELECT month(transaction_date) as Month, count(distinct customer_id) as active_user FROM transactions_log WHERE transaction_status = 'Borrowed' GROUP BY month(transaction_date)"
df_customer_2 = pd.read_sql(query_customer_2, connection)

# create an altair line chart to show x:Month, y:Active_Users from df_metric_4
customer_line_chart = (
    alt.Chart(df_customer_2)
    .mark_bar()
    .encode(
        x=alt.X(
            "Month:N",
            title="Month",
            axis=alt.Axis(labelAngle=-0),
            scale=alt.Scale(zero=False),
        ),
        y=alt.Y("active_user:Q", title="Active Users", scale=alt.Scale(zero=False)),
        tooltip=[
            alt.Tooltip("Month", title="Month"),
            alt.Tooltip("active_user:Q", title="Active Users"),
        ],
    )
    .interactive()
)
st.altair_chart(customer_line_chart, use_container_width=True)



st.subheader("Current User Growth Rate")
query_growth_rate = "select month(join_date) as Month, count(customer_id) as count, (count(customer_id)-lag(count(customer_id), 1) over (order by month(join_date)))/lag(count(customer_id), 1) over (order by month(join_date)) as growth from cup_adventure.customers_db group by 1 order by 1"
query_growth_rate = pd.read_sql(query_growth_rate, connection)
growth_rate=alt.Chart(query_growth_rate).mark_line().encode(x='Month:N',y='growth:Q')
st.altair_chart(growth_rate)




st.subheader("Average Users per Cup")
query_customer_unique_users_per_cup = "SELECT month(transaction_date) as Month, count(customer_id)/count(distinct cup_id) as unique_users_per_cup FROM cup_adventure.transactions_log GROUP BY month(transaction_date)"
query_customer_unique_users_per_cup = pd.read_sql(query_customer_unique_users_per_cup, connection)
customer_unique_users_per_cup=alt.Chart(query_customer_unique_users_per_cup).mark_line().encode(x='Month:N',y='unique_users_per_cup:Q')
st.altair_chart(customer_unique_users_per_cup)






st.subheader("Number of Active Cafe Distributing the Cups")
query_customer_4 = "SELECT month(transaction_date) as Month, count(distinct vendor_id) as active_vendor FROM transactions_log WHERE transaction_status = 'Borrowed' GROUP BY month(transaction_date)"
df_customer_4 = pd.read_sql(query_customer_4, connection)
unique_cafe=alt.Chart(df_customer_4).mark_line().encode(x='Month:N',y='active_vendor:Q')
st.altair_chart(unique_cafe)







st.subheader("Cups Sold")
query_customer_sold = "SELECT month(transaction_date) as Month, count(customer_id) as bought FROM transactions_log WHERE transaction_status = 'Bought' GROUP BY month(transaction_date)"
query_customer_sold = pd.read_sql(query_customer_sold, connection)
cup_sold=alt.Chart(query_customer_sold).mark_line().encode(x='Month:N',y='bought:Q')
st.altair_chart(cup_sold)




st.subheader("Cups Circulation Amount Per Month")
query_Circulation = "SELECT month(transaction_date) as Month, count(customer_id) as circulation FROM transactions_log WHERE transaction_status = 'Returned' GROUP BY month(transaction_date)"
query_Circulation = pd.read_sql(query_Circulation, connection)
cup_Circulation=alt.Chart(query_Circulation).mark_line().encode(x='Month:N',y='circulation:Q')
st.altair_chart(cup_Circulation)



st.subheader("Unique Cups by Month")

query_customer_1 = "SELECT month(join_date) as Month, COUNT(distinct customer_id) as new_user FROM customers_db GROUP BY month(join_date);"
df_customer_1 = pd.read_sql(query_customer_1, connection)

query_customer_3="SELECT month(transaction_date) as Month, count(distinct cup_id) as unique_cup FROM transactions_log GROUP BY month(transaction_date)"
df_customer_3=pd.read_sql(query_customer_3, connection)




unique=alt.Chart(df_customer_3).mark_line().encode(x='Month:N',y='unique_cup:Q')


st.altair_chart(unique)


st.subheader("New Users by Month")
# create an altair chart to show x:Month, y:new_user from df_metric_3
customer_chart = (
    alt.Chart(df_customer_1)
    .mark_bar()
    .encode(
        x=alt.X("Month:N", title="Month", axis=alt.Axis(labelAngle=-0)),
        y=alt.Y("new_user:Q", title="New Users"),
        tooltip=[
            alt.Tooltip("Month", title="Month"),
            alt.Tooltip("new_user:Q", title="New Users"),
        ],
)
    .interactive()
)
st.altair_chart(customer_chart, use_container_width=True)


connection.close()