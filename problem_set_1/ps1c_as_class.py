MONTH_COUNT = 12


class RateCalculator:
    high_portion_rate = 10000
    low_portion_rate = 0

    def __init__(self, annual_salary, semi_annual_raise, annual_return, total_months,
                 total_cost, portion_down_payment=1, margin_of_difference=100):
        self.annual_salary = annual_salary
        self.month_salary = annual_salary / MONTH_COUNT
        self.semi_annual_raise = semi_annual_raise
        self.annual_return = annual_return
        self.month_return = annual_return / MONTH_COUNT
        self.total_months = total_months
        self.total_cost = total_cost
        self.portion_down_payment = portion_down_payment
        self.portion_cost = self.total_cost * self.portion_down_payment
        self.margin_of_difference = margin_of_difference

    def calculate_optimal_rate(self):

        guess_portion_rate = self._get_guess_portion_rate()
        savings = 0.0
        while abs(savings - self.portion_cost) > self.margin_of_difference:
            format_guess_portion = self._get_format_guess_portion(guess_portion_rate)
            savings = self._calculate_savings(format_guess_portion)
            if savings > self.portion_cost:
                self.high_portion_rate = guess_portion_rate - 1
            else:
                self.low_portion_rate = guess_portion_rate + 1
            if self.low_portion_rate > self.high_portion_rate:
                print("It is not possible to pay the down payment ${0} in {1} months".
                      format(self.portion_cost, self.total_months))
            guess_portion_rate = self._get_guess_portion_rate()

        print("Best saving rate for saving ${0} in {1} months is {2}".
              format(self.portion_cost, self.total_months, self._get_format_guess_portion(guess_portion_rate)))

    def _get_guess_portion_rate(self):
        return (self.high_portion_rate + self.low_portion_rate) // 2

    @staticmethod
    def _get_format_guess_portion(guess_portion_rate):
        return guess_portion_rate / 10000.0

    def _calculate_savings(self, guess_portion_rate):
        savings = 0.0
        month_savings = self._get_months_savings(guess_portion_rate)
        for month in range(1, self.total_months+1):
            if self._is_month_raised(month):
                self._raise_month_savings(month_savings)
            savings += savings * self.month_return
            savings += month_savings
        return savings

    def _get_months_savings(self, guess_portion_rate):
        return self.month_salary * guess_portion_rate

    @staticmethod
    def _is_month_raised(month):
        if month % 6 == 0:
            return True
        return False

    def _raise_month_savings(self, month_savings):
        return month_savings * (1.0 + self.semi_annual_raise)
