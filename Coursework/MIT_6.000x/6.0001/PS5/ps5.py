"""
Problem Set 5 - RSS Feed Filter
"""
import feedparser
import string
import time
import threading
from project_util import translate_html
#from mtTkinter import *
import mtTkinter as Tk
#from mtTkinter import Tk, Label, Button, Frame, Scrollbar, StringVar, Text
from datetime import datetime
import pytz
#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1
# TODO: NewsStory
class NewsStory():
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description 
        self.link = link
        self.pubdate = pubdate
    
    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_description(self):
        return self.description
    
    def get_link(self):
        return self.link
    
    def get_pubdate(self):
        return self.pubdate
        
#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        """
        phrase (string): its the trigger phrase. 
                         one or more words separated by a single space between the words.
        Trigger should not be case-sensitive (it should treat "Intel" and "intel" as being equal).
        """
        self.phrase = phrase.lower()
    
    def is_phrase_in(self, text):
        """
        text (string) : any text, examples of text snippets below.
        
        Returns: True if the whole trigger phrase is present in text, False otherwise.
        
        For example, a phrase trigger with the phrase "purple cow" 
        should fire on the following text snippets: 
            ●'PURPLE COW'
            ●'The purple cow is soft and cuddly.'
            ●'The farmer owns a really PURPLE cow.'
            ●'Purple!!! Cow!!!'
            ●'purple@#$%cow'
            ●'Did you see a purple cow?'
        But it should not fire on these text snippets: 
            ●'Purple cows are cool!'
            ●'The purple blob over there is a cow.'
            ●'How now brown cow.'
            ●'Cow!!! Purple!!!'
            ●'purplecowpurplecowpurplecow'
        """
        text = text.lower()
        #Map special characters to whitespaces
        translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))
        text = text.translate(translator)
        
        #split words of 'phrase' and 'trigger' with space as separetor
        text_list = text.split()
        phrase_list = list(self.phrase.split())
        
        #compare 'text_list' and 'phrase_list' for consecutives
        for word_index in range(len(text_list) - len(phrase_list) + 1):
            if text_list[word_index:word_index+len(phrase_list)] == phrase_list:
                return True
        return False
            
# Problem 3
# TODO: TitleTrigger
# It is an abstract class, we will not be directly instantiating any PhraseTriggers.
# Note: instantiation creates an instance of an object.
class TitleTrigger(PhraseTrigger):
    #override the default evaluate method of superclass 'Trigger'
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())
    
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger (abstrtact class)
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        """
        time (string): in EST and in the format of "%d %b %Y %H:%M:%S".
                        ex. "3 Oct 2016 17:00:10"
        """
        self.time = datetime.strptime(time, "%d %b %Y %H:%M:%S").replace(tzinfo=pytz.timezone('EST'))
    
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        """
        BeforeTrigger fires when a story is published strictly before the trigger’s time
        """
        return story.get_pubdate().replace(tzinfo=pytz.timezone('EST')) < self.time
class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        """
        AfterTrigger fires when a story is published strictly after the trigger’s time
        """
        return story.get_pubdate().replace(tzinfo=pytz.timezone('EST')) > self.time

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger

    def evaluate(self, story):
        return not self.trigger.evaluate(story)

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)
    
#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    filtered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtered_stories.append(story)
    return filtered_stories

    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
#    return stories

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need to build triggers
    triggers_map = {}  # Dictionary of trigger names in files. keys == trigger_name
    triggers = []    # List of trigger objects specified in config file
    for line in lines:        
        param = line.split(',')  # param (list)
        if param[0] == 'ADD':
            for trigger_name in param[1:]:
                triggers.append(triggers_map[trigger_name])
        elif param[1] == 'TITLE':
            triggers_map[param[0]] = TitleTrigger(param[2])
        elif param[1] == 'DESCRIPTION':
            triggers_map[param[0]] = DescriptionTrigger(param[2])
        elif param[1] == 'AFTER':
            triggers_map[param[0]] = AfterTrigger(param[2])
        elif param[1] == 'BEFORE':
            triggers_map[param[0]] = BeforeTrigger(param[2])
        elif param[1] == 'NOT':
            triggers_map[param[0]] = NotTrigger(triggers_map[param[2]])
        elif param[1] == 'AND':
            triggers_map[param[0]] = AndTrigger(triggers_map[param[2]], triggers_map[param[3]])
        elif param[1] == 'OR':
            triggers_map[param[0]] = OrTrigger(triggers_map[param[2]], triggers_map[param[3]])
    return triggers
    
    print(lines) # for now, print it so you see what it contains!

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("coronavirus")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("China")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Tk.Frame(master)
        frame.pack(side=Tk.BOTTOM)
        scrollbar = Tk.Scrollbar(master)
        scrollbar.pack(side=Tk.RIGHT,fill=Tk.Y)

        t = "Google & Yahoo Top News"
        title = Tk.StringVar()
        title.set(t)
        ttl = Tk.Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=Tk.TOP)
        cont = Tk.Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=Tk.BOTTOM)
        cont.tag_config("title", justify='center')
        button = Tk.Button(frame, text="Exit", command=root.destroy)
        button.pack(side=Tk.BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(Tk.END, newstory.get_title()+"\n", "title")
                cont.insert(Tk.END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(Tk.END, newstory.get_description())
                cont.insert(Tk.END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()

