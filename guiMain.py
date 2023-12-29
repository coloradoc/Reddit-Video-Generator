import tkinter as tk
from tkinter import ttk

import subprocess

#imports
from moviepy.editor import *
import pandas as pd
import praw 
from config import *
import glob 
import os
import wget 


#blur
from skimage.filters import gaussian

#tts imports
import os, glob
from shutil import move
from urllib import response 
from google.cloud import texttospeech
from google.cloud import texttospeech_v1

#make database
import sqlite3

# importing the module
from mechanize import Browser


#make sentence spliter
import re

#reset pyvideos
import glob
# Create the main window
window = tk.Tk()
window.title("Reddit Video Generator")
window.geometry("1200x1000")
window.iconbitmap(r'images\pizzaIcon2.ico')

# Load the image
image = tk.PhotoImage(file=r"images\reddddd.png")

# Create a label to display the image
image_label = ttk.Label(window, image=image)
image_label.pack()

# Create a label to display some text
text_label = ttk.Label(window, text="Awesome", font=("TkDefaultFont", 30))
text_label.pack(pady=5)
text_label = ttk.Label(window, text="Reddit Video Generator", font=("TkDefaultFont", 20))
text_label.pack(pady=5)



# Create a label for the progress bar
progress_label = ttk.Label(window, text="Progress:")
progress_label.pack(pady=10)

# Create a progress bar
progress_bar = ttk.Progressbar(window, orient=tk.HORIZONTAL, length=200, mode='determinate')
progress_bar.pack(pady=10)

# Create a button to update the progress bar
def update_progress():
    progress_bar['value'] += 10

