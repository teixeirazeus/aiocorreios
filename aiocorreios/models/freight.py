from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Freight:
    codigo: str
    valor: Decimal
    prazo_entrega: int
    valor_sem_adicionais: Decimal
    valor_mao_propria: Decimal
    valor_aviso_recebimento: Decimal
    valor_valor_declarado: Decimal
    entrega_domiciliar: bool
    entrega_sabado: bool
