import numpy as np
import pandas

# class for collaborative filtering based Recommendation System
class collaborative_recommender_py():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.concurrence_matrix = None
        self.songs_dict = None
        self.rev_songs_dict = None
        self.collaborative_recommendations = None

    #get unique songs corresponding to a user
    def get_user_items(self, user):
        user_data = self.train_data[self.train_data[self.user_id] == user]
        user_items = list(user_data[self.item_id].unique())

        return user_items
    #get unique users for a given song
    def get_item_users(self, item):
        item_data = self.train_data[self.train_data[self.item_id] == item]
        item_users = set(item_data[self.user_id].unique())

        return item_users

    #concurrence matrix
    def make_concurrence_matrix(self, all_songs):

        user_songs_users = [] #users for all songs
        for i range(0, len(user_songs)):
            user_songs_users.append(self.get_item_users(user_songs_users[i]))

        #concurrence matrix of size- len(user_songs) X len(songs)
        concurrence_matrix = np.matrix(np.zeros(shape=(len(user_songs), len(all_songs))), float)

        #similarity between the user songs and all unique songs
        for i in range(0, len(all_songs)):
            #calculate the unique users of song j
            songs_i_data = self.train_data[self.train_data[self.item_id] == all_songs[i]]
            users_i = set(songs_i_data[self.user_id].unique())

            for j in range(0, len(user_songs)):
                #get unique users of song j
                users_j = user_songs_users[j]

                #calculate intersection of users of song i anf j
                user_intersection = users_i.intersection(users_j)

                if len(user_intersection) != 0:
                    users_union = users_i.union(users_j)
                    concurrence_matrix[j,i] = float(len(user_intersection))/float(len(users_union))
                else:
                    concurrence_matrix[j,i] = 0

        return concurrence_matrix

    #make Recommendations
    def top_recommendations(self, user, concurrence_matrix, all_songs, user_songs):
        print("Non zero values in cooccurence_matrix :%d" % np.count_nonzero(cooccurence_matrix))

        user_sim_scores = concurrence_matrix.sum(axis=0)/float(concurrence_matrix.shape[0])
        user_sim_scores = np.array(user_sim_scores)[0].tolist()

        sort_index = sorted(((e,i) for i,e in enumerate(list(user_sim_scores))), reverse=True)

        columns = ['user_id', 'song', 'rank']
        df = pandas.DataFrame(columns=columns) #data frame using pandas

        #fill the dataframe with top 10 recommendations

        rank = 1
        for i in range(0, len(sort_index)):
            if ~np.isnan(sort_index[i][0]) and all_songs[sort_index[i][1]] not in user_songs and rank <= 10:
                df.loc[len(df)] = [user, all_songs[sort_index[i][1]], sort_index[i][0], rank]
                rank = rank + 1

        #when there are no recommendations
        if df.shape[0] == 0:
            print("Current user has no training data")
            return -1
        else:
            return df

    #collaborative model
    def create(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id

    def recommend(self, user):
        user_songs = self.get_user_items(user) #unique songs for the user
        print("No. of unique songs for the user: %d" % len(user_songs))

        all_songs = self.get_all_items_train_data()
        print("no. of unique songs in the training set: %d" % len(all_songs))

        concurrence_matrix = self.make_concurrence_matrix(user_songs, all_songs)

        df_recommendatons = self.top_recommendations(user, concurrence_matrix, all_songs, user_songs)

        return df_recommendatons

    def get_similar_items(self, item_list):
        user_songs = item_list

        all_songs = self.get_all_items_train_data()

        print("no. of unique songs in the training set: %d" % len(all_songs))

        cooccurence_matrix = self.construct_cooccurence_matrix(user_songs, all_songs)
        
        user = ""
        df_recommendations = self.generate_top_recommendations(user, cooccurence_matrix, all_songs, user_songs)

        return df_recommendations
