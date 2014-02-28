from slurp_data import *

courses = CsvData('all_courses.csv')
courses = courses.groupby('Term')['S2']
schedules = CsvData('schedules.csv')
schedules = schedules.groupby('Term')['S2']
grouped =schedules.groupby('Student > Name')

def get_yog (student):
    yog = None
    if preference_data['2014'].find('Full',student).rows:
        yog = 2014
    elif preference_data['2015'].find('Full',student).rows:
        yog = 2015                
    elif preference_data['2016'].find('Full',student).rows:
        yog = 2016               
    elif preference_data['2017'].find('Full',student).rows:
        yog = 2017
    return yog

def get_paired_courses ():
    courses_by_root = {}
    for c in courses:
        title = c.Course
        if '-' in title:
            root = title.split('-')[0]
            if courses_by_root.has_key(root):
                courses_by_root[root].append(c)
            else:
                courses_by_root[root] = [c]
    return courses_by_root

def get_roster (course):
    if type(course) not in types.StringTypes:
        course = course.Course
    return schedules.find('Course',course)

if True:
    for student in grouped.keys():
        # Sections 1-4 are first semester
        for section in ['Math 110-001','Math 110-002','Math 110-003','Math 110-004']:
            if section in [r.Course for r in grouped[student]]:
                found_second_semester = False
                for section in ['Math 110-005','Math 110-006','Math 110-007','Math 110-008']:
                    if section in [r.Course for r in grouped[student]]:
                        found_second_semester = True
                if not found_second_semester:
                    print "DIDN'T FIND SECOND SEMESTER MATH FOR ",student

    
    courses_by_dept = courses.groupby('Department')
    eng = courses_by_dept['English']
    sp = courses_by_dept['World Language']
    eng_req = CsvData('english_req.csv')
    need_req = filter(lambda r: not r.RequirementMet and r.Grade in ['10','12'], eng_req.rows)

    preference_data = {
        '2014':CsvData('2014_selections.csv'),
        '2015':CsvData('2015_selections.csv'),
        '2016':CsvData('2016_selections.csv'),
        '2017':CsvData('2017_selections.csv'),
        }
    preference_data['all'] = Data(preference_data['2014'].rows + preference_data['2015'].rows + preference_data['2016'].rows + preference_data['2017'].rows)
    ENG_1 = 'My first choice preference for English classes is:'
    ENG_2 = 'My second choice preference for English classes is:'
    ENG_3 = 'My third choice preference for English classes is:'
    SP_1 =  'My first choice preference for Spanish classes is:'
    SP_2 =  'My second choice preference for Spanish classes is:'
    SP_3 =  'My third choice preference for Spanish classes is:'
    

if True:
    all_paired = get_paired_courses()
    outta_wack={}
    for course,sections in all_paired.items():
        if numpy.std([int(c.Total) for c in sections]) > 4:
            outta_wack[course] = sections
    for course in ['Spanish 261','Spanish 262']:
        overloaded_a_block = outta_wack[course][0]
        for s in get_roster(overloaded_a_block):
            print 'Looking for options for ',s['Student > Name'],'in overloaded course',course
            pd = preference_data['all'].find('Full',s['Student > Name'])
            if pd:
                pd = pd[0]
                if 'Plays' in pd[ENG_1] or 'Plays' in pd[ENG_2] or 'Plays' in pd[ENG_3]:
                    print 'We could move ',s,'to Power Plays'

def print_roster (course):
    for s in get_roster(course):
        print s['Student > Name'],get_yog(s['Student > Name'])
            
