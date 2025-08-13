import os
from typing import List

import aiohttp
from pymongo import MongoClient

import core_client
from core_client.api.activities import get_core_activity_by_sport_section_id, get_core_activity_by_id, \
    post_core_activity_id_enroll
from lkshmatch.adapters.base import (
    SportSectionName,
    TeamId,
    ActivityAdapter,
    UnknownError,
    Activity, Team, TgID, CoreID

)
from lkshmatch.admin.admin_privilege import PrivilegeChecker
from lkshmatch.domain.repositories.admin_repository import AdminRepository
from lkshmatch.config import settings
from lkshmatch.repositories.mongo.students import MongoLKSHStudentsRepository


class CoreActivityAdapter(ActivityAdapter):
    def __init__(self):
        # TODO DI
        core_client_url = f"{settings.get('CORE_HOST')}:{settings.get('CORE_PORT')}"
        self.client = core_client.Client(base_url=core_client_url)

    async def get_activities_by_sport_section(self, sport_section_id: int) -> List[Activity]:
        response = await get_core_activity_by_sport_section_id.asyncio(
            client=self.client,
            id=sport_section_id.id
        )
        if response is None:
            raise UnknownError("get all activity return null response")
        activity_result = []
        for activity in response:
            activity_result.append(activity)
        return activity_result

    async def get_activity_by_id(self, sport_section_id: int) -> List[Team]:
        response = await get_core_activity_by_id.asyncio(
            client=self.client,
            id=sport_section_id.id
        )
        if response is None:
            raise UnknownError("this section return null response")
        activity_result = []
        for activity in response:
            activity_result.append(activity)
        return activity_result



    async def make_team_in_activity(self, core_id: CoreID) -> Team:
        response = await post_core_activity_id_enroll.asyncio(
            client=self.client,
            id=core_id.id
        )
        if response is None:
            raise UnknownError("this team return null response")

        return response
