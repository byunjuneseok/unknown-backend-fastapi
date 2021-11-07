from uuid import UUID
from datetime import datetime, timedelta, timezone

from fastapi.params import Depends
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from app.celery.worker import task_collaborative_filtering, task_content_based_filtering
from app.core import const
from app.dependencies.database import get_database
from app.dependencies.permission import get_current_user
from app.models.cache import CollaborativeFilteringCache, ContentBasedFilteringCache
from app.models.user import User
from app.models.visit_log import VisitLog
from app.schemas.curation import CurationResponseSchema


router = APIRouter(prefix='/curation')


@router.post(path='/cf/')
async def collaborative_filtering(current_user: User = Depends(get_current_user), database: Session = Depends(get_database)):
    
    try:
        cached_item = CollaborativeFilteringCache.get(current_user.id)
    except CollaborativeFilteringCache.DoesNotExist:
        cache = CollaborativeFilteringCache(hash_key=current_user.id)
        cache.save()
        task_collaborative_filtering.delay(current_user.id)
        return CurationResponseSchema(status=const.CURATION_INFO_202_WORK_IN_PROGRESS)

    if cached_item.value is None:
        return CurationResponseSchema(status=const.CURATION_INFO_202_WORK_IN_PROGRESS)

    if datetime.now(timezone.utc) - cached_item.cached_time > timedelta(hours=6):
        cache = CollaborativeFilteringCache(hash_key=current_user.id)
        cache.save()
        task_collaborative_filtering.delay(current_user.id)
        return CurationResponseSchema(status=const.CURATION_INFO_202_WORK_IN_PROGRESS)

    return CurationResponseSchema(status=const.CURATION_INFO_200_JOB_IS_DONE, result=cached_item.value)

@router.post(path='/cbf/')
async def content_based_filtering(store_id: UUID, current_user: User = Depends(get_current_user), database: Session = Depends(get_database)):
    store_id = str(store_id)
    try:
        cached_item = ContentBasedFilteringCache.get(hash_key=store_id)
    except ContentBasedFilteringCache.DoesNotExist:
        cache = ContentBasedFilteringCache(hash_key=store_id)
        cache.save()
        task_content_based_filtering.delay(store_id)
        return CurationResponseSchema(status=const.CURATION_INFO_202_WORK_IN_PROGRESS)

    if cached_item.value is None:
        return CurationResponseSchema(status=const.CURATION_INFO_202_WORK_IN_PROGRESS)

    if datetime.now(timezone.utc) - cached_item.cached_time > timedelta(hours=6):
        cache = CollaborativeFilteringCache(hash_key=store_id)
        cache.save()
        task_content_based_filtering.delay(store_id)
        return CurationResponseSchema(status=const.CURATION_INFO_202_WORK_IN_PROGRESS)

    return CurationResponseSchema(status=const.CURATION_INFO_200_JOB_IS_DONE, result=cached_item.value)
