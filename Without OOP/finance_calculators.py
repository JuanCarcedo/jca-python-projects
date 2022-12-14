"""
    By: Juan Carcedo Aldecoa
    Date: 07/12/2022
    Description:
        This program calculates the interest of a loan or of an investment based
        on user selection.
"""
# IMPORTS =====
from math import pow


def calculate_loan_interest(present_value: float = 0,
                            interest_rate_yearly: float = 0,
                            months_for_repayment: int = 0) -> None:
    """
    Calculation of monthly repayment of a loan.
    to_repay_monthly = (i * P) / (1 - (1 + i) ^ ( -n ))
    :param present_value: Actual value of the house today (P)
    :param interest_rate_yearly: Will be used to calculate the monthly interest. (i) = annual rate / 12
    :param months_for_repayment: Number of months over which the loan will be repaid (n)
    :return:
    """
    # Calculate rate per month to be used in the repayment monthly
    rate_per_month = interest_rate_yearly / 12
    to_repay_monthly = (rate_per_month * present_value) / (1 - pow((1 + rate_per_month), (months_for_repayment * -1)))
    # Calculation of the total interest paid (nice to have)
    interest_paid = (to_repay_monthly * months_for_repayment) - present_value
    # Output presentation and display
    # Note ":," format introduces commas "," 1000 -> 1,000
    # Quantities rounded in format to 2 decimals ":.2f"
    print('\n\n+-----------------------------------------------------+')
    print('+------------- Loan calculation complete -------------+')
    print('+- Inputs: -+')
    print(f'+ Present value of the house: {present_value:,}')
    print(f'+ Interest Rate: {(interest_rate_yearly * 100)}%')
    print(f'+ Loan periods in months: {months_for_repayment}')
    print('+- End result: -+')
    print(f'+ Monthly repayment: {to_repay_monthly:,.2f}')
    print(f'+ Total interest paid: {interest_paid:,.2f}')
    print('+-----------------------------------------------------+')


def calculate_investment_interest(present_value: float = 0,
                                  interest_rate: float = 0,
                                  years_invested: int = 0,
                                  interest: str = 'simple') -> None:
    """
    Calculation of the interest from an investment.
    A = expected end balance at (t); P = amount invested [principal]; r = Interest Rate; t = time invested
    Simple interest method: A = P * (1 + r * t)
    Compound interest method: A = P * (1 + r) ^ t
    :param present_value: quantity invested (P)
    :param interest_rate: Interest Rate (r)
    :param years_invested: number of years that the investment will be held (t)
    :param interest: simple or compound (method)
    :return: None
    """
    # As "simple" method is set by default, the check is against compound
    if interest == 'compound':
        expected_final_amount = present_value * pow((1 + interest_rate), years_invested)
    else:
        expected_final_amount = present_value * (1 + interest_rate * years_invested)
    # Calculation of interest earned; nice to have
    total_interest_earned = expected_final_amount - present_value
    # Output presentation and display
    # Note ":," format introduces commas "," 1000 -> 1,000
    # Quantities rounded in format to 2 decimals ":.2f"
    print('\n\n+-----------------------------------------------------+')
    print('+---------- Investment calculation complete ----------+')
    print('+- Inputs: -+')
    print(f'+ Initial balance (invested)`: {present_value:,}')
    print(f'+ Interest Rate: {interest_rate * 100}%')
    print(f'+ Years holding the investment: {years_invested}')
    print(f'+- End result using {interest} method: -+')
    print(f'+ Expected end balance: {expected_final_amount:,.2f}')
    print(f'+ Interest earned: {total_interest_earned:,.2f}')
    print('+-----------------------------------------------------+')


if __name__ == '__main__':
    print('Choose either \'investment\' or \'loan\' from the menu below to proceed:\n')
    print('investment - to calculate the amount of interest you\'ll earn on your investment')
    print('loan - to calculate the amount you\'ll have to pay on a home loan')
    # Convert to lower to allow input like CAPITAL or capital
    selection = input('Please choose (loan/investment): ').lower()
    # Check that a proper answer is submitted.
    assert selection == 'loan' or selection == 'investment', 'Invalid selection, only select loan or investment.'
    print('Please fill in the following form:')
    if selection == 'loan':
        # try-except block to prevent wrong type inputs (words when integer/float is expected)
        try:
            value_of_house = float(input('Present value of the house: '))
            # assert included to prevent unrealistic data input
            assert value_of_house > 0, 'Please enter a value over 0.'
            annual_interest_rate = float(input('Annual Interest Rate: '))
            assert annual_interest_rate > 0, 'Please input an Interest Rate over 0.'
            # Changed from percentage to per unit (for calculations later on)
            annual_interest_rate = annual_interest_rate / 100
            months_to_repay_loan = int(input('Loan term (in months): '))
            assert months_to_repay_loan > 0, 'Please input a number of months over 0.'
        except ValueError:
            print('Wrong input detected; please follow the instructions.')
        else:
            # Function to calculate the interest of a loan and print the result
            calculate_loan_interest(value_of_house,
                                    annual_interest_rate,
                                    months_to_repay_loan)
    # elif not needed as correct input was already checked in the assert line
    else:
        # try-except block to prevent wrong type inputs (words when integer/float is expected)
        try:
            # assert included to prevent unrealistic data
            initial_amount = float(input('Amount invested: '))
            assert initial_amount > 0, 'Amount invested must be over 0.'
            interest_rate_percentage = float(input('Interest Rate: '))
            assert interest_rate_percentage > 0, 'Please enter a percentage over 0.'
            # Changed from percentage to per unit to comply with rate calculation (r)
            interest_rate_per_unit = interest_rate_percentage / 100
            years_to_invest = int(input('Years that the amount will be invested: '))
            assert years_to_invest > 0, 'Please only enter an amount of years over 0.'
            interest = input('Select method to use: \'simple\' or \'compound\': ').lower()
            assert interest == 'simple' or interest == 'compound', 'Please only select simple or compound.'
        except ValueError:
            print('Wrong input detected; please follow the instructions.')
        else:
            # Function to calculate the interest of an investment
            calculate_investment_interest(initial_amount,
                                          interest_rate_per_unit,
                                          years_to_invest,
                                          interest)
