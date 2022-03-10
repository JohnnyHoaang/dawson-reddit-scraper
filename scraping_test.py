from reddit_scraper import RedditScraper
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist


class Analyzer:
    # gets the most common keywords for post titles
    def get_common_title_keywords(self, data):
        all_titles = ""
        for i in data:
            import string
            all_titles += f"{i['title']} "
        # titles
        freq = FreqDist(self.__filter_data(all_titles))
        print("most common title keywords:")
        print(freq.most_common(5))
        print("least common title keywords:")
        print(freq.most_common()[-5:])

    # gets the most common keywords for post or comment text
    def get_common_text_keywords(self, data, data_type):
        all_text = ""
        for i in data:
            import string
            # remove punctuation
            if data_type == "submission":
                all_text += f"{i['selftext'].translate(str.maketrans('', '', string.punctuation))} "
            elif data_type == "comment":
                all_text += f"{i['body'].translate(str.maketrans('', '', string.punctuation))} "
            else:
                raise Exception
        freq = FreqDist(self.__filter_data(all_text))
        print("most common title keywords:")
        print(freq.most_common(5))
        print("least common title keywords:")
        print(freq.most_common()[-5:])

    # gets the average length of posts or comments
    def get_average_length_data(self, data, data_type):
        length_data = 0
        count_data = 0
        average_length = 0
        for i in data:
            count_data += 1
            if data_type == "submission":
                text = i['selftext']
            elif data_type == "comment":
                text = i["body"]
            else:
                raise Exception
            length_data += len(text)
        average_length = length_data / count_data
        return average_length

    # removes stop words and other to filter
    def __filter_data(self, data):
        stop_words = set(stopwords.words('english'))
        filter_data = word_tokenize(data)
        filtered = [d for d in filter_data if not d.casefold() in stop_words]
        computer_words = {'computer', 'science', 'technology'}
        double_filtered_data = [w for w in filtered if not w.casefold() in computer_words]
        return double_filtered_data
    # returns number of posts
    def get_frequency_of_posts(self, data):
        return len(data)

if __name__ == '__main__':
    s = RedditScraper()
    submissions = s.search_submission(['computer science'])
    comments = s.search_comments(['computer science'])
    a = Analyzer()
    print(f'Average post length: {a.get_average_length_data(submissions, "submission")}')
    print(f'Average comment length: {a.get_average_length_data(comments, "comment")}')
    a.get_common_title_keywords(submissions)
    a.get_common_text_keywords(comments, "comment")
    a.get_common_text_keywords(submissions, "submission")

    jan_mar = [1617152400, 1609462800]
    apr_jun = [1625014800, 1617238800]
    jul_sep = [1632963600,1625101200]
    oct_dec = [1640912400, 1633050000]
    q1 = a.get_frequency_of_posts(s.search_dates(['computer science'], jan_mar))
    q2 = a.get_frequency_of_posts(s.search_dates(['computer science'], apr_jun))
    q3= a.get_frequency_of_posts(s.search_dates(['computer science'], jul_sep))
    q4 = a.get_frequency_of_posts(s.search_dates(['computer science'], oct_dec))
    print(f"January to March: {q1}")
    print(f"April to June: {q2}")
    print(f"July to September: {q3}")
    print(f"October to December: {q4}")
