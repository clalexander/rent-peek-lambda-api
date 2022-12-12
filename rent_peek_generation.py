#!/usr/bin/env python
# coding: utf-8

# In[1]:


#add all the imports we need

from utils import get_zipcode_coverage_data, get_rental_data, get_email_creds

#for pandas
# import pandas as pd

#for creating image
from PIL import Image, ImageFont, ImageDraw

#for email sending
import os
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
import mimetypes

#for random number generation
from random import randrange, randint


STORAGE_BASE_PATH = '/tmp/'


# In[2]:


## Variables

# user_input_data = 'rp_form_submission.csv'


# In[3]:


## Functions

#gets user info from .csv (which is taken from Wix form submission)
# def get_user_info(file):
#     df = pd.read_csv(file, index_col='Submission Time')
    
#     user_data = {
#     'zipcode': df.iloc[0]['Zipcode'] ,
#     'rent': df.iloc[0]['Your rent'] ,
#     'beds': df.iloc[0]['Bedrooms'] ,
#     'baths': df.iloc[0]['Bathrooms'] ,
#     'email': df.iloc[0]['Email'] ,
#     'userID': df.iloc[0]['User ID'] 
#     }
    
#     return (user_data)



#gets rent data 
#gets average rent and the number of entries that match user input
#sets ratio and comparision variables for image output (more/less and %)
#Checks if there are at least 10 entries for that zip/bed/bath combo
def get_data(user_data):
    # df = pd.read_csv('nyc_rental_data.csv', index_col='Date')
    df = get_rental_data()
    
    #checks to make sure zipcode is in list
    # df1 = pd.read_csv('zipcode_coverage.csv')
    df1 = get_zipcode_coverage_data()
    df1['Zipcode']
    if user_data['zipcode'] in df1['Zipcode'].unique():
        user_data['reason'] = 'ok'
    else:
        user_data['reason'] = 'zipcode'
        return(user_data)
        
    
    
    count = df.loc[ (df['Zipcode'] == user_data['zipcode']) 
                   & (df['Beds'] == str(user_data['beds'])) 
                   & (df['Baths'] == user_data['baths']), 
                   'Gross Rent'].count()
    
    count1 = df.loc[ (df['Zipcode'] == user_data['zipcode']) 
                    & (df['Beds'] == str(user_data['beds'])) 
                    & (df['Baths'] == user_data['baths']) 
                    & (df['Gross Rent'] < user_data['rent']), 
                    'Gross Rent'].count()
     
    user_data['count'] = round(count)
    
    if count < 10:
        user_data['reason'] = 'data'
        return(user_data)
    else:
        user_data['reason'] = 'ok'
    
    
    mean = df.loc[ (df['Zipcode'] == user_data['zipcode']) 
                  & (df['Beds'] == str(user_data['beds'])) 
                  & (df['Baths'] == user_data['baths']), 
                  'Gross Rent'].mean()
    
    ratio = count1 / count
    user_data['ratio'] = round(ratio*100)     
    
    user_data['avg_rent'] = round(mean)
        
    return (user_data)



#rounds the percentage to nearest 5 and selects the corresponding dial image
def get_file(percentage):
        percentage = 5 * round(percentage/5)
        # modified filepath to get image file
        filename = './imgs/dial_' + str(percentage) + '.png'
        file_name = Image.open(filename)
        return file_name
    
    
