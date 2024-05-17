# -*- coding: utf-8 -*-

from api.FundingRateAPIManager import FundingRateAPIManager
from api.OHLCVAPIManager import OHLCVAPIManager
from api.CommitmentsOfTradersManager import CommitmentOfTradersManager
from api.bybitFunding import ByBit
from api.phemexFunding import Phemex
from logging import getLogger

def update_db():
    logger = getLogger(__name__)
    try:
        OHLCVAPIManager().update_db()
        # ByBit().update_db()
        Phemex().update_db()
        FundingRateAPIManager().update_db()
        # FundingRateAPIManager().update_db_mexc()
        FundingRateAPIManager().export_funding_summary()
        CommitmentOfTradersManager().update_db_all()
    except Exception as e:
        logger.error(e.args)
    
if __name__ == '__main__':
    update_db()