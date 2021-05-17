# Written by n0miya (Dulapah Vibulsanti)
from firebase_admin import credentials, db
import firebase_admin

# Authenticate Firebase database
cred = credentials.Certificate('data/acemath-n0miya-firebase-adminsdk-yft0t-e8061fb0b1.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://acemath-n0miya-default-rtdb.asia-southeast1.firebasedatabase.app/'
})


# Create new user in Firebase database
def create_new_user(user_name, user_password):
    user = db.reference('Users')
    user.child(user_name).set({
        'Key': user_password,
        'Gender': 0,
        'TimesPlayed': {
            'Easy': 0,
            'Normal': 0,
            'Hard': 0,
            'Expert': 0,
        },
        'FastestTime': {
            'Easy': "00.00s",
            'Normal': "00.00s",
            'Hard': "00.00s",
            'Expert': "00.00s",
            'EasyValue': 999999999,
            'NormalValue': 999999999,
            'HardValue': 999999999,
            'ExpertValue': 999999999,
        }
    })


# Write data to Firebase database
def write_to_firebase(user_name, child, data):
    user = db.reference('Users')
    user.child(user_name).update({
        child: data,
    })


# Get sum of TimesPlayed of user
def sum_times_played(user_name):
    easy = db.reference('Users/' + str(user_name) + '/TimesPlayed/Easy').get()
    normal = db.reference('Users/' + str(user_name) + '/TimesPlayed/Normal').get()
    hard = db.reference('Users/' + str(user_name) + '/TimesPlayed/Hard').get()
    expert = db.reference('Users/' + str(user_name) + '/TimesPlayed/Expert').get()
    sum_played = easy + normal + hard + expert
    return str(sum_played)


# Read data from data.txt
def read_data(line):
    file = open('data/data.txt', "r")
    content = file.readlines()
    data = (content[line])
    file.close()
    return data.rstrip('\n')


# Write data to data.txt
def write_data(line, data):
    file = open('data/data.txt', "r")
    content = file.readlines()
    content[line] = str(data) + "\n"
    file = open("data/data.txt", "w")
    file.writelines(content)
    file.close()


# Hide canvas
def hide_canvas(canvas):
    canvas.pack_forget()


# Show canvas
def show_canvas(canvas):
    canvas.pack()


# Hide widget
def hide_widget(widget):
    widget.place_forget()


# Show widget
def show_widget(widget, x_coordinate, y_coordinate):
    widget.place(x=x_coordinate, y=y_coordinate)
