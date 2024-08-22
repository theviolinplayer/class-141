from flask import Flask, jsonify
import pandas as pd
from demographic_filtering import output
from content_filtering import get_recommendations

movies_data = pd.read_csv('final.csv')

app = Flask(__name__)

# extracting important information from dataframe
all_movies = movies_data[["original_title","poster_link","release_date","runtime","weighted_rating"]]
liked_movies = []
disliked_movies = []
did_not_watch = []

# method to fetch data from database
def assign_movie():
  m_data = {"original_title":all_movies.iloc[0,0],
            "poster_link":all_movies.iloc[0,1],
            "release_date":all_movies.iloc[0,2] or "N/A",
            "runtime":all_movies.iloc[0,3],
            "weighted_rating":all_movies.iloc[0,4]/2
            }
  return m_data

#popular movies demographic
@app.route("/popular")
def pop_movies():
  movies = []
  for index, row in output.iterrows():
    temp = {
      "original_title":row["original_title"],
      "poster_link":row["poster_link"],
      "release_date":row["release_date"] or "N/A",
      "runtime":row["runtime"],
      "weighted_rating":row["weighted_rating"]/2
    }
    movies.append(temp)
  return jsonify({
    "data":movies,
    "status":"success"
  })

@app.route("/recommended")
def recommended_mov():
  global liked_movies
  all_recommended = pd.DataFrame(columns = ["original_title","poster_link","release_date","runtime","weighted_rating"])
  for movie in liked_movies:
    output = get_recommendations(movie["original_title"])
    all_recommended = all_recommended.append(output)

  movies = []
  for index, row in all_recommended.iterrows():
    temp = {
      "original_title":row["original_title"],
      "poster_link":row["poster_link"],
      "release_date":row["release_date"] or "N/A",
      "runtime":row["runtime"],
      "weighted_rating":row["weighted_rating"]/2
    }
    movies.append(temp)
  return jsonify({
    "data":movies,
    "status":"success"
  })

# /movies api
@app.route("/movies")
def get_movie():
  movie = assign_movie()
  return jsonify({
    "data":movie,
    "status":"success"
  })

# /like api
@app.route("/like")
def like_movie():
  global all_movies
  movie = assign_movie()
  liked_movies.append(movie)
  all_movies.drop([0], inplace = True)
  all_movies = all_movies.reset_index(drop = True)
  return jsonify({
    "status":"success"
  })

# /dislike api
@app.route("/dislike")
def dislike_movie():
  global all_movies
  movie = assign_movie()
  disliked_movies.append(movie)
  all_movies.drop([0], inplace = True)
  all_movies = all_movies.reset_index(drop = True)
  return jsonify({
    "status":"success"
  })

# /did_not_watch api
@app.route("/didntwatch")
def didnot():
  global all_movies
  movie = assign_movie()
  did_not_watch.append(movie)
  all_movies.drop([0], inplace = True)
  all_movies = all_movies.reset_index(drop = True)
  return jsonify({
    "status":"success"
  })

@app.route("/likes")
def likes():
  global liked_movies
  return jsonify({
    "status":"success",
    "data":liked_movies
  })

if __name__ == "__main__":
  app.run()