#creates the image and saves it to folder 'Results_output'      
def generate_output_img(user_data):
    
    # ______start______
    #formats the strings
    
    zipcode = str(user_data['zipcode'])
    beds = str(user_data['beds'])
    baths = str(user_data['baths'])
    rent = '$' + '{:,}'.format(user_data['rent'])
    avg_rent = '$' + '{:,}'.format(user_data['avg_rent'])
    total_users = str(user_data['count'] + randrange(121,214))
    # userID = str(user_data['userID'])
    percent = str(user_data['ratio'])
    
    
    # ______end________
    
    # ______start______
    #imports template image
    
    my_image = Image.open("./imgs/rent_template_2.png")
    
    # ______end________
    
    # ______start______
    #sets font type and size
    
    font = ImageFont.truetype('Roboto-Bold.ttf', 64)
    font2 = ImageFont.truetype('Roboto-Bold.ttf', 60)
    font3 = ImageFont.truetype('Roboto-Bold.ttf', 50)
    
    # ______end________
    
    # ______start______
    # draws the image
    
    image_editable = ImageDraw.Draw(my_image)
    
    # ______end________
    
    # ______start______
    #adds the text to the template
    #.text takes the following parameters (starting coordinates, font selection, text color in RGB, font style)
    
    image_editable.text((90,30), zipcode, (73, 79, 86), font=font)

    if beds == "Studio":
        image_editable.text((450,30), beds, (73, 79, 86), font=font)
    else:
        image_editable.text((520,30), beds, (73, 79, 86), font=font)

    image_editable.text((860,30), baths, (73, 79, 86), font=font)

    image_editable.text((445,275), rent, (73, 79, 86), font=font2) 
    image_editable.text((445,485), avg_rent, (73, 79, 86), font=font2) 

    image_editable.text((651,954), str(percent) + '%', (255, 189, 89), font=font3) 
    image_editable.text((196,998), total_users, (255, 189, 89), font=font3) 
    
    # ______end________
    
    # ______start______
    #takes the percent as an input then outputs the correct version of the dial image
    #get_file() defined in functions section
    
    dial = get_file(user_data['ratio'])
    
    # ______end________
    
    # ______start______
    # opens the image, changes white pixels to transparent, updates the image. 
    
    dial = dial.convert("RGBA")
    datas = dial.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    dial.putdata(newData)
    
    # ______end________
    
    # ______start______
    #overlays the image
    
    background = my_image
    foreground = dial

    background.paste(foreground, (0, 0), foreground)
    #background.show() // displays the image - used to test
    
    # ______end________
    
    
    # ______start______
    # saves the file into the "Results_output" folder
    
    imgfile = STORAGE_BASE_PATH + randint(10000, 99999) + ".png"
    background.save(imgfile)
    
    # ______end________
    
    # return 'C:/Users/scott/OneDrive/Documents/Code/Results_output/' + test
    return imgfile


# error check and send correct email
def send_user_email(user_data):
    if user_data['reason'] == 'zipcode':
        print('Zipcode not in coverage list.')
        send_fail_email(user_data['email'], user_data['reason'])
        
    elif user_data['reason'] == 'data':
        print('Not enough data.')
        send_fail_email(user_data['email'], user_data['reason'])
        
    elif user_data['reason'] == 'ok':
        print('Data sufficient. Results sent.')
        imgfile = generate_output_img(user_data)
        send_success_email(user_data['email'], imgfile)
        os.remove(imgfile)
        
    else:
        print('Unknown error. Reason not: zipcode, data or ok.')


# In[4]:


#Email send if there is enough data to generate result
#code is from here: https://stackoverflow.com/questions/920910/sending-multipart-html-emails-which-contain-embedded-images

