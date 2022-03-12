from reddit_scraper import RedditScraper
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
import nltk
from databases import CourseScrapingDatabase

class Analyzer:

    def get_cs_keywords(self) -> set:
        with CourseScrapingDatabase() as database:
            course_info = database.get_all_course_info()
        # I love python
        # keywords = [(info['course_name'], ' '.join(info['course_name'].split(' ')[0:-1]))[info['course_name'].split(' ')[-1][-1] == 'I' or info['course_name'].split(' ')[-1][-1] == 'V'] for info in course_info]
        keywords = []
        for info in course_info:
            name = info['course_name']
            # Remove the I's and V's from the course names
            name = (name, ' '.join(name.split(' ')[0:-1]))[
                name.split(' ')[-1][-1] == 'I' or name.split(' ')[-1][-1] == 'V']
            keywords.append(name.lower())
        keywords.append('computer science')
        keywords.append('computer')
        keywords.append('cs')
        keywords.append('cst')
        return set(keywords)
    # makes charts and converts them into a pdf file
    def __make_charts(self, all_data, data_type, most_common_path, least_common_path):
        import matplotlib.pyplot as plt
        most_common = FreqDist(self.__filter_data(all_data))
        fig = plt.figure()
        fig.set_size_inches(20, 10.5)
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.title(f"Most common keywords from {data_type} ")
        most_common.plot(5)
        fig.savefig(most_common_path)
        fig_2 = plt.figure()
        fig_2.set_size_inches(20, 10.5)
        plt.gcf().subplots_adjust(bottom=0.15)
        least_common = FreqDist(most_common.most_common()[-5:])
        plt.title(f"Least common keywords from {data_type} ")
        least_common.plot()
        fig_2.savefig(least_common_path)

    # plots the most common keywords for post titles
    def get_common_title_keywords_charts(self, data):
        all_titles = ""
        for i in data:
            import string
            all_titles += f"{i['title']} "
        # titles
        self.__make_charts(all_titles, 'titles',
                           './graphs/most_popular_title_keywords.pdf',
                           './graphs/least_popular_title_keywords.pdf')
    # plots the most common keywords for post or comment text
    def get_common_text_keywords(self, data, data_type):
        all_text = ""
        for i in data:
            import string
            # remove punctuation
            if data_type == "submissions":
                all_text += f"{i['selftext'].translate(str.maketrans('', '', string.punctuation))} "
            elif data_type == "comments":
                all_text += f"{i['body'].translate(str.maketrans('', '', string.punctuation))} "
            else:
                raise Exception
        self.__make_charts(all_text, data_type,
                           f'./graphs/most_popular_{data_type}_text_keywords.pdf',
                           f'./graphs/least_popular_{data_type}_text_keywords.pdf')

    # gets the average length of posts or comments
    def get_average_length_data(self, data, data_type):
        length_data = 0
        count_data = 0
        average_length = 0
        for i in data:
            count_data += 1
            if data_type == "submissions":
                text = i['selftext']
            elif data_type == "comments":
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
        computer_words = {'computer', 'science', 'technology', '?', "'" , ","}
        double_filtered_data = [w for w in filtered if not w.casefold() in computer_words]
        return double_filtered_data

    # gets posts and returns a list sorted by number of upvotes
    def get_most_upvoted_posts(self, data):
        # sorting most popular posts
        return self.__fill_list(data)[:5]

    def get_least_upvoted_posts(self, data):
        # sorting most popular posts
        return self.__fill_list(data)[-5:]

    def __fill_list(self, data):
        cs_posts = []
        for i in data['data']['children']:
            post = {'title': i['data']['title'], 'ups': i['data']['ups'], 'body': i['data']['selftext_html']}
            cs_posts.append(post)
        sorted_cs_posts = sorted(cs_posts, key=lambda value: value['ups'], reverse=True)
        return sorted_cs_posts
    def get_monthly_frequency(self, keywords):
        import matplotlib.pyplot as plt
        jan_mar = [1609462800, 1617152400]
        apr_jun = [1617238800, 1625014800]
        jul_sep = [1625101200, 1632963600]
        oct_dec = [1633050000, 1640912400]
        q1 = len(s.search_dates(keywords, jan_mar))
        q2 = len(s.search_dates(keywords, apr_jun))
        q3 = len(s.search_dates(keywords, jul_sep))
        q4 = len(s.search_dates(keywords, oct_dec))
        names = ["jan-mar", "apr-jun", "jul-sep", "oct-dec"]
        values = [q1, q2, q3, q4]
        plt.title("Frequency of posts by months")
        plt.bar(names, values)
        plt.savefig('./graphs/frequency_of_dates_plot.pdf')
        plt.show()


if __name__ == '__main__':
    s = RedditScraper()

    submissions = s.search_submission(['computer science'])
    comments = s.search_comments(['computer science'])
    # comments = s.search_comments(['computer science'])
    a = Analyzer()
    a.get_common_title_keywords_charts(submissions)
    a.get_common_text_keywords(comments, 'comments')
    a.get_common_text_keywords(submissions, 'submissions')
    a.get_monthly_frequency(['computer science'])