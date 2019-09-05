def euro_string(value):
    """
    Convert cents to string formatted euro
    """
    result = "€ {:.2f}".format(round(value / 100, 2))
    return result