if False:    
    spanish_data = CsvData('spanish_stats.csv')

    courses_by_student = schedules.groupby('Student > Name')
    for student in courses_by_student.keys():
        yog = get_yog(student)
        # Look up data on student:
        sdata = spanish_data.find('Student Name',student)
        their_courses = courses_by_student[student]
        # Find Spanish class
        spanish = None
        for c in their_courses:
            if 'Spanish' in c.Course:
                spanish = c
        level = None
        if spanish:
            #Check if it's the right level
            if ' 1' in spanish.Course:
                level = 1
            if ' 2' in spanish.Course:
                level = 2
            if ' 3' in spanish.Course:
                level = 3
        if sdata.rows:
            if spanish:
                sheet_level = sdata.rows[0].Level                
                if '%s'%level not in sheet_level:
                    print '!',yog,student,'Student is in ',spanish.Course,'but was recommended for level',sheet_level
                #else:
                #    print 'Student',student,yog,'is in ',spanish.Course,'which is good -- they should be at level ',sheet_level
            else:
                if level:
                    print '!',yog,student,'Student is not in Spanish but recommended for level',level
                else:
                    print yog,student,'Student is not in Spanish and listed as ',level

if False:
    for course in eng:
        course_size =  len(filter(lambda x: x['Course']==course.Course,schedules.rows))
        print '-'*60
        print 'ANALYZING POSSIBLE MOVES FOR: ', course.Course, course.Description,course_size
        print '-'*60
        for keyword in ['Journalism','Creative','Memoir','Writing']:
            if keyword in course.Description:
                if course_size < 15: continue
                options = []
                courses_in_block = filter(lambda x: x.Schedule==course.Schedule, eng)
                for option in courses_in_block:
                    if ((' 2' in course.Course and ' 2' in option.Course)
                        or
                        (' 3' in course.Course and ' 3' in option.Course)
                        or (not ' 3' in course.Course and not ' 2' in course.Course)
                        ):
                        if course.Course != option.Course:
                            print option.Course,option.Description,option.Schedule
                            option.size = len(filter(lambda x: x['Course']==option.Course,schedules.rows))
                            print '@',option.size
                            options.append(option)
                for sched_row in filter(lambda x: x['Course']==course.Course,schedules.rows):
                    name = sched_row['Student > Name']
                    if not filter(lambda r: r.Name==name, need_req):
                        #print name,'does not need ',course.Course,course.Description,course.Schedule,course_size
                        if len(preference_data['all'].find('Full',name)):
                            row = preference_data['all'].find('Full',name)[0]
                            #print 'his/her top English choices are: ',row[ENG_1],row[ENG_2],row[ENG_3]
                            for o in options:
                                if row[ENG_1].strip() in o.Description:
                                    print 'We could move ',name,get_yog(name),'from',course.Course,'(%s)'%course_size,'to their FIRST CHOICE',o.Course,o.Description,'(%s)'%o.size
                                if row[ENG_2].strip() in o.Description:
                                    print 'We could move ',name,get_yog(name),'from',course.Course,'(%s)'%course_size,'to their SECOND CHOICE',o.Course,o.Description,'(%s)'%o.size
                                if row[ENG_3].strip() in o.Description:
                                    print 'We could move ',name,get_yog(name),'from',course.Course,'(%s)'%course_size,'to their THIRD CHOICE',o.Course,o.Description,'(%s)'%o.size
                print 'Could switch to:'
                
                print
                print
        print '-'*60
        
    for course in sp:
        print course.Course, len(filter(lambda x: x['Course']==course.Course,schedules.rows))

    coursesched = courses.groupby('Schedule')
    print;print;print
    for block in coursesched.keys():
        print
        if 'Per 1(Mon' in block: print 'A BLOCK'
        if 'Per 2(Mon' in block: print 'B BLOCK'
        if 'Per 3(Mon' in block: print 'C BLOCK'
        if 'Per 6(Mon' in block: print 'D BLOCK'
        if 'Per 1(Tue' in block: print 'E BLOCK'
        if 'Per 2(Tue' in block: print 'F BLOCK'                                                                            
        print block
        print '-'*len(block)
        block_courses = coursesched[block]
        block_courses.rows.sort(key=lambda c: c.Course.split()[-1])
        for course in coursesched[block].rows:
            print course.Course, course.Description,course.Teacher,len(filter(lambda x: x['Course']==course.Course,schedules.rows))
        
    
