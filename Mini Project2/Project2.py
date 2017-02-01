from BeautifulSoup import *
from urllib2 import *
from Tkinter import *
from urlparse import urljoin
import ttk,re,clusters
                                                                        #Regular Expressions
re_professor = re.compile("^(<.*>)(.*)(-.*>)$",re.VERBOSE)              #This regular expression is for getting the professor name without any tag.
re_values = re.compile("^(<.*>)(.*)(<.*>)$",re.VERBOSE)                 #This is for getting values and fields like (year 2007/5) without any tag.
re_title = re.compile("^(<.*><.*>)(.*)(<.*><.*>)$",re.VERBOSE)          #This is for getting the title of each publication without any tag.
re_alphebetic = re.compile("^([0-9A-Za-z]+)(.*)$",re.VERBOSE)           #This is for getting the words without punctuations like Pathcase: will be Pathcase only.    
re_alphebetic_with_two_words = re.compile("^([0-9A-Za-z]+)(-)([A-Za-z]+)$",re.VERBOSE)
                                                                        #This is for getting the words like taxanomy-superimposed as a one word and properly.

                                                                        #Databases 
database = dict()                                                       #This is the whole database its keys will be the professor names values will be dictionaries
                                                                        #Keys of each inside dictionary will be title of publication and values will be an object.

wordcounts = dict()                                                     #This dictionary for getting the freqeuncy of each word.Keys will be words and values will be
                                                                        #dictionary,keys of dictionaries will be prof_name and values will be frequency of word
                                                                        #in each professor.

forbided_words = ['and','or','of','a','an','on','in','the','to','for','about']


#This class if for making each publish an object.This object will have several attributes like title,authors and so on.These objects will be used in database dict.
#At first all parameters are None because not all publishes have these features so lack of a feature symbolysied with None.
class Published(object):
    def __init__(self,title=None,authors=None,year=None,date=None,type_of = None,name_of=None,volume =None,issue=None,pages=None,publisher=None,citation_count=None):
        self.title = title                                              #This attribute is for title of publish,string
        self.authors = authors                                          #This attribute is for authors of publish,string
        self.year = year                                                #This attribute is for year of publish,integer
        self.date = date                                                #This attribute is for date of publish,list ([year,month,day])
        self.type_of = type_of                                          #This attribute is for type of publish,string like Conference,Journal and etc.
        self.name_of = name_of                                          #This attribute is for venue of publish,string.
        self.volume = volume                                            #This attribute is for volume of publish,string
        self.issue = issue                                              #This attribute is for issue of publish,string
        self.pages = pages                                              #This attribute is for pages of publish,string
        self.publisher = publisher                                      #This attribute is for publisher of publish,string
        self.citation_count = citation_count                            #This attribute is for citation_count of publish,integer

#This class has three main functions;__init__,fetch,reformat and five supporter function for reformat function like groupings and sortings.
        
