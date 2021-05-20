from src.scheduler.course import Course
from src.scheduler.course import ScheduleBuilder
from src.scheduler.time import TimeRange

# TODO: Clean up main
# TODO: Repeat the whole process with each course as the root node and remove duplicate schedules
# TODO: Add visual representation for a schedule
# END-GOAL: Flask web app 

def build_courses(names, hours, times, days):
    return list(map(lambda info: Course(info[0], info[1], info[2], info[3]), list(zip(names, hours, times, days))))

def run(courses, max_hours):
    tree = ScheduleBuilder(courses[0])
    tree.add_children(courses[1:])
    ScheduleBuilder.LIMIT_HOURS = max_hours

    tree.dfs()
    tree.get_schedules()
    
def main():
    # 15 Possible Courses
    names = [
        "CSC 2362", "CSC 3200", "CSC 3380", 
        "CSC 4330", "CSC 3501", "CSC 3730", 
        "CSC 4101", "CSC 4103", "CSC 4444", 
        "MATH 2060", "MATH 4020", "MATH 4031", 
        "MATH 4065", "MATH 4153", "MATH 4200"
    ]
    hours = [3, 1, 3, 3, 3, 3, 3, 3, 3, 1, 3, 3, 3, 3, 3] 
    times = [
        TimeRange('05:00 PM', '06:20 PM'), 
        TimeRange('10:30 AM', '11:20 AM'), 
        TimeRange('04:30 PM', '05:50 PM'),
        TimeRange('03:00 PM', '04:20 PM'), 
        TimeRange('01:30 PM', '02:50 PM'), 
        TimeRange('09:00 AM', '10:20 AM'),
        TimeRange('12:00 PM', '01:20 PM'), 
        TimeRange('01:30 PM', '02:50 PM'), 
        TimeRange('03:30 PM', '04:50 PM'),
        TimeRange('12:30 PM', '01:20 PM'), 
        TimeRange('01:30 PM', '02:50 PM'), 
        TimeRange('09:30 AM', '10:20 AM'),
        TimeRange('10:30 AM', '11:50 AM'), 
        TimeRange('03:00 PM', '04:20 PM'),
        TimeRange('08:30 AM', '09:20 AM'),
    ]
    days  = [
        ('M', 'W'), ('W'), ('T', 'Th'), 
        ('T', 'Th'), ('T', 'Th'), ('T', 'Th'), 
        ('M', 'W'), ('M', 'W'), ('M', 'W'), 
        ('T', 'Th'), ('T', 'Th'), ('M', 'W', 'F'), 
        ('T', 'Th'), ('T', 'Th'), ('M', 'W', 'F')
    ]

    run(build_courses(names, hours, times, days), 17)


if __name__ == '__main__':
    main()
