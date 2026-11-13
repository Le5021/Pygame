# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame  # Fornece janela, eventos, textos e desenhos.
import random  # Permite sortear o valor do dado.

pygame.init()  # Inicia os recursos do pygame.

# ----- Gera tela principal
largura_janela = 1000  # Define a largura da janela em pixels.
altura_janela = 680  # Define a altura da janela em pixels.
janela = pygame.display.set_mode((largura_janela, altura_janela))  # Cria a janela.
pygame.display.set_caption('Trilha dos desafios - Etapa 3')  # Define o título.

# ----- Define cores e fontes
cor_fundo = (245, 242, 230)  # Define o fundo claro.
cor_texto = (30, 42, 52)  # Define a cor escura dos textos e contornos.
cor_branca = (255, 255, 255)  # Define o branco do dado e dos olhos.
cor_preta = (0, 0, 0)  # Define o preto das bolinhas do dado.
cor_sombra = (207, 199, 178)  # Define a sombra das casas.
cor_perde_vez = (240, 120, 130)  # Marca uma casa revelada que encerra o turno.
cor_avanca = (100, 205, 130)  # Marca uma casa revelada que faz avançar.
cor_recua = (245, 165, 80)  # Marca uma casa revelada que faz recuar.
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



def sorteia_casas_especiais(quantidade):  # Recebe o número de pessoas e devolve os efeitos sorteados.
    casas_disponiveis = list(range(1, 19))  # Permite somente os índices das casas 2 a 19.
    random.shuffle(casas_disponiveis)  # Embaralha a lista para escolher casas sem repetir.
    tipos = ['avanca', 'avanca', 'recua']  # Define dois avanços e um recuo.
    if quantidade == 2:  # Verifica se existem duas pessoas na partida.
        tipos.append('perde_vez')  # Acrescenta a primeira casa de perda de vez.
        tipos.append('perde_vez')  # Acrescenta a segunda casa de perda de vez.
    especiais = {}  # Prepara o dicionário que relaciona cada casa ao seu efeito.
    for indice in range(len(tipos)):  # Percorre os efeitos que serão distribuídos.
        numero_passos = 0  # Começa com zero para o efeito de perder a vez.
        if tipos[indice] != 'perde_vez':  # Verifica se o efeito envolve deslocamento.
            numero_passos = random.randint(1, 3)  # Sorteia um deslocamento entre uma e três casas.
        especiais[casas_disponiveis[indice]] = {  # Registra o efeito na casa sorteada.
            'tipo': tipos[indice],  # Guarda se a casa avança, recua ou encerra o turno.
            'passos': numero_passos,  # Guarda a quantidade de casas do efeito.
            'revelada': False  # Mantém a aparência especial escondida inicialmente.
        }
    return especiais  # Entrega todos os efeitos da nova partida.


def cria_partida(quantidade):  # Recebe a quantidade de pessoas e reúne os dados da partida.
    dados = {  # Cria um dicionário para as funções compartilharem os dados sem usar global.
        'jogadores': cria_jogadores(quantidade),  # Cria as peças na casa inicial.
        'jogador_atual': 0,  # Dá o primeiro turno ao jogador 1.
        'casas_especiais': sorteia_casas_especiais(quantidade),  # Sorteia os efeitos ocultos.
        'valor_dado': 1,  # Define a face inicial do dado.
        'mensagem': 'Pronto para lançar!',  # Define a primeira mensagem do painel.
        'passos_restantes': 0,  # Guarda quantos passos faltam na animação.
        'direcao_movimento': 1,  # Usa 1 para avançar e -1 para recuar.
        'instante_ultimo_passo': 0,  # Guarda quando aconteceu o último passo.
        'origem_movimento': 'dado',  # Distingue o lançamento de um deslocamento especial.
        'casa_aviso': -1,  # Indica que ainda não existe uma casa aguardando confirmação.
        'mensagem_aviso': '',  # Guarda o texto da caixa de aviso.
        'inicio_resultado': 0,  # Guarda quando começou a mensagem de fim do turno.
        'vencedor': ''  # Guarda o nome de quem alcançar a chegada.
    }
    return dados  # Entrega a partida pronta para começar.


