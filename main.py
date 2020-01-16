import pandas
import matplotlib.pyplot as plt

#add the music datasets
triplets_file = 'https://static.turi.com/datasets/millionsong/10000.txt'
songs_metadata_file = 'https://static.turi.com/datasets/millionsong/song_data.csv'

#load the datasets using Pandas Library
song_df_1 = pandas.read_table(triplets_file, header=None)
song_df_1.columns = ['user_id', 'song_id', 'listen_count']

song_df_2 = pandas.read_csv(songs_metadata_file)
song_df = pandas.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")

song_df.head()

song_df = song_df.head(10000)
