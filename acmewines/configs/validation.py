"""
    acmewines.configs.validation
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This is the configuration for order validation
"""

# Valid U.S. state/area abbreviations for order
states = [AL, AK, AZ, AR, CA, CO, CT, DE, DC, FL, GA, HI,
    ID, IL, IN, IA, KS, KY, LA, ME, MD, MA, MI, MN, MS, MO,
    MT, NE, NV, NH, NJ, NM, NY, NC, ND, OH, OK, OR, PA, RI,
    SC, SD, TN, TX, UT, VT, VA, WA, WV, WI, WY, AS, GU, MP,
    PR, VI, FM, MH, PW]

# The States that we don't ship wines to
states_not_allowed = [NJ, CT, PA, MA, IL, ID, OR]

# Valid zipcode pattern in regular expression 
zipcode_pattern = '^\d{5}([\-]\d{4})?$'

# The maximum value of the zipcode's digit sum
zipcode_max_digit_sum = 20

# Valid date format for the orderer's birthday
birthday_format = '%b %d, %Y'

# The minimum age of the orderer
min_age = 21
