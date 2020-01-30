MONTH_COUNT = 12

ANNUAL_RETURN = 0.04
MONTH_RETURN = ANNUAL_RETURN / MONTH_COUNT

SEMI_ANNUAL_RAISE = 0.07
PORTION_SAVED = 0.5
TOTAL_MONTHS = 36

TOTAL_COST = 1_000_000
PORTION_DOWN_PAYMENT = 0.25
PORTION_COST = TOTAL_COST * PORTION_DOWN_PAYMENT

MARGIN_OF_DIFFERENCE = 100


def main():
    annual_salary = get_user_input()
    month_salary = get_month_salary(annual_salary)
    calculate_best_rate(month_salary)


def get_user_input():
    annual_salary = float(input("Enter your start salary: "))
    return annual_salary


def get_month_salary(annual_calary):
    return annual_calary / MONTH_COUNT


def calculate_best_rate(month_salary):
    bisection_search_steps = 0

    high_portion_saved = 10001
    low_potion_saved = 0

    guess_portion_saved = get_portion_saved(high_portion_saved, low_potion_saved)
    savings = 0

    while abs(savings - PORTION_COST) > MARGIN_OF_DIFFERENCE:
        # Get formatted guess portion
        format_guess_portion = get_format_portion(guess_portion_saved)
        # Calculate savings
        savings = calculate_savings(month_salary, format_guess_portion)
        if savings > PORTION_COST:
            high_portion_saved = guess_portion_saved-1
        else:
            low_potion_saved = guess_portion_saved+1
        if low_potion_saved > high_portion_saved:
            print("Its not possible to pay the down payment in {0} months".format(TOTAL_MONTHS))
            return
        guess_portion_saved = get_portion_saved(high_portion_saved, low_potion_saved)
        bisection_search_steps += 1

    print("For saving ${0} in {1} months with {2} month salary your optimal rate is {3}".
          format(PORTION_COST, TOTAL_MONTHS, month_salary, get_format_portion(guess_portion_saved)))
    print("Number of bisectional search steps: {0}".format(bisection_search_steps))


def get_portion_saved(high_portion_saved, low_portion_saved):
    return (high_portion_saved + low_portion_saved) // 2


def get_format_portion(portion):
    return portion / 10000.0


def calculate_savings(month_salary, portion_saved):
    savings = 0.0

    month_savings = get_month_savings(month_salary, portion_saved)
    for month in range(1, TOTAL_MONTHS+1):
        if is_raised_month(month):
            month_savings = raise_month_savings(month_savings, SEMI_ANNUAL_RAISE)
        savings += savings * MONTH_RETURN  # add months invest return
        savings += month_savings  # add month savings

    return savings


def get_month_savings(month_salary, portion_saved):
    return month_salary * portion_saved


def is_raised_month(number_of_month):
    if number_of_month % 6 == 0:
        return True
    return False


def raise_month_savings(month_savings, raise_portion):
    return month_savings * (1.0 + raise_portion)


if __name__ == '__main__':
    main()
