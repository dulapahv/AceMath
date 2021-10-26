#===============================================================#
#  Python Individual Project, Year 1, Semester 1                #
#                                                               #
#  Course: 13006107 Introduction to Computers and Programming   #
#  Program: Software Engineering Program                        #
#  University: Faculty of Engineering, KMITL                    #
#                                                               #
#  Project: AceMath                                             #
#  Repository: https://github.com/DulapahV/AceMath              #
#  Written by: Dulapah Vibulsanti (64011388)                    #
#===============================================================#

import winsound, random, time
from tkinter import Canvas, PhotoImage, Button, Label, Entry, Tk, font
from firebase_admin import initialize_app, credentials, db
from PIL import ImageTk, Image
 
#--[Program Data Path]------------------------------------------------------------
# The default path is "data/" (including slash and quotes)
# Inside the specified path must exist a folder named "sounds" and "images" (i.e. data/sounds and data/images)
# Inside the specified path must also exist a Firebase Service Account Key and data.txt (i.e. data/serviceAccountKey.json and data/data.txt)
data = "data/"

#--[Firebase Database Credential and Path]---------------------------------------
# The Service Account Key is stored in the default data path (i.e. data/serviceAccountKey.json)
# Internet connection is required to authenticate and access database
cred = credentials.Certificate(data + "serviceAccountKey.json")
initialize_app(cred, {"databaseURL": "https://acemath-n0miya-default-rtdb.asia-southeast1.firebasedatabase.app/"})

class AceMath(Tk):
    def __init__(self):
        super().__init__()
        
        #-------------------------------------------------------------------------
        # Program Configuration
        #-------------------------------------------------------------------------
        self.title("AcΣMαth")
        self.geometry("1920x1080")
        self.attributes("-fullscreen", True)
        self.wm_iconbitmap(data + "images/AceMath.ico")
        self.bind("<F11>", self.fullscreen)
        self.bind("<Escape>", self.close_confirmation)
        self.reinitialize()
        self.stopwatch = Stopwatch() # Create stopwatch object
        self.BGMusic = lambda: winsound.PlaySound(data + "sounds/BGMusic.wav", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
        self.gameFinishMusic = lambda: winsound.PlaySound(data + "sounds/GameFinish.wav", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
        self.gameStartMusic = lambda: winsound.PlaySound(data + "sounds/GameStart.wav", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
        self.DifficultySelectedMusic = lambda: winsound.PlaySound(data + "sounds/DifficultySelected.wav", winsound.SND_FILENAME)
        self.BGMusic()

        #-------------------------------------------------------------------------
        # Assets Initialization
        #-------------------------------------------------------------------------
        #--[Background Image]-----------------------------------------------------
        self.BGFullCanvas = Canvas(self, width = 1920, height = 1080)
        self.BGFullCanvas.pack()
        self.BGFull = ImageTk.PhotoImage(Image.open(data + "images/BGFull.jpg"))
        self.BGFullCanvas.create_image(0, 0, anchor = "nw", image = self.BGFull)

        self.BGCanvas = Canvas(self, width = 1920, height = 1080)
        self.BGCanvas.pack()
        self.BG = ImageTk.PhotoImage(Image.open(data + "images/BG.jpg"))
        self.BGCanvas.create_image(0, 0, anchor = "nw", image = self.BG)

        #--[Play Button]----------------------------------------------------------
        self.PlayButtonBG = PhotoImage(file = data + "images/Play.png")
        self.play_button = Button(self, image = self.PlayButtonBG, borderwidth = 0, command = self.play)
        self.play_button.place(x = 80, y = 292)

        #--[Sync Button]----------------------------------------------------------
        self.SyncButtonBG = PhotoImage(file = data + "images/Sync.png")
        self.sync_button = Button(self, image = self.SyncButtonBG, borderwidth = 0, command = self.sync)
        self.sync_button.place(x = 80, y = 425)

        #--[Profile Button]-------------------------------------------------------
        self.ProfileButtonBG = PhotoImage(file = data + "images/Profile.png")
        self.profile_button = Button(self, image = self.ProfileButtonBG, borderwidth = 0, command = self.profile)
        self.profile_button.place(x = 80, y = 558)

        #--[Leaderboard Button]-------------------------------------------------------
        self.LeaderboardButtonBG = PhotoImage(file = data + "images/Leaderboard.png")
        self.leaderboard_button = Button(self, image = self.LeaderboardButtonBG, borderwidth = 0, command = self.leaderboard)
        self.leaderboard_button.place(x = 80, y = 690)

        #--[About Button]---------------------------------------------------------
        self.AboutButtonBG = PhotoImage(file = data + "images/About.png")
        self.about_button = Button(self, image = self.AboutButtonBG, borderwidth = 0, command = self.about)
        self.about_button.place(x = 80, y = 810)

        #--[Exit Button]----------------------------------------------------------
        self.ExitButtonBG = PhotoImage(file = data + "images/Exit.png")
        self.exit_button = Button(self, image = self.ExitButtonBG, borderwidth = 0)
        self.exit_button.place(x = 80, y = 923)
        self.exit_button.bind("<Button-1>", self.close_confirmation)

        #--[Back Button]----------------------------------------------------------
        self.BackButtonBG = PhotoImage(file=data + "images/Back.png")
        self.back_button = Button(self, image = self.BackButtonBG, borderwidth = 0, command = self.to_main_menu)

        #--[About Description]----------------------------------------------------
        self.AboutCanvas = Canvas(self, width = 1920, height = 1080)
        self.AboutCanvas.pack()
        self.About = ImageTk.PhotoImage(Image.open(data + "images/AboutMe.jpg"))
        self.AboutCanvas.create_image(0, 0, anchor = "nw", image = self.About)

        #--[Exit Confirmation Dialog]---------------------------------------------
        self.ExitConfirmDiagBG = Image.open(data + "images/ExitDiag.png")
        self.ExitConfirmBG = ImageTk.PhotoImage(self.ExitConfirmDiagBG)
        self.exit_confirm = Label(image = self.ExitConfirmBG)

        self.ExitYesButtonBG = PhotoImage(file = data + "images/Yes.png")
        self.exit_yes_button = Button(self, image = self.ExitYesButtonBG, borderwidth = 0, command = self.close)

        self.ExitNoButtonBG = PhotoImage(file = data + "images/No.png")
        self.exit_no_button = Button(self, image = self.ExitNoButtonBG, borderwidth = 0, command = self.cancel)

        #--[Not Logged in Dialog]-------------------------------------------------
        self.AccountPromptDiagBG = Image.open(data + "images/AccountPrompt.png")
        self.AccountPromptBG = ImageTk.PhotoImage(self.AccountPromptDiagBG)
        self.account_prompt = Label(image = self.AccountPromptBG)

        self.AccountPromptDiagText = Image.open(data + "images/AccountPromptText.png")
        self.AccountPromptText = ImageTk.PhotoImage(self.AccountPromptDiagText)
        self.account_text = Label(image = self.AccountPromptText, borderwidth = 0)

        self.OfflineButtonBG = PhotoImage(file = data + "images/Offline.png")
        self.offline_button = Button(self, image = self.OfflineButtonBG, borderwidth = 0, command = self.play_offline)

        self.CreateButtonBG = PhotoImage(file = data + "images/Create.png")
        self.create_button = Button(self, image = self.CreateButtonBG, borderwidth = 0, command = self.create_account)

        self.LoginButtonBG = PhotoImage(file = data + "images/Login.png")
        self.login_button = Button(self, image = self.LoginButtonBG, borderwidth = 0, command = self.login_account)

        self.BackAuthButtonBG = PhotoImage(file = data + "images/Back_Account.png")
        self.back_auth_button = Button(self, image = self.BackAuthButtonBG, borderwidth = 0, command = self.back_auth)

        self.LoginAuthText = Image.open(data + "images/LoginAuth.png")
        self.LoginAuth = ImageTk.PhotoImage(self.LoginAuthText)
        self.login_auth = Label(image = self.LoginAuth, borderwidth = 0)

        self.CreateAccText = Image.open(data + "images/CreateAcc.png")
        self.CreateAcc = ImageTk.PhotoImage(self.CreateAccText)
        self.create_acc = Label(image = self.CreateAcc, borderwidth = 0)

        #--[Input Credential Dialog]----------------------------------------------
        self.username = Entry(self, width = 32, font = ("Comic Sans MS", 20))
        self.password = Entry(self, width = 32, show = "*", font = ("Comic Sans MS", 20))
        self.password_confirm = Entry(self, width = 32, show = "*", font = ("Comic Sans MS", 20))
        self.auth_message = Label(self, justify = "left", font = ("Comic Sans MS", 20))
        self.login_success = Label(self, anchor = "c", justify = "left", font = ("Comic Sans MS", 32))

        #--[Sync Dialog]----------------------------------------------------------
        self.SyncPromptText = Image.open(data + "images/SyncPromptMsg.png")
        self.SyncPrompt = ImageTk.PhotoImage(self.SyncPromptText)
        self.sync_prompt = Label(image = self.SyncPrompt, borderwidth = 0)

        self.GoToSyncBG = PhotoImage(file = data + "images/SyncContinue.png")
        self.go_to_sync = Button(self, image = self.GoToSyncBG, borderwidth = 0, command = self.sync)

        #--[Logout Dialog]--------------------------------------------------------
        self.LogoutPromptText = Image.open(data + "images/LogoutPrompt.png")
        self.LogoutPrompt = ImageTk.PhotoImage(self.LogoutPromptText)
        self.logout_prompt = Label(image = self.LogoutPrompt, borderwidth = 0)

        self.logout_button = Button(self, image = self.ExitYesButtonBG, borderwidth = 0, command = self.logout)
        self.cancel_logout_button = Button(self, image = self.ExitNoButtonBG, borderwidth = 0, command = self.to_main_menu)

        #--[Not Logged in Error Dialog]-------------------------------------------
        self.NoSyncText = Image.open(data + "images/NoSync.png")
        self.NoSync = ImageTk.PhotoImage(self.NoSyncText)
        self.no_sync = Label(image = self.NoSync, borderwidth = 0)

        self.OkButtonBG = PhotoImage(file = data + "images/Ok.png")
        self.ok_button = Button(self, image = self.OkButtonBG, borderwidth = 0, command = self.login_affirm)

        #--[User Profile Page]----------------------------------------------------
        self.DiagBoxBG = Image.open(data + "images/DiagBox.png")
        self.DiagBox = ImageTk.PhotoImage(self.DiagBoxBG)
        self.diag_box = Label(image = self.DiagBox, borderwidth = 0)

        self.profile_name = Label(self, justify = "left", font = ("Comic Sans MS", 44))
        self.profile_stat = Label(self, justify = "right", text = "Times Played : \nEasy : \nNormal : \nHard : \n Expert : ", font = ("Comic Sans MS", 28))
        self.profile_stat_game = Label(self, justify = "left", font = ("Comic Sans MS", 28))

        self.MaleProfilePicBG = Image.open(data + "images/Male.png")
        self.MaleProfilePic = ImageTk.PhotoImage(self.MaleProfilePicBG)
        self.male_profile_pic = Label(image = self.MaleProfilePic, borderwidth = 0)

        self.FemaleProfilePicBG = Image.open(data + "images/Female.png")
        self.FemaleProfilePic = ImageTk.PhotoImage(self.FemaleProfilePicBG)
        self.female_profile_pic = Label(image = self.FemaleProfilePic, borderwidth = 0)

        self.ChangeGenderBG = PhotoImage(file = data + "images/Gender.png")
        self.change_gender_button = Button(self, image = self.ChangeGenderBG, borderwidth = 0, command = self.change_gender)

        #--[Leaderboard Page]-----------------------------------------------------
        self.EasySmallBG = PhotoImage(file = data + "images/EasySmall.png")
        self.easy_small_button = Button(self, image = self.EasySmallBG, borderwidth = 0, command = self.easy_board)

        self.NormalSmallBG = PhotoImage(file = data + "images/NormalSmall.png")
        self.normal_small_button = Button(self, image = self.NormalSmallBG, borderwidth = 0, command = self.normal_board)

        self.HardSmallBG = PhotoImage(file = data + "images/HardSmall.png")
        self.hard_small_button = Button(self, image = self.HardSmallBG, borderwidth = 0, command = self.hard_board)

        self.ExpertSmallBG = PhotoImage(file = data + "images/ExpertSmall.png")
        self.expert_small_button = Button(self, image = self.ExpertSmallBG, borderwidth = 0, command = self.expert_board)
        
        self.EasyLeaderboardBG = Image.open(data + "images/EasyLeaderboard.png")
        self.EasyLeaderboard = ImageTk.PhotoImage(self.EasyLeaderboardBG)
        self.easy_leaderboard = Label(image = self.EasyLeaderboard, borderwidth = 0)

        self.NormalLeaderboardBG = Image.open(data + "images/NormalLeaderboard.png")
        self.NormalLeaderboard = ImageTk.PhotoImage(self.NormalLeaderboardBG)
        self.normal_leaderboard = Label(image = self.NormalLeaderboard, borderwidth = 0)

        self.HardLeaderboardBG = Image.open(data + "images/HardLeaderboard.png")
        self.HardLeaderboard = ImageTk.PhotoImage(self.HardLeaderboardBG)
        self.hard_leaderboard = Label(image = self.HardLeaderboard, borderwidth = 0)

        self.ExpertLeaderboardBG = Image.open(data + "images/ExpertLeaderboard.png")
        self.ExpertLeaderboard = ImageTk.PhotoImage(self.ExpertLeaderboardBG)
        self.expert_leaderboard = Label(image = self.ExpertLeaderboard, borderwidth = 0)

        self.leaderboardName = Label(self, justify = "left", font = ("Comic Sans MS", 28))
        self.leaderboardTime = Label(self, justify = "left", font = ("Comic Sans MS", 28))

        #--[Difficulty Selection Page]--------------------------------------------
        self.SelectDifficultyBG = Image.open(data + "images/SelectDifficulty.png")
        self.SelectDifficulty = ImageTk.PhotoImage(self.SelectDifficultyBG)
        self.select_difficulty = Label(image = self.SelectDifficulty, borderwidth = 0)

        self.EasyDifficultyBG = PhotoImage(file = data + "images/Easy.png")
        self.easy_difficulty_button = Button(self, image = self.EasyDifficultyBG, borderwidth = 0, command = lambda: self.difficulty_config("Easy", 19, 0, 9))

        self.NormalDifficultyBG = PhotoImage(file = data + "images/Normal.png")
        self.normal_difficulty_button = Button(self, image = self.NormalDifficultyBG, borderwidth = 0, command = lambda: self.difficulty_config("Normal", 19, 10, 99))

        self.HardDifficultyBG = PhotoImage(file = data + "images/Hard.png")
        self.hard_difficulty_button = Button(self, image = self.HardDifficultyBG, borderwidth = 0, command = lambda: self.difficulty_config("Hard", 19, 100, 999))

        self.ExpertDifficultyBG = PhotoImage(file = data + "images/Expert.png")
        self.expert_difficulty_button = Button(self, image = self.ExpertDifficultyBG, borderwidth = 0, command = lambda: self.difficulty_config("Expert", 19, 1000, 9999))

        #--[Pre-Countdown Text]---------------------------------------------------
        self.pre_countdown = Label(self, width = 25, font = ("Comic Sans MS", 40))

        #--[Random Integer Text]--------------------------------------------------
        self.rand_int_text = Label(self, width = 15, font = ("Comic Sans MS", 100))

        #--[Answer Field]---------------------------------------------------------
        self.user_answer = Entry(self, width = 20, font = ("Comic Sans MS", 40))
        self.user_answer.bind("<Key>", self.check_answer)

        #--[Cancel Ongoing Game Dialog]-------------------------------------------
        self.CancelGameBG = Image.open(data + "images/CancelGame.png")
        self.CancelGame = ImageTk.PhotoImage(self.CancelGameBG)
        self.cancel_game = Label(image = self.CancelGame, borderwidth = 0)

        self.CancelGameYes = PhotoImage(file = data + "images/Yes.png")
        self.cancel_game_yes = Button(self, image = self.CancelGameYes, borderwidth = 0, command = self.prompt_exit)

        self.CancelGameNo = PhotoImage(file = data + "images/No.png")
        self.cancel_game_no = Button(self, image = self.CancelGameNo, borderwidth = 0, command = self.prompt_exit_cancel)

        #--[Result Affirm Button]-------------------------------------------------
        self.FinishGame = PhotoImage(file = data + "images/Ok.png")
        self.finish_game = Button(self, image = self.FinishGame, borderwidth = 0, command = self.ok_result)

    #-----------------------------------------------------------------------------
    # Database
    #-----------------------------------------------------------------------------
    #--[Create New User in Firebase Database]-------------------------------------
    def create_new_user(self, user_name, user_password):
        user = db.reference("Users")
        user.child(user_name).set({
            "Key": user_password,
            "Gender": 0,
            "TimesPlayed": {
                "Easy": 0,
                "Normal": 0,
                "Hard": 0,
                "Expert": 0,
            },
            "FastestTime": {
                "Easy": "00.00s",
                "Normal": "00.00s",
                "Hard": "00.00s",
                "Expert": "00.00s",
                "EasyValue": 999999999,
                "NormalValue": 999999999,
                "HardValue": 999999999,
                "ExpertValue": 999999999,
            }
        })

    #--[Write Data to Firebase Database]------------------------------------------
    def write_to_firebase(self, user_name, child, data):
        user = db.reference("Users")
        user.child(user_name).update({
            child: data,
        })

    #--[Get leaderboard name and time from Firebase Database]---------------------
    def getLeaderboard(self, difficulty):
        allData = db.reference("Users").get()
        allUsername = list(allData.keys())
        scoreList = []
        for username in allUsername[:10]: # Limit to top 10 players
            time = db.reference("Users/" + username + "/FastestTime/" + difficulty).get()
            scoreList.append(float(time.removesuffix("s")))
        zipValue = zip(allUsername, scoreList)
        allScore = dict(zipValue)
        sortedLeaderboard = {}
        sortedLeaderboardKey = sorted(allScore, key = allScore.get)
        for value in sortedLeaderboardKey:
            if allScore[value] != 0:
                sortedLeaderboard[value] = allScore[value]
            else:
                continue
        leaderboardNameList = [""] * 10
        leaderboardTimeList = [""] * 10
        length = 20 # limit username length to 20 characters
        num = 0
        for key, value in sortedLeaderboard.items():
            key = (key[:length] + "...") if len(key) > length else key
            leaderboardNameList.insert(num, f"{num + 1:>2}. {key}")
            leaderboardTimeList.insert(num, f"{value}s")
            num += 1
        return leaderboardNameList, leaderboardTimeList

    #--[Get Amount of Times User Has Played]--------------------------------------
    def sum_times_played(self, user_name):
        easy = db.reference("Users/" + str(user_name) + "/TimesPlayed/Easy").get()
        normal = db.reference("Users/" + str(user_name) + "/TimesPlayed/Normal").get()
        hard = db.reference("Users/" + str(user_name) + "/TimesPlayed/Hard").get()
        expert = db.reference("Users/" + str(user_name) + "/TimesPlayed/Expert").get()
        sum_played = easy + normal + hard + expert
        return str(sum_played)

    #-----------------------------------------------------------------------------
    # Accessing data.txt
    #-----------------------------------------------------------------------------
    #--[Search and Get Value in data.txt]-----------------------------------------
    def read_data(self, string_to_search):
        lineNumber = 0
        value = ""
        with open(data + "data.txt", "r") as read_obj:
            for line in read_obj:
                lineNumber += 1
                if string_to_search in line:
                    value = line.rstrip()
        read_obj.close()
        return value.removeprefix(string_to_search + " = ")

    #--[Search and Replace Value in data.txt]-------------------------------------
    def write_data(self, string_to_search, value):
        lineNumber = 0
        with open(data + "data.txt", "r") as read_obj:
            filedata = read_obj.read()
            filedata = filedata.replace(string_to_search + " = " + self.read_data(string_to_search), string_to_search + " = " + str(value))
        with open(data + "data.txt", "w") as read_obj:
            read_obj.write(filedata)
        read_obj.close()

    #-----------------------------------------------------------------------------
    # Canvas and Widget Management
    #-----------------------------------------------------------------------------
    #--[Hide Canvas]--------------------------------------------------------------
    def hide_canvas(self, canvas):
        canvas.pack_forget()

    #--[Show Canvas]--------------------------------------------------------------
    def show_canvas(self, canvas):
        canvas.pack()

    #--[Hide Widget]--------------------------------------------------------------
    def hide_widget(self, widget):
        widget.place_forget()

    #--[Show Widget]--------------------------------------------------------------
    def show_widget(self, widget, x_coordinate, y_coordinate):
        widget.place(x = x_coordinate, y = y_coordinate)

    #-----------------------------------------------------------------------------
    # Program Functions
    #-----------------------------------------------------------------------------
    #--[Toggle Fullscreen]--------------------------------------------------------
    def fullscreen(self, event):
        if not self.attributes("-fullscreen"):
            self.attributes("-fullscreen", True)
        else:
            self.attributes("-fullscreen", False)

    #--[Moving out of MainMenu Event]---------------------------------------------
    def out_main_menu(self):
        hideWidgetList = [self.play_button, self.sync_button, self.profile_button, self.leaderboard_button, self.about_button, self.exit_button, 
                        self.exit_confirm, self.exit_no_button, self.exit_yes_button, self.account_prompt, self.no_sync, self.ok_button]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        self.show_widget(self.back_button, 80, 20)
        self.hide_canvas(self.BGFullCanvas)
        self.show_canvas(self.BGCanvas)

    #--[Moving to MainMenu Event]-------------------------------------------------
    def to_main_menu(self):
        if self.read_data("isUserInGame") == "True":
            self.stopwatch.stop()
            hideWidgetList = [self.pre_countdown, self.rand_int_text, self.user_answer]
            for widget in hideWidgetList:
                self.hide_widget(widget)
            showWidgetList = [[self.account_prompt, 500, 380], [self.cancel_game, 550, 480], [self.cancel_game_yes, 700, 683], [self.cancel_game_no, 1015, 683]]
            for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
            self.write_data("isStopwatchPaused", "True")
            self.user_answer.config(state = "disabled")
            self.hide_widget(self.diag_box)
        else:
            hideWidgetList = [self.go_to_sync, self.sync_prompt, self.offline_button, self.back_button, self.account_prompt, self.account_text, 
                            self.offline_button, self.create_button, self.login_button, self.logout_prompt, self.logout_button, self.cancel_logout_button, 
                            self.diag_box, self.profile_name, self.profile_stat, self.profile_stat_game, self.male_profile_pic, self.female_profile_pic, 
                            self.change_gender_button, self.select_difficulty, self.easy_difficulty_button, self.normal_difficulty_button, self.hard_difficulty_button, 
                            self.expert_difficulty_button, self.easy_small_button, self.normal_small_button, self.hard_small_button, self.expert_small_button, 
                            self.easy_leaderboard, self.normal_leaderboard, self.hard_leaderboard, self.expert_leaderboard, self.leaderboardName, self.leaderboardTime]
            for widget in hideWidgetList:
                self.hide_widget(widget)
            showWidgetList = [[self.play_button, 80, 292], [self.sync_button, 80, 425], [self.profile_button, 80, 558], [self.leaderboard_button, 80, 690], 
                            [self.about_button, 80, 810], [self.exit_button, 80, 923]]
            for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
            self.hide_canvas(self.BGCanvas)
            self.hide_canvas(self.AboutCanvas)
            self.show_canvas(self.BGFullCanvas)   

    #--[BACK Button (in auth screen) Event]---------------------------------------
    def back_auth(self):
        hideWidgetList = [self.login_auth, self.back_auth_button, self.auth_message, self.username, self.password, self.create_acc, self.password_confirm]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        showWidgetList = [[self.create_button, 700, 683], [self.login_button, 1015, 683], [self.account_text, 520, 400], [self.back_button, 80, 20]]
        for widget in range(len(showWidgetList)):
            self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        self.username.delete(0, "end")  # clear entered field
        self.password.delete(0, "end")
        self.password_confirm.delete(0, "end")
        self.write_data("isUserInCredentialScreen", "False")
    
    #--[Check if User Logged in]--------------------------------------------------
    def play(self):
        self.out_main_menu()
        # If not login, prompt player to play offline or go back to Sync menu
        if self.read_data("isFirebaseConnected") == "False":
            showWidgetList = [[self.account_prompt, 500, 380], [self.sync_prompt, 520, 400], [self.go_to_sync, 1015, 683], [self.offline_button, 700, 683]]
            for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        else:
            self.difficulty_select()

    #--[Play Offline]-------------------------------------------------------------
    def play_offline(self):
        self.difficulty_select()

    #--[Difficulty Selection Page]------------------------------------------------
    def difficulty_select(self):
        hideWidgetList = [self.account_prompt, self.sync_prompt, self.go_to_sync, self.offline_button]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        showWidgetList = [[self.diag_box, 227, 200], [self.select_difficulty, 289, 254], [self.easy_difficulty_button, 315, 418], 
                        [self.normal_difficulty_button, 650, 418], [self.hard_difficulty_button, 986, 418], [self.expert_difficulty_button, 1322, 418]]
        for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        
    #--[Difficulty Configuration]-------------------------------------------------
    def difficulty_config(self, selectedDifficulty, questionSize, minInteger, maxInteger):
        self.DifficultySelectedMusic()
        self.write_data("selectedDifficulty", selectedDifficulty)
        self.write_data("questionSize", questionSize)
        self.write_data("minInteger", minInteger)
        self.write_data("maxInteger", maxInteger)
        self.start_game()

    #--[SYNC Page]----------------------------------------------------------------
    def sync(self):
        self.out_main_menu()
        # Prompt user to choose whether they want to create an account, connect to existing account, or play offline
        if self.read_data("isFirebaseConnected") == "False":
            hideWidgetList = [self.go_to_sync, self.sync_prompt, self.offline_button]
            for widget in hideWidgetList:
                self.hide_widget(widget)
            showWidgetList = [[self.account_prompt, 500, 380], [self.account_text, 520, 400], [self.create_button, 700, 683], [self.login_button, 1015, 683]]
            for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        else:
            showWidgetList = [[self.account_prompt, 500, 380], [self.logout_prompt, 555, 500], [self.logout_button, 700, 683], [self.cancel_logout_button, 1015, 683]]
            for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])

    #--[PROFILE Page]-------------------------------------------------------------
    def profile(self):
        if self.read_data("isFirebaseConnected") == "False":
            showWidgetList = [[self.account_prompt, 500, 380], [self.no_sync, 650, 550], [self.ok_button, 860, 683]]
            for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        else:
            self.out_main_menu()
            showWidgetList = [[self.diag_box, 227, 200], [self.profile_name, 1000, 250], [self.profile_stat, 1000, 400], 
                            [self.profile_stat_game, 1245, 400], [self.change_gender_button, 248, 840]]
            for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
            length = 20
            name = self.read_data("firebaseUsername")
            name = (name[:length] + "...") if len(name) > length else name
            self.profile_name.config(text = name)
            self.profile_stat_game.config(text = self.sum_times_played(self.read_data("firebaseUsername")) + "\n" + 
                str(db.reference("Users/" + self.read_data("firebaseUsername") + "/TimesPlayed/Easy").get()) + " (Fastest : " + 
                str(db.reference("Users/" + self.read_data("firebaseUsername") + "/FastestTime/Easy").get()) + ")" + "\n" +
                
                str(db.reference("Users/" + self.read_data("firebaseUsername") + "/TimesPlayed/Normal").get()) + " (Fastest : " + 
                str(db.reference("Users/" + self.read_data("firebaseUsername") + "/FastestTime/Normal").get()) + ")" + "\n" +
                
                str(db.reference("Users/" + self.read_data("firebaseUsername") + "/TimesPlayed/Hard").get()) + " (Fastest : " + 
                str(db.reference("Users/" + self.read_data("firebaseUsername") + "/FastestTime/Hard").get()) + ")" + "\n" +
                
                str(db.reference("Users/" + self.read_data("firebaseUsername") + "/TimesPlayed/Expert").get()) + " (Fastest : " + 
                str(db.reference("Users/" + self.read_data("firebaseUsername") + "/FastestTime/Expert").get()) + ")" + "\n")
            if str(db.reference("Users/" + self.read_data("firebaseUsername") + "/Gender").get()) == "0":
                self.show_widget(self.male_profile_pic, 300, 300)
            else:
                self.show_widget(self.female_profile_pic, 300, 300)
    
    #--[LEADERBOARD Page]---------------------------------------------------------
    def leaderboard(self):
        self.out_main_menu()
        self.easy_board()
        showWidgetList = [[self.easy_small_button, 525, 44], [self.normal_small_button, 735, 44], [self.hard_small_button, 945, 44], 
                        [self.expert_small_button, 1155, 44], [self.easy_leaderboard, 525, 130]]
        for widget in range(len(showWidgetList)):
            self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
    
    def display_leaderboard(self, nameList, timeList):
        self.show_widget(self.leaderboardName, 550, 250)
        self.show_widget(self.leaderboardTime, 1500, 250)
        self.leaderboardName.config(text = f"{nameList[0]}\n{nameList[1]}\n{nameList[2]}\n{nameList[3]}\n{nameList[4]}\n" +
                                            f"{nameList[5]}\n{nameList[6]}\n{nameList[7]}\n{nameList[8]}\n{nameList[9]}\n")
        self.leaderboardTime.config(text = f"{timeList[0]}\n{timeList[1]}\n{timeList[2]}\n{timeList[3]}\n{timeList[4]}\n" +
                                            f"{timeList[5]}\n{timeList[6]}\n{timeList[7]}\n{timeList[8]}\n{timeList[9]}\n")

    def easy_board(self):
        hideWidgetList = [self.normal_leaderboard, self.hard_leaderboard, self.expert_leaderboard]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        self.show_widget(self.easy_leaderboard, 525, 130)
        nameList, timeList = self.getLeaderboard("Easy")
        self.display_leaderboard(nameList, timeList) 
    
    def normal_board(self):
        hideWidgetList = [self.easy_leaderboard, self.hard_leaderboard, self.expert_leaderboard]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        self.show_widget(self.normal_leaderboard, 525, 130)
        nameList, timeList = self.getLeaderboard("Normal")
        self.display_leaderboard(nameList, timeList)
    
    def hard_board(self):
        hideWidgetList = [self.easy_leaderboard, self.normal_leaderboard, self.expert_leaderboard]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        self.show_widget(self.hard_leaderboard, 525, 130)
        nameList, timeList = self.getLeaderboard("Hard")
        self.display_leaderboard(nameList, timeList)
    
    def expert_board(self):
        hideWidgetList = [self.easy_leaderboard, self.normal_leaderboard, self.hard_leaderboard]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        self.show_widget(self.expert_leaderboard, 525, 130)
        nameList, timeList = self.getLeaderboard("Expert")
        self.display_leaderboard(nameList, timeList)

    #--[ABOUT Page]---------------------------------------------------------------
    def about(self):
        self.out_main_menu()
        self.hide_canvas(self.BGCanvas)
        self.show_canvas(self.AboutCanvas)
        self.show_widget(self.back_button, 80, 20)
        self.back_button.lift()

    #--[Register Account Page]----------------------------------------------------
    def create_account(self):
        if self.read_data("isUserInCredentialScreen") == "False":
            hideWidgetList = [self.offline_button, self.login_button, self.account_text, self.back_button]
            for widget in hideWidgetList:
                self.hide_widget(widget)
            showWidgetList = [[self.create_button, 1188, 683], [self.create_acc, 520, 470], [self.back_auth_button, 520, 400], [self.username, 900, 470], 
                            [self.password, 900, 535], [self.password_confirm, 900, 602]]
            for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
            self.write_data("isUserInCredentialScreen", "True")
        else:
            # Check login credential
            self.show_widget(self.auth_message, 520, 683)
            if self.username.get() == "" or self.password.get() == "" or self.password_confirm.get() == "":
                self.auth_message.config(text = "Please complete all required fields.", fg = "red")
            elif self.password.get() != self.password_confirm.get():
                self.auth_message.config(text = "Passwords did not match. Try again.", fg = "red")
            elif str(db.reference("Users/" + self.username.get()).get()) != "None":
                self.auth_message.config(text = "This username is already taken.", fg = "red")
            else:
                self.create_new_user(self.username.get(), self.password.get())
                self.hide_widget(self.create_button)
                self.auth_message.config(text = "Account created successfully. Please go back and click on Login.", fg = "green")

    #--[Login Account Page]-------------------------------------------------------
    def login_account(self):
        if self.read_data("isUserInCredentialScreen") == "False":
            hideWidgetList = [self.offline_button, self.create_button, self.account_text, self.back_button]
            for widget in hideWidgetList:
                self.hide_widget(widget)
            showWidgetList = [[self.login_button, 1188, 683], [self.login_auth, 590, 520], [self.back_auth_button, 520, 400], 
                            [self.username, 820, 520], [self.password, 820, 585]]
            for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
            self.write_data("isUserInCredentialScreen", "True")
        else:
            # Check login credential
            self.show_widget(self.auth_message, 520, 683)
            user = db.reference("Users/" + self.username.get())
            key = db.reference("Users/" + self.username.get() + "/Key")
            if self.username.get() == "" or self.password.get() == "":
                self.auth_message.config(text = "Please complete all required fields.", fg = "red")
            elif user.get() == "None" or key.get() != self.password.get():
                self.auth_message.config(text = "Username or password is incorrect. Try again.", fg = "red")
            else:
                hideWidgetList = [self.auth_message, self.login_button, self.login_auth, self.back_auth_button, self.username, self.password]
                for widget in hideWidgetList:
                    self.hide_widget(widget)
                self.show_widget(self.ok_button, 1180, 683)
                self.show_widget(self.login_success, 550, 420)
                self.write_data("isFirebaseConnected", "True")
                self.write_data("firebaseUsername", self.username.get())
                self.write_data("isUserInCredentialScreen", "False")
                length = 20
                name = self.username.get()
                name = (name[:length] + "...") if len(name) > length else name
                self.login_success.config(text = f"Login Successful!\n\nWelcome back, {name}", fg = "green")
                self.username.delete(0, "end")
                self.password.delete(0, "end")

    #--[Login Affirm]-------------------------------------------------------------
    def login_affirm(self):
        hideWidgetList = [self.ok_button, self.no_sync, self.account_prompt, self.login_success]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        self.to_main_menu()

    #--[Logout]-------------------------------------------------------------------
    def logout(self):
        self.write_data("isUserInCredentialScreen", "False")
        self.write_data("firebaseUsername", "null")
        self.write_data("isFirebaseConnected", "False")
        self.to_main_menu()

    #--[Change Gender]------------------------------------------------------------
    def change_gender(self):
        if str(db.reference("Users/" + self.read_data("firebaseUsername") + "/Gender").get()) == "0":
            self.show_widget(self.female_profile_pic, 300, 300)
            self.hide_widget(self.male_profile_pic)
            self.write_to_firebase(self.read_data("firebaseUsername"), "Gender", 1)
        else:
            self.show_widget(self.male_profile_pic, 300, 300)
            self.hide_widget(self.female_profile_pic)
            self.write_to_firebase(self.read_data("firebaseUsername"), "Gender", 0)

    #--[Prompt Exit Confirmation While Game is Ongoing]---------------------------
    def prompt_exit(self):
        hideWidgetList = [self.diag_box, self.pre_countdown, self.user_answer, self.rand_int_text, self.account_prompt, self.cancel_game, 
                        self.cancel_game_yes, self.cancel_game_no]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        winsound.PlaySound(data + "sounds/BGMusic.wav", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
        self.reinitialize()
        self.to_main_menu()

    #--[Cancel Exit Confirmation While Game is Ongoing]---------------------------
    def prompt_exit_cancel(self):
        hideWidgetList = [self.account_prompt, self.cancel_game, self.cancel_game_yes, self.cancel_game_no]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        self.show_widget(self.rand_int_text, 370, 350)
        self.show_widget(self.diag_box, 227, 200)
        if self.read_data("isGameStarted") == "True":
            self.show_widget(self.user_answer, 670, 750)
            self.show_widget(self.pre_countdown, 870, 215)
            self.user_answer.config(state = "normal")
        else:
            self.show_widget(self.pre_countdown, 570, 520)
        self.write_data("isStopwatchPaused", "False") 
        self.stopwatch.start()

    #--[Countdown Timer]----------------------------------------------------------
    def countdown_timer(self, t):
        self.show_widget(self.pre_countdown, 570, 520)
        while t >= 0:
            if self.read_data("isStopwatchPaused") == "False":
                self.after(1000)
                self.pre_countdown.config(text = f"Game will start in {str(t)} seconds!\nPress 'ENTER' to submit answer", fg = "black")
                t -= 1
            self.update()  # Prevent Tkinter from locking up
        if self.read_data("isStopwatchPaused") == "False":
            self.stopwatch.restart()
            self.user_answer.config(state = "normal")
            self.show_widget(self.back_button, 80, 20)
            self.write_data("isGameStarted", "True")
            self.gameStartMusic()

    #--[Game Start]---------------------------------------------------------------
    def start_game(self):
        hideWidgetList = [self.select_difficulty, self.easy_difficulty_button, self.normal_difficulty_button, self.hard_difficulty_button, 
                        self.expert_difficulty_button, self.back_button]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        self.write_data("isUserInGame", "True")
        self.write_data("currentQuestionNumber", 0)
        self.countdown_timer(5)
        self.summon_question(int(self.read_data("questionSize")), int(self.read_data("minInteger")), int(self.read_data("maxInteger")))

    #--[Summon Question]----------------------------------------------------------
    def summon_question(self, questionSize, minInteger, maxInteger):
        if int(self.read_data("currentQuestionNumber")) <= questionSize:
            showWidgetList = [[self.user_answer, 670, 750], [self.rand_int_text, 370, 350], [self.pre_countdown, 870, 215]]
            for widget in range(len(showWidgetList)):
                self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
            self.user_answer.focus()
            int1, int2 = random.randint(minInteger, maxInteger), random.randint(minInteger, maxInteger)
            self.rand_int_text.config(text = str(int1) + " + " + str(int2))
            self.write_data("answer", int1 + int2)
            self.pre_countdown.config(text = str(int(self.read_data("currentQuestionNumber")) + 1) + "/" + str(questionSize + 1), anchor = "e")
        else:  # Game finishes
            hideWidgetList = [self.back_button, self.rand_int_text, self.user_answer]
            for widget in hideWidgetList:
                self.hide_widget(widget)
            self.show_widget(self.finish_game, 840, 770)
            self.stopwatch.stop()
            self.gameFinishMusic()
            self.user_answer.delete(0, "end")
            if self.read_data("isFirebaseConnected") == "True":
                self.show_widget(self.pre_countdown, 420, 450)
                self.submit_score() 
            else:
                self.show_widget(self.pre_countdown, 500, 450)
                self.pre_countdown.config(text = f"Your time is {str(self.stopwatch)}\nSign in to save your record!")
            self.reinitialize()
            
    #--[Check Answer]-------------------------------------------------------------
    def check_answer(self, event):
        if self.user_answer.get() == self.read_data("answer"):
            self.write_data("currentQuestionNumber", int(self.read_data("currentQuestionNumber")) + 1)
            self.user_answer.delete(0, "end")
            self.summon_question(int(self.read_data("questionSize")), int(self.read_data("minInteger")), int(self.read_data("maxInteger")))

    #--[Submit Score to Firebase Database]----------------------------------------
    def submit_score(self):
        timesPlayed = db.reference("Users/" + self.read_data("firebaseUsername") + "/TimesPlayed/" + self.read_data("selectedDifficulty")).get()
        timesPlayed += 1
        user = db.reference("Users")
        user.update({self.read_data("firebaseUsername") + "/TimesPlayed/" + self.read_data("selectedDifficulty"): timesPlayed,})
        previousBestTime = db.reference("Users/" + self.read_data("firebaseUsername") + "/FastestTime/" + self.read_data("selectedDifficulty") + "Value")
        if self.stopwatch.duration < previousBestTime.get():
            self.pre_countdown.config(text = f"Congratulations!\nYour time is {str(self.stopwatch)}\nNew Personal Record!", fg = "green")
            user.update({
                self.read_data("firebaseUsername") + "/FastestTime/" + self.read_data("selectedDifficulty"): str(self.stopwatch),
                self.read_data("firebaseUsername") + "/FastestTime/" + self.read_data("selectedDifficulty") + "Value": self.stopwatch.duration
            })
        else:
            self.show_widget(self.pre_countdown, 390, 450)
            self.pre_countdown.config(text = f"Your time is {str(self.stopwatch)}\nKeep on trying!")

    #--[Result Affirm]------------------------------------------------------------
    def ok_result(self):
        hideWidgetList = [self.diag_box, self.pre_countdown, self.finish_game]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        winsound.PlaySound(data + "sounds/BGMusic.wav", winsound.SND_ALIAS | winsound.SND_ASYNC | winsound.SND_LOOP)
        self.to_main_menu()
    
    #--[Reinitialize data.txt]----------------------------------------------------
    def reinitialize(self):
        self.write_data("isUserInCredentialScreen", "False")
        self.write_data("selectedDifficulty", "null")
        self.write_data("questionSize", 0)
        self.write_data("isGameStarted", "False")
        self.write_data("isStopwatchPaused", "False")
        self.write_data("isUserInGame", "False")
        self.write_data("currentQuestionNumber", 0)
        self.write_data("answer", 0)
        self.write_data("minInteger", 0)
        self.write_data("maxInteger", 0)

    #--[EXIT PROGRAM Confirmation Dialog]-----------------------------------------
    def close_confirmation(self, event):
        hideWidgetList = [self.account_prompt, self.no_sync, self.ok_button]
        for widget in hideWidgetList:
            self.hide_widget(widget)
        showWidgetList = [[self.exit_confirm, 525, 450], [self.exit_yes_button, 720, 570], [self.exit_no_button, 1000, 570]]
        for widget in range(len(showWidgetList)):
            self.show_widget(showWidgetList[widget][0], showWidgetList[widget][1], showWidgetList[widget][2])
        self.exit_confirm.lift()
        self.exit_yes_button.lift()
        self.exit_no_button.lift()

    #--[Cancel Exit Program Event]------------------------------------------------
    def cancel(self):
        self.hide_widget(self.exit_confirm)
        self.hide_widget(self.exit_yes_button)
        self.hide_widget(self.exit_no_button)

    #--[Exit Program Event]-------------------------------------------------------
    def close(self):
        self.reinitialize()
        self.destroy()
    
#--[Initialize Stopwatch]---------------------------------------------------------
class Stopwatch:
    def __init__(self):
        self._start = time.perf_counter()
        self._end = None

    @property
    def duration(self):
        return self._end - self._start if self._end else time.perf_counter() - self._start

    @property
    def running(self):
        return not self._end

    def restart(self):
        self._start = time.perf_counter()
        self._end = None
        return self

    def reset(self):
        self._start = time.perf_counter()
        self._end = self._start
        return self

    def start(self):
        if not self.running:
            self._start = time.perf_counter() - self.duration
            self._end = None
        return self

    def stop(self):
        if self.running:
            self._end = time.perf_counter()
        return self

    def __str__(self):
        time = self.duration * 1000
        if time >= 1000:
            return "{:.2f}s".format(time / 1000)
        if time >= 1:
            return "{:.2f}ms".format(time)
        return "{:.2f}μs".format(time * 1000)
    
if __name__ == "__main__":
    app = AceMath()
    app.mainloop()