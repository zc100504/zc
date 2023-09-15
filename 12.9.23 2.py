from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3
import bcrypt
from tkinter import ttk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime


root = Tk()
root.title('Login')
root.geometry('925x475+300+200')
root.configure(bg='#D3D3D3')
root.resizable(False, False)

def create_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data(
        id INTEGER PRIMARY KEY,
        subject_name TEXT,
        subject_code TEXT,
        credit_hour INTEGER,
        class_type TEXT,
        lecture_name TEXT,
        classes TEXT,
        capacity INTEGER,
        class_day TEXT,
        class_time TEXT,
        venue TEXT)''')
    conn.commit()
    conn.close()

def fetch_subjects():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM data')
    subject = cursor.fetchall()
    conn.close()
    return subject

def insert_subject(id, subject_name, subject_code, credit_hour, class_type, lecture_name, classes, capacity, class_day, class_time, venue):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO data(id, subject_name, subject_code, credit_hour, class_type, lecture_name, classes, capacity, class_day, class_time, venue) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                    (id, subject_name, subject_code, credit_hour, class_type, lecture_name, classes, capacity, class_day, class_time, venue))
    conn.commit()
    conn.close()

def delete_subject(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM data WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def update_subject(new_subject_name, new_subject_code, new_credit_hour, new_class_type, new_lecture_name, new_classes, new_capacity, new_class_day, new_class_time, new_venue, id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE data SET subject_name = ?, subject_code = ?, credit_hour = ?, class_type = ?, lecture_name = ?, classes = ?, capacity = ?, class_day = ?, class_time = ?, venue = ? WHERE id = ?",
                (new_subject_name, new_subject_code, new_credit_hour, new_class_type, new_lecture_name, new_classes, new_capacity, new_class_day, new_class_time, new_venue, id))
    conn.commit()
    conn.close()

def id_exists(id):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) from data WHERE id = ?', (id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

    create_table()

def clear_userid_entry():
    userid_entry2.delete(0, 'end')

def clear_password_entry():
    password_entry2.delete(0, 'end')

def logout_and_show_login(current_window):
    clear_userid_entry()  # Clear User ID entry
    clear_password_entry()  # Clear Password entry
    current_window.destroy()  # Close the current window
    root.deiconify()  # Show the login window again

def login():
    global userid
    userid = userid_entry2.get()
    password = password_entry2.get()

    if userid == 'admin' and password == '1234':
        # Admin login logic
        root.withdraw()  # Hide the original login window
        root1 = Toplevel(root)
        root1.title('Admin main page')
        root1.geometry('925x475+300+200')
        root1.config(bg='#CCCCCC')

        myLabel = Label(root1, text="WELCOME BACK ADMIN", bg='#CCCCCC', font=('Microsoft YaHei UI Light', 22, 'bold'))
        myLabel.grid(row=0, column=0,padx=290,pady=10)

        frame = LabelFrame(root1, text="Click Here ...",bg="#ECECEC", padx=80, pady=60)
        frame.place(x=40,y=70)  

        # Add a Logout button to go back to the login page
        logout_button = Button(root1, text='Logout', command=lambda: logout_and_show_login(root1),fg='#fff', bg='#E40404', relief='raised', borderwidth=2, cursor='hand2', width=15)
        logout_button.place(x=10,y=10)


        def create():
            global app
            global img1
            global new_pic1
            app = Toplevel()
            app.title("Create a new account")
            app.geometry("975x475+300+200")
            app.configure(bg='#D3D3D3')

            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()    

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                userid TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                emailaddress TEXT NOT NULL,
                contactnum TEXT NOT NULL,
                gender TEXT NOT NULL
            )''')


            def signup():
                userid = userid_entry.get()
                username = username_entry.get()
                password = password_entry.get()
                emailaddress = emailaddress_entry.get()
                contactnum = contactnum_entry.get()
                gender = gender_entry.get()


                if userid != '' and username != '' and password != '' and emailaddress != '' and contactnum != '' and gender != '':
                    cursor.execute('SELECT userid From users WHERE userid=?', [userid])
                    if cursor.fetchone() is not None:
                        messagebox.showerror('Error', 'ID already exists.')
                    else:
                        encoded_password = password.encode('utf-8')
                        hashed_password = bcrypt.hashpw(encoded_password,
                                                    bcrypt.gensalt())  # this make our password more secure
                        print(hashed_password)
                        cursor.execute('INSERT INTO users (userid,username,password,emailaddress,contactnum,gender) VALUES (?,?,?,?,?,?)', [userid,username,hashed_password,emailaddress,contactnum,gender])
                        conn.commit()
                        messagebox.showinfo('Success', 'Account has been created.')
                else:
                    messagebox.showerror('Error', 'Enter all data.')

            frame1 = Frame(app, bg='#D3D3D3', width=925, height=475.545)
            frame1.place(x=0, y=0)

            img1 = Image.open('Mini IT Project/acc.jpg')
            resized = img1.resize((338, 332))
            new_pic1 = ImageTk.PhotoImage(resized)
            image1_label = Label(frame1, image=new_pic1, bg='#D3D3D3')
            image1_label.place(x=70, y=50)

            signup_label = Label(frame1, text='SIGN UP', fg='#57a1f8', bg='#D3D3D3', font=('Microsoft YaHei UI Light', 23, 'bold'))
            signup_label.place(x=620, y=10)

            userid_entry = Label(frame1, text='Student ID:', fg='black', bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            userid_entry.place(x=480, y=125)

            userid_entry = Entry(frame1,  width=25, fg='Black', border=0, bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            userid_entry.place(x=483, y=150)
            Frame(frame1, width=195, height=2, bg='black').place(x=476, y=175)

            username_entry = Label(frame1, text='Student Name:', fg='black', bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            username_entry.place(x=480, y=195)

            username_entry = Entry(frame1,  width=25, fg='Black', border=0, bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            username_entry.place(x=483, y=220)
            Frame(frame1, width=195, height=2, bg='black').place(x=476, y=245)

            password_entry = Label(frame1, text='Password:', fg='black', bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            password_entry.place(x=480, y=265)

            password_entry = Entry(frame1, width=25, fg='Black', border=0, bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            password_entry.place(x=483, y=290)
            password_entry.config(show='●')
            Frame(frame1, width=195, height=2, bg='black').place(x=476, y=315)

            emailaddress_entry =  Label(frame1, text='Email Address:', fg='black', bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            emailaddress_entry.place(x=700, y=125)

            emailaddress_entry = Entry(frame1, width=25, fg='Black', border=0, bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            emailaddress_entry.place(x=703, y=150)
            Frame(frame1, width=195, height=2, bg='black').place(x=696, y=175)
            
            contactnum_entry = Label(frame1, text='Contact Number:', fg='black', bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            contactnum_entry.place(x=700, y=195)

            contactnum_entry = Entry(frame1, width=25, fg='Black', border=0, bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            contactnum_entry.place(x=703, y=220)
            Frame(frame1, width=195, height=2, bg='black').place(x=696, y=245)
            
            gender_entry = Label(frame1, text='Gender(MALE/FEMALE):', fg='black', bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            gender_entry.place(x=700, y=265)

            gender_entry = Entry(frame1, width=25, fg='Black', border=0, bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
            gender_entry.place(x=703, y=290)
            Frame(frame1, width=195, height=2, bg='black').place(x=696, y=315)

            def toggle_password_visibility():
                if show_password_var2.get():
                    password_entry.config(show='')
                else:
                    password_entry.config(show='●')

            show_password_var2 = IntVar()
            show_password_var2.set(0)  # Initially set to hide password
            toggle_radio2 = Checkbutton(frame1, text='', variable=show_password_var2, bg="#D3D3D3",
                                    command=toggle_password_visibility, cursor='hand2')
            toggle_radio2.place(x=650, y=290)

            signupbtn = Button(frame1, text='Sign up',  bg='#57a1f8', fg='white', border=0, command=signup, cursor='hand2', width=33, pady=5)
            signupbtn.place(x=565, y=360)


        def editstud():    
            root5 = Tk()
            root5.title('EDIT STUDENT INFORMATION')
            root5.geometry("975x475+300+200")
            root5.config(bg='#D3D3D3')

            font1 = ('Arial', 15, 'bold')

            delete_box = Entry(root5, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            delete_box.place(x=450, y=150)
            delete_box_label = Label(root5, text="Student ID :", font=font1, fg='black', bg='#D3D3D3')
            delete_box_label.place(x=300, y=150)
        
            def close1():
                root5.destroy()

            def update1():
                # Create a database or connect to one
                conn = sqlite3.connect('data.db')
            

                # Create cursor
                c = conn.cursor()

                record_id = delete_box.get()

                new_username = username_editor.get()
                new_password = password_editor.get()
                new_emailaddress = emailaddress_editor.get()
                new_contactnum = contactnum_editor.get()
                new_gender = gender_editor.get()


                # Hash the new password before saving
                encoded_password = new_password.encode('utf-8')
                hashed_password = bcrypt.hashpw(encoded_password,
                                                    bcrypt.gensalt())
                c.execute("""UPDATE users SET	
                    username = :username,
                    password = :password,
                    emailaddress = :emailaddress,
                    contactnum = :contactnum,
                    gender = :gender


                    WHERE userid = :userid""",
                    {
                    'username': new_username,
                    'password': hashed_password,
                    'emailaddress': new_emailaddress,
                    'contactnum' : new_contactnum,
                    'gender' : new_gender,
                    'userid': record_id
                    }) 


                    #Commit Changes
                conn.commit()

                # Close Connection 
                conn.close()
                editor.destroy()
                root5.deiconify()
            

            def edit():
                root.withdraw()
                global editor
                editor = Tk()
                editor.title('Update A Record')
                editor.geometry("975x475+300+200")
                editor.config(bg='#D3D3D3')

                def close2():
                   editor.destroy()
                # Create a database or connect to one
                conn = sqlite3.connect('data.db')
                # Create cursor
                c = conn.cursor()

                record_id = delete_box.get()

                # Query the database
                c.execute("SELECT * FROM users WHERE userid = ?", (record_id,))
                records = c.fetchall()

                if not records:
                    editor.destroy()
                    messagebox.showerror("Error", "Invalid Student ID ")
                    return
                    
             

                #Create Global Variables for text box names
                global username_editor
                global password_editor
                global emailaddress_editor
                global contactnum_editor
                global gender_editor
                
                
                    # Create Text Boxes
                username_editor = Entry(editor, font=font1, fg='black', bg='#fff', bd=3, width=26)
                username_editor.grid(row=0, column=1, padx=20, pady=(10, 0))

                password_editor = Entry(editor, font=font1, fg='black', bg='#fff', bd=3, width=26)
                password_editor.grid(row=1, column=1)

                emailaddress_editor = Entry(editor, font=font1, fg='black', bg='#fff', bd=3, width=26)
                emailaddress_editor.grid(row=2, column=1)

                contactnum_editor = Entry(editor,font=font1, fg='black', bg='#fff', bd=3, width=26)
                contactnum_editor.grid(row=3, column=1)

                gender_editor = Entry(editor, font=font1, fg='black', bg='#fff', bd=3, width=26)
                gender_editor.grid(row=4, column=1)

                    # Create Text Box Labels
                username_label = Label(editor, text=" Name", font=font1,fg='black', bg='#D3D3D3')
                username_label.grid(row=0, column=0, pady=(10, 0))
                password_label = Label(editor, text="Password", font=font1,fg='black', bg='#D3D3D3')
                password_label.grid(row=1, column=0)
                emailaddress_label = Label(editor, text="Email Address", font=font1,fg='black', bg='#D3D3D3')
                emailaddress_label.grid(row=2, column=0)
                contactnum_label = Label(editor, text="Contact Number", font=font1,fg='black', bg='#D3D3D3')
                contactnum_label.grid(row=3, column=0)
                gender_label = Label(editor, text="Gender",font=font1,fg='black', bg='#D3D3D3')
                gender_label.grid(row=4, column=0)

                # Loop thru results
                for record in records:
                    username_editor.insert(0, record[1])
                    #password_editor.insert(0, record[2])
                    emailaddress_editor.insert(0, record[3])
                    contactnum_editor.insert(0, record[4])
                    gender_editor.insert(0, record[5])


                # Create a Save Button To Save edited record
                edit_btn = Button(editor, text="Update information", command=update1,font=font1, fg='#fff', bg='#05A312', relief='raised', borderwidth=2, cursor='hand2', width=26)
                edit_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=145)

                back_button = Button(editor, text="BACK", command=close2,font=font1, fg='#fff', bg='#E40404', relief='raised', borderwidth=2, cursor='hand2', width=15)
                back_button.grid(row=10,  column=0, columnspan=2, pady=10, padx=10, ipadx=145)
        

            # Create a Save Button To Save edited record
            edit_btn = Button(root5, text="SEARCH", command=edit,font=font1,fg='#fff', bg='#05A312', relief='raised', borderwidth=2, cursor='hand2', width=26)
            edit_btn.place(x=300,y=200)   

            back_button2 = Button(root5, text="<<<", command=close1,font=font1, fg='#fff', bg='#E40404', relief='raised', borderwidth=2, cursor='hand2', width=4)
            back_button2.place(x=0, y=0)

        

        def deletefunction():
            df = Toplevel()
            df.title("STUDENT PERSONAL INFORMATION")
            df.geometry("975x475+300+200")
            df.config(bg='#D3D3D3')

            font1 = ('Arial', 15, 'bold')

            def close():
                df.destroy()
                

            delete_box = Entry(df, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            delete_box.place(x=450, y=150)
            delete_box_label = Label(df, text="Student ID :",font=font1, fg='black', bg='#D3D3D3')
            delete_box_label.place(x=300, y=150)
            

            def delete():
            # Create a database or connect to one
                conn = sqlite3.connect('data.db')

            # Create cursor
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE userid = ?", (delete_box.get(),))
                records = c.fetchall()

                if not records:
                    messagebox.showerror("Error", "Invalid Student ID ")
                    return

                else :
                    # Delete a record
                    c.execute('DELETE FROM users WHERE userid = ?', (delete_box.get(),))

                    delete_box.delete(0, END)
                    #Commit Changes
                    conn.commit()
                    # Close Connection 

                    conn.close()
                    messagebox.showinfo("Sucess", "DELETED")
                

            #Create A Delete Button
            delete_btn = Button(df, text="Delete Record", command=delete,font=font1, fg='#fff', bg='#05A312', relief='raised', borderwidth=2, cursor='hand2', width=26)
            delete_btn.place(x=350,y=205)
            #messagebox.showinfo("Sucessful deleted")

            back_button = Button(df, text="<<<", command=close,font=font1, fg='#fff', bg='#E40404', relief='raised', borderwidth=2, cursor='hand2', width=4)
            back_button.place(x=0, y=0)
                


        def student_information():
            new = Toplevel()
            new.title("Student Information")
            new.geometry("975x475+300+200")
            new.config(bg='#D3D3D3')

            frame111 = LabelFrame(new, text="Click Here ...",bg="#ECECEC", padx=110, pady=80)
            frame111.place(x=40,y=85)  

            myButton = Button(frame111, text="CREATE ", command=create,fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=15,height=3)
            myButton.grid(row=0, column=0,padx=15,pady=15)
            myButton2 = Button(frame111, text="UPDATE ",command=editstud,fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=15,height=3)
            myButton2.grid(row=0, column=1,padx=15,pady=15)
            myButton3 = Button(frame111, text="DELETE ",  command=deletefunction,fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=15,height=3)
            myButton3.grid(row=0, column=2,padx=15,pady=15)

        def student_list():
            r = tk.Tk()
            r.title("Student List")
            r.geometry('925x475+300+200')
            r.configure(bg='#D3D3D3')
            r.resizable(False, False)

            connect = sqlite3.connect(database="data.db")

            conn = connect.cursor()

            conn.execute("SELECT * FROM users")

            tree=ttk.Treeview(r)
            tree['show']='headings'

            s = ttk.Style(r)
            s.theme_use("clam")

            s.configure(".", font=('Helvetica', 11))
            s.configure("Treeview.Heading", fg='red', font=('Helvetica', 11, "bold"))
            s.configure('Treeview', foreground='#fff', background='#000', fieldbackground='#313837')
            s.map('Treeview', background=[('selected', '#1A8F2D')])

            #Define number of columns
            tree = ttk.Treeview(r, height=20)
            tree["columns"] = ("userid","username","emailaddress","contactnum","gender")
                            
            #Assign the width, minwidth and anchor to the respective columns
            tree.column('#0',width=0,stretch=tk.NO)
            tree.column("userid", width=125,  minwidth=125, anchor=tk.CENTER)
            tree.column("username", width=225,  minwidth=225, anchor=tk.CENTER)
            tree.column("emailaddress", width=200,  minwidth=200, anchor=tk.CENTER)
            tree.column("contactnum", width=150,  minwidth=150, anchor=tk.CENTER)
            tree.column("gender", width=100,  minwidth=100, anchor=tk.CENTER)

            #Assign the heading names to the respective columns
            tree.heading("userid", text="ID", anchor=tk.CENTER)
            tree.heading("username", text="NAME", anchor=tk.CENTER)
            tree.heading("emailaddress", text="EMAIL", anchor=tk.CENTER)
            tree.heading("contactnum", text="CONTACT", anchor=tk.CENTER)
            tree.heading("gender", text="GENDER", anchor=tk.CENTER)

            i = 0
            for ro in conn:
                tree.insert('', i, text=" ", values=(ro[0], ro[1], ro[3], ro[4], ro[5]))

            
            tree.pack()


        def course_information():

            import sqlite3
            import tkinter as tk
            from tkinter import ttk
            from tkinter import messagebox

            # database.py

            def create_table():
                conn = sqlite3.connect('data.db')
                cursor = conn.cursor()

                cursor.execute('''
                CREATE TABLE IF NOT EXISTS data(
                    id INTEGER PRIMARY KEY,
                    subject_name TEXT,
                    subject_code TEXT,
                    credit_hour INTEGER,
                    class_type TEXT,
                    lecture_name TEXT,
                    classes TEXT,
                    capacity INTEGER,
                    class_day TEXT,
                    class_time TEXT,
                    venue TEXT)''')
                conn.commit()
                conn.close()

            def fetch_subjects():
                conn = sqlite3.connect('data.db')
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM data')
                subject = cursor.fetchall()
                conn.close()
                return subject

            def insert_subject(id, subject_name, subject_code, credit_hour, class_type, lecture_name, classes, capacity, class_day, class_time, venue):
                conn = sqlite3.connect('data.db')
                cursor = conn.cursor()
                cursor.execute('INSERT INTO data(id, subject_name, subject_code, credit_hour, class_type, lecture_name, classes, capacity, class_day, class_time, venue) VALUES(?,?,?,?,?,?,?,?,?,?,?)',
                                (id, subject_name, subject_code, credit_hour, class_type, lecture_name, classes, capacity, class_day, class_time, venue))
                conn.commit()
                conn.close()

            def delete_subject(id):
                conn = sqlite3.connect('data.db')
                cursor = conn.cursor()
                cursor.execute('DELETE FROM data WHERE id = ?', (id,))
                conn.commit()
                conn.close()

            def update_subject(new_subject_name, new_subject_code, new_credit_hour, new_class_type, new_lecture_name, new_classes, new_capacity, new_class_day, new_class_time, new_venue, id):
                conn = sqlite3.connect('data.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE data SET subject_name = ?, subject_code = ?, credit_hour = ?, class_type = ?, lecture_name = ?, classes = ?, capacity = ?, class_day = ?, class_time = ?, venue = ? WHERE id = ?",
                            (new_subject_name, new_subject_code, new_credit_hour, new_class_type, new_lecture_name, new_classes, new_capacity, new_class_day, new_class_time, new_venue, id))
                conn.commit()
                conn.close()

            def id_exists(id):
                conn = sqlite3.connect('data.db')
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) from data WHERE id = ?', (id,))
                result = cursor.fetchone()
                conn.close()
                return result[0] > 0

            create_table()

            apps = tk.Tk()
            apps.title('Admin Course Function')
            apps.geometry('1450x600')
            apps.config(bg='#D3D3D3')
            # Configure the window to be full screen
            apps.attributes('-fullscreen', True)
            # Configure the window manager attributes for decorations
            apps.overrideredirect(False)  # Set to True to remove decorations
            apps.resizable(False, False)

            font1 = ('Arial', 15, 'bold')
            font2 = ('Arial', 12, 'bold')

            def close_app():
                apps.destroy()

            def add_to_threeview():
                subjects = fetch_subjects()
                tree.delete(*tree.get_children())
                for subject in subjects:
                    tree.insert('', tk.END, values=subject)

            def clear(*clicked):
                if clicked:
                    tree.selection_remove(tree.focus())
                    tree.focus('')
                id_entry.delete(0, tk.END)  # Use tk.END instead of just END
                subject_name_entry.delete(0, tk.END)
                subject_code_entry.delete(0, tk.END)
                credit_hour_entry.delete(0, tk.END)
                classes_type_entry.delete(0, tk.END)
                lecture_name_entry.delete(0, tk.END)
                class_entry.delete(0, tk.END)
                capacity_entry.delete(0, tk.END)
                class_day_entry.delete(0, tk.END)
                class_time_entry.delete(0, tk.END)
                venue_entry.delete(0, tk.END)

            def display_data(event):
                selected_item = tree.focus()
                if selected_item:  # when clicked on the row on treeview, if this condition is true ,will get the values of this row
                    row = tree.item(selected_item)['values']
                    clear() # call clear function whatever in the entry boxs
                    id_entry.insert(0,row[0])
                    subject_name_entry.insert(0,row[1])
                    subject_code_entry.insert(0,row[2])
                    credit_hour_entry.insert(0,row[3])
                    classes_type_entry.insert(0,row[4])
                    lecture_name_entry.insert(0,row[5])
                    class_entry.insert(0,row[6])
                    capacity_entry.insert(0,row[7])
                    class_day_entry.insert(0,row[8])
                    class_time_entry.insert(0,row[9])
                    venue_entry.insert(0,row[10])  

                    # Update the Treeview row with the new values
                    tree.item(selected_item, values=row)    
                else:
                    pass # if not clicked on the row in the treeview will pass ,will no do anything

            def delete1():
                selected_item = tree.focus()
                if not selected_item:
                    messagebox.showerror('Error','Choose an subject to delete.')
                else:
                    id = id_entry.get()
                    delete_subject(id) # call the delete_subject(id)function in database.db
                    add_to_threeview() # call the add_to_treeview function ,can get that data from the database to that treeview after the deletion
                    clear()
                    messagebox.showinfo('Success','Data has been deleted.')

            def update1():
                selected_item = tree.focus()
                if not selected_item:
                    messagebox.showerror('Error', 'Choose a subject to update.')
                else:
                    id = id_entry.get()
                    subject_name = subject_name_entry.get()
                    subject_code = subject_code_entry.get()
                    credit_hour = credit_hour_entry.get()
                    class_type = classes_type_entry.get()
                    lecture_name = lecture_name_entry.get()
                    classes = class_entry.get()
                    capacity = capacity_entry.get()
                    class_day = class_day_entry.get()
                    class_time = class_time_entry.get()
                    venue = venue_entry.get()
                    update_subject(subject_name,subject_code,credit_hour,class_type,lecture_name,classes,capacity,class_day,class_time,venue,id)
                    add_to_threeview()
                    clear()
                    messagebox.showinfo('Success', 'Data has been updated.')


            def insert():
                id = id_entry.get()
                subject_name = subject_name_entry.get()
                subject_code = subject_code_entry.get()
                credit_hour = credit_hour_entry.get()
                class_type = classes_type_entry.get()
                lecture_name = lecture_name_entry.get()
                classes = class_entry.get()
                capacity = capacity_entry.get()
                class_day = class_day_entry.get()
                class_time = class_time_entry.get()
                venue = venue_entry.get()
                if not (id and subject_name and subject_code and credit_hour and class_type and lecture_name and classes and capacity and class_day and class_time and venue):
                        messagebox.showerror('Error','Enter all fields.')

                elif id_exists(id):
                        messagebox.showerror('Error','ID already exists.')

                else:
                    insert_subject(id,subject_name,subject_code,credit_hour,class_type,lecture_name,classes,capacity,class_day,class_time,venue)
                    add_to_threeview()
                    clear()
                    messagebox.showinfo('Success','Data has been inserted.')


            id_label = tk.Label(apps, font=font1, text='ID                    : ', fg='black', bg='#D3D3D3')
            id_label.place(x=20, y=20)

            id_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            id_entry.place(x=170, y=20)

            subject_name_label = tk.Label(apps, font=font1, text='Subject Name : ', fg='black', bg='#D3D3D3')
            subject_name_label.place(x=20, y=80)

            subject_name_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            subject_name_entry.place(x=170, y=80)

            subject_code_label = tk.Label(apps, font=font1, text='Subject Code  : ', fg='black', bg='#D3D3D3')
            subject_code_label.place(x=20, y=140)

            subject_code_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            subject_code_entry.place(x=170, y=140)

            credit_hour_label = tk.Label(apps, font=font1, text='Credit Hour     : ', fg='black', bg='#D3D3D3')
            credit_hour_label.place(x=20, y=200)

            credit_hour_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            credit_hour_entry.place(x=170, y=200)

            classes_type_label = tk.Label(apps, font=font1, text='Class  Type    : ', fg='black', bg='#D3D3D3')
            classes_type_label.place(x=20, y=260)

            classes_type_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            classes_type_entry.place(x=170, y=260)

            lecture_name_label = tk.Label(apps, font=font1, text='Lecture Name : ', fg='black', bg='#D3D3D3')
            lecture_name_label.place(x=20, y=320)

            lecture_name_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            lecture_name_entry.place(x=170, y=320)

            class_label = tk.Label(apps, font=font1, text='Class              : ', fg='black', bg='#D3D3D3')
            class_label.place(x=20, y=380)

            class_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            class_entry.place(x=170, y=380)

            capacity_label = tk.Label(apps, font=font1, text='Capacity         : ', fg='black', bg='#D3D3D3')
            capacity_label.place(x=20, y=440)

            capacity_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            capacity_entry.place(x=170, y=440)

            class_day_label = tk.Label(apps, font=font1, text='Class Day       : ', fg='black', bg='#D3D3D3')
            class_day_label.place(x=20, y=500)

            class_day_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            class_day_entry.place(x=170, y=500)

            class_time_label = tk.Label(apps, font=font1, text='Class Time     : ', fg='black', bg='#D3D3D3')
            class_time_label.place(x=20, y=560)

            class_time_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            class_time_entry.place(x=170, y=560)

            venue_label = tk.Label(apps, font=font1, text='Venue             : ', fg='black', bg='#D3D3D3')
            venue_label.place(x=20, y=620)

            venue_entry = tk.Entry(apps, font=font1, fg='#000', bg='#fff', bd=3, width=26)
            venue_entry.place(x=170, y=620)


            # Replace custom button widget with standard tkinter.Button widget
            add_button = tk.Button(apps, command=insert, font=font1, text='Add Subject', fg='#fff', bg='#05A312', relief='raised', borderwidth=2, cursor='hand2', width=26)
            add_button.place(x=50, y=660)

            clear_button = tk.Button(apps, command=lambda: clear(True), font=font1, text='Clear', fg='#fff', bg='#161C25', relief='raised', borderwidth=2, cursor='hand2', width=26)
            clear_button.place(x=50, y=710)

            update_button = tk.Button(apps, command=update1, font=font1, text='Update Subject', fg='#fff', bg='#161C25', relief='raised', borderwidth=2, cursor='hand2', width=26)
            update_button.place(x=580, y=710)

            delete_button = tk.Button(apps, command=delete1, font=font1, text='Delete Subject', fg='#fff', bg='#E40404', relief='raised', borderwidth=2, cursor='hand2', width=26)
            delete_button.place(x=1100, y=710)

            close_button = tk.Button(apps, text="Close", command=close_app,font=font1, fg='#fff', bg='#E40404', relief='raised', borderwidth=2, cursor='hand2', width=15)
            close_button.place(x=50, y=760)

            style = ttk.Style(apps)
            style.theme_use('clam')
            style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
            style.map('Treeview', background=[('selected', '#1A8F2D')])

            tree = ttk.Treeview(apps, height=32)
            tree['columns'] = ('id','subject_name','subject_code','credit_hour','class_type','lecture_name','classes','capacity','class_day','class_time','venue')

            tree.column('#0',width=0,stretch=tk.NO) # Hide the default first column
            tree.column('id',anchor=tk.CENTER,width=50)
            tree.column('subject_name',anchor=tk.CENTER,width=110)
            tree.column('subject_code',anchor=tk.CENTER,width=80)
            tree.column('credit_hour',anchor=tk.CENTER,width=50)
            tree.column('class_type',anchor=tk.CENTER,width=110)
            tree.column('lecture_name',anchor=tk.CENTER,width=110)
            tree.column('classes',anchor=tk.CENTER,width=90)
            tree.column('capacity',anchor=tk.CENTER,width=50)
            tree.column('class_day',anchor=tk.CENTER,width=90)
            tree.column('class_time',anchor=tk.CENTER,width=110)
            tree.column('venue',anchor=tk.CENTER,width=110)

            tree.heading('id',text='ID')
            tree.heading('subject_name',text='Subject Name')
            tree.heading('subject_code',text='Subject Code')
            tree.heading('credit_hour',text='Credit Hour')
            tree.heading('class_type',text='Class Type')
            tree.heading('lecture_name',text='Lecture Name')
            tree.heading('classes',text='Class')
            tree.heading('capacity',text='Capacity')
            tree.heading('class_day',text='Class Day')
            tree.heading('class_time',text='Class Time')
            tree.heading('venue',text='Venue')

            tree.place(x=470,y=20)

            tree.bind('<ButtonRelease>', display_data)

            add_to_threeview()

            apps.mainloop()

        # Define a function to fetch all unique subjects from the database
        def fetch_all_subjects():
            try:
                # Connect to the database
                connect = sqlite3.connect(database="data.db")
                conn = connect.cursor()

                # Fetch all unique subjects from the ratings table
                subjects = conn.execute('SELECT DISTINCT subject_name FROM ratings').fetchall()

                # Close the database connection
                connect.close()

                return [subject[0] for subject in subjects]

            except Exception as e:
                print(f"Error fetching subjects: {str(e)}")
                return []

        # Define a function to calculate the average rating for a given subject
        def calculate_average_rating(subject_name):
            try:
                # Connect to the database
                connect = sqlite3.connect(database="data.db")
                conn = connect.cursor()

                # Fetch all ratings for the same class
                ratings = conn.execute('SELECT rating FROM ratings WHERE subject_name = ?', (subject_name,)).fetchall()

                # Close the database connection
                connect.close()

                if not ratings:
                    return None

                # Extract the ratings from the fetched data
                ratings = [entry[0] for entry in ratings]

                # Calculate the average rating
                average_rating = sum(ratings) / len(ratings)

                return average_rating

            except Exception as e:
                print(f"Error calculating average rating for {subject_name}: {str(e)}")
                return None

        # Define a function to display the average ratings in a histogram in a Tkinter GUI
        def display_average_ratings_histogram():
            subjects = fetch_all_subjects()

            if not subjects:
                print("No subjects found.")
                return

            # Create a Tkinter GUI window
            gui = tk.Tk()
            gui.title("Average Ratings Histogram")

            # Create a Matplotlib figure
            fig, ax = plt.subplots(figsize=(9, 7), dpi=60)

            # Fetch average ratings for each subject
            average_ratings = [calculate_average_rating(subject) for subject in subjects]

            # Plot the data as a bar chart
            ax.bar(subjects, average_ratings, color='blue')
            ax.set_title("Average Ratings by Subject")
            ax.set_xlabel("Subject")
            ax.set_ylabel("Average Rating")

            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha="right")

            # Create a Tkinter canvas to display the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig, master=gui)
            canvas.get_tk_widget().pack()

            # Start the Tkinter main loop
            gui.mainloop()

        # Create a function to display the average ratings in a histogram when the button is clicked
        def show_average_ratings_histogram():
            display_average_ratings_histogram()




        myLabel1 = Button(frame, text="STUDENT INFORMATION", command=student_information, fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=25,height=3)
        myLabel1.grid(row=0, column=0, padx=15, pady=15)

        myLabel2 = Button(frame, text="COURSE INFORMATION", command=course_information, fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=25,height=3)
        myLabel2.grid(row=0, column=1, padx=15, pady=15)

        myLabel3 = Button(frame, text="STUDENT LIST", command=student_list, fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=25,height=3)
        myLabel3.grid(row=1, column=0, padx=15, pady=15)

        myLabel4 = Button(frame, text="SHOW RANK CLASSES", command=show_average_ratings_histogram, fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=25,height=3)
        myLabel4.grid(row=1, column=1, padx=15, pady=15)
       
    else:
    # Student login logic
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        cursor.execute('''
             CREATE TABLE IF NOT EXISTS users (
               userid TEXT NOT NULL, 
               username TEXT NOT NULL,
               password TEXT NOT NULL)''')
        cursor.execute('SELECT password From users WHERE userid=?', [userid])
        result = cursor.fetchone()

        if result:
            if bcrypt.checkpw(password.encode('utf-8'), result[0]):
                root.withdraw()  # Hide the original login window
                root60 = Tk()
                root60.title("User GUI")
                root60.geometry('925x475+300+200')
                root60.configure(bg='#D3D3D3')
                root60.resizable(False, False)


                myLabel = Label(root60, text="WELCOME BACK STUDENT ", bg='#D3D3D3', font=('Calibri', 25))
                myLabel.place(x=300,y=5)

                # Create the Treeview widget
                tree = ttk.Treeview(root60)
                tree['columns'] = ('subject_name', 'subject_code', 'credit_hour', 'class_type', 'lecture_name', 'classes',
                                'capacity', 'class_day', 'class_time', 'venue')

                def view_timetable():
                    global userid_entry2
                    apps2 = tk.Tk()
                    apps2.title('Time Table')
                    apps2.geometry('925x475+300+200')
                    apps2.config(bg='#D3D3D3')

                    myLabel = tk.Label(apps2, text="TIME TABLE", bg='#D3D3D3', font=('Calibri, 15'))
                    myLabel.place(x=400, y=1)

                    connect = sqlite3.connect(database="data.db")
                    conn = connect.cursor()

                    student_id = userid_entry2.get()

                    # Create a SQL query to retrieve the user's timetable data sorted by day
                    timetable_query = """
                    SELECT * FROM register 
                    WHERE student_id = ? 
                    ORDER BY 
                        CASE 
                            WHEN class_day = 'MONDAY' THEN 7
                            WHEN class_day = 'TUESDAY' THEN 6
                            WHEN class_day = 'WEDNESDAY' THEN 5
                            WHEN class_day = 'THURSDAY' THEN 4
                            WHEN class_day = 'FRIDAY' THEN 3
                            WHEN class_day = 'SATURDAY' THEN 2
                            WHEN class_day = 'SUNDAY' THEN 1
                        END
                    """
                    conn.execute(timetable_query, [student_id])

                    tree = ttk.Treeview(apps2)
                    tree['show'] = 'headings'

                    font1 = ('Arial', 15, 'bold')
                    font2 = ('Arial', 12, 'bold')

                    style = ttk.Style(apps2)
                    style.theme_use('clam')
                    style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
                    style.map('Treeview', background=[('selected', '#1A8F2D')])

                    tree = ttk.Treeview(apps2, height=20)
                    tree['columns'] = ('class_type', 'class_day', 'class_start_time', 'class_end_time', 'subject_name','classes', 'venue')

                    tree.column('#0', width=0, stretch=tk.NO)  # Hide the default first column
                    tree.column('class_type', anchor=tk.CENTER, width=110)
                    tree.column('class_day', anchor=tk.CENTER, width=120)
                    tree.column('class_start_time', anchor=tk.CENTER, width=90)
                    tree.column('class_end_time', anchor=tk.CENTER, width=90)
                    tree.column('subject_name', anchor=tk.CENTER, width=180)
                    tree.column('classes', anchor=tk.CENTER, width=120)
                    tree.column('venue', anchor=tk.CENTER, width=140)

                    tree.heading('class_type', text='Type', anchor=tk.CENTER)
                    tree.heading('class_day', text='Day', anchor=tk.CENTER)
                    tree.heading('class_start_time', text='Start Time', anchor=tk.CENTER)
                    tree.heading('class_end_time', text='End Time', anchor=tk.CENTER)
                    tree.heading('subject_name', text='Subject', anchor=tk.CENTER)
                    tree.heading('classes', text='Class', anchor=tk.CENTER)
                    tree.heading('venue', text='Venue', anchor=tk.CENTER)

                    tree.place(x=35, y=25)

                    i = 0
                    for row in conn:
                        tree.insert('', i, text=" ", values=(row[5], row[9], row[10], row[11], row[2], row[7],row[12]))

                    apps2.mainloop()

                
                         
                #"subject name"只被显示一次在"Browse Course"页面上。当用户再次打开"Browse Course"页面时，相同的"subject name"不会重复显示。
                def browse_course():
                    displayed_subjects = set()  #创建一个空的集合来存储已经显示的"subject name"。
                    def on_item_double_click(event):
                        # Get the selected item's course information
                        selected_item = tree.selection()


                    browse_course_window = Toplevel(root60)
                    browse_course_window.title("Course Offered")
                    browse_course_window.geometry('925x475+300+200')
                    browse_course_window.resizable(False, False)
                    browse_course_window.config(bg='#D3D3D3')

                    browselLabel = tk.Label(browse_course_window, text="View Course Offered", bg='#D3D3D3', font=('Calibri', 20))
                    browselLabel.place(x=360,y=10)

                    style = ttk.Style(browse_course_window)
                    style.theme_use('clam')
                    style.configure('Treeview', foreground='#fff', background='#000', fieldbackground='#313837')
                    style.map('Treeview', background=[('selected', '#1A8F2D')])

                    tree = ttk.Treeview(browse_course_window,height=17)
                    tree.column('#0', width=0, stretch=tk.NO)  # Hide the default first column
                    tree['columns'] = ('subject_name', 'subject_code', 'credit_hour')

                    # Set Treeview column headings (excluding 'id')
                    for col in ('subject_name', 'subject_code', 'credit_hour'):
                        tree.heading(col, text=col)  # Use the actual column names
                        tree.column(col, width=250,anchor=tk.CENTER)  # Adjust column width as needed

                    # Fetch course information from the database
                    courses = fetch_subjects()

                    # Insert course information into the Treeview (excluding 'id')
                    for course in courses:
                        subject_name = course[1]
                        # Check if subject_name has been displayed already
                        if subject_name not in displayed_subjects:
                            displayed_subjects.add(subject_name)  # Add to the set
                            # Exclude the 'id' column from course_info
                            course_info = course[1:]  # Skip the first element (id)
                            tree.insert('', 'end', values=course_info)

                    tree.place(x=90,y=50)  # Use grid manager for the tree
                    # Bind the double-click event handler to the Treeview

                    tree.bind("<Double-1>", on_item_double_click)


                

                registered_courses = {}
                selected_index = 0

                def register_course_page():
                    def refresh():
                        root.destroy()
                        register_course_page()
                    def load_courses():
                        conn = sqlite3.connect('data.db')
                        cursor = conn.cursor()
                        cursor.execute("SELECT subject_name, subject_code, credit_hour, class_type, lecture_name, classes, capacity, class_day, class_time, venue FROM data")
                        courses = cursor.fetchall()
                        conn.close()
                        return courses

                    def update_selected_course(event):
                        global selected_index
                        selection = course_tree.selection()
                        if selection:
                            selected_index = course_tree.index(selection)
                            selected_course_info = courses[selected_index]
                            subject_name, subject_code, credit_hour, class_type, lecture_name, classes, capacity, class_day, class_time, venue = selected_course_info

                            course_entry.config(state='normal')
                            course_entry.delete(0, tk.END)
                            course_entry.insert(0, subject_name)
                            course_entry.config(state='readonly')

                            course_code_entry.config(state='normal')
                            course_code_entry.delete(0, tk.END)
                            course_code_entry.insert(0, subject_code)
                            course_code_entry.config(state='readonly')

                            class_type_entry.config(state='normal')
                            class_type_entry.delete(0, tk.END)
                            class_type_entry.insert(0, class_type)
                            class_type_entry.config(state='readonly')
                            
                            credit_hour_entry.config(state='normal')
                            credit_hour_entry.delete(0, tk.END)
                            credit_hour_entry.insert(0, credit_hour)
                            credit_hour_entry.config(state='readonly')

                            lecture_name_entry.config(state='normal')
                            lecture_name_entry.delete(0, tk.END)
                            lecture_name_entry.insert(0, lecture_name)
                            lecture_name_entry.config(state='readonly')

                            classes_entry.config(state='normal')
                            classes_entry.delete(0, tk.END)
                            classes_entry.insert(0, classes)
                            classes_entry.config(state='readonly')

                            class_day_entry.config(state='normal')
                            class_day_entry.delete(0, tk.END)
                            class_day_entry.insert(0, class_day)
                            class_day_entry.config(state='readonly')

                            class_start_time_entry.config(state='normal')
                            class_start_time_entry.delete(0, tk.END)
                            class_start_time_entry.insert(0, class_time.split('-')[0].strip())
                            class_start_time_entry.config(state='readonly')

                            class_end_time_entry.config(state='normal')
                            class_end_time_entry.delete(0, tk.END)
                            class_end_time_entry.insert(0, class_time.split('-')[1].strip())
                            class_end_time_entry.config(state='readonly')

                            venue_entry.config(state='normal')
                            venue_entry.delete(0, tk.END)
                            venue_entry.insert(0, venue)
                            venue_entry.config(state='readonly')

                            capacity_entry.config(state='normal')
                            capacity_entry.delete(0, tk.END)
                            capacity_entry.insert(0, capacity)
                            capacity_entry.config(state='readonly')

                    def check_class_capacity(course_name, class_type, classes):
                        conn = sqlite3.connect('data.db')
                        cursor = conn.cursor()

                        cursor.execute('''
                            CREATE TABLE IF NOT EXISTS register (
                                id INTEGER PRIMARY KEY,
                                student_id TEXT,
                                subject_name TEXT,
                                subject_code TEXT,
                                credit_hour INTEGER,
                                class_type TEXT,
                                lecture_name TEXT,
                                classes TEXT,
                                capacity INTEGER,
                                class_day TEXT,
                                class_start_time TEXT,
                                class_end_time TEXT,
                                venue TEXT
                            )''')

                        cursor.execute("SELECT COUNT(*) FROM register WHERE subject_name = ? AND class_type = ? AND classes = ?",
                                    (course_name, class_type, classes))
                        registered_count = cursor.fetchone()[0]

                        conn.close()
                        return registered_count

                    def view_class_capacity():
                        course_name = course_entry.get()
                        class_type = class_type_entry.get()
                        classes = classes_entry.get()

                        if not course_name or not class_type or not classes:
                            messagebox.showerror("", "Please enter both course name and class type.")
                            return

                        capacity = capacity_entry.get()
                        registered_count = check_class_capacity(course_name, class_type, classes)
                        available_places = int(capacity) - int(registered_count)

                        message = f"Class: {course_name} ({class_type})\n"
                        message += f"Capacity: {capacity}\n"
                        message += f"Registered Students: {registered_count}\n"
                        message += f"Available Places: {available_places}"

                        messagebox.showinfo("Class Capacity", message)

                    def check_course_clashes(student_id, class_day, class_time):
                        conn = sqlite3.connect('data.db')
                        cursor = conn.cursor()

                        # Fetch all the registrations for the given student
                        cursor.execute("SELECT class_day, class_start_time, class_end_time FROM register WHERE student_id = ?", (student_id,))
                        existing_registrations = cursor.fetchall()

                        # Check if the new registration clashes with any existing registration
                        for existing_registration in existing_registrations:
                            existing_class_day, existing_class_start_time, existing_class_end_time = existing_registration
                            # Check for clashes
                            if (class_day == existing_class_day and
                                (class_time >= existing_class_start_time and class_time <= existing_class_end_time)):
                                conn.close()
                                return True  # There is a clash

                        conn.close()
                        return False  # No clashes found

                    def save_registration():
                        student_id = student_id_entry.get()
                        course_name = course_entry.get()
                        course_code = course_code_entry.get()
                        class_type = class_type_entry.get()
                        credit_hour = credit_hour_entry.get()
                        lecture_name = lecture_name_entry.get()
                        classes = classes_entry.get()
                        class_day = class_day_entry.get()
                        class_start_time = class_start_time_entry.get()
                        class_end_time = class_end_time_entry.get()
                        venue = venue_entry.get()
                        capacity = capacity_entry.get()
                        global userid_entry2

                        current_capacity = check_class_capacity(course_name, class_type, classes)

                        if student_id == userid_entry2.get():
                            if int(current_capacity) >= int(capacity):
                                messagebox.showerror("", "Class is full. Registration is not allowed.")
                                return

                            # if check_course_clashes(student_id, class_day, class_start_time + '-' + class_end_time):
                            #     messagebox.showerror("", "Time or day clash with a registered course.")
                            #     return

                            if check_course_clashes(student_id, class_day, class_start_time + '-' + class_end_time):
                                messagebox.showerror("", "Time or day clash with a registered course.")
                                return

                            conn = sqlite3.connect('data.db')
                            cursor = conn.cursor()
                            cursor.execute("SELECT COUNT(*) FROM register WHERE student_id = ? AND subject_name = ? AND subject_code = ? AND class_type = ? AND classes = ?",
                                        (student_id, course_name, course_code , class_type, classes))
                            existing_registration_count = cursor.fetchone()[0]
                            conn.close()

                            if existing_registration_count > 0:
                                messagebox.showerror("", "You have already registered for this course.")
                                return

                            conn = sqlite3.connect('data.db')
                            cursor = conn.cursor()
                            cursor.execute('''
                                CREATE TABLE IF NOT EXISTS register (
                                    id INTEGER PRIMARY KEY,
                                    student_id TEXT,
                                    subject_name TEXT,
                                    subject_code TEXT,
                                    credit_hour INTEGER,
                                    class_type TEXT,
                                    lecture_name TEXT,
                                    classes TEXT,
                                    capacity INTEGER,
                                    class_day TEXT,
                                    class_start_time TEXT,
                                    class_end_time TEXT,
                                    venue TEXT
                                )''')

                            cursor.execute('INSERT INTO register (student_id, subject_name, subject_code, credit_hour, class_type, lecture_name,classes, capacity, class_day, class_start_time, class_end_time, venue) VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                        (student_id, course_name, course_code, credit_hour, class_type, lecture_name, classes, capacity, class_day, class_start_time, class_end_time, venue))

                            conn.commit()
                            conn.close()

                            if student_id in registered_courses:
                                registered_courses[student_id].append(course_code)
                            else:
                                registered_courses[student_id] = [course_code]

                            course_entry.delete(0, tk.END)
                            course_code_entry.delete(0, tk.END)
                            student_id_entry.delete(0, tk.END)
                            class_type_entry.delete(0, tk.END)
                            credit_hour_entry.delete(0, tk.END)
                            lecture_name_entry.delete(0, tk.END)
                            classes_entry.delete(0, tk.END)
                            class_day_entry.delete(0, tk.END)
                            class_start_time_entry.delete(0, tk.END)
                            class_end_time_entry.delete(0, tk.END)
                            venue_entry.delete(0, tk.END)
                            capacity_entry.delete(0, tk.END)
                            messagebox.showinfo("", "SUCCESSFUL REGISTER")
                        else:
                            messagebox.showerror("", "Invalid Student ID")

                    def delete_timetable_entry(event):
                        selected_item = tree.selection()[0]  # 获取选中的行
                        response = messagebox.askyesno("Confirm deletion", "Are you sure you want to delete this course?")
                        if response == True:
                            # 用户点击了"Yes"，删除选中的行
                            course_name = tree.item(selected_item, 'values')[4]  # 获取选中行的课程名称
                            class_type = tree.item(selected_item, 'values')[0]  # 获取选中行的课程类型
                            classes = tree.item(selected_item, 'values')[5]  # 获取选中行的班级
                            delete_course_from_database(course_name, class_type, classes)
                            tree.delete(selected_item)
                        # 如果用户点击了"No"，不执行任何操作

                    def delete_course_from_database(course_name, class_type, classes):
                        # 从数据库中删除课程信息的函数
                        conn = sqlite3.connect('data.db')
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM register WHERE subject_name = ? AND class_type = ? AND classes = ?",
                                    (course_name, class_type, classes))
                        conn.commit()
                        conn.close()


                    def close_register():
                        root.destroy()

                        

                    root = tk.Tk()
                    root.title("Course Registration")
                    root.resizable(False, False)
                    root.config(bg='#D3D3D3')
                    # Configure the window to be full screen
                    root.attributes('-fullscreen', True)
                    # Configure the window manager attributes for decorations
                    root.overrideredirect(False)  # Set to True to remove decorations

                    style = ttk.Style(root)
                    style.theme_use('clam')
                    style.configure('Treeview', foreground='#fff', background='#000', fieldbackground='#313837')
                    style.map('Treeview', background=[('selected', '#1A8F2D')])

                    # course_tree = ttk.Treeview(root, height=10)
                    course_tree = ttk.Treeview(root,height=18, columns=("ID", "Course Name", "Course Code", "Credit Hours", "Class Type", "Lecture Name", "Classes", "Capacity", "Class Day", "Class Time", "Venue"))
                    course_tree.column('#0', width=0, stretch=tk.NO)
                    course_tree['show'] = 'headings'
                    columns = ("ID", "Course Name", "Course Code", "Credit Hours", "Class Type", "Lecture Name", "Classes", "Capacity", "Class Day", "Class Time", "Venue")
                    for col in columns:
                        course_tree.column(col, width=97)
                        course_tree.heading(col, text=col, anchor=tk.CENTER)

                    conn = sqlite3.connect('data.db')
                    cursor = conn.cursor()

                    cursor.execute("SELECT * FROM data")
                    for row in cursor.fetchall():
                        course_tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))

                    course_tree.place(x=10,y=10)
                    course_tree.bind("<<TreeviewSelect>>", update_selected_course)

                    course_label = tk.Label(root, text="Select Course:", bg='#D3D3D3')
                    courses = load_courses()
                    course_entry = ttk.Entry(root, state='readonly')

                    course_code_label = tk.Label(root, text="Course code:", bg='#D3D3D3')
                    course_code_entry = ttk.Entry(root, state='readonly')

                    student_id_label = tk.Label(root, text="Student ID:", bg='#D3D3D3')
                    student_id_entry = ttk.Entry(root)

                    class_type_label = tk.Label(root, text="Class Type:", bg='#D3D3D3')
                    class_type_entry = ttk.Entry(root, state='readonly')

                    credit_hour_label = tk.Label(root, text="Credit_hour:", bg='#D3D3D3')
                    credit_hour_entry = ttk.Entry(root, state='readonly')

                    lecture_name_label = tk.Label(root, text="Lecture Name:", bg='#D3D3D3')
                    lecture_name_entry = ttk.Entry(root, state='readonly')

                    classes_label = tk.Label(root, text="Classes:", bg='#D3D3D3')
                    classes_entry = ttk.Entry(root, state='readonly')

                    class_day_label = tk.Label(root, text="Class Day:", bg='#D3D3D3')
                    class_day_entry = ttk.Entry(root, state='readonly')

                    class_start_time_label = tk.Label(root, text="Class Start Time:", bg='#D3D3D3')
                    class_start_time_entry = ttk.Entry(root, state='readonly')

                    class_end_time_label = tk.Label(root, text="Class End Time:", bg='#D3D3D3')
                    class_end_time_entry = ttk.Entry(root, state='readonly')

                    venue_label = tk.Label(root, text="Venue:", bg='#D3D3D3')
                    venue_entry = ttk.Entry(root, state='readonly')

                    capacity_label = tk.Label(root, text="Capacity:", bg='#D3D3D3')
                    capacity_entry = ttk.Entry(root, state='readonly')

                    save_button = tk.Button(root, text="Save Registration", command=save_registration)

                    # Arrange widgets in a grid
                    course_label.place(x=1100,y=20)
                    course_entry.place(x=1200,y=20)

                    course_code_label.place(x=1100,y=50)
                    course_code_entry.place(x=1200,y=50)

                    student_id_label.place(x=1100,y=80)
                    student_id_entry.place(x=1200,y=80)

                    class_type_label.place(x=1100,y=110)
                    class_type_entry.place(x=1200,y=110)

                    credit_hour_label.place(x=1100,y=140)
                    credit_hour_entry.place(x=1200,y=140)

                    lecture_name_label.place(x=1100,y=170)
                    lecture_name_entry.place(x=1200,y=170)

                    class_day_label.place(x=1100,y=200)
                    class_day_entry.place(x=1200,y=200)

                    class_start_time_label.place(x=1100,y=230)
                    class_start_time_entry.place(x=1200,y=230)

                    class_end_time_label.place(x=1100,y=260)
                    class_end_time_entry.place(x=1200,y=260)

                    venue_label.place(x=1100,y=290)
                    venue_entry.place(x=1200,y=290)

                    classes_label.place(x=1100,y=320)
                    classes_entry.place(x=1200,y=320)

                    capacity_label.place(x=1100,y=350)
                    capacity_entry.place(x=1200,y=350)

                    save_button.place(x=1200,y=400)

                    close_button = tk.Button(root, text="close", command=close_register)
                    close_button.place(x=1200,y=500)
                    
                    view_capacity_button = tk.Button(root, text="View Class Capacity", command=view_class_capacity)
                    view_capacity_button.place(x=1200,y=450)

                    refresh_button = tk.Button(root, text="Refresh", command=refresh)
                    refresh_button.place(x=1200,y=600)

                    title_label = tk.Label(root, text="Draft Timetable", bg='#D3D3D3')
                    title_label.place(x=500,y=405)

                    global userid_entry2

                    connect = sqlite3.connect(database="data.db")
                    conn = connect.cursor()

                    student_id = userid_entry2.get()

                    # Create a SQL query to retrieve the user's timetable data sorted by day
                    timetable_query = """
                    SELECT * FROM register 
                    WHERE student_id = ? 
                    ORDER BY 
                        CASE 
                            WHEN class_day = 'MONDAY' THEN 7
                            WHEN class_day = 'TUESDAY' THEN 6
                            WHEN class_day = 'WEDNESDAY' THEN 5
                            WHEN class_day = 'THURSDAY' THEN 4
                            WHEN class_day = 'FRIDAY' THEN 3
                            WHEN class_day = 'SATURDAY' THEN 2
                            WHEN class_day = 'SUNDAY' THEN 1
                        END
                    """
                    conn.execute(timetable_query, [student_id])

                    tree = ttk.Treeview(root)
                    tree['show'] = 'headings'

                    font1 = ('Arial', 15, 'bold')
                    font2 = ('Arial', 12, 'bold')

                    style = ttk.Style(root)
                    style.theme_use('clam')
                    style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
                    style.map('Treeview', background=[('selected', '#1A8F2D')])

                    tree = ttk.Treeview(root, height=17)
                    tree['columns'] = ('class_type', 'class_day', 'class_start_time', 'class_end_time', 'subject_name','classes', 'venue')

                    tree.column('#0', width=0, stretch=tk.NO)  # Hide the default first column
                    tree.column('class_type', anchor=tk.CENTER, width=160)
                    tree.column('class_day', anchor=tk.CENTER, width=150)
                    tree.column('class_start_time', anchor=tk.CENTER, width=100)
                    tree.column('class_end_time', anchor=tk.CENTER, width=100)
                    tree.column('subject_name', anchor=tk.CENTER, width=200)
                    tree.column('classes', anchor=tk.CENTER, width=195)
                    tree.column('venue', anchor=tk.CENTER, width=160)

                    tree.heading('class_type', text='Type', anchor=tk.CENTER)
                    tree.heading('class_day', text='Day', anchor=tk.CENTER)
                    tree.heading('class_start_time', text='Start Time', anchor=tk.CENTER)
                    tree.heading('class_end_time', text='End Time', anchor=tk.CENTER)
                    tree.heading('subject_name', text='Subject', anchor=tk.CENTER)
                    tree.heading('classes', text='Class', anchor=tk.CENTER)
                    tree.heading('venue', text='Venue', anchor=tk.CENTER)

                    tree.bind("<Double-1>", delete_timetable_entry)

                    tree.place(x=10, y=430)

                    i = 0
                    for row in conn:
                        tree.insert('', i, text=" ", values=(row[5], row[9], row[10], row[11], row[2], row[7],row[12]))


                def open_rating_popup(subject_name, lecture_name, student_id):
                    connect = sqlite3.connect(database="data.db")
                    conn = connect.cursor()

                    # Check if the student has already submitted a survey for this subject
                    existing_survey_query = "SELECT id FROM survey_submissions WHERE student_id = ? AND subject_name = ?"
                    
                    # Create the "survey_submissions" table if it doesn't exist
                    conn.execute('''
                        CREATE TABLE IF NOT EXISTS survey_submissions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            student_id INTEGER,
                            subject_name TEXT
                        )
                    ''')
                    
                    conn.execute(existing_survey_query, (student_id, subject_name))
                    existing_survey = conn.fetchone()

                    if existing_survey:
                        # If the student has already submitted a survey for this subject, show an error message
                        messagebox.showerror("Survey Already Submitted", f"You have already submitted a survey for {subject_name}.")
                    else:
                        def save_rating():
                            rating = rating_value.get()
                            connect = sqlite3.connect(database="data.db")
                            conn = connect.cursor()
                            
                            # Create a table to store the ratings if it doesn't exist
                            conn.execute('''
                                CREATE TABLE IF NOT EXISTS ratings (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    lecture_name TEXT,
                                    subject_name TEXT,
                                    rating INTEGER
                                )
                            ''')

                            # Create a table to store survey submissions if it doesn't exist
                            conn.execute('''
                                CREATE TABLE IF NOT EXISTS survey_submissions (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    student_id INTEGER,
                                    subject_name TEXT
                                )
                            ''')

                            # Insert rating data into the database
                            conn.execute("INSERT INTO ratings (lecture_name, subject_name, rating) VALUES (?, ?, ?)",
                                        (lecture_name, subject_name, rating))

                            # Insert survey submission record
                            conn.execute("INSERT INTO survey_submissions (student_id, subject_name) VALUES (?, ?)",
                                        (student_id, subject_name))

                            # Commit the database changes
                            connect.commit()

                            # Close both the rating popup window and the message box
                            popup_window.destroy()
                            messagebox.showinfo("Survey Submitted", f"Thank you for submitting a survey for {subject_name}. Your feedback has been recorded.")

                            # Print the rating information
                            print(f"Rating for {subject_name} - {lecture_name}: {rating}")

                        # Create the rating popup window
                        popup_window = tk.Toplevel()
                        popup_window.title("Rate Lecture")
                        popup_window.geometry("300x200")
                        popup_window.config(bg='#D3D3D3')

                        # Add labels and a radio button-based rating system
                        label = tk.Label(popup_window, bg='#D3D3D3', text=f"Rate the lecture for {subject_name} - {lecture_name}")
                        label.pack(pady=10)

                        rating_value = tk.IntVar()

                        def create_radio_button(value, text):
                            radio_button = tk.Radiobutton(popup_window, text=text, bg='#D3D3D3', variable=rating_value, value=value)
                            radio_button.pack(anchor=tk.W)

                        # Create radio buttons with star emoji symbols, ranging from 1 to 5
                        emoji_stars = ["★", "★★", "★★★", "★★★★", "★★★★★"]
                        for i, emoji_star in enumerate(emoji_stars):
                            create_radio_button(i + 1, emoji_star)

                        # Add a button to save the rating
                        save_button = tk.Button(popup_window, text="Save Rating", command=save_rating)
                        save_button.pack(pady=5)

                def survey_rank():
                    global userid_entry2

                    apps3 = tk.Tk()
                    apps3.title('Survey Rank')
                    apps3.geometry('925x475+300+200')
                    apps3.config(bg='#D3D3D3')

                    myLabel = tk.Label(apps3, text="Survey Rank", bg='#D3D3D3', font=('Calibri, 15'))
                    myLabel.place(x=400, y=1)

                    connect = sqlite3.connect(database="data.db")
                    conn = connect.cursor()

                    student_id = userid_entry2.get()

                    # Create an SQL query to get the student's course information
                    timetable_query = """
                    SELECT * FROM register 
                    WHERE student_id = ?
                    """
                    conn.execute(timetable_query, [student_id])

                    tree = ttk.Treeview(apps3)
                    tree['show'] = 'headings'

                    font1 = ('Arial', 15, 'bold')
                    font2 = ('Arial', 12, 'bold')

                    style = ttk.Style(apps3)
                    style.theme_use('clam')
                    style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
                    style.map('Treeview', background=[('selected', '#1A8F2D')])

                    tree = ttk.Treeview(apps3, height=20)
                    tree['columns'] = ('class_type', 'subject_name', 'subject_code', 'lecture_name')

                    tree.column('#0', width=0, stretch=tk.NO)  # Hide the default first column
                    tree.column('class_type', anchor=tk.CENTER, width=200)
                    tree.column('subject_name', anchor=tk.CENTER, width=200)
                    tree.column('subject_code', anchor=tk.CENTER, width=200)
                    tree.column('lecture_name', anchor=tk.CENTER, width=200)

                    tree.heading('class_type', text='Type', anchor=tk.CENTER)
                    tree.heading('subject_name', text='Subject', anchor=tk.CENTER)
                    tree.heading('subject_code', text='Subject code', anchor=tk.CENTER)
                    tree.heading('lecture_name', text='Lecture name', anchor=tk.CENTER)

                    tree.place(x=50, y=25)

                    i = 0
                    for ro in conn:
                        tree.insert('', i, text=" ", values=(ro[5], ro[2], ro[3], ro[6]))

                    # Bind the function to open the rating popup window to the Treeview item selection event
                    tree.bind('<ButtonRelease-1>', lambda event: open_rating_popup(tree.item(tree.selection())['values'][1], tree.item(tree.selection())['values'][3], student_id))

                    apps3.mainloop()

                def student_list_in_class():
                    def get_classes_from_register():
                        conn = sqlite3.connect('data.db')
                        cursor = conn.cursor()

                        global userid_entry2
                        student_id = userid_entry2.get()

                        # 查询学生已注册的班级
                        cursor.execute('''
                            SELECT DISTINCT register.classes
                            FROM register
                            WHERE register.student_id = ?
                        ''', (student_id,))

                        classes = [row[0] for row in cursor.fetchall()]

                        conn.close()

                        return classes

                    def get_students_registered_for_class(selected_class):
                        global userid_entry2  # 声明全局变量
                        conn = sqlite3.connect('data.db')
                        cursor = conn.cursor()

                        # 获取当前学生的ID
                        student_id = userid_entry2.get()

                        # 查询学生是否注册了选定的班级
                        cursor.execute('''
                            SELECT users.userid, users.username
                            FROM users
                            INNER JOIN register ON users.userid = register.student_id
                            WHERE register.classes = ? 
                        ''', (selected_class,))

                        registered_students = cursor.fetchall()

                        conn.close()

                        return registered_students


                    def show_students_for_selected_class():
                        selected_class = classes_combobox.get()
                        if not selected_class:
                            return

                        registered_students = get_students_registered_for_class(selected_class)

                        if registered_students:
                            result_tree.delete(*result_tree.get_children())  # Clear Treeview content
                            for student in registered_students:
                                result_tree.insert('', 'end', values=(student[0], student[1]))
                            
                            # 设置第一列的标题为 "Student ID"
                            result_tree.heading('#1', text='Student ID')
                        else:
                            messagebox.showinfo("Message", "No students are registered for this class.")



                    app111 = tk.Tk()
                    app111.title('Student List In Class')

                    # Configure the style
                    style = ttk.Style(app111)
                    style.theme_use('clam')
                    style.configure('Treeview', font=('Arial', 12, 'bold'), foreground='#fff', background='#000', fieldbackground='#313837')
                    style.map('Treeview', background=[('selected', '#1A8F2D')])

                    # Get all classes and create a combobox
                    classes_from_register = get_classes_from_register()
                    classes_combobox = ttk.Combobox(app111, values=classes_from_register)
                    classes_combobox.pack()

                    search_button = tk.Button(app111, text='Search', command=show_students_for_selected_class)
                    search_button.pack()

                    # Create Treeview to display student list
                    result_tree = ttk.Treeview(app111, columns=('Student ID', 'Student Name'))
                    result_tree.heading('#1', text='Student ID')
                    result_tree.heading('#2', text='Student Name')
                    result_tree.pack()

                    # Hide the first column
                    result_tree.column('#0', width=0, stretch=tk.NO)

                    app111.mainloop()

                                                 
                button_frame = LabelFrame(root60,text="Click Here ...",bg="#ECECEC", padx=80, pady=60)
                button_frame.place(x=40,y=70)

                timetable_button =Button(button_frame, text="View Timetable",command=view_timetable, fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=25,height=2)
                browse_button =Button(button_frame, text="View Courses Offered", command=browse_course, fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=25,height=2)
                register_button =Button(button_frame, text="Register Courses",command=register_course_page, fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=25,height=2)
                survey_button =Button(button_frame, text="Survey Rank", command=survey_rank, fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=25,height=2)
                student_list_button =Button(button_frame, text="Class Student List",command=student_list_in_class, fg='#fff', bg='#3F3F3F', font=('Arial', 16),relief='raised', borderwidth=2, cursor='hand2',width=25,height=2)

                timetable_button.grid(row=0, column=0, padx=15, pady=10)
                browse_button.grid(row=0, column=1, padx=15, pady=10)
                register_button.grid(row=1, column=0, padx=15, pady=10)
                survey_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="n")
                student_list_button.grid(row=1, column=1, padx=15, pady=10)

                # Add a Logout button to go back to the login page
                logout_button = Button(root60, text='Logout', command=lambda: logout_and_show_login(root60),fg='#fff', bg='#E40404', relief='raised', borderwidth=2, cursor='hand2', width=15)
                logout_button.place(x=10,y=5)
            else:
                messagebox.showerror('Error', 'Invalid username or password !')
        else:
            messagebox.showerror('Error', 'Invalid username or password !')

frame2 = Frame(root, bg='#D3D3D3', width=925, height=475.545)
frame2.place(x=0, y=0)

img = Image.open('Mini IT Project/MMU_LOGO.PNG')
resized = img.resize((398, 332))
new_pic = ImageTk.PhotoImage(resized)
Label(frame2, image=new_pic, bg='#D3D3D3').place(x=50, y=60)

loginlabel2 = Label(frame2, text='SIGN IN', fg='#57a1f8', bg='#D3D3D3', font=('Microsoft YaHei UI Light', 25, 'bold'))
loginlabel2.place(x=620, y=60)

userid_entry2_label = Label(frame2, text='User ID:', fg='black', bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11,'bold'))
userid_entry2_label.place(x=537, y=145)
userid_entry2 = Entry(frame2, width=25, fg='Black', border=0, bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
userid_entry2.place(x=540, y=170)
Frame(frame2, width=295, height=2, bg='black').place(x=536, y=195)

password_entry2_label = Label(frame2, text='Password:', fg='black', bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11,'bold'))
password_entry2_label.place(x=537, y=215)
password_entry2 = Entry(frame2, width=25, fg='Black', border=0, bg='#D3D3D3', font=('Microsoft YaHei UI Light', 11))
password_entry2.place(x=540, y=240)
password_entry2.config(show='●')
Frame(frame2, width=295, height=2, bg='black').place(x=536, y=265)

def toggle_password_visibility():
    if show_password_var2.get():
        password_entry2.config(show='')
    else:
        password_entry2.config(show='●')

show_password_var2 = IntVar()
show_password_var2.set(0)  # Initially set to hide password
toggle_radio2 = Checkbutton(frame2, text='', variable=show_password_var2, bg="#D3D3D3", command=toggle_password_visibility)
toggle_radio2.place(x=800, y=240)

loginbtn = Button(frame2, command=login,  bg='#57a1f8', fg='white', border=0, text='LOG IN', cursor='hand2', width=33, pady=5)
loginbtn.place(x=565, y=310)

root.mainloop()