def inicia_movimento(partida, deslocamento, origem, agora):  # Recebe os dados, o deslocamento, sua origem e o tempo atual.
    jogador = partida['jogadores'][partida['jogador_atual']]  # Seleciona a peça da vez.
    destino = jogador['posicao'] + deslocamento  # Calcula o índice pretendido.
    if destino < 0:  # Verifica se o recuo ultrapassaria o início.
        destino = 0  # Limita o destino à casa 1.
    elif destino > len(casas) - 1:  # Verifica se o avanço ultrapassaria a chegada.
        destino = len(casas) - 1  # Limita o destino à casa 20.
    partida['direcao_movimento'] = 1  # Prepara um movimento para a frente.
    if destino < jogador['posicao']:  # Verifica se o destino fica para trás.
        partida['direcao_movimento'] = -1  # Prepara um movimento de recuo.
    partida['passos_restantes'] = abs(destino - jogador['posicao'])  # Conta os passos sem sinal negativo.
    partida['instante_ultimo_passo'] = agora  # Inicia a contagem de tempo da animação.
    partida['origem_movimento'] = origem  # Registra se o movimento veio do dado ou de um efeito.


def atualiza_movimento(partida, agora):  # Recebe a partida e o tempo atual; devolve se a animação terminou.
    if partida['passos_restantes'] > 0:  # Verifica se ainda é necessário mover a peça.
        if agora - partida['instante_ultimo_passo'] >= intervalo_passo:  # Espera o intervalo sem travar a janela.
            jogador = partida['jogadores'][partida['jogador_atual']]  # Seleciona a peça da vez.
            jogador['posicao'] += partida['direcao_movimento']  # Move exatamente uma casa.
            partida['passos_restantes'] -= 1  # Desconta o passo realizado.
            partida['instante_ultimo_passo'] = agora  # Registra o instante deste passo.
    return partida['passos_restantes'] == 0  # Informa se todos os passos foram realizados.


def texto_efeito(efeito):  # Recebe os dados de uma casa especial e devolve seu aviso.
    if efeito['tipo'] == 'perde_vez':  # Identifica a casa que encerra o turno.
        return 'Poxa! Você perdeu sua vez :('  # Entrega a mensagem solicitada.
    palavra_casas = 'casas'  # Prepara o plural para dois ou três passos.
    if efeito['passos'] == 1:  # Verifica se haverá apenas um passo.
        palavra_casas = 'casa'  # Ajusta a mensagem para o singular.
    quantidade = str(efeito['passos']) + ' ' + palavra_casas  # Monta a quantidade por escrito.
    if efeito['tipo'] == 'avanca':  # Identifica a casa que faz avançar.
        return 'Parabéns! Você avançará ' + quantidade + ' XD'  # Entrega o aviso de avanço.
    return 'Ihh, você recuará ' + quantidade + ' :/'  # Entrega o aviso de recuo.


def prepara_resultado(partida, mensagem, agora):  # Recebe a partida, uma mensagem e o instante atual.
    partida['mensagem'] = mensagem  # Registra a mensagem curta no painel.
    partida['inicio_resultado'] = agora  # Inicia o tempo de exibição antes da troca de turno.


def resolve_parada(partida, agora):  # Analisa a casa de parada e devolve o próximo estado.
    jogador = partida['jogadores'][partida['jogador_atual']]  # Consulta o participante da vez.
    posicao = jogador['posicao']  # Guarda o índice em que a peça parou.
    if posicao == len(casas) - 1:  # Verifica a chegada antes de qualquer outro efeito.
        partida['vencedor'] = jogador['nome']  # Registra imediatamente o vencedor.
        partida['mensagem'] = 'Chegou à casa 20!'  # Atualiza a mensagem do painel.
        return 'fim'  # Bloqueia novos lançamentos e mostra a vitória.
    if partida['origem_movimento'] == 'dado':  # Permite efeitos somente após o movimento do dado.
        if posicao in partida['casas_especiais']:  # Verifica se a casa de parada é especial.
            partida['casa_aviso'] = posicao  # Registra qual casa aguarda confirmação.
            partida['mensagem_aviso'] = texto_efeito(partida['casas_especiais'][posicao])  # Prepara o aviso.
            return 'aviso'  # Abre a caixa sem revelar ou aplicar o efeito ainda.
    prepara_resultado(partida, 'Parou na casa ' + str(posicao + 1) + '.', agora)  # Mostra onde o movimento terminou.
    return 'resultado'  # Encerra o turno; as atividades serão incluídas na Etapa 4.


