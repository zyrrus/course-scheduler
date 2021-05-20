class Time:
    """ Converts a time string 'HH:MM _M' into an object representation of time

    Attributes
    ----------
    hour12 : int
        Hour in 12-hour time
    hour24 : int
        Hour in 24-hour time
    minute : int
        Minutes
    total : int
        Time converted to minutes

    Methods
    -------
    to_total_minutes() : None
        Calculates total time in minutes
    __repr__() : str
        Representation of time in the form 'HH:MM'
    """

    def __init__(self, time_str): 
        # Formatted as 'HH:MM PM'
        self.hour12 = int(time_str[:2])
        self.hour24 = self.hour12 + 12 if time_str[6] == 'P' and self.hour12 != 12 else self.hour12

        self.minute = int(time_str[3:5])
    
        self.total = self.minute
        self.to_total_minutes()

    def to_total_minutes(self):
        self.total += self.hour24 * 60

    def __repr__(self):
        return f"{self.hour12:02}{self.minute:02}"


class TimeRange:
    """ Represents a time interval with a start Time and end Time

    Attributes
    ----------
    start : Time
        Beginning of the time interval
    end : Time
        End of the time interval
    interval : Tuple(int, int)
        Tuple of the start and end times, each in total minutes

    Methods
    -------
    overlaps() : Bool
        Returns True if two time intervals overlap
    __repr__ : str
        Representation of the time interval as 'HH:MM-HH:MM'
    """

    def __init__(self, start, end):
        self.start = Time(start)
        self.end = Time(end)
        
        self.interval = (self.start.total, self.end.total)

    def overlaps(self, other):
        # Sort times
        if self.interval[0] < other.interval[0]:
            first = self.interval
            last = other.interval
        else:
            first = other.interval
            last = self.interval

        # Check overlap
        # Overlap types
        # ----[---]----{--}---- No Overlap
        # ----[---{----]--}----
        # ----[---{----}--]----
        if first[1] < last[0]:
            return False

        return True

    def __repr__(self):
        return f"{self.start}-{self.end}"
