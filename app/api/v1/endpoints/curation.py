from uuid import UUID

import numpy as np
import pandas as pd
from fastapi.params import Depends
from fastapi.routing import APIRouter
from scipy.sparse.linalg import svds
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session

from app.dependencies.database import get_database
from app.dependencies.permission import get_current_user
from app.models.store import Store, StoreStoreCategoryMap
from app.models.user import User
from app.models.visit_log import VisitLog

router = APIRouter(prefix='/curation')


@router.post(path='/cf/')
def collaborative_filtering(current_user: User = Depends(get_current_user), database: Session = Depends(get_database)):
    user_id = current_user.id
    
    stores = database.query(Store).all()
    visit_logs = database.query(VisitLog).all()

    store_list = list()
    for i in range(len(stores)):
        store_list.append([stores[i].id, stores[i].rating])

    visit_log_list = []
    for i in range(len(visit_logs)):
        visit_log_list.append([visit_logs[i].user_id, visit_logs[i].store_id, visit_logs[i].rating])

    df_ratings = pd.DataFrame(visit_log_list, columns=['userId', 'storeId', 'rating'])
    df_stores = pd.DataFrame(store_list, columns=['storeId', 'rating'])

    df_ratings.drop_duplicates(['userId', 'storeId'], inplace=True, keep='first')

    df_user_store_ratings = df_ratings.pivot(index='userId', columns='storeId', values='rating').fillna(0)
    user_store_ratings = np.array(df_user_store_ratings)
    user_ratings_mean = np.mean(user_store_ratings, axis=1)
    matrix_user_mean = user_store_ratings - user_ratings_mean.reshape(-1,1)

    u, sigma, vt = svds(matrix_user_mean, k=12)

    sigma = np.diag(sigma)
    svd_user_predicted_ratings = np.dot(np.dot(u, sigma), vt) + user_ratings_mean.reshape(-1,1)

    df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns=df_user_store_ratings.columns)

    user_row_number = user_id -1

    sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(ascending=False)

    user_data = df_ratings[df_ratings.userId == user_id]
    user_data = user_data.drop(columns=['rating'])
    user_history = user_data.merge(df_stores, on='storeId')
    user_history = user_history.sort_values(by='rating', ascending=False)
    recommendations = df_stores[~df_stores['storeId'].isin(user_history['storeId'])]
    recommendations = recommendations.merge(pd.DataFrame(sorted_user_predictions).reset_index(), on='storeId')
    recommendations = recommendations.rename(columns={user_row_number: 'Predictions'}).sort_values('Predictions', ascending=False).iloc[:9, :]

    recommendations = recommendations['storeId']
    recommendations = list(recommendations)

    similar_stores = list()
    for ss in recommendations:
        store = database.query(Store).filter(Store.id == ss).first()
        similar_stores.append(store)

    return {
        'result': {
            'user_id': user_id,
            'algorithm': 'cf',
            'recommendations': similar_stores,
        }
    }
    


@router.post(path='/cbf/')
async def content_based_filtering(store_id: UUID, current_user: User = Depends(get_current_user), database: Session = Depends(get_database)):
    store_id = str(store_id)
    all_category_maps = database.query(StoreStoreCategoryMap).order_by(StoreStoreCategoryMap.store_id).all()

    data = list()

    for mm in all_category_maps:
        if len(data) == 0:
            data.append({
                'store_id': mm.store_id,
                'store_category_ids': [str(mm.store_category_id)]
            })
        cur = data[-1]
        if cur.get('store_id') == mm.store_id:
            cur['store_category_ids'].append(str(mm.store_category_id))
        else:
            data.append({
                'store_id': mm.store_id,
                'store_category_ids': [str(mm.store_category_id)]
            })

    for idx, dd in enumerate(data):
        data[idx] = {
            'store_id': dd['store_id'],
            'store_category_ids': ' '.join(dd['store_category_ids'])
        }

    data = pd.DataFrame(data, columns=['store_id', 'store_category_ids'])
    count_vector = CountVectorizer(ngram_range=(1, 3))
    count_vector_categories = count_vector.fit_transform(data['store_category_ids'])
    category_cosine_similarity = cosine_similarity(count_vector_categories, count_vector_categories).argsort()[:, ::-1]
    target_store_index = data[data['store_id'] == store_id].index.values

    similar_indexes = category_cosine_similarity[target_store_index, :9].reshape(-1)
    similar_indexes = similar_indexes[similar_indexes != target_store_index]

    similar_stores_indexes = list()
    for ss in similar_indexes:
        similar_stores_indexes.append(int(ss))

    similar_stores = list()
    for ss in similar_stores_indexes:
        dd = data.iloc[ss]
        store = database.query(Store).filter(Store.id == dd['store_id']).first()
        dd['details'] = store
        similar_stores.append(dd)

    return {
        'result': {
            'requested_store':  database.query(Store).filter(Store.id == store_id).first(),
            'algorithm': 'cb',
            'recommendations': similar_stores
        }
    }

