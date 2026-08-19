# 🖌️ Lousa Mágica

Uma lousa digital controlada por gestos das mãos, usando a webcam. Desenhe no ar com o dedo indicador e veja o traço aparecer na tela em tempo real, sem precisar de mouse, caneta ou touch — tudo via visão computacional com o [MediaPipe](https://developers.google.com/mediapipe).

<p align="center">
  <img src="giflousa.gif" alt="Demonstração da Lousa Mágica em uso" width="700">
</p>

## Funcionalidades

- **Desenho por gesto**: levante apenas o dedo indicador para desenhar.
- **Modo seleção**: levante indicador + médio juntos para mover o cursor sem desenhar e escolher cores.
- **Paleta de cores**: 4 cores disponíveis (Roxo, Rosa Claro, Vermelho, Branco), selecionáveis tocando nos retângulos exibidos no topo da tela.
- **Botão Limpar**: apaga todo o desenho da tela.
- **Espessura ajustável**: aumente ou diminua a espessura do traço pelo teclado.
- **Download automático do modelo**: o modelo `hand_landmarker.task` do MediaPipe é baixado automaticamente na primeira execução.

## Controles

| Gesto / Tecla | Ação |
|---|---|
| Apenas indicador levantado | Desenhar |
| Indicador + médio levantados | Mover sem desenhar / selecionar cor ou limpar |
| Mover o dedo sobre as caixas de cor (topo) | Trocar a cor do traço |
| Mover o dedo sobre a caixa "LIMPAR" | Limpar a tela |
| `c` | Limpar a tela |
| `+` ou `=` | Aumentar espessura do traço |
| `-` | Diminuir espessura do traço |
| `q` | Sair do programa |

## Como executar

1. Clone ou baixe este repositório.
2. Instale as dependências:
   ```bash
   pip install opencv-python numpy mediapipe
   ```
3. Execute o script:
   ```bash
   python lousa_magica.py
   ```
4. Uma janela chamada **"Lousa Magica"** abrirá exibindo a imagem da sua webcam.
5. Levante o dedo indicador na frente da câmera e comece a desenhar!

## Como funciona

O script utiliza o modelo **HandLandmarker** do MediaPipe para detectar 21 pontos (landmarks) da mão em cada frame capturado pela webcam. A partir da posição relativa entre a ponta do dedo indicador (landmark 8) e sua articulação (landmark 6), e do dedo médio (landmarks 12 e 10), o código determina se os dedos estão "levantados" ou "abaixados", definindo o modo de operação:

- **Só o indicador levantado** → modo desenho: a posição do dedo é conectada por uma linha ao ponto anterior em um `canvas` separado (uma camada preta sobreposta ao vídeo).
- **Indicador + médio levantados** → modo navegação: permite mover o cursor sobre a tela e interagir com a paleta de cores ou o botão de limpar, sem desenhar.

O `canvas` de desenho é combinado com o frame da webcam a cada iteração usando operações de bitwise (`AND`/`OR`) para sobrepor o traço à imagem da câmera em tempo real.

