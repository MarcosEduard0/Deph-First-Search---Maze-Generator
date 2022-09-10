import pygame
from random import choice

RES = LARGURA, ALTURA = 1200, 900
BLOCO = 50
cols, rows = LARGURA // BLOCO, ALTURA // BLOCO

pygame.init()
pygame.display.set_caption('Deph First Search - Maze')
sc = pygame.display.set_mode(RES)
time = pygame.time.Clock()


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.paredes = {'cima': True, 'direita': True,
                        'baixo': True, 'esquerda': True}
        self.visitado = False
        self.volta = False
        self.espessura = 2

    def draw_current_cell(self):
        x, y = self.x * BLOCO, self.y * BLOCO

        pygame.draw.rect(sc, pygame.Color('white'),
                         (x+self.espessura, y+self.espessura, BLOCO-self.espessura, BLOCO-self.espessura))

    def draw(self):
        x, y = self.x * BLOCO, self.y * BLOCO

        if self.visitado and not self.volta:
            pygame.draw.rect(sc, pygame.Color('white'), (x, y, BLOCO, BLOCO))
        elif self.volta:
            pygame.draw.rect(sc, pygame.Color(
                'lightblue'), (x, y, BLOCO, BLOCO))

        if self.paredes['cima']:
            pygame.draw.line(sc, pygame.Color('black'),
                             (x, y), (x + BLOCO, y), self.espessura)
        if self.paredes['direita']:
            pygame.draw.line(sc, pygame.Color('black'),
                             (x + BLOCO, y), (x + BLOCO, y + BLOCO), self.espessura)
        if self.paredes['baixo']:
            pygame.draw.line(sc, pygame.Color('black'),
                             (x + BLOCO, y + BLOCO), (x, y + BLOCO), self.espessura)
        if self.paredes['esquerda']:
            pygame.draw.line(sc, pygame.Color('black'),
                             (x, y + BLOCO), (x, y), self.espessura)

    def verificar_bloco(self, x, y):
        def posicao(x, y): return x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[posicao(x, y)]

    def vizinhos(self):
        vizinhos = []
        cima = self.verificar_bloco(self.x, self.y - 1)
        direita = self.verificar_bloco(self.x + 1, self.y)
        baixo = self.verificar_bloco(self.x, self.y + 1)
        esquerda = self.verificar_bloco(self.x - 1, self.y)
        if cima and not cima.visitado:
            vizinhos.append(cima)
        if direita and not direita.visitado:
            vizinhos.append(direita)
        if baixo and not baixo.visitado:
            vizinhos.append(baixo)
        if esquerda and not esquerda.visitado:
            vizinhos.append(esquerda)
        return choice(vizinhos) if vizinhos else False


def remover_paredes(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.paredes['esquerda'] = False
        next.paredes['direita'] = False
    elif dx == -1:
        current.paredes['direita'] = False
        next.paredes['esquerda'] = False
    dy = current.y - next.y
    if dy == 1:
        current.paredes['cima'] = False
        next.paredes['baixo'] = False
    elif dy == -1:
        current.paredes['baixo'] = False
        next.paredes['cima'] = False


grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []
sc.fill(pygame.Color('black'))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [cell.draw() for cell in grid_cells]
    current_cell.visitado = True
    # current_cell.draw_current_cell()

    next_cell = current_cell.vizinhos()
    if next_cell:
        next_cell.visitado = True
        stack.append(current_cell)
        remover_paredes(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell.volta = True
        current_cell = stack.pop()
        if not current_cell.vizinhos():
            current_cell.volta = True

    pygame.display.flip()

    time.tick(10)
