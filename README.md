
# 🎹 Music - Finger Piano (Modular HUD Edition)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green?style=flat-square&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand_Tracking-orange?style=flat-square)
![Pygame](https://img.shields.io/badge/Pygame-Audio_Engine-yellow?style=flat-square)

Um piano virtual tocado no ar através de visão computacional! Este projeto permite que você toque a introdução de **"PlayList de Musicas"** utilizando apenas os movimentos dos seus dedos em frente à webcam.


## Requisitos

- Python 3.11 ou 3.12
- Webcam funcionando
- Saida de audio ativa
- Conexao com internet no primeiro uso para baixar o modelo do MediaPipe


## Instalação

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```


## Execução

```bash
python main.py
```
Se você tiver mais de uma câmera, escolha o índice explicitamente:

```bash
python main.py --camera-index 1
```

Modo demo, sem camera:

```bash
python main.py --demo
```

Modo demo com reproducao automatica da sequencia:

```bash
python main.py --demo --autoplay
```

No primeiro lançamento, o arquivo do modelo sera baixado automaticamente para a pasta do projeto.

No modo demo, a aplicacao abre a HUD com um frame sintético, sem tracking da mao e sem inicializar camera ou audio. Isso serve para validar layout, janela e fluxo basico mesmo sem hardware.

Controles no modo demo:

- `1`: polegar
- `2`: indicador
- `3`: medio
- `4`: anelar
- `5`: minimo
- `A`: liga ou desliga o autoplay durante a execucao

Com `--autoplay`, a propria aplicacao toca automaticamente a proxima nota esperada da sequencia.
Mesmo sem essa flag, voce pode ativar ou pausar o autoplay a qualquer momento pelo teclado no modo demo.


## Testes

Validacao de sintaxe:

```bash
python -m compileall config.py main.py ui.py tests
```

Testes unitarios:

```bash
python -m unittest discover -s tests -v
```

Observacoes:

- O teste de audio pode ser pulado se pygame ou scipy nao estiverem disponiveis no ambiente atual.
- O teste completo da aplicacao principal continua sendo manual, porque depende de webcam, janela OpenCV e audio em tempo real.


## Validacao Manual

Durante a execucao, confirme estes pontos:

1. A janela abre sem erro.
2. A webcam e detectada.
3. Os landmarks da mao aparecem quando a mao entra no quadro.
4. As notas tocam ao dobrar os dedos.
5. A tecla Q fecha a aplicacao corretamente.


## Solução de Problemas

- Se a camera nao abrir, feche outros programas que estejam usando webcam.
- Se nao houver som, verifique se ha um dispositivo de saida configurado no sistema.
- Se o download do modelo falhar, teste novamente com internet ativa.
- Se alguma dependencia nao importar, recrie o ambiente virtual e reinstale o requirements.txt.
- Falhas de inicializacao tambem aparecem em uma janela visual da aplicacao, alem do terminal.


---

## 🏗️ Arquitetura do Projeto

O sistema monolítico foi dividido em componentes especialistas para facilitar a leitura e escalabilidade:

```text
📦 runaway-finger-piano
 ┣ 📜 main.py       # Entry-point: Orquestra o loop principal do vídeo e do jogo.
 ┣ 📜 config.py     # Central de configurações: Frequências, cores, constantes e layout.
 ┣ 📜 vision.py     # Inteligência Artificial: Download do modelo e tracking da mão (MediaPipe).
 ┣ 📜 audio.py      # Motor de Som: Geração matemática das ondas e integração com Pygame.
 ┣ 📜 ui.py         # Renderização: Desenho de HUDs dinâmicos, osciloscópio e botões com OpenCV.
 ┣ 📜 requirements.txt
 ┗ 📜 .gitignore
