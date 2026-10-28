#import "@preview/grape-suite:4.0.0": exercise
#import exercise: project, task, subtask, solution, hint

#show: project.with(
    title: "Perceptron: Registro de Execução e Respostas",

    university: [UFAL],
    institute: [Campus Arapiraca],
    seminar: [Ciência da Computação -  Redes Neurais],

    author: "Lucas Ramos de Oliveira",

    show-solutions: true,

    task-type: [Tarefa],
    box-task-title: [Tarefa],
    box-solution-title: [Solução],
    solution-type: [Respostas],
    solutions-title: [Respostas],
)

#task(
    rubric: ((1, lorem(20)), (3, lorem(23))),
    [Registro de execução.],
    none,
    [
      #subtask()[
        Parâmetros finais:
        - Peso temperatura: $~ 0,55$
        - Peso umidade: $~ 0,265$
        - Viés: $-0.6$
      ]

      #subtask()[
        Número de épocas: $71$
      ]

      #subtask()[
        Métricas no conjunto de teste:
          - Acurácia: $100.00%$ (8/8)
          - Precisão: $100.00%$
          - Sensibilidade: $100.00%$
          - F1-Score: $100.00%$
      ]
    ],
)

#task(
    rubric: ((1, lorem(20)), (3, lorem(23))),
    [Respostas curtas.],
    none,
    [
        #subtask()[
            Para que serve o viés?
        ]

        #subtask()[
            Por que normalizar as entradas?
        ]

        #subtask()[
            O que um Perceptron simples não consegue classificar?
        ]

        #solution[

          #subtask()[
              O viés desloca a fronteira de decisão, permitindo que ela não precise passar pela origem. Ele atua como um limiar de ativação ajustável, sem ele, a reta $w_1 x_1 + w_2 x_2 = 0$ seria forçada a cruzar $(0, 0)$, o que limita os padrões que o modelo consegue separar.
          ]

          #subtask()[
              Para que as variáveis fiquem na mesma escala (nesse caso, a temperatura fica entre 0 e 40 e a umidade entre 0 e 100). Sem isso, a variável de maior magnitude tem muito mais impacto no cálculo e nas atualizações dos pesos.
          ]

          #subtask()[
              Problemas que não são linearmente separáveis, ou seja, problemas os quais nenhuma reta (ou hiperplano) separa as classes, como a função XOR. Para esses casos são necessárias redes com camadas ocultas.
          ]
        ]
    ],
)