import pandas as pd

models = ("Course Similarity", "User Profile", "Clustering", "Clustering with PCA", "KNN", "NMF", "Neural Network", "Regression with Embedding Features", "Classification with Embedding Features")

data_path = "data/"

def load_ratings():
    return pd.read_csv(data_path + "ratings.csv")

def load_course_sims():
    return pd.read_csv(data_path + "sim.csv")

def load_courses():
    df = pd.read_csv(data_path + "course_processed.csv")
    df['TITLE'] = df['TITLE'].str.title()
    return df

def load_bow():
    return pd.read_csv(data_path + "courses_bows.csv")

def add_new_ratings(new_courses):
    res_dict = {}
    if len(new_courses) > 0:
        ratings_df = load_ratings()
        new_id = ratings_df['user'].max() + 1
        users = [new_id] * len(new_courses)
        ratings = [3.0] * len(new_courses)
        res_dict['user'] = users
        res_dict['item'] = new_courses
        res_dict['rating'] = ratings
        new_df = pd.DataFrame(res_dict)
        updated_ratings = pd.concat([ratings_df, new_df])
        updated_ratings.to_csv(data_path + "ratings.csv", index=False)
        return new_id

def get_doc_dicts():
    bow_df = load_bow()
    grouped_df = bow_df.groupby(['doc_index', 'doc_id']).max().reset_index(drop=False)
    idx_id_dict = grouped_df[['doc_id']].to_dict()['doc_id']
    id_idx_dict = {v: k for k, v in idx_id_dict.items()}
    del grouped_df
    return idx_id_dict, id_idx_dict

def course_similarity_recommendations(idx_id_dict, id_idx_dict, enrolled_course_ids, sim_matrix):
    all_courses = set(idx_id_dict.values())
    unselected_course_ids = all_courses.difference(enrolled_course_ids)
    res = {}
    for enrolled_course in enrolled_course_ids:
        for unselect_course in unselected_course_ids:
            if enrolled_course in id_idx_dict and unselect_course in id_idx_dict:
                idx1 = id_idx_dict[enrolled_course]
                idx2 = id_idx_dict[unselect_course]
                sim = sim_matrix[idx1][idx2]
                if unselect_course not in res:
                    res[unselect_course] = sim
                else:
                    if sim >= res[unselect_course]:
                        res[unselect_course] = sim
    res = {k: v for k, v in sorted(res.items(), key=lambda item: item[1], reverse=True)}
    return res

def train(model_name):
    pass

def predict(model_name, user_ids, params):
    sim_threshold = params.get("sim_threshold", 60) / 100.0
    idx_id_dict, id_idx_dict = get_doc_dicts()
    sim_matrix = load_course_sims().to_numpy()
    users, courses, scores = [], [], []
    for user_id in user_ids:
        if model_name == models[0]:
            ratings_df = load_ratings()
            user_enrolled_courses = ratings_df[ratings_df['user'] == user_id]['item'].values.tolist()
            results = course_similarity_recommendations(idx_id_dict, id_idx_dict, user_enrolled_courses, sim_matrix)
            top_results = {k: v for k, v in results.items() if v >= sim_threshold}
            if len(top_results) > 0:
                for k, v in top_results.items():
                    users.append(user_id)
                    courses.append(k)
                    scores.append(v)
    res_dict = {
        'USER_ID': users,
        'COURSE_ID': courses,
        'SCORE': scores
    }
    res_df = pd.DataFrame(res_dict)
    return res_df
