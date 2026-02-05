Trabalho 1 - Aprendizado Supervisionado

Alunos:

Ana Luíza Colombi Sanfelice (577504)

Lorenzo Cadó Nemitz (584809)

Natan Feijó Tristão (585193)

Regressão Linear

Parâmetros utilizados:

b = 0 e w = 1, apesar de não influenciarem no resultado.

alpha = 0.0117, num_iterations = 800.

Com 500 iterações já havia menos de 0,005% de diferença.

Métrica de desempenho:

Erro quadrático médio: 6,4778.

Conclusões:

Aumentar o número de iterações acima de 800 não melhora a precisão.

Alterar o valor de alpha (exceto variações muito pequenas) tende a aumentar o erro quadrático médio.

2) TensorFlow / Keras

Características dos datasets:

MNIST:

Classes: 10 (dígitos de 0 a 9)

Amostras: 70.000 (60.000 treino + 10.000 teste)

Dimensão: 28 × 28 × 1 (tons de cinza)

Fashion MNIST:

Classes: 10 (tipos de roupas, sapatos e acessórios)

Amostras: 70.000 (60.000 treino + 10.000 teste)

Dimensão: 28 × 28 × 1 (tons de cinza)

CIFAR-10:

Classes: 10 (avião, automóvel, pássaro, gato, etc.)

Amostras: 60.000 (50.000 treino + 10.000 teste)

Dimensão: 32 × 32 × 3 (RGB)

CIFAR-100:

Classes: 100 (objetos, animais, veículos, etc.)

Amostras: 60.000 (50.000 treino + 10.000 teste)

Dimensão: 32 × 32 × 3 (RGB)

2.1) Reflexões sobre cada dataset

MNIST: Foi mais simples e fácil, pois as imagens são bem limpas, apenas com o dígito em branco escrito sobre um fundo preto. Pensando que os números variam de 0 a 9, os padrões são limitados, facilitando a separação das classes diferentes. Além disso, a resolução é baixa (28x28) e só tons de cinza.

Fashion MNIST: Semelhante ao MNIST, tem mesmo tamanho e formato sendo 28x28 e apenas tons de cinza. Porém é mais difícil que o anterior, possui mais classes distintas, como camisetas, sandálias, e dentro da classe as roupas se confundem, como entre camiseta e blusa. Portanto, é necessário distinguir padrões mais sutis de textura e forma.

CIFAR-10: É mais difícil que os anteriores, pois possui mais classes diversas, imagens com cor e maior dimensão. Pensando na variedade de classes, é preciso reconhecer padrões mais complexos, percebendo sutilezas e considerando elementos externos no fundo.

CIFAR-100: É o mais complexo ainda, pois possui 100 classes diferentes, tendo portanto menos amostras por classe e algumas classes sendo muito semelhantes entre si, como um lobo e uma raposa. As imagens são pequenas e com pouca resolução, dificultando perceber diferenças entre as classes parecidas.

2.2) Análise das acurácias

MNIST: 94,49%, aumento do número de neurônios na camada densa para 50.

Fashion MNIST: 89,33%, aumento do número de neurônios na camada densa para 128.

CIFAR-10: 56,68%, aumento do número de neurônios na camada densa para 139.

CIFAR-100: 46,95%. Devido ao grande tamanho e complexidade do dataset, para alcançar uma acurácia acima de 20% foi necessário aumentar o número de camadas. Temos 3 camadas de convolução que possuem:

BatchNormalization, para garantir uma distribuição mais estável.

MaxPooling, para diminuir o tamanho dos dados.

Dropout, que desliga alguns pesos para tornar a rede mais robusta e diminuir o overfitting, que é um grande problema do CIFAR-100.

A última camada densa tem 512 neurônios, mas é possível que números melhores fossem encontrados.
