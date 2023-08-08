class PercentageConverter:
    """
    # Usage
    converter = PercentageConverter()
    integer = 0
    percentage = converter.int_to_pct(integer)
    print(f"{integer} is {percentage}%")

    percentage = 100
    integer = converter.pct_to_int(percentage)
    print(f"{percentage}% is {integer}")
    
    # output
    0 is 100%
    100% is 0
    """
    def int_to_pct(self, integer):
        return round(100 - (integer * 100) / 99)

    def pct_to_int(self, percentage):
        return round(99 - (percentage * 99) / 100)



