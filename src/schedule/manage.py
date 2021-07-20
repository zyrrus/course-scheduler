import json

from schedule.tree import Course, Possibilitree


class Manager:
    def __init__(self, course_json):
        self.course_dict = Manager.__courses_from_json(course_json)
        self.course_list = Manager.__list_from_json(course_json)
        
        p = Possibilitree(self.course_list)
        self.schedules = p.gen_paths(filtered=True)

    # Remove later
    def print_courses(self):
        print(self.course_dict)


    # Converts list of CNodes to list of course names
    def get_schedules(self):
        named_schedules = []
        for schedule in self.schedules:
            named_schedules.append([node.course.name for node in schedule])

        return named_schedules


    # JSON str to dict of course info
    @staticmethod
    def __courses_from_json(course_json):
        json_list = json.loads(course_json)
        course_dict = {}

        for course in json_list:
            course_dict[course['name']] = {
                "name": course['name'],
                "start": course['start'],
                "end": course['end'],
                "days": course['days']
            }

        return course_dict


    # List of course objects
    @staticmethod
    def __list_from_json(course_json):
        json_list = json.loads(course_json)
        course_list = []

        for course in json_list:
            course_list.append(Manager.__course_from_dict(course))

        return course_list


    # Dict of course objects
    @staticmethod
    def course_dict_from_dict(courses_dict):
        obj_dict = {}

        for k, v in courses_dict.items():
            obj_dict[k] = Manager.__course_from_dict(v)

        return obj_dict


    # Course dict to Course obj
    @staticmethod
    def __course_from_dict(course_dict):
        return Course(
            course_dict['name'],
            course_dict['start'],
            course_dict['end'],
            course_dict['days']
        )


class Week:
    def __init__(self, schedule):
        self.weekdays = {
            'M': [],
            'T': [],
            'W': [],
            'Th': [],
            'F': []
        }
        self.__fill_week(schedule)

    def __fill_week(self, schedule):
        for course in schedule:
            # Build a course box
            coursebox = _CourseBox(course)

            # Then place it in the appropriate weekday lists
            for day in course.days:
                self.weekdays[day].append(coursebox)


class _CourseBox:
    def __init__(self, course): 
        self.course = course.name

        # Start at 7:00am
        start_time = self.get_total_minutes(course.start)  - (7 * 60)
        end_time = self.get_total_minutes(course.end) - (7 * 60)

        self.top = self.calc_start(start_time)
        self.length = self.calc_height(end_time - start_time)

    def calc_start(self, minutes):
        # Start at 2.5 rem and each space is 1.2 rem
        return 2.5 + (1.2 * (minutes / 30))

    def calc_height(self, minutes):
        # Each space is 1.2 rem
        return 1.2 * (minutes / 30)
    
    def get_total_minutes(self, time):
        h, m = time.split(':')
        total = int(h) * 60 + int(m)
        return total


def main():
    details1 = {
        "names": [
            "CSC 2362", "CSC 3200", "CSC 3380", 
            "CSC 4330", "CSC 3501", "CSC 3730", 
            "CSC 4101", "CSC 4103", "CSC 4444", 
            "MATH 2060", "MATH 4020", "MATH 4031", 
            "MATH 4065", "MATH 4153", "MATH 4200"
        ],
        "starts": [
            time(15, 0),  time(10, 30), time(16, 30), 
            time(15, 0),  time(13, 30), time(9, 0), 
            time(12, 0),  time(13, 30), time(15, 30), 
            time(12, 30), time(13, 30), time(9, 30), 
            time(10, 30), time(15, 0),  time(8, 30)
        ],
        "ends": [
            time(16, 20), time(11, 20), time(17, 50), 
            time(16, 20), time(14, 50), time(10, 20), 
            time(13, 20), time(14, 50), time(16, 50), 
            time(13, 20), time(14, 50), time(10, 20), 
            time(11, 50), time(16, 20), time(9, 20)
        ], 
        "days": [
            ['M', 'W'],  ['W'],       ['T', 'Th'], 
            ['T', 'Th'], ['T', 'Th'], ['T', 'Th'], 
            ['M', 'W'],  ['M', 'W'],  ['M', 'W'], 
            ['T', 'Th'], ['T', 'Th'], ['M', 'W', 'F'], 
            ['T', 'Th'], ['T', 'Th'], ['M', 'W', 'F']
        ]
    }

    details2 = {
        "names": [x for x in "ABCDE"],
        "starts": [time(10, 0),  time(16, 0), time(11, 0), time(17, 0),  time(13, 0)],
        "ends": [time(12, 0),  time(18, 0), time(14, 0), time(19, 0),  time(15, 0)],
        "days": [['M', 'W', 'T']]*5
    }
    '''
    10 11 12 13 14 15 16 17 18 19
    10 -a-12          16 -b-18
    11  -c-  14       17 -d-19
            13 -e-15
    '''
    
    details = details1

    ls_courses = []
    for i in range(len(details["names"])):
        ls_courses.append(Course(details["names"][i], details["starts"][i], details["ends"][i], details["days"][i]))

    
    for c in ls_courses:
        print(c)

if __name__ == '__main__':
    main()