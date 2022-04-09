# Documentação

## Diagrama de Casos de Uso

![Diagrama de Casos de Uso](diagrams/use-cases.png)

O principal documento deste jogo é composto por um [diagrama de casos de uso](diagrams/), onde há dois atores:

- o **Jogador** (_Player_), que controla o **Personagem Jogável** ou **PJ** (_Player Character_ ou PC);
- e os **Monstros** (_Monsters_), que são controlado pela própria lógica do jogo.

O Jogador pode tomar algumas ações como:

- Mover seu personagem;
- Abrir o menu de opções;
- Interagir com um objeto;
- Atacar um monstro.

Já os Monstros são mais limitados, e devem aguardar a presença do personagem do jogador em seu raio de visão para realizarem ações predefinidas.

### Movimento do Personagem Jogável (PJ)

O Jogador move seu personagem em duas direções: horizontal e vertical. Ele pode mover-se em duas direções ao mesmo tempo, movendo-se em uma vetor resultante, na mesma velocidade de um movimento mais simples, na vertical ou horizontal.

Caso o PJ encontre-se em um bloco sólido, que o impeça de passar, o movimento deve ser interrompido, seguido por um som de "**Thud!!**". Sim, essa foi uma referência ao Barry de Pokémon.

### Menu de Opções

Caso o Jogador decida acessar o Menu de Opções, ele poderá realizar algumas ações, conforme descrito na tabela abaixo.

| Ação                 | Descrição                                                                                                 |
| -------------------- | --------------------------------------------------------------------------------------------------------- |
| Gerenciar Inventário | Mostra todos os itens, permite o Jogador criar novos itens (como bombas) e usar poções para recuperar PV. |
| Salvar Jogo          | Salva o estado atual do jogo, desde a última Dungeon.                                                     |
| Fechar Menu          | Fecha o menu e continua o jogo.                                                                           |
| Fechar Jogo          | Encerra a execução do programa e fecha o jogo.                                                            |

Enquanto o menu estiver aberto, o jogo deverá permanecer pausado, e quando ele for fechado, o jogo retornará ao estado anterior.

### Interações

O Jogador pode interagir com os objetos presentes no ambiente das diferentes fases.

Estes objetos podem fazer parte do nível (como é o caso de alavancas, por exemplo), ou serem coletáveis (como é o caso de pólvora e sucata). Caso eles sejam coletáveis e o PJ interaja com eles, o objeto vai para o inventário do jogador, onde poderá ser consumido ou usado para construir itens consumíveis (como bombas, chaves, tochas etc).

### Sistema de Combate

O Jogador pode fazer com que seu personagem realize um ataque de espada (_melee attack_) ou lance uma bomba (_ranged attack_). Caso haja colisão com um Monstro, este deverá receber dano.

Caso o PJ esteja na linha de visão de um Monstro, este caminhará na direção dele, atacando-o na primeira oportunidade. O padrão de ataque varia de acordo com o tipo de monstro. Por exemplo, slimes colidem e causam envenenamento, esqueletos atacam com armas etc.

**Obs.:** Pode ser interessante fazer com que as bombas quebre certas parede, revelando passagens secretas em algum momento, mas isso faria parte de "Interações".

## Especificações de Casos de Uso

Estes [documentos textuais](specifications/) representam cada ação individualmente com mais detalhes, com base no diagrama principal de casos de uso.
