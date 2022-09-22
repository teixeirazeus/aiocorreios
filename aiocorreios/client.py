from typing import List
from .data_util import DataUtil
from .models.freight import Freight
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
        freight_data = self._get_freigth_data(body)
        freight = self._create_freigth(freight_data)

        return freight

    def _get_freigth_data(self, body: str) -> dict:
        """
        Parse the xml response.
        """
        result_dict = xmltodict.parse(body)
        return result_dict['Servicos']['cServico']

    def _create_freigth(self, freight_data: dict) -> Freight:
        """
        Create a Freight object.
        """
        return Freight(
            codigo=freight_data['Codigo'],
            valor=DataUtil.to_decimal(freight_data['Valor']),
            prazo_entrega=freight_data['PrazoEntrega'],
            valor_sem_adicionais=DataUtil.to_decimal(
                freight_data['ValorSemAdicionais']),
            valor_mao_propria=DataUtil.to_decimal(
                freight_data['ValorMaoPropria']),
            valor_aviso_recebimento=DataUtil.to_decimal(
                freight_data['ValorAvisoRecebimento']),
            valor_valor_declarado=DataUtil.to_decimal(
                freight_data['ValorValorDeclarado']),
            entrega_domiciliar=freight_data['EntregaDomiciliar'] == "S",
            entrega_sabado=freight_data['EntregaSabado'] == "S",
        )
