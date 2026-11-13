# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame  # Fornece janela, eventos, textos e desenhos.
import random  # Permite sortear o valor do dado.

pygame.init()  # Inicia os recursos do pygame.

# ----- Gera tela principal
largura_janela = 1000  # Define a largura da janela em pixels.
altura_janela = 680  # Define a altura da janela em pixels.
janela = pygame.display.set_mode((largura_janela, altura_janela))  # Cria a janela.
pygame.display.set_caption('Trilha dos desafios - Etapa 2')  # Define o título.

# ----- Define cores e fontes
cor_fundo = (245, 242, 230)  # Define o fundo claro.
cor_texto = (30, 42, 52)  # Define a cor escura dos textos e contornos.
cor_branca = (255, 255, 255)  # Define o branco do dado e dos olhos.
cor_preta = (0, 0, 0)  # Define o preto das bolinhas do dado.
cor_sombra = (207, 199, 178)  # Define a sombra das casas.
cor_painel = (229, 233, 224)  # Define o fundo do painel lateral.
cor_jogador_1 = (100, 50, 185)  # Define o roxo da primeira peça.
cor_jogador_2 = (220, 55, 85)  # Define o vermelho da segunda peça.
cores_casas = [(255, 204, 62), (174, 205, 64), (40, 185, 186)]  # Alterna três cores.
fonte_titulo = pygame.font.Font(None, 44)  # Cria a fonte padrão para títulos.
fonte_normal = pygame.font.Font(None, 28)  # Cria a fonte padrão para textos.
fonte_pequena = pygame.font.Font(None, 22)  # Cria a fonte padrão para legendas.

# ----- Define funções de preparação
def cria_casas():  # Devolve os retângulos das casas na ordem do percurso.
    # Cada tupla guarda o centro horizontal e vertical de uma casa fixa.
    centros = [
        (80, 575),   # Casa 1: início na região inferior esquerda.
        (160, 525),  # Casa 2: começa a subida.
        (160, 435),  # Casa 3: continua subindo.
        (95, 355),   # Casa 4: curva para a esquerda.
        (90, 250),   # Casa 5: chega à região superior esquerda.
        (190, 190),  # Casa 6: curva para a direita.
        (300, 220),  # Casa 7: segue pela parte superior.
        (410, 175),  # Casa 8: ponto mais alto do percurso.
        (520, 215),  # Casa 9: começa a curva para baixo.
        (520, 325),  # Casa 10: desce para a curva interna.
        (460, 405),  # Casa 11: entra na região central.
        (375, 380),  # Casa 12: segue para a esquerda.
        (290, 390),  # Casa 13: termina a curva interna.
        (285, 480),  # Casa 14: desce novamente.
        (345, 560),  # Casa 15: curva na região inferior.
        (445, 575),  # Casa 16: segue pela parte inferior.
        (540, 545),  # Casa 17: começa a subida final.
        (615, 465),  # Casa 18: sobe pela direita.
        (660, 365),  # Casa 19: aproxima-se da chegada.
        (670, 255)   # Casa 20: chegada na região direita.
    ]
    casas_criadas = []  # Começa uma lista vazia de retângulos.
    for centro in centros:  # Percorre os centros na ordem das casas.
        casa = pygame.Rect(centro[0] - 36, centro[1] - 36, 72, 72)  # Cria uma casa.
        casas_criadas.append(casa)  # Acrescenta a casa à lista.
    return casas_criadas  # Entrega a lista pronta para o programa.


def cria_jogadores(quantidade):  # Recebe quantas pessoas jogarão e devolve seus dados.
    lista_jogadores = []  # Prepara a lista dos participantes.
    lista_jogadores.append({'nome': 'Jogador 1', 'cor': cor_jogador_1, 'posicao': 0})  # Cria o primeiro.
    if quantidade == 2:  # Verifica se uma segunda pessoa foi escolhida.
        lista_jogadores.append({'nome': 'Jogador 2', 'cor': cor_jogador_2, 'posicao': 0})  # Cria o segundo.
    return lista_jogadores  # Entrega um ou dois jogadores, ambos na casa 1.


