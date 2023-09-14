class SchoolClass:
    def __init__(self, subject:str, course:str, name:str, grade:str, credits:int):
        self.subject=subject
        self.course=course
        self.subject_course = f"{self.subject} {self.course}"
        self.name=name
        self.grade=grade
        self.credits=credits
        self.was_dropped = (self.grade == "WC")
        self.points = self.get_number_grade() * self.credits # if negative, class was dropped, can be ignored
        

    def get_number_grade(self):
        if self.was_dropped:
            return -1
        gpa_grades = {"A":4.0,"A-":3.7,"B+":3.3,"B":3.0,"B-":2.7,"C+":2.3,"C":2.0,"C-":1.7,"D+":1.3,"D":1.0,"D-":0.7,"F":0}
        return gpa_grades[self.grade]
    

    def __str__(self):
        return f"{self.subject} {self.course} {self.name} [{self.credits}]: {self.grade}"
    

    def is_major(self):
        return self.subject in ("MAT", "CS", "STT")
    


class Semester:
    def __init__(self,name:str, classes_list:list[SchoolClass]):
        self.name=name
        self.classes=[]
        for school_class in classes_list:
            if type(school_class) == SchoolClass:
                self.classes.append(school_class)
            else:
                raise Exception("Cannot add non-SchoolClass objects to a Semester")
        self.classes_points_dict = {}
        self.classes_credits_dict = {}
        for school_class in self.classes:
            if not school_class.was_dropped:
                self.classes_points_dict[school_class.subject_course] = school_class.points
                self.classes_credits_dict[school_class.subject_course] = school_class.credits  
        
    
    def __str__(self):
        string=self.name
        for school_class in self.classes:
            string += "\n"
            string += str(school_class)
        return string 
    

    def credits_attempted(self):
        attempted_credits = 0
        for school_class in self.classes:
            attempted_credits += school_class.get_credits()
        return attempted_credits
    

    def semester_gpa(self):
        sem_gpa = 0
        for school_class in self.classes:
            sem_gpa += school_class.get_number_grade() * school_class.get_credits()
        sem_gpa /= self.credits_attempted()
        return sem_gpa
    

    def major_credits_attempted(self):
        major_attempted_credits = 0
        for school_class in self.classes:
            if school_class.is_major():
                major_attempted_credits += school_class.get_credits()
        return major_attempted_credits
    

    def major_semester_gpa(self):
        major_sem_gpa = 0
        for school_class in self.classes:
            if school_class.is_major():
                major_sem_gpa += school_class.get_number_grade() * school_class.get_credits()
        major_sem_gpa /= self.major_credits_attempted()
        return major_sem_gpa



class DegreeProgram:

    def __init__(self, semesters_list: list[Semester]):
        self.semesters = []
        for semester in semesters_list:
            if type(semester) == Semester:
                self.semesters.append(semester)
            else:
                raise Exception("Cannot add non-Semester objects to a DegreeProgram.")
            
        self.classes_points_dict = {} # each class + points gained for it,
        self.total_credits_attempted = 0

        self.major_classes_points_dict = {}
        self.major_credits_attempted = 0

        for semester in self.semesters:
            for name,points in semester.classes_points_dict.items():
                if name not in self.classes_points_dict:
                    self.classes_points_dict[name] = points
                    self.total_credits_attempted += semester.classes_credits_dict[name]

                    if name.split()[0] in ("MAT", "CS", "STT"):
                        self.major_classes_points_dict[name] = points
                        self.major_credits_attempted += semester.classes_credits_dict[name]
                else:
                    if self.classes_points_dict[name] < points:
                        self.classes_points_dict[name] = points

                        if name.split()[0] in ("MAT", "CS", "STT"):
                            self.major_classes_points_dict[name] = points
        
        self.total_points = sum(self.classes_points_dict.values())
        self.major_points = sum(self.major_classes_points_dict.values())
        self.total_gpa = self.total_points / self.total_credits_attempted
        self.major_gpa = self.major_points / self.major_credits_attempted

    
def read_semester_classes(filename):
    classes = []
    with open(filename) as f:
        for line in f:
            parts = line.split(",")
            classes.append(SchoolClass(parts[0],parts[1],parts[2],parts[3],int(parts[4])))
    return classes


def create_semester(name, filename):
    classes = read_semester_classes(filename)
    return Semester(name, classes)


def main():   
    semester1 = create_semester("Fall 2022", "semester1.txt")
    semester2 = create_semester("Spring 2023", "semester2.txt")
    semester3 = create_semester("Fall 2023", "semester3.txt")
    semester4 = create_semester("Spring 2024", "semester4.txt")
    yearone = [semester1, semester2]
    yeartwo = [semester3, semester4]

    degreeprogram = DegreeProgram(yearone+yeartwo)
    MAJOR_GPA = degreeprogram.major_gpa
    print(f"MAJOR GPA: {str(MAJOR_GPA)[:4]}")

    TOTAL_GPA = degreeprogram.total_gpa
    print(f"TOTAL GPA: {str(TOTAL_GPA)[:4]}")


def testing():
    class1 = SchoolClass("CS", "2435", "INTRO TO SCIENTIFIC PROGRAM", "A", 4)
    class2 = SchoolClass("ART", "1001", "FOUNDATIONS I", "WC", 0)
    class3 = SchoolClass("SD","2400","PRINC SUSTAINABLE DEVELOPMNT","A",3)
    fake_semester = Semester("Fake",[class3])
    semester1 = create_semester("Fall 2022", "semester1.txt")
    semester2 = create_semester("Spring 2023", "semester2.txt")
    semester3 = create_semester("Fall 2023", "semester3.txt")
    semester4 = create_semester("Spring 2024", "semester4.txt")
    degreeprogramyr1 = DegreeProgram([semester1,semester2])
    fake_degreeprogram = DegreeProgram([semester1,semester2,fake_semester])
    print(degreeprogramyr1.total_gpa)
    print(fake_degreeprogram.total_gpa)
    
    

if __name__ == "__main__":
    main()
    #testing()