# Create a button to run the Python code
def run_python_code(subReddit, maxLengthOfParent, maxScoreOfParent, HowManyComments, credential_pathTTS, credential_pathYT, Rclient_id, Rclient_secret, Rpassword, Ruser_agent, Rusername):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_pathTTS
    credential_pathTTS = texttospeech_v1.TextToSpeechClient()

    import random
    # Create a button to start the progress bar
    update_progress()

    con = sqlite3.connect('titles.db')
    cur = con.cursor()


    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    digits = "([0-9])"

    #tts make link shorter
    #changes the url to "this link"
    def remove_urls(text):
        text = re.sub(r'http\S+', 'this link', text)
        return text


    def splice_url(text):
        # target url
        url = 'text'
        
        # creating a Browser instance
        br = Browser()
        br.open(url)
        
        return br.title()


    #1.scrape
    #authentication
    reddit = praw.Reddit(client_id=Rclient_id, client_secret=Rclient_secret, password=Rpassword, user_agent=Ruser_agent, username=Rusername)

    subreddit = reddit.subreddit(subReddit)
    #change hot_python to limt=20
    #program might error out this part of code, its because limit reaches its limit

    #year can be month
    hot_python = subreddit.top("year", limit=100)
    print(hot_python)

    #make url custom names 
    urls= []
    SubmissionAuthors = []
    SubmissionTitles = []
    SubmissionScore = []
    commentslist = []

    ammountofworkingurls = -1

    #define and get info from database to not repost
    tittlelist= []
    for title1 in cur.execute('''SELECT * FROM title'''):

        tittlelist.append(title1)

    #make it so it wont repost, i removed getting posts randomly because it sucked
    #scrape comments
    def scrapecomments(commentslist, SubmissionAuthors, SubmissionTitles, urls, hot_python, ammountofworkingurls, tittlelist):
        print(hot_python)
        print(f'The url work: {ammountofworkingurls}')
        count = -1
        #change rand to (0,18)
        rand = random.randint(0,18)
        print(rand)
        margin_of_error = 0
        for submission in hot_python:
            print(submission.title)
            count += 1
            print(count)
            print(rand)
            final_db = submission.title.replace("'", "")
            if int(count) == int(count):
            # print("COUNT == RAND")
            #change in str tittlelist if things get messed up and we need to call a required title
                if not submission.stickied and margin_of_error < 80 and submission.score > 10000 and final_db not in str(tittlelist) and not int(len(submission.title)) > 130: #FOR REFERNCE CODE IF VALUES ARE CHANGED
                    #if not submission.stickied and margin_of_error < 80 and submission.score > 10000 and final_db in "What was “The Incident” at your High School?" and not int(len(submission.title)) > 90:
                    #submission.comments.replace_more(limit=50)
                    print(f"Here is the length of the title {len(submission.title)}")
                    print(f"here is the title list{str(tittlelist)}")
                    print(f"here is the title list{str(submission.title)}")
                    #!------------------uncomment the following code to add to database so that it will not be selected again------------------------!
                    #cur.execute("INSERT OR IGNORE INTO title VALUES (?)", (final_db,)) 

                    #con.commit() 
                    #print(f"Author: {submission.author} Title: {submission.title}  Have we visted: {submission.visited} created: {submission.created}")
                    commentAmmount = 0 
                    overallBodyLength = 0 
                    #normaly 300
                    scoreRequirement = 300

                    AmmountComment = 0
                    HowManyComment = HowManyComments
                    for comment in submission.comments:
                        if AmmountComment < int(HowManyComment):
                            #check if there is too many comments/letters overall
                            #at 1000 len overall the video is:

                            if margin_of_error < 120 and overallBodyLength < 25000:
                                print(f"Overall body length: {overallBodyLength}")
                                print(f"Comment ammout is {commentAmmount}")
                                #check if the post is over required upvotes
                                try:
                                    commentstr = str(comment)
                                    print(commentstr)
                                    commentreal = reddit.comment(commentstr) 
                                    score = int(commentreal.score)
                                    bodylen = len(commentreal.body)


                                    if score > scoreRequirement and bodylen > 35:
                                        AmmountComment = AmmountComment + 1
                                        overallBodyLength += bodylen
                                        commentAmmount += 1
                                        commentslist.append(str(comment))
                                        print(f"the body{commentreal.body}")
                                        print(score)
                                        print(f"body len{bodylen}")
                                    else:
                                        #if there is not enough comments, then lower requirements
                                        scoreRequirement = 50
                                        print("score too low")
                                        margin_of_error += 1
                                        print(f"Margin of error: {margin_of_error}")
                                except:
                                    print("Comment broke error: MoreComments children")

                    #print(submission.url)
                    if overallBodyLength <8000:
                        continue1 = input("POST SIZE NOT LARGE ENOUGH, WILL MAKE TOO SHORT OF A VIDEO. CONTINUE?")
                    print("Margin of error became too high")
                    SubmissionAuthors.append(submission.author)
                    SubmissionTitles.append(submission.title)
                    SubmissionScore.append(submission.score)

                    urls.append(submission.url)
                    break
                else:
                    print("SUBMISSION DID NOT WORK")
            else:
                print("count x= rand")
            print("Post data collection has been completed!")




            #print(dir(submission))


    realcommentsauthor = []
    realcommentsscore = []
    realcommentslist = []
    realcommentstime = []
    import math
    from datetime import datetime 
    def getcommentdetails(commentslist, realcommentslist, realcommentsscore, realcommentsauthor, realcommentstime):
        for commentids in commentslist:
            # instantiating the Comment class
            #the program errors out when i try to show the comments body which should work, i think its because it trys to enter in the full list valve pls fix
            

            print(commentids)
            commentreal = reddit.comment(commentids)

                
            # fetching the author attribute
            #author = commentreal.author
            body = commentreal.body
            score = commentreal.score
            author = commentreal.author

            realcommentslist.append(body)
            realcommentsscore.append(score)
            realcommentsauthor.append(author)

            
            
            # fetching the Unix time
            unix_time = commentreal.created_utc 

            # converting the Unix time 
            redditdate = datetime.fromtimestamp(unix_time)

            first_time = datetime.now()

            difference = redditdate - first_time
            dif = (difference.days - difference.days) - difference.days
            print(f" dif is {dif}")


            hourdif = str(redditdate)[11:13] 
            hourdif2 = str(first_time)[11:13]
            hourdifs = int(hourdif) 


            if hourdifs <= 0:
                hourdifs = 1
            #FINDS TIME OF POSTS
            if dif >= 256:
                timeago = dif / 256
                timeagoreal = f"{math.floor(timeago)} years ago"
            elif dif >= 29:
                timeago = dif /30 
                timeagoreal = f"{math.floor(timeago)} months ago"
            if dif <= 29 and dif > 1:
                timeago = dif
                timeagoreal = f"{math.floor(timeago)} days ago"
            elif dif == 1:
                timeagoreal = f"{math.floor(hourdifs)} hours ago"



            print(timeagoreal)
            realcommentstime.append(timeagoreal)
        

    #comments info
    scrapecomments(commentslist, SubmissionAuthors, SubmissionTitles, urls, hot_python, ammountofworkingurls, tittlelist)
    getcommentdetails(commentslist, realcommentslist, realcommentsscore, realcommentsauthor, realcommentstime)
    print(f"here is the comments body: {realcommentslist}")
    print(realcommentsauthor)
    print(realcommentsscore)
    print(realcommentstime)
    print("Done")
    #the posts author info
    print(SubmissionTitles)
    print(SubmissionAuthors)
    print(urls)

    update_progress()

    #asks user for input testing purp only for now
    #name = input('What is your name?\n')


    #splits the text from \n, then removes the \n but creates something that says to make a new text below the current one
    #moviepy
    #splits sentences and keeps \n (thank god)
    from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters

    #moivepy
    #is unoptimised because it checks every sentence, not only the ones that have \n
    def split_into_sentences_moivepy(text):
        for i in range(10):
                text = text.replace("&#x200B;", ' ')
        punkt_param = PunktParameters()
        abbreviation = ['f', 'fr', 'k']
        punkt_param.abbrev_types = set(abbreviation)

        tokenizer = PunktSentenceTokenizer(punkt_param)
        tokenizer.train(text)


        e = tokenizer.tokenize(text)



        return e

    def split_into_sentences_tts(text):
        #might break here because not checking enough
        for i in range(20):
                text = text.replace("\n", ' ')
        for i in range(10):
                text = text.replace("&#x200B;", ' ')
        punkt_param = PunktParameters()
        abbreviation = ['f', 'fr', 'k']
        punkt_param.abbrev_types = set(abbreviation)

        tokenizer = PunktSentenceTokenizer(punkt_param)
        tokenizer.train(text)


        e = tokenizer.tokenize(text)

            

        return e


    #split sentecnes to make tts more efficent
    realsentencemoviepy = []
    realsentencetts = []
    realreaction = []
    #make two diffrent data frames one with no \n for tss and one with \n f
    #if text contains a \n, just split it and make tts not read it, but display it on the video

    #moviepy
    #remove sentences
    for sentence in realcommentslist:
        

        realsen = split_into_sentences_moivepy(sentence)



        print(realsen)
        if realsen == []:
            realsentencemoviepy.append([sentence])
        else:
            realsentencemoviepy.append(realsen)
    #tts
    for sentences1 in realcommentslist:
        
        realsen1 = remove_urls(sentences1)
        realsen = split_into_sentences_tts(realsen1)



        print(realsen)
        if realsen == []:
            realsentencetts.append([realsen])
        else:
            realsentencetts.append(realsen)
        #reaction
    for sentences1 in realcommentslist:
        
        realsen1 = remove_urls(sentences1)
        realsen = split_into_sentences_tts(realsen1)



        print(realsen)
        if realsen == []:
            realreaction.append([realsen])
        else:
            realreaction.append(realsen)



    print(f"here is the real sen: {realsentencemoviepy}")
    print(f"here is the real tts: {realsentencetts}")
    print(f"here is the real reaction: {realreaction}")

    #run 



    #sort of all the data to pandas
    #moviepy
    comment_detailsmoivepy = list(zip(realcommentsauthor, realsentencemoviepy, realcommentsscore, realcommentstime))

    comment_details_dfmoviepy = pd.DataFrame(comment_detailsmoivepy, columns=["Author", "TextBody", "Score", "Time"])
    #sort df
    #comment_details_dfmoviepy = comment_details_dfmoviepy.sort_values(by=['Score'], ascending=False)
    #save to cvs
    comment_details_dfmoviepy.to_csv('movie.csv', index=False)
    path = r'cvs folders'
    comment_details_dfmoviepy.to_csv(os.path.join(path,r'moviepy.csv'))

    #sort of all the data to pandas
    #tts
    comment_detailstts = list(zip(realcommentsauthor, realsentencetts, realcommentsscore))
    comment_details_dftts = pd.DataFrame(comment_detailstts, columns=["Author", "TextBody", "Score"])
    #sort df
    #comment_details_dftts = comment_details_dftts.sort_values(by=['Score'], ascending=False)
    #save to cvs
    comment_details_dftts.to_csv(os.path.join(path,r'tts.csv'))
    print("the moviepy dataframe")
    print(comment_details_dfmoviepy)
    print("the tts dataframe")
    print(comment_details_dftts)

    update_progress()



    #first do the title, then do the comments





    
    voice1 = texttospeech.VoiceSelectionParams(
         language_code="en-UK", ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    print(dir(texttospeech_v1.SsmlVoiceGender))

    print(credential_pathTTS.list_voices)


    #output file config

    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding=texttospeech_v1.AudioEncoding.MP3
    )
    def clean_tts_folders(realcommentslist):
        comment_number = 0
        for comment in realcommentslist:
            comment_number += 1
            pth = f"file that might save audio who knows please dont delete everything please god\commentfolder{comment_number}"
            #clean tts folder
            filelist = glob.glob(os.path.join(pth, "*"))
            for f in filelist:
                os.remove(f)
    def clean_reaction_folders():

        pth = r"reactionGPTvideos"
        #clean tts folder
        filelist = glob.glob(os.path.join(pth, "*"))
        for f in filelist:
            os.remove(f)
    #instead of using a single list to hold our text info im going to use a df, i need to find a way to loop using a df so that i can get a an audio group of a single comments split
    #into sentences
    clean_reaction_folders()





    def makeintotts(client, voice1, audio_config, SubmissionTitles):
        pth = f"file that might save audio who knows please dont delete everything please god\\introtext"

        for i in SubmissionTitles:
            sentence = i

        #make tss folder
        if not os.path.exists(pth):
            os.makedirs(pth)
        #saves tts for each sentence


        #cleans text from emojis
        def remove_emoji(string):
            emoji_pattern = re.compile("["
                                    u"\U0001F600-\U0001F64F"  # emoticons
                                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                    u"\U00002500-\U00002BEF"  # chinese char
                                        u"\U00002702-\U000027B0"
                                        u"\U00002702-\U000027B0"
                                        u"\U000024C2-\U0001F251"
                                        u"\U0001f926-\U0001f937"
                                        u"\U00010000-\U0010ffff"
                                        u"\u2640-\u2642"
                                        u"\u2600-\u2B55"
                                        u"\u200d"
                                        u"\u23cf"
                                        u"\u23e9"
                                        u"\u231a"
                                        u"\ufe0f"  # dingbats
                                        u"\u3030"
                                        "]+", flags=re.UNICODE)
            return emoji_pattern.sub(r'', string)


        #remove emoji
        sentence = remove_emoji(sentence)
        sentence = re.sub(r"&", "and", sentence)
        sentence = re.sub(r">", "", sentence)
        sentence = re.sub(r"<", "", sentence)
        #makes tts
        #made this part commented out because it broke the tts
        #text = f"<speak>{sentence}</speak>"
        text = f"{sentence}"
        print(f"TTS intro text: {text}")
        synthesis_input = texttospeech_v1.SynthesisInput(ssml=text)
        response1 = client.synthesize_speech(
                input=synthesis_input,
                voice=voice1,
                audio_config=audio_config
            )
            #save tts
        with open(os.path.join(pth,f"commentintro"+".mp3"),'wb') as output1:
            output1.write(response1.audio_content)
    #saves the text to speech to the voice folder


    makeintotts(credential_pathTTS, voice1, audio_config, SubmissionTitles)









    def maketts(client, voice1, audio_config, comment_details_df):
        #extract from dataframe

        #this part gets the comments from the df and stores them into their respective lists
        comment_number1 = -1
        comment_text_list=[]
        print(comment_details_df)



        comment_text_list = comment_details_df['TextBody'].values.tolist()
        #how to get df to list
        #product = df['product'].values.tolist()

        #this part makes tts with the list of comments chosen comments
        print(comment_text_list)
        comment_number = 0
        for comment in comment_text_list:

            comment_number += 1
            pth = f"file that might save audio who knows please dont delete everything please god\commentfolder{comment_number}"

            #make tss folder
            if not os.path.exists(pth):
                os.makedirs(pth)
            counter = 0
            #saves tts for each sentence

            for sentence in comment:
                #cleans text from emojis
                import re
                def remove_emoji(string):
                    emoji_pattern = re.compile("["
                                            u"\U0001F600-\U0001F64F"  # emoticons
                                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                            u"\U00002500-\U00002BEF"  # chinese char
                                            u"\U00002702-\U000027B0"
                                            u"\U00002702-\U000027B0"
                                            u"\U000024C2-\U0001F251"
                                            u"\U0001f926-\U0001f937"
                                            u"\U00010000-\U0010ffff"
                                            u"\u2640-\u2642"
                                            u"\u2600-\u2B55"
                                            u"\u200d"
                                            u"\u23cf"
                                            u"\u23e9"
                                            u"\u231a"
                                            u"\ufe0f"  # dingbats
                                            u"\u3030"
                                            "]+", flags=re.UNICODE)
                    return emoji_pattern.sub(r'', string)


                #remove emoji
                sentence = remove_emoji(sentence)
                sentence = re.sub(r"&", "and", sentence)
                sentence = re.sub(r">", "", sentence)
                sentence = re.sub(r"<", "", sentence)
                #makes tts
                counter += 1
                #text = f"<speak>{sentence}</speak>"
                text = f"{sentence}"
                print(f"TTS text: {text}")
                synthesis_input = texttospeech_v1.SynthesisInput(ssml=text)
                response1 = client.synthesize_speech(
                    input=synthesis_input,
                    voice=voice1,
                    audio_config=audio_config
                )
                #save tts
                with open(os.path.join(pth,f"comment{comment_number} sentence{counter}"+".mp3"),'wb') as output1:
                    output1.write(response1.audio_content)
    #saves the text to speech to the voice folder

    



    #video config
    vcodec =   "libx264"
    videoquality = "24"

    # slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    compression = "slow"

    #loading video file clip
    test = "blah blah blah blah"
    randomvideobackround = random.randint(1,2)
    clip = VideoFileClip(f"videopy\\space{randomvideobackround}.mp4") 
    clip = clip.volumex(1) 

    #loading and def the blur effect for moivepy
    #blur is at 0 for testing to make videos faster
    def blur(image):
        """ Returns a blurred (radius=2 pixels) version of the image """
        return gaussian(image.astype(float), sigma=1.5)


    def make_intro(clip, SubmissionAuthors, SubmissionScore, SubmissionTitles):

        for i in SubmissionAuthors:
            author = str(i)
            print(f"Author is: {i}")
        for i in SubmissionScore:
            score = str(i)
            print(f"Score is: {i}")
        for i in SubmissionTitles:
            title = str(i)
            print(f"Title is: {i}")

        score = f"{score} points"
        moveaway = len(author)*11

        found = False
        rounded = 0
        char_ammount = len(title)

        
        while found == False:
            rounded += 90
            #makes new line according to the old ones already made
            #the higer the ammount rounded is multiplied by, the more char it takes to create a new line

            titlefontsize = 70
            timesround = .3
            #if the char ammout is too big, make the text smaller 
            if char_ammount > 88:
                timesround = .6*1.2
                titlefontsize = 35*1.2

            roundedammount = rounded*timesround
            if char_ammount < roundedammount:
                char_ammount_true = rounded
                #if text has a \n, make a new line by adding + 26-30 idk to char ammount
                haystack = title
                needle = "\n"
                for i, x in enumerate(haystack):
                    if haystack[i:i + len(needle)] == needle:
                        char_ammount_true += 26
                found = True



        txt_author = TextClip(author,color='DodgerBlue', font="Verdana",
                    kerning = 0, fontsize=30, method='label', align=('Northwest')).set_position((50, 150))

        txt_score = TextClip(score,color='white', font="Verdana",
                    kerning = 0, fontsize=30, method='label', align=('Northwest')).set_position((200+moveaway, 150))

        txt_title = TextClip(title,color='white', font="Verdana",
                    kerning = 0, fontsize=titlefontsize, method='caption', size = (1160, char_ammount_true), align=('Northwest')).set_position((50, 190))

        txt_col = txt_title.on_color(size=(txt_title.w+5, txt_title.h+5), color=(26, 26, 27), col_opacity=1).set_position((50, 190))
        
        txt_author_blank = TextClip(" ", font="Verdana",
                    kerning = 0, fontsize=18, method='label', align=('Northwest')).set_position((50, 150))
        lenofscore = len(score) *4
        txt_info_col = txt_author_blank.on_color(size=(txt_author.w+180+moveaway+lenofscore, txt_author.h), color=(26, 26, 27), col_opacity=1).set_position((50, 150))



        # dont forget to make the intro tts
        audio = AudioFileClip(f"file that might save audio who knows please dont delete everything please god\\introtext\\commentintro.mp3")
        clipadded = clip.subclip(100, 100+audio.duration)
        clipadded1 = clipadded.set_audio(audio)

        #blur backround
        clip_blurred = clipadded1.fl_image( blur )





        videoclip = CompositeVideoClip([clip_blurred, txt_info_col, txt_col, txt_score, txt_author]).set_duration(audio.duration)
        return videoclip





    intro = make_intro(clip, SubmissionAuthors, SubmissionScore, SubmissionTitles)





    import time
    def make_video(sentences, clip, comment_details_df, intro):
        count = 0
        screensize = clip.size
        clips = []
        videos = []
        videos.append(intro)
        comment_text_list = []
        comment_number1 = -1
        counter_for_lists = -1

        #the reason posts are not sorted by number, is because comment_nummber1 is sorting by number, not by score, we should fix this

        comment_text_list = comment_details_df["TextBody"].values.tolist()
        print(comment_text_list)

        comment_author_list = comment_details_df["Author"].values.tolist()

        comment_score_list = comment_details_df["Score"].values.tolist()

        comment_time_list = comment_details_df["Time"].values.tolist()





        # for each sentence in the comments text list 
        #makes the backround clip time stamps
        overalltime = 0
        for comment in comment_text_list:
                counter_for_lists += 1
                scoreofcomment = str(comment_score_list[counter_for_lists])
                authorofcomment = str(comment_author_list[counter_for_lists])
                timeofcomment = str(comment_time_list[counter_for_lists])
                print(scoreofcomment)
                print(authorofcomment)
                #add time here
                scoreofcomment = f"   {scoreofcomment} points   •   {timeofcomment}"


                count += 1
                sentence_count = 0
                #makes the text 
                prev_text = ""
                prev_text_gap = ""
                hei = 175 
                comments_nsplit = []
                countn = -1
                SetTimeAt = random.randint(5,200)
                for sentence in comment:
                    def remove_emoji(string):
                        emoji_pattern = re.compile("["
                                                u"\U0001F600-\U0001F64F"  # emoticons
                                                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                                u"\U00002500-\U00002BEF"  # chinese char
                                                    u"\U00002702-\U000027B0"
                                                    u"\U00002702-\U000027B0"
                                                    u"\U000024C2-\U0001F251"
                                                    u"\U0001f926-\U0001f937"
                                                    u"\U00010000-\U0010ffff"
                                                    u"\u2640-\u2642"
                                                    u"\u2600-\u2B55"
                                                    u"\u200d"
                                                    u"\u23cf"
                                                    u"\u23e9"
                                                    u"\u231a"
                                                    u"\ufe0f"  # dingbats
                                                    u"\u3030"
                                                    "]+", flags=re.UNICODE)
                        return emoji_pattern.sub(r'', string)


                    #remove emoji
                    sentence = remove_emoji(sentence)
                    print(sentence)
                    countn += 1


    
                    print(sentence)
                    sentence_count += 1
                    try:

                        text = f"{prev_text+sentence}"
                        text = text

                        print(f'text{text}')
                        print(sentence)
                        prev_text += sentence + " "
                        print(prev_text)
                        #align is our lord and savior to make text start on the left
                        print(screensize)
                        #if too big reset the text
                        char_ammount = len(prev_text)
                        found = False
                        rounded = 0

                        while found == False:
                            rounded += 26
                            print(rounded)
                            #makes new line according to the old ones already made
                            #the higher the ammount rounded is multiplied by, the more char it takes to create a new line
                            roundedammount = rounded*4.2
                            if char_ammount < roundedammount:
                                char_ammount_true = rounded
                                #if text has a \n, make a new line by adding + 26-30 idk to char ammount
                                haystack = text
                                needle = "\n"
                                for i, x in enumerate(haystack):
                                    if haystack[i:i + len(needle)] == needle:
                                        char_ammount_true += 26
                                found = True

                        #stops the text from going over the limit
                        if char_ammount_true > 480:
                            prev_text = ""
                        else:
                            fontsizes = 20
                            #make the current text that is not being read transparrent, and the text being read normal


                        txt_clip = TextClip(text,color='white', font="Verdana",
                                    kerning = 0, fontsize=fontsizes, method='caption', size = (1160, char_ammount_true), align=('Northwest')).set_position((50, 175))
                            
                        txt_col = txt_clip.on_color(size=(txt_clip.w+5, txt_clip.h+5), color=(26, 26, 27), col_opacity=.9).set_position((50, 175))

                        txt_author = TextClip(authorofcomment,color='DodgerBlue', font="Verdana",
                                    kerning = 0, fontsize=18, method='label', align=('Northwest')).set_position((50, 150))

                        moveaway = len(authorofcomment)*16
                        if moveaway <150:
                            moveaway = 150
                        lenofscore = len(scoreofcomment)
                        txt_score = TextClip(scoreofcomment,color='white', font="Verdana",
                                    kerning = 0, fontsize=18, method='label', align=('Northwest')).set_position((moveaway, 150))

                        txt_author_blank = TextClip(" ", font="Verdana",
                                    kerning = 0, fontsize=18, method='label', align=('Northwest')).set_position((50, 150))

                        txt_info_col = txt_author_blank.on_color(size=(txt_author.w+150+moveaway+lenofscore, txt_author.h), color=(26, 26, 27), col_opacity=.9).set_position((50, 150))

                        #make image clip of the upvote
                        upvote = ImageClip("videopy\\upvotes downvote.png").set_position((10, 150)).resize(0.4)

                        #if there is a gap (\n\n) then make a new text with a gap 


                        
                        audio = AudioFileClip(f"file that might save audio who knows please dont delete everything please god\\commentfolder{count}\\comment{count} sentence{sentence_count}.mp3")
                        
                        print(overalltime)
                        print(audio.duration)

                        addedtime = overalltime+ audio.duration
                        print(addedtime)
                        print(clip.duration)
                        clipadded = clip.subclip(overalltime+SetTimeAt, addedtime+SetTimeAt)
                        clipadded1 = clipadded.set_audio(audio)

                        #blur backround
                        #clip_blurred = clipadded1.fl_image( blur )

                        videoclip = CompositeVideoClip([clipadded1, txt_info_col, txt_col, txt_score, txt_author, upvote]).set_duration(audio.duration)
                        clips.append(videoclip)
                        overalltime += audio.duration
                    except:
                        print("Sentence did not work")
                        pass

                #define the outro and transits
                trans= VideoFileClip(r"clips for video\Upvote transition.mp4") 
                trans1 = trans.subclip(0, trans.duration).resize( (1280, 720) )

                finished_trans = concatenate_videoclips([trans1])

                outro = VideoFileClip(r"clips for video\outro.mp4") 
                outro1 = outro.subclip(0, outro.duration).resize( (1280, 720) )

                finished_outro = concatenate_videoclips([outro1])



                #finished clip is the current video clip, videos is all the clips saved together
                finished_clip = concatenate_videoclips(clips)
                videos.append(finished_clip)
                #insert reaciton here
                    #what we should do here is run the program that will get the reaction, to do this we must run and return it
                    #first we have to send over a addedtime so we can start the video footage where we left off, or maybe use a dif background 
                #videos.append(make_reaction(clip, reaction, addedtime))
                # path to the Python script you want to run
                reaction = False
                if reaction == True:
                    script_path = r"moviepyReactionTesting.py"

                    # string value to pass to the script
                    string_value = realcommentslist[counter_for_lists]

                    # run the script with the string value as an argument
                    result = subprocess.run(["python", script_path, string_value, str(counter_for_lists)])

                    # print the output of the script
                    
                    time.sleep(1)
                    print("appending gpt video")
                    reaction = VideoFileClip(f"reactionGPTvideos\\redditGPTtesting{counter_for_lists}.mp4") 
                    reaction = reaction.subclip(0, reaction.duration).resize( (1280, 720) )

                    finished_reaction = concatenate_videoclips([reaction])

                    videos.append(finished_reaction)
                videos.append(finished_trans)
                #reset clips so video does not loop
                clips = []

        #fix below videos is empty

        videos.append(finished_outro)

        final_clip = concatenate_videoclips(videos)

        #make audio music
        randomvideomusic = random.randint(1,2)
        audioclip = AudioFileClip(f"videopy\\music{randomvideomusic}.mp4")

        audioclip = audioclip.volumex(.04)

        audioclip = audioclip.subclip(0, final_clip.duration)


        fca = final_clip.audio

        fca1= CompositeAudioClip([audioclip, fca])

        final_clip = final_clip.set_audio(fca1)


        final_clip.write_videofile(r'finished videos\coolTextEffects.mp4',fps=25,codec=vcodec, preset= compression, ffmpeg_params=['-crf', videoquality]) 

    #makethumbnail
    def makethumbnail(SubmissionTitles):
        imgchoose = random.randint(1,24)
        backround = ImageClip(r"imagesforthumbnail\background\thumbnail prototype11.png")
        image = ImageClip(f"imagesforthumbnail\\selection\\s{imgchoose}.png").set_position((600, 50))
        print(image.size)
        image = image.resize( (820,720) )
        for i in SubmissionTitles:
            title = str(i)
    



        char_ammount = len(title)
        print(char_ammount)
        titlefontsize = 75

        if char_ammount > 60:
            titlefontsize = 65
        if char_ammount > 90:
            titlefontsize = 55
        if char_ammount > 120:
            titlefontsize = 45




        txt_title = TextClip(title[0:char_ammount],color='white', font="Verdana",
                    kerning = 0, fontsize=titlefontsize, method='caption', size = (600, 1000), align=('Northwest')).set_position((20, 200))

        txt_title2 = TextClip(title[0:char_ammount],color='red', font="Verdana",
                kerning = 0, fontsize=titlefontsize, method='caption', size = (600, 1000), align=('Northwest')).set_position((txt_title.pos))





        
        thumby = CompositeVideoClip([backround, txt_title2, txt_title, image])
        thumby.duration = (.03)
        
        return thumby
    #to make video, make txt clips for each sentences, then display them when each sentence is done being spoken.!!!!!!!!!!!!!!!!!!


    #video config
    vcodec =   "libx264"
    videoquality = "24"

    # slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    compression = "slow"




    makethumbnail(SubmissionTitles).save_frame(r'imagesforthumbnail\finished thumbnail\thumbnail1.png')


    #upload to youtube
    def uploadtoyoutube(SubmissionTitles):
        for i in SubmissionTitles:
            title = str(i)
        #pt1 
        import pickle
        import os
        from datetime import datetime 
        from google_auth_oauthlib.flow import Flow, InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
        from google.auth.transport.requests import Request


        def Create_Service(client_secret_file, api_name, api_version, *scopes):
            print(client_secret_file, api_name, api_version, scopes, sep='-')
            CLIENT_SECRET_FILE = client_secret_file
            API_SERVICE_NAME = api_name
            API_VERSION = api_version
            SCOPES = [scope for scope in scopes[0]]
            print(SCOPES)

            cred = None

            pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
            # print(pickle_file)

            if os.path.exists(pickle_file):
                with open(pickle_file, 'rb') as token:
                    cred = pickle.load(token)

            if not cred or not cred.valid:
                if cred and cred.expired and cred.refresh_token:
                    cred.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
                    cred = flow.run_local_server()

                with open(pickle_file, 'wb') as token:
                    pickle.dump(cred, token)

            try:
                service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
                print(API_SERVICE_NAME, 'service created successfully')
                return service
            except Exception as e:
                print('Unable to connect.')
                print(e)
                return None

        def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
            dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
            return dt


        #pt2
        import datetime
        from googleapiclient.http import MediaFileUpload


        CLIENT_SECRET_FILE = credential_pathYT
        API_NAME = 'youtube'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'

        request_body = {
            'snippet': {
                'categoryI': 24,
                'title': f'{title} (r/AskReddit)',
                'description': 'Thanks for watching this video! Please sub to the channel to help us grow! #reddit #redditposts #redditstories #redditstory',
                'tags': ['Memes', 'Reddit', 'Reddit Stories']
            },
            'status': {
                'privacyStatus': 'private',
                'publishAt': upload_date_time,
                'selfDeclaredMadeForKids': False, 
            },
            'notifySubscribers': True
        }

        mediaFile = MediaFileUpload(r'finished videos\coolTextEffects.mp4')

        response_upload = service.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=mediaFile
        ).execute()


        service.thumbnails().set(
            videoId=response_upload.get('id'),
            media_body=MediaFileUpload(r'imagesforthumbnail\finished thumbnail\thumbnail1.png')
        ).execute()

    #to make video, make txt clips for each sentences, then display them when each sentence is done being spoken.!!!!!!!!!!!!!!!!!!
        

    update_progress()
    clean_tts_folders(realcommentslist)
    update_progress()
    maketts(credential_pathTTS, voice1, audio_config, comment_details_dftts)
    update_progress()
    make_video(realcommentslist, clip, comment_details_dfmoviepy, intro)
    update_progress()
    makethumbnail(SubmissionTitles).write_videofile(r'imagesforthumbnail\finished thumbnail\thumbnail.mp4',fps=25,codec=vcodec, preset= compression, ffmpeg_params=['-crf', videoquality]) 
    update_progress()
    update_progress()
    #uploadtoyoutube(SubmissionTitles)

    #print out name of post for title (for user)
    for i in SubmissionAuthors:
        author = str(i)
        print(f"Author is: {i}")
    for i in SubmissionTitles:
        score = str(i)
        print(f"Title is: {i}")
        import random
        result = random.randint(1, 100)
        output_label.configure(text=result)
        progress_bar['value'] += 10
