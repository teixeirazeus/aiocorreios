from typing import List
from .url_util import UrlUtil
from .models.zipcodes import Zipcodes
from .models.package import Package
import aiohttp
import xmltodict
from decimal import Decimal


class Correios:
    FRETE_URL = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.aspx'

    def __init__(self, username: str, password: str, session=None):
        """
        Correios client.
        """
        self.session = session or aiohttp.ClientSession()
        self.username = username
        self.password = password

    async def close(self):
        """
        Close the session.
        """
        await self.session.close()

    async def calculate_freight(self,
                                path: Zipcodes,
                                package: Package,
                                services: List[str],
                                value: float) -> dict:
        """
        Method to calculate the freight.
        """
        url = UrlUtil.get_url(self.FRETE_URL, {
            "nCdEmpresa": self.username,
            "sDsSenha": self.password,
            "sCepOrigem": path.origin,
            "sCepDestino": path.destiny,
            "nVlPeso": Decimal(package.weight),
            "nCdFormato": package.package_type,
            "nVlComprimento": Decimal(package.length),
            "nVlAltura": Decimal(package.heigth),
            "nVlLargura": Decimal(package.width),
            "sCdMaoPropria": 'n',
            "nVlValorDeclarado": value,
            "sCdAvisoRecebimento": 'n',
            "nCdServico": ','.join(services),
            "nVlDiametro": Decimal(package.diameter),
            "StrRetorno": 'xml',
            "nIndicaCalculo": 3
        })

        response = await self.session.get(url)
        if response.status != 200:
            raise Exception(f'Error: {response.status}')

        body = await response.text()
        frete_json = xmltodict.parse(body)

        return frete_json
