
import os,time,threading
from playsound import playsound
import smtplib
import email
import imaplib
import speech_recognition as sr
from gtts import gTTS
from email.header import decode_header
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.animation import Animation
from kivy.clock import Clock, mainthread
from kivy.uix.gridlayout import GridLayout

from CONSTANTS import EMAIL_ID, PASSWORD, LANGUAGE

Builder.load_string("""
<AnimWidget@Widget>:
    canvas:
        Color:
            rgba: 0.7, 0.3, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size
    size_hint: None, None
    size: 400, 30


<RootWidget>:
    cols: 1

    canvas:
        Color:
            rgba: 0.9, 0.9, 0.9, 1
        Rectangle:
            pos: self.pos
            size: self.size

    anim_box: anim_box
    but_1: but_1
    lab_1: lab_1
    lab_2: lab_2

    Button:
        id: but_1
        font_size: 20
        text: 'Start second thread'
        on_press: root.start_second_thread(lab_2.text)

    Label:
        id: lab_1
        font_size: 30
        color: 0.6, 0.6, 0.6, 1
        text_size: self.width, None
        halign: 'center'

    AnchorLayout:
        id: anim_box

    Label:
        id: lab_2
        font_size: 100
        color: 0.8, 0, 0, 1
        text: '3'
""")


