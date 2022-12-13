from .. models import Livre, Auteur, Genre,Note,Profil,Langue
from django.contrib.auth.models import User
import math
#vecteur user:livre,note
def get_ratings_vector(user):
    ratings = Note.objects.filter(user_id=user, note__gt=0).values('livre_id', 'note')
    res = {}
    for r in ratings:
        res[r['livre_id']] = r['note']
    return res



def cosinus(user1_ratings, user2_ratings):
    result = 0.0
    l1 = list(user1_ratings.keys())
    l2 = list(user2_ratings.keys())
#trouver les items en commun
    common_items = list(set(l1).intersection(l2))
    if len(common_items) == 0:
        return 0

    top_result = 0.0
    bottom_left_result = 0.0
    bottom_right_result = 0.0
#parcourir les itmes
    for item in common_items:
        rxs = user1_ratings[item]
        rys = user2_ratings[item]
# calcul numérateur note-user1 * note_user2
        top_result += (rxs) * (rys)
#dénominateur
        bottom_left_result += pow(rxs, 2)
        bottom_right_result += pow(rys, 2)
    bottom_left_result = math.sqrt(bottom_left_result)
    bottom_right_result = math.sqrt(bottom_right_result)
#numérateur/ dénominateur
    result = top_result / (bottom_left_result * bottom_right_result)
    return result

def pearson_correlation(user1, user2):
    result = 0.0
    rx_avg = user_average_rating(user1)
    ry_avg = user_average_rating(user2)

    l1= list(user1.keys())
    l2=list(user2.keys())
    common_items =list(set(l1).intersection(l2))

    top_result = 0.0
    bottom_left_result = 0.0
    bottom_right_result = 0.0
    for item in common_items:
        rxs = user1[item]
        rys = user2[item]
        top_result += (rxs - rx_avg) * (rys - ry_avg)
        bottom_left_result += pow((rxs - rx_avg), 2)
        bottom_right_result += pow((rys - ry_avg), 2)
    bottom_left_result = math.sqrt(bottom_left_result)
    bottom_right_result = math.sqrt(bottom_right_result)
    bottom= (bottom_left_result * bottom_right_result)
    if bottom==0:
        return 0
    result = top_result / bottom
    return result




#calculer la moyenne des note d'un utilisateur

def user_average_rating(user_data):
    avg_rating = 0.0
    size = len(user_data)
    for rating in user_data.values():
        avg_rating += float(rating)
    avg_rating /= size * 1.0
    return avg_rating


#calcule de la prediction
def predict(item,knn ,rating_user_context):
    users_corr=list(knn.keys())
#selectionner les utilisateurs valide
    valid_users = check_neighbors_validattion(item, users_corr)
    if not len(valid_users):
        return 0.0

    top_result = 0.0
    bottom_result = 0.0
    avg_rating_user=user_average_rating(rating_user_context)
#parcourire les utilisateurs valide
    for u in valid_users:
#vecteur de notes de l'utilisateur actif
        rating_user = get_ratings_vector(u)
#similarite avec utilisateur ui
        u_similarity = knn[u]
        rating = rating_user[item.id]
        avg_u =user_average_rating(rating_user)
#calculer le numérateur
        top_result += u_similarity * (rating-avg_u )
#calculer le  dénominateur
        bottom_result += u_similarity
        if bottom_result == 0 :
            return 0
    result = avg_rating_user+(top_result/bottom_result)
    return result
#fonction qui selectionne les utilisateur valide
def check_neighbors_validattion(item,users_corr):
    result = []
    for user in users_corr:
        ratings = get_ratings_vector(user)
        if item.id in ratings.keys() :
            result.append(user)
    return result


def get_predict_list(user):
    products = Livre.objects.all()
    users = User.objects.all().exclude(id=user.id)
    v1 = get_ratings_vector(user.id)
    if not v1 :
        return []
    products_no_marks = []
    for p in products:
        if p.id in v1.keys():
            continue
        products_no_marks.append(p)

    users_corr = []
    similarity_to_user = {}

    for u in users:
        v2 = get_ratings_vector(u.id)
#calculer la simelarite
        similarity = cosinus(v1, v2)
        if similarity > 0 :
            similarity_to_user[u.id] = similarity
            #users_corr.append(u)
#tri de la liste des similarite
    knn=sorted(similarity_to_user.items(), key=lambda t: t[1] , reverse=True)[:20]
    knn=dict(knn)

    predict_list = {}
    list=[]
#parcourire les items non note
    for item in products_no_marks:
#calculer la prediction pou item i
        predict_item = predict(item,knn,v1)
        if predict_item > 3:
            predict_list[item.id] = predict_item
#tri de la liste de prediction
    p=sorted(predict_list.items(), key=lambda t: t[1] , reverse=True)[:20]
    for i in p:
        list.append(i[0])

    return list


#fonction recommandation demographique
def get_demogrephic_list(user):
    profil =Profil.objects.get(user=user)
	
    livres =Livre.objects.all()
    livres_corr={}
    products_no_marks=[]
    v1=get_ratings_vector(user.id)
#selectionner les livre 
    for p in livres:
        if p.id in v1.keys():
            continue
        products_no_marks.append(p)
    langue = profil.langues.all().values()
    for livre in products_no_marks:
        corr=0
#comparaison profil utilisateur et profil des items
        for l in langue:
            if livre.langue in l.values():
                corr=corr+1
        if livre.limite_age is not None:
            if profil.age >livre.limite_age:
                corr = corr + 1
        if profil.specialite is not None and livre.public_cible is not None :
            if profil.specialite == livre.public_cible:
                corr = corr + 1
        for genre in livre.genres.all() :
            if genre is not None :
                if genre in profil.genre.all():
                    corr = corr + 1

        if corr >=1:
            livres_corr[livre.id]=corr
    sorted_list = dict(sorted(livres_corr.items(), key=lambda t: t[1], reverse=True)[:20])

    return sorted_list



