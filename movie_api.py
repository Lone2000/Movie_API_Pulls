import requests_with_caching
import json

def get_movies_from_tastedive(find):
    base_url = 'https://tastedive.com/api/similar'
    para_dict = {}
    para_dict['q'] = find
    para_dict['limit'] = 5
    para_dict['type'] = 'movies'
    
    req = requests_with_caching.get(base_url, para_dict)
    print(req.url)
    return json.loads(req.text)

def extract_movie_titles(movie_dict):
    movie_titles = []
    for movie in movie_dict["Similar"]["Results"]:
        movie_titles.append(movie["Name"])
    return movie_titles
        


# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages
def get_related_titles(movie_titles_lst):
    combined_movie_lst = []
    for title in movie_titles_lst:
        movie_dict = get_movies_from_tastedive(title)
        for elm in extract_movie_titles(movie_dict):
            if elm not in combined_movie_lst:
                combined_movie_lst.append(elm)
            else:
                pass
    return combined_movie_lst

def get_movie_data(title):
    base_url = "http://www.omdbapi.com/"
    para_dict = {}
    para_dict["t"] = title
    para_dict["r"] = 'json'
    
    res = requests_with_caching.get(base_url, para_dict)

    return json.loads(res.text)
    
def get_movie_rating(movie_info):
    #print(movie_info["Ratings"])
    for source in movie_info["Ratings"]:
        if source["Source"] == "Rotten Tomatoes":
            return int(source["Value"].replace("%",""))
        else:
            continue
        
    return 0

# some invocations that we use in the automated tests; uncomment these if you are getting errors and want better error messages

def get_sorted_recommendations(movie_lst):
    related_movies_lst = get_related_titles(movie_lst)
    x = sorted(related_movies_lst, key=lambda movie: -get_movie_rating(get_movie_data(movie)))
    return x


get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"])