def rola_dado():  # Sorteia o resultado de um lançamento.
    return random.randint(1, 6)  # Devolve um inteiro entre 1 e 6, incluindo os extremos.


# ----- Define funções de desenho
def desenha_texto(texto, fonte, cor, esquerda, topo):  # Recebe conteúdo, aparência e posição.
    texto_desenhado = fonte.render(texto, True, cor)  # Transforma o texto em uma superfície.
    janela.blit(texto_desenhado, (esquerda, topo))  # Coloca o texto na janela.


def desenha_menu():  # Mostra as opções de quantidade de jogadores.
    desenha_texto('TRILHA DOS DESAFIOS', fonte_titulo, cor_texto, 290, 160)  # Mostra o título.
    desenha_texto('Escolha quantas pessoas vão jogar:', fonte_normal, cor_texto, 320, 230)  # Orienta a escolha.
    pygame.draw.rect(janela, cores_casas[1], botao_um_jogador)  # Desenha a primeira opção.
    pygame.draw.rect(janela, cores_casas[2], botao_dois_jogadores)  # Desenha a segunda opção.
    pygame.draw.rect(janela, cor_texto, botao_um_jogador, 2)  # Contorna o primeiro botão.
    pygame.draw.rect(janela, cor_texto, botao_dois_jogadores, 2)  # Contorna o segundo botão.
    desenha_texto('1 jogador', fonte_normal, cor_texto, 450, 303)  # Identifica o primeiro botão.
    desenha_texto('2 jogadores', fonte_normal, cor_texto, 440, 393)  # Identifica o segundo botão.
    desenha_texto('Etapa 2: tabuleiro, peças e dado.', fonte_pequena, cor_texto, 365, 490)  # Explica esta versão.


def desenha_tabuleiro():  # Desenha o percurso fixo e suas vinte casas.
    for indice in range(len(casas) - 1):  # Percorre as casas que possuem uma próxima casa.
        pygame.draw.line(janela, cor_sombra, casas[indice].center, casas[indice + 1].center, 8)  # Liga casas vizinhas.
    for indice in range(len(casas)):  # Percorre todas as casas para desenhá-las sobre as linhas.
        casa = casas[indice]  # Seleciona o retângulo da casa atual.
        cor_casa = cores_casas[indice % len(cores_casas)]  # Repete a sequência de três cores.
        pygame.draw.rect(janela, cor_sombra, (casa.x + 5, casa.y + 5, 72, 72))  # Desenha a sombra.
        pygame.draw.rect(janela, cor_casa, casa)  # Preenche a casa.
        pygame.draw.rect(janela, cor_texto, casa, 2)  # Desenha o contorno.
        desenha_texto(str(indice + 1), fonte_normal, cor_texto, casa.x + 6, casa.y + 4)  # Mostra o número de 1 a 20.
    desenha_texto('INÍCIO', fonte_pequena, cor_texto, 50, 625)  # Marca a primeira casa.
    desenha_texto('CHEGADA', fonte_pequena, cor_texto, 630, 195)  # Marca a última casa.


def desenha_personagem(esquerda, topo, cor):  # Recebe a posição e a cor da peça pixel art.
    pygame.draw.rect(janela, cor_texto, (esquerda + 4, topo, 16, 12))  # Desenha a cabeça escura.
    pygame.draw.rect(janela, cor, (esquerda + 4, topo, 16, 4))  # Desenha a faixa colorida.
    pygame.draw.rect(janela, cor_branca, (esquerda + 7, topo + 6, 3, 3))  # Desenha um olho.
    pygame.draw.rect(janela, cor_branca, (esquerda + 14, topo + 6, 3, 3))  # Desenha o outro olho.
    pygame.draw.rect(janela, cor, (esquerda + 4, topo + 12, 16, 12))  # Desenha o corpo.
    pygame.draw.rect(janela, cor, (esquerda, topo + 12, 4, 8))  # Desenha um braço.
    pygame.draw.rect(janela, cor, (esquerda + 20, topo + 12, 4, 8))  # Desenha o outro braço.
    pygame.draw.rect(janela, cor_texto, (esquerda + 4, topo + 24, 6, 8))  # Desenha uma perna.
    pygame.draw.rect(janela, cor_texto, (esquerda + 14, topo + 24, 6, 8))  # Desenha a outra perna.


