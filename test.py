import csv,sys,os
project_dir='./PFE'
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import django
django.setup()



import math
from Livres.models import Livre,Auteur,BX_Books,BX_Users,BX_Book_Ratings
#from Livres.recommander.recommander2 import



def cosinus(user1_ratings, user2_ratings):
    result = 0.0

    l1 = list(user1_ratings.keys())
    l2 = list(user2_ratings.keys())
    common_items = list(set(l1).intersection(l2))
    print ('\n\n\n com',common_items)
    if len(common_items) == 0:
        return 0

    top_result = 0.0
    bottom_left_result = 0.0
    bottom_right_result = 0.0
    for item in common_items:
        rxs = user1_ratings[item]
        rys = user2_ratings[item]
        top_result += (rxs) * (rys)
        bottom_left_result += pow(rxs, 2)
        bottom_right_result += pow(rys, 2)
    bottom_left_result = math.sqrt(bottom_left_result)
    bottom_right_result = math.sqrt(bottom_right_result)
    bottom=(bottom_left_result * bottom_right_result)
    if bottom == 0:
        return 0
    result = top_result / bottom

    return result


def user_average_rating(user_data):
    avg_rating = 0.0
    size = len(user_data)
    for rating in user_data.values():
        avg_rating += float(rating)
    avg_rating /= size * 1.0
    return avg_rating



def get_ratings_vector(user):
    ratings = BX_Book_Ratings.objects.filter(User_ID=user).values('ISBN', 'Book_Rating')
    res = {}
    for r in ratings:
        res[r['ISBN']] = r['Book_Rating']
    return res

def check_neighbors_validattion(item,users_corr):
    result = []
    for user in users_corr:
        ratings = get_ratings_vector(user)
        if item in ratings.keys() :
            result.append(user)

    return result

"""
def get_ratings_test_vector(user):
    ratings = BX_Book_Ratings.objects.filter(User_ID=user, Book_Rating__gt=0).values('ISBN_id', 'Book_Rating')
    res = {}
    for r in ratings:
        res[r['ISBN_id']] = r['Book_Rating']
    return res
"""

def predict(item,users_corr , similarity_to_user,rating_user_context):
    valid_users = check_neighbors_validattion(item, users_corr)
    if not len(valid_users):
        return 0.0

    top_result = 0.0
    bottom_result = 0.0
    avg_rating_user=user_average_rating(rating_user_context)

    for u in list(similarity_to_user.keys()):
        rating_user = get_ratings_vector(u)
        u_similarity = similarity_to_user[u]
        if item in rating_user.keys():
            rating = rating_user[item]
            avg_u =user_average_rating(rating_user)
            top_result += u_similarity * (rating-avg_u )
            bottom_result += u_similarity

    if bottom_result==0:
        return 0
    result = avg_rating_user+(top_result/bottom_result)
    return result

def get_predict(users,user,item,user_ratings):
    v1 = user_ratings
    users_corr = []
    similarity_to_user = {}
    for u in users:
        if u != user:
            v2 = get_ratings_vector(u)
            #print ('vector1\n',v1)
            #print ('vector1\n',v2)
            similarity = cosinus(v1, v2)

            similarity_to_user[u] = similarity
           # print ('simsim\n',similarity_to_user)
            users_corr.append(u)
    knn=sorted(similarity_to_user.items(), key=lambda t: t[1] , reverse=True)[:20]
    knn=dict(knn)

    predict_item = predict(item, users_corr, knn,v1)
    return predict_item


def validation():
    ratings = BX_Book_Ratings.objects.all().values('User_ID', 'ISBN', 'Book_Rating')
    res = {}
    for r in ratings:
        if r['User_ID'] not in res.keys():
            res[r['User_ID']] = []
        res[r['User_ID']].append([r['ISBN'], r['Book_Rating']])

    users=list(res.keys())
    test_users=users[:50]
    lite_pre=[]
    nb=0
    sum=0
    sq_sum=0
    for user in test_users:
        if len(res[user])>2:
            nb+=1
            test=res[user][0]
            v1=dict(res[user][1:])
            predict=get_predict(users,user,test[0],v1)
            print (predict,'->',test[1])
            lite_pre.append(predict)
            sum+=test[1]-predict
            sq_sum+=(test[1]-predict)**2

    mae=sum/nb
    rmse=math.sqrt(sq_sum/nb)
    print ('mae=',mae)
    print ('rmse=',rmse)
    return lite_pre


validation()