# CAMIKAZE: O Voo da Capitã Camila ✈️

> **Builders League Edition LATAM 2026** — Uma evolução e customização completa do projeto base **Flappy Kiro**.
Um jogo retrô de navegação contínua no navegador, desenvolvido em HTML5, Vanilla JavaScript e Canvas API. Pilote a Capitã Camila desviando de arranha-céus, coletando estrelas e ativando power-ups em um cenário noturno dinâmico!

![Camikaze Game UI](img/example-ui.png)

## 🚀 Live Demo

👉 **[Jogar CAMIKAZE no GitHub Pages](https://camialmeidas.github.io/camikaze-flappy-game/)**

---

## 🎮 Como Jogar

1. Abra o arquivo `index.html` em qualquer navegador (ou sirva localmente com `python3 -m http.server 8000`).
2. Escolha a sua aeronave na tela inicial de seleção.
3. Clique ou pressione **Espaço** para iniciar e dar impulso/voar.
4. Navegue pelos espaços livres entre os prédios para pontuar.
5. Colete estrelas douradas e power-ups para acumular pontos e obter habilidades especiais!

---

## ⌨️ Controles

| Entrada | Ação |
|---|---|
| **Espaço / Clique / Toque** | Selecionar aeronave / Dar impulso / Reiniciar |

---

## ✨ Recursos & Melhorias (Camikaze)

- **Seleção de 3 Aeronaves Vetoriais (SVG)**:
  - 🛩️ **Vintage Militar**: Monoplano esportivo verde-oliva.
  - ✈️ **Caça Supersônico**: Jato moderno em tons de azul e ciano.
  - 🚁 **Heli-Patrulha**: Helicóptero em ciano neon de alto contraste para visibilidade noturna.

- **Zeppelin com Banner Publicitário**: Dirigível clássico navegando pelo fundo do céu noturno, puxando uma faixa rosa estilizada: *"★ CAMIKAZE ★ PILOTA: CAPITÃ CAMILA"*.

- **Progressão Dinâmica de Velocidade**: O jogo aumenta suavemente a velocidade de rolagem dos prédios a cada 10 pontos acumulados!

- **Sistema de Áudio via Web Audio API**: Som de derrota estilo *arcade* (glissando descendente de "whomp-whomp") sintetizado sem arquivos externos.

- **Power-ups & Efeitos Visuais**:
  - 🌟 **Estrelas Douradas**: Pontuação extra com explosão de partículas brilhantes ao coletar.
  - 🥊 **Punho Destruidor**: Proteção temporária contra obstáculos.
  - 🧲 **Ímã**: Atração automática de estrelas próximas.

- **Painel HUD Translúcido**: Exibição limpa de Pontos, Recorde Pessoal e Status de Power-up ativo no canto superior.

- **Física & Animação**: Rotação dinâmica do avião conforme a velocidade vertical e colisão imediata com prédios e chão.

---

## 🏗️ Arquitetura & Motor (Baseado em Flappy Kiro)

### Máquina de Estados

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Playing : Espaço / Clique / Toque
    Playing --> GameOver : Colisão (Chão/Prédios)
    GameOver --> Playing : Espaço / Clique / Toque
```

### Game Loop (Estado: Jogando)

```mermaid
flowchart LR
    A[Processar Input] --> B[Atualizar Física]
    B --> C[Spawn Prédios/Itens]
    C --> D[Mover Entidades]
    D --> E[Checar Colisões]
    E --> F[Atualizar Score/Velocidade]
    F --> G[Atualizar Efeitos/Partículas]
    G --> H[Renderizar Frame]
    H --> A
```

### Módulos do Sistema

```mermaid
graph TD
    CONFIG["Objeto CONFIG"]
    Physics["Engine de Física<br/>updateAirplane, jump"]
    BuildingManager["Gerenciador de Prédios<br/>spawnBuilding, updateBuildings"]
    CloudManager["Gerenciador de Estrelas<br/>initClouds, updateClouds"]
    CollisionDetector["Detector de Colisão<br/>checkCollision"]
    Scoring["Pontuação & Velocidade<br/>updateScore, updateDifficulty"]
    PowerupSystem["Sistema de Power-ups<br/>spawnPowerup, updatePowerups"]
    Renderer["Renderizador Canvas/SVG<br/>render, drawAirplane, drawZeppelin"]
    AudioManager["Sintetizador de Áudio<br/>playSound"]
    InputHandler["Manipulador de Entrada<br/>handleInput"]
    GameLoop["Game Loop<br/>gameLoop, idleLoop"]
    Persistence["Persistência<br/>localStorage High Score"]

    CONFIG --> Physics
    CONFIG --> BuildingManager
    CONFIG --> CloudManager
    CONFIG --> CollisionDetector
    CONFIG --> Renderer

    GameLoop --> Physics
    GameLoop --> BuildingManager
    GameLoop --> CloudManager
    GameLoop --> CollisionDetector
    GameLoop --> Scoring
    GameLoop --> PowerupSystem
    GameLoop --> Renderer
    InputHandler --> GameLoop
    InputHandler --> PowerupSystem
```

### Pipeline de Renderização (Render Pipeline)

```mermaid
flowchart TD
    A["Limpar Canvas"] --> B["Céu Noturno Base"]
    B --> C["Estrelas e Nuvens"]
    C --> D["Zeppelin e Banner em Background"]
    D --> E["Prédios com Janelas"]
    E --> F["Power-ups, Moedas e Partículas"]
    F --> G["Aeronave Selecionada SVG com Rotação"]
    G --> H["Painel HUD de Pontuação Translúcido"]
    H --> I["Overlays de Game Over / Tela Inicial"]
```

### Fluxo de Detecção de Colisão

```mermaid
flowchart TD
    A["checkCollision"] --> B{Bateu no Chão/Teto?}
    B -->|Sim| C["Retornar true / Game Over"]
    B -->|Não| D{Para cada Prédio}
    D --> E{Colisão Hitbox Prédio Superior?}
    E -->|Sim| C
    E -->|Não| G{Colisão Hitbox Prédio Inferior?}
    G -->|Sim| C
    G -->|Não| D
    D -->|Concluído| J["Retornar false / Voo Seguro"]
```

### Fluxo do Sistema de Power-Ups

```mermaid
sequenceDiagram
    participant P as Jogador
    participant G as Game Loop
    participant PU as Sistema de Power-ups
    participant R as Renderizador

    P->>G: Avião encosta em Power-up flutuante
    G->>PU: Ativa Efeito e Partículas
    PU->>G: Timer = 8 Segundos
    alt Ímã Ativado (Magnet)
        loop A cada Frame
            PU->>G: Atrai estrelas próximas ao jogador
            R->>R: Desenha anéis pulsantes ao redor do avião
        end
    else Punho Ativado (Punch)
        loop A cada Frame
            PU->>G: Modo Invencível (Ignora colisão de prédios)
            R->>R: Desenha escudo bolha ao redor do avião
        end
    end
    G->>G: Timer expira → Status Volta ao Normal
```

### 📁 Estrutura do Projeto

```
├── index.html          # Aplicação completa (HTML + CSS + Canvas + JavaScript + SVGs)
├── game-config.json    # Parâmetros e configurações do motor
├── assets/             # Recursos de áudio e sprites originais (backup)
├── img/                # Capturas de tela para documentação
├── LICENCE.md          # Licença do projeto
└── README.md           # Documentação do projeto
```

### ⚙️ Objeto CONFIG

Todas as variáveis de física e jogabilidade podem ser ajustadas no objeto `window.CONFIG` via console:

| Variável | Valor Padrão | Descrição |
|---|---|---|
| `gravity` | 800 | Aceleração da gravidade (px/s²) |
| `jumpVelocity` | -300 | Impulso de subida ao pressionar espaço (px/s) |
| `speed` | 120 | Velocidade inicial de rolagem dos obstáculos (px/s) |
| `gap` | 140 | Espaço vertical seguro de passagem entre os prédios (px) |

---

## 🏆 Créditos & Agradecimentos

**Desenvolvido para:** Builders League 🏆

**Projeto Base:** Flappy Kiro por DD.

**Assistência de Código:** Construído e polido com apoio do Kiro AI.

---

## 📜 Licença

Veja o arquivo LICENCE.md.