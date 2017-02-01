from BeautifulSoup import *
from urllib2 import *
from Tkinter import *
import optimization,re

Optimization_Dictionary = {1:"Hill Climbing",2:"Simulated Annealing",3:"Genetic Optimization",4:"Random Optimization"}
                                                                        #This dictionary is for determining the type of optimization
Days_of_Week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
                                                                        #This list is for printing days of week.
regular_expression_for_together_days = re.compile('^([A-Z].*)([A-Z].*)$',re.VERBOSE)
                                                                        #This re is for seperating the together days like TuesdayMonday,WednesdayFriday.
#This class is for creating object.Each course will be object created by this class.Each object will have 3 attributes;course code,course name and course time and day
class Course():
    def __init__(self,code=None,course_name=None,time_and_day = None):
        self.code = code                                                #This attribute is for course code,unicode
        self.course_name = course_name                                  #This is for course name,unicode
        self.time_and_day = time_and_day                                #This contains both times and days of course,list of tuples.(time,day)
        
#This class has three main classes;Interface,Command for fetching,Command for optimizing.Two supporter functions helps the command for optimization;Cost Function and
#Representation Function
class Course_Schedule_Advisor():
    def __init__(self):
        self.Interface()

    def Interface(self):
        #Main window part
        self.main_window = Tk()
        self.main_window.geometry("1000x700+100+-10")
        self.main_window.resizable(width=False,height=False)
    
        #Background part
        self.Main_Background = Label(bg="Light Blue")
        self.Main_Background.place(relx = 0.0,rely = 0.0,width = 1000,height = 1000)
    
        #Title of project part
        self.Main_Title = Label(text = 'Course Schedule Advisor',font = "Times 30 bold",bg = "light green")
        self.Main_Title.place(relx = 0.1,rely = 0.0,width = 800)

        #Title of Entry
        self.Url_offering_title = Label(text = "Provide Course Offerings URL:",font = "Times 12 bold",bg = "orange")
        self.Url_offering_title.place(relx = 0.1,rely = 0.1)

        #Entry of URL(Entry)
        self.Url_taker = Entry()
        self.Url_taker.place(relx = 0.1,rely = 0.15,width = 500,height = 25)

        #Button of Fetching(Button)
        self.Fetching_url = Button(text = """Fetch Course\n Offerings""",font= "Times 12 bold",bg = "Orange",command = self.Command_of_fetching)
        self.Fetching_url.place(relx = 0.75,rely=0.1,width = 150,height = 65)

        #Title of Course Code Shower
        self.Course_code_shower_title = Label(text = """Select\nCourse\nCodes""",font = "Times 15 bold",bg = "light blue")
        self.Course_code_shower_title.place(relx = 0.1 ,rely=0.2,height = 75,width =80)

        #List of Course Codes(Listbox)
        self.Course_code_shower = Listbox(selectmode=EXTENDED)
        self.Course_code_shower.place(relx =0.2 ,rely = 0.2,width = 125,height = 150)

        #Scrollbar
        self.scroll = Scrollbar(self.Course_code_shower)
        self.scroll.pack(side=RIGHT,fill=Y)
        self.scroll.config(command = self.Course_code_shower.yview)

        #Title of Number of Courses
        self.Course_number_taker_title = Label(text = """Provide the\nNumber of\nCourses""",font = "Times 15 bold",bg = "light blue")
        self.Course_number_taker_title.place(relx = 0.38,rely=0.2,height = 75,width = 100)

        #Number of Courses(Entry)
        self.Course_number_taker = Entry(font = "Times 15 bold")
        self.Course_number_taker.place(relx = 0.5,rely = 0.21,height = 25,width =50)

        #Title of Optimization Method
        self.Optimization_methods_title = Label(text = """Choose the\nOptimization\nMethod""",font = "Times 15 bold",bg = "light blue")
        self.Optimization_methods_title.place(relx = 0.6,rely = 0.2,width = 125)

        #Optiomization Methods(Radio Buttons)
        self.Radio_Values = IntVar()
        self.Hill_Climbing_Button = Radiobutton(text = "Hill Climbing",variable = self.Radio_Values,value = 1,bg = "light blue",font = "Times 10 bold")
        self.Hill_Climbing_Button.place(relx = 0.75,rely = 0.21)
        self.Simulated_Annealing_Button = Radiobutton(text = "Simulated Annealing",variable = self.Radio_Values,value = 2,bg = "light blue",font = "Times 10 bold")
        self.Simulated_Annealing_Button.place(relx = 0.75,rely = 0.24)
        self.Genetic_Optimization_Button = Radiobutton(text = "Genetic Optimization",variable = self.Radio_Values,value = 3,bg = "light blue",font = "Times 10 bold")
        self.Genetic_Optimization_Button.place(relx = 0.75,rely = 0.27)
        self.Random_Optimization_Button = Radiobutton(text = "Random Optimization",variable = self.Radio_Values,value = 4,bg = "light blue",font = "Times 10 bold")
        self.Random_Optimization_Button.place(relx = 0.75,rely = 0.30)
        self.Radio_Values.set(1)
        
        #Button of Creating Course Schedule
        self.Create_course_scheudle = Button(text = "Create Course Schedule",font = "Times 15 bold",bg = "orange",command = self.Command_of_schedule_showing)
        self.Create_course_scheudle.place(relx = 0.1,rely =0.45)

        #Last Showing Part(Text)
        self.Last_Showing_Part = Text(font="Bold 12")
        self.Last_Showing_Part.place(relx =0.1,rely=0.52,width=800,height = 350)
        
        mainloop()
        
    def Command_of_fetching(self):
        url = self.Url_taker.get()                                      #Taking the url from entry for getting the informations.
        if len(url) < 10:                                               #If url is not proper for the fetching,program will show an error.
            self.Error_Message_Function("""Please give\na proper url for\nFetching""")
            return
        request = Request(url)
        response = urlopen(request)                                     
        html_version = response.read()      
        soup = BeautifulSoup(html_version)                              #Making soup the informations inside of the url.

        All_informations = [i.text  for i in soup.fetch('span') if (('style'  in dict(i.attrs) and i['style']) == ("font-size:8pt;font-family:helvetica, sans-serif"))]
                                                                        #This takes each information inside of each box like Course code,course name, ...
        List_of_all_courses = list()                                    #This will be list of object.Each course will be an object by Course class at above.                        
        self.Dictionary_of_course_codes = dict()                        #Keys of dictionary will be only first part of course code(unicode) like ARAB,MATH,PHYS and
                                                                        #values will be list of courses(objects) starting with key's code.
        number_of_course = len(All_informations)/6                      #Each course has 6 component;code,name,time,day,room,teacher so with dividing 6,course number
                                                                        #is determined.Actually the number of rows in websited is determined
        
        for i in range(1,number_of_course):                             #For loop starts from 1 because first row is useless because it only contains heady of columns     

            if  [pure_days for day in All_informations[6*i+2].split('\n') for pure_days in day.split('\r') if pure_days != '' ] == []:
                                                                        #Getting rid of the courses without any time and date.All_informations[6*i+2] symbolysis time.
                continue
            
            code = str(All_informations[6*i])                           #First element(All_informations[6*i]) of each 6 group elements is the code of course.str                    
            
            course_name = [pure_names for names in All_informations[6*i+1].split('\n') for pure_names in names.split('\r') if pure_names != '']
            course_name = ''.join(course_name)                          #Second element(All_informations[6*i+1]) of each 6 group elements is the name of course.str

                                                                        #Third element(All_informations[6*i+2]) of each 6 group elements is the days of course.
            if len(All_informations[6*i+2].split('\n')) == 1 and len(All_informations[6*i+2]) > 10:
                days = list()
                day1 = regular_expression_for_together_days.match(str(All_informations[6*i+2])).group(1)
                day2 = regular_expression_for_together_days.match(str(All_informations[6*i+2])).group(2)
                days.append(day1)
                days.append(day2)                                       #This if clause for getting the days writting together like TuesdayWednesday.list

            else:                                    
                days = [purest_days for day in All_informations[6*i+2].split('\n') for pure_days in day.split('\r') for purest_days in pure_days.split(' ')
                        if purest_days != '' ]                          #This else for getting the days in normal format.list
                days = ','.join(days)
                days = tuple(days.split(','))
                        
                                                                        #Fourth element(All_informations[6*i+3]) of each 6 group elements is the times of course.
            if len(All_informations[6*i+3].split('\n')) == 1 and len(All_informations[6*i+3]) > 11:
                time = list()                                           #This if clause for getting the times writting together like 12:00-14:0014:00-16:00.list
                time1,time2 = All_informations[6*i+3][0:11],All_informations[6*i+3][11:len(All_informations[6*i+3])]
                time.append(time1)
                time.append(time2)
                    
            else:
                time = [purest_times for times in All_informations[6*i+3].split('\n') for pure_time in times.split('\r') for purest_times in pure_time.split(' ')
                        if purest_times != '']                          #This else for getting the times in normal format.list
                time = ','.join(time)
                time = tuple(time.split(','))
            

            time_and_day = list()                                       #This will be list of tuple;(time,day).
            if len(days) == len(time):                                  #If each days has a time,making symetric tuples.
                for i in range(len(days)):
                    time_and_day.append((time[i].strip(' '),days[i].strip(' ')))

            else:                                                       #If all days have only one time,each tuple will have the same time.
                for i in range(len(days)):
                    time_and_day.append((str(time[0]).strip(' '),str(days[i]).strip(' ')))
            
            my_course = Course(code = code,course_name = course_name,time_and_day = time_and_day)
                                                                        #Creating an object with three attributes
            List_of_all_courses.append(my_course)                       #Adding each course(object) to the list.
        
        for i in List_of_all_courses:                   
            course_code = i.code.split(' ')[0]                          #Getting the uniqe codes of objects and values will be list of objects starting with this cod 
            self.Dictionary_of_course_codes.setdefault(course_code,list())
            self.Dictionary_of_course_codes[course_code].append(i)

        all_course_code = self.Dictionary_of_course_codes.keys()
        all_course_code.sort()
        for codes in all_course_code:                                   #Inserting the all uniqe codes to the listbox.
            self.Course_code_shower.insert(END,codes)

        

    def Command_of_schedule_showing(self):
        if len(self.Course_code_shower.get(0,END)) == 0:                #If there is no course code in listbox,program will show an error.
            self.Error_Message_Function("""Please First use the\nFetching Button""")
            return
        
        selections =  map(int,self.Course_code_shower.curselection())   #Returning the list of indexes selected in the listbox
        all_course_types = self.Course_code_shower.get(0,END)
        selected_course_types = [all_course_types[i] for i in selections ]

        if len(selected_course_types) == 0:                             #If demanded course codes is not selected,program will show an error.
            self.Error_Message_Function("""Please Select\nSome Course Code""")
            return
                                                                        #Returning the list of selected course codes.
        self.List_of_all_avaiable_courses = list()
        for course_types in selected_course_types:                      #Creating a list of courses from the course code dictionary with adding lists togetgher.
            self.List_of_all_avaiable_courses.extend(self.Dictionary_of_course_codes[course_types])

        if len(self.Course_number_taker.get()) == 0:                    #If demanded course number is not provided,program will show an error.
            self.Error_Message_Function("""Please give\nCourse number""")
            return

        try:
            number_of_courses = int(self.Course_number_taker.get())     #Getting the demanded number of course from entry
        except:                                                         #If it is not a number,program will comply.
            self.Error_Message_Function("""Please give\nCourse number\nproperlyas integer""")
            return

        if number_of_courses > len(self.List_of_all_avaiable_courses):  #If demeanded course number exceed avaiable course number,there will be an error.
            self.Error_Message_Function("""These course codes\nhave insufficient course""")
            return
        self.domain = [(0,len(self.List_of_all_avaiable_courses)- i-1 ) for i in range(number_of_courses)]
                                                                        #Domain
        type_of_optimization = Optimization_Dictionary[self.Radio_Values.get()]
                                                                        #Type of optimization come from the dictionary.
        if type_of_optimization == "Hill Climbing":
            solution = optimization.hillclimb(self.domain,self.My_Cost_Function)
            
        elif type_of_optimization == "Simulated Annealing":
            solution = optimization.annealingoptimize(self.domain,self.My_Cost_Function)

        elif type_of_optimization == "Genetic Optimization":
            if number_of_courses < 3:                                   #For genetic optimization,we need at least three course demand
                self.Error_Message_Function("""Genetic Optimization is\n valid for \nmore than  3 courses""")
                return
            solution = optimization.geneticoptimize(self.domain,self.My_Cost_Function)
            
        elif type_of_optimization == "Random Optimization":
            solution = optimization.randomoptimize(self.domain,self.My_Cost_Function)

        Last_Showing = self.My_Representation_function(solution)        #This returns a dictionary where keys are days and values will be list of tuple(time,course).       
        self.Last_Showing_Part.delete(0.0,END)                          #Deleting all the elements
        for days in Days_of_Week:                                       #List of days
            self.Last_Showing_Part.insert(END,days+":\n") 
            if days in Last_Showing:                                    #If day inside of dictionary, inserting all tuples in the list(value of day).       
                for times,course in Last_Showing[days]:
                    self.Last_Showing_Part.insert(END,times+'(%s %s),'%(course.code,course.course_name))
            else:                                                       #If day is not inside of the dictionary inserting no classes.
                self.Last_Showing_Part.insert(END,'NO CLASSES')
            self.Last_Showing_Part.insert(END,'\n')

    def Error_Message_Function(self,writing):
        error_message_window = Toplevel()
        error_message = Label(error_message_window,text = writing,font="Times 100 bold",bg = "Red",fg = "Black")
        error_message.pack()
            
    def My_Cost_Function(self,solution): 
        avaiable_courses = self.List_of_all_avaiable_courses[::]
        self.grouping_dict = dict() 
                                                                        #Copying the all avaiable courses created at above.
        total = 0                                                       #Initially total cost equals 0.
        total_overlapping_minute = 0                                    #Initially total overlapping cost equals 0.
        total_break_minute = 1                                          #Initially total length of breaks equals 1 because this will be multiplied.
        for i in range(len(solution)):
            x = int(solution[i])
            course = avaiable_courses[x]                                #It is an object,selected from copied avaiable courses with index from solution at the end
                                                                        #of the loop this course will be deleted from the copied avaiable courses.
            for time,day in course.time_and_day:                        #List of tuple.(time,day)
                self.grouping_dict.setdefault(day,[])                   #Adding the days as keys to schedule dictionary,where values are list of times in the day. 
                if self.grouping_dict[day] == []:                       #Initialazing the time list.
                    self.grouping_dict[day].append(time)
                    continue

                else:                                                   #If no need for initialization
                    for times in self.grouping_dict[day]:
                        time1,time2 = time.split('-')                   #Splitting time for using in function which converts time to minutes like 12:00 = 720
                        time3,time4 = times.split('-')
                        
                        time1,time2,time3 = optimization.getminutes(time1),optimization.getminutes(time2),optimization.getminutes(time3)
                        time4 = optimization.getminutes(time4)          #Converting the times to minutes.12:00 = 720
                
                        if time1 >= time3 and time4 > time1:            #Overlapping situations
                            if time4 >= time2:                          #For example; time1 = 12:00 , time2 = 13:00; time3 = 11:30, time4 = 13:30
                                total_overlapping_minute += time2-time1 #Overlapping_minute = 13:00-12:00 = 60 minutes 
                            else:                                       #For example; time1 = 12:00 , time2 = 13:00; time3 = 11:30, time4 = 12:30
                                total_overlapping_minute += time4-time1 #Overlapping_minute = 12:30-12:00 = 30 minutes      

                        elif time3 > time1 and time2 > time3:
                            if time4 >=time2:                           #For example; time1 = 11:00 , time2 = 13:00; time3 = 11:30, time4 = 13:30
                                total_overlapping_minute += time2-time3 #Overlapping_minute = 13:00-11:30 = 90 minutes 
                            else:                                       #For example; time1 = 12:00 , time2 = 13:30; time3 = 12:30, time4 = 12:30
                                total_overlapping_minute += time4-time3 #Overlapping_minute = 12:30-11:30 = 60 minutes 
                                
                    self.grouping_dict[day].append(time)                #This time is added to schedule
                    self.grouping_dict[day].sort()                      #Sorting accoring to their times inside of days
                    
            del avaiable_courses[x] 

        for list_of_time_intervals in self.grouping_dict.values():      #Looking each day's times.
            if len(list_of_time_intervals) == 1:                        #If there is no more than one course in a day there will be no break between courses in a day.
                continue

            for index in range(len(list_of_time_intervals)-1):          #This for is untill the last second element because it always look the next element in loop.
                earlier_time = optimization.getminutes(list_of_time_intervals[index].split('-')[1])
                                                                        #Finish time of the first course(sorted),minutes
                later_time = optimization.getminutes(list_of_time_intervals[index+1].split('-')[0])
                                                                        #Starting time of the second course(sorted),minutes
                if (later_time - earlier_time) > 0:                     #If it is smaller than 0,it means there is overlapping and it is calculated.
                    total_break_minute *= float(later_time-earlier_time)

        substraction_because_of_free_days = 0 
        for i in Days_of_Week:                                          #List of days
            if i not in self.grouping_dict.keys():                      #If this day not in our schedule we will substract 1000,and this day is Monday,Friday
                                                                        #or Weekend day we will substract 2000
                if i == "Monday" or i == "Friday" or i == "Saturday" or i == "Sunday":
                    substraction_because_of_free_days += 2000
                else:
                    substraction_because_of_free_days += 1000
          
                
        total = (total_overlapping_minute*1000) + (total_break_minute/1000) - substraction_because_of_free_days

        return total                                                    #Returning the total cost.

    def My_Representation_function(self,solution):                      #This takes list of indexes like in the cost function
        avaiable_courses = self.List_of_all_avaiable_courses[::]
        last_showing_dictionary = dict()                                #Avaiable courses again is copied.
        
        for i in range(len(solution)):
            x = int(solution[i])
            course = avaiable_courses[x]
            
            for time,day in course.time_and_day:
                last_showing_dictionary.setdefault(day,[])
                last_showing_dictionary[day].append((time,course))      #Creating a dictionary with groups of days and each day is sorted accoring to times.
                last_showing_dictionary[day].sort()
                
            del avaiable_courses[x]

        return last_showing_dictionary                                  #Returns a dictionary where keys are days and where values are list of tuples(time,course).

App = Course_Schedule_Advisor()
