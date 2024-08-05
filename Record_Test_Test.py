import sounddevice as sd
import wavio as wv

import speech_recognition as sr
import pyttsx3

import smtplib
import ssl
from email.message import EmailMessage

# ========================================= Functions ======================================= #
def record(msg_section, duration):
    #Samping frequency
    frequency = 44100

    #Initialize recorder with the given values for duration and sample frequency
    record = sd.rec(int(duration * frequency), samplerate = frequency, channels = 2)

    #Record audio for the given duration
    sd.wait()

    #Convert the NumPy array to audio file
    wv.write(msg_section+'.wav', record, frequency, sampwidth = 2)
    r = sr.Recognizer()
    
    audio = sr.AudioFile(msg_section+'.wav')
    with audio as src:
        audio = r.record(src)
        msg_line = r.recognize_google(audio)
        
    #Initialize array to store split-up audio-to-text
    msg_split = []

    #Append audio-to-text, after capitalization
    for i in msg_line.split():
        msg_split.append(i.capitalize())

    #Initialize variable to join the split text
    msg_join = ''

    #If 'Sender_Name' or 'Receiver_Name', returns 'None after below function, otherwise skip
    if (msg_section == 'Sender_FName' or msg_section == 'Sender_LName' or msg_section == 'Receiver_Name'):
        msg_greeting(msg_split, msg_join, msg_section)
        return
    
    #Join the split text
    for i in msg_split:
        msg_join += i
        msg_join += ' '
    msg_join = msg_join[0:len(msg_join)-1]

    num_dict = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9}

    for num in num_dict.keys():
        if msg_join == num:
            msg_join = num_dict[num]

    #Store the final text as an individual message section
    msg[msg_section] = msg_join
    

def msg_greeting(msg_split, msg_join, msg_section):
    #Join the split text
    for i in msg_split:
        msg_join += i

    #Lower all letters of name
    msg_join = msg_join.lower()
    #Capitalize the result
    msg_join = msg_join.capitalize()

    #Store the final text as an individual message section
    msg[msg_section] = msg_join

# ========================================= Functions ======================================= #

# =========================================== Main ========================================= #
    
#Initialize message array
msg = {}

engine = pyttsx3.init()

#Record audio for 'Subject'
engine.say('Enter the Subject')
engine.runAndWait()

record('Subject', 5)

#Record the 'Sender Name' and 'Sender_LName'
engine.say('Enter your First Name')
engine.runAndWait()
record('Sender_FName', 5)

engine.say('Enter your Last Name')
engine.runAndWait()
record('Sender_LName', 5)

#Record audio for 'Salutation'
engine.say('Enter the Salutation')
engine.runAndWait()
record('Salutation', 5)

#Record the 'Receiver Name'
engine.say('Enter the Receiver Name')
engine.runAndWait()
record('Receiver_Name', 5)

#Record the number of paragraphs
engine.say('Enter the Number of Paragraphs')
engine.runAndWait()
record('Paragraph_Count', 5)

for i in range(msg['Paragraph_Count']):
    #Enter number of lines for every paragraph
    engine.say('Enter the Number of Lines for Paragraph ' + str(i+1))
    engine.runAndWait()
    record('Line_Count', 5)

    for j in range(int(msg['Line_Count'])):
        #Record audio for every line
        engine.say('Enter Line ' + str(j+1) + ' of Paragraph ' + str(i+1))
        engine.runAndWait()
        record(str(i+1)+str(j+1), 5)

#Record audio for 'Closing'
engine.say('Enter the Closing')
engine.runAndWait()
record('Closing', 5)

print('Subject:', msg['Subject'])
print('')
print(msg['Salutation'], msg['Receiver_Name'] + ',')
print('')

for i in range(msg['Paragraph_Count']):
    for j in range(msg['Line_Count']):
        print(msg[str(i+1)+str(j+1)], end = '. ')
    print('')
    print('')

print(msg['Closing'] + ',')
print(msg['Sender_FName'], msg['Sender_LName'])
    
email_sender = 'yohanrajumavely@hotmail.com'
email_password = 'JesusChrist'
email_receiver = 'yohanmavely@gmail.com'

email_subject = msg['Subject']

body = ''

body += msg['Salutation'] + ' ' + msg['Receiver_Name'] + ','
body += '\n\n'

for i in range(msg['Paragraph_Count']):
    for j in range(msg['Line_Count']):
        body += msg[str(i+1)+str(j+1)]
        body += '. '
    body += '\n'

body += '\n'
body += msg['Closing'] + ','
body += '\n'
body += msg['Sender_FName'] + ' ' + msg['Sender_LName']

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = email_subject
em.set_content(body)

for i in range(msg['Paragraph_Count']):
    for j in range(msg['Line_Count']):
        with open(str(i+1)+str(j+1)+'.wav', 'rb') as f:
            file_data = f.read()
            file_name = f.name
            em.add_attachment(file_data, maintype = 'application', subtype = 'wav', filename = file_name)

context = ssl.create_default_context()

with smtplib.SMTP('smtp.outlook.com', 587) as smtp:
    smtp.starttls(context=context)
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())
    
engine.say('The mail has been successfully sent to '+str(msg['Receiver_Name']))
engine.runAndWait()
