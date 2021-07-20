from datetime import time


# Holds course info
class Course:
    def __init__(self, name, start, end, days):
        self.name = name
        self.start = start
        self.end = end
        self.days = days
    
    # def __repr__(self):
    #     return f'{{"name":"{self.name}","start":"{self.start.strftime("%H:%M")}","end":"{self.end.strftime("%H:%M")}","days":{self.days}}},'


# Acts as a node for the graph, but it contains a course 
class CNode:
    def __init__(self, course):
        self.course = course
        self.children = []
        self.invalids = set()
        self.visited = False

    def __repr__(self):
        return self.course.name


# Performs the graph search to find all schedules
class Possibilitree:
    def __init__(self, course_list):
        self.nodes = [CNode(course) for course in course_list]

        # Create all edges between nodes
        for i, node in enumerate(self.nodes):
            self.set_children(node, self.nodes[i+1:])

        self.__remove_overlaps(self.nodes[0])
        

    def set_children(self, node, children):
        for child in children:
            node.children.append(child)


    def __remove_overlaps(self, node):
        marked_edges = []
        for child in node.children:
            self.__remove_overlaps(child)
            if self.__courses_intersect(node, child):
                marked_edges.append(child)

        for child in marked_edges:
            node.children.remove(child)
            node.invalids.add(child)


    def __courses_intersect(self, node1, node2):
        if self.__days_intersect(node1.course.days, node2.course.days):
            # Sort nodes by start time
            first = node1
            last = node2
            if node1.course.start > node2.course.start:
                first = node2
                last = node1

            # Check for overlapping times
            return not first.course.end < last.course.start
        # Courses share no days
        return False


    def __days_intersect(self, days1, days2):
        set1 = set(days1)
        set2 = set(days2)

        return set1 & set2

    
    def gen_paths(self, filtered=False):
        schedules = []
        for node in self.nodes:
            all_invalids = node.invalids
            stack = [node]
            schedule = []

            # DFS
            while stack:
                cur_node = stack.pop(0)
                all_invalids = all_invalids.union(cur_node.invalids)

                for child in cur_node.children:
                    if child not in all_invalids and child not in stack:
                        stack.append(child)
                
                # Changing list during iteration - Bad!
                for n in stack:
                    if n in all_invalids:
                        stack.remove(n)
                                
                schedule.append(cur_node)
                schedules.append(schedule[:])

        if filtered:
            # Removes all lists that are subsets of other lists
            l = schedules
            l2 = [m for i, m in enumerate(l) if not any(set(m).issubset(set(n)) for n in (l[:i] + l[i+1:]))]
            schedules = l2
                
        return schedules


    def print_nodes(self):
        for node in self.nodes:
            print(node.course.name, "->", [child.course.name for child in node.children])


    def print_invalids(self):
        for node in self.nodes:
            print(node.course.name, "->", [child.course.name for child in node.invalids])


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

    p = Possibilitree(ls_courses)

    for c in ls_courses:
        print(c)
    

if __name__ == '__main__':
    main()
    