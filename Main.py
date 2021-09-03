#=============================================#
# Written by Dulapah Vibulsanti (64011388)    #
#                                             #
# Please run these commands in terminal!      #
# pip install Pillow                          #
# pip install firebase-admin                  #
# pip install stopwatch.py                    #
#=============================================#
import tkinter
import random
import winsound
import firebase_admin
from tkinter import font
from tkinter import *
from PIL import ImageTk, Image
from stopwatch import Stopwatch  # https://pypi.org/project/stopwatch.py/
from firebase_admin import credentials, db


stopwatch = Stopwatch()  # Initialize stopwatch variable

# Authenticate Firebase database
cred = credentials.Certificate('data/acemath-n0miya-firebase-adminsdk-yft0t-e8061fb0b1.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://acemath-n0miya-default-rtdb.asia-southeast1.firebasedatabase.app/'})


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


# Search and get value in data.txt
def read_data(string_to_search):
    lineNumber = 0
    with open("data/data.txt", 'r') as read_obj:
        for line in read_obj:
            lineNumber += 1
            if string_to_search in line:
                value = line.rstrip()
    read_obj.close()
    return value.removeprefix(string_to_search + " = ")


# Search and replace value in data.txt
def write_data(string_to_search, value):
    lineNumber = 0
    with open("data/data.txt", 'r') as read_obj:
        filedata = read_obj.read()
        filedata = filedata.replace(string_to_search + " = " + read_data(string_to_search), string_to_search + " = " + str(value))
    with open("data/data.txt", 'w') as read_obj:
        read_obj.write(filedata)
    read_obj.close()


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
    widget.place(x = x_coordinate, y = y_coordinate)


# Toggle fullscreen when user presses F11 key
def fullscreen(event):
    if not MainWindow.attributes('-fullscreen'):
        MainWindow.attributes('-fullscreen', True)
    else:
        MainWindow.attributes('-fullscreen', False)


# Show/Hide widgets and canvases when user moves from MainMenu
def out_main_menu():
    hideWidgetList = [play_button, sync_button, profile_button, about_button, exit_button, exit_confirm, exit_no_button, exit_yes_button]
    for widget in hideWidgetList:
        hide_widget(widget)
    show_widget(back_button, 80, 20)
    hide_canvas(BGFullCanvas)
    show_canvas(BGCanvas)


# Show/Hide widgets and canvases when user moves to MainMenu
def to_main_menu(event):
    if read_data("isUserInGame") == "True":
        stopwatch.stop()
        hideWidgetList = [pre_countdown, rand_int_text, user_answer]
        for widget in hideWidgetList:
            hide_widget(widget)
        showWidgetList = [[account_prompt, 500, 380], [cancel_game, 550, 480], [cancel_game_yes, 700, 683], [cancel_game_no, 1015, 683]]
        for widget in range(len(showWidgetList)):
            show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        write_data("isStopwatchPaused", "True")
        user_answer.config(state = "disabled")
        hide_widget(diag_box)
    else:
        hideWidgetList = [go_to_sync, sync_prompt, offline_button, back_button, account_prompt, account_text, offline_button, create_button,
                        login_button, logout_prompt, logout_button, cancel_logout_button, diag_box, profile_name, profile_stat, profile_stat_game,
                        male_profile_pic, female_profile_pic, change_gender_button, select_difficulty, easy_difficulty_button, normal_difficulty_button,
                        hard_difficulty_button, expert_difficulty_button]
        for widget in hideWidgetList:
            hide_widget(widget)
        showWidgetList = [[play_button, 80, 425], [sync_button, 80, 558], [profile_button, 80, 690], [about_button, 80, 810], [exit_button, 80, 923]]
        for widget in range(len(showWidgetList)):
            show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        hide_canvas(BGCanvas)
        hide_canvas(AboutCanvas)
        show_canvas(BGFullCanvas)   


# If user press Back button in Auth
def back_auth(event):
    hideWidgetList = [login_auth, back_auth_button, auth_message, username, password, create_acc, password_confirm]
    for widget in hideWidgetList:
        hide_widget(widget)
    showWidgetList = [[create_button, 700, 683], [login_button, 1015, 683], [account_text, 520, 400], [back_button, 80, 20]]
    for widget in range(len(showWidgetList)):
        show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
    username.delete(0, 'end')  # clear entered field
    password.delete(0, 'end')
    password_confirm.delete(0, 'end')
    write_data("isUserInCredentialScreen", "False")