class RootWidget(GridLayout):

    stop = threading.Event()

    def start_second_thread(self, l_text):
        threading.Thread(target=self.main,).start()

    def StartAnimation(self, *args):
        self.remove_widget(self.but_1)
        self.lab_1.text = ('The UI remains responsive while the '
                           'second thread is running.')

        anim_bar = Factory.AnimWidget()
        self.anim_box.add_widget(anim_bar)

        anim = Animation(opacity=0.3, width=100, duration=0.6)
        anim += Animation(opacity=1, width=400, duration=0.8)
        anim.repeat = True
        anim.start(anim_bar)

    @mainthread
    def printMsg(self, msgtxt):
        self.lab_1.text = msgtxt

    @mainthread
    def StopAnimation(self):
        self.lab_1.text = ('Second thread exited, a new thread has started. '
                           'Close the app to exit the new thread and stop '
                           'the main process.')

        self.lab_2.text = str(int(self.lab_2.text) + 1)

        self.remove_widget(self.anim_box)


    def SpeakText(self, command, langinp=LANGUAGE):
        """
        Text to Speech using GTTS

        Args:
            command (str): Text to speak
            langinp (str, optional): Output language. Defaults to "en".
        """
        self.printMsg(command)
        if langinp == "": langinp = "en"
        try:
            tts = gTTS(text=command, lang=langinp)
            tts.save("~tempfile01.mp3")
            playsound("~tempfile01.mp3")
            os.remove("~tempfile01.mp3")
        except:
            print("cannot play")
        return None

    def speech_to_text(self):
        """
        Speech to text

        Returns:
            str: Returns transcripted text
        """

        self.printMsg("Listning...")
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=0.1)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                print("You said: "+MyText)
                return MyText

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            return None

        except sr.UnknownValueError:
            print("unknown error occured")
            return None


    def sendMail(self, sendTo, msg):
        """
        To send a mail

        Args:
            sendTo (list): List of mail targets
            msg (str): Message
        """
        mail = smtplib.SMTP('smtp.gmail.com', 587)  # host and port
        # Hostname to send for this command defaults to the FQDN of the local host.
        mail.ehlo()
        mail.starttls()  # security connection
        mail.login(EMAIL_ID, PASSWORD)  # login part
        for person in sendTo:
            mail.sendmail(EMAIL_ID, person, msg)  # send part
            print("Mail sent successfully to " + person)
        mail.close()


    def composeMail(self):
        """
        Compose and create a Mail

        Returns:
            None: None
        """
        self.SpeakText("Mention the gmail ID of the persons to whom you want to send a mail. Email IDs should be separated with the word, AND.")
        receivers = self.speech_to_text()
        receivers = receivers.replace("at the rate", "@")
        emails = receivers.split(" and ")
        index = 0
        for email in emails:
            emails[index] = email.replace(" ", "")
            index += 1

        self.SpeakText("The mail will be send to " +
                (' and '.join([str(elem) for elem in emails])) + ". Confirm by saying YES or NO.")
        confirmMailList = self.speech_to_text()

        if confirmMailList.lower() != "yes":
            self.SpeakText("Operation cancelled by the user")
            return None

        self.SpeakText("Say your message")
        msg = self.speech_to_text()

        self.SpeakText("You said  " + msg + ". Confirm by saying YES or NO.")
        confirmMailBody = self.speech_to_text()
        if confirmMailBody.lower() == "yes":
            self.SpeakText("Message sent")
            self.sendMail(emails, msg)
        else:
            self.SpeakText("Operation cancelled by the user")
            return None


    def getMailBoxStatus(self):
        """
        Get mail counts of all folders in the mailbox
        """
        # host and port (ssl security)
        M = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        M.login(EMAIL_ID, PASSWORD)  # login

        for i in M.list()[1]:
            l = i.decode().split(' "/" ')
            if l[1] == '"[Gmail]"':
                continue

            stat, total = M.select(f'{l[1]}')
            l[1] = l[1][1:-1]
            messages = int(total[0])
            if l[1] == 'INBOX':
                self.SpeakText(l[1] + " has " + str(messages) + " messages.")
            else:
                self.SpeakText(l[1].split("/")[-1] + " has " + str(messages) + " messages.")

        M.close()
        M.logout()


    def clean(self, text):
        """
        clean text for creating a folder
        """
        return "".join(c if c.isalnum() else "_" for c in text)


    def getLatestMails(self):
        """
        Get latest mails from folders in mailbox (Defaults to 3 Inbox mails)
        """
        mailBoxTarget = "INBOX"
        self.SpeakText("Choose the folder name to get the latest mails. Say 1 for Inbox. Say 2 for Sent Mailbox. Say 3 for Drafts. Say 4 for important mails. Say 5 for Spam. Say 6 for Starred Mails. Say 7 for Bin.")
        cmb = self.speech_to_text()
        if cmb == "1" or cmb.lower() == "one":
            mailBoxTarget = "INBOX"
            self.SpeakText("Inbox selected.")
        elif cmb == "2" or cmb.lower() == "two" or cmb.lower() == "tu":
            mailBoxTarget = '"[Gmail]/Sent Mail"'
            self.SpeakText("Sent Mailbox selected.")
        elif cmb == "3" or cmb.lower() == "three":
            mailBoxTarget = '"[Gmail]/Drafts"'
            self.SpeakText("Drafts selected.")
        elif cmb == "4" or cmb.lower() == "four":
            mailBoxTarget = '"[Gmail]/Important"'
            self.SpeakText("Important Mails selected.")
        elif cmb == "5" or cmb.lower() == "five":
            mailBoxTarget = '"[Gmail]/Spam"'
            self.SpeakText("Spam selected.")
        elif cmb == "6" or cmb.lower() == "six":
            mailBoxTarget = '"[Gmail]/Starred"'
            self.SpeakText("Starred Mails selected.")
        elif cmb == "7" or cmb.lower() == "seven":
            mailBoxTarget = '"[Gmail]/Bin"'
            self.SpeakText("Bin selected.")
        else:
            self.SpeakText("Wrong choice. Hence, default option Inbox wil be selected.")

        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(EMAIL_ID, PASSWORD)

        status, messages = imap.select(mailBoxTarget)
        
        messages = int(messages[0])

        if messages == 0:
            self.SpeakText("Selected MailBox is empty.")
            return None
        elif messages == 1:
            N = 1   # number of top emails to fetch
        elif messages == 2:
            N = 2   # number of top emails to fetch
        else:
            N = 3   # number of top emails to fetch

        msgCount = 1
        for i in range(messages, messages-N, -1):
            self.SpeakText(f"Message {msgCount}:")
            res, msg = imap.fetch(str(i), "(RFC822)")   # fetch the email message by ID
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])     # parse a bytes email into a message object

                    subject, encoding = decode_header(msg["Subject"])[0]    # decode the email subject
                    if isinstance(subject, bytes): 
                        subject = subject.decode(encoding)      # if it's a bytes, decode to str
                    
                    From, encoding = decode_header(msg.get("From"))[0]      # decode email sender
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    self.SpeakText("Subject: " + subject)
                    FromArr = From.split()
                    FromName = " ".join(namechar for namechar in FromArr[0:-1])
                    self.SpeakText("From: " + FromName)
                    self.SpeakText("Sender mail: " + FromArr[-1])
                    self.SpeakText("The mail says or contains the following:")
                    
                    # MULTIPART
                    if msg.is_multipart(): 
                        for part in msg.walk(): # iterate over email parts
                            content_type = part.get_content_type()      # extract content type of email
                            content_disposition = str(
                                part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()   # get the email body
                            except:
                                pass

                            # PLAIN TEXT MAIL
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                self.SpeakText("Do you want to listen to the text content of the mail ? Please say YES or NO.")
                                talkMSG1 = self.speech_to_text()
                                if "yes" in talkMSG1.lower():
                                    self.SpeakText("The mail body contains the following:")
                                    self.SpeakText(body)
                                else:
                                    self.SpeakText("You chose NO")

                            # MAIL WITH ATTACHMENT
                            elif "attachment" in content_disposition:
                                self.SpeakText("The mail contains attachment, the contents of which will be saved in respective folders with it's name similar to that of subject of the mail")
                                filename = part.get_filename()  # download attachment
                                if filename:
                                    folder_name = self.clean(subject)
                                    if not os.path.isdir(folder_name):
                                        os.mkdir(folder_name)   # make a folder for this email (named after the subject)
                                    filepath = os.path.join(folder_name, filename)
                                    open(filepath, "wb").write(part.get_payload(decode=True))   # download attachment and save it
                    
                    # NOT MULTIPART
                    else:
                        content_type = msg.get_content_type()    # extract content type of email
                        body = msg.get_payload(decode=True).decode()    # get the email body
                        if content_type == "text/plain":
                            self.SpeakText("Do you want to listen to the text content of the mail ? Please say YES or NO.")
                            talkMSG2 = self.speech_to_text()
                            if "yes" in talkMSG2.lower():
                                self.SpeakText("The mail body contains the following:")
                                self.SpeakText(body)
                            else:
                                self.SpeakText("You chose NO")


                    # HTML CONTENTS
                    if content_type == "text/html":
                        self.SpeakText("The mail contains an HTML part, the contents of which will be saved in respective folders with it's name similar to that of subject of the mail. You can view the html files in any browser, simply by clicking on them.")
                        # if it's HTML, create a new HTML file
                        folder_name = self.clean(subject)
                        if not os.path.isdir(folder_name):  
                            os.mkdir(folder_name)   # make a folder for this email (named after the subject)
                        filename = "index.html"
                        filepath = os.path.join(folder_name, filename)
                        # write the file
                        open(filepath, "w").write(body)
                        
                        # webbrowser.open(filepath)     # open in the default browser

                    self.SpeakText(f"\nEnd of message {msgCount}:")
                    msgCount += 1
                    print("="*100)
        imap.close()
        imap.logout()


    def searchMail(self):
        """
        Search mails by subject / author mail ID

        Returns:
            None: None
        """
        M = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        M.login(EMAIL_ID, PASSWORD)

        mailBoxTarget = "INBOX"
        self.SpeakText("Where do you want to search ? Say 1 for Inbox. Say 2 for Sent Mailbox. Say 3 for Drafts. Say 4 for important mails. Say 5 for Spam. Say 6 for Starred Mails. Say 7 for Bin.")
        cmb = self.speech_to_text()
        if cmb == "1" or cmb.lower() == "one":
            mailBoxTarget = "INBOX"
            self.SpeakText("Inbox selected.")
        elif cmb == "2" or cmb.lower() == "two" or cmb.lower() == "tu":
            mailBoxTarget = '"[Gmail]/Sent Mail"'
            self.SpeakText("Sent Mailbox selected.")
        elif cmb == "3" or cmb.lower() == "three":
            mailBoxTarget = '"[Gmail]/Drafts"'
            self.SpeakText("Drafts selected.")
        elif cmb == "4" or cmb.lower() == "four":
            mailBoxTarget = '"[Gmail]/Important"'
            self.SpeakText("Important Mails selected.")
        elif cmb == "5" or cmb.lower() == "five":
            mailBoxTarget = '"[Gmail]/Spam"'
            self.SpeakText("Spam selected.")
        elif cmb == "6" or cmb.lower() == "six":
            mailBoxTarget = '"[Gmail]/Starred"'
            self.SpeakText("Starred Mails selected.")
        elif cmb == "7" or cmb.lower() == "seven":
            mailBoxTarget = '"[Gmail]/Bin"'
            self.SpeakText("Bin selected.")
        else:
            self.SpeakText("Wrong choice. Hence, default option Inbox wil be selected.")


        M.select(mailBoxTarget)

        self.SpeakText("Say 1 to search mails from a specific sender. Say 2 to search mail with respect to the subject of the mail.")
        mailSearchChoice = self.speech_to_text()
        if mailSearchChoice == "1" or mailSearchChoice.lower() == "one":
            self.SpeakText("Please mention the sender email ID you want to search.")
            searchSub = self.speech_to_text()
            searchSub = searchSub.replace("at the rate", "@")
            searchSub = searchSub.replace(" ", "")
            status, messages = M.search(None, f'FROM "{searchSub}"')
        elif mailSearchChoice == "2" or mailSearchChoice.lower() == "two" or mailSearchChoice.lower() == "tu":
            self.SpeakText("Please mention the subject of the mail you want to search.")
            searchSub = self.speech_to_text()
            status, messages = M.search(None, f'SUBJECT "{searchSub}"')
        else:
            self.SpeakText("Wrong choice. Performing default operation. Please mention the subject of the mail you want to search.")
            searchSub = self.speech_to_text()
            status, messages = M.search(None, f'SUBJECT "{searchSub}"')
        
        
        if str(messages[0]) == "b''":
            self.SpeakText(f"Mail not found in {mailBoxTarget}.")
            return None

        msgCount = 1
        for i in messages:
            self.SpeakText(f"Message {msgCount}:")
            res, msg = M.fetch(i, "(RFC822)")   # fetch the email message by ID
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])     # parse a bytes email into a message object

                    subject, encoding = decode_header(msg["Subject"])[0]    # decode the email subject
                    if isinstance(subject, bytes): 
                        subject = subject.decode(encoding)      # if it's a bytes, decode to str
                    
                    From, encoding = decode_header(msg.get("From"))[0]      # decode email sender
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    self.SpeakText("Subject: " + subject)
                    FromArr = From.split()
                    FromName = " ".join(namechar for namechar in FromArr[0:-1])
                    self.SpeakText("From: " + FromName)
                    self.SpeakText("Sender mail: " + FromArr[-1])

                    # MULTIPART
                    if msg.is_multipart(): 
                        for part in msg.walk(): # iterate over email parts
                            content_type = part.get_content_type()      # extract content type of email
                            content_disposition = str(
                                part.get("Content-Disposition"))
                            try:
                                body = part.get_payload(decode=True).decode()   # get the email body
                            except:
                                pass

                            # PLAIN TEXT MAIL
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                self.SpeakText("Do you want to listen to the text content of the mail ? Please say YES or NO.")
                                talkMSG1 = self.speech_to_text()
                                if "yes" in talkMSG1.lower():
                                    self.SpeakText("The mail body contains the following:")
                                    self.SpeakText(body)
                                else:
                                    self.SpeakText("You chose NO")

                            # MAIL WITH ATTACHMENT
                            elif "attachment" in content_disposition:
                                self.SpeakText("The mail contains attachment, the contents of which will be saved in respective folders with it's name similar to that of subject of the mail")
                                filename = part.get_filename()  # download attachment
                                if filename:
                                    folder_name = self.clean(subject)
                                    if not os.path.isdir(folder_name):
                                        os.mkdir(folder_name)   # make a folder for this email (named after the subject)
                                    filepath = os.path.join(folder_name, filename)
                                    open(filepath, "wb").write(part.get_payload(decode=True))   # download attachment and save it
                    
                    # NOT MULTIPART
                    else:
                        content_type = msg.get_content_type()    # extract content type of email
                        body = msg.get_payload(decode=True).decode()    # get the email body
                        if content_type == "text/plain":
                            self.SpeakText("Do you want to listen to the text content of the mail ? Please say YES or NO.")
                            talkMSG2 = self.speech_to_text()
                            if "yes" in talkMSG2.lower():
                                self.SpeakText("The mail body contains the following:")
                                self.SpeakText(body)
                            else:
                                self.SpeakText("You chose NO")


                    # HTML CONTENTS
                    if content_type == "text/html":
                        self.SpeakText("The mail contains an HTML part, the contents of which will be saved in respective folders with it's name similar to that of subject of the mail. You can view the html files in any browser, simply by clicking on them.")
                        # if it's HTML, create a new HTML file
                        folder_name = self.clean(subject)
                        if not os.path.isdir(folder_name):  
                            os.mkdir(folder_name)   # make a folder for this email (named after the subject)
                        filename = "index.html"
                        filepath = os.path.join(folder_name, filename)
                        # write the file
                        open(filepath, "w").write(body)
                        
                        # webbrowser.open(filepath)     # open in the default browser

                    self.SpeakText(f"\nEnd of message {msgCount}:")
                    msgCount += 1
                    print("="*100)

        M.close()
        M.logout()

    def main(self):
        """
        Main function that handles primary choices
        """
        Clock.schedule_once(self.StartAnimation, 0)

        if EMAIL_ID != "" and PASSWORD != "":

            self.SpeakText("Choose and speak out the option number for the task you want to perform. Say 1 to send a mail. Say 2 to get your mailbox status. Say 3 to search a mail. Say 4 to get the last 3 mails.")
            choice = self.speech_to_text()
            choice = choice if choice else ''

            if choice == '1' or choice.lower() == 'one':
                self.composeMail()
            elif choice == '2' or choice.lower() == 'too' or choice.lower() == 'two' or choice.lower() == 'to' or choice.lower() == 'tu':
                self.getMailBoxStatus()
            elif choice == '3' or choice.lower() == 'tree' or choice.lower() == 'three':
                self.searchMail()
            elif choice == '4' or choice.lower() == 'four' or choice.lower() == 'for':
                self.getLatestMails()
            else:
                self.SpeakText("Wrong choice. Please say only the number")

        else:
            self.SpeakText("Both Email ID and Password should be present")

class RunApp(App):

    def on_stop(self):
        self.root.stop.set()

    def build(self):
        return RootWidget()

if __name__ == '__main__':
    RunApp().run()