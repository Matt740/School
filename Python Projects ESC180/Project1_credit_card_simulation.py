def initialize():
    '''Define all variables that need to be defined'''
    global last_update_day, last_update_month, cur_balance_owing_recent, cur_balance_owing_intst, num_purchases, disabled, last_country, last_country2
    last_update_day = -1
    last_update_month = -1
    cur_balance_owing_recent = 0
    cur_balance_owing_intst = 0
    num_purchases = 0
    disabled = False
    last_country = None
    last_country2 = None

def date_same_or_later(day1, month1, day2, month2):
    '''Return True if day1, month1 occurs after day2, month2, False if not'''
    if month1 > month2:
        return True
    elif month1 == month2:
        if day1 >= day2:
            return True
    return False

def all_three_different(c1,c2,c3):
    '''Return True if all c1, c2, and c3 are different strings, False if not'''
    if c1 != c3 and c1 != c2 and c2 != c3:
        return True
    return False

def purchase(amount, day, month, country):
    '''Test to see whether or not purchase should go through with date
    and fraud protection and then updating the account on interest and
    inputting the amount into cur_balance_owing_recent'''
    global last_update_day, last_update_month, cur_balance_owing_recent, num_purchases, disabled, last_country, last_country2, disabled
    if disabled:
        return "error"
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    if num_purchases > 1:
        if all_three_different(country,last_country, last_country2) == True:
            disabled = True
            return "error"
    last_country2 = last_country
    last_country = country
    num_purchases += 1
    amount_owed(day, month)
    cur_balance_owing_recent += amount


def amount_owed(day, month):
    '''Return amount of money owed on a certain date'''
    global last_update_day, last_update_month, cur_balance_owing_recent, cur_balance_owing_intst
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    if month > last_update_month:
        cur_balance_owing_intst = 1.05 ** (month - last_update_month) * cur_balance_owing_intst + 1.05 ** (month - last_update_month - 1) * cur_balance_owing_recent
        cur_balance_owing_recent = 0
    last_update_day = day
    last_update_month = month
    tot_amount_owed = cur_balance_owing_recent + cur_balance_owing_intst
    return tot_amount_owed

def pay_bill(amount, day, month):
    '''Test whether or not payment can go through with previous date and then
     updating account with interest, and then subtracting amount from cur_balance_owing_intst
    first, and then cur_balance_owing_recent'''
    global last_update_day, last_update_month, cur_balance_owing_recent, cur_balance_owing_intst
    if date_same_or_later(day, month, last_update_day, last_update_month) == False:
        return "error"
    amount_owed(day, month) # Call amount_owed to update cur_balance_owing_recent and cur_balance_owing_intst with proper interest to date before payment on said date is completed
    if amount > cur_balance_owing_intst:
        cur_balance_owing_recent -= (amount - cur_balance_owing_intst)
        cur_balance_owing_intst = 0

    else:
        cur_balance_owing_intst -= amount



if __name__ == "__main__":
    initialize()
    print(date_same_or_later(3,4,2,4))
    print(all_three_different("Uganda","Vatican City","Lithuania"))
    purchase(15, 1, 1, "Canada")
    print(amount_owed(1,1))
    purchase(15, 1, 1, "France")
    print(amount_owed(1,1))
    purchase(15, 1, 1, "Canada")
    print(amount_owed(1,1))
    purchase(15, 1, 1, "U.K.")
    print(amount_owed(1,1))
    print(amount_owed(3, 3))
    pay_bill(30, 3, 3)
    print(amount_owed(3,3))
    purchase(15, 4, 5, "Canada")
    purchase(15, 4, 5, "Canada")

