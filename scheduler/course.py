import copy 

class Course:
    """ Stores all relevant information about a course

    Attributes
    ----------
    name : str
        the name of the course
    credit_hours : int
        the number of credit hourse for the course
    time : TimeRange
        the time period of the course
    days : (str, ...)
        the days when the course is scheduled
            - recommended values: ('M', 'T', 'W', 'Th', 'F')

    Methods
    -------
    __repr__() : str
        Courses are represented by their name alone
    get_info() : str
        Returns detailed course info as a formatted string 
    """

    def __init__(self, name, credit_hours, time, days):
        self.name = name
        self.hours = credit_hours
        self.time = time
        self.days = days

    def __repr__(self): 
        # Simplified representation
        return self.name 
        

    def get_info(self):
        # Detailed representation
        week = ''.join(self.days)
        return f"{self.name}: {self.hours}h {self.time} {week}"


class ScheduleBuilder:
    """ Traverses a tree of courses to find all schedules 
    around a given number of credit hours

    Class Attributes
    ----------
    LIMIT_HOURS : int (constant)
        The target amount of course hours 
    Cur_Hours : int
        The current schedule's number of course hours
    Good_Schedules : [[Course, ...], ...]
        A list of schedules(lists of courses) around the set hour limit
    Cur_Schedules : [[Course, ...], ...]
        The current, work-in-progress schedule

    Instance Attributes
    ----------
    course : Course
        The value of the node in the tree
    children : [ScheduleBuilder, ...]
        The children of a node are sub-trees 

    Methods
    -------
    add_children([Courses, ...]: children) : None
        Builds the tree of courses
    dfs() : None
        Traverses the course tree recursively to find all possible schedules. 
        Adds any currently valid schedules to Good_Schedules
    get_schedules() : None
        Prints all valid schedules that meet the target time
    """
    
    LIMIT_HOURS = 0
    Cur_Hours = 0
    Good_Schedules = []
    Cur_Schedule = []
  
    def __init__(self, course):
        self.course = course
        self.children = []

    def add_children(self, children):
        for i, child in enumerate(children):
            tree = ScheduleBuilder(child)
            self.children.append(tree)
            tree.add_children(children[(i+1):])

    def dfs(self):
        # Check for scheduling conflicts
        overlap = False
        for course in ScheduleBuilder.Cur_Schedule:
            if set(self.course.days).intersection(set(course.days)):
                if (self.course.name != course.name) and self.course.time.overlaps(course.time):
                    overlap = True
                    break
        
        # If there are no conflicts, check if the current schedule's
        # hours is lower than the limit
        if not overlap:
            if ScheduleBuilder.Cur_Hours < ScheduleBuilder.LIMIT_HOURS:
                ScheduleBuilder.Cur_Hours += self.course.hours

                ScheduleBuilder.Cur_Schedule.append(self.course)

                # Add current schedule to list of good schedules 
                # if it's within a couple hours from the limit
                if ScheduleBuilder.Cur_Hours >= ScheduleBuilder.LIMIT_HOURS - 2:
                    ScheduleBuilder.Good_Schedules.append(copy.deepcopy(ScheduleBuilder.Cur_Schedule))

                # Recursively depth first search for next courses
                for child in self.children:
                    child.dfs()

                # Remove hours and current course
                ScheduleBuilder.Cur_Hours -= self.course.hours
                if ScheduleBuilder.Cur_Schedule:
                    ScheduleBuilder.Cur_Schedule.pop()

    def get_schedules(self):
        for schedule in ScheduleBuilder.Good_Schedules:
            print(schedule)