# When user presses Play button
def play(event):
    out_main_menu()
    # If not login, player only have choice to play offline or go back to Sync menu
    if read_data("isFirebaseConnected") == "False":
        showWidgetList = [[account_prompt, 500, 380], [sync_prompt, 520, 400], [go_to_sync, 1015, 683], [offline_button, 700, 683]]
        for widget in range(len(showWidgetList)):
            show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
    else:
        difficulty_select(event)


# When user presses Sync button
def sync(event):
    out_main_menu()
    # Prompt user to choose whether they want to create an account, connect to existing account, or play offline
    if read_data("isFirebaseConnected") == "False":
        hideWidgetList = [go_to_sync, sync_prompt, offline_button]
        for widget in hideWidgetList:
            hide_widget(widget)
        showWidgetList = [[account_prompt, 500, 380], [account_text, 520, 400], [create_button, 700, 683], [login_button, 1015, 683]]
        for widget in range(len(showWidgetList)):
            show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
    else:
        showWidgetList = [[account_prompt, 500, 380], [logout_prompt, 555, 500], [logout_button, 700, 683], [cancel_logout_button, 1015, 683]]
        for widget in range(len(showWidgetList)):
            show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])


# When user presses Profile button
def profile(event):
    if read_data("isFirebaseConnected") == "False":
        showWidgetList = [[account_prompt, 500, 380], [no_sync, 650, 550], [ok_button, 860, 683]]
        for widget in range(len(showWidgetList)):
            show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
    else:
        out_main_menu()
        showWidgetList = [[diag_box, 227, 200], [profile_name, 1000, 250], [profile_stat, 1000, 400], [profile_stat_game, 1245, 400], 
                        [change_gender_button, 248, 840]]
        for widget in range(len(showWidgetList)):
            show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        profile_name.config(text=read_data("firebaseUsername"))
        profile_stat_game.config(text=sum_times_played(read_data("firebaseUsername")) + "\n" + 
            str(db.reference('Users/' + read_data("firebaseUsername") + '/TimesPlayed/Easy').get()) + " (Fastest : " + 
            str(db.reference('Users/' + read_data("firebaseUsername") + '/FastestTime/Easy').get()) + ")" + "\n" +
            
            str(db.reference('Users/' + read_data("firebaseUsername") + '/TimesPlayed/Normal').get()) + " (Fastest : " + 
            str(db.reference('Users/' + read_data("firebaseUsername") + '/FastestTime/Normal').get()) + ")" + "\n" +
            
            str(db.reference('Users/' + read_data("firebaseUsername") + '/TimesPlayed/Hard').get()) + " (Fastest : " + 
            str(db.reference('Users/' + read_data("firebaseUsername") + '/FastestTime/Hard').get()) + ")" + "\n" +
            
            str(db.reference('Users/' + read_data("firebaseUsername") + '/TimesPlayed/Expert').get()) + " (Fastest : " + 
            str(db.reference('Users/' + read_data("firebaseUsername") + '/FastestTime/Expert').get()) + ")" + "\n")
        if str(db.reference('Users/' + read_data("firebaseUsername") + '/Gender').get()) == "0":
            show_widget(male_profile_pic, 300, 300)
        else:
            show_widget(female_profile_pic, 300, 300)


# When user presses About button
def about(event):
    out_main_menu()
    hide_canvas(BGCanvas)
    show_canvas(AboutCanvas)
    show_widget(back_button, 80, 20)
    back_button.lift()


# When user presses Exit button
def close_confirmation(event):
    showWidgetList = [[exit_confirm, 525, 450], [exit_yes_button, 720, 570], [exit_no_button, 1000, 570]]
    for widget in range(len(showWidgetList)):
        show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
    exit_confirm.lift()
    exit_yes_button.lift()
    exit_no_button.lift()


# Close the game
def close(event):
    MainWindow.destroy()


# Close the exit confirmation dialog and return to MainMenu
def cancel(event):
    hide_widget(exit_confirm)
    hide_widget(exit_yes_button)
    hide_widget(exit_no_button)


