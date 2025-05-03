# Roguelike Game

Um jogo Roguelike feito com PgZero.
 
 
## Como Executar
1. Instale o Python 3.x e PgZero:
   ```sh
   pip install pgzero
   ```
2. Certifique-se de que você está na pasta do projeto (onde está o arquivo `game.py`).
3. Execute o jogo com:
   ```sh
   pgzrun game.py
   ```

## Estrutura do Projeto
- `game.py`: Código principal do jogo.
- `images/`: Sprites do herói, inimigos, tiles e animações de ataque.
- `sounds/`: Efeitos sonoros do jogo (ex: step.ogg).
- `music/`: Música de fundo (ex: background.mp3).
- `Map/` e `roguelike-maps/`: Mapas e assets visuais.

## Explicação das Funções e Classes

### Button
- Representa um botão do menu.
- `__init__`: Cria o botão com texto e posição.
- `draw()`: Desenha o botão na tela.
- `check_hover(pos)`: Atualiza o estado de hover do botão.

### Hero
- Classe do personagem principal controlado pelo jogador.
- `__init__`: Inicializa atributos do herói (posição, vida, animação, etc).
- `attack()`: Ataca todos os inimigos em uma área 5x5 ao redor do herói.
- `draw()`: Desenha o herói e a animação de ataque (em tamanho dobrado).
- `update()`: Atualiza animação, movimentação contínua (segurando as setas), ataque e invulnerabilidade.

### Enemy
- Classe dos inimigos que patrulham pontos fixos no mapa.
- `__init__`: Inicializa atributos do inimigo (posição, patrulha, animação, etc).
- `update()`: Atualiza animação e movimentação do inimigo (patrulha área grande, movimento lento).
- `draw()`: Desenha o inimigo na tela.

### GameMenu
- Gerencia o menu principal e suas interações.
- `__init__`: Cria os botões do menu.
- `draw()`: Desenha o menu e seus botões.
- `handle_click(pos)`: Gerencia cliques nos botões do menu (iniciar, som, música, sair).
- `handle_mouse_move(pos)`: Atualiza o estado de hover dos botões do menu.

### reset_game
- Reinicia o herói e os inimigos para o início do jogo.

### update
- Atualiza o estado do jogo, entidades e música a cada frame.
- Controla movimentação, lógica de vitória/derrota, e música de fundo.

### draw
- Desenha o estado atual do jogo na tela (menu, jogando, vitória).

### on_mouse_down
- Gerencia cliques do mouse no menu.

### on_mouse_move
- Gerencia movimento do mouse para hover no menu.

### on_key_down
- Gerencia teclas pressionadas para pausa (P), ataque (ESPAÇO) e sair do jogo (ESC).

## Lógica do Jogo
- **Movimentação contínua:** O herói anda enquanto a seta estiver pressionada.
- **Animação de idle e movimento:** Herói e inimigos alternam entre frames idle e move.
- **Ataque em área:** O herói ataca todos os inimigos em um raio de 2 tiles (área 5x5).
- **Animação de ataque:** O efeito visual do ataque é desenhado em tamanho dobrado.
- **Inimigos patrulham** áreas grandes e se movem lentamente.
- **Menu interativo:** Opções de som, música, iniciar, retomar e sair.
- **Condição de vitória:** Derrote todos os inimigos para vencer.
- **Condição de derrota:** Ao perder toda a vida, volta ao menu.
- **Pausa:** Pressione P.
- **Música:** background.mp3 toca em todos os estados do jogo, controlada pelo botão Music ON/OFF no menu.

## Possíveis Melhorias
- Novos tipos de inimigos e patrulhas.
- Itens, power-ups e armas diferentes.
- IA dos inimigos mais avançada.
- Fases, mapas maiores e geração procedural.
- Salvar progresso do jogador.
- Animações e efeitos sonoros mais ricos.

## Créditos dos Assets
- Roguelike/RPG pack: https://kenney.nl/assets/roguelike-rpg-pack
- Roguelike Characters: https://kenney.nl/assets/roguelike-characters

---

Este projeto é um ponto de partida para jogos roguelike em Python, fácil de expandir e modificar!