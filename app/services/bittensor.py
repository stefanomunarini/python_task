import asyncio
import logging

from async_substrate_interface import AsyncSubstrateInterface
from bittensor.core.chain_data.utils import decode_account_id
from bittensor_wallet.utils import SS58_FORMAT
from typing_extensions import Optional

logger = logging.getLogger(__name__)


async def fish(
        netuid: Optional[int] = None,
        account: Optional[str] = None
):
    async def exhaust(qmr):
        r = []
        async for k, v in await qmr:
            r.append((k, v))
        return r

    async with AsyncSubstrateInterface(
            "wss://entrypoint-finney.opentensor.ai:443",
            ss58_format=SS58_FORMAT
    ) as substrate:
        block_hash = await substrate.get_chain_head()

        if not account and not netuid:
            tasks = [
                substrate.query_map(
                    "SubtensorModule",
                    "TaoDividendsPerSubnet",
                    [net_uid],
                    block_hash=block_hash
                ) for
                net_uid in range(1, 51)
            ]
            tasks = [exhaust(task) for task in tasks]
            results_dicts_list = []
            for future in asyncio.as_completed(tasks):
                result = await future
                results_dicts_list.extend(
                    [(decode_account_id(k), v.value) for k, v in result])

            return results_dicts_list, block_hash

        if account:
            result = await substrate.query(
                module='SubtensorModule',
                storage_function='TaoDividendsPerSubnet',
                params=[netuid, account],
                block_hash=block_hash
            )
            results = [result.value] if result else []
        else:
            task = await substrate.query_map(
                "SubtensorModule",
                "TaoDividendsPerSubnet",
                [netuid],
                block_hash=block_hash
            )
            result = await exhaust(task)
            results = [v.value for _, v in result]

    return results, block_hash