# If user selects play offline
def play_offline(event):
    difficulty_select(event)


# If user selects register account
def create_account(event):
    if read_data("isUserInCredentialScreen") == "False":
        hideWidgetList = [offline_button, login_button, account_text, back_button]
        for widget in hideWidgetList:
            hide_widget(widget)
        showWidgetList = [[create_button, 1188, 683], [create_acc, 520, 470], [back_auth_button, 520, 400], [username, 900, 470], 
                        [password, 900, 535], [password_confirm, 900, 602]]
        for widget in range(len(showWidgetList)):
            show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        write_data("isUserInCredentialScreen", "True")
    else:
        # Check login credential
        show_widget(auth_message, 520, 683)
        if username.get() == "" or password.get() == "" or password_confirm.get() == "":
            auth_message.config(text = "Please complete all required fields.", fg = "red")
        elif password.get() != password_confirm.get():
            auth_message.config(text = "Passwords did not match. Try again.", fg = "red")
        elif str(db.reference('Users/' + username.get()).get()) != "None":
            auth_message.config(text = "This username is already taken.", fg = "red")
        else:
            create_new_user(username.get(), password.get())
            hide_widget(create_button)
            auth_message.config(text="Account created successfully. Please go back and click on Login.", fg = "green")


# If user selects login account
def login_account(event):
    if read_data("isUserInCredentialScreen") == "False":
        hideWidgetList = [offline_button, create_button, account_text, back_button]
        for widget in hideWidgetList:
            hide_widget(widget)
        showWidgetList = [[login_button, 1188, 683], [login_auth, 590, 520], [back_auth_button, 520, 400], [username, 820, 520], [password, 820, 585]]
        for widget in range(len(showWidgetList)):
            show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        write_data("isUserInCredentialScreen", "True")
    else:
        # Check login credential
        show_widget(auth_message, 520, 683)
        user = db.reference('Users/' + username.get())
        key = db.reference('Users/' + username.get() + '/Key')
        if username.get() == "" or password.get() == "":
            auth_message.config(text="Please complete all required fields.", fg = "red")
        elif user.get() == "None" or key.get() != password.get():
            auth_message.config(text="Username or password is incorrect. Try again.", fg = "red")
        else:
            hideWidgetList = [auth_message, login_button, login_auth, back_auth_button, username, password]
            for widget in hideWidgetList:
                hide_widget(widget)
            show_widget(ok_button, 860, 683)
            show_widget(login_success, 800, 420)
            write_data("isFirebaseConnected", "True")
            write_data("firebaseUsername", username.get())
            write_data("isUserInCredentialScreen", "False") 
            login_success.config(text = "Login successful! \n\n  Username : " + username.get() + "\nHave a nice day!", fg = "green")
            username.delete(0, 'end')
            password.delete(0, 'end')


# Clear login data and parameter
def logout(event):
    write_data("isUserInCredentialScreen", "False")
    write_data("firebaseUsername", "null")
    write_data("isFirebaseConnected", "False")
    to_main_menu(event)


# When user press Ok
def ok(event):
    hideWidgetList = [ok_button, no_sync, account_prompt, login_success]
    for widget in hideWidgetList:
        hide_widget(widget)
    to_main_menu(event)


# Change gender
def change_gender(event):
    if str(db.reference('Users/' + read_data("firebaseUsername") + '/Gender').get()) == "0":
        show_widget(female_profile_pic, 300, 300)
        hide_widget(male_profile_pic)
        write_to_firebase(read_data("firebaseUsername"), "Gender", 1)
    else:
        show_widget(male_profile_pic, 300, 300)
        hide_widget(female_profile_pic)
        write_to_firebase(read_data("firebaseUsername"), "Gender", 0)


# Prompt user to select difficulty
def difficulty_select(event):
    hideWidgetList = [account_prompt, sync_prompt, go_to_sync, offline_button]
    for widget in hideWidgetList:
        hide_widget(widget)
    showWidgetList = [[diag_box, 227, 200], [select_difficulty, 289, 254], [easy_difficulty_button, 315, 418], 
                    [normal_difficulty_button, 650, 418], [hard_difficulty_button, 986, 418], [expert_difficulty_button, 1322, 418]]
    for widget in range(len(showWidgetList)):
            show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])


