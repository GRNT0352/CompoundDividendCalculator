import matplotlib.pyplot as plt

# set by user
stock_price = 50.12
period_dividend = 0.256
initial_shares = 142.770866
periods_per_year = 12

# probably user doesn't need to touch this
num_periods = 100 * 4

# internal variables for cogitation
num_shares = initial_shares
years = 0

# matplotlib will use these
annual_dividend_payment = 0
periods = []  # plotted on x axis
total_equities = []  # plotted on y
annual_dividends = []  # plotted on y


# Define calculations
def calculate_total_equity(num_shares, stock_price):
  return num_shares * stock_price


def calculate_dividend_payment(num_shares, period_dividend):
  return num_shares * period_dividend


def calculate_new_shares(num_shares, dividend_payment):
  return dividend_payment / stock_price


def calculate_forward_dividend(periods_per_year, dividend_payment):
  return periods_per_year * dividend_payment


def calculate_equity_delta(total_equity, initial_shares, stock_price):
  return total_equity - (initial_shares * stock_price)


def calculate_years(years, period, periods_per_year):
  if period % periods_per_year == 0:
    years += 1
  return years


# print column headers
print(
  f"{'year':<3} | {'pd':<3} | {'total_eq':^11} | {'num_shares':^10} | {'div_pmnt':^9} | {'fwd_yld':^11} | {'eq_delta':^10}"
)

for period in range(1, num_periods + 1):

  # Calculate total equity before reinvesting dividend
  total_equity = calculate_total_equity(num_shares, stock_price)

  # Calculate dividend payment
  dividend_payment = calculate_dividend_payment(num_shares, period_dividend)

  # Reinvest dividend
  new_shares = calculate_new_shares(num_shares, dividend_payment)
  num_shares += new_shares

  # Calculate a flat forward dividend (4x quarterly_dividend w/ no compounding)
  forward_dividend_income = calculate_forward_dividend(periods_per_year, dividend_payment)

  # Calculate delta between current equity and calculated equity
  # "How much do I need to invest to get same yield as this period"
  equity_delta = calculate_equity_delta(total_equity, initial_shares, stock_price)

  # Calculate the number of years that have passed since 0
  years = calculate_years(years, period, periods_per_year)

  # Accumulate dividend payments
  annual_dividend_payment += calculate_dividend_payment(
    num_shares, period_dividend)

  # Append data to matplotlib lists
  periods.append(period)
  total_equities.append(calculate_total_equity(num_shares, stock_price))

  # Record annual dividend payment at the end of each year
  if period % periods_per_year == 0:
    annual_dividends.append(annual_dividend_payment)
    annual_dividend_payment = 0  # Reset for the next year

  print(
    f"{years:<4} | {period:<3} | ${total_equity:^10,.2f} | {num_shares:^10,.6f} | ${dividend_payment:8,.2f} | ${forward_dividend_income:10,.2f} | ${equity_delta:10,.2f}"
  )

# create a fancy graph
fig, ax1 = plt.subplots()

# ax1 is total value of the equity in question
color = 'tab:red'
ax1.set_xlabel('Period')
ax1.set_ylabel('Total Equity ($)', color=color)
ax1.plot(periods, total_equities, color=color)
ax1.tick_params(axis='y', labelcolor=color)

# ax2 is the $ value of the dividend per year
ax2 = ax1.twinx()  
color = 'tab:blue'
ax2.set_ylabel('Annual Dividend ($)', color=color)  
ax2.plot(periods[(periods_per_year - 1)::periods_per_year], annual_dividends, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  
plt.title('Total Equity and Annual Dividend Over Time')
plt.show()
