class AdultPerInfantsOnLapError(Exception):
    """
    Raised when the number of adults is less than the number of infants on lap
    """
    pass


class NoFlightsFoundError(Exception):
    """
    Raised when no flights are found
    """
    pass