
from Tkinter import *
from BeautifulSoup import *
from urllib2 import *
from urlparse import urljoin
import ttk,docclass

database = dict()

class Guess_My_Departmant():
    def __init__(self):
        self.Interface()

    def Interface(self):
        #Main window part
        self.main_window = Tk()
        self.main_window.geometry("1000x700+100+-10")
        self.main_window.resizable(width=False,height=False)
    
        #Background part
        self.Main_Background = Label(bg="light blue")
        self.Main_Background.place(relx = 0.0,rely = 0.0,width = 1000,height = 1000)

        #Title of project part
        self.Main_Title = Label(text = 'Guess My Departmant',font = "Times 30 bold",bg = "light green")
        self.Main_Title.place(relx = 0.1,rely = 0.0,width = 800)

        #Title of Entry
        self.Url_offering_title = Label(text = "Provide SEHIR Faculty List URL:",font = "Times 13 bold",bg = "light green")
        self.Url_offering_title.place(relx = 0.1,rely = 0.1)

        #Entry of URL(Entry)
        self.Url_taker = Entry()
        self.Url_taker.place(relx = 0.1,rely = 0.15,width = 800,height = 25)

        #Button of Fetching(Button)
        self.Fetching_url = Button(text = """Fetch Faculty Profiles""",font= "Times 13 bold",bg = "light green",command = self.Command_of_fetching)
        self.Fetching_url.place(relx = 0.1,rely=0.2,width = 200,height = 40)

        #Status Showing Part(Listbox)
        self.Status_shower = Listbox(font = "Times 10 bold")
        self.Status_shower.place(relx = 0.1,rely = 0.27,width = 800,height = 150)

        #Scrollbar
        self.scroll = Scrollbar(self.Status_shower)
        self.scroll.pack(side=RIGHT,fill=Y)
        self.scroll.config(command = self.Status_shower.yview)

        #Classification Method Part
        self.Title_of_classification_method = Label(text = """Choose\nClassfication\nMethods:""",font = "Times 15 bold",bg="light green")
        self.Title_of_classification_method.place(relx = 0.1,rely=0.5)

        #RadioButtons
        self.Radio_values = IntVar()
        self.Bayes_radio = Radiobutton(text = "Naive Bayes",variable=self.Radio_values,value = 1,bg = "light green",font = "Times 15 bold")
        self.Bayes_radio.place(relx = 0.25,rely= 0.5)
        self.Fisher_radio = Radiobutton(text = "Fisher",variable=self.Radio_values,value = 2,bg = "light green",font = "Times 15 bold")
        self.Fisher_radio.place(relx = 0.25,rely= 0.54)

        #Selecting Professor Name(Combobox)
        self.Prof_name_selection = Label(text = "Select a\nProfessor:",font = "Times 15 bold",bg = "light green")
        self.Prof_name_selection.place(relx = 0.1,rely = 0.64)
        
        self.Prof_name_variable = StringVar()
        self.Professor_combobox = ttk.Combobox(textvariable = self.Prof_name_variable,state = "readonly")
        self.Professor_combobox.place(relx = 0.25,rely =0.64,width = 250)

        #Selecting Treshold Part(Listbox,2 button,entry,combox)
        self.Title_of_setting_treshold = Label(text = "Set the Tresholds:",font = "Times 13 bold",bg = "light green")
        self.Title_of_setting_treshold.place(relx=0.6,rely = 0.5)

        #Listbox
        self.Treshold_Shower = Listbox()
        self.Treshold_Shower.place(relx =0.6 ,rely=0.55,width = 200,height = 100)

        #Button for removing
        self.Button_of_removing = Button(text = """Remove\nSelected""",font = "Times 13 bold",bg = "light green",command = self.Command_of_removing)
        self.Button_of_removing.place(relx = 0.81,rely = 0.55,width = 90)

        #Combobox for Faculties
        self.Faculty_name_variable = StringVar()
        self.Faculty_combobox = ttk.Combobox(textvariable = self.Faculty_name_variable,state="readonly")
        self.Faculty_combobox.place(relx = 0.6,rely =0.71,width = 200)

        #Entry
        self.Entry_for_treshold = Entry(font = "Times 13 bold")
        self.Entry_for_treshold.place(relx =0.81,rely = 0.71,width =42.5,height = 20)

        #Button for Setting
        self.Button_of_setting = Button(text = "Set",font="Times 13 bold",bg="light green",command=self.Command_of_setting)
        self.Button_of_setting.place(relx = 0.86,rely=0.71,width=42.5,height = 22)

        #Button for Guessing_Departmant
        self.Button_of_guessing = Button(text="Guess the Depertamant of the Selected Professor",font="Times 13 bold",bg ="light green",command = self.Command_of_guessing)
        self.Button_of_guessing.place(relx = 0.1,rely = 0.8,width = 400)

        #Title of Last Part
        self.Title_of_last_part = Label(text = "Predicted Department:",font="Times 15 bold",bg = "light green")
        self.Title_of_last_part.place(relx = 0.1,rely =0.9,width = 200,height = 50)
        
        mainloop()

    def Command_of_fetching(self):
        url = self.Url_taker.get()                                      #Taking the url from entry for getting the informations.
        if len(url) < 10:                                               #If url is not proper for the fetching,program will show an error.
            self.Error_Message_Function("""Please give\na proper url for\nFetching""")
            return
        soup = self.opening_url_and_making_soup(url)                    #Making soup the informations inside of the url.
        
        initially_all_departments = list()                              #List of all departments
        all_uniqe_departments = list()                                  #List of fetched departments (professor names in these departments are fetched)
        all_professor_name = list()                                     #List of all professor name
        for i in soup.fetch():                                          #It fetchs all the tags
            if 'class' in dict(i.attrs) and i['class'] == 'ms-rteElement-H3B':
                                                                        #This if only takes the department names in a listed way,department name always updated,
                                                                        #in the end it takes valid departments due to the fact that the bottom if clause
                department = i.text.upper()                             #Bottom if claues means if it has a link take it so department will be true in this way.
            if i.get('href') != None and i.get('href').split('=')[0] == '/en/Pages/Academic/AcademicList.aspx?akademid':
                if department not in initially_all_departments:         
                    initially_all_departments.append(department)        #Appending all uniqe department names to the list.
        self.Status_shower.insert(END,"FETCHING DEPARMENT AND PROFESSOR LIST(Done)")
        self.Status_shower.update()
        counter_for_teacher = 0                                         #This counts how many professor exist
        counter_for_information = 0                                     #This counts how many professor information exist
                                                                        #These counter is for correcting that each professor has one biography,because some prof.
                                                                        #has no biography.
        for i in soup.fetch():                                          #it fetchs all tags.
            if 'class' in dict(i.attrs) and i['class'] == 'ms-rteElement-H3B':
                                                                        #Again taking the correct department names like at the above.
                department = i.text.upper()
            if i.get('href') != None and i.get('href').split('=')[0] == '/en/Pages/Academic/AcademicList.aspx?akademid':
                                                                        #Taking urls like at the above but this time we will fetch all urls and then take the names
                new_url = urljoin(url,i.get('href'))                    #and biographies of teachers.
                new_soup = self.opening_url_and_making_soup(new_url)
                for j in new_soup.fetch('span'):                        #Taking the names of professors.
                    if 'class' in dict(j.attrs) and j['class'] == "isim bolder":
                        prof_name = j.text
                        counter_for_teacher += 1                        #Incrementing the counter of professor name.
                for k in new_soup.fetch('div'):
                    if 'class' in dict(k.attrs) and k['class'][0:8] == "External":
                        information = k.text                            #Taking the biography of professors.
                        counter_for_information += 1                    #Incrementing the counter of biography.
                        break    
                if counter_for_teacher != counter_for_information:      #Some Professors do not have any biography.
                    information = ' '                                   #If a professor has not biography,we assign its biography as empty string.
                    counter_for_information += 1                        #Incrementing the counter of biography.
                    
                if department not in all_uniqe_departments:             #Adding the uniqe fetched departments.
                    all_uniqe_departments.append(department)            
                    if len(all_uniqe_departments) == 1:                 #This means if it first departmant is now fetching, it is in progress.
                        self.Status_shower.delete(0,END)
                        self.Status_shower.insert(END,"FETCHING DEPARMENT AND PROFESSOR LIST(Done)")
                        self.Status_shower.insert(END,"%s(In Progress)"%all_uniqe_departments[0])
                        
                        
                        for pendings in range(1,len(initially_all_departments)-1):
                                                                        #Others are pending
                            self.Status_shower.insert(END,"%s(Pending)"%initially_all_departments[pendings])
                        self.Status_shower.update()
                    else:                                               #This means if other(not first) is now fetching.
                        self.Status_shower.delete(0,END)
                        self.Status_shower.insert(END,"FETCHING DEPARMENT AND PROFESSOR LIST(Done)")
                        for departments in range(len(all_uniqe_departments)-1):
                                                                        #It takes all elements in the list except last one because last one is now fetching so others
                                                                        #will be 'done' last one will be 'in progress'
                            self.Status_shower.insert(END,'%s(Done)'%all_uniqe_departments[departments])
                            self.Status_shower.update()
                        self.Status_shower.insert(END,'%s(In progress)'%all_uniqe_departments[len(all_uniqe_departments)-1])
                        
                        for pendings in range(len(all_uniqe_departments),len(initially_all_departments)-1):
                            self.Status_shower.insert(END,"%s(Pending)"%initially_all_departments[pendings])
                                                                        #Other departments not in the list will be pending.
                        self.Status_shower.update()
                all_professor_name.append(prof_name)                    #Adding the professor names to the list.
                database[(department,prof_name)] = information          #Adding prof_name,his/her department with their biographies to the database. 

        self.Status_shower.delete(END)
        self.Status_shower.insert(END,'%s(done)'%all_uniqe_departments[len(all_uniqe_departments)-1]) 
        self.Status_shower.update()                                     #Inserting the last element to the listbox as 'done'
        all_uniqe_departments.sort(),all_professor_name.sort()
        self.Faculty_combobox['values'] = tuple(all_uniqe_departments)  #Inserting department names to the combobox
        self.Professor_combobox['values'] = tuple(all_professor_name)   #Inserting professor names to the combobox
        
    def opening_url_and_making_soup(self,url):                          #At this level url is opened by urllib2 then it is read finally it is made a soup by BS.
        request = Request(url)
        response = urlopen(request)                                     
        html_version = response.read()   
        soup = BeautifulSoup(html_version.decode('utf-8','ignore'))     #Decoding is for Turkish Characters in the professor names.
        return soup

    def Command_of_removing(self):
        selections =  map(int,self.Treshold_Shower.curselection())
        for i in selections:
            self.Treshold_Shower.delete(i)                              #Deleting the selected department in the lisbox of treshold values.
            
    def Command_of_setting(self):                                       
        value_of_treshold = self.Entry_for_treshold.get()               #Value of treshold
        course_name_for_treshold = self.Faculty_name_variable.get()     #Which department will have treshold
        treshold_values_for_departments = self.Treshold_Shower.get(0,END)
                                                                        #Already what we have as treshold values.
        real_values_of_tresholds = dict([(str(i.split('-')[1]),float(i.split('-')[0])) for i in treshold_values_for_departments])
                                                                        #Dictionary where keys are departments and values are float number of treshold.
        if course_name_for_treshold in real_values_of_tresholds:        #If we already have the treshold value of this department,program will give an error.
            self.Error_Message_Function("""It already has\na treshold value""")
            return
        else:
            self.Treshold_Shower.insert(END,"%s-%s"%(value_of_treshold,course_name_for_treshold))
        
    def Command_of_guessing(self):
        if len(database) < 2:
            self.Error_Message_Function("""Please first\nfetch before \nguessing""")
            return
        treshold_values_for_departments = self.Treshold_Shower.get(0,END)
        real_values_of_tresholds = dict([(str(i.split('-')[1]),float(i.split('-')[0])) for i in treshold_values_for_departments])
                                                                        #Dictionary where keys are departments and values are float number of treshold like above one.
        classification_type = self.Radio_values.get()                   #Classification type
        if classification_type == 0:
            self.Error_Message_Function("""Please choose\na classification type\nfor guessing""")
            return                                                      #If any of the classification is not selected,program will give an error.
        selected_professor_name = self.Prof_name_variable.get()         #Professor name
        if selected_professor_name == '':                               #If any of the professor name is selected, program will give an error.
            self.Error_Message_Function("""Please select\na professor name\nfor guessing""")
            return
        if classification_type == 1:                                    #Naive Bayes
            my_object_for_classification = docclass.naivebayes(docclass.getwords)
                                                                        #Creating objects.
            for faculty in real_values_of_tresholds:                    #Setting the treshold values
                my_object_for_classification.setthreshold(faculty,real_values_of_tresholds[faculty])
            for departments,prof_name in database.keys():               
                if prof_name == selected_professor_name:                #We will train the object with information of all profs except selected one.
                    real_answer = departments                           #Department of selected proffessor
                    continue
                my_object_for_classification.train(database[(departments,prof_name)],departments)

            classification_result = my_object_for_classification.classify(database[(real_answer,selected_professor_name)])
                                                                        #Classifaction Result.
                    
        else:                                                           #Fisher
            my_object_for_classification = docclass.fisherclassifier(docclass.getwords)
                                                                        #Creating objects.
            for faculty in real_values_of_tresholds:                    #Setting the treshold values
                my_object_for_classification.setminimum(faculty,real_values_of_tresholds[faculty])

            for departments,prof_name in database.keys():               #We will train the object with information of all profs except selected one.
                if prof_name == selected_professor_name:                #Department of selected proffessor
                    real_answer = departments
                    continue
                my_object_for_classification.train(database[(departments,prof_name)],departments)

            classification_result = my_object_for_classification.classify(database[(real_answer,selected_professor_name)])
                                                                        #Classifaction Result.

        if classification_result == real_answer:                        #True case
            my_showing_label = Label(text = classification_result,bg="green")
            my_showing_label.place(relx=0.3,rely=0.9,width=600,height =50)
        elif classification_result == None:                             #Unknown case
            my_showing_label = Label(text = "Unknown",bg="Blue")
            my_showing_label.place(relx=0.3,rely=0.9,width=600,height =50)
        else:                                                           #False case
            my_showing_label = Label(text = classification_result+"(Correct Answer:"+real_answer+')',bg="red")
            my_showing_label.place(relx=0.3,rely=0.9,width=600,height =50)

    def Error_Message_Function(self,writing):
        error_message_window = Toplevel()
        error_message = Label(error_message_window,text = writing,font="Times 100 bold",bg = "Red",fg = "Black")
        error_message.pack()
        

App = Guess_My_Departmant()
