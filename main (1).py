import smtplib
import ssl
import random
from email.message import EmailMessage
import flet
import sqlite3
from datetime import datetime

from flet import Text, AlertDialog, ListTile
from flet import Icon,Icons
from flet import TextField, ElevatedButton, Image, View, Column, Row, Icon, Icons, Tabs, Tab, Container, alignment
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

DB_NAME="pharmacy.db"

# ---------------------- Database Setup ----------------------
def create_db():
    conn=sqlite3.connect(DB_NAME)
    c=conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS medicines (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        quantity INTEGER,
        expiry_date TEXT,
        price REAL
    )''')
    conn.commit()
    conn.close()


def add_medicine(name, quantity, expiry_date, price):
    conn=sqlite3.connect(DB_NAME)
    c=conn.cursor()
    c.execute("INSERT INTO medicines (name, quantity, expiry_date, price) VALUES (?, ?, ?, ?)",
              (name, quantity, expiry_date, price))
    conn.commit()
    conn.close()


def get_all_medicines():
    conn=sqlite3.connect(DB_NAME)
    c=conn.cursor()
    c.execute("SELECT * FROM medicines")
    results=c.fetchall()
    conn.close()
    return results


def search_medicine(query):
    conn=sqlite3.connect(DB_NAME)
    c=conn.cursor()
    c.execute("SELECT * FROM medicines WHERE name LIKE ?", ('%' + query + '%',))
    results=c.fetchall()
    conn.close()
    return results





from flet import (
    Page, Container, Text, Row, Column, ElevatedButton,
    Icon, Icons, padding, alignment, Image, View, Tabs, Tab, TextField, Ref
)

# Global variable to store OTP
otp_variable=None

# Function to generate OTP
def otp_generate():
    otp=random.randint(100000, 999999)
    print(otp)  # Debugging print to check the generated OTP
    return otp

# Function to send OTP via email
def send_otp_email(user_email, otp):
    email_sender='dynamicdeveloper250@gmail.com'  # Your email
    email_passw='nvaxnpqmfilbindp'  # Your email password
    email_receiver=user_email.lower().strip()

    subject='Your QuickMeds App Login One-Time Password (OTP)'
    body=f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Your QuickMeds App Login One-Time Password (OTP)</title>
    </head>
    <body>
        <p><strong>Dear QuickMeds User,</strong></p>
        <p>Welcome to <strong>QuickMeds</strong>! As part of our secure login process, here is your One-Time Password (OTP) for logging in:</p>
        <p><strong>Your OTP: {otp}</strong></p>
        <p>Please enter the OTP on the login screen of the <strong>QuickMeds</strong> app to complete the login process.</p>
        <p><strong>Security Reminder:</strong> To ensure the safety of your account, please refrain from sharing this OTP with anyone else.</p>
        <p>If you encounter any issues during login or have any questions, don't hesitate to contact our support team.</p>
        <p><strong>Welcome to QuickMeds Community,</strong><br><strong>QuickMeds admin team</strong></p>
    </body>
    </html>
    """
    em=EmailMessage()
    em['From']='QuickMeds+'
    em['To']=email_receiver
    em['subject']=subject
    em.set_content(body, subtype='html')

    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_passw)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        print(f"OTP sent to {email_receiver}")

# Main Flet App
def app(page: Page):
    global otp_variable  # Access the global OTP variable
    page.title="QuickMeds+"
    page.padding=padding.only(top=50, left=10, right=10)
    page.bgcolor='white'
    page.theme_mode='dark'
    


    page.scroll=True
    email_ref=Ref[TextField]()  # Reference for the email field
    otp_ref=Ref[TextField]()    # Reference for the OTP field

    # Handle OTP request (sending OTP)
    def handle_login_click(page, email_ref):
        global otp_variable  # Access the global variable
        email=email_ref.current.value
        if len(email) < 2 or "@" not in email or '.' not in email:
            print("Please enter a valid email address.")

        else:
            otp_variable=otp_generate()  # Generate OTP
            send_otp_email(email, otp_variable)  # Send OTP to the email
            print(f"OTP sent successfully. Generated OTP: {otp_variable}")  # Debugging print
            page.go('/enter_otp')  # Navigate to OTP entry page

    # Handle OTP verification
    def verify_otp(page, otp_ref):
        entered_otp=otp_ref.current.value
        print(f"Entered OTP: {entered_otp}, Generated OTP: {otp_variable}")  # Debugging print
        if entered_otp==str(otp_variable):  # Compare with global OTP
            print("OTP verified successfully.")
            page.go('/loggedin')  # Navigate to logged-in page
        else:
            print("Invalid OTP entered. Please try again.")  # Show error message for invalid OTP



    def add_view(page: Page):

        name=TextField(label="Medicine Name",color='black')
        qty=TextField(label="Quantity", keyboard_type="NUMBER",color='black')
        exp=TextField(label="Expiry Date (YYYY-MM-DD)",color='black')
        price=TextField(label="Price", keyboard_type="NUMBER",color='black')
        msg=Text(color='black')
        dlg=AlertDialog(title=Text("Added"),content=Text("Medicine added successfully!"),alignment=alignment.center,on_dismiss=lambda e: print("Dialog dismissed!"),title_padding=padding.all(25),)
        page.dialog=dlg  
        page.overlay.append(dlg)
        def save(e):
            try:
                add_medicine(name.value, int(qty.value), exp.value, float(price.value))
                # msg.value="Medicine added successfully!"
                page.update()  
                if int(qty.value) <= 5:
                    dlg.title.value="Warning"
                    dlg.content.value=f"Stock for '{name.value}' is low (only {qty.value} left)!"  

                    dlg.open=True
                    page.update()
                else:
                    dlg.title.value="Added"
                    dlg.content.value=f"Medicine added successfully" 
                    dlg.open=True
                    page.update()
            except Exception as ex:
                msg.value=f"Error adding medicine: Please fill all boxes"  
            page.update()

        return Column(
            controls=[
                Text("Add Medicine", size=20, weight="bold", color='black'),
                name, qty, exp, price,
                ElevatedButton("Save", on_click=save), 
                msg
            ]
        )

    def view_view():
        search_field=TextField(label="Search Medicine",color='black')
        result_column=Column()

        def search(e):
            result_column.controls.clear()
            data=search_medicine(search_field.value)
            for med in data:
                status="Out of Stock" if med[2]==0 else ("Low" if med[2] <= 5 else "Available")
                result_column.controls.append(
                    # Text(f"{med[1]} | Qty: {med[2]} | Exp: {med[3]} | ₹{med[4]} | Status: {status}",color='black')
                
                ListTile(
        title=Text(f"Name:{med[1]}", color='black'),
        subtitle=Text(f"Qty: {med[2]} Exp: {med[3]}", color='black'),
        leading=Icon(name=Icons("health_and_safety"),color='green'),

        content_padding=10,
        dense=True # chota kardeta pure element ku
        

        ))
            page.update()

        return Column(
    controls=[
        Text("Inventory List", size=20, weight="bold", color='black'),
        search_field,
        ElevatedButton("Search", on_click=search),
        Column(
            controls=[result_column],  
            scroll=True  
        ),
    ]
)






    def change_route(route):
        if page.route=='/':
            logo=Image(src="logo.png", fit='cover',width=200, border_radius=30)
            text=Text("QuickMeds+", size=36, color='green', font_family='Georgia')
            button=ElevatedButton(
                text="Get in", elevation=10,
                icon=Icon(name=Icons("login"), color="black"),
                # icon=Icons.LOGIN, icon_color='gray',
                on_click=lambda e: e.page.go('/login')
            )
            view=View(
                bgcolor='white',
                route='/',
                controls=[Container(
                    alignment=alignment.center,
                    content=Column(
                        alignment=alignment.center,
                        horizontal_alignment='center',
                        controls=[logo, text, button]
                    ),
                    expand=True
                )]
            )
            page.views.append(view)
            page.update()

        elif page.route=='/login':
            tab=Tabs(
                indicator_color="black",
                label_color="black",
                tabs=[Tab(
                    text='Log in',
                    content=Column(
                        alignment=alignment.center,
                        horizontal_alignment='center',
                        controls=[
                            Text(height=1),
                            TextField(
                                ref=email_ref,
                                content_padding=10,
                                text_size=18,
                                color='black',
                                border_color='white',
                                icon=Icon(name=Icons("email"), color="black"),
                                label='Email',
                                keyboard_type='TEXT'
                            ),
                            ElevatedButton(
                                content=Row(
                                    alignment='center',
                                    controls=[Text(value="Send OTP")]
                                ),
                                bgcolor='#282828',
                                on_click=lambda e: handle_login_click(page, email_ref)  
                            )
                        ]
                    )
                )],
                selected_index=0,
                animation_duration=700,
                on_change=lambda e: print("Tab changed!")
            )
            view=View(route='/login', bgcolor='white', controls=[tab])
            page.views.append(view)
            page.update()

        elif page.route=='/enter_otp':
            otp_tab=Tabs(
                indicator_color="black",
                label_color="black",
                tabs=[Tab(
                    text='Enter OTP',
                    content=Column(
                        alignment=alignment.center,
                        horizontal_alignment='center',
                        controls=[
                            Text(height=1),
                            TextField(
                                ref=otp_ref,
                                content_padding=10,
                                text_size=18,
                                color='black',
                                border_color='white',
                                icon=Icon(name=Icons("lock"), color="black"),
                                max_length=6,
                                label='OTP',
                                keyboard_type='TEXT'
                            ),
                            ElevatedButton(
                                content=Row(
                                    alignment='center',
                                    controls=[Text(value="Verify OTP")]
                                ),
                                bgcolor='#282828',
                                on_click=lambda e: verify_otp(page, otp_ref)  # Handle OTP verification
                            )
                        ]
                    )
                )],
                selected_index=0,
                animation_duration=700,
                on_change=lambda e: print("Tab changed!")
            )
            view=View(route='/enter_otp', bgcolor='white', controls=[otp_tab])
            page.views.append(view)
            page.update()

        elif page.route=='/loggedin':
            view=View(
                route='/loggedin',
        bgcolor='white',
        controls=[Column(
            alignment=alignment.center,

            controls=[
                # Add the Add Medicine and View Inventory tabs here
                Tabs(indicator_color="black",
                label_color="black",

                    tabs=[
                        Tab(
                            text="Add Medicine",
                            content=add_view(page),
                        ),
                        Tab(
                            text="View Inventory",
                            content=view_view()
                        ),
                    ],

                    selected_index=0,  # Default tab (Add Medicine)
                    animation_duration=700,
                    on_change=lambda e: page.update()  # Trigger page update when switching tabs
                ),
                # Logout button
                ElevatedButton(
                    text="Logout",
                    icon=Icon(name=Icons("logout"), color="black"),
                    # icon=Icons.LOGOUT,
                    on_click=lambda e: page.go("/")
                ),
            ]
        )]
    )
            page.views.append(view)
            page.update()


        page.update()

    def last_visited_page(e):
        page.views.pop()
        if page.views:
            top_view=page.views[-1]
            page.go(top_view.route)

    page.on_route_change=change_route
    page.on_view_pop=last_visited_page
    page.go(page.route)
    page.update()


flet.app(target=app, assets_dir='assets')