def desenha_pecas():  # Desenha todos os participantes em suas casas.
    for indice in range(len(jogadores)):  # Percorre os participantes presentes na partida.
        jogador = jogadores[indice]  # Consulta os dados de um participante.
        casa = casas[jogador['posicao']]  # Localiza o retângulo da casa da peça.
        esquerda = casa.x + 7 + indice * 32  # Separa as peças dentro da mesma casa.
        topo = casa.y + 32  # Coloca a peça abaixo do número da casa.
        desenha_personagem(esquerda, topo, jogador['cor'])  # Desenha a peça na posição calculada.


def desenha_dado():  # Desenha a face correspondente ao valor atual do dado.
    pygame.draw.rect(janela, cor_branca, retangulo_dado)  # Desenha o fundo do dado.
    pygame.draw.rect(janela, cor_texto, retangulo_dado, 3)  # Desenha sua borda.
    # Cada tupla indica uma bolinha dentro de uma grade imaginária de três por três.
    faces = {
        1: [(1, 1)],  # Uma bolinha central.
        2: [(0, 0), (2, 2)],  # Duas bolinhas em diagonal.
        3: [(0, 0), (1, 1), (2, 2)],  # Diagonal com o centro preenchido.
        4: [(0, 0), (2, 0), (0, 2), (2, 2)],  # Quatro cantos preenchidos.
        5: [(0, 0), (2, 0), (1, 1), (0, 2), (2, 2)],  # Quatro cantos e o centro.
        6: [(0, 0), (2, 0), (0, 1), (2, 1), (0, 2), (2, 2)]  # Duas colunas de três.
    }
    for ponto in faces[valor_dado]:  # Percorre as bolinhas da face sorteada.
        centro_horizontal = retangulo_dado.x + 25 + ponto[0] * 35  # Calcula a posição horizontal.
        centro_vertical = retangulo_dado.y + 25 + ponto[1] * 35  # Calcula a posição vertical.
        pygame.draw.circle(janela, cor_preta, (centro_horizontal, centro_vertical), 8)  # Desenha a bolinha.


def desenha_painel():  # Mostra participantes, instruções e resultado do lançamento.
    pygame.draw.rect(janela, cor_painel, (760, 100, 220, 550))  # Desenha o painel lateral.
    desenha_texto('PARTICIPANTES', fonte_normal, cor_texto, 780, 125)  # Mostra o título do painel.
    for indice in range(len(jogadores)):  # Percorre os jogadores para montar a legenda.
        jogador = jogadores[indice]  # Consulta o participante atual da legenda.
        altura_legenda = 175 + indice * 55  # Separa verticalmente os nomes.
        desenha_personagem(780, altura_legenda, jogador['cor'])  # Mostra a peça ao lado do nome.
        desenha_texto(jogador['nome'], fonte_pequena, cor_texto, 815, altura_legenda + 6)  # Mostra o nome.
    desenha_texto('Clique no dado.', fonte_normal, cor_texto, 780, 320)  # Explica o controle.
    desenha_texto('As peças se moverão', fonte_pequena, cor_texto, 780, 360)  # Explica o limite da etapa.
    desenha_texto('na próxima etapa.', fonte_pequena, cor_texto, 780, 385)  # Completa a explicação.
    desenha_texto(mensagem_dado, fonte_pequena, cor_texto, 780, 440)  # Exibe o resultado ou o convite.
    desenha_dado()  # Mostra o dado na parte inferior direita.


