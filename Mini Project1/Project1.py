from recommendations import *
from Tkinter import *
from xlrd import *
from tkFileDialog import *
import ttk


class Virtual_Advisor(object):
    def __init__(self):

        self.main_window = Tk()
        self.main_window.geometry("950x700")
        self.main_window.resizable(width= False,height = False)                 
        self.Interface()
        mainloop()
        
    def Interface(self):
        Title = Label(text = "Virtual Advisor 1.0",bg = "White" ,font = "Times 50 italic",width = 100)
        Title.pack()

        Background = Label(bg = "Purple" ,font = "Times 500 italic",width = 100)    #It is background
        Background.pack()
        
        First_Button = Button(text = "Load Past Student Grades" ,font = "Times 20 italic",command = self.First_Button_Command,bg = "red")
        First_Button.place(relx = 0.0,rely = 0.18,width = 425,height = 100)
        
        Second_Button = Button(text = "Load Your Current Transcript" ,font = "Times 20 italic",command = self.Second_Button_Command,bg = "red")
        Second_Button.place(relx = 0.56,rely = 0.18,width = 450,height = 100)

        self.radio_values = IntVar()
        self.Radio_Button1 = Radiobutton(text = "Userbased",variable=self.radio_values,value = 1,bg = "red",font = "Times 10 italic")
        self.Radio_Button1.place(relx = 0.34,rely = 0.355,width = 100,height = 35)
        self.Radio_Button2 = Radiobutton(text = "ItemBased",variable=self.radio_values,value = 2,bg = "red",font = "Times 10 italic")
        self.Radio_Button2.place(relx = 0.34,rely = 0.40,width = 100,height = 34.5)
        self.radio_values.set(1)                                                #As default value Userbased will be filled
        Name_of_Radio_Buttons = Label(text="""Collaborative \n  Choosing Type:""",bg="red",font="Times 20 italic")
        Name_of_Radio_Buttons.place(relx=0.0,rely=0.355,height = 66,width = 325)

        self.combobox_value = StringVar()
        self.box = ttk.Combobox(self.main_window,textvariable = self.combobox_value,state ='reodanly')
        self.box['values'] = ('Pearson','Jaccard','Euclidean')
        self.box.place(relx = 0.80,rely = 0.35,width = 150,height = 20)
        self.box.set('Pearson')                                                 #As default value Pearson will be shown
        Name_of_the_Combo_Box = Label(text = """Similarity\nMeasure:""",bg="red",font="Times 20 italic")
        Name_of_the_Combo_Box.place(relx = 0.56,rely = 0.35,width = 228)
        
        Fourth_Button = Button(text = """See the Recommended \nCourses""",font = "Times 20 italic",command = self.Fourth_Button_Command,bg = "red")
        Fourth_Button.place(relx = 0.0,rely = 0.5,width = 425,height = 100)


    file_opt = options = {}
    options['defaultextension'] = '.xlsx'
    options['initialdir'] = 'C:\\'

    all_grades = dict()                             #This will be the dictionary like critics in the recommendations.py
    all_grades_values = {u'A+':4.1,u'A':4.0,u'A-':3.7,u'B+':3.3,u'B':3.0,u'B-':2.7,u'C+':2.3,u'C':2.0,u'C-':1.7,u'D+':1.3,u'D':1.0,u'D-':0.5,u'F':0.0}
    #This dictionary will be used to convert the letter grades to the calculatable grade to find similarities.
    
    def Transkripts(self,a):                        #This function has parameter as the opened excel-file with the askopenfilename(s) functions.
        book = open_workbook(a)
        sheet = book.sheet_by_index(0)
        Virtual_Advisor.all_grades[a] = dict()      #The filename will be key and its value will be another dictionary with
        self.Course_Codes_to_Names = dict()         #the keys are the tuples of the name and the code of the course and the values are the letter grades of courses.

        for row_index in range(1,sheet.nrows):      #It starts from 1 because the first row is just the names of the columns so this row is skipped.
            for col_index in range(0,sheet.ncols,2):
                if sheet.cell(row_index,col_index).value not in Virtual_Advisor.all_grades_values:
                    Virtual_Advisor.all_grades[a][(str(sheet.cell(row_index,col_index).value),str(sheet.cell(row_index,col_index+1).value))] = Virtual_Advisor.all_grades_values[sheet.cell(row_index,col_index+2).value]
                    #all_grades = {filename:{(course_code,course_name):converted_grade}}                                                        #This automatically get the value of the grade                   

    def Grade_Converter(self,grade):            #The last conversion from float-number grade to the letter grade to show.
        
        if grade > 4.0 and grade <=4.1:
            return "A+"
        elif grade > 3.7 and grade <= 4.0:
            return "A"
        elif grade > 3.3 and grade <= 3.7:
            return "A-"
        elif grade > 3.0 and grade <= 3.3:
            return "B+"
        elif grade > 2.7 and grade <= 3.0:
            return "B"
        elif grade > 2.3 and grade <= 2.7:
            return "B-"
        elif grade > 2.0 and grade <= 2.3:
            return "C+"
        elif grade > 1.7 and grade <= 2.0:
            return "C"
        elif grade > 1.3 and grade <= 1.7:
            return "C-"
        elif grade > 1.0 and grade <= 1.3:
            return "D+"
        elif grade > 0.7 and grade <= 1.0:
            return "D"
        elif grade > 0.3 and grade <= 0.7:
            return "D-"
        elif grade > 3.0 and grade <= 3.3:
            return "B+"
        elif grade > 2.7 and grade <= 3.0:
            return "B"
        elif grade > 0.0 and grade <= 0.3:
            return "F"

    def calculateSimilarItems_Revised(self,prefs, n=10,similarity = sim_distance):          #This function is copied directly from the recommendations.py but one more parameter added 
        result = {}                                                                         #similarity parameter added due to change which type of similarity measure will be used
        itemPrefs = transformPrefs(prefs)
        c = 0
        for item in itemPrefs:
            c += 1
            if c % 100 == 0: print "%d / %d" % (c, len(itemPrefs))
            scores = topMatches(itemPrefs, item, n=n, similarity=sim_distance)
            result[item] = scores
        return result

    def Error_Message_Function(self):                                                       #Message for error showing
        error_message_window = Toplevel()
        error_message = Label(error_message_window,text = """Fatal Error!\nPlease Enter the \nTranskripts properly""",font="Times 100 bold",bg = "Red",fg = "Black")
        error_message.pack()

        
     
    def First_Button_Command(self):
        try:
            self.filenames = askopenfilenames(**Virtual_Advisor.file_opt)
            self.splitted_filenames = list(self.filenames)
            for files in self.splitted_filenames:                                               #Each file will be one key of the dictionary of all_grades
                self.Transkripts(files)
        except IOError:                                                                         #If user do not select file from askopenfilename button
            pass
            
            
    def Second_Button_Command(self):
        try:
            self.filename = askopenfilename(**Virtual_Advisor.file_opt)
            self.Transkripts(self.filename)
        except IOError:                                                                         #If user do not select file from askopenfilename button
            pass
        
    def Fourth_Button_Command(self):
        
        try:                                                                               #Trying to catches the exceptions like not getting the transkripts properly.
            for i in self.splitted_filenames:
                if i:
                    pass
            if self.filename:
                pass
        except (AttributeError,IOError,KeyError):
            self.Error_Message_Function()
            return 

        if len(Virtual_Advisor.all_grades) == 1 or len(Virtual_Advisor.all_grades) ==0:         #If the all_grades dictionary empty or just have one key.
            self.Error_Message_Function()           
            return
            
        if self.radio_values.get() == 1:                                                    #User Based Filtering
            if self.combobox_value.get() == "Pearson":
                all_recommended_courses = getRecommendations(Virtual_Advisor.all_grades,self.filename,similarity=sim_pearson)
        
            elif self.combobox_value.get() == "Euclidean":
                all_recommended_courses = getRecommendations(Virtual_Advisor.all_grades,self.filename,similarity=sim_distance)
                
            elif self.combobox_value.get() == "Jaccard":
                all_recommended_courses = getRecommendations(Virtual_Advisor.all_grades,self.filename,similarity=sim_jaccard2)
                
        elif self.radio_values.get() == 2:                                                  #Item Based Filtering
            if self.combobox_value.get() == "Pearson":
                new_grades = self.calculateSimilarItems_Revised(Virtual_Advisor.all_grades,similarity=sim_pearson)   #The copied version of function is used.
                all_recommended_courses = getRecommendedItems(Virtual_Advisor.all_grades,new_grades,self.filename)
        
            elif self.combobox_value.get() == "Euclidean":
                new_grades = self.calculateSimilarItems_Revised(Virtual_Advisor.all_grades,similarity=sim_distance)
                all_recommended_courses = getRecommendedItems(Virtual_Advisor.all_grades,new_grades,self.filename)
    
            elif self.combobox_value.get() == "Jaccard":
                new_grades = self.calculateSimilarItems_Revised(Virtual_Advisor.all_grades,similarity=sim_jaccard2)
                all_recommended_courses = getRecommendedItems(Virtual_Advisor.all_grades,new_grades,self.filename)

        first_title = "Recommended Course"                                                                #Titles of the Columns
        second_title = "Predicted Grade"
        
        List_of_Recommended_Courses_c1 = Listbox(self.main_window,font="Times 12 bold")         #First Column
        List_of_Recommended_Courses_c1.place(relx = 0.0,rely = 0.65,width = 500,height = 250)
        List_of_Recommended_Courses_c1.tk_setPalette("#D0A9F5")
        List_of_Recommended_Courses_c1.delete(ACTIVE)                                           #Always Deleting all current writings not to be confused with new ones
        List_of_Recommended_Courses_c1.insert(END,first_title)                                  #The Title of the column

        List_of_Recommended_Courses_c2 = Listbox(self.main_window,font="Times 12 bold")         #Second Column
        List_of_Recommended_Courses_c2.place(relx = 0.5,rely = 0.65,width = 500,height = 250)
        List_of_Recommended_Courses_c2.tk_setPalette("#D0A9F5")
        List_of_Recommended_Courses_c2.delete(ACTIVE)                                           #Always Deleting all current writings not to be confused with new ones
        List_of_Recommended_Courses_c2.insert(END,second_title)                                 #The Title of the column

 
        counter = 0                                                                             #It counts how many row will be shown
        for i,j in all_recommended_courses:
            counter += 1
            List_of_Recommended_Courses_c1.insert(END,j[0]+" "+j[1])                            #Inserting on the first column
            List_of_Recommended_Courses_c2.insert(END,self.Grade_Converter(i)+" (%s)"%str(i))   #Inserting on the second column
            
            if counter == 6:
                break
        
App = Virtual_Advisor()