def aplica_casa_especial(partida, agora):  # Aplica o efeito apenas depois de o aviso ser fechado.
    efeito = partida['casas_especiais'][partida['casa_aviso']]  # Consulta a casa que abriu o aviso.
    efeito['revelada'] = True  # Torna sua marcação visível pelo restante da partida.
    if efeito['tipo'] == 'perde_vez':  # Verifica se o efeito encerra o turno atual.
        prepara_resultado(partida, 'Você perdeu a vez.', agora)  # Prepara a mensagem antes da troca.
        return 'resultado'  # Aguarda brevemente e passa a vez sem movimento extra.
    deslocamento = efeito['passos']  # Prepara a quantidade de casas para avançar.
    if efeito['tipo'] == 'recua':  # Verifica se o movimento deve ser para trás.
        deslocamento = -deslocamento  # Transforma o avanço em recuo.
    inicia_movimento(partida, deslocamento, 'especial', agora)  # Inicia o deslocamento sem ativar outro efeito no destino.
    partida['mensagem'] = 'Aplicando o efeito...'  # Indica a animação extra no painel.
    return 'movimento'  # Continua a animação no mesmo loop principal.


def troca_turno(partida):  # Recebe a partida e escolhe quem lançará o próximo dado.
    partida['jogador_atual'] += 1  # Tenta passar ao próximo participante.
    if partida['jogador_atual'] >= len(partida['jogadores']):  # Verifica se a lista terminou.
        partida['jogador_atual'] = 0  # Retorna ao primeiro jogador, inclusive no modo individual.
    partida['mensagem'] = 'Pronto para lançar!'  # Prepara a instrução do novo turno.


# ----- Define funções de desenho
def desenha_texto(texto, fonte, cor, esquerda, topo):  # Recebe conteúdo, aparência e posição.
    texto_desenhado = fonte.render(texto, True, cor)  # Transforma o texto em uma superfície.
    janela.blit(texto_desenhado, (esquerda, topo))  # Coloca o texto na janela.


def desenha_texto_centralizado(texto, fonte, cor, centro_horizontal, topo):  # Recebe o texto, sua aparência, o centro desejado e a altura.
    texto_desenhado = fonte.render(texto, True, cor)  # Prepara o texto para desenhar e medir.
    largura_texto = texto_desenhado.get_width()  # Obtém a largura real da frase em pixels.
    esquerda = centro_horizontal - largura_texto // 2  # Coloca metade da largura de cada lado do centro.
    janela.blit(texto_desenhado, (esquerda, topo))  # Desenha o texto centralizado sem alterar sua altura.