# ----- Inicia estruturas de dados
casas = cria_casas()  # Guarda as vinte casas em posições fixas.
jogadores = []  # Aguarda a escolha do modo para criar os participantes.
quantidade_jogadores = 0  # Guarda a quantidade escolhida no menu.
valor_dado = 1  # Mostra a face de um ponto antes do primeiro lançamento.
mensagem_dado = 'Pronto para lançar!'  # Guarda a mensagem exibida acima do dado.
retangulo_dado = pygame.Rect(810, 495, 120, 120)  # Define o desenho e a área clicável do dado.
botao_um_jogador = pygame.Rect(350, 280, 300, 65)  # Define a área da primeira opção.
botao_dois_jogadores = pygame.Rect(350, 370, 300, 65)  # Define a área da segunda opção.
estado = 'menu'  # Começa na tela de escolha dos participantes.
pedido_inicio = False  # Registra se o menu recebeu uma escolha.
pedido_dado = False  # Registra se o dado recebeu um clique válido.
jogo_ativo = True  # Mantém a janela aberta enquanto seu valor for verdadeiro.
relogio = pygame.time.Clock()  # Controla a velocidade de atualização da janela.

# ===== Loop principal =====
while jogo_ativo:  # Repete eventos, lógica e saídas enquanto a janela estiver aberta.
    # ----- Trata eventos
    for evento in pygame.event.get():  # Recebe os eventos pendentes do pygame.
        if evento.type == pygame.QUIT:  # Verifica se a pessoa clicou para fechar a janela.
            jogo_ativo = False  # Solicita o encerramento do loop principal.
        elif evento.type == pygame.MOUSEBUTTONDOWN:  # Verifica se houve um clique.
            if evento.button == 1:  # Aceita somente o botão esquerdo do mouse.
                if estado == 'menu':  # Trata os cliques da tela inicial.
                    if botao_um_jogador.collidepoint(evento.pos):  # Verifica a primeira opção.
                        quantidade_jogadores = 1  # Registra uma pessoa na partida.
                        pedido_inicio = True  # Solicita a preparação da partida.
                    elif botao_dois_jogadores.collidepoint(evento.pos):  # Verifica a segunda opção.
                        quantidade_jogadores = 2  # Registra duas pessoas na partida.
                        pedido_inicio = True  # Solicita a preparação da partida.
                elif estado == 'tabuleiro':  # Trata os cliques da tela do tabuleiro.
                    if retangulo_dado.collidepoint(evento.pos):  # Confere se o clique atingiu o dado.
                        pedido_dado = True  # Solicita um lançamento na parte de lógica.

    # ----- Atualiza a lógica do jogo
    if jogo_ativo:  # Evita atualizar ou desenhar depois de receber o pedido de fechamento.
        if estado == 'menu':  # Atualiza a escolha dos participantes.
            if pedido_inicio:  # Confere se uma opção foi escolhida.
                jogadores = cria_jogadores(quantidade_jogadores)  # Prepara os participantes.
                estado = 'tabuleiro'  # Troca a tela inicial pelo tabuleiro.
                pedido_inicio = False  # Limpa o pedido já atendido.
        elif estado == 'tabuleiro':  # Atualiza o dado na tela do tabuleiro.
            if pedido_dado:  # Verifica se existe um lançamento solicitado.
                valor_dado = rola_dado()  # Sorteia a nova face do dado.
                mensagem_dado = 'Você tirou: ' + str(valor_dado)  # Prepara a mensagem do resultado.
                pedido_dado = False  # Impede que o mesmo pedido se repita em outro frame.

        # ----- Gera saídas
        janela.fill(cor_fundo)  # Apaga o frame anterior preenchendo o fundo.
        if estado == 'menu':  # Verifica se a tela inicial deve aparecer.
            desenha_menu()  # Desenha as opções de participantes.
        elif estado == 'tabuleiro':  # Verifica se o tabuleiro deve aparecer.
            desenha_texto('TRILHA DOS DESAFIOS', fonte_titulo, cor_texto, 35, 25)  # Desenha o título.
            desenha_texto('Etapa 2 | Percurso fixo de 20 casas', fonte_pequena, cor_texto, 37, 73)  # Identifica a versão.
            desenha_tabuleiro()  # Desenha as casas e o caminho.
            desenha_pecas()  # Desenha os jogadores sobre as casas.
            desenha_painel()  # Desenha as instruções e o dado.
        pygame.display.update()  # Apresenta na janela tudo o que foi desenhado neste frame.
        relogio.tick(60)  # Limita o loop a, no máximo, sessenta atualizações por segundo.

# ===== Finalização =====
pygame.quit()  # Libera os recursos do pygame e fecha a janela.