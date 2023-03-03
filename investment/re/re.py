import argparse
import json

# from investment_strategy import InvestmentStrategy


class RealEstate:
    def __init__(self, house_price, down_payment_percentage, property_tax_rate_percentage, mortgage_interest_rate, mortgage_term_years, misc_monthly_expenses, home_appreciation_rate, monthly_rental_income, extra_misc_expenses):
        self.house_price = house_price
        self.down_payment_percentage = down_payment_percentage*0.01
        self.property_tax_rate_percentage = property_tax_rate_percentage*0.01
        self.mortgage_interest_rate = mortgage_interest_rate*0.01
        self.mortgage_term_years = mortgage_term_years
        self.misc_monthly_expenses = misc_monthly_expenses
        self.home_appreciation_rate = home_appreciation_rate*0.01
        self.monthly_rental_income = monthly_rental_income
        self.extra_misc_expenses = extra_misc_expenses

    def calculate_down_payment(self):
        return self.house_price * self.down_payment_percentage

    def calculate_loan_amount(self):
        # print("loan amt: " + str(self.house_price - self.calculate_down_payment()))
        return self.house_price - self.calculate_down_payment()

    def calculate_monthly_mortgage_payment(self, loan_amount, mortgage_interest_rate):
        # Calculate the monthly mortgage payment using the formula for a fixed-rate mortgage
        # P = L[c(1 + c)^n]/[(1 + c)^n - 1]
        # where P is the monthly mortgage payment, L is the loan amount, c is the monthly interest rate,
        # and n is the number of monthly payments
        n_months = self.mortgage_term_years * 12
        c = mortgage_interest_rate / 12
        numerator = c * (1 + c)**n_months
        denominator = (1 + c)**n_months - 1
        # print("monthly mortgage amt: " +
        #      str(loan_amount * numerator / denominator))
        return loan_amount * numerator / denominator

    def calculate_total_mortgage_payment(self, n_years):
        loan_amount = self.calculate_loan_amount()
        monthly_mortgage_payment = self.calculate_monthly_mortgage_payment(
            loan_amount, self.mortgage_interest_rate)
        return monthly_mortgage_payment * 12 * n_years

    def calculate_total_expenses(self, n_years):
        # Calculate the total expenses by adding up mortgage payments, and miscellaneous expenses
        total_mortgage_payment = self.calculate_total_mortgage_payment(n_years)
        total_property_tax = self.calculate_property_tax(n_years)
        total_misc_expenses = (
            self.misc_monthly_expenses * 12 * n_years) + self.extra_misc_expenses
        return round(total_mortgage_payment + total_misc_expenses + total_property_tax, 2)

    def calculate_property_tax(self, n_years):
        return round(self.property_tax_rate_percentage * n_years * self.house_price, 2)

    def calculate_future_value(self, n_years):
        # Calculate the future value of the house after n years by compounding the home appreciation rate
        # FV = PV(1 + r)^n
        # where FV is the future value, PV is the present value (the house price), r is the annual appreciation rate,
        # and n is the number of years
        return self.house_price * (1 + self.home_appreciation_rate)**n_years

    def print(self):
        # Print the input values
        print(f"House price: ${self.house_price}")
        print(f"Down payment percentage: {self.down_payment_percentage}%")
        print(f"Tax rate percentage: {self.property_tax_rate_percentage}%")
        print(f"Mortgage interest rate: {self.mortgage_interest_rate}%")
        print(f"Miscellaneous monthly expenses: ${self.misc_monthly_expenses}")
        print(f"Home appreciation rate: {self.home_appreciation_rate}%")

    def calculate_rental_income(self, n_years):
        return self.monthly_rental_income*12*n_years

    def calculate_total_income(self, n_years):
        rental_income = self.calculate_rental_income(n_years)
        appreciation = self.calculate_future_value(n_years) - self.house_price
        return round(rental_income + appreciation, 2)

    def calculate_net_income(self, n_years):
        return round(self.calculate_total_income(n_years) - self.calculate_total_expenses(n_years), 2)

    def calculate_return_on_down_payment(self, n_years):
        down_pay = self.calculate_down_payment()
        total = down_pay + self.calculate_net_income(n_years)
        power = 1/n_years
        return (((total/down_pay) ** power) - 1)*100


if __name__ == '__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description='Calculate mortgage payments and costs')

    # Add the arguments
    parser.add_argument('--house_price', type=float,
                        help='The price of the house')
    parser.add_argument('--down_payment_percentage', type=float,
                        help='The down payment percentage  ')
    parser.add_argument('--property_tax_rate_percentage', type=float,
                        help='The tax rate percentage  ')
    parser.add_argument('--mortgage_interest_rate', type=float,
                        help='The annual mortgage interest rate  ')
    parser.add_argument('--misc_monthly_expenses', type=float,
                        help='The miscellaneous monthly expenses')
    parser.add_argument('--home_appreciation_rate', type=float,
                        help='The annual home appreciation rate  ')
    parser.add_argument('--total_time_years', type=int,
                        help='Total time in years')
    parser.add_argument('--monthly_rental_income', type=int,
                        help='Total time in years')
    parser.add_argument('--mortgage_term_years', type=int,
                        help='Total term in years for mortgage payments')
    parser.add_argument('--extra_misc_expenses', type=int,
                        help='Total misc expenses all years - repairs, selling costs, etc.')
    parser.add_argument('--config_file', type=str,
                        default='re_config.json', help='The path to the config file')

    # Parse the arguments
    args = parser.parse_args()

    # Read the config file
    with open(args.config_file, 'r') as f:
        config = json.load(f)

    # Set the arguments from the config file if not provided
    if args.house_price is None:
        args.house_price = config['house_price']
    if args.down_payment_percentage is None:
        args.down_payment_percentage = config['down_payment_percentage']
    if args.property_tax_rate_percentage is None:
        args.property_tax_rate_percentage = config['property_tax_rate_percentage']
    if args.mortgage_interest_rate is None:
        args.mortgage_interest_rate = config['mortgage_interest_rate']
    if args.misc_monthly_expenses is None:
        args.misc_monthly_expenses = config['misc_monthly_expenses']
    if args.home_appreciation_rate is None:
        args.home_appreciation_rate = config['home_appreciation_rate']
    if args.total_time_years is None:
        args.total_time_years = config['total_time_years']
    if args.monthly_rental_income is None:
        args.monthly_rental_income = config['monthly_rental_income']
    if args.mortgage_term_years is None:
        args.mortgage_term_years = config['mortgage_term_years']
    if args.extra_misc_expenses is None:
        args.extra_misc_expenses = config['extra_misc_expenses']
    re = RealEstate(
        args.house_price,
        args.down_payment_percentage,
        args.property_tax_rate_percentage,
        args.mortgage_interest_rate,
        args.mortgage_term_years,
        args.misc_monthly_expenses,
        args.home_appreciation_rate,
        args.monthly_rental_income,
        args.extra_misc_expenses)
    # re.print()
    # print(re.calculate_down_payment())
    # print(re.calculate_future_value(args.total_time_years))
    print(
        f"Future value of house: {re.calculate_future_value(args.total_time_years)}")
    print(f"total income: {re.calculate_total_income(args.total_time_years)}")
    print(
        f"total expenses: {re.calculate_total_expenses(args.total_time_years)}")
    print(
        f"Pretax income: {re.calculate_net_income(args.total_time_years)}")
    print(
        f"Rate of return on down pay (${re.calculate_down_payment()}): {re.calculate_return_on_down_payment(args.total_time_years)}%")
