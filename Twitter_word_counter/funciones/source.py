import re
from stop_words import get_stop_words
import twitter

def word_counter(array):
    acceptable_languages = ['arabic', 'bulgarian', 'catalan', 'czech', 'danish', 'dutch', 'english', 'finnish',
                            'french', 'german', 'hungarian', 'indonesian', 'italian',
                            'norwegian', 'polish', 'portuguese', 'romanian', 'russian', 'spanish', 'swedish', 'turkish',
                            'ukrainian']

    if not isinstance(array, str):
        raise TypeError

    string_list_lowercase = []
    final_list = []
    list_aux = []
    forbidden_words = []

    for language in acceptable_languages:
        forbidden_words.append(get_stop_words(language))

    word_list = (array.lower()).split()

    for word in word_list:
        is_stopword = 0
        for forbidden in forbidden_words:

            if word in forbidden and is_stopword == 0:
                is_stopword = 1

        if is_stopword == 0:
            list_aux.append(word)

    for x in list_aux:
        reemplazo = re.sub("[^\w]", "", x)
        if reemplazo != '':
            string_list_lowercase.append(re.sub("[^\w]", "", x))

    while len(string_list_lowercase) > 0:
        current_word = string_list_lowercase[0]
        counter = string_list_lowercase.count(current_word)
        while current_word in string_list_lowercase:
            string_list_lowercase.remove(current_word)

        final_list.append([current_word, counter])

    return sorted(final_list, key=lambda x: x[1], reverse=True)


'''CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN_KEY = os.environ['ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']'''

class Twitter2:

    def __init__(self,username):
        self.username = username

    def word_count(self):
        api = twitter.Api(consumer_key='xJBNVbtmRJrd44fslR38GiJNr',
                          consumer_secret='w22znbElOOjVs2oYORs2hqxmUF1K6MfJ3YUEoefttZVDG5SbwW',
                          access_token_key='831510109629071361-OFLx61XL1iiFQNDvH1OeBYgBWZn5dQR',
                          access_token_secret='l3NObDqc4psYpok3YSv7HFKwuVEAdijABoE0WSE3CEfDT')

        tweets = api.GetUserTimeline(screen_name= self.username, count=200, exclude_replies=True, include_rts=False)[
               0:50]

        array = ''
        for tweet in tweets:
            exclude = []
            for url in tweet.urls:
                exclude.append(url.url)
            if tweet.media is not None:
                for media in tweet.media:
                    exclude.append(media.url)
            aux = tweet.text.split()
            array = array + ' '.join([i for i in aux if i not in exclude]) + ' '
        return word_counter(array)[0:20]