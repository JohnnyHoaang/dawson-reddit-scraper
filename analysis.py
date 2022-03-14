from reddit_scraper import RedditScraper
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
import nltk
from databases import CourseScrapingDatabase


class Analyzer:
    # Returns keywords about computer science
    def get_cs_keywords(self):
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

    # Makes charts of most/common keywords of data and converts them into a pdf file
    def __make_keyword_charts(self, all_data, data_type, most_common_path, least_common_path):
        import matplotlib.pyplot as plt
        most_common = FreqDist(self.__filter_data(all_data))
        fig = plt.figure()
        # create figure for the first plot
        fig.set_size_inches(10, 10)
        # readjusts the size of the figure
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.title(f"Most common keywords from {data_type} ")
        # Plots most common keywords
        most_common.plot(5)
        fig.savefig(most_common_path)
        fig_2 = plt.figure()
        # create figure for the first plot
        fig_2.set_size_inches(10, 10)
        plt.gcf().subplots_adjust(bottom=0.15)
        least_common = FreqDist(most_common.most_common()[-5:])
        plt.title(f"Least common keywords from {data_type} ")
        # Plots least common keywords
        least_common.plot()
        fig_2.savefig(least_common_path)

    # Plots the most/least common keywords for post titles
    def get_common_title_keywords_charts(self, data):
        all_titles = ""
        for i in data:
            import string
            all_titles += f"{i['title'].translate(str.maketrans('', '', string.punctuation))} "
        # titles
        self.__make_keyword_charts(all_titles, 'titles',
                                   './graphs/most_popular_title_keywords.png',
                                   './graphs/least_popular_title_keywords.png')

    # Plots the most/least common keywords for post or comment text
    def get_common_text_keywords(self, data, data_type):
        all_text = ""
        for i in data:
            import string
            if data_type == "submissions":
                all_text += f"{i['selftext'].translate(str.maketrans('', '', string.punctuation))} "
                # remove punctuation from string
            elif data_type == "comments":
                all_text += f"{i['body'].translate(str.maketrans('', '', string.punctuation))} "
            else:
                raise Exception
        self.__make_keyword_charts(all_text, data_type,
                                   f'./graphs/most_popular_{data_type}_text_keywords.png',
                                   f'./graphs/least_popular_{data_type}_text_keywords.png')

    # Returns the average length of posts or comments
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

    # Returns the number of sentences of a post or comment
    def __get_number_of_sentences(self, data, data_type):
        text = ''
        count = 0
        count_sentence = 0
        for i in data:
            if data_type == "comments":
                text = i['body']
            elif data_type == "submissions":
                text = i['selftext']
            count_sentence += len(sent_tokenize(text))
            count += 1
        return count_sentence / count

    # Generates a graph that represents the average number of sentences for posts and comments
    def get_chart_average_number_of_sentence(self, submissions, comments):
        import matplotlib.pyplot as plt
        names = ["submissions", "comments"]
        values = [self.__get_number_of_sentences(submissions, "submissions"),
                  self.__get_number_of_sentences(comments, "comments")]
        plt.title("Average number of sentences for posts and comments")
        plt.bar(names, values)
        plt.savefig("./graphs/average_num_of_sentences.png")
        plt.show()

    # Removes stop words and cs words to filter the data
    def __filter_data(self, data):
        stop_words = set(stopwords.words('english'))
        filter_data = word_tokenize(data)
        filtered = [d for d in filter_data if not d.casefold() in stop_words]
        computer_words = {'computer', 'science', 'technology', 'cs', 'cst', '’'}
        double_filtered_data = [w for w in filtered if not w.casefold() in computer_words]
        return double_filtered_data

    # Fetches posts and returns a list of most upvoted posts
    def get_most_upvoted_posts(self, data):
        # sorting most popular posts
        return self.__fill_list(data)[:5]

    # Fetches posts and returns a list of least upvoted posts
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

    # Returns the epoch values for each month
    def __get_epoch_values(self):
        months = {"jan-mar": [1609459200, 1617148800], "apr-jun": [1617235200, 1625011200],
                  "jul-sep": [1625097600, 1632960000], "oct-dec": [1633046400, 1640908800]}
        return months

    # Returns posts according to months
    def __get_all_posts_from_dates(self, keywords, months):
        rs = RedditScraper()
        values = [len(rs.search_dates(keywords, months["jan-mar"])), len(rs.search_dates(keywords, months["apr-jun"])),
                  len(rs.search_dates(keywords, months["jul-sep"])),
                  len(rs.search_dates(keywords, months["oct-dec"]))]
        return values

    # Plots the amount of posts per interval of months
    def get_monthly_frequency(self, keywords):
        import matplotlib.pyplot as plt
        all_months = self.__get_epoch_values()
        names = ["january-march", "april-june", "july-september", "october-december"]
        values = self.__get_all_posts_from_dates(keywords, all_months)
        plt.title("Frequency of posts by months in 2021")
        plt.bar(names, values)
        plt.savefig('./graphs/frequency_of_dates_plot.png')
        plt.show()


# creates all graphs for the analysis report
def create_analysis_graphs():
    rs = RedditScraper()
    submissions = rs.search_submission(['computer science'])
    comments = rs.search_comments(['computer science'])
    a = Analyzer()
    a.get_common_title_keywords_charts(submissions)
    a.get_common_text_keywords(comments, 'comments')
    a.get_common_text_keywords(submissions, 'submissions')
    a.get_chart_average_number_of_sentence(submissions, comments)
    a.get_monthly_frequency(['computer science'])
