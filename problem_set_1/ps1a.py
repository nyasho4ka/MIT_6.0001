PORTION_DOWN_PAYMENT = 0.25
ANNUAL_RETURN = 0.04
MONTH_COUNT = 12
MONTH_RETURN = ANNUAL_RETURN / MONTH_COUNT


def main():
    annual_salary, portion_saved, total_cost = get_user_input()
    # how much money need for saving
    down_payment_cost = total_cost * PORTION_DOWN_PAYMENT

    month_salary = annual_salary / MONTH_COUNT
    month_savings = month_salary * portion_saved

    number_of_months = calculate_number_of_saving_months(down_payment_cost, month_savings)

    print("You need to save your money for {0} months".format(number_of_months))


def get_user_input():
    """
    Ask user to input annual salary, portion saved and total cost of dream house
    :return:
    """
    annual_salary = float(input("Enter your annual salary: $"))
    portion_saved = float(input("Enter your portion saved (decimal): "))
    total_cost = float(input("Enter total cost of your dream house: "))
    return annual_salary, portion_saved, total_cost


def calculate_number_of_saving_months(down_payment_cost, month_savings):
    current_savings = 0.0
    num_of_months = 0
    while current_savings < down_payment_cost:
        current_savings += current_savings * MONTH_RETURN
        current_savings += month_savings
        num_of_months += 1
    return num_of_months


if __name__ == '__main__':
    main()