import json
# Read the JSON file
file_path = 'secrets\\passwords.json'

with open(file_path, 'r') as file:
    data = json.load(file)

def get_password(credentials_list, service):
    for credentials in credentials_list:
        if credentials['service'] == service:
            return credentials['credential_path']
    return None  # Return None if service is not found
def get_reddit_password(credentials_list, service):
    for credentials in credentials_list:
        if credentials['service'] == service:
            return [credentials['client_id'], credentials['client_secret'],credentials['password'],credentials['user_agent'],credentials['username']]
    return None  # Return None if service is not found
credentials_list = data
#tts google
credential_pathTTS = get_password(credentials_list, 'tts google credential_path')
credential_pathYT = get_password(credentials_list, 'youtube CLIENT_SECRET_FILE')
try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_pathTTS
    client = texttospeech_v1.TextToSpeechClient()
except:
    print("must provide path")
#reddit info
reddit_password = get_reddit_password(credentials_list, 'reddit praw')
Rclient_id = reddit_password[0]   
Rclient_secret = reddit_password[1]
Rpassword = reddit_password[2]
Ruser_agent = reddit_password[3]
Rusername = reddit_password[4]


subReddit = "AskReddit"
maxLengthOfParent = "90"
maxScoreOfParent = "10000"
maxComment = "1000"
def on_button_click():
    global Rclient_id
    global credential_pathTTS
    global credential_pathYT
    global Rclient_secret
    global Rusername
    global Ruser_agent
    global Rpassword
    global subReddit
    global maxLengthOfParent
    global maxScoreOfParent
    global maxComment
    credential_pathTTS = passwordTTS.get()
    credential_pathYT = passwordYT.get()
    subReddit = entry.get()
    Rclient_id = Rclient_idValue.get()
    Rclient_secret = Rclient_secretValue.get()
    Rpassword = RpasswordValue.get()
    Ruser_agent = Ruser_agentValue.get()
    Rusername = RusernameValue.get()
    maxLengthOfParent = lengthParent.get()
    maxComment = commentParent.get()
    maxScoreOfParent = scoreParent.get()

    data[0]['credential_path'] = credential_pathTTS #tts
    data[1]['credential_path'] = credential_pathYT #yt
    data[2]['client_id'] = Rclient_id #reddit praw 
    data[2]['client_secret'] = Rclient_secret 
    data[2]['password'] = Rpassword
    data[2]['user_agent'] = Ruser_agent
    data[2]['username'] = Rusername

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
    print("Subreddit changed to:", subReddit)



