import asyncio
from aiocorreios.client import Correios
from aiocorreios.models.zipcodes import Zipcodes
from aiocorreios.models.package import Package
from aiocorreios.models.correio_services import Services


async def main():
    correios = Correios('09146920', '123456')
    zipcodes = Zipcodes('70002900', '84015780')
    package = Package(
        width=30.0, heigth=30.0, length=30.0, diameter=0, weight=1)
    value = 50
    result = await correios.calculate_freight(zipcodes, package, [Services.SERVICE_SEDEX], value)

    print(result)
    await correios.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
