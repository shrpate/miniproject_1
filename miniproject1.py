import sqlite3, time, random

connection = sqlite3.connect('miniproject1.db') #DB name
c = connection.cursor()
loggedIn = False #by default, the user will not be logged in

def register(email, name, phone, pwd): #registers the user
    c.execute ("INSERT INTO members VALUES (:email, :name, :phone, :pwd)", {'email': email, 'name': name, 'phone': phone, 'pwd': pwd})
    
def askDupEmail(email): #checks of the email already exists in the DB

    dupEmail = False #assumption is there email is unique
    c.execute("SELECT m.email FROM members m")
    emailList = c.fetchall()
    for items in emailList:
        if dupEmail == True: #the email is duplicate
            break
        for elements in (list(items)):
            if elements == email:
                print('This email already exist. Please try a different Email.')
                dupEmail = True #Throw an Error if this is True (it is Flase by default)
                break
    return dupEmail #return to see it its true or false
    
def registering():    
    mainInput = str(input("To register, type 1\nTo go back to main screen, type 2\nTo exit, type 0: "))
    if mainInput == '1':
        valEmail = False #The input is assumned to be invalid
        
        while not valEmail: #keep looping until the valid input is received.
            email = str(input("Enter your E-mail: "))
            if email == '0':
                loginScreen() #take the user to the login screen
            
            if askDupEmail(email) == False: #if there email is unique, register them.
                name = str(input("Enter your Name: "))
                phone = str(input("Enter your Phone Number: "))
                pwd = str(input("Enter your Pwd: "))
                valEmail = True
                register(email, name, phone, pwd)
                
    elif mainInput == '2':
        loginScreen()
    elif mainInput == '0':
        time.sleep(0.5)
        print('Exiting')
    
    else:
        registering() #Recall the function agian, if the user couldn't register.

def loginScreen():
    Input = input("\n\nPress 1 to login with a valid E-mail and Password.\nPress 2 to sign up today.\nPress 0 to exit this program.\t\t\t____")
    
    if Input == '1':    #if you are already a member
        login() #log them in
        
    elif Input == '2':  #if you want to sign up
        registering()      #register then with a unique email address  
        
    elif Input == '0':  # To exit
        print("Exiting...")
        time.sleep(0.5)
        print("goodBye!")
    else:
        print("Invalid input, Try Again!")
        loginScreen() # if the input in invalid, call the loginScreen function again. 
        
def printMessages(email):
    c.execute("SELECT i.content FROM inbox i, members m WHERE m.email = (:email) AND i.seen = 'n'", {'email': email})
    messages = c.fetchall()
    
    update_seen = """UPDATE inbox SET seen = 'y' WHERE seen = 'n'""" #change the staus to "y" (seen) onces they view their email.
    c.execute(update_seen)
    for item in messages:
        print(item) #print the messages for the user
    if messages == None:
        print('You have no new messages') #if no messages, print this.

def offerRide(email):
    # give rdate, seats, lugDesc, src, dst, price
    # optional: add a cno and enroute.lcode
    #   if cno is entered: query and check that the cno belongs to the member
    # for locations: take an input from the member offering a ride that can be a keyword or lcode
    # if lcode: return the locations
    #   if len(location query) >= 5: limit to 5 results, give user option to see more or select a location
    #       if see more:
    #           display all matching locations (fetchall)
    #       elif select_location:
    #           take input for the locations
    #           valid_selection = True
    # elif not lcode: return all locations that have the keyword as a substring in city, province or address fields
    #   if len(location query) >= 5: limit to 5 results, give user the option to see more or select a location
    # if a valid_selection == True (i.e. is confirmed): assign a random rno and set that offering member as the driver.
    # ride_offer =  # pass off the offering member's email

#try:
    c.execute("SELECT rides.rdate, rides.seats, rides.lugDesc, rides.src, rides.dst, rides.price FROM rides WHERE rides.driver = (?)", (email,))
    #print("here")
#except:
    #pass
    #print("some error occurred")
