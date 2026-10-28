import csv
from collections.abc import Callable


class Entrada:
    def __init__(self, id: int, temp: float, umid: float, classe: bool):
        self.id = id
        self.temp = temp
        self.umid = umid
        self.classe = classe


class Parametros:
    def __init__(self, peso_temp: float, peso_umid: float, vies: float):
        self.peso_temp = peso_temp
        self.peso_umid = peso_umid
        self.vies = vies


def carregar_entradas(*caminhos: str) -> list[Entrada]:
    entradas: list[Entrada] = []
    lista_caminhos = []
    for item in caminhos:
        if isinstance(item, (list, tuple)):
            lista_caminhos.extend(item)
        else:
            lista_caminhos.append(item)

    for caminho in lista_caminhos:
        with open(caminho, mode='r', encoding='utf-8') as f:
            leitor = csv.DictReader(f, skipinitialspace=True)
            for linha in leitor:
                entradas.append(
                    Entrada(
                        id=int(linha['id']),
                        temp=float(linha['temp']),
                        umid=float(linha['umid']),
                        classe=bool(int(linha['classe']))
                    )
                )
    return entradas


def normal(entrada: Entrada) -> Entrada:
    temperatura_normalizada = entrada.temp / 40
    umidade_normalizada = entrada.umid / 100
    return Entrada(entrada.id, temperatura_normalizada, umidade_normalizada, entrada.classe)


def previsao(entrada: Entrada, parametros: Parametros) -> bool:
    return (parametros.peso_temp * entrada.temp) + (parametros.peso_umid * entrada.umid) + parametros.vies >= 0


def atualizacao(saida_esperada: bool, saida_obtida: bool, parametros: Parametros, taxa_aprendizado: float, entrada: Entrada) -> Parametros:
    erro = int(saida_esperada) - int(saida_obtida)
    novo_peso_temp = parametros.peso_temp + (taxa_aprendizado * erro * entrada.temp)
    novo_peso_umid = parametros.peso_umid + (taxa_aprendizado * erro * entrada.umid)
    novo_vies = parametros.vies + (taxa_aprendizado * erro)
    return Parametros(novo_peso_temp, novo_peso_umid, novo_vies)


def treinamento(entradas: list[Entrada], parametros: Parametros, taxa_aprendizado: float, epocas: int, previsao: Callable, atualizacao: Callable) -> Parametros:
    epocas_executadas = 0
    erros_ultima_epoca = 0

    for epoca in range(1, epocas + 1):
        epocas_executadas = epoca
        erros_ultima_epoca = 0
        for entrada in entradas:
            saida_obtida = previsao(entrada, parametros)
            if saida_obtida != entrada.classe:
                erros_ultima_epoca += 1
            parametros = atualizacao(entrada.classe, saida_obtida, parametros, taxa_aprendizado, entrada)

        if erros_ultima_epoca == 0:
            break

    print(f"Épocas executadas: {epocas_executadas}")
    print(f"Erros da última época: {erros_ultima_epoca}")
    print(f"Valores finais dos parâmetros: Peso Temp: {parametros.peso_temp}, Peso Umid: {parametros.peso_umid}, Viés: {parametros.vies}")

    return parametros


def teste(entradas: list[Entrada], parametros: Parametros, previsao: Callable) -> dict[str, float]:
    vp = 0  # (classe=1, prev=1)
    vn = 0  # (classe=0, prev=0)
    fp = 0  # (classe=0, prev=1)
    fn = 0  # (classe=1, prev=0)

    for entrada in entradas:
        saida_obtida = previsao(entrada, parametros)
        if entrada.classe and saida_obtida:
            vp += 1
        elif not entrada.classe and not saida_obtida:
            vn += 1
        elif not entrada.classe and saida_obtida:
            fp += 1
        else:
            fn += 1

    total = len(entradas)
    acuracia = (vp + vn) / total if total > 0 else 0.0
    precisao_val = vp / (vp + fp) if (vp + fp) > 0 else 0.0
    sensibilidade = vp / (vp + fn) if (vp + fn) > 0 else 0.0
    f1_score = (
        2 * (precisao_val * sensibilidade) / (precisao_val + sensibilidade)
        if (precisao_val + sensibilidade) > 0
        else 0.0
    )

    print("Métricas no conjunto de teste:")
    print(f"  Acurácia: {acuracia * 100:.2f}% ({vp + vn}/{total})")
    print(f"  Precisão: {precisao_val * 100:.2f}%")
    print(f"  Sensibilidade (Recall): {sensibilidade * 100:.2f}%")
    print(f"  F1-Score: {f1_score * 100:.2f}%\n")

    return {
        "acuracia": acuracia,
        "precisao": precisao_val,
        "sensibilidade": sensibilidade,
        "f1_score": f1_score,
    }


def interface(parametros: Parametros, previsao: Callable, normal: Callable) -> None:
    temp = float(input("Digite a temperatura (°C): "))
    umid = float(input("Digite a umidade relativa (%): "))
    entrada = normal(Entrada(id=0, temp=temp, umid=umid, classe=False))
    resultado = "ALERTA (1)" if previsao(entrada, parametros) else "NORMAL (0)"
    print(f"Classificação prevista: {resultado}")

