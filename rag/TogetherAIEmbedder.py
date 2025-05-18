import os
import sys
import numpy as np
from dotenv import load_dotenv
from together import Together
from pydantic import BaseModel, field_validator
from typing import List, Union
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from exceptions.EmbedderException import EmbedderException
from schemas.EmbedderConfig import EmbedderConfig
from Embedder import BaseEmbedder

load_dotenv()

CONFIG_EMBEDDER = EmbedderConfig(
    api_key = os.getenv('API_KEY_LLM', None),
    model = 'togethercomputer/m2-bert-80M-8k-retrieval'
)

class TogetherAIEmbedder(BaseEmbedder):
    def __init__(self, config: EmbedderConfig):
        self.config = config
        self.client = Together(
            api_key = self.config.api_key
        )

    def create_embeddings(self, inputs: Union[List[str], str]) -> List[List[float]]:
        """Create embeddings of the incoming texts

        Args:
            inputs (List[str]): text

        Returns:
            List[List[float]]: List of embeddings
        """
        if not inputs:
            raise ValueError(
                "Input texts cannot be empty"
            )
        try:
            if isinstance(inputs,str):
                inputs = [inputs]

            response = self.client.embeddings.create(
            model = self.config.model,
            input = inputs
            )
            embeddings = np.array([data_block.embedding for data_block in response.data])
            
            if embeddings is None:
                raise ValueError(
                    "Empty response from embedder"
                )
            return embeddings

        except Exception as error:
            raise EmbedderException(
                message=str(error)
            )
        
    def retrieve(self, query: str, top_k: int = 1, index: np.ndarray = None) -> List[int]:
        query_embeddings = self.create_embeddings(query)
        cosine_similarity_score = cosine_similarity(query_embeddings, index)
        return np.argsort(-cosine_similarity_score)[:top_k]


if __name__ == '__main__':
    data = [
        "Гиперспектральный анализ флуминантных структур в условиях квантовой резонансной дисперсии",
        "Аннотация:\nВ данной работе рассматривается влияние гиперфлюктуативного поля на стабилизацию флуминантных структур в псевдоквазисредах типа «лемноид-кластер». Применяется методология спектрально-латеральной экспансии с использованием тензора квантовой контрапозиции. Результаты экспериментов подтверждают существование устойчивых зон флоксации при резонансном параметре ζ > 4.73.",
        "1. Введение",
        "Исследование квантовых взаимодействий в области флуминантных коллапсаров остаётся актуальным направлением в псевдотеоретической динамике материи. Особенно интерес представляет феномен спонтанной декогерентной рефракции, впервые описанный в работах Зондермана и Траксиуса (2019), при котором фрактальные векторы вступают в автосинхронизированный резонанс с лемнискатной компонентой поля.",
        "2. Методология",
        "Для эмпирического анализа был применён гибридный подход, включающий спектроскопию в диапазоне α-фибрации и метод инвертированной тетрафазной сборки. Основным инструментом служила мультиосцилляторная платформа TYPHON-9, модифицированная для работы в условиях низкой пертурбации константы Бринеля (κ ≈ 0.0024).",
        "3. Результаты и обсуждение",
        "На рисунке 3 показано, что при экстраполяции параметра τ к псевдоасимптотическому пределу, наблюдается флоксовый сдвиг в пределах 0.2–0.3 наносаликов, что подтверждает теоретическую модель Штрауда-Лемна.",
        "Также были зафиксированы случаи гипервибрационной детонации в субстрате, особенно при введении дополнительного флусона на фазе ε-инверсии.",
        "4. Заключение",
        "Полученные данные подтверждают валидность гипотезы о существовании устойчивых флуминантных зон в условиях квантовой резонансной дисперсии. Это открывает перспективы для дальнейшего развития квазиреверсивной термофилософии и синтеза многомерных аксиом в рамках гипотетического супервакуума.",
        "Литература",
        "Траксиус И.Ю., Зондерман В.А. \"Фрактальные контуры в многогранной ауре\", Журнал гипотетической физики, 2019.",
        "Штрауд Г., Лемн К. \"О природе флуминантного перенаправления\", Proceedings of the 12th Lemnoid Congress, 2022."
    ]


    embedder = TogetherAIEmbedder(CONFIG_EMBEDDER)
    document_embeddings = embedder.create_embeddings(
        data
    )

    query = 'Для чего применяется Гиперспектральный анализ флуминантных структур?'

    array = embedder.retrieve(
        query=query,
        top_k=1,
        index=document_embeddings
    )

    response = embedder.client.chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=[
        {"role": "system", "content": "Ты ученый"},
        {"role": "user", "content": f"{query}. Здесь ищи информацию: {data}"},
        ],
    )

    print(response.choices[0].message.content)
     
    

