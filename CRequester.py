#-*- coding: utf-8 -*-
import pymysql
import datetime
import random

class CRequester: 						 
    

    #################### Pomocnicza Metoda sluzaca okreslenie ID Loginu uzytkownika w celu ograniczenia operacji tylko na swoich zgloszeniach  ###########################      
    
    def ID_login_req(self):
        self.sql15 ="SELECT * FROM requester left join logins on requester.ID_Login_req=logins.ID_L where logins.login=%s"
        self.cursor.execute(self.sql15,(self.login))  
        self.results = self.cursor.fetchall()   					 
        
        for row in self.results:
            self.ID_log_req = row[0]
        
        #print("Wyciagniety ID LOG: "+str(self.ID_log_req))  
     
     
    ################ Glowne Menu uzytkownika #######################    
    def requester(self):
        self.i = input('Co chcesz zrobić: \n 1.-Dodaj zgłoszenie \n 2. Podejrzj zgłoszenie \n 3. Otwrzo ponownie zgłoszenie \n(Q)-wyjście \n Wybor: ')
        if(self.i == '1'):
            #print("Dodaje zgłoszenie")
            self.ID_login_req()
            self.list_of_repairers()
            self.AddReports()
            self.requester()
        elif(self.i == '2'):
            #print("Wyswietlam zgłoszenie")
            self.ShowReportsReq()
            self.requester()
        elif(self.i=='3'):
            #print("Otwieram zgłoszenie")
            self.ID_login_req()
            self.OpenReport()
            self.requester()
        elif((self.i == 'q') or (self.i == 'Q')):
            print("Koniec")
        else:
            print("Podano zły znak proszę wybrać (1,2,3,Q)")
            self.requester()
     
     
    ############### Metoda ktora pozwala ponownie otworzyc zgloszenie ######################        
    def OpenReport(self):
        self.ShowReportsReq()
        self.ID = input("Podaj ID Zgłoszenia do Otwarcia: ")
        self.secOpenRep()
        if(self.ID is ''):
            print("\n")
            print("Podano nieprawidlowy parametr dozwolone "+str(self.TabSecdel))
            print("\n")
            self.OpenReport()         
        elif(((self.ID) in str(self.TabSecdel))==True):
            self.status_z = input("Zmien Status na (2 - W realizacji )")
            if(self.status_z=="2"):
                self.sql11 = "UPDATE reports SET Status=%s WHERE (ID_Z=%s and requester=%s)"
                self.cursor.execute(self.sql11,(self.status_z,self.ID,self.ID_log_req))
                self.conn.commit()
                print("Status zmieniono pomyślnie")
            else:
                print("\n")
                print("Podano zły parametr dozwolony tylko 2 - W realizacji")
                print("\n")
                self.OpenReport()
        else:
            print("\n")
            print("Podałes nieprawidlowy numer dozwolone"+str(self.TabSecdel))
            print("\n")
            self.OpenReport()
    ############### Metoda która wyciaga ID loginu uzytkownika pomaga zabezpieczyc otwieranei nieswojego zgloszenia #########        
    def secOpenRep(self):
        self.TabSecdel = []
        self.sqlsecOR="SELECT * from reports WHERE requester=%s"
        self.cursor.execute(self.sqlsecOR,(self.ID_log_req))
        self.results=self.cursor.fetchall()
        for row in self.results:
            self.TabSecdel.append(row[0])        
            
        print(str(self.TabSecdel))
    ################ Metoda ktora losuje serwisanta do zgloszenia #######################      
    def list_of_repairers(self):
        self.Lista=[]
        self.sql = "SELECT * FROM list_of_repairers"   						 
        self.cursor.execute(self.sql)   						 
        self.results = self.cursor.fetchall()   					 
        #print ("%1s" % ("Logins") )
        for row in self.results:
            self.Login1 = row[0]
            self.Lista.append(self.Login1)    
        #print(self.Lista)
        
    ############################## Metoda ktora dodaje nowe zgloszenie ###################
    def AddReports(self):
        self.title = input("Podaj tytul Zgłoszenia: ")
        self.descr = input("Podaj opis zgłoszenia: ")
        self.logrep = random.choice(self.Lista)
        #print(self.logrep)
        self.data=datetime.date.today()
        #print(self.data)
        self.prior = input("Podaj Priorytet: ")
        if(self.prior=="1" or self.prior=="2" or self.prior=="3" or self.prior=="4"):
            self.sql5 = "INSERT INTO reports (Title, description,Requester,Repairer,Data_R,priority) VALUES (%s,%s,%s,%s,%s,%s)"
            self.cursor.execute(self.sql5,(self.title,self.descr,self.ID_log_req,self.logrep,self.data,self.prior))
            self.conn.commit()
        else:
            print("\n")
            print("Podano zły parametr dozwolone 1,2,3,4")
            print("\n")
            self.AddReports()
               
    ########################### Metoda ktora pokazje zgloszenia tylko zalogowanego serwisanta ##################################    
    def ShowReportsReq(self):   
        
        self.sql6 = "SELECT ID_Z,Title,description,priority_p,E_mail_rep,E_mail_req,Status_s,Data_R FROM view_request_how_requester WHERE Login=%s"   						 
        self.cursor.execute(self.sql6,(self.login))
        self.results = self.cursor.fetchall() 					 
        print ("%5s%40s%40s%15s%25s%25s%15s%15s" % ("ID","Title","Description","Priorytet","E_mail_rep","E-mail_req","Status","Data"))
        for row in self.results:
            self.lp = row[0]
            self.Title = row[1]
            self.description = row[2]
            self.priority = row[3]
            self.repairerr = row[4]
            self.requesterr = row[5]
            self.Status = row[6]
            self.Data_R = row[7]
            print ("%5s%40s%40s%15s%25s%25s%15s%15s" % (self.lp, self.Title, self.description,self.priority,self.repairerr,self.requesterr,self.Status,self.Data_R,))