def desenha_menu():  # Mostra as opções de quantidade de jogadores.
    desenha_texto_centralizado('TRILHA DOS DESAFIOS', fonte_titulo, cor_texto, largura_janela // 2, 160)  # Centraliza o título na janela.
    desenha_texto_centralizado('Escolha quantas pessoas vão jogar:', fonte_normal, cor_texto, largura_janela // 2, 230)  # Centraliza a instrução na janela.
    pygame.draw.rect(janela, cores_casas[1], botao_um_jogador)  # Desenha a primeira opção.
    pygame.draw.rect(janela, cores_casas[2], botao_dois_jogadores)  # Desenha a segunda opção.
    pygame.draw.rect(janela, cor_texto, botao_um_jogador, 2)  # Contorna o primeiro botão.
    pygame.draw.rect(janela, cor_texto, botao_dois_jogadores, 2)  # Contorna o segundo botão.
    desenha_texto('1 jogador', fonte_normal, cor_texto, 450, 303)  # Identifica o primeiro botão.
    desenha_texto('2 jogadores', fonte_normal, cor_texto, 440, 393)  # Identifica o segundo botão.
    desenha_texto_centralizado('Etapa 3: movimento, turnos e surpresas.', fonte_pequena, cor_texto, largura_janela // 2, 490)  # Explica esta versão.


def desenha_tabuleiro(partida):  # Recebe a partida e desenha as casas com os efeitos já revelados.
    for indice in range(len(casas) - 1):  # Percorre as casas que possuem uma próxima casa.
        pygame.draw.line(janela, cor_sombra, casas[indice].center, casas[indice + 1].center, 8)  # Liga casas vizinhas.
    for indice in range(len(casas)):  # Percorre todas as casas para desenhá-las sobre as linhas.
        casa = casas[indice]  # Seleciona o retângulo da casa atual.
        cor_casa = cores_casas[indice % len(cores_casas)]  # Repete a sequência de três cores.
        simbolo = ''  # Mantém a casa sem marca especial enquanto estiver escondida.
        if indice in partida['casas_especiais']:  # Verifica se existe efeito nesta casa.
            efeito = partida['casas_especiais'][indice]  # Consulta os dados do efeito.
            if efeito['revelada']:  # Só muda a aparência após a confirmação do aviso.
                if efeito['tipo'] == 'perde_vez':  # Identifica a perda de vez.
                    cor_casa = cor_perde_vez  # Muda a casa para vermelho.
                    simbolo = 'P'  # Marca a perda de vez.
                elif efeito['tipo'] == 'avanca':  # Identifica o avanço.
                    cor_casa = cor_avanca  # Muda a casa para verde.
                    simbolo = '+' + str(efeito['passos'])  # Mostra quantas casas avançar.
                else:  # Trata o efeito de recuo.
                    cor_casa = cor_recua  # Muda a casa para laranja.
                    simbolo = '-' + str(efeito['passos'])  # Mostra quantas casas recuar.
        pygame.draw.rect(janela, cor_sombra, (casa.x + 5, casa.y + 5, 72, 72))  # Desenha a sombra.
        pygame.draw.rect(janela, cor_casa, casa)  # Preenche a casa.
        pygame.draw.rect(janela, cor_texto, casa, 2)  # Desenha o contorno.
        desenha_texto(str(indice + 1), fonte_normal, cor_texto, casa.x + 6, casa.y + 4)  # Mostra o número de 1 a 20.
        desenha_texto_centralizado(simbolo, fonte_pequena, cor_texto, casa.centerx + 13, casa.y + 8)  # Deixa o símbolo acima das peças.
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


def desenha_pecas(partida):  # Recebe a partida para desenhar suas peças.
    jogadores = partida['jogadores']  # Consulta os participantes desta partida.
    for indice in range(len(jogadores)):  # Percorre os participantes presentes na partida.
        jogador = jogadores[indice]  # Consulta os dados de um participante.
        casa = casas[jogador['posicao']]  # Localiza o retângulo da casa da peça.
        esquerda = casa.x + 7 + indice * 32  # Separa as peças dentro da mesma casa.
        topo = casa.y + 32  # Coloca a peça abaixo do número da casa.
        desenha_personagem(esquerda, topo, jogador['cor'])  # Desenha a peça na posição calculada.


def desenha_dado(valor_dado):  # Recebe o número da face que será desenhada.
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


def desenha_painel(partida, estado):  # Recebe a partida e o estado para mostrar as instruções adequadas.
    pygame.draw.rect(janela, cor_painel, (760, 100, 220, 550))  # Desenha o painel lateral.
    desenha_texto('PARTICIPANTES', fonte_normal, cor_texto, 780, 125)  # Identifica a legenda.
    for indice in range(len(partida['jogadores'])):  # Percorre os participantes da partida.
        jogador = partida['jogadores'][indice]  # Consulta os dados do participante.
        altura_legenda = 175 + indice * 55  # Calcula a altura de cada nome.
        if indice == partida['jogador_atual']:  # Identifica o jogador responsável pelo turno.
            pygame.draw.rect(janela, cor_branca, (773, altura_legenda - 5, 198, 42))  # Destaca o participante atual.
        desenha_personagem(780, altura_legenda, jogador['cor'])  # Desenha a peça da legenda.
        desenha_texto(jogador['nome'], fonte_pequena, cor_texto, 815, altura_legenda + 6)  # Desenha o nome.
    jogador_atual = partida['jogadores'][partida['jogador_atual']]  # Consulta o participante da vez.
    instrucoes = {  # Relaciona cada estado à instrução exibida acima do dado.
        'tabuleiro': 'Clique no dado.',  # Indica que um lançamento está permitido.
        'movimento': 'Peça em movimento',  # Indica que a animação está em andamento.
        'aviso': 'Leia o aviso',  # Orienta a confirmação da caixa.
        'resultado': 'Turno encerrado',  # Indica a espera antes do próximo turno.
        'fim': 'Partida encerrada'  # Informa que a chegada foi alcançada.
    }
    desenha_texto_centralizado(instrucoes[estado], fonte_normal, cor_texto, retangulo_dado.centerx, 320)  # Centraliza a instrução.
    desenha_texto_centralizado(jogador_atual['nome'], fonte_pequena, cor_texto, retangulo_dado.centerx, 365)  # Identifica quem está jogando.
    desenha_texto_centralizado('Casa ' + str(jogador_atual['posicao'] + 1) + ' de 20', fonte_pequena, cor_texto, retangulo_dado.centerx, 390)  # Mostra a posição.
    desenha_texto_centralizado(partida['mensagem'], fonte_pequena, cor_texto, retangulo_dado.centerx, 440)  # Centraliza a mensagem do turno.
    desenha_dado(partida['valor_dado'])  # Mostra a última face sorteada.
    if estado != 'tabuleiro':  # Verifica se o lançamento está bloqueado.
        desenha_texto_centralizado('Dado bloqueado', fonte_pequena, cor_texto, retangulo_dado.centerx, 625)  # Explica por que o clique não funciona.


def desenha_caixa(titulo, mensagem, texto_botao):  # Recebe os textos do aviso ou da vitória.
    pygame.draw.rect(janela, cor_sombra, (168, 213, 680, 250))  # Desenha a sombra da caixa.
    pygame.draw.rect(janela, cor_branca, (160, 205, 680, 250))  # Desenha a caixa sobre o tabuleiro.
    pygame.draw.rect(janela, cor_texto, (160, 205, 680, 250), 3)  # Desenha o contorno da caixa.
    desenha_texto_centralizado(titulo, fonte_titulo, cor_texto, largura_janela // 2, 235)  # Centraliza o título.
    desenha_texto_centralizado(mensagem, fonte_normal, cor_texto, largura_janela // 2, 300)  # Centraliza o aviso.
    pygame.draw.rect(janela, cores_casas[1], botao_confirmar)  # Desenha o botão de confirmação.
    pygame.draw.rect(janela, cor_texto, botao_confirmar, 2)  # Contorna o botão.
    desenha_texto_centralizado(texto_botao, fonte_normal, cor_texto, botao_confirmar.centerx, 382)  # Mostra o texto do botão.
    desenha_texto_centralizado('Clique no botão ou pressione Enter.', fonte_pequena, cor_texto, largura_janela // 2, 430)  # Explica os dois controles.


# ----- Inicia estruturas de dados
casas = cria_casas()  # Guarda as vinte casas nas mesmas posições da Etapa 2.
partida = {}  # Aguarda a escolha do modo para receber os dados da partida.
retangulo_dado = pygame.Rect(810, 495, 120, 120)  # Define a área do dado.
botao_um_jogador = pygame.Rect(350, 280, 300, 65)  # Define a primeira opção do menu.
botao_dois_jogadores = pygame.Rect(350, 370, 300, 65)  # Define a segunda opção do menu.
botao_confirmar = pygame.Rect(400, 365, 200, 55)  # Define o botão das caixas de aviso.
intervalo_passo = 250  # Espera 250 milissegundos entre passos da peça.
duracao_resultado = 900  # Exibe o fim do turno por 900 milissegundos.
estado = 'menu'  # Começa na escolha da quantidade de pessoas.
jogo_ativo = True  # Mantém o loop principal em funcionamento.
relogio = pygame.time.Clock()  # Limita a velocidade de atualização da janela.

# ===== Loop principal =====
while jogo_ativo:  # Mantém eventos, lógica e saídas em um único loop.
    # ----- Prepara os pedidos deste frame
    pedido_inicio = 0  # Guarda uma escolha de um ou dois jogadores; zero significa nenhuma.
    pedido_dado = False  # Guarda se houve clique válido no dado neste frame.
    pedido_confirmacao = False  # Guarda a confirmação do aviso ou o pedido de jogar novamente.

    # ----- Trata eventos
    for evento in pygame.event.get():  # Recebe os eventos pendentes da janela.
        if evento.type == pygame.QUIT:  # Verifica se a janela deve ser fechada.
            jogo_ativo = False  # Solicita o encerramento sem processar novos movimentos.
        elif evento.type == pygame.MOUSEBUTTONDOWN:  # Verifica se houve clique do mouse.
            if evento.button == 1:  # Aceita apenas o botão esquerdo.
                if estado == 'menu':  # Trata as opções da tela inicial.
                    if pedido_inicio == 0:  # Aceita somente a primeira escolha deste frame.
                        if botao_um_jogador.collidepoint(evento.pos):  # Verifica a opção individual.
                            pedido_inicio = 1  # Solicita uma partida com uma pessoa.
                        elif botao_dois_jogadores.collidepoint(evento.pos):  # Verifica a opção em dupla.
                            pedido_inicio = 2  # Solicita uma partida com duas pessoas.
                elif estado == 'tabuleiro':  # Permite lançar somente quando não existe outra ação em andamento.
                    if retangulo_dado.collidepoint(evento.pos):  # Confere a área clicável do dado.
                        pedido_dado = True  # Registra um único pedido, mesmo com vários cliques no frame.
                elif estado == 'aviso' or estado == 'fim':  # Trata somente o botão da caixa aberta.
                    if botao_confirmar.collidepoint(evento.pos):  # Verifica se o botão foi atingido.
                        pedido_confirmacao = True  # Solicita a ação do botão: continuar ou jogar novamente.
        elif evento.type == pygame.KEYDOWN:  # Verifica o pressionamento de uma tecla.
            if evento.key == pygame.K_RETURN:  # Reconhece a tecla Enter.
                if estado == 'aviso' or estado == 'fim':  # Aceita Enter apenas nas caixas.
                    pedido_confirmacao = True  # Faz o mesmo que clicar no botão.

    # ----- Atualiza a lógica do jogo
    if jogo_ativo:  # Evita atualizar os dados após um pedido de fechamento.
        agora = pygame.time.get_ticks()  # Consulta o tempo transcorrido desde a inicialização.
        if estado == 'menu':  # Prepara a partida depois da escolha.
            if pedido_inicio != 0:  # Verifica se uma quantidade foi selecionada.
                partida = cria_partida(pedido_inicio)  # Cria participantes e sorteia efeitos escondidos.
                estado = 'tabuleiro'  # Libera o primeiro lançamento.
        elif estado == 'tabuleiro':  # Aguarda um lançamento do participante da vez.
            if pedido_dado:  # Verifica o pedido recebido nos eventos.
                partida['valor_dado'] = rola_dado()  # Sorteia uma única vez por lançamento.
                partida['mensagem'] = 'Dado: ' + str(partida['valor_dado'])  # Mostra o resultado.
                inicia_movimento(partida, partida['valor_dado'], 'dado', agora)  # Prepara os passos.
                estado = 'movimento'  # Bloqueia o dado durante a animação.
        elif estado == 'movimento':  # Executa os passos sem pausar o programa.
            if atualiza_movimento(partida, agora):  # Verifica se a peça terminou de andar.
                estado = resolve_parada(partida, agora)  # Decide entre aviso, fim do turno ou vitória.
        elif estado == 'aviso':  # Mantém o efeito pendente enquanto a caixa está aberta.
            if pedido_confirmacao:  # Verifica se a pessoa leu e fechou o aviso.
                estado = aplica_casa_especial(partida, agora)  # Revela a casa e aplica seu efeito.
        elif estado == 'resultado':  # Mantém a mensagem de fim do turno por um pequeno intervalo.
            if agora - partida['inicio_resultado'] >= duracao_resultado:  # Verifica se a espera terminou.
                troca_turno(partida)  # Alterna a pessoa ou mantém o jogador individual.
                estado = 'tabuleiro'  # Libera o dado para o novo turno.
        elif estado == 'fim':  # Mantém a partida encerrada após a chegada.
            if pedido_confirmacao:  # Verifica se a pessoa escolheu jogar novamente.
                partida = {}  # Descarta os dados e as marcações da partida encerrada.
                estado = 'menu'  # Volta à escolha de participantes sem fechar a janela.

        # ----- Gera saídas
        if jogo_ativo:  # Desenha somente enquanto a janela deve permanecer aberta.
            janela.fill(cor_fundo)  # Limpa os desenhos do frame anterior.
            if estado == 'menu':  # Verifica se a escolha de participantes deve aparecer.
                desenha_menu()  # Mostra os botões do menu.
            else:  # Desenha o tabuleiro nos demais estados.
                desenha_texto('TRILHA DOS DESAFIOS', fonte_titulo, cor_texto, 35, 25)  # Mostra o título do tabuleiro.
                desenha_tabuleiro(partida)  # Mostra casas comuns e efeitos já revelados.
                desenha_pecas(partida)  # Mostra as peças nas posições atuais.
                desenha_painel(partida, estado)  # Mostra o participante da vez e as instruções.
                if estado == 'aviso':  # Verifica se há uma casa especial aguardando confirmação.
                    desenha_caixa('CASA ESPECIAL', partida['mensagem_aviso'], 'Continuar')  # Sobrepõe o aviso.
                elif estado == 'fim':  # Verifica se alguém alcançou a última casa.
                    desenha_caixa('CHEGADA!', partida['vencedor'] + ' venceu!', 'Jogar novamente')  # Mostra a vitória e permite começar outra partida.
            pygame.display.update()  # Apresenta o frame completo na janela.
            relogio.tick(60)  # Limita o loop a sessenta atualizações por segundo.

# ===== Finalização =====
pygame.quit()  # Libera os recursos do pygame e fecha a janela.
