from dataclasses import dataclass, asdict
import json

@dataclass
class Serie:
    id: int
    nome: str
    ordem: int
    ano_estreia: int
    ano_encerramento: int
    episodios: int
    classificacao_indicativa: int
    nota_imdb: float
    link: str
    popularidade: float
    atores: list

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)
