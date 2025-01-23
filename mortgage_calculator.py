import streamlit as st
import pandas as pd
import math

st.title("Mortgage Repayment Calculator")

#Input fields
st.write("### Input Data")
col1, col2 = st.columns(2)
home_value = col1.number_input("Home Value", min_value=0, max_value=5000000)
deposit = col1.number_input("Deposit", min_value=0, max_value=2000000)
interest_rate = col2.number_input("Interest Rate (in %)", min_value=1.0, max_value=10.0, step=0.1)
loan_term = col2.number_input("Loan Term (in years)", min_value=1, max_value=45)

#Calculate loan repayments
loan_amount = home_value - deposit
monthly_interest_rate = (interest_rate/100) / 12
number_of_payments = loan_term * 12
monthly_payment = (
        loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
        / ((1 + monthly_interest_rate) ** number_of_payments - 1))

# Repayments Display
total_payments = monthly_payment * number_of_payments
total_interest = total_payments - loan_amount

st.write("### Repayments")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
col2.metric(label="Total_Repayments", value=f"${total_payments:,.0f}")
col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")

# Creating a data-frame with the payment schedule
schedule = []
remaining_balance = loan_amount

for i in range (1, number_of_payments +1):
    interest_payment = remaining_balance * monthly_interest_rate
    principle_payment = monthly_payment - interest_rate
    remaining_balance -= principle_payment
    year = math.ceil(i/12) # Calculates the year into the loan
    schedule.append(
        [
            i,
            monthly_payment,
            principle_payment,
            interest_payment,
            remaining_balance,
            year,
        ]
    )

# Plotting the data-frame
df = pd.DataFrame(
    schedule,
    columns=["Month", "Payment", "Principle", "Interest", "Remaining Balance", "Year"],
)

# Displaying the data-frame as a chart
st.write("### Payment Schedule")
payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payments_df)
