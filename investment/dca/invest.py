import argparse
import math

from investment_strategy import InvestmentStrategy


class DCA(InvestmentStrategy):

    def __init__(self, initial_amount):
        self.initial_amount = initial_amount

    def init(self):
        self.yearly_balance = [self.initial_amount]
        self.amount_invested = self.initial_amount
        self.lumpsum_rate = 0

    def get_total_balance(self, monthly_investment, rate_of_return, years, n=12):
        """
        Calculate the total amount of money at the end of t years, given x amount is invested every month
        into an investment asset that compounds by r percent each year, and n is the number of times 
        the interest is compounded per year.
        """
        self.init()
        total = self.initial_amount
        self.amount_invested = self.initial_amount
        for i in range(years*n):
            total = total + monthly_investment
            monthly_return_percent = (rate_of_return/n)
            total = total * (1 + monthly_return_percent/100)
            self.amount_invested = self.amount_invested + monthly_investment
            if i != 1 and i % 12 == 1:
                self.yearly_balance.append(total)
        self.yearly_balance.append(total)
        self.lumpsum_rate = round(self._get_lumpsum_rate(total, years), 2)
        return round(total, 2)

    def _get_lumpsum_rate(self, net, years):
        return (math.pow(net/self.amount_invested, 1/years) - 1)*100

    def get_time_in_years_for_net(self, net, monthly_investment, rate_of_return, n=12):
        self.init()
        total = self.initial_amount
        self.amount_invested = self.initial_amount
        total = self.initial_amount
        months = 0
        while total < net:
            months = months + 1
            total = total + monthly_investment
            monthly_return_percent = (rate_of_return/n)
            total = total * (1 + monthly_return_percent/100)
            self.amount_invested = self.amount_invested + monthly_investment
            if months != 1 and months % 12 == 1:
                self.yearly_balance.append(total)
        self.yearly_balance.append(total)
        years = (months+1)/12
        self.lumpsum_rate = self._get_lumpsum_rate(total, years)
        return years


if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Dollar Cost Averaging')

    # Add the arguments
    # Parse the arguments
    parser.add_argument('calc', default='net', choices=[
                        'net', 'time'], help='Choose whether to calculate amount or time')
    parser.add_argument('-p', default=0, type=int, help='The principal amount')
    parser.add_argument(
        '-r', type=float, help='The annual interest rate (eg: 5.7)')
    parser.add_argument(
        '-n', type=int, help='Number of years (as an int)')
    parser.add_argument(
        '-target', default=0, type=int, help='Total target amount (as an int)')
    parser.add_argument('-m', type=float,
                        help='The monthly investment amount')
    args = parser.parse_args()
    if args.calc == "net":

        dca = DCA(args.p)
        amount = dca.get_total_balance(
            monthly_investment=args.m, rate_of_return=args.r, years=args.n)
        print(
            f"Net amount in {args.n} years (initial_inv={args.p}, monthly_inv ={args.m}, rate={args.r}): ${amount} ({dca.lumpsum_rate}% lumpsum rate)")
    elif args.calc == "time":
        dca = DCA(args.p)
        time = dca.get_time_in_years_for_net(net=args.target,
                                             monthly_investment=args.m, rate_of_return=args.r)
        print(
            f"Time taken to target {args.target} (initial_inv={args.p}, monthly_inv={args.m}, rate={args.r}): {time} years")
