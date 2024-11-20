import asyncio

from . import bp


@bp.route("")
async def temp():
    await asyncio.sleep(5)
    return "sex", 200