class GoogleScholarFetcher(object):
    def __init__(self,url):
        self.url = url                                                  #Url has taken as instance-level attribute in initialization.

    def fetch(self):                                                    #This function will use the give url in initialization.
        soup = self.opening_url_and_making_soup(self.url)               #It is a supporting function
        
        self.professor_name =  re_professor.match((str(soup.title))).group(2)
                                                                        #Regular expression used to get rid of tags.This re divide the expression to three piece and
                                                                        #always second piece is the professor name so .group(2) used in this code.

        database[self.professor_name] = dict()                          #key is added to database with value of another inside dictionary.

        for i in soup.fetch('a'):                                       #The things with 'a' has the links. 
            myvalues2 = list()                                          #This list for getting values of fields with tags like; value = 2007/6/16
            myfields2 = list()                                          #This list for getting fields with tags.                field = Publication date
                                                                        #These lists will be used by all urls so as for loop go these lists will be recreated and
                                                                        #used for each inside url.
            if ('class' in dict(i.attrs)) and (i['class'] == "gsc_a_at"):
                new_url  = urljoin(self.url,i['href'])                  #This if determined only the links we need then it add to our inside url.
                                                                        #With this way we created a proper adress for each url.

                new_soup = self.opening_url_and_making_soup(new_url)      #Same process with above it opened the inside url and made it soup.
                
                for i in new_soup.fetch('div'):
                    if ('id' in dict(i.attrs) and i['id'] == 'gsc_title'):
                        if re_title.match(str(i)) != None:              #It controls whether the re works or not.
                            self.title = re_title.match(str(i)).group(2)#Getting the title    
                  

                                                                        #Getting the fields and adds these fields with tags to the list created at the above.
                myfields2 = [i for i in new_soup.fetch('div') if(('class' in dict(i.attrs)) and (i['class'] == 'gsc_field' ))]
                                                                        #Getting the values and adds these values with tags to the list created at the above.
                myvalues2 = [i for i in new_soup.fetch('div') if(('class' in dict(i.attrs)) and (i['class'] == 'gsc_value') and (i.get('id') != 'gsc_descr')
                                                                 and(i.get('a') == None))]
        

                untagged_citation = re.findall("Cited by .*}",str(myvalues2[len(myvalues2)-2]))
                                                                        #This will return a list with tagged elements if there is no citation the list will be empty.
                                                                        #If there is a citation count it is always at the last two lines of the values.
                if len(untagged_citation) != 0:                         #It controls whether citation is or not.
                    splitted_untagged_citation = untagged_citation[0].split('</') 
                    more_splitted_citation_count = splitted_untagged_citation[0].split(' ')         
                    count_of_citation =  int(more_splitted_citation_count[2]) 
                                                                        #These things for getting the citation way properly.
                else:
                    count_of_citation = None                            #If there is no citation it will be None.
                    
                                                                        #Converting the element of the fields and values to the untagged versions.
                                                                        #This conversion could be done above but the reason behind is getting the citation count.
                untagged_information = [re_values.match(str(i)).group(2) for i in myvalues2]                                       
                untagged_information2 = [re_values.match(str(i)).group(2) for i in myfields2]

                #At initial part we know only the title and others are just None.
                title,authors,year,date,pages,volume,issue,publisher,type_of,name_of = self.title,None,None,None,None,None,None,None,None,None
                for i in range(len(untagged_information)-1):            #The -1 for not getting the last useless part of the values and fields.
                    if untagged_information2[i] == "Authors" or untagged_information2[i] == "Inventors":
                        authors = untagged_information[i]               #In this if,elif part the check is done on the fields then the values will be getting
                                                                        #because always the length of the values and fields lists will be the same and indexes also.
                    elif untagged_information2[i] == "Publication date":
                        date = list()
                        whole_date = untagged_information[i].split('/') 
                        for i in whole_date:
                            date.append(int(i))                         #Date is the list of integers.
                        year = date[0]                                  #Year is an integer which is the first part of the date.

                    elif untagged_information2[i] == "Pages":
                        pages = untagged_information[i]

                    elif untagged_information2[i] == "Volume" or untagged_information2[i] == "Patent number":
                        volume = untagged_information[i]

                    elif untagged_information2[i] == "Issue" or untagged_information2[i] == "Application number":
                        issue = untagged_information[i]

                    elif untagged_information2[i] == "Publisher":
                        publisher = untagged_information[i]

                    elif ((untagged_information2[i] == "Journal")or(untagged_information2[i] == "Conference")or(untagged_information2[i] == "Book")
                          or(untagged_information2[i] == "Patent office")):
                        type_of = untagged_information2[i]
                        name_of = untagged_information[i]

                if type_of == None:                                     #Outside of the for the type is checked if there is not type it will be a technical work.
                    type_of = "Technical Work"      
                
                published = Published(title=title,authors=authors,year=year,date=date,type_of = type_of,
                                          name_of=name_of,volume =volume,issue=issue,pages=pages,publisher=publisher,citation_count=count_of_citation)
                                                                        #In this part the object is created and it is added to the database and for loop goes on.
                database[self.professor_name][self.title] = published

        return self.professor_name                                      #This function will return the name of professor at the end.

    def opening_url_and_making_soup(self,url):                          #At this level url is opened by urllib2 then it is read finally it is made a soup by BS.
        request = Request(url)
        response = urlopen(request)                                     
        html_version = response.read()      
        soup = BeautifulSoup(html_version)
        return soup
            
                                                                        #This function has three parameters,first and second will come from radiobuttons and third
    def reformat(self,group_by,sort_by,prof_name):                      #one will come from combobox.
        if group_by == "Year":
            returned = self.year_part_of_grouping(prof_name)            #This returns a dictionary

            if sort_by == "Year":
                return self.year_part_of_sorting(returned)              #This returns a list
            elif sort_by == "Citation Count":
                return self.citation_part_of_sorting(returned)          #This returns a list  
            
        elif group_by == "Type":
            returned = self.type_part_of_grouping(prof_name)            #This returns a dictionary
            
            if sort_by == "Year":
                return self.year_part_of_sorting(returned)              #This returns a list
            elif sort_by == "Citation Count":
                return self.citation_part_of_sorting(returned)          #This returns a list

        else:
            if sort_by == "Year":                                       #It creates a list of tuple with elements (publishes date(list),publish as object)
                mylist = [(i.date,i) for i in database[prof_name].values()] 
                mylist.sort(reverse=True)                               #In this section it is sorted by their dates
                return mylist
            
            elif sort_by == "Citation Count":                           #It creates a list of tuple with elements (publishes citation count(int),publish as object)
                mylist = [(i.citation_count,i) for i in database[prof_name].values()]
                mylist.sort(reverse=True)                               #In this section it is sorted by their citation count
                return mylist

    def year_part_of_grouping(self,prof_name):                          #These two functions are the same
        mylist = [(i.year,i) for i in database[prof_name].values()]     #It creates a list of tuple with elements (publishes year(int),publish as object)
        
        mynewlist = dict()                                              #This dictionary is for grouping, the keys will be years(int) as group name and values will be 
        for i,j in mylist:                                              #list of the publishes(object) which is in this group. 
            if i not in mynewlist:                                      
                mynewlist[i] = list()
                mynewlist[i].append(j)
            else:
                mynewlist[i].append(j)
        return mynewlist                                                #It is a dictionary of grouping
    
    def type_part_of_grouping(self,prof_name):                          
        mylist = [(i.type_of,i) for i in database[prof_name].values()]  #It creates a list of tuple with elements (publishes type(str),publish as object)

        mynewlist = dict()                                              #This dictionary is for grouping, the keys will be types(str) as group name and values will be
        for i,j in mylist:                                              #list of the publishes(object) which is in this group.
            if i not in mynewlist:
                mynewlist[i] = list()
                mynewlist[i].append(j)
            else:
                mynewlist[i].append(j)
        return mynewlist                                                #It is a dictionary of grouping
        
                                                                        #These two functions are the same
    def year_part_of_sorting(self,returned):                            #This function takes the parameter of dictionary which is returned from grouping functions
        grouped_sorted_year = list()                                    
        for  i,j in returned.items():
            sorting_list = [(k.date,k) for k in j]                      #This list consist tuple of (publish(objects)'s date,publish(object)
            sorting_list.sort(reverse = True)                           #Then it sorts according to their date.
            last_sorting = [n1 for n,n1 in sorting_list]                #n1 = k , n = k.date
            grouped_sorted_year.append((i,last_sorting))                #This list consist tuple with (group name,list of the sorted object which were in the group.
        grouped_sorted_year.sort(reverse = True)                        #It sorts the group names:year(int),type(str)
        return grouped_sorted_year                                      #It is a list of tuple

    def citation_part_of_sorting(self,returned):                        #This function takes the parameter of dictionary which is returned from grouping functions
        grouped_sorted_cite = list() 
        for  i,j in returned.items():
            sorting_list = [(k.citation_count,k) for k in j]            #This list consist tuple of (publish(objects)'s date,publish(object)
            sorting_list.sort(reverse = True)                           #Then it sorts according to their citation count.
            last_sorting = [n1 for n,n1 in sorting_list]                #n1 = k , n = k.citation_count
            grouped_sorted_cite.append((i,last_sorting))                #This list consist tuple with (group name,list of the sorted object which were in the group.
        grouped_sorted_cite.sort(reverse = True)                        #It sorts the group names:year(int),type(str)
        return grouped_sorted_cite                                      #It is a list of tuple

                                                        
