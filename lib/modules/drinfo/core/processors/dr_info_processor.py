from datetime import datetime

from lib.models.session_dto import SessionDto
from lib.modules.drinfo.core.enricher.dr_info_enricher import DrInfoEnricher

'''
process, clean, transform futures price data to be ready for analysis and iteration
Enrich futures price data with dr info
'''


class DrInfoProcessor:
    def __init__(self):
        self.sorted_sessions = None
        self._dr_info_enricher = DrInfoEnricher()

    def process(self, sessions_group: dict[datetime, SessionDto]) -> dict[datetime, SessionDto]:
        sessions_data = self._dr_info_enricher.enrich_group(sessions_group)
        self.sorted_sessions = sorted(sessions_data.keys())
        return sessions_data
