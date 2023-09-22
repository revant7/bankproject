import pymysql,time
import random,string,time,csv,os
from datetime import datetime,date,timedelta

print("-"*40,"Welcome To ABCBank","-"*40)

c = pymysql.connect(user="root",host="localhost", password="root",database="abcbank")
cur = c.cursor()

def Main_Menu(): 
    print("\nEnter: ")
    print("\t1: To Create New Account")
    print("\t2: To Login To Existing Account")
    print("\t3: For Permanent Closure of Account")
    print("\t4: For Opening or Closing of Fixed Deposit")
    print("\t9: To Exit\n")

def custid():
    res1 = "".join(random.choices(string.ascii_uppercase,k=4))
    res2 = "".join(random.choices(string.digits,k=4))
    res = res1 + res2
    return res

def accno():
    no = "".join(random.choices(string.digits,k=6))
    no = "1210000085" + no
    no = int(no)
    return no

def transid():
    no = "".join(random.choices(string.digits,k=12))
    return no

def tridchk():
    cur.execute("""select Transaction_ID from trans""")
    transids = cur.fetchall()
    trans_id = transid()
    while trans_id in transids[0]:
        trans_id = transid()
    return trans_id

while True:
    Main_Menu()
    choice = int(input("\nEnter Your Choice:- "))
    #Choice 1

    if choice == 1:
        try:
            name = input("Enter Your Name:- ")
            gen = input("Gender [M / F] :- ")
            typ = input("""Enter Type of Account You want to open [SAVINGS / CURRENT] :- """)
            pin = int(input("Set Your Pin [4 Digit] :- "))
            pinc=int(input("Confirm Your Pin :- "))
            cust_id = custid()
            acc_no = accno()

            while pin != pinc:
                print("\nPin Does Not Match!")
                pin = int(input("Set Your Pin:- "))
                pinc=int(input("Confirm Your Pin:- "))
                print()

            cur.execute("select Customer_ID from cd")
            ids = cur.fetchall()
            for i in ids:
                while cust_id in i:
                    cust_id = custid()

            cur.execute("select Account_Number from cd")
            accnos = cur.fetchall()
            for i in accnos:
                while acc_no in i:
                    acc_no = accnos()

            cur.execute(f"""insert into cd values('{cust_id}','{name}','{gen}',
                            {acc_no},'{typ}',{pin},{0})""")
            c.commit()
            print("\nAccount Created Successfully")
            cur.execute(f"select * from cd where Customer_ID='{cust_id}'")
            print("""\nPlease Note Your Account Details Carefully And
                      Don't Share It With Anyone.""")
            print("\n","*"*60,"\n")
            d=cur.fetchall()
            for i in d:
                print("Customer ID:-" ,i[0])
                print("Account Name:-" ,i[1])
                print("Gender:-" ,i[2])
                print("Account Number:-" ,i[3])
                print("Account Type" ,i[4])
                print("Balance:-" ,i[6])
                print("\n","*"*60,"\n")

        except Exception as e:
            print(e)
            print("\nTry Again!")
            continue

    #Choice 2

    elif choice == 2:
        cid = input("\nEnter Your Customer ID :- ")
        pinn = int(input("Enter Your Pin :- "))
        cur.execute(f"""select * from cd where Customer_ID = '{cid}'
and Pin = {pinn}""")
        data = cur.fetchall()
        if len(data) == 0:
            print("\nInvalid Customer ID or Pin!")
            continue
        print(f"\nWelcome {data[0][1]},\n")
        print("Enter:- ")
        print("\t1 To Add Money")
        print("\t2 For Online Money Transfer")
        print("\t3 To Display Transaction History")
        print("\t4 To Download Transaction History")
        print("\t5 To Withdraw Money")
        print("\t6 To View Your Account Details")
        print("\t9 To Go back to main menu")

        while True:
            ch = int(input("\nEnter Your Choice:- "))
            
            #option 1 in choice 2
            try:
                if ch == 1:
                    mon = float(input("Enter Amount To Add In Account:- "))
                    cur.execute(f"""update cd set Balance = Balance +
                                {mon} where Customer_ID = '{cid}'""")
                    
                    cur.execute(f"""insert into trans values ('{cid}','{tridchk()}',
                                '{str(datetime.now())}',{mon},'CREDIT')""")
                    
                    print("\nAmount Added Successfully.")
                    
                    cur.execute(f"select Balance from cd where Customer_ID = '{cid}'")
                    print(f"\nUpdated Balance = {cur.fetchall()[0][0]}")
                    c.commit()
                    continue

               #option 2 in choice 2

                elif ch == 2:
                    acc2 = int(input("\nEnter Payee Account Number:- "))
                    amt2 = float(input("Enter Amount To Be Transferred:- "))
                    pin2 = int(input("Enter Your Account Pin To ConfirmTransaction:- "))
                    
                    cur.execute(f"""select * from cd where
    Customer_ID = '{cid}' and Pin = {pin2}""")
                    
                    dat = cur.fetchall()
                    if len(dat) != 0:
                        cur.execute("select Account_Number from cd")
                        dat2 = cur.fetchall()
                        list_accno = []
                        for i in dat2:
                            for j in i:
                                list_accno.append(j)
                        while acc2 not in list_accno:
                            print("\nAccount with this Account Number Does Not Exists.")
                            print("Enter Again. or enter 0 to Cancel Transaction")
                            acc2 = int(input("\nEnter Payee Account Number:- "))
                            if acc2 == 0:
                                break
                        cur.execute(f"select Balance from cd where Customer_ID = '{cid}'")
                        dat4 = cur.fetchall()
                        while amt2 > dat4[0][0]:
                            print("\nLow Balance In Your Account.")
                            print("Enter Amount Again or enter 0 to Cancel Transaction.")
                            amt2 = float(input("\nEnter Amount To Be Transferred:- "))
                            if amt2 == 0:
                                break
                        
                        cur.execute(f"""update cd set Balance = Balance +
    {amt2} where Account_Number={acc2}""")
                        
                        cur.execute(f"""update cd set Balance = Balance -
    {amt2} where Customer_ID='{cid}'""")
                        
                        cur.execute(f"""insert into trans values ('{cid}','{tridchk()}',
    '{str(datetime.now())}',{amt2},'DEBIT')""")
                        
                        cur.execute(f"""select Customer_ID from cd where
    Account_Number={acc2};""")
                        dat6 = cur.fetchall()[0][0]
                        cur.execute(f"""insert into trans values ('{dat6}','{tridchk()}',
    '{str(datetime.now())}',{amt2},'CREDIT')""")
                        cur.execute(f"""update cd set Balance =
    Balance + {amt2/100} where Customer_ID='{cid}'""")
    
                        time.sleep(1)
                        
                        cur.execute(f"""insert into trans values ('{cid}','{tridchk()}',
    '{str(datetime.now())}',{amt2/100},'CREDIT')""")
                        
                        c.commit()
                        print("\n")
                        print(f"Your Online Transaction Is Successfull.")
                        print(f"Amount: {amt2} is Transferred To Account Number: {acc2}")
                        print(f"Yay! You have won a cashback of Rupees {amt2/100}\n")

                #option 3 in choice 2    
                elif ch==3:
                    cur.execute(f"""select * from trans where Customer_ID = '{cid}'
    order by TimeStamp asc""")
                    th = cur.fetchall()
                    print("\n","*"*60,"\n")
                    print("Transaction ID",end="\t\t")
                    print("Date",end="\t\t")
                    print("Time",end="\t\t")
                    print("Amount",end="\t\t")
                    print("Transaction Type")
                    for i in th:
                        print(i[1],end="\t\t")
                        print(datetime.strftime(i[2],"%d-%m-%Y"),end="\t")
                        print(str(i[2].time()),end="\t\t")
                        print(i[3],end="\t\t")
                        print(i[4],end="\t\t")
                        print()
                    print("\n","*"*60,"\n")
                    
                #option 4 in choice 2
                elif ch==4:
                    with open("Transaction_History.txt","w") as f:
                        hd = ["S. No.","Transaction ID","Date","Time","Amount",
                              "Transaction Type"]
                        for i in hd:
                            f.write(f"{i}\t\t")
                        cur.execute(f"""select * from trans where
    Customer_ID = '{cid}' order by TimeStamp asc""")
                        th1 = cur.fetchall()
                        j = 0
                        for i in th1:
                            j = j + 1
                            f.write(f"\n{j}\t\t")
                            f.write(f"{i[1]}\t\t")
                            f.write(f"{datetime.strftime(i[2],'%d-%m-%Y')}\t")
                            f.write(f"{str(i[2].time())}\t\t")
                            f.write(f"{str(i[3])}\t\t")
                            f.write(f"{i[4].strip()}\n")
                        print("File Downloaded Successfully.")
                        print("File Name:- ",f.name)
                        print("File Location:- ",os.getcwd())

                #option 5 in choice 2

                elif ch==5:
                    mon1 = float(input("Enter Amount To Be Withdrawn From Account:- "))
                    cur.execute(f"update cd set Balance = Balance - {mon1} where Customer_ID = '{cid}'")
                    
                    cur.execute(f"""insert into trans values
    ('{cid}','{tridchk()}','{str(datetime.now())}',{mon1},'DEBIT')""")
                    
                    print("""Amount Withdrawn Successfully.""")
                    cur.execute(f"select Balance from cd where Customer_ID = '{cid}'")
                    print(f"Updated Balance = {cur.fetchall()[0][0]}")
                    c.commit()

                #option 6 in choice 2
                elif ch==6:
                    cur.execute(f"select * from cd where Customer_ID='{cid}'")
                    print("\nPlease Note Your Account Details Carefully And Don't Share It With Anyone.\n")
                    print("\n","*"*60,"\n")

                    d10=cur.fetchall()
                    for i in d10:
                        print("Customer ID:-" ,i[0])
                        print("Account Name:-" ,i[1])
                        print("Gender:-" ,i[2])
                        print("Account Number:-" ,i[3])
                        print("Account Type" ,i[4])
                        print("Balance:-" ,i[6])
                    print("\n","*"*60,"\n")

                elif ch==9:
                    break
            except Exception as e:
                print(e)
                print("\nTry Again\n")
                continue

            else:
                while ch not in [1,2,3,4,5,6,9]:
                    print("Invalid Input! Enter Again.")
                    ch = int(input("Enter Your Choice:- "))

    #choice 3                       
    elif choice == 3:
        name = input("Enter Your Name:- ")
        cuid = input("Enter Your Customer ID:- ")
        acno = int(input("Enter Your Account Number:- "))
        pinnc = int(input("Enter Your Pin:- "))
        cur.execute(f"""select * from cd where Customer_ID = '{cuid}' and
Account_Number = {acno} and Name = '{name}' and Pin = {pinnc}""")
        data10 = cur.fetchall()
        if len(data10) != 0:
            cur.execute(f"""delete from cd where Customer_ID = '{cuid}' and
Account_Number = {acno} and Name = '{name}' and Pin = {pinnc}""")
            c.commit()
            print("Your Account Is Permanently Closed.")
        else:
            print("Wrong Entry. Try Again.")
    #choice 4
    elif choice == 4:

        c_id = input("Enter Your Customer ID:- ")
        pin1 = int(input("Enter Your Pin:- "))
        cur.execute(f"""select * from cd where
Customer_ID = '{c_id}' and Pin = {pin1}""")
        data2 = cur.fetchall()

        if len(data2) != 0:

            ap = """Enter    1 To Open Fixed Deposit
    2 To Close Fixed Deposit
    9 To Go back to main menu
    """
            print("\n","*"*60,"\n")
            print("\t\tTime Period",end="\t\t")
            print("Rate Of Interest",end="\n\t\t")
            print("Less Than 6 Months",end="\t\t")
            print("4.25%",end="\n\t\t")
            print("6 Months To 1 Year",end="\t\t")
            print("5%",end="\n\t\t")
            print("1 Year To Less Than 2 Years",end="\t\t")
            print("6.4%",end="\n\t\t")
            print("2 Years",end="\t\t\t\t")
            print("7%",end="\n\t\t")
            print("More Than 2 Years Upto 5 Years",end="\t")
            print("6.6%",end="\n\t\t")
            print("\n","*"*60,"\n")
            print(ap)

            uch = int(input("Enter Your Choice :- "))

            if uch == 1:
                pamt = float(input("Enter Principal Amount:- "))
                tmp = int(input("Enter Time Period [in no. of days] :- "))
                cur.execute(f"select Balance from cd where Customer_ID = '{c_id}'")
                dataf = cur.fetchall()
                while pamt>dataf[0][0]:
                    print("Insufficient Balance! Press 0 to Exit or modify Principal amount.")
                    pamt = float(input("Enter Principal Amount or 0 to Exit :- "))
                    if pamt == 0:
                        break
                while tmp > 1830:
                    print("Time Period is Greater than expected value. Enter Again or 0 to exit.")
                    tmp = int(input("Enter Time Period [in no. of days] :- "))
                    if tmp == 0:
                        break
                    break
                if tmp<180:
                    roi = 4.25
                elif 180<=tmp<=365:
                    roi = 5
                elif 365<tmp<730:
                    roi = 6.4
                elif tmp == 730:
                    roi = 7
                else:
                    roi = 6.6
                dtoday=str(date.today())
                fdno = "".join(random.choices(string.digits,k=8))
                mamt = (((roi/100)*pamt)/365) * tmp + pamt
                fdate = datetime.strptime(dtoday, "%Y-%m-%d") + timedelta(days=tmp)
                qf = f"""insert into fds values
('{c_id}','{fdno}','{dtoday}',{pamt},'{tmp}','{fdate}',{roi},{mamt})"""    
                cur.execute(qf)
                cur.execute(f"""update cd set Balance =
Balance - {pamt} where Customer_ID = '{c_id}'""")
                
                cur.execute(f"""insert into trans values
('{c_id}','{tridchk()}','{str(datetime.now())}',{pamt},'DEBIT')""")
                c.commit()
                cur.execute(f"select * from fds where Customer_ID='{c_id}'")
                tp9 = cur.fetchall()[0]
                print("\nFD has been created successfully.\n")
                print("FD Number",tp9[1])

            elif uch == 2:
                print("FD's Associated With Given Customer ID are Below:- ")
                cur.execute(f"select * from fds where Customer_ID='{c_id}'")
                rec2 = cur.fetchall()
                for i in rec2:
                    print(i,"\n")
                uin2 = int(input("Enter FD Number of the FD to be Closed:- "))
                fpin2 = int(input("Enter Your Pin To Continue:- "))
                cur.execute(f"""select * from cd where Customer_ID='{c_id}' and
                            Pin={fpin2}""")
                fdata2 = cur.fetchall()
                if len(fdata2) != 0:
                    cur.execute(f"select * from fds where FD_Number={uin2}")
                    fdata9 = cur.fetchall()
                    dtoday1=str(date.today())
                    fdate1 = datetime.strptime(dtoday1, "%Y-%m-%d") - datetime.strptime(str(fdata9[0][2]),"%Y-%m-%d")
                    fdamt1 = (((fdata9[0][6]/100)*fdata9[0][3])/365) * fdate1.days + fdata9[0][3]
                    cur.execute(f"""update cd set Balance=Balance+{fdamt1}
where Customer_ID='{c_id}'""")
                    
                    cur.execute(f"insert into trans values ('{c_id}','{tridchk()}','{str(datetime.now())}',{fdamt1},'CREDIT')")
                    cur.execute(f"delete from fds where FD_Number={uin2}")
                    c.commit()
                    print(f"\nFD with FD number {uin2} has been successfully closed.")
                    print(f"The maturity amount of Rupees {fdamt1} has been successfully added to your account.\n")         
            elif uch == 9:
                break
            else:
                print("Invalid Input! Try Again.")
                uch = int(input("Enter Your Choice :- "))
    elif choice == 9:
        print("Thank You. Visit Again.")
        break
    else:
        while choice not in [1,2,3,4,9]:
            print("Invalid Input! Enter Again.")
            choice = int(input("Enter Your Choice:- "))
print("Thank You! Please Visit Again")            
                
                
                    

                    











































                
        
        
    
    
    
    