# When user want to go to MainMenu while game is in progress
def prompt_exit(event):
    hideWidgetList = [diag_box, pre_countdown, user_answer, rand_int_text, account_prompt, cancel_game, cancel_game_yes, cancel_game_no]
    for widget in hideWidgetList:
        hide_widget(widget)
    write_data("isUserInGame", "False")
    write_data("isStopwatchPaused", "False")
    write_data("isGameStarted", "False")
    winsound.PlaySound('data/sounds/BGMusic.wav', winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
    to_main_menu(event)


# When user decline to go to MainMenu while game is in progress
def prompt_exit_cancel(event):
    hideWidgetList = [account_prompt, cancel_game, cancel_game_yes, cancel_game_no]
    for widget in hideWidgetList:
        hide_widget(widget)
    show_widget(rand_int_text, 400, 350)
    show_widget(diag_box, 227, 200)
    if read_data("isGameStarted") == "True":
        show_widget(user_answer, 670, 750)
        show_widget(pre_countdown, 900, 215)
        user_answer.config(state = 'normal')
    else:
        show_widget(pre_countdown, 580, 520)
    write_data("isStopwatchPaused", "False") 
    stopwatch.start()


# If user select easy gamemode
def easy_gamemode(event):
    write_data("selectedDifficulty", "Easy")
    write_data("questionSize", 19)
    write_data("integerSize", 1)
    start_game()


# If user select normal gamemode
def normal_gamemode(event):
    write_data("selectedDifficulty", "Normal")
    write_data("questionSize", 19)
    write_data("integerSize", 2)
    start_game()


# If user select hard gamemode
def hard_gamemode(event):
    write_data("selectedDifficulty", "Hard")
    write_data("questionSize", 19)
    write_data("integerSize", 3)
    start_game()


# If user select expert gamemode
def expert_gamemode(event):
    write_data("selectedDifficulty", "Expert")
    write_data("questionSize", 19)
    write_data("integerSize", 4)
    start_game()


# Countdown
def countdown_timer(t):
    winsound.PlaySound(None, winsound.SND_PURGE)
    show_widget(pre_countdown, 580, 520)
    while t >= 0:
        if read_data("isStopwatchPaused") == "False":
            MainWindow.after(1000)
            pre_countdown.config(text = "Game will start in " + str(t) + " seconds!\nPress 'ENTER' to submit answer", fg = "black")
            t -= 1
        MainWindow.update()  # Prevent Tkinter from locking up
    if read_data("isStopwatchPaused") == "False":
        stopwatch.restart()
        user_answer.config(state = 'normal')
        show_widget(back_button, 80, 20)
        write_data("isGameStarted", "True")
        winsound.PlaySound('data/sounds/GameStart.wav', winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)


# Game start
def start_game():
    hideWidgetList = [select_difficulty, easy_difficulty_button, normal_difficulty_button, hard_difficulty_button, expert_difficulty_button, back_button]
    for widget in hideWidgetList:
        hide_widget(widget)
    write_data("isUserInGame", "True")
    write_data("currentQuestionNumber", 0)
    countdown_timer(5)
    summon_question()


# Create questions based on difficulty
def summon_question():
    integer_size = read_data("integerSize")
    if integer_size == "1":
        write_data("minInteger", 0)
        write_data("maxInteger", 9)
    elif integer_size == "2":
        write_data("minInteger", 10)
        write_data("maxInteger", 99)
    elif integer_size == "3":
        write_data("minInteger", 100)
        write_data("maxInteger", 999)
    elif integer_size == "4":
        write_data("minInteger", 1000)
        write_data("maxInteger", 9999)
    summon_integer()


# Create sets of integers for questions
def summon_integer():
    if int(read_data("currentQuestionNumber")) <= int(read_data("questionSize")):
        show_widget(user_answer, 670, 750)
        show_widget(rand_int_text, 400, 350)
        user_answer.focus()
        min_integer = int(read_data("minInteger"))
        max_integer = int(read_data("maxInteger"))
        int1 = random.randint(min_integer, max_integer)
        int2 = random.randint(min_integer, max_integer)
        rand_int_text.config(text = str(int1) + " + " + str(int2))
        write_data("answer", int1 + int2)
        show_widget(pre_countdown, 900, 215)
        q_number = read_data("currentQuestionNumber")
        q_number_f = int(q_number) + 1
        q_number_all = read_data("questionSize")
        q_number_all_f = int(q_number_all) + 1
        pre_countdown.config(text = str(q_number_f) + "/" + str(q_number_all_f), anchor = "e")
    else:  # Game finishes
        hideWidgetList = [back_button, rand_int_text, user_answer]
        for widget in hideWidgetList:
            hide_widget(widget)
        stopwatch.stop()
        winsound.PlaySound('data/sounds/GameFinish.wav', winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
        write_data("currentQuestionNumber", 0)
        write_data("isUserInGame", "False")
        write_data("isGameStarted", "False")
        show_widget(finish_game, 840, 770)
        show_widget(pre_countdown, 420, 450)
        pre_countdown.config(text = "Your time is " + str(stopwatch) + "\nKeep on trying!")
        user_answer.delete(0, 'end')
        submit_score()


# Check if user input correct answer
def check_answer(event):
    if user_answer.get() == read_data("answer"):
        write_data("currentQuestionNumber", int(read_data("currentQuestionNumber")) + 1)
        user_answer.delete(0, 'end')
        summon_integer()


# Submit score to Firebase if user already login
def submit_score():
    if read_data("isFirebaseConnected") == "True":
        times_played = db.reference('Users/' + read_data("firebaseUsername") + '/TimesPlayed/' + read_data("selectedDifficulty"))
        played = times_played.get()
        played += 1
        user = db.reference('Users')
        user.update({read_data("firebaseUsername") + '/TimesPlayed/' + read_data("selectedDifficulty"): played,})
        best_time_prev = db.reference('Users/' + read_data("firebaseUsername") + '/FastestTime/' + read_data("selectedDifficulty") + 'Value')
        if stopwatch.duration < best_time_prev.get():
            pre_countdown.config(text="Congratulations!" + "\n" + "Your time is " + str(stopwatch) + "\nNew Record!", fg = "green")
            user.update({
                read_data("firebaseUsername") + '/FastestTime/' + read_data("selectedDifficulty"): str(stopwatch),
                read_data("firebaseUsername") + '/FastestTime/' + read_data("selectedDifficulty") + 'Value': stopwatch.duration
            })


# Go back to MainMenu after game is finished
def ok_result(event):
    hideWidgetList = [diag_box, pre_countdown, finish_game]
    for widget in hideWidgetList:
        hide_widget(widget)
    winsound.PlaySound('data/sounds/BGMusic.wav', winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
    to_main_menu(event)


### Initialize Program ###
MainWindow = Tk()
MainWindow.title('AcΣMαth')
MainWindow.geometry("1920x1080")
MainWindow.attributes('-fullscreen', True)
MainWindow.wm_iconbitmap('data/images/AceMath.ico')
MainWindow.bind('<F11>', fullscreen)
MainWindow.bind('<Escape>', close_confirmation)
winsound.PlaySound('data/sounds/BGMusic.wav', winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
write_data("isUserInCredentialScreen", "False")
write_data("isGameStarted", "False")
write_data("isStopwatchPaused", "False")
write_data("isUserInGame", "False")
write_data("currentQuestionNumber", 0)


### Create background ###
BGFullCanvas = Canvas(MainWindow, width=1920, height=1080)
BGFullCanvas.pack()
BGFull = ImageTk.PhotoImage(Image.open("data/images/BGFull.jpg"))
BGFullCanvas.create_image(0, 0, anchor = NW, image = BGFull)

BGCanvas = Canvas(MainWindow, width = 1920, height = 1080)
BGCanvas.pack()
BG = ImageTk.PhotoImage(Image.open("data/images/BG.jpg"))
BGCanvas.create_image(0, 0, anchor = NW, image = BG)

### Play button ###
PlayButtonBG = PhotoImage(file = "data/images/Play.png")
play_button = Button(MainWindow, width = 274, height = 109, image = PlayButtonBG, borderwidth = 0)
play_button.place(x = 80, y = 425)
play_button.bind('<Button-1>', play)

### Sync button ###
SyncButtonBG = PhotoImage(file = "data/images/Sync.png")
sync_button = Button(MainWindow, width = 276, height = 107, image = SyncButtonBG, borderwidth = 0)
sync_button.place(x = 80, y = 558)
sync_button.bind('<Button-1>', sync)

### Profile button ###
ProfileButtonBG = PhotoImage(file = "data/images/Profile.png")
profile_button = Button(MainWindow, width = 363, height = 94, image = ProfileButtonBG, borderwidth = 0)
profile_button.place(x = 80, y = 690)
profile_button.bind('<Button-1>', profile)

### About button ###
AboutButtonBG = PhotoImage(file = "data/images/About.png")
about_button = Button(MainWindow, width = 335, height = 90, image = AboutButtonBG, borderwidth = 0)
about_button.place(x = 80, y = 810)
about_button.bind('<Button-1>', about)

### Exit button ###
ExitButtonBG = PhotoImage(file = "data/images/Exit.png")
exit_button = Button(MainWindow, width = 252, height = 87, image = ExitButtonBG, borderwidth = 0)
exit_button.place(x = 80, y = 923)
exit_button.bind('<Button-1>', close_confirmation)

### Back button ###
BackButtonBG = PhotoImage(file="data/images/Back.png")
back_button = Button(MainWindow, width = 314, height = 95, image = BackButtonBG, borderwidth = 0)
back_button.bind('<Button-1>', to_main_menu)
hide_widget(back_button)

### About description ###
AboutCanvas = Canvas(MainWindow, width = 1920, height = 1080)
AboutCanvas.pack()
About = ImageTk.PhotoImage(Image.open("data/images/AboutMe.jpg"))
AboutCanvas.create_image(0, 0, anchor = NW, image = About)
hide_canvas(AboutCanvas)

### Exit confirmation dialog ###
ExitConfirmDiagBG = Image.open("data/images/ExitDiag.png")
ExitConfirmBG = ImageTk.PhotoImage(ExitConfirmDiagBG)
exit_confirm = tkinter.Label(image = ExitConfirmBG)
hide_widget(exit_confirm)

ExitYesButtonBG = PhotoImage(file = "data/images/Yes.png")
exit_yes_button = Button(MainWindow, width = 241, height = 61, image = ExitYesButtonBG, borderwidth = 0)
exit_yes_button.bind('<Button-1>', close)
hide_widget(exit_yes_button)

ExitNoButtonBG = PhotoImage(file = "data/images/No.png")
exit_no_button = Button(MainWindow, width = 241, height = 61, image = ExitNoButtonBG, borderwidth = 0)
exit_no_button.bind('<Button-1>', cancel)
hide_widget(exit_no_button)

### Account Prompt ###
AccountPrompDiagBG = Image.open("data/images/AccountPrompt.png")
AccountPrompBG = ImageTk.PhotoImage(AccountPrompDiagBG)
account_prompt = tkinter.Label(image = AccountPrompBG)
hide_widget(account_prompt)

AccountPrompDiagText = Image.open("data/images/AccountPromptText.png")
AccountPrompText = ImageTk.PhotoImage(AccountPrompDiagText)
account_text = tkinter.Label(image = AccountPrompText, borderwidth = 0)
hide_widget(account_text)

OfflineButtonBG = PhotoImage(file = "data/images/Offline.png")
offline_button = Button(MainWindow, width = 239, height = 72, image = OfflineButtonBG, borderwidth = 0)
offline_button.bind('<Button-1>', play_offline)
hide_widget(offline_button)

CreateButtonBG = PhotoImage(file = "data/images/Create.png")
create_button = Button(MainWindow, width = 239, height = 72, image = CreateButtonBG, borderwidth = 0)
create_button.bind('<Button-1>', create_account)
hide_widget(create_button)

LoginButtonBG = PhotoImage(file = "data/images/Login.png")
login_button = Button(MainWindow, width = 239, height = 72, image = LoginButtonBG, borderwidth = 0)
login_button.bind('<Button-1>', login_account)
hide_widget(login_button)

BackAuthButtonBG = PhotoImage(file = "data/images/Back_Account.png")
back_auth_button = Button(MainWindow, width = 62, height = 60, image = BackAuthButtonBG, borderwidth = 0)
back_auth_button.bind('<Button-1>', back_auth)
hide_widget(back_auth_button)

LoginAuthText = Image.open("data/images/LoginAuth.png")
LoginAuth = ImageTk.PhotoImage(LoginAuthText)
login_auth = tkinter.Label(image = LoginAuth, borderwidth = 0)
hide_widget(login_auth)

CreateAccText = Image.open("data/images/CreateAcc.png")
CreateAcc = ImageTk.PhotoImage(CreateAccText)
create_acc = tkinter.Label(image = CreateAcc, borderwidth = 0)
hide_widget(create_acc)

### Get User's credential ###
custom_font = font.Font(family = 'Segoe UI', size = 20)

username = Entry(MainWindow, width = 35)
username['font'] = custom_font
hide_widget(username)

password = Entry(MainWindow, width = 35, show = "*")
password['font'] = custom_font
hide_widget(password)

password_confirm = Entry(MainWindow, width = 35, show = "*")
password_confirm['font'] = custom_font
hide_widget(password_confirm)

auth_message = Label(MainWindow, justify = 'left')
auth_message['font'] = custom_font
hide_widget(auth_message)

login_success = Label(MainWindow, anchor = 'c', justify = 'center')
login_success['font'] = custom_font
login_success.config(font = ("Segoe UI", 28))
hide_widget(login_success)

### Prompt user to sync ###
SyncPromptText = Image.open("data/images/SyncPromptMsg.png")
SyncPrompt = ImageTk.PhotoImage(SyncPromptText)
sync_prompt = tkinter.Label(image = SyncPrompt, borderwidth = 0)
hide_widget(sync_prompt)

GoToSyncBG = PhotoImage(file = "data/images/SyncContinue.png")
go_to_sync = Button(MainWindow, width = 239, height = 72, image = GoToSyncBG, borderwidth = 0)
go_to_sync.bind('<Button-1>', sync)
hide_widget(go_to_sync)

### Prompt user to logout ###
LogoutPromptText = Image.open("data/images/LogoutPrompt.png")
LogoutPrompt = ImageTk.PhotoImage(LogoutPromptText)
logout_prompt = tkinter.Label(image = LogoutPrompt, borderwidth = 0)
hide_widget(logout_prompt)

logout_button = Button(MainWindow, width = 241, height = 61, image = ExitYesButtonBG, borderwidth = 0)
logout_button.bind('<Button-1>', logout)
hide_widget(logout_button)

cancel_logout_button = Button(MainWindow, width = 241, height = 61, image = ExitNoButtonBG, borderwidth = 0)
cancel_logout_button.bind('<Button-1>', to_main_menu)
hide_widget(cancel_logout_button)

### Display no sync dialog error ###
NoSyncText = Image.open("data/images/NoSync.png")
NoSync = ImageTk.PhotoImage(NoSyncText)
no_sync = tkinter.Label(image = NoSync, borderwidth = 0)
hide_widget(no_sync)

OkButtonBG = PhotoImage(file = "data/images/Ok.png")
ok_button = Button(MainWindow, width = 241, height = 61, image = OkButtonBG, borderwidth = 0)
ok_button.bind('<Button-1>', ok)
hide_widget(ok_button)

### User's Profile ###
DiagBoxBG = Image.open("data/images/DiagBox.png")
DiagBox = ImageTk.PhotoImage(DiagBoxBG)
diag_box = tkinter.Label(image = DiagBox, borderwidth = 0)
hide_widget(diag_box)

profile_name = Label(MainWindow, justify = 'left')
profile_name['font'] = custom_font
profile_name.config(font = ("Segoe UI", 44))
hide_widget(profile_name)

profile_stat = Label(MainWindow, justify = 'right', text = "Times Played : \nEasy : \nNormal : \nHard : \n Expert : ")
profile_stat['font'] = custom_font
profile_stat.config(font = ("Segoe UI", 28))
hide_widget(profile_stat)

profile_stat_game = Label(MainWindow, justify = 'left')
profile_stat_game['font'] = custom_font
profile_stat_game.config(font = ("Segoe UI", 28))
hide_widget(profile_stat_game)

MaleProfilePicBG = Image.open("data/images/Male.png")
MaleProfilePic = ImageTk.PhotoImage(MaleProfilePicBG)
male_profile_pic = tkinter.Label(image = MaleProfilePic, borderwidth = 0)
hide_widget(male_profile_pic)

FemaleProfilePicBG = Image.open("data/images/Female.png")
FemaleProfilePic = ImageTk.PhotoImage(FemaleProfilePicBG)
female_profile_pic = tkinter.Label(image = FemaleProfilePic, borderwidth = 0)
hide_widget(female_profile_pic)

ChangeGenderBG = PhotoImage(file = "data/images/Gender.png")
change_gender_button = Button(MainWindow, width = 76, height = 76, image = ChangeGenderBG, borderwidth = 0)
change_gender_button.bind('<Button-1>', change_gender)
hide_widget(change_gender_button)

### Difficulty selection ###
SelectDifficultyBG = Image.open("data/images/SelectDifficulty.png")
SelectDifficulty = ImageTk.PhotoImage(SelectDifficultyBG)
select_difficulty = tkinter.Label(image = SelectDifficulty, borderwidth = 0)
hide_widget(select_difficulty)

EasyDifficultyBG = PhotoImage(file = "data/images/Easy.png")
easy_difficulty_button = Button(MainWindow, width = 288, height = 418, image = EasyDifficultyBG, borderwidth = 0)
easy_difficulty_button.bind('<Button-1>', easy_gamemode)
hide_widget(easy_difficulty_button)

NormalDifficultyBG = PhotoImage(file = "data/images/Normal.png")
normal_difficulty_button = Button(MainWindow, width = 288, height = 418, image = NormalDifficultyBG, borderwidth = 0)
normal_difficulty_button.bind('<Button-1>', normal_gamemode)
hide_widget(normal_difficulty_button)

HardDifficultyBG = PhotoImage(file = "data/images/Hard.png")
hard_difficulty_button = Button(MainWindow, width = 288, height = 418, image = HardDifficultyBG, borderwidth = 0)
hard_difficulty_button.bind('<Button-1>', hard_gamemode)
hide_widget(hard_difficulty_button)

ExpertDifficultyBG = PhotoImage(file = "data/images/Expert.png")
expert_difficulty_button = Button(MainWindow, width = 288, height = 418, image = ExpertDifficultyBG, borderwidth = 0)
expert_difficulty_button.bind('<Button-1>', expert_gamemode)
hide_widget(expert_difficulty_button)

### PreCountdown text ###
pre_countdown = Label(MainWindow, width = 25)
pre_countdown['font'] = custom_font
pre_countdown.config(font = ("Segoe UI", 40))
hide_widget(pre_countdown)

### Random integer ###
rand_int_text = Label(MainWindow, width = 15)
rand_int_text['font'] = custom_font
rand_int_text.config(font = ("Segoe UI", 100))
hide_widget(rand_int_text)

### Answer field ###
user_answer = Entry(MainWindow, width = 20)
user_answer['font'] = custom_font
user_answer.config(font = ("Segoe UI", 40))
user_answer.bind('<Key>', check_answer)
hide_widget(user_answer)

### Prompt user to cancel game ###
CancelGameBG = Image.open("data/images/CancelGame.png")
CancelGame = ImageTk.PhotoImage(CancelGameBG)
cancel_game = tkinter.Label(image = CancelGame, borderwidth = 0)
hide_widget(cancel_game)

CancelGameYes = PhotoImage(file = "data/images/Yes.png")
cancel_game_yes = Button(MainWindow, width = 241, height = 61, image = CancelGameYes, borderwidth = 0)
cancel_game_yes.bind('<Button-1>', prompt_exit)
hide_widget(cancel_game_yes)

CancelGameNo = PhotoImage(file = "data/images/No.png")
cancel_game_no = Button(MainWindow, width = 241, height = 61, image = CancelGameNo, borderwidth = 0)
cancel_game_no.bind('<Button-1>', prompt_exit_cancel)
hide_widget(cancel_game_no)

### Ok Button when game finished ###
FinishGame = PhotoImage(file = "data/images/Ok.png")
finish_game = Button(MainWindow, width = 241, height = 61, image = FinishGame, borderwidth = 0)
finish_game.bind('<Button-1>', ok_result)
hide_widget(finish_game)

MainWindow.mainloop()