#else:
    optional_input = str(input("would you like to add a car number and enroute locations? (y/n): "))
    valid_selection = False
    while not valid_selection:
        if optional_input == 'y':
            check_cno = "SELECT cars.cno, cars.owner, rides.cno, rides.driver FROM cars, rides WHERE cars.cno = rides.cno AND cars.owner = :email", {"email":email}
            c.execute(check_cno)
            if check_cno: # if the query returns True get the enroute location
                enroute_input = str(input("enter a location code (lcode) or a location keyword: "))
                enroute_location = get_location(enroute_input) # query the search with this function and return it
                print(enroute_location)
                #enroute_confirmation =
                #str(input("Please select from this list: %s", enroute_location))
                # book the enroute location
                valid_selection = True
        elif optional_input == 'n':
            location_input = str(input("Enter a location code or a location keyword: "))
            location = get_location(location_input)
            print(location)
            #location_confirmation =
            #str(input("Please select from this list: %s", location))
            # book the enroute locations
            valid_selection = True
        else:
            print("Please enter a valid input")
    if valid_selection:
        rno = random.randint(1, 100000)
        #update_offer = 
        c.execute("UPDATE rides SET driver = (:email), rno = (:rno)", {"email":email, "rno": rno})
        print("driver and ride number have been updated")

def get_location(location):
   try:
       c.execute("SELECT locations.lcode FROM locations WHERE locations.lcode LIKE (:location)", {"location":location})
       attempt1 = c.fetchall()
       return attempt1
   except:
       pass
   try:
       c.execute("SELECT locations.city FROM locations WHERE locations.city LIKE (:location)", {"location":location})
       attempt2 = c.fetchall()
       return attempt2
   except:
       pass
   try:
       c.execute("SELECT locations.prov FROM locations WHERE locations.prov LIKE (:location)", {"location":location})
       attempt3 = c.fetchall()
       return attempt3
   except:
       pass
   try:
       c.execute("SELECT locations.address FROM locations WHERE locations.address LIKE (:location)", {"location":location})
       attempt4 = c.fetchall()
       return attempt4
   except:
       pass
   else:
       print("please enter a better search term: ")


def SearchRides():
    locVal = False
    while not locVal:
        locNo = input('Type a number between 1 and 3 for the number of location keywords you want to enter.\nType 0 to exit: ')
        
        def QWithLim (searchInput): #Query as a function with limit 5
            c.execute("SELECT r.rno FROM rides r, locations l, enroute e WHERE (:searchInput) == r.src or (:searchInput) == r.dst or (:searchInput) == l.lcode or (:searchInput) == e.lcode or (:searchInput) == l.city or (:searchInput) == l.prov or (:searchInput) == l.address LIMIT 5" , {'searchInput': searchInput})
        def QWithoutLim(searchInput):     #Query as a function with all options      
            c.execute("SELECT r.rno FROM rides r, locations l, enroute e WHERE (:searchInput) == r.src or (:searchInput) == r.dst or (:searchInput) == l.lcode or (:searchInput) == e.lcode or (:searchInput) == l.city or (:searchInput) == l.prov or (:searchInput) == l.address" , {'searchInput': searchInput})        
            
        if locNo == '1':
            searchInput = input('Enter the location key: ')
            QWithLim(searchInput)             #with 5 at max limit
            SearchQuery = c.fetchall()
            print(SearchQuery[0])
            op = input("To view all the rides type 'more' or press '1' to continue: ")
            if op == "more":
                QWithoutLim(searchInput)      #with no limit, views all.
                SearchQuery = c.fetchall()
                print(SearchQuery[0])                
            
        if locNo == '2':
                searchInput1 = input('Enter the location key: ')
                searchInput2 = input('Enter the location key: ')
                
                QWithLim(searchInput1)             #with 5 at max limit
                SearchQuery1 = c.fetchall()
                QWithLim(searchInput2)             #with 5 at max limit
                SearchQuery2 = c.fetchall()                
                print(SearchQuery1[0])
                print(SearchQuery2[0])
                op = input("To view all the rides type 'more' or press '1' to continue: ")
                if op == "more":
                    QWithoutLim(searchInput1)             #with no limit, views all.
                    SearchQuery1 = c.fetchall()
                    QWithoutLim(searchInput2)             #with no limit, views all.
                    SearchQuery2 = c.fetchall()                
                    print(SearchQuery1[0])
                    print(SearchQuery2[0])             
                
                
        if locNo == '3':
                searchInput1 = input('Enter the location key: ')
                searchInput2 = input('Enter the location key: ')
                searchInput3 = input('Enter the location key: ')
                
                QWithLim(searchInput1)             #with 5 at max limit
                SearchQuery1 = c.fetchall()
                QWithLim(searchInput2)             #with 5 at max limit
                SearchQuery2 = c.fetchall()
                QWithLim(searchInput3)             #with 5 at max limit
                SearchQuery3 = c.fetchall()                
                print(SearchQuery1[0])
                print(SearchQuery2[0])
                print(SearchQuery3[0])
                op = input("To view all the rides type 'more' or press '1' to continue: ")
                if op == "more":
                    QWithoutLim(searchInput1)             #with no limit, views all.
                    SearchQuery1 = c.fetchall()
                    QWithoutLim(searchInput2)             #with no limit, views all.
                    SearchQuery2 = c.fetchall()
                    QWithoutLim(searchInput3)             #with no limit, views all.
                    SearchQuery3 = c.fetchall()                     
                    print(SearchQuery1[0])
                    print(SearchQuery2[0])
                    print(SearchQuery3[0])
                
        if locNo == '0':
            print("Exiting...")
            time.sleep(0.5)
            print("goodBye!")
            locVal = True

def bookings(email):
    c.execute("SELECT * FROM bookings b WHERE b.email == (:email)", {'email': email})
    rideReq = c.fetchall() # grab all the valid bookings for the user
    if rideReq == []: # incase theu don't have any bookings in DB
        print('You have no bookings made under this Email Address.\n')
        login() # take them to the login screen again. (break)
        
    print('You currently have the following requests: ')
    for item in rideReq:
        print(item) #print all the bookings the user have in the DB.
     
    option1 = input('Do you want to cancle any? (Y/N): ')
    if option1 == 'y': #if they want to chancel a booking
        try:
            delBook = input("Enter the booking number that you want to cancel: ") #bno
            c.execute("SELECT r.driver, r.rno FROM bookings b, rides r WHERE b.rno = r.rno AND b.email = (:email)", {'email':email})
            qOutput = c.fetchall() #grab email for the driver and the ride number
            print(qOutput[0][1])
            sender = (qOutput[0][0]) #driver
            rno = (qOutput[0][1])        
            
            c.execute("DELETE FROM bookings WHERE bno = (:delBook)", {'delBook': delBook})
            print("The booking has successfully been cancled and the driver has been notified")
      
            msgTimestamp = time.strftime("%Y-%m-%d %H:%M:%S") #print the date and the time at the time of cancling the booking
    
            message = ("The member with E-mail address '%s' has cancled their booking."% email) #print a proper cancelation message to the driver
            seen = 'n'
    
            c.execute("INSERT INTO inbox VALUES (:email, :msgTimestamp, :sender, :message, :rno, :seen)", {'email': sender, 'msgTimestamp': msgTimestamp, 'sender': email, 'message': message, 'rno': rno, 'seen': seen})

        except:
            print("Error occurred, please try again.") #if something goes wrong above, raise error and break out of the function.
            
    else:
        pass

def rideRequests(email):
       
    rid = random.randint(1, 100000) #random & unique ride number for the user.
    rdate = input("Provide a date in MM/DD/YYYY form: ")
    pickup = input("Provide a Pick up Location code: ")
    dropoff = input("Provide a Drop off Location code: ")
    amount = input("Provide the amount willing to pay per seat: $")
    #create a request for the user
    try:
        c.execute("INSERT INTO requests VALUES (:rid, :email, :rdate, :pickup, :dropoff, :amount)", {'rid': rid, 'email': email, 'rdate': rdate, 'pickup': pickup, 'dropoff': dropoff, 'amount': amount})
        print("The ride request has been successfully created!")
    except:
        print("Error occured, please try again!")
        rideRequests(email)
       