text_label = ttk.Label(window, text="Select subreddit", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

#subreddit
text_variable = tk.StringVar(window, value=subReddit)


entry = tk.Entry(window, textvariable=text_variable)
entry.pack()

#length
text_label = ttk.Label(window, text="Select max length of parent comment", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

length = tk.StringVar(window, value=maxLengthOfParent)


lengthParent = tk.Entry(window, textvariable=length)
lengthParent.pack()

#length
text_label = ttk.Label(window, text="Select max ammount of comments", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

comment = tk.StringVar(window, value=maxComment)


commentParent = tk.Entry(window, textvariable=comment)
commentParent.pack()

#score
text_label = ttk.Label(window, text="Select max length of parent score", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

score = tk.StringVar(window, value=maxScoreOfParent)


scoreParent = tk.Entry(window, textvariable=score)
scoreParent.pack()
#score
text_label = ttk.Label(window, text="Select Reddit Client_id", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

score = tk.StringVar(window, value=Rclient_id)


Rclient_idValue = tk.Entry(window, textvariable=score)
Rclient_idValue.pack()
#split
text_label = ttk.Label(window, text="Select Reddit Client_secret", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

score = tk.StringVar(window, value=Rclient_secret)


Rclient_secretValue = tk.Entry(window, textvariable=score)
Rclient_secretValue.pack()
#split
text_label = ttk.Label(window, text="Select Reddit Password", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

score = tk.StringVar(window, value=Rpassword)


RpasswordValue = tk.Entry(window, textvariable=score)
RpasswordValue.pack()
#split
text_label = ttk.Label(window, text="Select Reddit User_agent", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

score = tk.StringVar(window, value=Ruser_agent)


Ruser_agentValue = tk.Entry(window, textvariable=score)
Ruser_agentValue.pack()
#split
text_label = ttk.Label(window, text="Select Reddit Username", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

score = tk.StringVar(window, value=Rusername)


RusernameValue = tk.Entry(window, textvariable=score)
RusernameValue.pack()


#set passwords
text_label = ttk.Label(window, text="Select PasswordTTS", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

#subreddit
text_variable = tk.StringVar(window, value=credential_pathTTS)


passwordTTS = tk.Entry(window, textvariable=text_variable)
passwordTTS.pack()

#set passwords
text_label = ttk.Label(window, text="Select PasswordYT", font=("TkDefaultFont", 10))
text_label.pack(pady=5)

#subreddit
text_variable = tk.StringVar(window, value=credential_pathYT)


passwordYT = tk.Entry(window, textvariable=text_variable)
passwordYT.pack()



button = tk.Button(window, text="Apply", command=on_button_click)
button.pack()


run_button = ttk.Button(window, text="Run Reddit Video Generator", command=lambda: run_python_code(subReddit, maxLengthOfParent, maxScoreOfParent, maxComment, credential_pathTTS, credential_pathYT, Rclient_id, Rclient_secret, Rpassword, Ruser_agent, Rusername))
run_button.pack(pady=10)

# Create a label to display the output of the Python code
output_label = ttk.Label(window, text="")
output_label.pack(pady=10)

window.mainloop()
