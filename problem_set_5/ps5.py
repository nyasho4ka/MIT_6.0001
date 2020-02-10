# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
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


class NewsStory:
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


class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase.lower()

    def is_phrase_in(self, text):
        text = self.format_text(text)
        return self.is_phrase_in_text(text)

    def format_text(self, text):
        text = self.remove_punctuation(text)
        text = self.reduce_multiple_spaces_to_single(text)
        text = self.cast_to_lowercase(text)
        return text

    @staticmethod
    def remove_punctuation(text):
        new_text = text

        for punctuation in string.punctuation:
            new_text = new_text.replace(punctuation, ' ')

        return new_text

    @staticmethod
    def reduce_multiple_spaces_to_single(text):
        return ' '.join(text.split())

    @staticmethod
    def cast_to_lowercase(text):
        return text.lower()

    def is_phrase_in_text(self, text):
        return self.phrase in text and not (self.is_letter_before(text) or self.is_letter_after(text))

    def is_letter_before(self, text):
        if text.startswith(self.phrase):
            return False

        index_before = text.find(self.phrase) - 1
        if text[index_before] in string.ascii_letters:
            return True

        return False

    def is_letter_after(self, text):
        if text.endswith(self.phrase):
            return False

        index_after = text.find(self.phrase) + len(self.phrase)
        if text[index_after] in string.ascii_letters:
            return True

        return False


# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.title)


# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.description)

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.


class TimeTrigger(Trigger):
    datetime_format = '%d %b %Y %H:%M:%S'

    def __init__(self, string_datetime):
        self.date = datetime.strptime(string_datetime, self.datetime_format).replace(tzinfo=pytz.timezone('EST'))


# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.pubdate
        if not story.pubdate.tzinfo:
            pubdate = story.pubdate.replace(tzinfo=pytz.timezone('EST'))
        return (self.date - pubdate).total_seconds() > 0


class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        pubdate = story.pubdate
        if not story.pubdate.tzinfo:
            pubdate = story.pubdate.replace(tzinfo=pytz.timezone('EST'))
        return (pubdate - self.date).total_seconds() > 0

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
    def __init__(self, first_trigger, second_trigger):
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger

    def evaluate(self, story):
        return self.first_trigger.evaluate(story) and self.second_trigger.evaluate(story)
# Problem 9
# TODO: OrTrigger


class OrTrigger(Trigger):
    def __init__(self, first_trigger, second_trigger):
        self.first_trigger = first_trigger
        self.second_trigger = second_trigger

    def evaluate(self, story):
        return self.first_trigger.evaluate(story) or self.second_trigger.evaluate(story)


TRIGGER_TYPE_TO_CLASS = {
    'TITLE': TitleTrigger,
    'DESCRIPTION': DescriptionTrigger,
    'AFTER': AfterTrigger,
    'BEFORE': BeforeTrigger,
    'NOT': NotTrigger,
    'AND': AndTrigger,
    'OR': OrTrigger,
}


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
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    filtering_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                filtering_stories.append(story)
                break
    return filtering_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
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
    # lines is the list of lines that you need to parse and for which you need
    # to build triggers
    trigger_list = list()
    trigger_dict = dict()
    for trigger in lines:
        if trigger.startswith('ADD'):
            add_trigger_to_trigger_list(trigger, trigger_dict, trigger_list)
        else:
            # Parse line: trigger name, trigger type, trigger arguments
            trigger_name, trigger_type, *trigger_args = parse_trigger_line(trigger)
            # If trigger type is binary (AND or OR)
            if is_trigger_binary(trigger_type):
                # convert trigger arguments from string to trigger objects from trigger dict
                trigger_args = convert_string_arguments_to_triggers(trigger_dict, trigger_args)
            # create new trigger with trigger type and trigger arguments
            new_trigger = create_new_trigger(trigger_type, *trigger_args)
            # add new trigger to trigger dict
            trigger_dict.update({trigger_name: new_trigger})
        pass

    print(lines)  # for now, print it so you see what it contains!
    return trigger_list


def add_trigger_to_trigger_list(trigger_line, trigger_dict, trigger_list):
    # get trigger names from line
    trigger_names = trigger_line.split(',')[1:]
    # add triggers to trigger list from trigger dict by names
    for trigger_name in trigger_names:
        if trigger_name in trigger_dict:
            trigger_list.append(trigger_dict.get(trigger_name, None))


def parse_trigger_line(trigger_line):
    return trigger_line.split(',')


def is_trigger_binary(trigger_type):
    return trigger_type == 'AND' or trigger_type == 'OR'


def convert_string_arguments_to_triggers(trigger_dict, trigger_arguments):
    trigger_list = []
    for trigger in trigger_arguments:
        if trigger in trigger_dict:
            trigger_list.append(trigger_dict.get(trigger, None))
    return trigger_list


def create_new_trigger(trigger_type, *trigger_args):
    return TRIGGER_TYPE_TO_CLASS[trigger_type](*trigger_args)



SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        # t1 = TitleTrigger("election")
        # t2 = DescriptionTrigger("Trump")
        # t3 = DescriptionTrigger("Clinton")
        # t4 = AndTrigger(t2, t3)
        # triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('own_trigger.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
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
# if __name__ == '__main__':
#     trigger_list = read_trigger_config('triggers.txt')
