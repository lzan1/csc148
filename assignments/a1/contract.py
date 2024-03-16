"""
CSC148, Winter 2024
Assignment 1

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Bogdan Simion, Diane Horton, Jacqueline Smith
"""
import datetime
from math import ceil
from typing import Optional

from bill import Bill
from call import Call


# Constants for the month-to-month contract monthly fee and term deposit
MTM_MONTHLY_FEE = 50.00
TERM_MONTHLY_FEE = 20.00
TERM_DEPOSIT = 300.00

# Constants for the included minutes and SMSs in the term contracts (per month)
TERM_MINS = 100

# Cost per minute and per SMS in the month-to-month contract
MTM_MINS_COST = 0.05

# Cost per minute and per SMS in the term contract
TERM_MINS_COST = 0.1

# Cost per minute and per SMS in the prepaid contract
PREPAID_MINS_COST = 0.025


class Contract:
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        self.start = start
        self.bill = None

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>.
        This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        raise NotImplementedError

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.
        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        self.bill.add_billed_minutes(ceil(call.duration / 60.0))

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        self.start = None
        return self.bill.get_cost()


class TermContract(Contract):
    """
    Term deposit monthly fee
    TERM_MONTHLY_FEE = 20.00
    TERM_DEPOSIT = 300.00

    #Included free minutes and SMSs in the term contracts (monthly)
    TERM_MINS = 100
    # Cost per minute/SMS in the term contract
    TERM_MINS_COST = 0.1
    """
    start: datetime.date
    end: datetime.date
    bill: Optional[Bill]
    curr_date: datetime.date

    def __init__(self, start: datetime.date, end: datetime.date) -> None:
        """ Create a new Term Contract with the <start> date, starts as inactive
        """
        # End date is last day of month
        # Incoming calls are free
        super().__init__(start)
        self.curr_date = start
        self.end = end

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>.
        This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.
        """
        self.bill = bill
        # Check if first time initializing
        if month == self.curr_date.month and year == self.curr_date.year:
            bill.add_fixed_cost(TERM_DEPOSIT)
        # Every-month occurance
        bill.add_fixed_cost(TERM_MONTHLY_FEE)
        bill.set_rates('TERM', TERM_MINS_COST)
        # For billing purposes, set day to 1
        self.curr_date = datetime.date(year, month, 1)

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.

        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        # Add everything at first
        self.bill.add_free_minutes(ceil(call.duration / 60.0))
        # Then subtract as needed
        if self.bill.free_min > TERM_MINS:
            self.bill.add_billed_minutes(self.bill.free_min - TERM_MINS)
            self.bill.free_min = TERM_MINS

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        # If canceled after end date, refund deposit
        if self.curr_date > self.end:
            return TERM_DEPOSIT - self.bill.get_cost()
        else:
            # Take the deposit if canceled before end date
            return self.bill.get_cost()


class MTMContract(Contract):
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]

    """
    # Constants for the month-to-month contract monthly fee and term deposit
    MTM_MONTHLY_FEE = 50.00
    
    # Cost per minute and per SMS in the month-to-month contract
    MTM_MINS_COST = 0.05
    """
    def __init__(self, start: datetime.date) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        super().__init__(start)

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>.
        This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        self.bill = bill
        bill.set_rates('MTM', MTM_MINS_COST)
        bill.add_fixed_cost(MTM_MONTHLY_FEE)

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.
        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        super().bill_call(call)

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        return super().cancel_contract()


class PrepaidContract(Contract):
    """ A contract for a phone line

    This class is not to be changed or instantiated. It is an Abstract Class.

    === Public Attributes ===
    start:
         starting date for the contract
    bill:
         bill for this contract for the last month of call records loaded from
         the input dataset
    """
    start: datetime.date
    bill: Optional[Bill]
    balance: float
    """
    # Cost per minute and per SMS in the prepaid contract
    PREPAID_MINS_COST = 0.025
    """
    def __init__(self, start: datetime.date, balance: float) -> None:
        """ Create a new Contract with the <start> date, starts as inactive
        """
        super().__init__(start)
        self.balance = balance

    def new_month(self, month: int, year: int, bill: Bill) -> None:
        """ A new month has begun corresponding to <month> and <year>.
        This may be the first month of the contract.
        Store the <bill> argument in this contract and set the appropriate rate
        per minute and fixed cost.

        DO NOT CHANGE THIS METHOD
        """
        # Check if this is first time initializing
        if self.bill is None:
            self.bill = bill
            bill.add_fixed_cost(-self.balance)
        bill.set_rates('PREPAID', PREPAID_MINS_COST)
        if self.bill:  # Carry over bill from last month
            self.balance += bill.fixed_cost
        if self.balance < -10:
            # Automatic top-up
            self.balance -= 25

    def bill_call(self, call: Call) -> None:
        """ Add the <call> to the bill.
        Precondition:
        - a bill has already been created for the month+year when the <call>
        was made. In other words, you can safely assume that self.bill has been
        already advanced to the right month+year.
        """
        super().bill_call(call)

    def cancel_contract(self) -> float:
        """ Return the amount owed in order to close the phone line associated
        with this contract.

        Precondition:
        - a bill has already been created for the month+year when this contract
        is being cancelled. In other words, you can safely assume that self.bill
        exists for the right month+year when the cancelation is requested.
        """
        # Take credit amount out of total bill
        if self.balance < 0:
            self.bill.add_fixed_cost(self.balance)
        return self.bill.get_cost()


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'datetime', 'bill', 'call', 'math'
        ],
        'disable': ['R0902', 'R0913'],
        'generated-members': 'pygame.*'
    })
