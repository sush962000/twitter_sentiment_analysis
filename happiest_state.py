import sys
import json 

# parse sentiment file and create a <term, sentiment_score> dictionary
def parse_sentiment_file(sent_file):
    sentiment = sent_file
    # read each line and add to the dict
    sentiment_dict = {}
    for line in sentiment:
        sentiment_list = line.split("\t")
        sentiment = sentiment_list[0]
        try:
            sentiment_value = int(sentiment_list[1])
        except ValueError:
            sentiment_value = 0.0
        if  sentiment not in sentiment_dict:
            sentiment_dict[sentiment] = sentiment_value
    return sentiment_dict


# determine the sentiment score of each tweet
def score_tweet(pytweet, sentiment_dict):
    if pytweet.has_key("text"):
        tweettext = pytweet["text"].encode('utf-8')
        tweettext.replace("#", "")
        wordlist = tweettext.strip().split()
        sentiment_count = 0.0

        for word in wordlist:
            if word in sentiment_dict:
                sentiment_count = sentiment_count + sentiment_dict[word]

        return sentiment_count

        
def create_list_of_states():    
    state_list = [("Alabama", "AL"), ("Alaska", "AK"), ("Arizona", "AZ"), ("Arkansas", "AR"),
                  ("California", "CA"), ("Colorado", "CO"), ("Connecticut", "CT"),
                  ("Delaware", "DE"), ("Florida", "FL"), ("Georgia", "GA"), ("Hawaii", "HI"),
                  ("Idaho", "ID"), ("Illinois", "IL"), ("Indiana", "IN"), ("Iowa", "IA"),
                  ("Kansas", "KS"), ("Kentucky", "KY"), ("Louisiana", "LA"), ("Maine", "ME"),
                  ("Maryland", "MD"), ("Massachusetts", "MA"), ("Michigan", "MI"),
                  ("Minnesota", "MN"), ("Mississippi", "MS"), ("Missouri", "MO"),
                  ("Montana", "MT"), ("Nebraska", "NE"), ("Nevada", "NV"),
                  ("New Hampshire", "NH"), ("New Jersey", "NJ"), ("New Mexico", "NM"),
                  ("New York", "NY"), ("North Carolina", "NC"), ("North Dakota", "ND"),
                  ("Ohio", "OH"), ("Oklahoma", "OK"), ("Oregon", "OR"), ("Pennsylvania", "PA"),
                  ("Rhode Island", "RI"), ("South Carolina", "SC"), ("South Dakota", "SD"),
                  ("Tennessee", "TN"), ("Texas", "TX"), ("Utah", "UT"), ("Vermont", "VT"),
                  ("Virginia", "VA"), ("Washington", "WA"), ("West Virginia", "WV"),
                  ("Wisconsin", "WI"), ("Wyoming", "WY")]

    return state_list

# helper method to check which state it originates from
def location_matches_a_state(location, state_list):
    for index in range(len(state_list)):
        if state_list[index][0].lower() in location.lower() or state_list[index][1].lower() == location.lower():
            return state_list[index][0]   
       
               
# decode the tweet to determine the user location and create a <state, happiness_score> dictionary
def create_state_happiness_dictionary(tweet_file, state_list, sentiment_dict):
    tweet = tweet_file
    state_happiness_dictionary = {}
    state_tweet_count = {}
    for line in tweet:
        pytweet = json.loads(line)
        if pytweet.has_key("user") and pytweet["user"].has_key("location"):
            location = pytweet["user"]["location"].encode('utf-8')
            # check if the origin is from any of the states
            abbreviated_state = location_matches_a_state(location, state_list)
            # if you get a real state, add it to the dictionary and
            # increase the sentiment score for that state
            if  abbreviated_state != "":
                sentiment_score = score_tweet(pytweet, sentiment_dict)
                if state_happiness_dictionary.has_key(abbreviated_state):
                    state_happiness_dictionary[abbreviated_state] += sentiment_score
                    state_tweet_count[abbreviated_state] += 1
                else:
                    if abbreviated_state != None:
                        state_happiness_dictionary[abbreviated_state] = sentiment_score
                        state_tweet_count[abbreviated_state] = 1
    for key in state_happiness_dictionary:
        state_happiness_dictionary[key] /= state_tweet_count[key]
        
    return state_happiness_dictionary

def print_happiness_score_of_states(state_happiness_dictionary):
    print(state_happiness_dictionary)
    # print max(state_happiness_dictionary, key=state_happiness_dictionary.get)
            


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])   

    # parse sentiment file and create a <term, sentiment_score> dictionary
    sentiment_dict = parse_sentiment_file(sent_file)        

    # create the state_list
    state_list = create_list_of_states()

    # determine the sentiment of each tweet and it's origin state
    # create a <state, happiness> dictionary by aggregating the sentiment score of each tweet originating in that state
    state_happiness_dictionary = create_state_happiness_dictionary(tweet_file, state_list, sentiment_dict)

    # print happiness scores of states
    print_happiness_score_of_states(state_happiness_dictionary)
    

if __name__ == '__main__':
    main()
