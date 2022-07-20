from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.core.window import Window

histories = []

Window.size=(400,700)

class CustomWidget(ButtonBehavior, MDBoxLayout):
    pass
class Custom_Button(ButtonBehavior,Image):
    pass

class MainWidget(Screen):

    def switching_to_chat(self):
        self.ids.sm.current = "chat_screen"
        self.ids.sm.transition.direction = 'up'

    def showing_history(self):
        histories.clear()
        self.ids.historyItems.children.clear()
        copy,date,lineHistory,time,Name,Content = False,"","","","",""
        for line in open('ab12345.txt').readlines():
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
        
        self.ids.historyItems.height = ((len(histories)//2)+1)*125
        
        for i,child in enumerate(self.ids.historyItems.children):
            child.bind(on_press=self.showing_history_item)
            try:
                child.ids[f'historyItem_date_{i}'] = child.ids.pop('historyItem_date') # CHANGE ID OF ELEMENTS
                child.ids[f'historyItem_time_{i}'] = child.ids.pop('historyItem_time') # CHANGE ID OF ELEMENTS
                child.ids[f'historyItem_title_{i}'] = child.ids.pop('historyItem_title') # CHANGE ID OF ELEMENTS
                child.ids[f'historyItem_image_{i}'] = child.ids.pop('historyItem_image') # CHANGE ID OF ELEMENTS
                child.ids[f'historyItem_date_{i}'].text = histories[i]['date']
                child.ids[f'historyItem_time_{i}'].text = histories[i]['time']
                child.ids[f'historyItem_title_{i}'].text = histories[i]['name']
                child.ids[f'historyItem_image_{i}'].source = images[histories[i]['name']]
            except:pass

        self.ids.sm.current = "history_main_screen"
        self.ids.sm.transition.direction = 'left'

    def showing_history_item(self,ChildObject):
        id = ChildObject.parent.children.index(ChildObject)
        self.ids.history_name_placeholder.text = histories[id]['name']
        self.ids.history_placeholder.text = histories[id]['content']
        self.ids.history_date_placeholder.text = histories[id]['date']
        self.ids.history_time_placeholder.text = histories[id]['time']
        self.ids.sm.current = "history_screen"
        self.ids.sm.transition.direction = 'right'
        

class MainApp(MDApp):
    pass

MainApp().run()