values_of_radiobuttons = {0:"Year",1:"Type",2:"None",3:"Year",4:"Citation Count"}
                                                                        #This dictionary for converting the radiobuttons in left side value to the proper names.
values_of_clustering = {0:"Hierarcial",1:"K-Means"}
                                                                        #This is also for converting the the raiobuttons value to the proper names but in right side.

#In this class we have the interface function,button's functions and 3 supporting functions,one is for showing the proper showing the results in the listbox named as
#function_for_insering_properly(),other one is for preparing the proper writing and returns a string named as supporting_func(),and the third one is for calculating
#the frequency of the words and making txt data for the clustering.

class Publication_Analyzer():
    def __init__(self):
        self.Interface()    
    
    def Command_of_Downloading_Profiles(self):
        if len(self.Entry_of_urls.get(1.0,END)) <= 10:                  #One url should had at least 10 words
            self.Error_Message_Function()
            return
        self.list_of_fetched_urls = list() 
        self.got = self.Entry_of_urls.get(1.0,END)                      #It gets the all the urls as one string
        
        self.newgot = self.got.split('\n')                              #We converted the string to the list with newline.But as we do that there will be some empty
                                                                        #elements,so these empty elements were deleted with the following for loop.
        for i in range(len(self.newgot)-1):
            if (self.newgot[i] == "") or (self.newgot[i] == " "):
                del self.newgot[i]
        del self.newgot[len(self.newgot)-1]
        self.number_of_urls = len(self.newgot)                          #It is the actual number of the people in the urls.
        
        for urls in self.newgot: 
            fetching = GoogleScholarFetcher(urls)                       #Creating object for per url
            proffessor_name = fetching.fetch()                          #Then we call the fetch() method for this object, this method will return the prof_name.
            self.list_of_fetched_urls.append((proffessor_name,"%s(downloaded)"%proffessor_name,fetching))
                                                                        #This is the list of tuple and each tuple has three elements.(name,str,object)
            self.List_of_downloading_researchers.delete(0,END)          #Every time all things in the listbox is deleted for the proper showing.
            
            for i in range(len(self.list_of_fetched_urls)):             #Its range equal to number of fetched urls.
                self.List_of_downloading_researchers.insert(END,"%d-%s"%(i+1,self.list_of_fetched_urls[i][1])) 
                self.List_of_downloading_researchers.update()           #Every time it updates the listbox with the list of fetched url,i start from 0 so i+1 is used.
            difference = self.number_of_urls - len(self.list_of_fetched_urls)
                                                                        #This difference for determening the number of unfetched urls.
            if difference >= 1:                                         #If there are more then one it insert 'processing' right after the last downloaded fetch.
                self.List_of_downloading_researchers.insert(END,"%d-Processing"%(len(self.list_of_fetched_urls)+1))
                self.List_of_downloading_researchers.update()

            for j in range(difference-1):                               #Remaining is filled with 'pending',every time diffirence-1 because 1 is used for processing.
                self.List_of_downloading_researchers.insert(END,"%d-Pending"%(len(self.list_of_fetched_urls)+j+2))
                self.List_of_downloading_researchers.update()

        self.frequency_finder_and_cluster_maker()                       #After all urls are fetched and database is created we call the function for creating .txt
                                                                        #for clustering

        values = tuple()                                                #This tuple is for updating the values of the combox with the name of the professors.
        for name,show,fetched in self.list_of_fetched_urls:
            values += name,
        self.Names_of_Researchers['values'] = values

    def frequency_finder_and_cluster_maker(self): 
        for prof_name,value in database.items():                        #This function will take the all words as lower from title and name_of of the publishs as
            for title,work in value.items():                            #objects.Then the frequency of all words for all prof_names will be calculated by nested 
                if work.title != None:                                  #dictionary.
                    words_in_title = work.title.split(' ')
                else:
                    continue
                self.support_function_for_clustering(words_in_title,prof_name)
                
                if work.name_of != None:
                    words_in_name_of = work.name_of.split(' ')
                else:
                    continue
                self.support_function_for_clustering(words_in_name_of,prof_name)

        will_be_clustered = file('Will_be_Cluestered.txt','w')          #The .txt is created similar to the blogdata.txt.In this .txt columns will be words and rows 
        will_be_clustered.write('Professors')                           #will be frequencies.
        
        profs_names = database.keys() 
        all_words = wordcounts.keys()
        for word in all_words:
             will_be_clustered.write('\t%s'%word)
        will_be_clustered.write('\n')
        
        for profs in profs_names:
            will_be_clustered.write(profs)
            for word in all_words:
                if profs in wordcounts[word].keys():
                    will_be_clustered.write('\t%d'%wordcounts[word][profs])
                else:
                    will_be_clustered.write('\t0')
            will_be_clustered.write('\n')

    def support_function_for_clustering(self,t,p_name):
        for i in t:
                if re_alphebetic_with_two_words.match(i) != None:       #First looking the words like a-b
                    real_word = re_alphebetic_with_two_words.match(i).group().lower()
                else:                                                   #if the is not in this form,looking the single words.
                    if re_alphebetic.match(i) != None:
                        real_word = re_alphebetic.match(i).group(1).lower()
                    else:
                        continue       
                if real_word in forbided_words:                         #Making nested dictionary,keys of outer dictionary will be words,values will be dictionary,
                    continue                                            #Keys of the inner dictionary,professor names and the values of the inner dictionary will be
                if real_word not in wordcounts:                         #frequency of word appears in this professor.
                    wordcounts[real_word] = dict()
                    wordcounts[real_word][p_name] = 1          
                else:
                    if p_name not in wordcounts[real_word]:
                        wordcounts[real_word][p_name] = 1
                    else:
                        wordcounts[real_word][p_name] += 1

    def viewing_lists(self):
        if len(database) == 0:
            self.Error_Message_Function()
            return

        elif len(self.Names_of_Researchers.get()) == 0:
            self.Error_Message_Function2()
            return
        self.All_Results_Part.delete(0,END)                             #Deleting the things on listbox
        prof_name = self.Combo_Values.get()                             #Prof name come from combobox
        
        for name,show,fetching in self.list_of_fetched_urls:            #We use the list is created in the first command with tuples(name,string,object)
            if name == prof_name:                                       #We will use the object to utilize the reformat function of the object.
                grouping_type = values_of_radiobuttons[self.Radio_Values1.get()]
                                                                        #Finding the proper value from the dictionary with using the radiobutton as key
                sorting_type = values_of_radiobuttons[self.Radio_Values2.get()]
                                                                        #Same with above
                if grouping_type == "None":
                    list_for_view = fetching.reformat(grouping_type,sorting_type,prof_name)
                                                                        #Reformat function always return a list, in None frouping list of tuples with(date,object)
                    counter = 1                                         #This counter is for writing the number of the publish properly to the listbox
                    for i,obje in list_for_view:                        
                        self.function_for_inserting_properly(counter,obje,100.0)
                                                                        #This function insert to the listbox
                        counter += 1
                else:
                    list_for_view = fetching.reformat(grouping_type,sorting_type,prof_name)
                                                                        #This is also list of tuples with elements (groupname(int or str),list of objects)
                    for group,lists in list_for_view:                   
                        self.All_Results_Part.insert(END,str(group)+":")#This ':' for attesting the grouping name
                        counter = 1                                         
                        for obje in lists:                              
                            self.function_for_inserting_properly(counter,obje,100.0)
                                                                        #Same with above one,inserting
                            counter += 1

    def function_for_inserting_properly(self,counter,obje,length):      #This function take the three parameters;one counter(it will chage with iteration at above) 
        x = 2                                                           #other one is publish as object for inserting and the last one the length of the one line
                                                                        #This third one actually depens on the font size of listbox for proper inserting.
        lines,remaining = divmod(len(self.supporter_func(obje)),length) #Number of lines and at the last line how much shoulde be inserted.
        self.All_Results_Part.insert(END," "*2+"%d-%s"%(counter,self.supporter_func(obje)[0:int(length)]))
        for line in range(int(lines)+1):                                #These were calling function for creating str and then insert part by part this string.
            self.All_Results_Part.insert(END," "*4 + self.supporter_func(obje)[int((x-1)*length):int((x)*length)]) 
            x += 1                                                      
        self.All_Results_Part.insert(END,self.supporter_func(obje)[int((x)*length):int((x*length+int(remaining)))])

    def supporter_func(self,obje):                                      #This function takes one parameters as object and this function checks all the attributes
        showing = ""                                                    #of the object if it is not None it adds the attribute's value to the string with punctiations
        if obje.authors != None:                                        #and finally this function returns a string
            showing += obje.authors+"."
        if obje.title != None:
            showing += "%s"%(obje.title) + "."
        if obje.name_of != None:
            showing += obje.name_of + "," 
        if obje.volume != None:
            showing += "Vol.%s"%obje.volume
        if obje.issue != None:
            showing += "(%s)"%obje.issue + ","
        if obje.pages != None:
            showing += "pp.%s"%obje.pages
        if obje.date != None:
            showing += ",%d"%obje.year + "."
        if obje.citation_count != None:
            showing += "[%d]"%obje.citation_count
        return showing

    def clustering_button(self):
        if len(database) == 0:
            self.Error_Message_Function()
            return
        prof_names,words,data = clusters.readfile("Will_be_Cluestered.txt")
        type_of_clustering = values_of_clustering[int(self.Radio_Values3.get())]
                                                                        #Determining the type of clustering with the dictionary.
        if type_of_clustering == "Hierarcial":
            clust = clusters.hcluster(data)
            self.All_Results_Part.delete(0,END)
            for i in range(len(clusters.clust2str(clust,labels = prof_names).split('\n'))-1):
                                                                        #split method is used for proper showing of cluster.
                self.All_Results_Part.insert(END,clusters.clust2str(clust,labels = prof_names).split('\n')[i])                                                   
                                                                        #Last line of list will be empty string so it is neglected.
        elif type_of_clustering == "K-Means":
            clust = clusters.kcluster(data,k = int(self.Value_of_k.get()))
                                                                        #k is getting from the entry.
            prof_names = database.keys()
            new_list_with_length_of_elements = [(len(i),i) for i in clust]
            new_list_with_length_of_elements.sort(reverse=True)
            counter = 0
            self.All_Results_Part.delete(0,END)
            for i,j in new_list_with_length_of_elements:
                new_proper_list = [prof_names[k] for k in range(len(j))]
                new_str = ""
                for i in new_proper_list:
                    new_str += str(i)+"  "
                self.All_Results_Part.insert(END,"Cluster %d:{"%(counter+1)+new_str+"}"+"\n")
                counter += 1

    def Error_Message_Function(self):                                   #Message for error showing
        error_message_window = Toplevel()
        error_message = Label(error_message_window,text = """Please enter at least\n one url""",font="Times 100 bold",bg = "Red",fg = "Black")
        error_message.pack()

    def Error_Message_Function2(self):
        error_message_window = Toplevel()
        error_message = Label(error_message_window,text = """Please Choose a \nProfessor Name""",font="Times 100 bold",bg = "Red",fg = "Black")
        error_message.pack()

    def Interface(self):

        #Main window part
        self.main_window = Tk()
        self.main_window.geometry("1000x1000+100+-22")
        self.main_window.resizable(width=False,height=False)
    
        #Background part
        self.Main_Background = Label(bg="Orange")
        self.Main_Background.place(relx = 0.0,rely = 0.0,width = 1000,height = 1000)
    
        #Title of project part
        self.Main_Title = Label(text = 'Publication Analyzer v1.0',font = "Times 30 bold")
        self.Main_Title.place(relx = 0.3,rely = 0.0)
        #Quit Button
        self.Quit_Button = Button(text = "Quit",bg = "Red",command = self.main_window.destroy)
        self.Quit_Button.place(relx = 0.97,rely = 0.0)
    
        #Top-Left part of project
        self.Title_of_urls_part = Label(text = 'Please enter Google Scholar profile URLs(one URL per line:)',font= "Times 15")
        self.Title_of_urls_part.place(relx = 0.05 ,rely = 0.08)
        self.Entry_of_urls = Text(font = "Times 7")
        self.Entry_of_urls.place(relx = 0.05 ,rely =0.13,height = 150,width=500)
    
        #Top-Right part of project
        self.Button_of_downloading_profiles = Button(text = 'Download Publication Profiles',font = "Times 15",command =  self.Command_of_Downloading_Profiles)
        self.Button_of_downloading_profiles.place(relx = 0.65,rely = 0.08)
        self.List_of_downloading_researchers = Listbox(font = "Times 12")
        self.List_of_downloading_researchers.place(relx = 0.65,rely=0.13,height = 150,width = 250)

        #Listing publication part(Middle-Left part)
        self.Title_of_listing_publications = Label(text='View Publication for a Researcher',font ="Times 15")
        self.Title_of_listing_publications.place(relx = 0.05,rely =0.29)
        self.Background_of_publication_list_part = Label(bg = "Light Blue")
        self.Background_of_publication_list_part.place(relx =0.05 ,rely = 0.318,width = 500,height=200)
        self.Name_of_Combobox = Label(text = """Choose a\n   Researcher:""",bg = "Light Blue",font = "Times 10 bold")
        self.Name_of_Combobox.place(relx = 0.05,rely=0.33,width=75,height = 50)
        self.Combo_Values = StringVar()
        self.Names_of_Researchers = ttk.Combobox(textvariable = self.Combo_Values,state="readonly")
        self.Names_of_Researchers.place(relx = 0.150,rely = 0.34,width = 150)
        #Radio Button(Grouping) part of Middle-Left part
        self.Name_of_Radio_Button1 = Label(text = "Group by:",bg = "Light Blue",font = "Times 10 bold")
        self.Name_of_Radio_Button1.place(relx = 0.35,rely=0.33,width=75,height = 50)
        self.Radio_Values1 = IntVar()
        self.Types_of_Grouping1 = Radiobutton(text = "Year",variable = self.Radio_Values1,bg = "Light Blue",value = 0)
        self.Types_of_Grouping1.place(relx = 0.43 ,rely = 0.320)
        self.Types_of_Grouping2 = Radiobutton(text = "Type",variable = self.Radio_Values1,bg = "Light Blue",value = 1)
        self.Types_of_Grouping2.place(relx = 0.43 ,rely = 0.345)
        self.Types_of_Grouping3 = Radiobutton(text = "None",variable = self.Radio_Values1,bg = "Light Blue",value = 2)
        self.Types_of_Grouping3.place(relx = 0.43 ,rely = 0.370)
        self.Radio_Values1.set(0)
        #Radio Button(Sorting) part of Middle-Left part
        self.Name_of_Radio_Button2 = Label(text = "Sort by:",bg = "Light Blue",font = "Times 10 bold")
        self.Name_of_Radio_Button2.place(relx = 0.35,rely=0.41,width=75,height = 50)
        self.Radio_Values2 = IntVar()
        self.Types_of_Sorting1 = Radiobutton(text = "Year",variable = self.Radio_Values2,bg = "Light Blue",value = 3)
        self.Types_of_Sorting1.place(relx = 0.43 ,rely = 0.410)
        self.Types_of_Sorting1 = Radiobutton(text = "Citation Count",variable = self.Radio_Values2,bg = "Light Blue",value = 4)
        self.Types_of_Sorting1.place(relx = 0.43 ,rely = 0.435)
        self.Radio_Values2.set(3)
        #Button of listing publications
        self.Button_of_Listing_Publications = Button(text = 'List Publications',font = "Times 13",command = self.viewing_lists)
        self.Button_of_Listing_Publications.place(relx = 0.38 ,rely = 0.47)

        #Clustering publications part(Middle-Right part)
        self.Title_of_viewing_clusterings = Label(text='Cluster Resarchers',font ="Times 15")
        self.Title_of_viewing_clusterings.place(relx = 0.65,rely =0.29)
        self.Background_of_vieving_clustrings_part = Label(bg = "Light Blue")
        self.Background_of_vieving_clustrings_part.place(relx =0.65 ,rely = 0.318,width = 250,height=200)
        #Radio Button(Clustering) part of Middle-Right part
        self.Name_of_Radio_Button3 = Label(text = "Clustering Method:",bg = "Light Blue",font = "Times 10 bold")
        self.Name_of_Radio_Button3.place(relx = 0.65,rely=0.32,width=125,height = 50)
        self.Radio_Values3 = IntVar()
        self.Types_of_Clustring1 = Radiobutton(text = "Hiearacial",variable = self.Radio_Values3,bg = "Light Blue",value = 0)
        self.Types_of_Clustring1.place(relx = 0.68 ,rely = 0.36)
        self.Types_of_Clustring2 = Radiobutton(text = "K-Means",variable = self.Radio_Values3,bg = "Light Blue",value = 1)
        self.Types_of_Clustring2.place(relx = 0.68 ,rely = 0.385)
        self.Radio_Values3.set(0)
        #Value of k part
        self.Name_of_k = Label(text = "k:",font = "Times 10 bold",bg = "Light Blue")
        self.Name_of_k.place(relx = 0.8,rely= 0.385)
        self.Value_of_k = Entry()
        self.Value_of_k.place(relx = 0.82,rely = 0.385,width = 50)
        self.Value_of_k.insert(END,5)
        #Button for clustering
        self.Button_of_Listing_Publications = Button(text = 'View Clusters',font = "Times 13",command = self.clustering_button)
        self.Button_of_Listing_Publications.place(relx = 0.77 ,rely = 0.47)

        #Button part of the project
        self.All_Results_Part = Listbox(font = "Bold 12")
        self.All_Results_Part.place(relx = 0.05,rely = 0.530,width = 850,height = 200)
        self.scroll = Scrollbar(self.All_Results_Part)
        self.scroll.pack(side=RIGHT,fill=Y)
        self.scroll.config(command = self.All_Results_Part.yview)
        
        mainloop()
       
App = Publication_Analyzer()
    