def send_success_email(recipient, imgfile):
    
    sender = 'Rent Peek <info@rentpeek.co>'
    #recipient = ['scott.mongiardo@gmail.com']
    subject = 'Your Rent Peek Results!'
    #attachment = ["C:/Users/scott/OneDrive/Documents/Code/Results_output/results_401820.png"]
    # user = 'info@rentpeek.co'
    # pw = 'p'

    msg = EmailMessage()

    # generic email headers
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # set the plain text body
    msg.set_content('You are seeing this because your email does not support HTML. If you would like to\
                    recieve the image of your rent details, please respond to this email.')

    # now create a Content-ID for the image
    image_cid = make_msgid(domain='rentpeek.co')

    # set an alternative html body
    msg.add_alternative("""\
    <html>

            <div class="layout one-col fixed-width stack" style="Margin: 0 auto; \
            max-width: 600px;min-width: 320px; width: 320px;width: calc(28000% - 167400px); \
            overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;">

            <div class="layout__inner" style="border-collapse: collapse;display: table;width: 100%; \
            background-color: #ffffff;">

            <!--[if (mso)|(IE)]>
            <table align="center" cellpadding="0" cellspacing="0" role="presentation">
            <tr class="layout-fixed-width" style="background-color: #ffffff;">
            <td style="width: 600px" class="w560"><![endif]-->

              <div class="column" style="text-align: left;color: #565656;font-size: 14px; \
              line-height: 21px;font-family: Arial,sans-serif;">

            <div style="Margin-left: 20px;Margin-right: 20px;Margin-top: 24px;">
            <div style="mso-line-height-rule: exactly;mso-text-raise: 11px;vertical-align: middle;">

            <h1 style="Margin-top: 0;Margin-bottom: 0;font-style: normal;font-weight: normal; \
            color: #565656;font-size: 22px;line-height: 31px;font-family: Arial,sans-serif; \
            text-align: center;">

            <span class="font-arial" style="text-decoration: inherit;">

            Your Rent Peek data

            </span>
            </h1>

            <p class="size-16" style="Margin-top: 20px;Margin-bottom: 0; Margin-left: 50px;Margin-right: 50px; \
            font-family: Arial,sans-serif;font-size: 16px;line-height: 24px;text-align: center;" lang="x-size-16">
            
            <span class="font-arial" style="text-decoration: inherit;">

            Below is the average rent paid by Rent Peek users in your zip code. \
            <br> \

            </span>
            </p>

            <p class="size-16" style="Margin-top: 20px;Margin-bottom: 20px; Margin-left: 50px;Margin-right: 50px;
            font-family: Arial,sans-serif; \
            font-size: 16px;line-height: 24px;text-align: center;" lang="x-size-16">
            
            <span class="font-arial" style="text-decoration: inherit;">

            Want even more detailed results? \
            <b>Download the app below</b> to sort by square feet, amenities, lease start date, and more!

            </span>
            </p>
          </div>
        </div>

                <div style="Margin-left: 20px;Margin-right: 20px;">
            <div style="font-size: 12px;font-style: normal;font-weight: normal;line-height: 19px; \
            Margin-bottom: 20px;" align="center">

              <img style="border: 0;display: block;height: auto;width: 100%;max-width: 400px; \
              " alt="Your Rent Peek results" width="400" src="cid:{image_cid}">

            </div>
          </div>

                <div style="Margin-left: 20px;Margin-right: 20px;">
          <div class="divider" style="display: block;font-size: 2px;line-height: 2px; \
          Margin-left: auto;Margin-right: auto;width: 40px;background-color: #c8c8c8;Margin-bottom: 20px;">
          &nbsp;
          </div>
        </div>

                <div style="Margin-left: 20px;Margin-right: 20px;">
          <div style="mso-line-height-rule: exactly;mso-text-raise: 11px;vertical-align: middle;">
            <p class="size-20" style="Margin-top: 0;Margin-bottom: 20px;font-family: Arial,sans-serif; \
            font-size: 17px;line-height: 26px;text-align: center;" lang="x-size-20">

            <span class="font-arial" style="text-decoration: inherit;">
            <strong>

            <a href="https://www.rentpeek.co/">Download the app now</a>

            </strong>
            </span>
            </p>
          </div>
        </div>

              </div>
            <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
            </div>
          </div>

    </html>
    """.format(image_cid=image_cid[1:-1]), subtype='html')
    # image_cid looks like <long.random.number@xyz.com>
    # to use it as the img src, we don't need `<` or `>`
    # so we use [1:-1] to strip them off

    #test_img = 'C:/Users/scott/OneDrive/Documents/Code/Results_output/results_401820.png'
    # now open the image and attach it to the email
    with open(imgfile, 'rb') as img:

        # know the Content-Type of the image
        maintype, subtype = mimetypes.guess_type(img.name)[0].split('/')

        # attach it
        msg.get_payload()[1].add_related(img.read(), 
                                             maintype=maintype, 
                                             subtype=subtype, 
                                             cid=image_cid)


    # the message is ready now
    # you can write it to a file
    # or send it using smtplib

    send_email(msg, sender, recipient)


# In[5]:


#Email if not enough data
#code is from here: https://stackoverflow.com/questions/920910/sending-multipart-html-emails-which-contain-embedded-images

def send_fail_email(recipient, reason):
    
    sender = 'Rent Peek <info@rentpeek.co>'
    subject = 'Your Rent Peek Results!'

    msg = EmailMessage()

    # generic email headers
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    # set the plain text body
    msg.set_content('You are seeing this because your email does not support HTML. Normally we format the email \
                    nicely for you but your email client is blocking HTML. If you are unable to see the data \
                    please reply to this email and we\'ll get it to you right away')

    if reason == 'zipcode':
    # set an alternative html body
        msg.add_alternative("""\
    <html>

            <div class="layout one-col fixed-width stack" style="Margin: 0 auto; \
            max-width: 600px;min-width: 320px; width: 320px;width: calc(28000% - 167400px); \
            overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;">

            <div class="layout__inner" style="border-collapse: collapse;display: table;width: 100%; \
            background-color: #ffffff;">

            <!--[if (mso)|(IE)]>
            <table align="center" cellpadding="0" cellspacing="0" role="presentation">
            <tr class="layout-fixed-width" style="background-color: #ffffff;">
            <td style="width: 600px" class="w560"><![endif]-->

              <div class="column" style="text-align: left;color: #565656;font-size: 14px; \
              line-height: 21px;font-family: Arial,sans-serif;">

            <div style="Margin-left: 20px;Margin-right: 20px;Margin-top: 24px;">
            <div style="mso-line-height-rule: exactly;mso-text-raise: 11px;vertical-align: middle;">

            <h1 style="Margin-top: 0;Margin-bottom: 0;font-style: normal;font-weight: normal; \
            color: #565656;font-size: 22px;line-height: 31px;font-family: Arial,sans-serif; \
            text-align: center;">

            <span class="font-arial" style="text-decoration: inherit;">

            Your Rent Peek data

            </span>
            </h1>

            <p class="size-16" style="Margin-top: 20px;Margin-bottom: 0; Margin-left: 50px;Margin-right: 50px; \
            font-family: Arial,sans-serif;font-size: 16px;line-height: 24px;text-align: center;" lang="x-size-16">
            
            <span class="font-arial" style="text-decoration: inherit;">

            Unfortunately, we are not yet live for this zip code. \
            We start to cover a zip code once we have at least 30 user submissions. \
            <br>
            <br>
            Refer your friends so you can get your estimate! \

            <br> \

            </span>
            </p>

            <p class="size-16" style="Margin-top: 20px;Margin-bottom: 20px; Margin-left: 50px;Margin-right: 50px;
            font-family: Arial,sans-serif; \
            font-size: 16px;line-height: 24px;text-align: center;" lang="x-size-16">
            
            <span class="font-arial" style="text-decoration: inherit;">

            <b>Download the app</b> to get notified instantly when we launch in your zipcode!\

            </span>
            </p>
          

                <div style="Margin-left: 20px;Margin-right: 20px;">
          <div class="divider" style="display: block;font-size: 2px;line-height: 2px; \
          Margin-left: auto;Margin-right: auto;width: 40px;background-color: #c8c8c8;Margin-bottom: 20px;">
          &nbsp;
          </div>
        </div>

                <div style="Margin-left: 20px;Margin-right: 20px;">
          <div style="mso-line-height-rule: exactly;mso-text-raise: 11px;vertical-align: middle;">
            <p class="size-20" style="Margin-top: 0;Margin-bottom: 20px;font-family: Arial,sans-serif; \
            font-size: 17px;line-height: 26px;text-align: center;" lang="x-size-20">

            <span class="font-arial" style="text-decoration: inherit;">
            <strong>

            <a href="https://www.rentpeek.co/">Download the app now</a>

            </strong>
            </span>
            </p>
          </div>
        </div>

              </div>
            <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
            </div>
          </div>

    </html>
    """, subtype='html')
    
    else: 
        msg.set_content('You are seeing this because your email does not support HTML. Normally we format the email \
                    nicely for you but your email client is blocking HTML. If you are unable to see the data \
                    please reply to this email and we\'ll get it to you right away')

    # set an alternative html body
        msg.add_alternative("""\
    <html>

            <div class="layout one-col fixed-width stack" style="Margin: 0 auto; \
            max-width: 600px;min-width: 320px; width: 320px;width: calc(28000% - 167400px); \
            overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;">

            <div class="layout__inner" style="border-collapse: collapse;display: table;width: 100%; \
            background-color: #ffffff;">

            <!--[if (mso)|(IE)]>
            <table align="center" cellpadding="0" cellspacing="0" role="presentation">
            <tr class="layout-fixed-width" style="background-color: #ffffff;">
            <td style="width: 600px" class="w560"><![endif]-->

              <div class="column" style="text-align: left;color: #565656;font-size: 14px; \
              line-height: 21px;font-family: Arial,sans-serif;">

            <div style="Margin-left: 20px;Margin-right: 20px;Margin-top: 24px;">
            <div style="mso-line-height-rule: exactly;mso-text-raise: 11px;vertical-align: middle;">

            <h1 style="Margin-top: 0;Margin-bottom: 0;font-style: normal;font-weight: normal; \
            color: #565656;font-size: 22px;line-height: 31px;font-family: Arial,sans-serif; \
            text-align: center;">

            <span class="font-arial" style="text-decoration: inherit;">

            Your Rent Peek data

            </span>
            </h1>

            <p class="size-16" style="Margin-top: 20px;Margin-bottom: 0; Margin-left: 50px;Margin-right: 50px; \
            font-family: Arial,sans-serif;font-size: 16px;line-height: 24px;text-align: center;" lang="x-size-16">
            
            <span class="font-arial" style="text-decoration: inherit;">

            Unfortunately, we don’t have enough data yet for this apartment size. 
            
            <br> 
            <br>
            The more submissions we get, the more accurate our estimates become. \
            Share Rent Peek with other renters in your area to improve your data. \

            <br> \

            </span>
            </p>

            <p class="size-16" style="Margin-top: 20px;Margin-bottom: 20px; Margin-left: 50px;Margin-right: 50px;
            font-family: Arial,sans-serif; \
            font-size: 16px;line-height: 24px;text-align: center;" lang="x-size-16">
            
            <span class="font-arial" style="text-decoration: inherit;">

            <b>Download the app</b> to get an instant update when the data becomes available. \

            </span>
            </p>
          

                <div style="Margin-left: 20px;Margin-right: 20px;">
          <div class="divider" style="display: block;font-size: 2px;line-height: 2px; \
          Margin-left: auto;Margin-right: auto;width: 40px;background-color: #c8c8c8;Margin-bottom: 20px;">
          &nbsp;
          </div>
        </div>

                <div style="Margin-left: 20px;Margin-right: 20px;">
          <div style="mso-line-height-rule: exactly;mso-text-raise: 11px;vertical-align: middle;">
            <p class="size-20" style="Margin-top: 0;Margin-bottom: 20px;font-family: Arial,sans-serif; \
            font-size: 17px;line-height: 26px;text-align: center;" lang="x-size-20">

            <span class="font-arial" style="text-decoration: inherit;">
            <strong>

            <a href="https://www.rentpeek.co/">Download the app now</a>

            </strong>
            </span>
            </p>
          </div>
        </div>

              </div>
            <!--[if (mso)|(IE)]></td></tr></table><![endif]-->
            </div>
          </div>

    </html>
    """, subtype='html')

    # the message is ready now
    # you can write it to a file
    # or send it using smtplib
    send_email(msg, sender, recipient)
    


def send_email(msg: EmailMessage, sender: str, recipient: str):
  creds = get_email_creds()
  smtp = smtplib.SMTP("smtp.gmail.com", port=587)
  smtp.starttls()
  smtp.login(creds['user'], creds['pw'])
  smtp.sendmail(sender, recipient, msg.as_string())
  smtp.quit()


# In[13]:


# user_data = {}
# user_data = get_user_info(user_input_data)
# print(user_data)
# get_data(user_data)
# print(user_data)
# send_email(user_data)


# In[ ]:




