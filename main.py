import pyrebase
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from collections import Counter
from datetime import datetime
from plyer import filechooser
import shutil,os

config={
  "apiKey": "AIzaSyAEn8vK6vMr6N-YUi8_sXFEuQw2aaNx1ho",
  "authDomain": "optotriage.firebaseapp.com",
  "databaseURL": "https://optotriage-default-rtdb.firebaseio.com",
  "projectId": "optotriage",
  "storageBucket": "optotriage.appspot.com",
  "messagingSenderId": "285095993077",
  "appId": "1:285095993077:web:c2f0d1140f9d91e19aefbc",
  "measurementId": "G-RK353DFDV9"
}
firebase=pyrebase.initialize_app(config)
database=firebase.database()
auth=firebase.auth()
storage=firebase.storage()
Window.size=(400,700)

age = 0
name = ''
percentages = ''
percentages2 = ''
percentages3 = ''

diagrams = {'Headache':"", 'Flashes of Light':"", 'Anisicoria':""}
histories = []

class Chat_Screen(Screen):
    pass
class History(Screen):
    pass
class HistoryMain(Screen):
    pass
class Account_Screen(Screen):
    pass
class Account_Edit_Screen(Screen):
    pass
class Result_Screen(Screen):
    pass
class Custom_Button(ButtonBehavior,Image):
    pass
class Headache(Screen):
    pass
class Flashes(Screen):
    pass
class Anisicoria(Screen):
    pass
class Problem_Lst_Screen(Screen):
    pass
class Registration_Screen(Screen):
    pass
class Asking_Username(Screen):
    pass
class Login_Screen(Screen):
    pass
class Main_Screen(Screen):
    pass
class CustomWidget(ButtonBehavior, MDBoxLayout):
    pass

class MainWidget(BoxLayout):
    headaches_list = []
    headaches_diag = []
    flashes_list = []
    flashes_diag = []
    anisicoria_list = []
    anisicoria_diag = []
    def switching_to_chat(self):
        self.ids.sm.current = "chat_screen"
        self.ids.sm.transition.direction = 'up'
    def profile_image(self):
        try:
            dist = os.path.join(os.getcwd(), f"{self.username}.jpeg")
            self.image_path = filechooser.open_file(title="Choose Profile Image", filters=[("*.jpeg")])
            shutil.copyfile(self.image_path[0],dist)
            self.ids.profile_image_placeholder.source = self.ids.profile_image_placeholder_edit.source = dist
            database.child(self.username).update({"Profile_image":dist})
        except:
            dialog = MDDialog(
                text="Oops! Image Upload Failed!" , radius=[20, 7, 20, 7])
            dialog.open()

    def showing_history(self):
        try:
            histories.clear()
            self.ids.historyItems.clear_widgets()
            copy,date,lineHistory,time,Name,Content = False,"","","","",""
            for line in open(self.username + ".txt").readlines():
                if date=="1":
                    date,time = line.strip().split(" ")
                    Name = "1"
                elif Name=="1":
                    Name = line.strip()
                    copy = True
                elif copy and line.strip() == "<--->":
                    copy = False
                    temp = {'name':Name, 'date':date, 'time':time, 'content':Content}
                    histories.append(temp)
                    Content = ""
                elif copy:
                    if lineHistory.find("?") >=0:
                        Content = Content+"[font=ElsieSwashCaps-Black]"+line+"[/font]"
                    else:
                        Content = Content+line.replace("%", "[font=EduTASBeginner-Regular][size=15sp] %[/size][/font]")
                if not copy and line.strip() == "<--->":
                    date = "1"
                lineHistory = line
            if copy:
                temp = {'name':Name, 'date':date, 'time':time, 'content':Content}
                histories.append(temp)
                
            images = {"Headache":"icon_folder/Headache.png","Flashes of Light":"icon_folder/BlueEye.png","Anisicoria":"icon_folder/PupilEye2.png"}

            for _ in range(len(histories)):
                self.ids.historyItems.add_widget(CustomWidget())
            
            self.ids.historyItems.height = ((len(histories)//2)+1)*145

            for i,child in enumerate(self.ids.historyItems.children):
                child.bind(on_press=self.showing_history_item)
                child.ids[f'historyItem_date_{i}'] = child.ids.pop('historyItem_date') # CHANGE ID OF ELEMENTS
                child.ids[f'historyItem_time_{i}'] = child.ids.pop('historyItem_time') # CHANGE ID OF ELEMENTS
                child.ids[f'historyItem_title_{i}'] = child.ids.pop('historyItem_title') # CHANGE ID OF ELEMENTS
                child.ids[f'historyItem_image_{i}'] = child.ids.pop('historyItem_image') # CHANGE ID OF ELEMENTS
                child.ids[f'historyItem_date_{i}'].text = histories[i]['date']
                child.ids[f'historyItem_time_{i}'].text = histories[i]['time']
                child.ids[f'historyItem_title_{i}'].text = histories[i]['name']
                child.ids[f'historyItem_image_{i}'].source = images[histories[i]['name']]

            self.ids.sm.current = "history_main_screen"
            self.ids.sm.transition.direction = 'left'
        except:
            dialog = MDDialog(
                text="Cannot Get History!" , radius=[20, 7, 20, 7])
            dialog.open()

    def showing_history_item(self,ChildObject):
        id = ChildObject.parent.children.index(ChildObject)
        self.ids.history_name_placeholder.text = histories[id]['name']
        self.ids.history_placeholder.text = histories[id]['content']
        self.ids.history_date_placeholder.text = histories[id]['date']
        self.ids.history_time_placeholder.text = histories[id]['time']
        self.ids.sm.current = "history_screen"
        self.ids.sm.transition.direction = 'right'

    def logging_out(self):
        self.ids.sm.current = "main_screen"
        self.ids.sm.transition.direction = 'right'
    def switching_to_account_page(self):
        self.ids.sm.current = "account_screen"
        self.ids.sm.transition.direction = 'up'
    def switching_to_account_edit_page(self):
        self.ids.sm.current = "account_edit_screen"
        self.ids.sm.transition.direction = 'up'
    def back_to_home(self,side):
        self.ids.sm.current = "problem_lst_screen"
        self.ids.sm.transition.direction = side
        
    def cancelTest(self, instance):
        global age, name, percentages, percentages2, percentages3
        age = 0
        name = ''
        
        if instance == 'Headache':
            percentages = ''
            self.headaches_list = []
            self.headaches_diag = []
            self.ids.headache_question.text = "Are the headaches unilateral or bilateral?"
            self.ids.headache_btn1.text = "Unilateral"
            self.ids.headache_btn2.text = "Bilateral"
            diagrams['Headache'] = ""
        elif instance == 'Flashes of Light':
            percentages2 = ''
            self.flashes_list = []
            self.flashes_diag = []
            self.ids.flashes_question.text = "Are the flashes unilateral or bilateral?"
            self.ids.flashes_btn1.text = "Unilateral"
            self.ids.flashes_btn2.text = "Bilateral"
            diagrams['Flashes of Light'] = ""
        elif instance == 'Anisicoria':
            percentages3 = ''
            self.anisicoria_list = []
            self.anisicoria_diag = []
            self.ids.anisicoria_question.text = "Is it recent or longstanding?"
            self.ids.anisicoria_btn1.text = "Recent"
            self.ids.anisicoria_btn2.text = "Longstanding"
            diagrams['Anisicoria'] = ""

        self.ids.sm.current = "problem_lst_screen"
        self.ids.sm.transition.direction = "right"

    def back_to_login(self):
        self.ids.sm.current = "main_screen"
        self.ids.sm.transition.direction = 'right'
    def back_to_reg(self):
        self.ids.sm.current = "reg_screen"
        self.ids.sm.transition.direction = 'right'
    def switching_to_headache_screen(self):
        self.ids.sm.current = "headaches"
        self.ids.sm.transition.direction = 'left'
    def switching_to_flashes_screen(self):
        self.ids.sm.current = "flashes_screen"
        self.ids.sm.transition.direction = 'left'
    def switching_to_anisicoria_screen(self):
        self.ids.sm.current = "anisicoria_screen"
        self.ids.sm.transition.direction = 'left'
    def switching_to_registration(self):
        self.ids.reg_toolbar.ids.label_title.font_name = "ElsieSwashCaps-Regular.ttf"
        self.ids.sm.current="reg_screen"
        self.ids.sm.transition.direction = 'left'
    def switching_to_asking_username(self):
        self.f_name=self.ids.f_name.text
        self.l_name=self.ids.l_name.text
        self.birth_date = self.ids.birth_date.text
        self.phone_number = self.ids.phone_number.text
        self.city = self.ids.city.text
        self.country = self.ids.country.text
        if self.f_name !="" and self.l_name !="" and self.birth_date !="" and self.phone_number !="" and self.city !="" and self.country !="":
            self.ids.user_toolbar.ids.label_title.font_name = "ElsieSwashCaps-Regular.ttf"
            self.ids.sm.current ="asking_username"
            self.ids.sm.transition.direction = 'left'
        else:
            dialog=MDDialog(text="Invalid Information")
            dialog.open()

    def login(self):
        email=self.ids.login_email_address.text
        password=self.ids.login_password.text
        self.username=email.split("@")[0]
        try:
            auth.sign_in_with_email_and_password(email,password)
            data=database.get()
            users=data
            for user in users.each():
                if str(user.key())==self.username:
                    info_dict=user.val()
                    self.ids.account_lname_edit.text         = self.ids.account_lname.text         = info_dict["Last Name"]
                    self.ids.account_fname_edit.text         = self.ids.account_fname.text    = info_dict["First Name"]
                    self.ids.dob_edit.text                   = self.ids.dob.text                   = info_dict["Birth Date"]
                    self.ids.account_phone_number_edit.text  = self.ids.account_phone_number.text  = info_dict["Phone Number"]
                    self.ids.account_email_address_edit.text = self.ids.account_email_address.text = info_dict["Email Address"]
                    self.ids.account_country_edit.text       = self.ids.account_country.text       = info_dict["Country"]
                    self.ids.account_city_edit.text          = self.ids.account_city.text          = info_dict["City"]
                    try:
                        self.ids.profile_image_placeholder_edit.source = self.ids.profile_image_placeholder.source = info_dict["Profile_image"]
                    except Exception as e:
                        print("Image Load Failed!")
                        self.ids.profile_image_placeholder.source = "icon_folder/Account_.png"
                    break
            self.headaches_list = []
            self.headaches_diag = []
            self.flashes_list = []
            self.flashes_diag = []
            self.anisicoria_list = []
            self.anisicoria_diag = []

            print("Success")
            self.ids.sm.current = "problem_lst_screen"
            self.ids.sm.transition.direction = 'left'
        except Exception as e:
            print(e)
            dialog = MDDialog(
                text="Oops! Login Failed!" , radius=[20, 7, 20, 7])
            dialog.open()

    def registering(self):
        email_address=self.ids.username.text
        password= self.ids.password.text
        confirm_password=self.ids.confirm_password.text
        if password==confirm_password:
            information={
                "First Name": self.f_name,
                "Last Name": self.l_name,
                "Birth Date": self.birth_date,
                "Email Address": email_address,
                "Phone Number": self.phone_number,
                "Country": self.country,
                "City": self.city,
                "Password": password,
                "Profile_image":"icon_folder/Account_.png"
            }
            username=email_address.split("@")[0]
            try:
                auth.create_user_with_email_and_password(email_address,password)
                database.child(username).set(information)
                self.ids.sm.current = "main_screen"
                self.ids.sm.transition.direction = 'right'
            except Exception as e:
                print(e)
                dialog = MDDialog(
                    text="1. Enter a Correct Email Address\n2. Password must contain 7 alphanumeric digits\n3. Check your internet connection", radius=[20, 7, 20, 7])
                dialog.open()
        else:
            print("Password Does not match")

    def saving(self):
        information={
            "First Name": self.ids.account_fname_edit.text,
            "Last Name": self.ids.account_lname_edit.text,
            "Birth Date": self.ids.dob_edit.text,
            "Email Address": self.ids.account_email_address_edit.text,
            "Phone Number": self.ids.account_phone_number_edit.text,
            "Country": self.ids.account_country_edit.text,
            "City": self.ids.account_city_edit.text,
        }
        try:
            username=self.ids.account_email_address_edit.text.split("@")[0]
            database.child(username).set(information)
            dialog = MDDialog(
                text="Details Saved Successfully !", radius=[20, 7, 20, 7])
            dialog.open()
            self.ids.account_lname.text = self.ids.account_lname_edit.text
            self.ids.account_fname.text = self.ids.account_fname_edit.text
            self.ids.dob.text = self.ids.dob_edit.text
            self.ids.account_phone_number.text = self.ids.account_phone_number_edit.text
            self.ids.account_email_address.text = self.ids.account_email_address_edit.text
            self.ids.account_country.text = self.ids.account_country_edit.text
            self.ids.account_city.text = self.ids.account_city_edit.text
        except Exception as e:
            print(e)
            dialog = MDDialog(
                text="1. Enter a Correct Email Address\n2. Check your internet connection", radius=[20, 7, 20, 7])
            dialog.open()

    def main_logic(self, btn_instance_id, label_instance_id, instance):
        global age, name, percentages, percentages2, percentages3
        question_text=label_instance_id.text
        btn_text=btn_instance_id.text

        diagrams[instance] = f"{diagrams[instance]}\n{question_text}\n{btn_text}"

        if question_text=="Are the headaches unilateral or bilateral?" and btn_text=="Unilateral":
            self.ids.headache_question.text="Did this headache come on suddenly or gradually?"
            self.ids.headache_btn1.text="Suddenly"
            self.ids.headache_btn2.text = "Gradually"

            print('unilateral')
            self.headaches_list = []
            self.headaches_diag.extend(["Migraine(Routine)", "Migraine(Advise)", "ON(PSD)", "ON(PU1)", "ON(Acute)"])
            print(self.headaches_diag)

        elif question_text=="Are the headaches unilateral or bilateral?" and btn_text=="Bilateral":
            self.ids.headache_question.text = "Did this headache come on suddenly or gradually?"
            self.ids.headache_btn1.text = "Suddenly"
            self.ids.headache_btn2.text = "Gradually"

            print('bilateral')
            self.headaches_list = []
            self.headaches_diag.extend(
                ["Migraine(Routine)", "Migraine(Advise)", "ON(PSD)", "ON(PU1)", "ON(Acute)", "Brain Disease(SD)",
                 "HCD(Routine)", "ETTH(Advise)"])
            print(self.headaches_diag)

        elif question_text=="Did this headache come on suddenly or gradually?" and btn_text=="Suddenly":
            self.ids.headache_question.text = "Does this occur in transient episodes? if YES state whether seconds,or up to an hour?"
            self.ids.headache_btn1.text = "Seconds"
            self.ids.headache_btn2.text = "Hours"
            self.ids.headache_btn3.text = "No"
            self.ids.headache_btn3.disabled= False

            print('suddenly')
            self.headaches_diag.extend(["ON(Acute)"])
            print(self.headaches_diag)

        elif question_text=="Did this headache come on suddenly or gradually?" and btn_text=="Gradually":
            self.ids.headache_question.text = "Does this occur in transient episodes? if YES state whether seconds,or up to an hour?"
            self.ids.headache_btn1.text = "Seconds"
            self.ids.headache_btn2.text = "Hours"
            self.ids.headache_btn3.text = "No"
            self.ids.headache_btn3.disabled = False

            print('gradually')
            self.headaches_diag.extend(["ON(PSD)", "ON(PU1)"])
            print(self.headaches_diag)

        #Transient
        elif question_text=="Does this occur in transient episodes? if YES state whether seconds,or up to an hour?" and btn_text=="Seconds":
            self.ids.headache_question.text = "Are the headaches recurrent?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"
            self.ids.headache_btn3.disabled = True

            print('seconds')
            self.headaches_diag.extend(["Brain Disease(SD)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Does this occur in transient episodes? if YES state whether seconds,or up to an hour?" and btn_text=="Hours":
            self.ids.headache_question.text = "Are the headaches recurrent?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"
            self.ids.headache_btn3.disabled = True

            print('hours')
            self.headaches_diag.extend(["Migraine(Routine)", "Migraine(Advise)", "Brain Disease(SD)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Does this occur in transient episodes? if YES state whether seconds,or up to an hour?" and btn_text=="No":
            self.ids.headache_question.text = "Are the headaches recurrent?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"
            self.ids.headache_btn3.disabled = True

            print('no hours seconds')
            self.headaches_diag.extend(["Migraine(Routine)", "Migraine(Advise)", "ON(PSD)", "ON(PU1)", "ON(Acute)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        #Recurrent
        elif question_text=="Are the headaches recurrent?" and btn_text=="Yes":
            self.ids.headache_question.text = "Is Vision Loss present?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            print('headache recurrent yes')
            self.headaches_diag.extend(
                ["Migraine(Routine)", "Migraine(Advise)", "Brain Disease(SD)", "HCD(Routine)", "ETTH(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Are the headaches recurrent?" and btn_text=="No":
            self.ids.headache_question.text = "Is Vision Loss present?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["ON(PSD)", "ON(PU1)", "ON(Acute)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        #Vision Loss
        #True
        elif question_text=="Is Vision Loss present?" and btn_text=="Yes":
            self.ids.headache_question.text = "Is Vision loss in central, peri, or shadow like?"
            self.ids.headache_btn1.text = "Central"
            self.ids.headache_btn2.text = "Peri"
            self.ids.headache_btn3.text = "Shadow"
            self.ids.headache_btn3.disabled = False

            print('yes vision loss')
            self.headaches_diag.extend(
                ["Brain Disease(SD)", "ON(PSD)", "ON(PU1)", "ON(Acute)", "Migraine(Routine)", "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Is Vision loss in central, peri, or shadow like?" and btn_text=="Central":
            self.ids.headache_question.text = "Do you have any of the following: unusual headache, tender scalp, jaw ache when chewing, ear or neck pain, weight loss, fatigue, muscle aches?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"
            self.ids.headache_btn3.disabled = True

            print('central')
            self.headaches_diag.extend(["ON(PSD)", "ON(PU1)", "ON(Acute)", "Migraine(Routine)", "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)
            self.headaches_list = []

        elif question_text=="Is Vision loss in central, peri, or shadow like?" and btn_text=="Peri":
            self.ids.headache_question.text = "Do you have any of the following: unusual headache, tender scalp, jaw ache when chewing, ear or neck pain, weight loss, fatigue, muscle aches?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"
            self.ids.headache_btn3.disabled = True

            print('peri')
            self.headaches_diag.extend(
                ["Brain Disease(SD)", "ON(PSD)", "ON(PU1)", "ON(Acute)", "Migraine(Routine)", "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)
            self.headaches_list = []

        elif question_text=="Is Vision loss in central, peri, or shadow like?" and btn_text=="Shadow":
            self.ids.headache_question.text = "Do you have any of the following: unusual headache, tender scalp, jaw ache when chewing, ear or neck pain, weight loss, fatigue, muscle aches?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"
            self.ids.headache_btn3.disabled = True

            print('shdaow')
            self.headaches_diag.extend([])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)
            self.headaches_list = []

        #False
        elif question_text=="Is Vision Loss present?" and btn_text=="No":
            self.ids.headache_question.text = "Do you have any of the following: unusual headache, tender scalp, jaw ache when chewing, ear or neck pain, weight loss, fatigue, muscle aches?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            print('no vision loss')
            self.headaches_diag.extend(["HCD(Routine)", "ETTH(Advise)"])

        #List of Diseases
        elif question_text == "Do you have any of the following: unusual headache, tender scalp, jaw ache when chewing, ear or neck pain, weight loss, fatigue, muscle aches?" and btn_text=="Yes":
            self.ids.headache_question.text = "Do you have Eye pain?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["Temporal Arteritis"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text == "Do you have any of the following: unusual headache, tender scalp, jaw ache when chewing, ear or neck pain, weight loss, fatigue, muscle aches?" and btn_text=="No":
            self.ids.headache_question.text = "Do you have Eye pain?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(
                ["ON(PSD)", "ON(PU1)", "ON(Acute)", "HCD(Routine)", "ETTH(Advise)", "Migraine(Routine)",
                 "Migraine(Advise)", "Brain Disease(SD)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        #Eye Pain
        elif question_text =="Do you have Eye pain?" and btn_text=="Yes":
            self.ids.headache_question.text = "Is pain mild, moderate to severe, or shooting.?"
            self.ids.headache_btn1.text = "Mild"
            self.ids.headache_btn2.text = "Moderate"
            self.ids.headache_btn3.text = "Shooting"
            self.ids.headache_btn3.disabled = False

            self.headaches_diag.extend(["Brain Disease(SD)", "ON(PSD)", "ON(PU1)", "ON(Acute)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text =="Is pain mild, moderate to severe, or shooting.?" and btn_text=="Mild":
            self.ids.headache_question.text ="Do you have any head/neck pain?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"
            self.ids.headache_btn3.disabled = True

            self.headaches_diag.extend([])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text =="Is pain mild, moderate to severe, or shooting.?" and btn_text=="Moderate":
            self.ids.headache_question.text ="Do you have any head/neck pain?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"
            self.ids.headache_btn3.disabled = True

            self.headaches_diag.extend([])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text =="Is pain mild, moderate to severe, or shooting.?" and btn_text=="Shooting":
            self.ids.headache_question.text ="Do you have any head/neck pain?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"
            self.ids.headache_btn3.disabled = True

            self.headaches_diag.extend([])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Do you have any head/neck pain?" and btn_text=="Yes":
            self.ids.headache_question.text = "Is eye pain worse when moving your eye?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend([])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Do you have any head/neck pain?" and btn_text=="No":
            self.ids.headache_question.text = "Is eye pain worse when moving your eye?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(
                ["Brain Disease(SD)", "ON(PSD)", "ON(PU1)", "ON(Acute)", "HCD(Routine)", "ETTH(Advise)",
                 "Migraine(Routine)", "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text== "Is eye pain worse when moving your eye?" and btn_text=="Yes":
            self.ids.headache_question.text = "Are the headaches worse when lying down?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["ON(PSD)", "ON(PU1)", "ON(Acute)"])
            self.headaches_list = []
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text== "Is eye pain worse when moving your eye?" and btn_text=="No":
            self.ids.headache_question.text = "Are the headaches worse when lying down?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(
                ["Brain Disease(SD)", "HCD(Routine)", "ETTH(Advise)", "Migraine(Routine)", "Migraine(Advise)"])
            self.headaches_list = []
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text =="Do you have Eye pain?" and btn_text=="No":
            self.ids.headache_question.text ="Are the headaches worse when lying down?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["HCD(Routine)", "ETTH(Advise)", "Migraine(Routine)", "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        #Headache during lying down
        elif question_text=="Are the headaches worse when lying down?" and btn_text=="Yes":
            self.ids.headache_question.text = "Do the headaches come with aura?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["Brain Disease(SD)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Are the headaches worse when lying down?" and btn_text=="No":
            self.ids.headache_question.text = "Do the headaches come with aura?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(
                ["ON(PSD)", "ON(PU1)", "ON(Acute)", "HCD(Routine)", "ETTH(Advise)", "Migraine(Routine)",
                 "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        #Aura
        elif question_text=="Do the headaches come with aura?" and btn_text=="Yes":
            self.ids.headache_question.text = "Do you have any of the following: vertigo, limb weakness or numbness?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["Migraine(Routine)", "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Do the headaches come with aura?" and btn_text=="No":
            self.ids.headache_question.text = "Do you have any of the following: vertigo, limb weakness or numbness?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(
                ["Brain Disease(SD)", "ON(PSD)", "ON(PU1)", "ON(Acute)", "HCD(Routine)", "ETTH(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        #Vertigo, etc
        elif question_text=="Do you have any of the following: vertigo, limb weakness or numbness?" and btn_text =="Yes":
            self.ids.headache_question.text = "Do you ever see flashes of light in your vision?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["Brain Disease(SD)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Do you have any of the following: vertigo, limb weakness or numbness?" and btn_text =="No":
            self.ids.headache_question.text = "Do you ever see flashes of light in your vision?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(
                ["ON(PSD)", "ON(PU1)", "ON(Acute)", "HCD(Routine)", "ETTH(Advise)", "Migraine(Routine)",
                 "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        #Flashes of Light
        elif question_text=="Do you ever see flashes of light in your vision?" and btn_text=="Yes":
            self.ids.headache_question.text = "Do the flashes flash/flicker in one eye?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["Brain Disease(SD)", "Migraine(Routine)", "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Do the flashes flash/flicker in one eye?" and btn_text=="Yes":
            self.ids.headache_question.text = "Do you ever see a transient patch of blurred vision with ‘zig-zag’ lines, ‘sparkling lights’ or coloured lines?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["Retinal Detachment/Tear"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Do the flashes flash/flicker in one eye?" and btn_text=="No":
            self.ids.headache_question.text = "Do you ever see a transient patch of blurred vision with ‘zig-zag’ lines, ‘sparkling lights’ or coloured lines?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(
                ["Brain Disease(SD)", "ON(PSD)", "ON(PU1)", "ON(Acute)", "HCD(Routine)", "ETTH(Advise)",
                 "Migraine(Routine)", "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Do you ever see a transient patch of blurred vision with ‘zig-zag’ lines, ‘sparkling lights’ or coloured lines?" and btn_text=="Yes":
            self.ids.headache_question.text = "Have you had a medical history of migraine?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["Brain Disease(SD)", "Migraine(Routine)", "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)
            self.headaches_list = []

        elif question_text=="Do you ever see a transient patch of blurred vision with ‘zig-zag’ lines, ‘sparkling lights’ or coloured lines?" and btn_text=="No":
            self.ids.headache_question.text = "Have you had a medical history of migraine?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["ON(PSD)", "ON(PU1)", "ON(Acute)", "HCD(Routine)", "ETTH(Advise)"])
            self.headaches_list = []
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text == "Do you ever see flashes of light in your vision?" and btn_text == "No":
            self.ids.headache_question.text = "Have you had a medical history of migraine?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["HCD(Routine)", "ETTH(Advise)", "ON(Acute)", "ON(PSD)", "ON(PU1)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        #Migraine History
        elif question_text=="Have you had a medical history of migraine?" and btn_text == "Yes":
            self.ids.headache_question.text = "Have you had a family history of migraine?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(["Migraine(Routine)", "Migraine(Advise)"])
            print("CURRENT DIAGNOSIS:", self.headaches_diag)

        elif question_text=="Have you had a medical history of migraine?" and btn_text == "No":
            self.ids.headache_question.text = "Have you had a family history of migraine?"
            self.ids.headache_btn1.text = "Yes"
            self.ids.headache_btn2.text = "No"

            self.headaches_diag.extend(
                ["Brain Disease(SD)", "ON(PSD)", "ON(PU1)", "ON(Acute)", "HCD(Routine)", "ETTH(Advise)"])

        #Family Migraine
        elif question_text == "Have you had a family history of migraine?" and btn_text == "Yes":
            self.headaches_diag.extend(["Migraine(Routine)", "Migraine(Advise)"])

            today = datetime.today().strftime("%m/%d %H:%M")
            history = open(self.username + ".txt", "a+")
            history.write("<--->\n")
            history.write(f"{str(today)}\n")
            history.write(f"{instance}\n")
            history.write(diagrams[instance])
            history.write('\n\nResult:')
            history.close()

            count2 = Counter(self.headaches_diag).items()
            percentages2 = {x: int(float(y) / len(self.headaches_diag) * 100) for x, y in count2}
            if self.ids.lst_placeholder.children:
                self.ids.lst_placeholder.remove_widget(self.ids.lst_placeholder.children[0])
            boxlayout=MDBoxLayout(adaptive_height= True, orientation="vertical", spacing=15)
            self.ids.lst_placeholder.add_widget(boxlayout)
            self.ids.heading.text="Headaches"
            self.ids.heading_img.source="icon_folder/Headache.png"
            history=open(self.username+".txt", "a+")
            sorted_percentages2 = sorted(percentages2.items(), key=lambda vari: vari[1], reverse=True)
            for i in sorted_percentages2:
                history.write(f"{i[0]}:    {i[1]}%\n")
                label_widget = MDLabel(text=f"{i[0]} - {i[1]} %", size_hint_y=None, height=50, halign="center",md_bg_color=(212/255, 175/255, 185/255, 0.3), radius=10)
                boxlayout.add_widget(label_widget)
                # self.ids['result'].text = f"FINAL DIAGNOSIS: ('%s - %s%s' % (name, pct, '%')"
            # self.ids.percent.text = str(percentages2)
            history.write("\n\n")
            history.close()
            storage.child(self.username+".txt").put(self.username+".txt")
            print(percentages2)
            self.cancelTest(instance)
            self.ids.sm.current = "result_screen"
        elif question_text == "Have you had a family history of migraine?" and btn_text == "No":
            self.headaches_diag.extend(["Brain Disease(SD)", "ON(PSD)", "ON(PU1)", "ON(Acute)", "HCD(Routine)", "ETTH(Advise)"])

            today = datetime.today().strftime("%m/%d %H:%M")
            history = open(self.username + ".txt", "a+")
            history.write("<--->\n")
            history.write(f"{str(today)}\n")
            history.write(f"{instance}\n")
            history.write(diagrams[instance])
            history.write('\n\nResult:')
            history.close()

            count2 = Counter(self.headaches_diag).items()
            percentages2 = {x: int(float(y) / len(self.headaches_diag) * 100) for x, y in count2}
            if self.ids.lst_placeholder.children:
                self.ids.lst_placeholder.remove_widget(self.ids.lst_placeholder.children[0])
            boxlayout = MDBoxLayout(adaptive_height=True, orientation="vertical", spacing=15)
            self.ids.lst_placeholder.add_widget(boxlayout)
            history = open(self.username + ".txt", "a+")
            sorted_percentages2 = sorted(percentages2.items(), key=lambda vari: vari[1], reverse=True)
            for i in sorted_percentages2:
                history.write(f"{i[0]}:    {i[1]}%\n")
                label_widget = MDLabel(text=f"{i[0]} - {i[1]} %", size_hint_y=None, height=50, halign="center",
                                       md_bg_color=(212 / 255, 175 / 255, 185 / 255, 0.3), radius=10)
                boxlayout.add_widget(label_widget)
            history.write("\n\n")
            history.close()
            storage.child(self.username + ".txt").put(self.username + ".txt")
            print(percentages2)
            self.cancelTest(instance)
            self.ids.sm.current = "result_screen"

        ###############################################Flashes#####################################################
        elif question_text=="Are the flashes unilateral or bilateral?" and btn_text=="Unilateral":
            self.ids.flashes_question.text = "Did these flashes come on suddenly or gradually?"
            self.ids.flashes_btn1.text="Suddenly"
            self.ids.flashes_btn2.text = "Gradually"

            print('unilateral')
            self.flashes_list = []
            self.flashes_diag.extend(["pvd", "tear)", "detach)", "migraine"])
            print(self.flashes_diag)

        elif question_text=="Are the flashes unilateral or bilateral?" and btn_text=="Bilateral":
            self.ids.flashes_question.text = "Did these flashes come on suddenly or gradually?"
            self.ids.flashes_btn1.text="Suddenly"
            self.ids.flashes_btn2.text = "Gradually"

            print('bilateral')
            self.flashes_list = []
            self.flashes_diag.extend(["pvd", "tear)", "detach)"])
            print(self.flashes_diag)

        elif question_text=="Did these flashes come on suddenly or gradually?" and btn_text=="Suddenly":
            self.ids.flashes_question.text ="Do the flashes occur in transient episodes? if YES state whether seconds,or up to an hour?"
            self.ids.flashes_btn1.text = "Seconds"
            self.ids.flashes_btn2.text = "Hour"
            self.ids.flashes_btn3.text = "No"
            self.ids.flashes_btn3.disabled=False

            print('suddenly')
            self.flashes_diag.extend(["pvd", "tear)", "detach)"])
            print(self.flashes_diag)

        elif question_text=="Did these flashes come on suddenly or gradually?" and btn_text=="Gradually":
            self.ids.flashes_question.text ="Do the flashes occur in transient episodes? if YES state whether seconds,or up to an hour?"
            self.ids.flashes_btn1.text = "Seconds"
            self.ids.flashes_btn2.text = "Hour"
            self.ids.flashes_btn3.text = "No"
            self.ids.flashes_btn3.disabled=False

            print('gradually')
            self.flashes_diag.extend(["pvd", "tear)", "detach)", "migraine", "tia", "braindis"])
            print(self.flashes_diag)

        elif question_text=="Do the flashes occur in transient episodes? if YES state whether seconds,or up to an hour?" and btn_text=="Seconds":
            self.ids.flashes_btn3.disabled = True
            self.ids.flashes_question.text ="Are the flashes recurrent?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            print('seconds')
            self.flashes_diag.extend(["tia", "braindis"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="Do the flashes occur in transient episodes? if YES state whether seconds,or up to an hour?" and btn_text=="Hour":
            self.ids.flashes_btn3.disabled = True
            self.ids.flashes_question.text ="Are the flashes recurrent?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            print('hours')
            self.flashes_diag.extend(["pvd", "tear)", "detach)", "tia"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="Do the flashes occur in transient episodes? if YES state whether seconds,or up to an hour?" and btn_text=="No":
            self.ids.flashes_btn3.disabled = True
            self.ids.flashes_question.text ="Are the flashes recurrent?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            print('no hours seconds')
            self.flashes_diag.extend(["pvd", "tear)", "detach)"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="Are the flashes recurrent?" and btn_text=="Yes":
            self.ids.flashes_question.text = "Is floaters present?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            print('headache recurrent yes')
            self.flashes_diag.extend(["migraine", "braindis"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="Are the flashes recurrent?" and btn_text=="No":
            self.ids.flashes_question.text = "Is floaters present?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            self.flashes_diag.extend(["pvd", "tear)", "detach)", "tia"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="Is floaters present?" and btn_text=="Yes":
            self.ids.flashes_question.text = "Flashes/flickers lights?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            print('yes floaters')
            self.flashes_diag.extend(["pvd", "tear)", "detach)"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="Is floaters present?" and btn_text=="No":
            self.ids.flashes_question.text = "Flashes/flickers lights?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            print('no Floaters')
            self.flashes_diag.extend(["migraine", "tia", "braindis"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)
            self.flashes_list = []

        elif question_text=="Flashes/flickers lights?" and btn_text=="Yes":
            self.ids.flashes_question.text = "zig zag / sparkling lights?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            print('peri')
            self.flashes_diag.extend(["pvd", "tear)", "detach)"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)
            self.flashes_list = []

        elif question_text=="Flashes/flickers lights?" and btn_text=="No":
            self.ids.flashes_question.text = "zig zag / sparkling lights?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            print('shdaow')
            self.flashes_diag.extend(["migraine", "tia", "braindis"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)
            self.flashes_list = []

        elif question_text=="zig zag / sparkling lights?" and btn_text=="Yes":
            self.ids.flashes_question.text = "Do you have vertigo, limb weakness?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            self.flashes_diag.extend(["migraine", "tia", "braindis"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="zig zag / sparkling lights?" and btn_text=="No":
            self.ids.flashes_question.text = "Do you have vertigo, limb weakness?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            self.flashes_diag.extend(["pvd", "tear)", "detach)"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="Do you have vertigo, limb weakness?" and btn_text=="Yes":
            self.ids.flashes_question.text ="Are you high myope >-3.00D?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            self.flashes_diag.extend(["tia", "braindis"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="Do you have vertigo, limb weakness?" and btn_text=="No":
            self.ids.flashes_question.text ="Are you high myope >-3.00D?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            self.flashes_diag.extend(["pvd", "tear)", "detach)"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="Are you high myope >-3.00D?" and btn_text=="Yes":
            self.ids.flashes_question.text ="prev surgery?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            self.flashes_diag.extend(["tear)", "detach)"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="Are you high myope >-3.00D?" and btn_text=="No":
            self.ids.flashes_question.text ="prev surgery?"
            self.ids.flashes_btn1.text = "Yes"
            self.ids.flashes_btn2.text = "No"

            self.flashes_diag.extend(["pvd", "migraine", "tia", "braindis"])
            print("CURRENT DIAGNOSIS:", self.flashes_diag)

        elif question_text=="prev surgery?" and btn_text=="Yes":
            self.flashes_diag.extend(["tear)", "detach)"])

            today = datetime.today().strftime("%m/%d %H:%M")
            history = open(self.username + ".txt", "a+")
            history.write("<--->\n")
            history.write(f"{str(today)}\n")
            history.write(f"{instance}\n")
            history.write(diagrams[instance])
            history.write('\n\nResult:')
            history.close()

            count = Counter(self.flashes_diag).items()
            percentages = {x: int(float(y) / len(self.flashes_diag) * 100) for x, y in count}
            if self.ids.lst_placeholder.children:
                self.ids.lst_placeholder.remove_widget(self.ids.lst_placeholder.children[0])
            boxlayout = MDBoxLayout(adaptive_height=True, orientation="vertical", spacing=15)
            self.ids.lst_placeholder.add_widget(boxlayout)
            self.ids.heading.text = "Flashes of Light"
            self.ids.heading_img.source = "icon_folder/BlueEye.png"
            history=open(self.username+".txt", "a+")

            sorted_percentages = sorted(percentages.items(), key=lambda vari: vari[1], reverse=True)
            for i in sorted_percentages:
                history.write(f"{i[0]}:    {i[1]}%\n")
                label_widget = MDLabel(text=f"{i[0]} - {i[1]} %", size_hint_y=None, height=50, halign="center",
                                       md_bg_color=(212 / 255, 175 / 255, 185 / 255, 0.3), radius=10)
                boxlayout.add_widget(label_widget)
                # self.ids['result'].text = f"FINAL DIAGNOSIS: ('%s - %s%s' % (name, pct, '%')"
            # self.ids.percent.text = str(percentages)
            history.write("\n\n")
            history.close()
            storage.child(self.username + ".txt").put(self.username + ".txt")
            print(percentages)
            self.cancelTest(instance)
            self.ids.sm.current = "result_screen"
        elif question_text=="prev surgery?" and btn_text=="No":
            self.flashes_diag.extend(["pvd", "migraine", "tia", "brain dis"])

            today = datetime.today().strftime("%m/%d %H:%M")
            history = open(self.username + ".txt", "a+")
            history.write("<--->\n")
            history.write(f"{str(today)}\n")
            history.write(f"{instance}\n")
            history.write(diagrams[instance])
            history.write('\n\nResult:')
            history.close()

            count = Counter(self.flashes_diag).items()
            percentages = {x: int(float(y) / len(self.flashes_diag) * 100) for x, y in count}
            if self.ids.lst_placeholder.children:
                self.ids.lst_placeholder.remove_widget(self.ids.lst_placeholder.children[0])
            boxlayout = MDBoxLayout(adaptive_height=True, orientation="vertical", spacing=15)
            self.ids.lst_placeholder.add_widget(boxlayout)
            self.ids.heading.text="Flashes of Light"
            self.ids.heading_img.source="icon_folder/BlueEye.png"
            history=open(self.username+".txt", "a+")

            sorted_percentages = sorted(percentages.items(), key=lambda vari: vari[1], reverse=True)
            for i in sorted_percentages:
                history.write(f"{i[0]}:    {i[1]}%\n")
                label_widget = MDLabel(text=f"{i[0]} - {i[1]} %", size_hint_y=None, height=50, halign="center",
                                       md_bg_color=(212 / 255, 175 / 255, 185 / 255, 0.3), radius=10)
                boxlayout.add_widget(label_widget)
                # self.ids['result'].text = f"FINAL DIAGNOSIS: ('%s - %s%s' % (name, pct, '%')"
            # self.ids.percent.text = str(percentages)
            history.write("\n\n")
            history.close()
            storage.child(self.username + ".txt").put(self.username + ".txt")
            print(percentages)
            self.cancelTest(instance)
            self.ids.sm.current = "result_screen"
    #########################################Anisicoria##########################################################
        elif question_text=="Is it recent or longstanding?" and btn_text=="Recent":
            self.ids.anisicoria_question.text = "Is there any vision loss?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_list = []
            self.anisicoria_diag.extend(["horner SAME", "3rd Nerve Palsy", "Uveitis", "Closed AGA"])
            print(self.anisicoria_diag)
        elif question_text=="Is it recent or longstanding?" and btn_text=="Longstanding":
            self.ids.anisicoria_question.text = "Is there any vision loss?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_list = []
            self.anisicoria_diag.extend(["physiological", "Adies", "Horner Routine"])
            print(self.anisicoria_diag)
        elif question_text== "Is there any vision loss?" and btn_text=="Yes":
            self.ids.anisicoria_question.text = "Is there any double vision?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(["Adies", "Uveitis", "Closed AGA"])
            print(self.anisicoria_diag)
        elif question_text== "Is there any vision loss?" and btn_text=="No":
            self.ids.anisicoria_question.text = "Is there any double vision?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(["physiological", "3rd Nerve Palsy", "Horner Routine", "horner SAME"])
            print(self.anisicoria_diag)
        elif question_text=="Is there any double vision?" and btn_text=="Yes":
            self.ids.anisicoria_question.text ="Is there any pain?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(["3rd Nerve Palsy"])
            print(self.anisicoria_diag)
        elif question_text=="Is there any double vision?" and btn_text=="No":
            self.ids.anisicoria_question.text ="Is there any pain?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(
                ["physiological", "Adies", "Uveitis", "Closed AGA", "Horner Routine", "horner SAME"])
            print(self.anisicoria_diag)
        elif question_text=="Is there any pain?" and btn_text=="Yes":
            self.ids.anisicoria_question.text = "Is there any light sensitivity?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(["Uveitis", "Closed AGA"])
            print(self.anisicoria_diag)
        elif question_text=="Is there any pain?" and btn_text=="No":
            self.ids.anisicoria_question.text = "Is there any light sensitivity?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(["physiological", "Adies", "3rd Nerve Palsy", "Horner Routine", "horner SAME"])
            print(self.anisicoria_diag)
        elif question_text=="Is there any light sensitivity?" and btn_text=="Yes":
            self.ids.anisicoria_question.text ="Is there any haloes around lights?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(["Uveitis"])
            print(self.anisicoria_diag)
        elif question_text=="Is there any light sensitivity?" and btn_text=="No":
            self.ids.anisicoria_question.text ="Is there any haloes around lights?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(
                ["physiological", "Adies", "3rd Nerve Palsy", "Horner Routine", "horner SAME", "Closed AGA"])
            print(self.anisicoria_diag)
        elif question_text=="Is there any haloes around lights?" and btn_text=="Yes":
            self.ids.anisicoria_question.text ="Have you had previous uveitis?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(["Closed AGA"])
            print(self.anisicoria_diag)
        elif question_text=="Is there any haloes around lights?" and btn_text=="No":
            self.ids.anisicoria_question.text ="Have you had previous uveitis?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(
                ["physiological", "Adies", "3rd Nerve Palsy", "Horner Routine", "horner SAME", "Uveitis"])
            print(self.anisicoria_diag)
        elif question_text=="Have you had previous uveitis?" and btn_text=="Yes":
            self.ids.anisicoria_question.text ="Do you have diabetes or high blood pressure?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(["Uveitis"])
            print(self.anisicoria_diag)
        elif question_text=="Have you had previous uveitis?" and btn_text=="No":
            self.ids.anisicoria_question.text ="Do you have diabetes or high blood pressure?"
            self.ids.anisicoria_btn1.text = "Yes"
            self.ids.anisicoria_btn2.text = "No"
            self.anisicoria_diag.extend(
                ["physiological", "Adies", "3rd Nerve Palsy", "Horner Routine", "horner SAME", "Closed AGA"])
            print(self.anisicoria_diag)
        elif question_text=="Do you have diabetes or high blood pressure?" and btn_text=="Yes":
            self.anisicoria_diag.extend(["3rd Nerve Palsy"])

            today = datetime.today().strftime("%m/%d %H:%M")
            history = open(self.username + ".txt", "a+")
            history.write("<--->\n")
            history.write(f"{str(today)}\n")
            history.write(f"{instance}\n")
            history.write(diagrams[instance])
            history.write('\n\nResult:')
            history.close()

            count3 = Counter(self.anisicoria_diag).items()
            percentages3 = {x: int(float(y) / len(self.anisicoria_diag) * 100) for x, y in count3}
            if self.ids.lst_placeholder.children:
                self.ids.lst_placeholder.remove_widget(self.ids.lst_placeholder.children[0])
            boxlayout = MDBoxLayout(adaptive_height=True, orientation="vertical", spacing=15)
            self.ids.lst_placeholder.add_widget(boxlayout)
            self.ids.heading.text="Anisicoria"
            self.ids.heading_img.source="icon_folder/PupilEye2.png"
            history=open(self.username+".txt", "a+")

            sorted_percentages = sorted(percentages3.items(), key=lambda vari: vari[1], reverse=True)
            for i in sorted_percentages:
                history.write(f"{i[0]}:    {i[1]}%\n")
                label_widget = MDLabel(text=f"{i[0]} - {i[1]} %", size_hint_y=None, height=50, halign="center",
                                       md_bg_color=(212 / 255, 175 / 255, 185 / 255, 0.3), radius=10)
                boxlayout.add_widget(label_widget)
                # self.ids['result'].text = f"FINAL DIAGNOSIS: ('%s - %s%s' % (name, pct, '%')"
            # self.ids.percent.text = str(percentages)
            history.write("\n\n")
            history.close()
            storage.child(self.username + ".txt").put(self.username + ".txt")
            print(percentages3)
            self.cancelTest(instance)
            self.ids.sm.current = "result_screen"
        elif question_text=="Do you have diabetes or high blood pressure?" and btn_text=="No":
            self.anisicoria_diag.extend(
                ["physiological", "Adies", "Uveitis", "Closed AGA", "Horner Routine", "horner SAME"])

            today = datetime.today().strftime("%m/%d %H:%M")
            history = open(self.username + ".txt", "a+")
            history.write("<--->\n")
            history.write(f"{str(today)}\n")
            history.write(f"{instance}\n")
            history.write(diagrams[instance])
            history.write('\n\nResult:')
            history.close()

            count3 = Counter(self.anisicoria_diag).items()
            percentages3 = {x: int(float(y) / len(self.anisicoria_diag) * 100) for x, y in count3}
            if self.ids.lst_placeholder.children:
                self.ids.lst_placeholder.remove_widget(self.ids.lst_placeholder.children[0])
            boxlayout = MDBoxLayout(adaptive_height=True, orientation="vertical", spacing=15)
            self.ids.lst_placeholder.add_widget(boxlayout)
            self.ids.heading.text = "Anisicoria"
            self.ids.heading_img.source = "icon_folder/PupilEye2.png"
            history = open(self.username + ".txt", "a+")

            sorted_percentages = sorted(percentages3.items(), key=lambda vari: vari[1], reverse=True)
            for i in sorted_percentages:
                history.write(f"{i[0]}:    {i[1]}%\n")
                label_widget = MDLabel(text=f"{i[0]} - {i[1]} %", size_hint_y=None, height=50, halign="center",
                                       md_bg_color=(212 / 255, 175 / 255, 185 / 255, 0.3), radius=10)
                boxlayout.add_widget(label_widget)
                # self.ids['result'].text = f"FINAL DIAGNOSIS: ('%s - %s%s' % (name, pct, '%')"
            # self.ids.percent.text = str(percentages)
            history.write("\n")
            history.close()
            storage.child(self.username + ".txt").put(self.username + ".txt")
            print(percentages3)
            self.cancelTest(instance)
            self.ids.sm.current = "result_screen"
class DiagnosticApp(MDApp):
    pass
DiagnosticApp().run()