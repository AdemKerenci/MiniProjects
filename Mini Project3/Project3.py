from Tkinter import *
import os,time

#This class contains interface part,initalizing part and lastly searching part.For initialzing part we have used 5 functions; Wordlocation_creator ,
#citations_citation_counts_pagerank creator,pagerank_calculator. The other 2 functions just copied from searchengine.py. For searching we have used 3 functions;
#Searcher,command_of_next and command_of_previous.

class LibrarySearcher():
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
        self.Main_Title = Label(text = 'Digital Library Search Engine',font = "Times 35 bold",bg = "Orange",fg = "White")
        self.Main_Title.place(relx = 0.1,rely = 0.005,width = 800)

        #Time Showing Part
        self.time_shower = Label(bg = "light blue",font="Times 10 bold")
        self.time_shower.place(relx =0.1,rely =0.2,height =15)

        #Entry Part
        self.Keyword_Entry = Entry(font = "Times 15 bold",bg = "white")
        self.Keyword_Entry.place(relx = 0.2,rely = 0.1,width = 600)

        #Button For Initalizition
        self.Initialize_Button = Button(text = "Initialize",font = "Times 10 bold",command = self.Command_of_Initialization)
        self.Initialize_Button.place(relx = 0.45,rely = 0.15,width = 100)

        #Text Widget For Showing
        self.Shower = Text(font = "Times 10")
        self.Shower.place(relx= 0.1,rely=0.22,width=800,height=500)

        #Bottom Part(2 buttons,2 labels)
        self.label_of_page = Label(text = "Page:",bg = "Light Blue",font = "Time 10 bold")
        self.label_of_page.place(relx = 0.65,rely = 0.95)

        self.Button_Previous = Button(text = "Previous",font = "Time 10 bold",command = self.command_of_previous)
        self.Button_Previous.place(relx = 0.7,rely = 0.945)

        self.Label_of_page_number = Label(text = "1",bg = "orange",fg = "white",font = "Time 10 bold")
        self.Label_of_page_number.place(relx = 0.78,rely = 0.95,width = 50)

        self.Button_Next = Button(text = "Next",font = "Time 10 bold",command = self.command_of_next)
        self.Button_Next.place(relx = 0.84,rely = 0.945,width = 60)
        
        mainloop()

    def Command_of_Initialization(self):
        self.Shower.delete(0.0,END)
        self.Shower.insert(END,"Please wait while the search engine performs the initializiton phase:"+"\n")
        self.Shower.insert(END," "*3+"Loading Paper Metadata...(in progress...)")
        self.Shower.update()
        
        self.Wordlocations = self.Word_location_dictionary_creator()    #It is a nested dictionary with words keys values are dictionarty and inside keys are ids
                                                                        #inside values are the indexes of word appears in id.
        self.Shower.delete(0.0,END)
        self.Shower.insert(END,"Please wait while the search engine performs the initializiton phase:"+"\n")
        self.Shower.insert(END," "*3+"Loading Paper Metadata...(downloaded)"+"\n")
        self.Shower.insert(END," "*3+"Loading Citation Data...(in progress...)")
        self.Shower.update()
        print "Paper Metadata completed"
        
        self.Citations = self.Citation_and_Citationcounts_and_Pagerank_dictionaries_creator()
                                                                        #This function returns one dictionary but create and populate 3 dictionary in total
        self.Shower.delete(0.0,END)
        self.Shower.insert(END,"Please wait while the search engine performs the initializiton phase:"+"\n")
        self.Shower.insert(END," "*3+"Loading Paper Metadata...(downloaded)"+"\n")
        self.Shower.insert(END," "*3+"Loading Citation Data...(downloaded)"+"\n")
        self.Shower.insert(END," "*3+"Computing PageRank Scores...(in progress...)")
        self.Shower.update()
        print "Citation Data completed"

        self.Pageranks = self.Pagerank_Scores_Computer()                #This function returns pageranks,we can change the number of iteration with putting a number 
        self.Shower.delete(0.0,END)                                     #as parameter
        self.Shower.insert(END,"Please wait while the search engine performs the initializiton phase:"+"\n")
        self.Shower.insert(END," "*3+"Loading Paper Metadata...(downloaded)"+"\n")
        self.Shower.insert(END," "*3+"Loading Citation Data...(downloaded)"+"\n")
        self.Shower.insert(END," "*3+"Computing PageRank Scores...(downloaded)")
        self.Shower.update()
        print "Page rank scores completed"

        self.Initialize_Button.configure(text = 'Search')
        self.Initialize_Button.configure(command = self.Searcher)

    def Word_location_dictionary_creator(self):
        self.Id_Title_Dictionary = dict()                               #This dictionary is for converting from id to title name.
        Wordlocations = dict()                                          #This is for indexing.It is a nested dictionary
        for i in os.listdir(os.curdir):                                                                  
            if i == "metadata":                                         #Finding the directory named as metadata
                os.chdir(i)                                             #Going inside of the metadata directory
                break
        for i in os.listdir(os.curdir):                                 #Looking for all the pages                       
            open_file = open(i)                                         
            read = open_file.read()
            open_file.close()                                           #Closing each page
            
            first_split = read.split('\\\\')                            #It splits from lines with \\.
            abstract_part = first_split[len(first_split)-2]             #Last element of list is just '',and last second element is always abstract.
            Id_of_book = first_split[1].split('/')[1].split('\n')[0]    #Id is always in the line start with 'Paper' which is in the second element of list
                                                                        #We need extra 2 split to get id.
            second_split = read.split('\n\n')                           #It splits from lines with nothing.
            third_split = second_split[1].split("Author")               #This split for getting the part with starting with 'Title:'
            Title_of_book = third_split[0]
            Title_of_book = Title_of_book.split('Title:')               #Get rid of 'Title:',prufying the name of title.
            del Title_of_book[0]                                        
            Title_of_book = ''.join(Title_of_book)
            Title_of_book = Title_of_book.split('\n')                   #Some titles can be with more than one line.
            Title_of_book = "".join(Title_of_book)

            
            words_in_title = [self.separatewords_revised(words) for words in Title_of_book.split('\n') if words != '']
            words_in_abstract = [self.separatewords_revised(words) for words in abstract_part.split('\n') if words != '']
            
            all_words_in_list = list()                                  #This list contains the title and abstract of each page in each iteration
            for lists in words_in_title:
                all_words_in_list.extend(lists)
            for lists in words_in_abstract:
                all_words_in_list.extend(lists)
                
            self.Id_Title_Dictionary[Id_of_book] = Title_of_book        #Getting Each id's title.
            
            for i in range(len(all_words_in_list)):                     #To get indexes of word.
                Wordlocations.setdefault(all_words_in_list[i],{})       #The keys of dictionary are words,values are dictionary
                Wordlocations[all_words_in_list[i]].setdefault(Id_of_book,[])
                                                                        #keys are the id and values are indexes.
                Wordlocations[all_words_in_list[i]][Id_of_book].append(i)
            
        
        os.chdir(os.pardir)                                             #Making current directory as it is in before.
        return Wordlocations

    def separatewords_revised(self,text):                               #The same function in searchengine.
        splitter=re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!='']

        
    def Citation_and_Citationcounts_and_Pagerank_dictionaries_creator(self):
        self.Initialpageranks = dict()                                  
        self.Citationcounts = dict()                                    
        Citations = dict()
        file_of_citation = open("citations.txt")                        #Opening citations.txt
        read = file_of_citation.read()
        file_of_citation.close()
        list_of_lines = read.split('\n')

        citing_and_cited_paper_list = [tuple(lines.split('\t')) for lines in list_of_lines[2:-1]]
                                                                        #Firs two lines are useless so they are neglegted
                                                                        #List of tuples (citing,cited)
        for citing,cited in citing_and_cited_paper_list:                
            Citations.setdefault(cited,[])                              #Dictionary: keys are id of cited papers,values are list of id of citing papers
            Citations[cited].append(citing)

            self.Citationcounts.setdefault(citing,0)                    #Dictionary: keys are id of citing papers,values are times of citation.
            self.Citationcounts[citing] += 1
                
            self.Initialpageranks.setdefault(citing,1.0)                #Initially all the paper's pageranks are 1.
            self.Initialpageranks.setdefault(cited,1.0)

        return Citations

    def Pagerank_Scores_Computer(self,times_of_looping=20):             #This function for computing pageranks of papers.
        Pageranks = self.Initialpageranks                               #Initially all pageranks are 1.0
        for i in range(times_of_looping):   
            for cited,list_of_citing in self.Citations.items():
                pr = 0.15                           
                for citing in list_of_citing:
                    pr += 0.85*(Pageranks[citing]/self.Citationcounts[citing])
                Pageranks[cited] = pr                                   #This is the formula for computing pageranks.
                
        Pageranks = self.normalizescores_revised(Pageranks)             #Normalizing the pageranks.
        return Pageranks

    def normalizescores_revised(self,scores,smallIsBetter=0):
        vsmall=0.00001                                                  # Avoid division by zero errors
        if smallIsBetter:
          minscore=min(scores.values())
          return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) in scores.items()])
        else:
          maxscore=max(scores.values())
          if maxscore==0: maxscore=vsmall
          return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

    def Searcher(self):
        if self.Keyword_Entry.get() == '':                              #If entry is empty it will give error
            self.Error_Message_Function()
            return
        
        first_time = time.clock()                                       #Starting time
        self.page_number = 1                                            #This is for determinin the current page
        self.Label_of_page_number.configure(text = "1")                 #Every search start with page 1.               
        self.Label_of_page_number.update()
        Ranking_computer = dict()                                       #This dictionary is for ranking.
        keywords = self.Keyword_Entry.get().split(' ')                  
        for words in keywords:                                          #This for line is for checking the keywords.
            words = words.lower()                                       #Every word must be considered at lower case.
            if words == '':                                             #Getting rid of useless elements.
                continue
            
            if words not in self.Wordlocations:                         #If keyword not in the wordlist,it will give an error.
                self.Error_Message_Function2(words)
                return
            
        for words in keywords:
            words = words.lower()
            if words == '':
                continue
            
            for ids in self.Wordlocations[words]:
                detector = True                                         #This detector is for checking whether a id in all words or not.
                for inside_words in keywords: 
                    inside_words = inside_words.lower()
                    if inside_words == '':
                        continue

                    if ids not in self.Wordlocations[inside_words]:
                        detector = False
                        break
                    
                if detector == True:
                    for inside_words in keywords:
                        inside_words = inside_words.lower()
                        if inside_words == '':
                            continue
                        
                        Ranking_computer.setdefault(ids,1)              #Content based measure
                        Ranking_computer[ids] *= len(self.Wordlocations[inside_words][ids])
            break                                                       #One word is enaugh becaue if an id not in this word no matter what other ids in other words.                                              
        
        try:                                                            #Normalizing
            Ranking_computer = self.normalizescores_revised(Ranking_computer)
        except:
            return

        for papers in Ranking_computer:                                 #Some papers are not in the Page rank dictionary
            if papers in self.Pageranks:
                Ranking_computer[papers] += self.Pageranks[papers]      #Summing the content-based and link-based measure

        self.Sorted_Ranking_Results = [(scores,self.Id_Title_Dictionary[ids]) for ids,scores in Ranking_computer.items()]
        self.Sorted_Ranking_Results.sort(reverse = True)                #Sorting the results.
        page_number,remaining = divmod(len(self.Sorted_Ranking_Results),17)
        self.maximum_page_number = page_number + 1                      #Total page number,Every page contains at most 17 papers.
        self.Shower.delete(0.0,END)
        if page_number == 0:                                            #If only one page in the system,showing all of them.
            for i in range(len(self.Sorted_Ranking_Results)):
                self.Shower.insert(END," %d-%s:  %s\n\n"%(i+1,self.Sorted_Ranking_Results[i][1],self.Sorted_Ranking_Results[i][0]))
        else:                                                           #Else,show first 17 papers in the first page.
            for i in range(17):
                self.Shower.insert(END," %d-%s:  %s\n\n"%(i+1,self.Sorted_Ranking_Results[i][1],self.Sorted_Ranking_Results[i][0]))

        last_time = time.clock()
        during_time = last_time - first_time                            #Time of searching
        self.time_shower.configure(text = "%s papers(%s seconds)"%(str(len(self.Sorted_Ranking_Results)),str(during_time)[0:6]))
                                                                        #Shows how many pages found in how much time.
        self.time_shower.place(relx =0.1,rely =0.2,height =15)
            
            
    def Error_Message_Function(self):                                   #Message for error showing
        error_message_window = Toplevel()
        error_message = Label(error_message_window,text = """Please Enter\nSome Keywords\nfor Searching""",font="Times 100 bold",bg = "Red",fg = "Black")
        error_message.pack()

    def Error_Message_Function2(self,word):                             #Message for error showing
        error_message_window = Toplevel()
        error_message = Label(error_message_window,text = """%s is\n a wrong keyword"""%word,font="Times 100 bold",bg = "Red",fg = "Black")
        error_message.pack()

    def command_of_previous(self):
        if self.page_number == 1:                                       #If page is 1 previous command will be useless.
            return
        self.page_number -= 1                                           #Every previous button substract one from the current page.
        self.Shower.delete(0.0,END)
        for i in range((self.page_number-1)*17,self.page_number*17):    #Showing the 17 papers,with depending on the current page.
            self.Shower.insert(END," %d-%s:  %s\n\n"%(i+1,self.Sorted_Ranking_Results[i][1],self.Sorted_Ranking_Results[i][0]))
            
        self.Label_of_page_number.configure(text = "%d"%self.page_number)
                                                                        #Showing the current page in the label.
        self.Label_of_page_number.update()
        

    def command_of_next(self):
        if self.page_number == self.maximum_page_number:                #If current page is maximum,next button will be useless.
            return
        self.page_number += 1                                           #Adding one to current page.
        if self.page_number == self.maximum_page_number:                #If we reach maximum page number we should show from last page to last paper.(All items)
            self.Shower.delete(0.0,END)
            for i in range((self.page_number-1)*17,len(self.Sorted_Ranking_Results)):
                self.Shower.insert(END," %d-%s:  %s\n\n"%(i+1,self.Sorted_Ranking_Results[i][1],self.Sorted_Ranking_Results[i][0]))
            
        else:                                                           #Else, we should show the 17 papers with depending on the current page number.
            self.Shower.delete(0.0,END)
            for i in range((self.page_number-1)*17,self.page_number*17):
                self.Shower.insert(END," %d-%s:  %s\n\n"%(i+1,self.Sorted_Ranking_Results[i][1],self.Sorted_Ranking_Results[i][0]))

        self.Label_of_page_number.configure(text = "%d"%self.page_number)
                                                                        #Showing current page in the label
        self.Label_of_page_number.update()

App = LibrarySearcher()
