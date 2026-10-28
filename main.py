from lib import (
    Parametros,
    atualizacao,
    carregar_entradas,
    interface,
    normal,
    previsao,
    teste,
    treinamento,
)


def main() -> None:
    entradas = carregar_entradas('treinamento.csv')
    entradas_normalizadas = [normal(entrada) for entrada in entradas]
    parametros_iniciais = Parametros(0, 0, 0)
    parametros_treinados = treinamento(
        entradas_normalizadas,
        parametros_iniciais,
        taxa_aprendizado=0.1,
        epocas=100,
        previsao=previsao,
        atualizacao=atualizacao,
    )

    entradas_teste = carregar_entradas('teste.csv')
    entradas_teste_normalizadas = [normal(entrada) for entrada in entradas_teste]
    teste(entradas_teste_normalizadas, parametros_treinados, previsao=previsao)

    interface(parametros_treinados, previsao, normal)


if __name__ == "__main__":
    main()