def searchDelRideReq(email): # delete a ride request. #also need to send a proper message, which is yet to implement.
    c.execute("SELECT * FROM requests r WHERE r.email ==  (:email)", {'email': email})
    rideReq = c.fetchall()
    for item in rideReq:
        print(item)
        rid = rideReq[0][0]
    if rideReq == None:
        print('You have no current ride requests')
    else:
        delReq = input("Enter the ride number that you want to delete or 0 to go back to the main menu: ")
    
    if delReq == '0':
        login()
    else:
        c.execute("DELETE FROM requests WHERE rid=(:delReq)", {'delReq': delReq})
        if not (c.fetchall()):
            print("The request has successfully been deleted.")
        else:
            print("Error occurred, please try again.")
            
    searchRidReq = input("Enter a location code or a city that you want to see the listing for, or press 0 to exit: ") 
    
    if searchRidReq == '0':
        print("Exiting...")
        time.sleep(0.5)
        print("goodBye!")
        
    else:
        c.execute("SELECT r.rid, r.email, r.rdate, r.pickup, r.dropoff, r.amount FROM requests r, locations l WHERE (l.lcode = (:searchRidReq) or l.city = (:searchRidReq)) AND (r.pickup = l.lcode or r.pickup = l.city) LIMIT 5", {'searchRidReq': searchRidReq}) #will get upto 5 rides as per the user's wish. 
        for item in (c.fetchall()):
            print (item) # prints (upto 5) rides here
        
        moreOp = input("To print more option type 'more' or '1' to continue: ") #if they wish to see more then 5 rides.
        if moreOp == "more":
            c.execute("SELECT r.rid, r.email, r.rdate, r.pickup, r.dropoff, r.amount FROM requests r, locations l WHERE (l.lcode = (:searchRidReq) or l.city = (:searchRidReq)) AND (r.pickup = l.lcode or r.pickup = l.city)", {'searchRidReq': searchRidReq}) #will return ALL the rides as per the user's wish.
            for item in (c.fetchall()):
                print (item) #print ALL the rides here
        
        option1 = input("Enter the rid for the ride you want to request of press 0 to exit: ")
        
        if option1 == '0':  #TO EXIT
            print("Exiting...")
            time.sleep(0.5)
            print("goodBye!")  
        else:
            c.execute("SELECT r.email FROM requests r WHERE r.rid = (:option1)", {'option1': option1}) #gets the email of to driver to whom, the program will send the message to
            output1 = c.fetchall()
            msgTimestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            message = ("The member with E-mail address '%s' would like to check out a ride."% email) #message that the driver gets on behalf of the sender(current user)
            seen = 'n'
            
            c.execute("INSERT INTO inbox VALUES (:email, :msgTimestamp, :sender, :message, :rno, :seen)", {'email': output1[0][0], 'msgTimestamp': msgTimestamp, 'sender': email, 'message': message, 'rno': option1, 'seen': seen})
            print("Your request has been succefully completed and the driver is been notified.") #Success message, no error check as there are 0% chance or error here.

def login(): #proper login
    loginSuccess = False # login unsuccesfull by default

    email = str(input("Please enter E-mail or press 0 to go back to main screen: "))
    if email == '0':
        loginScreen() #to go back to the options 
    pwd = str(input("Please enter password: "))
    c.execute("SELECT m.email FROM members m")
    userEmail = c.fetchall()
    
    userFound = False # false by default
    for items in userEmail:
        if userFound == True: #user is found so break out of the loop
            break
        else:
            check = email in list(items)
            if check:
                userFound = True #user found fo break the loop
                
                c.execute("SELECT m.pwd FROM members m WHERE m.email = (:email)", {'email': email})
                dataPwd = c.fetchall()
                
                for item in dataPwd:
                    if (pwd == ''.join(item)):
                        print("Login Successful!")
                        loggedIn = True
                        loginSuccess = True
                        break                           
    if not userFound:
        print("Invalid Email\n") # if the user is not found
        login()
        
    if not loginSuccess: #if the user is found, but their password is incorrect
        print("Invalid Password\n")
        login()
    
    if loggedIn:
        printMessages(email) # print all their messages as outlined
        optionVal = False #unvalid option is provided by default. When true, the option provided is valid.
        while not optionVal: # if invalid, keep looping.   
            optionInput = input('\nPress 1 to Offer a ride.\nPress 2 to Search for rides.\nPress 3 to Book members or cancle bookings.\nPress 4 to Post ride requests.\nPress 5 to Search and delete ride requests.\nPress 0 to exit.\n')
            
            if optionInput == '1':
                offerRide(email) #offer a ride. Spec 1
                optionVal = True
                
            elif optionInput == '2':
                SearchRides() # search for a ride, Spec 2
                optionVal = True
                
            elif optionInput == '3':
                bookings(email) #book or cancel, spec 3
                optionVal = True
                
            elif optionInput == '4':
                rideRequests(email) # input a valid request for a ride, SPec 4
                optionVal = True
                
            elif optionInput == '5':
                searchDelRideReq(email) # search and delete the ride, SPec 5
                optionVal = True
                
            elif optionInput == '0':  # To exit 
                optionVal = True
                print("Exiting...")
                time.sleep(0.5)
                print("goodBye!")
           #in all these cases the option input is valid, so the loop won't be repeated.  
            
def main():
    loginScreen() #take them to the loggin screen and find your way from their based on what operations you want to perform.
    connection.commit()
    connection.close()
    
main()
