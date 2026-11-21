# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame  # Fornece janela, eventos, textos e desenhos.
import random  # Permite sortear o valor do dado.
import math  # Permite calcular os ângulos do relógio do cronômetro.
import os  # Permite descobrir a pasta do próprio arquivo, para achar as fontes e os sons não importa de onde o jogo for executado.

pasta_jogo = os.path.dirname(os.path.abspath(__file__))  # Guarda a pasta onde este arquivo .py está salvo.


def caminho_recurso(caminho_relativo):  # Monta o caminho completo de um arquivo dentro da pasta do jogo.
    return os.path.join(pasta_jogo, caminho_relativo)  # Junta a pasta do jogo com o caminho pedido, como caminho_recurso('assets/sons/som_pulo.wav').


try:  # Prepara o áudio com uma configuração mais compatível antes de iniciar o pygame.
    pygame.mixer.pre_init(44100, -16, 2, 1024)  # Define frequência, formato e buffer antes do pygame.init(), o que evita som ausente em algumas placas de som.
except pygame.error:  # Evita travar caso o próprio pre_init falhe.
    pass  # Deixa o pygame.init() tentar com os valores padrão.
pygame.init()  # Inicia os recursos do pygame.
pygame.key.stop_text_input()  # Mantém a digitação desativada até começar uma atividade de texto.

# ----- Gera tela principal
largura_janela = 1000  # Define a largura da janela em pixels.
altura_janela = 680  # Define a altura da janela em pixels.
janela = pygame.display.set_mode((largura_janela, altura_janela), pygame.FULLSCREEN)  # Abre o jogo em tela cheia.
largura_janela = janela.get_width()  # Consulta a largura efetiva caso o computador ajuste o modo de tela cheia.
altura_janela = janela.get_height()  # Consulta a altura efetiva para posicionar a saída junto ao rodapé.
pygame.display.set_caption('Trilha dos Desafios')  # Define o título.

# ----- Define cores e fontes
cor_fundo = (245, 242, 230)  # Define o fundo claro.
cor_fundo_cinza = (180, 180, 180)  # Define o fundo cinza do tabuleiro e das telas de desafio.
cor_texto = (30, 42, 52)  # Define a cor escura dos textos e contornos.
cor_sair = (190, 35, 50)  # Define o vermelho do botão de saída e dos avisos de tempo.
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
cores_confete = cores_casas + [cor_jogador_1, cor_jogador_2]  # Reaproveita as cores do jogo nos confetes da vitória.
try:  # Tenta usar a fonte Poppins escolhida para o jogo.
    fonte_titulo = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Bold.ttf'), 52)  # Cria a fonte dos títulos, maior e mais chamativa.
    fonte_titulo_jogo = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Bold.ttf'), 56)  # Cria a fonte própria, maior, do título de cada desafio.
    fonte_normal = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Medium.ttf'), 26)  # Cria a fonte dos textos.
    fonte_instrucao = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Medium.ttf'), 22)  # Cria a fonte, um pouco menor, da instrução de cada desafio.
    fonte_pequena = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Medium.ttf'), 20)  # Cria a fonte das legendas.
    fonte_frase = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Medium.ttf'), 24)  # Cria a fonte maior da frase do ditado e do enigma.
    fonte_aviso_atividade = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Medium.ttf'), 22)  # Cria uma fonte um pouco menor para o aviso de tempo, que é mais longo.
    fonte_subtitulo = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Medium.ttf'), 20)  # Cria a fonte maior do subtítulo do tabuleiro.
    fonte_painel = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Medium.ttf'), 16)  # Cria a fonte menor das legendas próximas ao dado.
    fonte_relogio = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Bold.ttf'), 28)  # Cria a fonte em negrito do cronômetro, maior, pois o círculo cresceu.
    fonte_jogador = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Medium.ttf'), 30)  # Cria a fonte maior do nome do jogador na tela de desafio.
    fonte_nivel = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Medium.ttf'), 20)  # Cria a fonte maior do nível na tela de desafio.
    fonte_caixa_titulo = pygame.font.Font(caminho_recurso('assets/fontes/Poppins-Bold.ttf'), 38)  # Cria uma fonte própria para o título da caixa de aviso, que é mais estreita.
except FileNotFoundError:  # Evita travar o jogo caso os arquivos de fonte não estejam na pasta assets.
    fonte_titulo = pygame.font.Font(None, 52)  # Usa a fonte padrão do pygame para títulos.
    fonte_titulo_jogo = pygame.font.Font(None, 58)  # Usa a fonte padrão do pygame para o título de cada desafio.
    fonte_normal = pygame.font.Font(None, 28)  # Usa a fonte padrão do pygame para textos.
    fonte_instrucao = pygame.font.Font(None, 24)  # Usa a fonte padrão do pygame para a instrução de cada desafio.
    fonte_pequena = pygame.font.Font(None, 22)  # Usa a fonte padrão do pygame para legendas.
    fonte_frase = pygame.font.Font(None, 26)  # Usa a fonte padrão do pygame para a frase do ditado e do enigma.
    fonte_aviso_atividade = pygame.font.Font(None, 24)  # Usa a fonte padrão do pygame, um pouco menor, para o aviso de tempo.
    fonte_subtitulo = pygame.font.Font(None, 22)  # Usa a fonte padrão do pygame para o subtítulo.
    fonte_painel = pygame.font.Font(None, 18)  # Usa a fonte padrão do pygame para as legendas próximas ao dado.
    fonte_jogador = pygame.font.Font(None, 32)  # Usa a fonte padrão do pygame para o nome do jogador.
    fonte_nivel = pygame.font.Font(None, 22)  # Usa a fonte padrão do pygame para o nível.
    fonte_caixa_titulo = pygame.font.Font(None, 40)  # Usa a fonte padrão do pygame para o título da caixa de aviso.
    fonte_relogio = pygame.font.Font(None, 30)  # Usa a fonte padrão do pygame para o cronômetro, maior, pois o círculo cresceu.

# ----- Carrega sons e músicas
som_disponivel = True  # Marca se os sons puderam ser carregados, para não travar o jogo sem áudio.
musica_atual = ''  # Guarda qual trilha está tocando agora, para não reiniciá-la a cada frame.
som_pulo = None  # Garante que o nome já exista mesmo se o carregamento falhar logo abaixo.
som_vitoria = None  # Garante que o nome já exista mesmo se o carregamento falhar logo abaixo.
try:  # Tenta carregar os efeitos sonoros e preparar o mixer de música.
    pygame.mixer.init()  # Garante que o mixer esteja pronto mesmo se o pygame.init() não tiver ativado o áudio.
    som_pulo = pygame.mixer.Sound(caminho_recurso('assets/sons/som_pulo.wav'))  # Carrega o efeito tocado a cada passo da peça.
    som_vitoria = pygame.mixer.Sound(caminho_recurso('assets/sons/som_vitoria.wav'))  # Carrega o efeito tocado quando alguém vence.
    som_pulo.set_volume(1.0)  # Garante que o efeito não comece com o volume baixo.
    som_vitoria.set_volume(1.0)  # Garante que o efeito não comece com o volume baixo.
    print('Áudio carregado com sucesso. Mixer:', pygame.mixer.get_init())  # Confirma no terminal que o som está pronto.
except (FileNotFoundError, pygame.error) as erro:  # Evita travar o jogo caso os arquivos de som ou o áudio não estejam disponíveis.
    som_disponivel = False  # Mantém o jogo funcionando normalmente, apenas sem som.
    print('Não foi possível carregar o áudio:', erro)  # Mostra o motivo exato no terminal, para facilitar a correção.


def toca_som(som):  # Toca um efeito sonoro apenas se o áudio estiver disponível.
    if som_disponivel and som is not None:  # Evita chamar o mixer quando o carregamento falhou.
        som.play()  # Reproduz o efeito uma única vez.


def toca_musica(caminho_arquivo):  # Troca a música de fundo apenas quando ela muda, para não reiniciá-la a cada frame.
    global musica_atual  # Permite atualizar a trilha atualmente tocando.
    if not som_disponivel:  # Evita chamar o mixer quando o carregamento falhou.
        return  # Sai sem fazer nada.
    if musica_atual == caminho_arquivo:  # Verifica se essa já é a música tocando.
        return  # Evita reiniciar a mesma música repetidamente.
    try:  # Tenta trocar a trilha sem travar o jogo em caso de falha do mixer.
        pygame.mixer.music.load(caminho_arquivo)  # Carrega a nova trilha.
        pygame.mixer.music.set_volume(1.0)  # Garante que a música não comece com o volume baixo.
        pygame.mixer.music.play(-1)  # Toca em loop infinito, como pedido.
        musica_atual = caminho_arquivo  # Registra a trilha atual.
    except pygame.error as erro:  # Evita travar caso o arquivo não seja encontrado.
        print('Não foi possível tocar', caminho_arquivo, ':', erro)  # Mostra o motivo exato no terminal.


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
    return random.randint(1, 4)  # Sorteia somente 1, 2, 3 ou 4, com a mesma chance.



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
        'proximo_valor_dado': 1,  # Guarda o resultado que aparecerá ao terminar a rotação.
        'inicio_giro_dado': 0,  # Guarda o começo da animação vertical do dado.
        'mensagem': 'Pronto para lançar!',  # Define a primeira mensagem do painel.
        'passos_restantes': 0,  # Guarda quantos passos faltam na animação.
        'direcao_movimento': 1,  # Usa 1 para avançar e -1 para recuar.
        'instante_ultimo_passo': 0,  # Guarda quando aconteceu o último passo.
        'origem_movimento': 'dado',  # Distingue o lançamento de um deslocamento especial.
        'casa_aviso': -1,  # Indica que ainda não existe uma casa aguardando confirmação.
        'mensagem_aviso': '',  # Guarda o texto da caixa de aviso.
        'inicio_resultado': 0,  # Guarda quando começou a mensagem de fim do turno.
        'vencedor': '',  # Guarda o nome de quem alcançar a chegada.
        'ultima_atividade': '',  # Guarda o último desafio da partida, compartilhado entre os jogadores.
        'atividade': {}  # Aguarda os dados do desafio atual.
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
            toca_som(som_pulo)  # Toca o som de pulo a cada casa percorrida.
    return partida['passos_restantes'] == 0  # Informa se todos os passos foram realizados.


def texto_efeito(efeito):  # Recebe os dados de uma casa especial e devolve seu aviso.
    if efeito['tipo'] == 'perde_vez':  # Identifica a casa que encerra o turno.
        return 'Poxa! Você perdeu sua vez!'  # Entrega a mensagem solicitada.
    palavra_casas = 'casas'  # Prepara o plural para dois ou três passos.
    if efeito['passos'] == 1:  # Verifica se haverá apenas um passo.
        palavra_casas = 'casa'  # Ajusta a mensagem para o singular.
    quantidade = str(efeito['passos']) + ' ' + palavra_casas  # Monta a quantidade por escrito.
    if efeito['tipo'] == 'avanca':  # Identifica a casa que faz avançar.
        return 'Parabéns! Você avançará ' + quantidade + '!'  # Entrega o aviso de avanço.
    return 'Ihh, você recuará ' + quantidade + '! '  # Entrega o aviso de recuo.


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
    if partida['origem_movimento'] == 'dado':  # Abre um desafio somente em uma parada comum do dado.
        prepara_atividade(partida, agora)  # Sorteia um desafio diferente do anterior e inicia seu cronômetro.
        if partida['atividade']['aguarda_inicio']:  # Esconde o enunciado enquanto o jogador lê o prazo.
            return 'aviso_atividade'  # Aguarda Começar ou Enter sem consumir tempo.
        return 'atividade'  # Abre diretamente os desafios sem aviso.
    prepara_resultado(partida, 'Parou na casa ' + str(posicao + 1) + '.', agora)  # Mostra onde o movimento terminou.
    return 'resultado'  # Encerra um movimento especial ou uma penalidade sem abrir outro desafio.


def aplica_casa_especial(partida, agora):  # Aplica o efeito apenas depois de o aviso ser fechado.
    efeito = partida['casas_especiais'][partida['casa_aviso']]  # Consulta a casa que abriu o aviso.
    efeito['revelada'] = True  # Marca permanentemente nesta partida; sair da casa ou trocar de turno não apaga a revelação.
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



# ----- Define funções da atividade de pontos
def cria_pontos(quantidade_pares):  # Cria mais pares conforme a dificuldade da casa.
    cores_pontos = [(210, 55, 75), (40, 110, 210), (35, 155, 95), (235, 175, 25), (150, 65, 195), (235, 110, 30)]  # Oferece seis cores.
    pontos = []  # Guarda os pontos das duas colunas.
    for coluna in range(2):  # Cria um ponto de cada cor em cada lado.
        cores_coluna = cores_pontos[:quantidade_pares]  # Seleciona as cores da dificuldade atual.
        random.shuffle(cores_coluna)  # Varia a ordem em cada coluna.
        for linha in range(quantidade_pares):  # Distribui todos os pares na mesma área.
            pontos.append({
                'centro': (largura_janela // 2 - 220 + coluna * 440, 205 + linha * 300 // (quantidade_pares - 1)),  # Mantém os círculos dentro do quadro.
                'cor': cores_coluna[linha],  # Identifica o par.
                'ligado': False  # Começa sem conexão.
            })
    return pontos  # Entrega quatro, cinco ou seis pares.


# ----- Define funções da atividade de blocos
def cria_pilhas(quantidade_cores):  # Cria pilhas misturadas a partir de uma solução conhecida.
    cores = [(210, 55, 75), (40, 110, 210), (235, 175, 25), (35, 155, 95), (150, 65, 195)]  # Oferece até cinco cores.
    cores = cores[:quantidade_cores]  # Define três, quatro ou cinco pares de blocos.
    random.shuffle(cores)  # Varia a ordem inicial das cores.
    pilhas = []  # Prepara as pilhas organizadas.
    for cor in cores:  # Coloca dois blocos iguais em cada pilha.
        pilhas.append([cor, cor])  # Mantém a capacidade original de dois blocos.
    pilhas.append([])  # Reserva uma pilha vazia para os movimentos.
    pilhas[-1].append(pilhas[0].pop())  # Guarda temporariamente o topo da primeira pilha.
    for indice in range(quantidade_cores - 1):  # Transfere o topo da próxima pilha para a anterior.
        pilhas[indice].append(pilhas[indice + 1].pop())  # Mistura cada par com uma cor diferente.
    pilhas[quantidade_cores - 1].append(pilhas[-1].pop())  # Fecha o ciclo e deixa a última pilha vazia.
    random.shuffle(pilhas)  # Muda a posição visual das pilhas.
    return pilhas  # Todos os movimentos podem ser desfeitos, garantindo solução.


def cria_areas_pilhas(quantidade):  # Ajusta o tamanho das áreas à quantidade de pilhas.
    areas = []  # Guarda os retângulos usados para desenho e cliques.
    passo = 640 // quantidade  # Divide a largura disponível igualmente.
    for indice in range(quantidade):  # Distribui quatro, cinco ou seis pilhas.
        esquerda = largura_janela // 2 - 320 + indice * passo + 10  # Deixa espaço entre as pilhas.
        areas.append(pygame.Rect(esquerda, 220, passo - 20, 285))  # Mantém as alturas originais.
    return areas  # Entrega as áreas deste desafio.


def encontra_pilha(atividade, posicao_mouse):  # Procura o clique nas áreas do desafio atual.
    for indice in range(len(atividade['areas_pilhas'])):  # Considera a quantidade variável de pilhas.
        if atividade['areas_pilhas'][indice].collidepoint(posicao_mouse):  # Confere a área clicada.
            return indice  # Devolve a pilha encontrada.
    return -1  # Ignora cliques fora das pilhas.


def trata_clique_pilhas(atividade, posicao_mouse):  # Recebe o desafio e seleciona uma origem ou move seu bloco do topo.
    indice = encontra_pilha(atividade, posicao_mouse)  # Descobre a pilha clicada.
    if indice == -1:  # Verifica se o clique foi fora das áreas do desafio.
        return  # Ignora o clique sem alterar a seleção.
    pilhas = atividade['pilhas']  # Consulta as listas que representam as pilhas.
    origem = atividade['selecionado']  # Consulta a pilha escolhida como origem.
    if origem == -1:  # Verifica se ainda falta escolher de onde retirar um bloco.
        if len(pilhas[indice]) == 0:  # Verifica se a pilha clicada está vazia.
            atividade['mensagem'] = 'Escolha uma pilha que tenha algum bloco.'  # Explica por que ela não pode ser a origem.
        else:  # Trata uma pilha que possui um bloco no topo.
            atividade['selecionado'] = indice  # Destaca a pilha de origem.
            atividade['mensagem'] = 'Agora clique em uma pilha com espaço.'  # Solicita a escolha do destino.
    elif origem == indice:  # Verifica se a pessoa clicou novamente na origem.
        atividade['selecionado'] = -1  # Cancela a seleção sem mover blocos.
        atividade['mensagem'] = 'Seleção cancelada. Escolha outra pilha.'  # Explica o cancelamento.
    elif len(pilhas[indice]) >= capacidade_pilha:  # Verifica se a pilha de destino já está cheia.
        atividade['mensagem'] = 'Pilha cheia! Escolha outra ou clique na origem para cancelar.'  # Mantém a origem selecionada para outra tentativa.
    else:  # Permite mover para qualquer pilha com espaço, mesmo que tenha outra cor.
        bloco = pilhas[origem].pop()  # Retira somente o bloco do topo da origem.
        pilhas[indice].append(bloco)  # Coloca o bloco no topo do destino.
        atividade['selecionado'] = -1  # Libera a escolha de uma nova origem.
        atividade['mensagem'] = 'Bloco movido! Continue separando as cores.'  # Confirma o movimento.


def conta_pilhas_prontas(pilhas):  # Recebe as pilhas e conta quantas estão completas com uma única cor.
    quantidade = 0  # Inicia o contador de pilhas organizadas.
    for pilha in pilhas:  # Examina cada pilha.
        if len(pilha) == capacidade_pilha:  # Exige os dois blocos, sem contar pilhas vazias ou incompletas.
            if pilha[0] == pilha[1]:  # Compara as cores dos dois blocos.
                quantidade += 1  # Conta uma pilha completa e organizada.
    return quantidade  # Entrega o total para o placar e a verificação de sucesso.


def verifica_pilhas(atividade):  # Recebe o desafio e verifica sua condição de vitória.
    return conta_pilhas_prontas(atividade['pilhas']) == atividade['quantidade_cores']  # Exige todos os pares organizados e deixa uma pilha vazia.



# ----- Define funções da atividade de ditados
def normaliza_texto(texto):  # Recebe uma resposta e devolve uma versão simples para comparação.
    equivalentes = {  # Relaciona letras acentuadas às versões sem acento.
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a',  # Simplifica variações da letra a.
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',  # Simplifica variações da letra e.
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',  # Simplifica variações da letra i.
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',  # Simplifica variações da letra o.
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',  # Simplifica variações da letra u.
        'ç': 'c'  # Simplifica a cedilha.
    }
    texto = ' '.join(texto.lower().split())  # Converte para minúsculas e elimina espaços excedentes.
    normalizado = ''  # Prepara o texto que será devolvido.
    for caractere in texto:  # Percorre cada letra da resposta.
        if caractere in equivalentes:  # Verifica se a letra possui uma versão sem acento.
            normalizado += equivalentes[caractere]  # Acrescenta a letra simplificada.
        else:  # Trata os caracteres que não precisam de substituição.
            normalizado += caractere  # Mantém o caractere original.
    return normalizado  # Entrega a resposta preparada para comparação.


def confere_resposta_palavra(atividade):  # Recebe o desafio e confere o conteúdo do campo de texto.
    resposta = normaliza_texto(atividade['texto_digitado'])  # Simplifica o texto digitado sem mudar sua aparência na tela.
    if atividade['tipo'] == 'enigma':  # Aceita respostas como 'o pente' além de 'pente'.
        palavras = resposta.split()  # Separa as palavras da resposta já normalizada.
        if len(palavras) > 1 and palavras[0] in ['o', 'a', 'um', 'uma']:  # Reconhece um artigo opcional.
            resposta = ' '.join(palavras[1:])  # Compara apenas o nome do objeto.
    for alternativa in atividade['respostas']:  # Examina as respostas aceitas para o desafio.
        if resposta == normaliza_texto(alternativa):  # Compara as palavras sem distinguir acentos ou maiúsculas.
            return True  # Informa que a palavra está correta.
    return False  # Informa que nenhuma alternativa corresponde à resposta.


def trata_resposta_digitada(partida, acoes_texto, agora):  # Recebe as ações de teclado na ordem em que aconteceram.
    atividade = partida['atividade']  # Consulta o desafio digitado em andamento.
    for acao in acoes_texto:  # Percorre inserções, apagamentos e confirmações na ordem recebida.
        if atividade['resultado'] == '':  # Ignora as ações restantes se o desafio já foi resolvido.
            comando = acao[0]  # Identifica se a ação digita, apaga ou confirma.
            conteudo = acao[1]  # Consulta os caracteres enviados junto com a ação.
            if comando == 'digitar':  # Trata os caracteres recebidos pelo evento TEXTINPUT.
                for caractere in conteudo:  # Permite receber mais de uma letra em um único evento.
                    if len(atividade['texto_digitado']) < limite_caracteres:  # Evita ultrapassar o espaço do campo.
                        if atividade['tipo'] == 'calculo':  # Aceita algarismos e um sinal negativo no início.
                            if caractere in '0123456789' or (caractere == '-' and atividade['texto_digitado'] == ''):  # Impede sinais repetidos ou no meio do número.
                                atividade['texto_digitado'] += caractere  # Acrescenta o caractere válido.
                        elif caractere.isalpha() or caractere == ' ':  # Mantém letras e espaços nos desafios de palavras.
                            atividade['texto_digitado'] += caractere  # Preserva a grafia original da resposta.
                atividade['mensagem'] = 'Pressione Enter para confirmar sua resposta.'  # Orienta a confirmação.
            elif comando == 'apagar':  # Trata o pressionamento de Backspace.
                atividade['texto_digitado'] = atividade['texto_digitado'][:-1]  # Apaga o último caractere, mesmo se o campo já estiver vazio.
                atividade['mensagem'] = 'Edite a resposta e pressione Enter.'  # Orienta uma nova tentativa.
            elif comando == 'confirmar':  # Trata o pressionamento de Enter.
                if normaliza_texto(atividade['texto_digitado']) == '':  # Verifica se a resposta contém apenas espaços ou está vazia.
                    atividade['mensagem'] = 'Digite uma resposta antes de confirmar.'  # Solicita uma resposta sem encerrar o desafio.
                elif confere_resposta(atividade):  # Verifica se a palavra completa corretamente a frase.
                    conclui_atividade(partida, 'sucesso', 'Muito bem! Resposta correta.', agora)  # Registra o sucesso uma única vez.
                else:  # Trata uma palavra incorreta.
                    atividade['mensagem'] = 'Ainda não! Use Backspace e tente novamente.'  # Permite novas tentativas dentro do mesmo prazo.


# ----- Define a dificuldade e os cálculos matemáticos
def dificuldade_da_casa(posicao):  # Recebe o índice da casa ocupada pelo jogador da vez.
    numero_casa = posicao + 1  # Converte o índice para o número visível no tabuleiro.
    nivel = 1  # Usa a primeira faixa até a casa 7.
    if numero_casa >= 14:  # A última faixa antecede a chegada.
        nivel = 3  # Aplica a maior dificuldade nas casas 14 a 19.
    elif numero_casa >= 8:  # Identifica a região intermediária.
        nivel = 2  # Aplica dificuldade média nas casas 8 a 13.
    return nivel  # Cada jogador usa a própria posição; recuar pode reduzir a dificuldade.


def prazo_atividade(tipo, nivel):  # Centraliza os prazos dos cinco jogos.
    if tipo in ['ditado', 'enigma']:  # Reduz o tempo dos desafios de palavras conforme o avanço.
        return [20000, 10000, 10000][nivel - 1]  # Usa vinte segundos na primeira faixa e dez nas demais.
    if tipo == 'calculo':  # Mantém o prazo das contas em todas as faixas.
        return 20000  # Permite vinte segundos para digitar o resultado.
    return 10000  # Mantém dez segundos para pontos e blocos.


def cria_calculo(nivel):  # Gera contas com limites próprios para cada operação.
    operacao = random.choice(['+', '-', 'x', '÷'])  # Sorteia uma das quatro operações.
    if operacao in ['+', '-']:  # Preserva as faixas de soma e subtração.
        minimo, maximo = [(1, 9), (10, 30), (30, 99)][nivel - 1]  # Aumenta os números conforme a casa.
        primeiro = random.randint(minimo, maximo)  # Sorteia o primeiro número.
        segundo = random.randint(minimo, maximo)  # Sorteia o segundo número.
        if operacao == '+':  # Calcula uma soma.
            resposta = primeiro + segundo  # Guarda o total.
        else:  # Mantém a regra anterior das subtrações.
            primeiro, segundo = max(primeiro, segundo), min(primeiro, segundo)  # Coloca o maior primeiro.
            resposta = primeiro - segundo  # Guarda a diferença.
    else:  # Aplica os novos limites às multiplicações e divisões.
        if operacao == 'x':  # Limita os dois fatores, independentemente da casa.
            maximo = [5, 8, 10][nivel - 1]  # Aumenta a dificuldade sem ultrapassar dez em valor absoluto.
            primeiro = random.randint(1, maximo)  # Sorteia um fator de um até o limite da faixa.
            segundo = random.randint(1, maximo)  # Sorteia o outro fator no mesmo intervalo.
        else:  # Gera apenas divisões exatas, com ambos os números limitados a cem.
            maximo = [20, 50, 100][nivel - 1]  # Aumenta o limite absoluto conforme o avanço no tabuleiro.
            primeiro = random.randint(1, maximo)  # Sorteia o dividendo positivo, nunca maior que cem.
            divisores = []  # Guarda somente divisores exatos e diferentes de zero.
            for candidato in range(1, primeiro + 1):  # Examina os números de um até o dividendo.
                if primeiro % candidato == 0:  # Exige resto zero.
                    divisores.append(candidato)  # Permite sortear este divisor.
            segundo = random.choice(divisores)  # Garante um divisor entre um e cem e um quociente inteiro.
        if random.randint(0, 1) == 0:  # Permite que o primeiro número seja negativo.
            primeiro = -primeiro  # Altera apenas o sinal, preservando o limite absoluto.
        if random.randint(0, 1) == 0:  # Sorteia o sinal do segundo número de forma independente.
            segundo = -segundo  # Permite contas com um ou dois números negativos.
        if operacao == 'x':  # Resolve a multiplicação com os sinais sorteados.
            resposta = primeiro * segundo  # O produto pode ser positivo ou negativo.
        else:  # Resolve a divisão que já foi construída com resto zero.
            resposta = primeiro // segundo  # O resultado continua inteiro, inclusive quando negativo.
    texto_segundo = str(segundo)  # Prepara o segundo número para aparecer na tela.
    if segundo < 0:  # Destaca um sinal negativo depois do operador.
        texto_segundo = '(' + texto_segundo + ')'  # Mostra, por exemplo, -8 x (-3).
    return {'enunciado': str(primeiro) + ' ' + operacao + ' ' + texto_segundo + ' = ?', 'resposta': resposta}  # Entrega a conta e o resultado.


def confere_resposta(atividade):  # Escolhe a comparação apropriada ao desafio digitado.
    if atividade['tipo'] == 'calculo':  # Confere a resposta numérica.
        texto = atividade['texto_digitado']  # Consulta exatamente o conteúdo do campo.
        algarismos = texto  # Separa os algarismos do sinal opcional.
        if texto.startswith('-'):  # Aceita um único sinal de menos antes do número.
            algarismos = texto[1:]  # Remove apenas o primeiro caractere para validar os dígitos.
        if algarismos == '' or not algarismos.isdecimal():  # Rejeita vazio, sinal isolado e sinais fora de posição.
            return False  # Mantém a tentativa aberta.
        return int(texto) == atividade['resposta']  # Aceita também zeros à esquerda.
    return confere_resposta_palavra(atividade)  # Preserva a comparação que ignora acentos e maiúsculas.


def inicia_atividade(partida, agora):  # Inicia o cronômetro somente quando o desafio pode ser jogado.
    atividade = partida['atividade']  # Consulta o desafio preparado.
    atividade['aguarda_inicio'] = False  # Fecha o aviso anterior ao ditado ou enigma.
    atividade['inicio'] = agora  # Zera a contagem sem incluir o tempo de leitura do aviso.
    if atividade['tipo'] in ['ditado', 'calculo', 'enigma']:  # Ativa o teclado apenas para respostas digitadas.
        pygame.key.set_text_input_rect(campo_resposta)  # Informa onde fica o campo.
        pygame.key.start_text_input()  # Começa a receber texto.
    return 'atividade'  # Libera os controles do desafio.


# ----- Define funções comuns às atividades
def escolhe_atividade(partida):  # Sorteia uma atividade sem repetir a última apresentada na partida.
    opcoes = []  # Reúne apenas os desafios diferentes do anterior.
    for tipo in atividades_disponiveis:  # Percorre os jogos implementados; mantendo a regra entre os cinco.
        if tipo != partida['ultima_atividade']:  # Exclui o último jogo, mesmo após falha ou troca de jogador.
            opcoes.append(tipo)  # Permite sortear este desafio.
    return random.choice(opcoes)  # Sorteia entre as opções restantes com chances iguais.


def prepara_atividade(partida, agora):  # Recebe a partida e prepara o próximo desafio sem repetição consecutiva.
    tipo = escolhe_atividade(partida)  # Escolhe pelo histórico da partida, independentemente da casa.
    pygame.key.stop_text_input()  # Desativa qualquer entrada de texto de um desafio anterior.
    jogador = partida['jogadores'][partida['jogador_atual']]  # Consulta a posição de quem vai jogar.
    nivel = dificuldade_da_casa(jogador['posicao'])  # Calcula a faixa desta casa.
    atividade = {  # Prepara os dados compartilhados pelas cinco atividades.
        'tipo': tipo,  # Guarda o desafio que receberá cliques e será desenhado.
        'nivel': nivel,  # Guarda a dificuldade até o fim do desafio.
        'aguarda_inicio': tipo in ['ditado', 'enigma'],  # Exige aviso antes dos desafios de palavras.
        'selecionado': -1,  # Indica que ainda não existe ponto ou pilha selecionado.
        'inicio': agora,  # Guarda o instante inicial em milissegundos.
        'limite': prazo_atividade(tipo, nivel),  # Define o prazo conforme o jogo e a faixa.
        'mensagem': '',  # Aguarda a instrução específica do desafio.
        'resultado': '',  # Mantém o resultado indefinido enquanto o desafio está ativo.
        'tempo_final': prazo_atividade(tipo, nivel) // 1000  # Prepara o cronômetro desta faixa.
    }
    if tipo == 'pontos':  # Prepara a atividade de conectar cores iguais.
        atividade['pontos'] = cria_pontos(nivel + 3)  # Prepara quatro, cinco ou seis pares.
        atividade['ligacoes'] = []  # Começa sem linhas concluídas.
        atividade['mensagem'] = 'Clique em um ponto e depois no outro da mesma cor.'  # Explica o primeiro passo.
    elif tipo == 'blocos':  # Prepara a atividade de organizar pilhas.
        atividade['quantidade_cores'] = nivel + 2  # Usa seis, oito ou dez blocos.
        atividade['pilhas'] = cria_pilhas(atividade['quantidade_cores'])  # Garante uma configuração solucionável.
        atividade['areas_pilhas'] = cria_areas_pilhas(len(atividade['pilhas']))  # Ajusta desenho e cliques juntos.
        atividade['limite'] = 10000  # Define dez segundos para organizar os blocos.
        atividade['tempo_final'] = 10  # Prepara o valor inicial do cronômetro de blocos.
        atividade['mensagem'] = 'Escolha uma pilha para retirar o bloco do topo.'  # Explica o primeiro passo.
    elif tipo == 'ditado':  # Prepara a atividade de completar uma palavra.
        ditado = random.choice(ditados)  # Sorteia um dos ditados cadastrados.
        atividade['enunciado'] = ditado['enunciado']  # Guarda a frase com uma lacuna.
        atividade['respostas'] = ditado['respostas']  # Guarda as palavras aceitas para essa lacuna.
        atividade['texto_digitado'] = ''  # Começa com o campo de resposta vazio.
        atividade['mensagem'] = 'Digite a palavra que falta e pressione Enter.'  # Explica como responder.
    elif tipo == 'enigma':  # Prepara a quinta atividade, com aviso antes do cronômetro.
        enigma = random.choice(enigmas)  # Sorteia uma pergunta do banco de enigmas.
        atividade['enunciado'] = enigma['enunciado']  # Guarda a pergunta sem mostrá-la no aviso.
        atividade['respostas'] = enigma['respostas']  # Guarda as respostas que serão aceitas.
        atividade['texto_digitado'] = ''  # Começa com o campo vazio.
        atividade['mensagem'] = 'Descubra a resposta, digite e pressione Enter.'  # Explica como responder.
    elif tipo == 'calculo':  # Prepara a quarta atividade.
        conta = cria_calculo(nivel)  # Sorteia uma operação com números da faixa atual.
        atividade['enunciado'] = conta['enunciado']  # Guarda a conta exibida.
        atividade['resposta'] = conta['resposta']  # Guarda o resultado esperado.
        atividade['texto_digitado'] = ''  # Começa com o campo vazio.
        atividade['mensagem'] = 'Digite o resultado e pressione Enter.'  # Explica a resposta.
    partida['atividade'] = atividade  # Substitui integralmente os dados do desafio anterior.
    partida['ultima_atividade'] = tipo  # Impede repetir a atividade mesmo após falha ou troca de jogador.
    if not atividade['aguarda_inicio']:  # Jogos sem aviso começam imediatamente.
        inicia_atividade(partida, agora)  # Ativa os controles e o cronômetro.


def calcula_tempo_restante(atividade, agora):  # Recebe o desafio e o tempo atual; devolve os segundos restantes.
    if atividade['aguarda_inicio']:  # Não desconta o tempo de leitura do aviso.
        return atividade['limite'] // 1000  # Mantém o prazo completo até a confirmação.
    milissegundos = atividade['limite'] - (agora - atividade['inicio'])  # Desconta o tempo já utilizado.
    if milissegundos < 0:  # Verifica se o limite já foi ultrapassado.
        milissegundos = 0  # Evita exibir valores negativos no cronômetro.
    return (milissegundos + 999) // 1000  # Arredonda para cima para mostrar zero somente ao terminar o prazo.


def encontra_ponto(pontos, posicao_mouse):  # Recebe os pontos e um clique; devolve o índice atingido ou -1.
    for indice in range(len(pontos)):  # Examina a área circular de cada ponto.
        centro = pontos[indice]['centro']  # Consulta o centro do ponto.
        diferenca_horizontal = posicao_mouse[0] - centro[0]  # Mede a distância horizontal até o clique.
        diferenca_vertical = posicao_mouse[1] - centro[1]  # Mede a distância vertical até o clique.
        if diferenca_horizontal ** 2 + diferenca_vertical ** 2 <= raio_ponto ** 2:  # Verifica se o clique está dentro do círculo.
            return indice  # Informa qual ponto foi atingido.
    return -1  # Indica que o clique aconteceu fora dos pontos.


def trata_clique_pontos(atividade, posicao_mouse):  # Recebe o desafio e trata um clique sem encerrar a atividade.
    indice = encontra_ponto(atividade['pontos'], posicao_mouse)  # Descobre qual ponto foi clicado.
    if indice == -1:  # Verifica se o clique atingiu apenas o fundo.
        return  # Ignora o clique fora dos pontos.
    ponto = atividade['pontos'][indice]  # Consulta o ponto atingido.
    if ponto['ligado']:  # Verifica se esse ponto já pertence a uma conexão concluída.
        return  # Impede reutilizar um ponto já conectado.
    selecionado = atividade['selecionado']  # Consulta o primeiro ponto escolhido.
    if selecionado == -1:  # Verifica se a pessoa está escolhendo o primeiro ponto do par.
        atividade['selecionado'] = indice  # Destaca o ponto escolhido.
        atividade['mensagem'] = 'Agora clique no outro ponto da mesma cor.'  # Orienta o segundo clique.
    elif selecionado == indice:  # Verifica se a pessoa clicou novamente no mesmo ponto.
        atividade['selecionado'] = -1  # Cancela a seleção, sem criar uma ligação consigo mesmo.
        atividade['mensagem'] = 'Seleção cancelada. Escolha outro ponto.'  # Explica o cancelamento.
    elif ponto['cor'] == atividade['pontos'][selecionado]['cor']:  # Confere se as duas cores combinam.
        atividade['ligacoes'].append((selecionado, indice))  # Registra uma linha permanente entre os pontos.
        atividade['pontos'][selecionado]['ligado'] = True  # Marca o primeiro ponto como concluído.
        ponto['ligado'] = True  # Marca o segundo ponto como concluído.
        atividade['selecionado'] = -1  # Libera a escolha de outro par.
        atividade['mensagem'] = 'Par conectado! Escolha o próximo.'  # Confirma a conexão.
    else:  # Trata a tentativa de ligar cores diferentes.
        atividade['mensagem'] = 'Cores diferentes. Procure o par do ponto destacado.'  # Mantém a primeira seleção e permite tentar novamente.


def verifica_pontos(atividade):  # Recebe o desafio e verifica se todos os pares foram conectados.
    return len(atividade['ligacoes']) == len(atividade['pontos']) // 2  # Exige todos os pares completos.


def conclui_atividade(partida, resultado, mensagem, agora):  # Recebe a partida, o resultado, sua mensagem e o tempo atual.
    atividade = partida['atividade']  # Consulta os dados do desafio.
    atividade['resultado'] = resultado  # Guarda 'sucesso' ou 'falha'.
    pygame.key.stop_text_input()  # Encerra a captura de texto ao terminar o desafio.
    atividade['mensagem'] = mensagem  # Prepara a mensagem visível ao participante.
    atividade['tempo_final'] = calcula_tempo_restante(atividade, agora)  # Congela o cronômetro ao terminar.
    atividade['selecionado'] = -1  # Remove qualquer destaque de seleção.
    partida['inicio_resultado'] = agora  # Inicia a breve exibição do resultado do desafio.


def atualiza_atividade(partida, cliques, acoes_texto, desistir, agora):  # Recebe os pedidos do frame e devolve o próximo estado.
    atividade = partida['atividade']  # Consulta o desafio em andamento.
    if atividade['aguarda_inicio']:  # Bloqueia respostas e penalidades antes da confirmação.
        return 'aviso_atividade'  # Mantém o aviso aberto sem consumir o prazo.
    if agora - atividade['inicio'] >= atividade['limite']:  # Confere o prazo antes de aceitar qualquer resposta.
        conclui_atividade(partida, 'falha', 'Tempo esgotado! Você voltará uma casa.', agora)  # Registra a falha por tempo.
        return 'resultado_atividade'  # Mostra a falha antes de aplicar a penalidade.
    if desistir:  # Verifica se o botão de desistência foi clicado.
        conclui_atividade(partida, 'falha', 'Você desistiu. Voltará uma casa.', agora)  # Registra a desistência.
        return 'resultado_atividade'  # Mostra a consequência antes do recuo.
    for posicao_mouse in cliques:  # Trata os cliques recebidos neste frame na ordem de chegada.
        if atividade['resultado'] == '':  # Impede processar cliques adicionais depois de vencer.
            if atividade['tipo'] == 'pontos':  # Encaminha o clique para a atividade de pontos.
                trata_clique_pontos(atividade, posicao_mouse)  # Tenta selecionar ou conectar um par.
                if verifica_pontos(atividade):  # Verifica se todos os pares foram concluídos.
                    conclui_atividade(partida, 'sucesso', 'Muito bem! Você conectou todos os pares.', agora)  # Registra o sucesso nos pontos.
            elif atividade['tipo'] == 'blocos':  # Encaminha o clique para a atividade de blocos.
                trata_clique_pilhas(atividade, posicao_mouse)  # Tenta selecionar uma pilha ou mover seu topo.
                if verifica_pilhas(atividade):  # Verifica se todas as cores foram organizadas.
                    conclui_atividade(partida, 'sucesso', 'Muito bem! Você organizou todas as cores.', agora)  # Registra o sucesso nos blocos.
    if atividade['tipo'] in ['ditado', 'calculo', 'enigma']:  # Encaminha o teclado para os desafios digitados.
        trata_resposta_digitada(partida, acoes_texto, agora)  # Processa digitação, Backspace e Enter depois de conferir o prazo.
    if atividade['resultado'] == 'sucesso':  # Verifica se o desafio acabou por cliques ou digitação.
        return 'resultado_atividade'  # Mantém o desafio resolvido visível por um breve intervalo.
    return 'atividade'  # Continua recebendo cliques até o sucesso ou o fim do prazo.


# ----- Define funções de desenho
def desenha_texto(texto, fonte, cor, esquerda, topo):  # Recebe conteúdo, aparência e posição.
    texto_desenhado = fonte.render(texto, True, cor)  # Transforma o texto em uma superfície.
    janela.blit(texto_desenhado, (esquerda, topo))  # Coloca o texto na janela.


def desenha_texto_centralizado(texto, fonte, cor, centro_horizontal, topo):  # Recebe o texto, sua aparência, o centro desejado e a altura.
    texto_desenhado = fonte.render(texto, True, cor)  # Prepara o texto para desenhar e medir.
    largura_texto = texto_desenhado.get_width()  # Obtém a largura real da frase em pixels.
    esquerda = centro_horizontal - largura_texto // 2  # Coloca metade da largura de cada lado do centro.
    janela.blit(texto_desenhado, (esquerda, topo))  # Desenha o texto centralizado sem alterar sua altura.


def desenha_decoracao_menu():  # Desenha um trecho de tabuleiro só por estética, sem nenhuma função no jogo.
    centros_decoracao = [(160, 500), (280, 555), (400, 500), (520, 555), (640, 500), (760, 555), (880, 500)]  # Define um zigue-zague fixo, só decorativo.
    tamanho_decoracao = 54  # Define o tamanho de cada casa decorativa, menor que as casas reais.
    for indice in range(len(centros_decoracao) - 1):  # Percorre os pares de casas vizinhas.
        pygame.draw.line(janela, cor_sombra, centros_decoracao[indice], centros_decoracao[indice + 1], 8)  # Liga as casas decorativas.
    for indice in range(len(centros_decoracao)):  # Percorre cada casa decorativa.
        centro_x, centro_y = centros_decoracao[indice]  # Consulta o centro desta casa.
        cor_decoracao = cores_casas[indice % len(cores_casas)]  # Repete as mesmas três cores do tabuleiro real.
        meio = tamanho_decoracao // 2  # Calcula a metade do tamanho para montar o retângulo.
        pygame.draw.rect(janela, cor_sombra, (centro_x - meio + 4, centro_y - meio + 4, tamanho_decoracao, tamanho_decoracao))  # Desenha a sombra.
        pygame.draw.rect(janela, cor_decoracao, (centro_x - meio, centro_y - meio, tamanho_decoracao, tamanho_decoracao))  # Preenche a casa decorativa.
        pygame.draw.rect(janela, cor_texto, (centro_x - meio, centro_y - meio, tamanho_decoracao, tamanho_decoracao), 2)  # Contorna a casa decorativa.


def desenha_menu():  # Mostra as opções de quantidade de jogadores.
    desenha_texto_centralizado('TRILHA DOS DESAFIOS', fonte_titulo, cor_texto, largura_janela // 2, 160)  # Centraliza o título na janela.
    desenha_texto_centralizado('Escolha quantas pessoas irão jogar:', fonte_normal, cor_texto, largura_janela // 2, 230)  # Centraliza a instrução na janela.
    pygame.draw.rect(janela, cores_casas[1], botao_um_jogador)  # Desenha a primeira opção.
    pygame.draw.rect(janela, cores_casas[2], botao_dois_jogadores)  # Desenha a segunda opção.
    pygame.draw.rect(janela, cor_texto, botao_um_jogador, 2)  # Contorna o primeiro botão.
    pygame.draw.rect(janela, cor_texto, botao_dois_jogadores, 2)  # Contorna o segundo botão.
    desenha_texto_centralizado('1 Jogador', fonte_normal, cor_texto, botao_um_jogador.centerx, botao_um_jogador.centery - fonte_normal.get_height() // 2)  # Centraliza o nome no primeiro botão, na horizontal e na vertical.
    desenha_texto_centralizado('2 Jogadores', fonte_normal, cor_texto, botao_dois_jogadores.centerx, botao_dois_jogadores.centery - fonte_normal.get_height() // 2)  # Centraliza o nome no segundo botão, na horizontal e na vertical.
    desenha_decoracao_menu()  # Mostra o trechinho de tabuleiro decorativo abaixo dos botões.


def desenha_tabuleiro(partida):  # Recebe a partida e desenha as casas com os efeitos já revelados.
    for indice in range(len(casas) - 1):  # Percorre as casas que possuem uma próxima casa.
        pygame.draw.line(janela, cor_sombra, casas[indice].center, casas[indice + 1].center, 8)  # Liga casas vizinhas.
    for indice in range(len(casas)):  # Percorre todas as casas para desenhá-las sobre as linhas.
        casa = casas[indice]  # Seleciona o retângulo da casa atual.
        cor_casa = cores_casas[indice % len(cores_casas)]  # Repete a sequência de três cores.
        simbolo = ''  # Mantém a casa sem marca especial enquanto estiver escondida.
        if indice in partida['casas_especiais']:  # Verifica se existe efeito nesta casa.
            efeito = partida['casas_especiais'][indice]  # Consulta os dados do efeito.
            if efeito['revelada']:  # Redesenha a marca em todo frame do tabuleiro, mesmo sem jogador sobre a casa.
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
    desenha_texto('INÍCIO', fonte_pequena, cor_texto, 45, 515)  # Marca o início acima da casa e deixa o rodapé livre para a saída.
    desenha_texto('CHEGADA', fonte_pequena, cor_texto, 630, 195)  # Marca a última casa.


def calcula_pose_personagem(progresso):  # Recebe a fração do salto e devolve os retângulos da pose atual.
    indice_quadro = 0  # Começa procurando entre as duas primeiras poses.
    while indice_quadro < len(instantes_poses) - 2 and progresso > instantes_poses[indice_quadro + 1]:  # Avança até encontrar o trecho atual.
        indice_quadro += 1  # Escolhe o próximo par de poses.
    inicio = instantes_poses[indice_quadro]  # Consulta o instante inicial do trecho.
    fim = instantes_poses[indice_quadro + 1]  # Consulta o instante final do trecho.
    fracao = min(1, max(0, (progresso - inicio) / (fim - inicio)))  # Mede quanto falta para alcançar a próxima pose.
    fracao = fracao * fracao * (3 - 2 * fracao)  # Suaviza a transição entre os quadros.
    pose = []  # Prepara a lista dos retângulos interpolados.
    for indice_parte in range(len(quadros_personagem[0])):  # Percorre cabeça, tronco, braços e pernas.
        anterior = quadros_personagem[indice_quadro][indice_parte]  # Consulta a parte na pose anterior.
        seguinte = quadros_personagem[indice_quadro + 1][indice_parte]  # Consulta a mesma parte na pose seguinte.
        retangulo = []  # Prepara posição horizontal, vertical, largura e altura desta parte.
        for coordenada in range(4):  # Interpola os quatro valores do retângulo.
            valor = anterior[coordenada] + (seguinte[coordenada] - anterior[coordenada]) * fracao  # Aproxima o valor da próxima pose.
            retangulo.append(round(valor))  # Arredonda para manter os contornos nos pixels da tela.
        pose.append(retangulo)  # Acrescenta a parte à pose completa.
    return pose  # Entrega os retângulos que serão desenhados neste frame.


def desenha_parte_personagem(esquerda, topo, retangulo, cor, direcao):  # Desenha um retângulo do personagem, espelhando quando necessário.
    horizontal = retangulo[0]  # Consulta a posição da parte dentro do personagem.
    if direcao == -1:  # Verifica se o salto segue para a esquerda.
        horizontal = 24 - retangulo[0] - retangulo[2]  # Espelha a parte dentro da largura original de vinte e quatro pixels.
    area = (int(esquerda) + horizontal, int(topo) + retangulo[1], retangulo[2], retangulo[3])  # Posiciona a parte na janela.
    pygame.draw.rect(janela, cor, area)  # Desenha a parte usando somente um retângulo.


def desenha_personagem(esquerda, topo, cor, progresso=0, direcao=1):  # Recebe posição, cor e pose; os valores padrão desenham o personagem parado.
    pose = calcula_pose_personagem(progresso)  # Calcula a posição dos braços e das pernas neste instante.
    for indice in range(len(pose)):  # Percorre todas as partes do personagem.
        cor_parte = cor_texto  # Usa a cor escura para cabeça e pernas.
        if indice >= 1 and indice <= 5:  # Identifica o tronco e os quatro segmentos dos braços.
            cor_parte = cor  # Usa a cor do jogador na roupa e nos braços.
        desenha_parte_personagem(esquerda, topo, pose[indice], cor_parte, direcao)  # Desenha esta parte na orientação do salto.
    cabeca = pose[0]  # Consulta a cabeça para manter a faixa e os olhos presos a ela.
    faixa = (cabeca[0], cabeca[1], 16, 4)  # Define a faixa nas medidas originais.
    olho_esquerdo = (cabeca[0] + 3, cabeca[1] + 6, 3, 3)  # Posiciona o primeiro olho.
    olho_direito = (cabeca[0] + 10, cabeca[1] + 6, 3, 3)  # Posiciona o segundo olho.
    desenha_parte_personagem(esquerda, topo, faixa, cor, direcao)  # Desenha a faixa colorida.
    desenha_parte_personagem(esquerda, topo, olho_esquerdo, cor_branca, direcao)  # Desenha o primeiro olho.
    desenha_parte_personagem(esquerda, topo, olho_direito, cor_branca, direcao)  # Desenha o segundo olho.


def desenha_personagem_grande(esquerda, topo, cor, escala):  # Desenha o personagem parado numa escala maior, para a tela de nome.
    pose = pose_parada  # Usa sempre a pose parada, sem animação, nessa tela.
    for indice in range(len(pose)):  # Percorre todas as partes do personagem.
        cor_parte = cor_texto  # Usa a cor escura para cabeça e pernas.
        if 1 <= indice <= 5:  # Identifica o tronco e os quatro segmentos dos braços.
            cor_parte = cor  # Usa a cor do jogador na roupa e nos braços.
        x, y, largura_parte, altura_parte = pose[indice]  # Consulta a posição e o tamanho originais da parte.
        area = (esquerda + x * escala, topo + y * escala, largura_parte * escala, altura_parte * escala)  # Amplia a parte pela escala pedida.
        pygame.draw.rect(janela, cor_parte, area)  # Desenha a parte já ampliada.
    cabeca = pose[0]  # Consulta a cabeça para manter a faixa e os olhos presos a ela.
    faixa = (cabeca[0], cabeca[1], 16, 4)  # Define a faixa nas medidas originais.
    olho_esquerdo = (cabeca[0] + 3, cabeca[1] + 6, 3, 3)  # Posiciona o primeiro olho.
    olho_direito = (cabeca[0] + 10, cabeca[1] + 6, 3, 3)  # Posiciona o segundo olho.
    for retangulo, cor_parte in [(faixa, cor), (olho_esquerdo, cor_branca), (olho_direito, cor_branca)]:  # Percorre a faixa e os dois olhos.
        x, y, largura_parte, altura_parte = retangulo  # Consulta a posição e o tamanho originais.
        area = (esquerda + x * escala, topo + y * escala, largura_parte * escala, altura_parte * escala)  # Amplia a parte pela escala pedida.
        pygame.draw.rect(janela, cor_parte, area)  # Desenha a parte já ampliada.


def desenha_tela_nome(partida, indice_jogador_nome, nome_digitado, agora):  # Desenha a tela que pede o nome de um jogador antes do tabuleiro.
    jogador = partida['jogadores'][indice_jogador_nome]  # Consulta o jogador que está digitando o nome agora.
    desenha_texto_centralizado(jogador['nome'].upper(), fonte_titulo_jogo, cor_texto, largura_janela // 2, 75)  # Mostra de quem é a vez, bem grande.
    desenha_personagem_grande(140, 260, jogador['cor'], 7)  # Mostra o bonequinho do jogador numa escala bem maior.
    caixa = (430, 190, 470, 280)  # Define a área da caixa branca de digitação.
    pygame.draw.rect(janela, cor_branca, caixa)  # Desenha o fundo da caixa.
    pygame.draw.rect(janela, cor_preta, caixa, 3)  # Contorna a caixa.
    desenha_texto('Digite o seu nome:', fonte_normal, cor_texto, caixa[0] + 30, 215)  # Identifica o campo de digitação.
    pygame.draw.rect(janela, cor_fundo, campo_nome)  # Desenha o fundo do campo.
    pygame.draw.rect(janela, cor_texto, campo_nome, 2)  # Contorna o campo que já começa ativo.
    desenha_texto(nome_digitado, fonte_normal, cor_texto, campo_nome.x + 12, campo_nome.y + 18)  # Mostra o nome digitado até agora.
    if (agora // 500) % 2 == 0:  # Faz o cursor piscar enquanto a pessoa pode digitar.
        esquerda_cursor = campo_nome.x + 12 + fonte_normal.size(nome_digitado)[0]  # Coloca o cursor depois do último caractere.
        pygame.draw.line(janela, cor_texto, (esquerda_cursor, campo_nome.y + 14), (esquerda_cursor, campo_nome.y + 43), 2)  # Desenha o cursor.
    desenha_texto(str(len(nome_digitado)) + '/' + str(limite_nome_caracteres) + ' caracteres', fonte_pequena, cor_texto, caixa[0] + 30, 335)  # Mostra quantos caracteres já foram digitados.
    pygame.draw.rect(janela, cores_casas[1], botao_confirmar_nome)  # Desenha o fundo do botão de confirmação.
    pygame.draw.rect(janela, cor_texto, botao_confirmar_nome, 2)  # Contorna o botão.
    desenha_texto_centralizado('Confirmar', fonte_normal, cor_texto, botao_confirmar_nome.centerx, botao_confirmar_nome.centery - fonte_normal.get_height() // 2)  # Centraliza o texto do botão.


def calcula_animacao_peca(partida, indice, estado, agora):  # Devolve a fração do salto e a orientação dos membros de uma peça.
    progresso = 0  # Mantém a pose parada quando não existe um salto.
    direcao = 1  # Usa a orientação padrão enquanto a peça está parada.
    if estado == 'movimento' and indice == partida['jogador_atual'] and partida['passos_restantes'] > 0:  # Anima somente o participante que está andando.
        jogador = partida['jogadores'][indice]  # Consulta a casa atual do participante.
        casa_atual = casas[jogador['posicao']]  # Localiza o ponto de partida do salto.
        casa_seguinte = casas[jogador['posicao'] + partida['direcao_movimento']]  # Localiza o ponto de chegada.
        progresso = min(1, max(0, (agora - partida['instante_ultimo_passo']) / intervalo_passo))  # Calcula o progresso entre zero e um.
        if casa_seguinte.centerx < casa_atual.centerx:  # Verifica se a peça está seguindo para a esquerda da tela.
            direcao = -1  # Espelha braços e pernas para acompanhar o caminho.
        elif casa_seguinte.centerx == casa_atual.centerx and partida['direcao_movimento'] == -1:  # Trata um recuo vertical.
            direcao = -1  # Usa a pose espelhada também nesse recuo.
    return (progresso, direcao)  # Entrega as informações da pose sem alterar a posição lógica da peça.


def calcula_posicao_peca(partida, indice, estado, agora):  # Calcula onde desenhar uma peça, incluindo seu salto.
    jogador = partida['jogadores'][indice]  # Consulta a posição lógica do participante.
    casa = casas[jogador['posicao']]  # Localiza a casa em que a peça está apoiada.
    esquerda = casa.x + 7 + indice * 32  # Separa as duas peças quando ocuparem a mesma casa.
    topo_chao = casa.y + 32  # Define a altura normal da peça sobre o tabuleiro.
    altura_atual = 0  # Mantém a peça no chão quando não existe movimento.
    if estado == 'movimento' and indice == partida['jogador_atual']:  # Anima somente a peça da vez.
        if partida['passos_restantes'] > 0:  # Verifica se ainda existe um salto para executar.
            proxima_casa = casas[jogador['posicao'] + partida['direcao_movimento']]  # Consulta a próxima casa do percurso.
            progresso = min(1, max(0, (agora - partida['instante_ultimo_passo']) / intervalo_passo))  # Mede o avanço deste salto entre zero e um.
            progresso = min(1, max(0, (progresso - 0.15) / 0.70))  # Reserva o começo para o agachamento e o final para a aterrissagem.
            deslocamento_suave = progresso * progresso * (3 - 2 * progresso)  # Suaviza a saída e a chegada da peça.
            esquerda += (proxima_casa.x - casa.x) * deslocamento_suave  # Interpola a posição horizontal até a próxima casa.
            topo_chao += (proxima_casa.y - casa.y) * deslocamento_suave  # Interpola a altura do caminho, inclusive nas curvas.
            altura_atual = altura_salto * 4 * progresso * (1 - progresso)  # Forma um arco que começa e termina com altura zero.
    return (esquerda, topo_chao - altura_atual, topo_chao)  # Entrega a posição da peça e a altura de sua sombra.


def desenha_pecas(partida, estado, agora):  # Desenha todos os participantes, usando a posição animada quando necessário.
    for indice in range(len(partida['jogadores'])):  # Percorre as peças existentes.
        jogador = partida['jogadores'][indice]  # Consulta a cor do participante.
        posicao = calcula_posicao_peca(partida, indice, estado, agora)  # Calcula a posição dentro do salto atual.
        animacao = calcula_animacao_peca(partida, indice, estado, agora)  # Seleciona a pose e a orientação correspondentes a este salto.
        pygame.draw.ellipse(janela, cor_sombra, (int(posicao[0]) + 2, int(posicao[2]) + 29, 20, 5))  # Mantém uma pequena sombra no chão nas dimensões originais.
        desenha_personagem(posicao[0], posicao[1], jogador['cor'], animacao[0], animacao[1])  # Desenha cabeça, braços e pernas na pose calculada.


def projeta_ponto_dado(horizontal, vertical, profundidade, seno, cosseno):  # Converte um ponto do cubo em uma posição na tela.
    altura_girada = vertical * cosseno + profundidade * seno  # Faz a face atual girar para baixo.
    profundidade_girada = profundidade * cosseno - vertical * seno  # Calcula a profundidade depois da rotação.
    perspectiva = 1 + 0.12 * (profundidade_girada - 1)  # Deixa as partes mais afastadas um pouco mais estreitas.
    esquerda = retangulo_dado.centerx + horizontal * retangulo_dado.width / 2 * perspectiva  # Converte a posição horizontal.
    topo = retangulo_dado.centery + altura_girada * retangulo_dado.height / 2  # Converte a posição vertical.
    return (int(esquerda), int(topo))  # Entrega um ponto para os polígonos e as bolinhas.


def desenha_face_dado(valor, face, seno, cosseno):  # Desenha uma das faces visíveis durante a rotação.
    vertices_cubo = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1)]  # Define os quatro cantos da face frontal.
    compressao = cosseno  # Faz a face antiga ficar mais baixa ao girar para baixo.
    luminosidade = int(255 - 55 * seno)  # Escurece suavemente a face que está saindo.
    if face == 'superior':  # Prepara a nova face que entra pela parte de cima.
        vertices_cubo = [(-1, -1, -1), (1, -1, -1), (1, -1, 1), (-1, -1, 1)]  # Define os cantos da face superior.
        compressao = seno  # Faz a nova face ganhar altura ao virar para a frente.
        luminosidade = int(200 + 55 * seno)  # Clareia a face que está chegando.
    if compressao < 0.005:  # Evita desenhar uma face que está totalmente de perfil.
        return  # Deixa aparecer apenas a outra face.
    vertices_tela = []  # Prepara a lista de cantos projetados.
    for vertice in vertices_cubo:  # Percorre os quatro cantos da face.
        vertices_tela.append(projeta_ponto_dado(vertice[0], vertice[1], vertice[2], seno, cosseno))  # Projeta um canto.
    pygame.draw.polygon(janela, (luminosidade, luminosidade, luminosidade), vertices_tela)  # Preenche a face com iluminação simples.
    pygame.draw.polygon(janela, cor_texto, vertices_tela, 3)  # Mantém os três pixels do contorno original do dado.
    distancia_bolinhas = 35 / (retangulo_dado.width / 2)  # Preserva os trinta e cinco pixels de distância entre as bolinhas da grade original.
    pontos_faces = {  # Define as quatro faces permitidas pelo jogo.
        1: [(0, 0)],  # Coloca uma bolinha no centro.
        2: [(-distancia_bolinhas, -distancia_bolinhas), (distancia_bolinhas, distancia_bolinhas)],  # Coloca duas bolinhas em diagonal.
        3: [(-distancia_bolinhas, -distancia_bolinhas), (0, 0), (distancia_bolinhas, distancia_bolinhas)],  # Acrescenta o centro à diagonal.
        4: [(-distancia_bolinhas, -distancia_bolinhas), (distancia_bolinhas, -distancia_bolinhas), (-distancia_bolinhas, distancia_bolinhas), (distancia_bolinhas, distancia_bolinhas)]  # Coloca uma bolinha em cada canto.
    }
    for ponto in pontos_faces[valor]:  # Desenha as bolinhas do valor desta face.
        if face == 'superior':  # Posiciona as bolinhas sobre o plano superior do cubo.
            centro = projeta_ponto_dado(ponto[0], -1, ponto[1], seno, cosseno)  # A profundidade vira a posição vertical da nova face.
        else:  # Posiciona as bolinhas sobre a face antiga.
            centro = projeta_ponto_dado(ponto[0], ponto[1], 1, seno, cosseno)  # Mantém os pontos presos à face frontal.
        altura_bolinha = max(1, int(16 * compressao))  # Achata a bolinha de dezesseis pixels de acordo com a inclinação da face.
        pygame.draw.ellipse(janela, cor_preta, (centro[0] - 8, centro[1] - altura_bolinha // 2, 16, altura_bolinha))  # Mantém o tamanho original das bolinhas sem usar imagens.


def desenha_dado(partida, estado, agora):  # Desenha o dado parado ou durante sua rotação vertical.
    if estado == 'rolando_dado':  # Verifica se o lançamento está animando.
        progresso = min(1, max(0, (agora - partida['inicio_giro_dado']) / duracao_giro_dado))  # Mede a fração concluída do giro.
        seno = progresso * progresso * (3 - 2 * progresso)  # Suaviza o começo e o fim da rotação.
        cosseno = (1 - seno * seno) ** 0.5  # Calcula a outra componente da rotação sem importar uma biblioteca matemática.
        desenha_face_dado(partida['valor_dado'], 'frontal', seno, cosseno)  # Desenha o número atual descendo.
        desenha_face_dado(partida['proximo_valor_dado'], 'superior', seno, cosseno)  # Desenha o novo número chegando por cima.
    else:  # Trata os estados em que o dado já está parado.
        desenha_face_dado(partida['valor_dado'], 'frontal', 0, 1)  # Mostra a face atual completamente de frente.


def desenha_painel(partida, estado, agora):  # Recebe a partida e o estado para mostrar as instruções adequadas.
    pygame.draw.rect(janela, cor_painel, (760, 100, 220, 550))  # Desenha o painel lateral.
    pygame.draw.rect(janela, cor_preta, (760, 100, 220, 550), 3)  # Contorna o painel com borda preta para destacá-lo.
    desenha_texto_centralizado('PARTICIPANTES', fonte_normal, cor_texto, 870, 125)  # Centraliza a legenda dentro do painel.
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
        'rolando_dado': 'Rolando o dado...',  # Identifica a animação antes do deslocamento.
        'movimento': 'Peça em movimento',  # Indica que a animação está em andamento.
        'aviso': 'Leia o aviso',  # Orienta a confirmação da caixa.
        'resultado': 'Turno encerrado',  # Indica a espera antes do próximo turno.
        'fim': 'Partida encerrada'  # Informa que a chegada foi alcançada.
    }
    desenha_texto_centralizado(instrucoes[estado], fonte_pequena, cor_texto, retangulo_dado.centerx, 400)  # Centraliza a instrução, próxima ao dado, em fonte menor.
    desenha_texto_centralizado(jogador_atual['nome'], fonte_painel, cor_texto, retangulo_dado.centerx, 435)  # Identifica quem está jogando, próximo ao dado, em fonte menor.
    desenha_texto_centralizado(partida['mensagem'], fonte_painel, cor_texto, retangulo_dado.centerx, 463)  # Centraliza a mensagem do turno, logo acima do dado, em fonte menor.
    desenha_dado(partida, estado, agora)  # Mostra a última face sorteada.
    if estado != 'tabuleiro':  # Verifica se o lançamento está bloqueado.
        desenha_texto_centralizado('Dado bloqueado', fonte_pequena, cor_texto, retangulo_dado.centerx, 625)  # Explica por que o clique não funciona.


def desenha_caixa(titulo, mensagem, texto_botao, fonte_mensagem=None):  # Recebe os textos do aviso ou da vitória; fonte_mensagem permite usar uma fonte menor quando o texto for mais longo.
    if fonte_mensagem is None:  # Usa a fonte padrão quando nenhuma for especificada.
        fonte_mensagem = fonte_normal  # Mantém o tamanho de sempre para as mensagens curtas (casa especial e vitória).
    pygame.draw.rect(janela, cor_sombra, (largura_janela // 2 - 332, 213, 680, 250))  # Desenha a sombra da caixa centralizada.
    pygame.draw.rect(janela, cor_branca, (largura_janela // 2 - 340, 205, 680, 250))  # Desenha a caixa sobre o tabuleiro.
    pygame.draw.rect(janela, cor_texto, (largura_janela // 2 - 340, 205, 680, 250), 3)  # Desenha o contorno da caixa.
    desenha_texto_centralizado(titulo, fonte_caixa_titulo, cor_texto, largura_janela // 2, 235)  # Centraliza o título, em fonte própria para caber na caixa mais estreita.
    desenha_texto_centralizado(mensagem, fonte_mensagem, cor_texto, largura_janela // 2, 300)  # Centraliza o aviso.
    pygame.draw.rect(janela, cores_casas[1], botao_confirmar)  # Desenha o botão de confirmação.
    pygame.draw.rect(janela, cor_texto, botao_confirmar, 2)  # Contorna o botão.
    desenha_texto_centralizado(texto_botao, fonte_normal, cor_texto, botao_confirmar.centerx, botao_confirmar.centery - fonte_normal.get_height() // 2)  # Centraliza o texto no meio do botão verde.
    if texto_botao != 'Começar':  # Remove a explicação redundante apenas nas telas de preparação do desafio.
        desenha_texto_centralizado('Clique no botão ou pressione Enter.', fonte_pequena, cor_texto, largura_janela // 2, 430)  # Explica os dois controles.


def cria_confetes(quantidade):  # Cria as partículas de confete mostradas atrás da caixa de vitória.
    lista = []  # Guarda cada confete criado.
    for _ in range(quantidade):  # Repete para cada partícula pedida.
        lista.append({
            'x': random.uniform(0, largura_janela),  # Sorteia a posição horizontal inicial.
            'y': random.uniform(-altura_janela, 0),  # Começa acima da tela, em alturas variadas.
            'vx': random.uniform(-25, 25),  # Sorteia um leve desvio lateral.
            'vy': random.uniform(90, 180),  # Sorteia a velocidade de queda.
            'largura': random.uniform(6, 13),  # Sorteia a largura do retângulo.
            'altura': random.uniform(10, 18),  # Sorteia a altura do retângulo.
            'angulo': random.uniform(0, 360),  # Sorteia o ângulo inicial de rotação.
            'vangulo': random.uniform(-180, 180),  # Sorteia a velocidade de rotação.
            'cor': random.choice(cores_confete)  # Sorteia uma cor já usada no jogo.
        })
    return lista  # Devolve a lista pronta para ser animada.


def atualiza_confetes(confetes, segundos_passados):  # Move cada confete e o faz reaparecer no topo ao sair por baixo da tela.
    for confete in confetes:  # Percorre cada partícula.
        confete['y'] += confete['vy'] * segundos_passados  # Aplica a queda.
        confete['x'] += confete['vx'] * segundos_passados  # Aplica o desvio lateral.
        confete['angulo'] += confete['vangulo'] * segundos_passados  # Aplica a rotação.
        if confete['y'] > altura_janela + 20:  # Verifica se o confete já saiu por baixo da tela.
            confete['y'] = random.uniform(-40, -10)  # Faz reaparecer acima da tela.
            confete['x'] = random.uniform(0, largura_janela)  # Sorteia uma nova posição horizontal.


def desenha_confetes(confetes):  # Desenha cada confete como um pequeno retângulo girado.
    for confete in confetes:  # Percorre cada partícula.
        meia_largura = confete['largura'] / 2  # Calcula a metade da largura para centralizar o giro.
        meia_altura = confete['altura'] / 2  # Calcula a metade da altura para centralizar o giro.
        cantos = [(-meia_largura, -meia_altura), (meia_largura, -meia_altura), (meia_largura, meia_altura), (-meia_largura, meia_altura)]  # Define os quatro cantos do retângulo.
        radianos = math.radians(confete['angulo'])  # Converte o ângulo atual para radianos.
        cosseno = math.cos(radianos)  # Calcula o cosseno do ângulo.
        seno = math.sin(radianos)  # Calcula o seno do ângulo.
        pontos = [(confete['x'] + x * cosseno - y * seno, confete['y'] + x * seno + y * cosseno) for x, y in cantos]  # Gira e desloca cada canto.
        pygame.draw.polygon(janela, confete['cor'], pontos)  # Desenha o confete já girado.


def desenha_pontos(atividade):  # Recebe o desafio de pontos para desenhar suas conexões e seu progresso.
    for ligacao in atividade['ligacoes']:  # Percorre as conexões já concluídas.
        primeiro = atividade['pontos'][ligacao[0]]  # Consulta o ponto inicial da linha.
        segundo = atividade['pontos'][ligacao[1]]  # Consulta o ponto final da linha.
        pygame.draw.line(janela, primeiro['cor'], primeiro['centro'], segundo['centro'], 7)  # Desenha a conexão abaixo dos pontos.
    for indice in range(len(atividade['pontos'])):  # Percorre todos os pontos do desafio.
        ponto = atividade['pontos'][indice]  # Consulta a aparência e a posição do ponto.
        centro = ponto['centro']  # Guarda o centro para os desenhos seguintes.
        pygame.draw.circle(janela, cor_branca, centro, raio_ponto + 5)  # Separa o ponto das linhas que passam por ele.
        pygame.draw.circle(janela, ponto['cor'], centro, raio_ponto)  # Desenha o ponto colorido.
        pygame.draw.circle(janela, cor_texto, centro, raio_ponto, 2)  # Desenha o contorno do ponto.
        if indice == atividade['selecionado']:  # Verifica se esse é o primeiro ponto selecionado.
            pygame.draw.circle(janela, cor_texto, centro, raio_ponto + 5, 3)  # Destaca a seleção com um anel.
        if ponto['ligado']:  # Verifica se a conexão desse ponto está concluída.
            pygame.draw.line(janela, cor_branca, (centro[0] - 8, centro[1]), (centro[0] - 2, centro[1] + 6), 3)  # Desenha o começo do sinal de confirmação.
            pygame.draw.line(janela, cor_branca, (centro[0] - 2, centro[1] + 6), (centro[0] + 9, centro[1] - 7), 3)  # Completa o sinal de confirmação.
    desenha_texto_centralizado('Pares conectados: ' + str(len(atividade['ligacoes'])) + '/' + str(len(atividade['pontos']) // 2), fonte_normal, cor_texto, largura_janela // 2, 552)  # Mostra o progresso.


def desenha_pilhas(atividade):  # Recebe o desafio de blocos para desenhar todas as pilhas.
    for indice in range(len(atividade['pilhas'])):  # Percorre as pilhas na ordem em que aparecem na tela.
        pilha = atividade['pilhas'][indice]  # Consulta os blocos desta pilha, da base para o topo.
        area = atividade['areas_pilhas'][indice]  # Consulta o retângulo usado também para detectar cliques.
        cor_borda = cor_sombra  # Define a borda normal de uma pilha.
        if indice == atividade['selecionado']:  # Verifica se a pilha foi escolhida como origem.
            cor_borda = cor_texto  # Destaca a seleção com uma borda escura.
        pygame.draw.rect(janela, cor_fundo, area)  # Desenha o fundo da área clicável.
        pygame.draw.rect(janela, cor_borda, area, 4)  # Contorna a área da pilha.
        for nivel in range(capacidade_pilha):  # Desenha os dois espaços disponíveis nesta pilha.
            topo = area.bottom - 16 - (nivel + 1) * 86  # Calcula a altura do espaço a partir da base.
            espaco = pygame.Rect(area.x + 15, topo, area.width - 30, 78)  # Define o retângulo de um bloco.
            pygame.draw.rect(janela, cor_sombra, espaco, 2)  # Mostra o limite de um espaço vazio.
            if nivel < len(pilha):  # Verifica se existe um bloco ocupando esse nível.
                pygame.draw.rect(janela, pilha[nivel], espaco)  # Desenha a cor do bloco.
                pygame.draw.rect(janela, cor_texto, espaco, 2)  # Contorna o bloco para separar as peças.
    prontas = conta_pilhas_prontas(atividade['pilhas'])  # Conta as pilhas completas e de uma cor.
    desenha_texto_centralizado('Pilhas prontas: ' + str(prontas) + '/' + str(atividade['quantidade_cores']), fonte_normal, cor_texto, largura_janela // 2, 552)  # Mostra o progresso.



def quebra_texto(texto, fonte, largura_maxima):  # Divide uma frase em linhas que cabem na área de desenho.
    linhas = []  # Guarda as linhas já completas.
    linha_atual = ''  # Começa uma linha vazia.
    for palavra in texto.split():  # Acrescenta uma palavra de cada vez.
        tentativa = palavra  # Prepara a primeira palavra de uma linha.
        if linha_atual != '':  # Verifica se já existem palavras na linha.
            tentativa = linha_atual + ' ' + palavra  # Testa a inclusão da próxima palavra.
        if fonte.size(tentativa)[0] <= largura_maxima:  # Verifica se a linha ainda cabe na largura disponível.
            linha_atual = tentativa  # Mantém a palavra na mesma linha.
        else:  # Trata uma frase que precisa continuar em outra linha.
            linhas.append(linha_atual)  # Guarda a linha concluída.
            linha_atual = palavra  # Começa a próxima linha com a palavra que não coube.
    if linha_atual != '':  # Verifica se restou uma última linha.
        linhas.append(linha_atual)  # Acrescenta a última parte da frase.
    return linhas  # Entrega as linhas para serem desenhadas.


def desenha_resposta_digitada(atividade, agora):  # Recebe o desafio e o tempo para desenhar a pergunta, o campo e o cursor.
    frase = atividade['enunciado']  # Consulta a frase com a palavra faltando.
    if atividade['resultado'] == 'sucesso':  # Revela a resposta correta após o acerto.
        if atividade['tipo'] == 'calculo':  # Completa a igualdade matemática.
            frase = frase.replace('?', str(atividade['resposta']))
        elif atividade['tipo'] == 'enigma':  # Revela a solução somente após o acerto.
            frase = 'Resposta: ' + atividade['respostas'][0]  # Mostra a resposta por extenso.
        else:  # Completa a palavra do ditado.
            frase = frase.replace('______', atividade['respostas'][0])  # Mostra o ditado completo depois do acerto.
    fonte_da_frase = fonte_frase if atividade['tipo'] in ('ditado', 'enigma') else fonte_normal  # Usa a fonte maior própria do ditado e do enigma.
    linhas = quebra_texto(frase, fonte_da_frase, 620)  # Divide frases longas para evitar que ultrapassem o quadro.
    for indice in range(len(linhas)):  # Percorre as linhas do ditado.
        desenha_texto_centralizado(linhas[indice], fonte_da_frase, cor_texto, largura_janela // 2, 220 + indice * 28)  # Centraliza cada linha.
    desenha_texto('Sua resposta:', fonte_pequena, cor_texto, campo_resposta.x, 325)  # Identifica o campo de digitação.
    pygame.draw.rect(janela, cor_fundo, campo_resposta)  # Desenha o fundo do campo.
    pygame.draw.rect(janela, cor_texto, campo_resposta, 2)  # Contorna o campo que já começa ativo.
    texto = atividade['texto_digitado']  # Consulta a resposta sem remover acentos ou maiúsculas da tela.
    desenha_texto(texto, fonte_normal, cor_texto, campo_resposta.x + 12, campo_resposta.y + 18)  # Mostra a palavra digitada.
    if atividade['resultado'] == '' and (agora // 500) % 2 == 0:  # Faz o cursor piscar enquanto a pessoa pode responder.
        esquerda_cursor = campo_resposta.x + 12 + fonte_normal.size(texto)[0]  # Coloca o cursor depois do último caractere.
        pygame.draw.line(janela, cor_texto, (esquerda_cursor, campo_resposta.y + 14), (esquerda_cursor, campo_resposta.y + 43), 2)  # Desenha o cursor.
    desenha_texto_centralizado('Backspace: Apagar  |  Enter: Confirmar', fonte_pequena, cor_texto, largura_janela // 2, 450)  # Explica os controles.
    objetivo = 'Complete com uma única palavra.'  # Define o objetivo dos ditados.
    fonte_objetivo = fonte_normal  # Usa a fonte normal do objetivo por padrão.
    if atividade['tipo'] == 'enigma':  # Explica o objetivo da quinta atividade.
        objetivo = 'Descubra a resposta a partir das pistas.'  # Cada enigma possui uma resposta curta.
    elif atividade['tipo'] == 'calculo':  # Explica o formato numérico.
        objetivo = 'Responda com um número inteiro. Use "-" para resultados negativos.'  # Corrige a gramática da instrução.
        fonte_objetivo = fonte_painel  # Reduz ainda mais a fonte apenas aqui para não colidir com o botão de desistir.
    desenha_texto_centralizado(objetivo, fonte_objetivo, cor_texto, largura_janela // 2, 552)  # Reforça o objetivo do desafio.


def desenha_relogio(centro_x, centro_y, raio, segundos, limite_ms, cor):  # Desenha um cronômetro circular simples, só com o círculo e o tempo centralizado.
    pygame.draw.circle(janela, cor_branca, (centro_x, centro_y), raio)  # Preenche o fundo branco do relógio.
    pygame.draw.circle(janela, cor_texto, (centro_x, centro_y), raio, 3)  # Contorna o círculo com uma borda simples, sem anel colorido.
    minutos = segundos // 60  # Separa os minutos para o formato do cronômetro.
    segundos_exibidos = segundos % 60  # Separa os segundos restantes depois dos minutos completos.
    texto_tempo = str(minutos) + ':' + str(segundos_exibidos).zfill(2)  # Monta o texto no formato minuto:segundo.
    desenha_texto_centralizado(texto_tempo, fonte_relogio, cor, centro_x, centro_y - fonte_relogio.get_height() // 2)  # Mostra o tempo em negrito, centralizado dentro do círculo.


def desenha_atividade(partida, agora):  # Recebe a partida e o tempo atual para desenhar o desafio.
    atividade = partida['atividade']  # Consulta os dados e o resultado do desafio atual.
    jogador = partida['jogadores'][partida['jogador_atual']]  # Identifica quem deve resolver o desafio.
    tempo = calcula_tempo_restante(atividade, agora)  # Calcula os segundos disponíveis.
    if atividade['resultado'] != '':  # Verifica se o desafio já terminou.
        tempo = atividade['tempo_final']  # Mantém o tempo congelado durante a mensagem final.
    cor_cronometro = cor_texto  # Define a cor normal do cronômetro.
    if tempo <= 5:  # Destaca os últimos cinco segundos.
        cor_cronometro = cor_sair  # Muda o cronômetro para vermelho.
    desenha_texto(jogador['nome'], fonte_jogador, jogador['cor'], 35, 35)  # Mostra o participante da vez, em fonte maior.
    titulo = 'CONECTE AS CORES'  # Prepara o título da atividade de pontos.
    instrucao = 'Clique em dois pontos da mesma cor para conectá-los.'  # Explica os cliques nos pontos.
    regra = 'Complete todos os pares. As linhas podem se cruzar.'  # Explica a vitória nos pontos.
    if atividade['tipo'] == 'blocos':  # Ajusta as instruções para a atividade de blocos.
        titulo = 'ORGANIZE OS BLOCOS'  # Prepara o título do novo desafio.
        instrucao = 'Clique na pilha de origem e depois na pilha de destino.'  # Explica os dois cliques.
        regra = ''  # Remove a frase de regras desta tela, a pedido.
    elif atividade['tipo'] == 'ditado':  # Ajusta o cabeçalho para o desafio de texto.
        titulo = 'COMPLETE O DITADO'  # Define o título do novo desafio.
        instrucao = 'Digite a palavra que falta e pressione Enter.'  # Explica a confirmação.
        regra = 'Maiúsculas e acentos não alteram a resposta.'  # Explica as variações aceitas.
    elif atividade['tipo'] == 'enigma':  # Ajusta o cabeçalho da quinta atividade.
        titulo = 'DECIFRE O ENIGMA'  # Identifica o desafio de adivinhação.
        instrucao = 'Leia as pistas, digite a resposta e pressione Enter.'  # Explica a confirmação.
        regra = 'Maiúsculas e acentos não alteram a resposta.'  # Aceita diferentes grafias equivalentes.
    elif atividade['tipo'] == 'calculo':  # Ajusta o cabeçalho das contas.
        titulo = 'CÁLCULO MATEMÁTICO'  # Identifica a quarta atividade.
        instrucao = 'Resolva a conta, digite o resultado e pressione Enter.'  # Explica o controle.
        regra = 'Divisões exatas. Multiplicações e divisões podem ter negativos.'  # Evita dúvidas sobre o formato.
    desenha_texto('Nível ' + str(atividade['nivel']), fonte_nivel, cor_texto, 35, 82)  # Mostra a dificuldade atual, mais afastada do nome e em fonte maior.
    desenha_texto_centralizado(titulo, fonte_titulo_jogo, cor_texto, largura_janela // 2, 35)  # Apresenta o desafio atual, mais grande e um pouco mais para baixo.
    desenha_relogio(largura_janela - 82, 65, 52, tempo, atividade['limite'], cor_cronometro)  # Mostra o cronômetro circular bem maior, mais à direita.
    desenha_texto_centralizado(instrucao, fonte_instrucao, cor_texto, largura_janela // 2, 128)  # Explica o controle, numa fonte um pouco menor, próxima da caixa do jogo.
    pygame.draw.rect(janela, cor_branca, (largura_janela // 2 - 340, 170, 680, 365))  # Desenha a área principal da atividade.
    pygame.draw.rect(janela, cor_preta, (largura_janela // 2 - 340, 170, 680, 365), 3)  # Contorna a área do desafio com borda preta, como no painel.
    if atividade['tipo'] == 'pontos':  # Escolhe os desenhos do desafio de pontos.
        desenha_pontos(atividade)  # Mostra círculos, conexões e contagem de pares.
    elif atividade['tipo'] == 'blocos':  # Escolhe os desenhos do desafio de blocos.
        desenha_pilhas(atividade)  # Mostra as pilhas e sua organização.
    elif atividade['tipo'] in ['ditado', 'calculo', 'enigma']:  # Escolhe a tela com campo de resposta.
        desenha_resposta_digitada(atividade, agora)  # Mostra o enunciado, a resposta e o cursor.
    if atividade['resultado'] == '':  # Mantém o botão de desistência somente durante o desafio.
        pygame.draw.rect(janela, cor_painel, botao_desistir)  # Desenha o fundo do botão.
        pygame.draw.rect(janela, cor_texto, botao_desistir, 2)  # Contorna o botão de desistência.
        desenha_texto_centralizado('Desistir', fonte_pequena, cor_texto, botao_desistir.centerx, botao_desistir.centery - fonte_pequena.get_height() // 2)  # Centraliza a palavra dentro do botão.


def desenha_botao_sair():  # Desenha uma saída permanente em todas as telas.
    pygame.draw.rect(janela, cor_sair, botao_sair)  # Cria o bloco vermelho afastado das margens.
    pygame.draw.rect(janela, cor_texto, botao_sair, 2)  # Contorna o bloco para destacá-lo.
    desenha_texto_centralizado('Sair', fonte_pequena, cor_branca, botao_sair.centerx, botao_sair.centery - fonte_pequena.get_height() // 2)  # Centraliza o comando de saída dentro do botão.


# ----- Define os quadros da animação do personagem
# Cada tupla contém esquerda, topo, largura e altura de uma parte, em pixels relativos à peça.
# A ordem das partes é sempre: cabeça, tronco, dois segmentos do braço esquerdo,
# dois segmentos do braço direito, coxa e pé esquerdos, coxa e pé direitos.
pose_parada = [  # Mantém exatamente a silhueta original de vinte e quatro por trinta e dois pixels.
    (4, 0, 16, 12),  # Posiciona a cabeça.
    (4, 12, 16, 12),  # Posiciona o tronco.
    (0, 12, 4, 4), (0, 16, 4, 4),  # Mantém o braço esquerdo junto ao corpo.
    (20, 12, 4, 4), (20, 16, 4, 4),  # Mantém o braço direito junto ao corpo.
    (4, 24, 6, 4), (4, 28, 6, 4),  # Mantém a perna esquerda esticada.
    (14, 24, 6, 4), (14, 28, 6, 4)  # Mantém a perna direita esticada.
]
pose_agachada = [  # Abaixa o corpo antes do impulso e amortece a chegada ao chão.
    (4, 3, 16, 12),  # Abaixa a cabeça três pixels.
    (4, 15, 16, 10),  # Abaixa o tronco e reduz sua altura.
    (0, 15, 4, 4), (0, 19, 4, 6),  # Abaixa o braço esquerdo para preparar o impulso.
    (20, 15, 4, 4), (20, 19, 4, 6),  # Abaixa o braço direito para preparar o impulso.
    (4, 25, 7, 3), (2, 28, 9, 4),  # Flexiona a perna esquerda mantendo o pé no chão.
    (13, 25, 7, 3), (13, 28, 9, 4)  # Flexiona a perna direita mantendo o pé no chão.
]
pose_subida = [  # Abre os membros durante o impulso, inspirando-se na postura de salto da referência.
    (4, 0, 16, 12),  # Mantém a cabeça acima do tronco.
    (4, 12, 16, 12),  # Estica o tronco durante o salto.
    (0, 13, 4, 4), (-4, 13, 4, 4),  # Estende o braço esquerdo para trás.
    (20, 8, 4, 8), (20, 2, 4, 7),  # Levanta o braço direito ao lado da cabeça.
    (2, 24, 8, 4), (-1, 28, 7, 4),  # Estica uma perna para trás e para baixo.
    (14, 22, 9, 4), (21, 17, 4, 9)  # Dobra a outra perna para a frente, com o pé levantado.
]
pose_descida = [  # Começa a recolher os membros para preparar a aterrissagem.
    (4, 0, 16, 12),  # Mantém a cabeça na altura normal da peça.
    (4, 12, 16, 12),  # Mantém o tronco esticado.
    (0, 14, 4, 4), (-3, 17, 4, 4),  # Recolhe parcialmente o braço de trás.
    (20, 10, 4, 7), (20, 6, 4, 5),  # Começa a baixar o braço levantado.
    (3, 24, 7, 4), (1, 28, 8, 4),  # Aproxima a perna de trás da posição de apoio.
    (14, 23, 8, 4), (20, 21, 4, 7)  # Abaixa o pé da frente sem esticar a perna de uma vez.
]
quadros_personagem = [pose_parada, pose_agachada, pose_subida, pose_descida, pose_agachada, pose_parada]  # Define a sequência completa de preparação, salto e chegada.
instantes_poses = [0, 0.15, 0.40, 0.65, 0.85, 1]  # Define em que fração do salto cada pose é alcançada.

# ----- Inicia estruturas de dados
casas = cria_casas()  # Guarda as vinte casas nas mesmas posições da Etapa 2.
atividades_disponiveis = ['pontos', 'blocos', 'ditado', 'calculo', 'enigma']  # Mantém apenas os jogos já implementados; deve conter pelo menos dois tipos diferentes.
# As cinco atividades participam do sorteio; a última apresentada fica excluída da próxima escolha.
# A escolha exclui a última atividade da partida, incluindo entre jogadores e após casas especiais.
ditados = [  # Guarda doze frases com uma palavra faltando e suas respostas aceitas.
    {'enunciado': 'Quem não arrisca, não ______.', 'respostas': ['petisca']},  # Ditado sobre tentar.
    {'enunciado': 'Água mole em pedra dura, tanto bate até que ______.', 'respostas': ['fura']},  # Ditado sobre persistência.
    {'enunciado': 'Mais vale um pássaro na mão do que dois ______.', 'respostas': ['voando']},  # Ditado sobre valorizar o que se tem.
    {'enunciado': 'De grão em grão, a galinha enche o ______.', 'respostas': ['papo']},  # Ditado sobre pequenas conquistas.
    {'enunciado': 'Quem espera sempre ______.', 'respostas': ['alcança']},  # Ditado com uma resposta acentuada.
    {'enunciado': 'Nem tudo que reluz é ______.', 'respostas': ['ouro']},  # Ditado sobre aparências.
    {'enunciado': 'Casa de ferreiro, espeto de ______.', 'respostas': ['pau']},  # Ditado sobre uma situação contraditória.
    {'enunciado': 'Em terra de cego, quem tem um olho é ______.', 'respostas': ['rei']},  # Ditado sobre uma vantagem relativa.
    {'enunciado': 'Cavalo dado não se olha os ______.', 'respostas': ['dentes']},  # Ditado sobre presentes.
    {'enunciado': 'Filho de peixe, peixinho ______.', 'respostas': ['é']},  # Ditado sobre semelhanças entre pais e filhos.
    {'enunciado': 'Quem semeia vento colhe ______.', 'respostas': ['tempestade']},  # Ditado sobre consequências.
    {'enunciado': 'Antes tarde do que ______.', 'respostas': ['nunca']}  # Ditado sobre fazer algo mesmo com atraso.
]
enigmas = [  # Perguntas curtas para permitir a leitura e a digitação também nas faixas de dez segundos.
    {'enunciado': 'Tenho dentes, não mordo e desembaraço cabelos. O que sou?', 'respostas': ['pente']},  # Objeto usado para pentear.
    {'enunciado': 'Quanto mais seco seu corpo, mais molhada fico. O que sou?', 'respostas': ['toalha']},  # Objeto usado após o banho.
    {'enunciado': 'Sou uma abertura no chão: quanto mais terra tiram de mim, maior fico. O que sou?', 'respostas': ['buraco']},  # Espaço criado ao cavar.
    {'enunciado': 'Acompanho seu corpo na luz, mas não tenho corpo próprio. O que sou?', 'respostas': ['sombra']},  # Silhueta produzida pela luz.
    {'enunciado': 'Tenho ponteiros e marco as horas. O que sou?', 'respostas': ['relógio']},  # Objeto que indica a hora.
    {'enunciado': 'Tenho capa e páginas, e guardo histórias. O que sou?', 'respostas': ['livro']},  # Objeto de leitura.
    {'enunciado': 'Tenho um olho por onde passa a linha e uma ponta para costurar. O que sou?', 'respostas': ['agulha']},  # Instrumento de costura.
    {'enunciado': 'Tenho gargalo e guardo líquidos. O que sou?', 'respostas': ['garrafa']},  # Recipiente para líquidos.
    {'enunciado': 'Sou cheia de furinhos, absorvo água e ajudo a lavar a louça. O que sou?', 'respostas': ['esponja']},  # Objeto de limpeza.
    {'enunciado': 'Mostro cidades, estradas e rios desenhados, mas não sou o lugar real. O que sou?', 'respostas': ['mapa']},  # Representação de lugares.
    {'enunciado': 'Tenho degraus para você subir ou descer. O que sou?', 'respostas': ['escada']},  # Estrutura com degraus.
    {'enunciado': 'Tenho camadas e faço seus olhos lacrimejarem quando me cortam na cozinha. O que sou?', 'respostas': ['cebola']}  # Alimento com camadas.
]
campo_resposta = pygame.Rect(largura_janela // 2 - 290, 355, 580, 60)  # Define a área do texto digitado.
limite_caracteres = 24  # Limita a resposta para manter o texto dentro do campo.
capacidade_pilha = 2  # Limita cada pilha a dois blocos.
partida = {}  # Aguarda a escolha do modo para receber os dados da partida.
retangulo_dado = pygame.Rect(810, 495, 120, 120)  # Define a área do dado.
botao_um_jogador = pygame.Rect(largura_janela // 2 - 150, 280, 300, 65)  # Centraliza a primeira opção do menu.
botao_dois_jogadores = pygame.Rect(largura_janela // 2 - 150, 370, 300, 65)  # Centraliza a segunda opção do menu.
botao_confirmar = pygame.Rect(largura_janela // 2 - 140, 365, 280, 55)  # Centraliza o botão das caixas de aviso, já largo o suficiente para caber "Jogar novamente".
botao_confirmar_nome = pygame.Rect(565, 390, 200, 50)  # Posiciona o botão de confirmação centralizado dentro da caixa branca (caixa vai de x=430 até x=900, centro em x=665).
campo_nome = pygame.Rect(460, 260, 410, 60)  # Define a área do campo de texto na tela de nome.
botao_sair = pygame.Rect(20, janela.get_height() - 40, 80, 26)  # Posiciona a saída a vinte pixels da esquerda e dezesseis do fundo, em tamanho reduzido.
botao_desistir = pygame.Rect(largura_janela - 150, 550, 120, 42)  # Permite abandonar apenas a atividade atual.
raio_ponto = 24  # Define o tamanho visual e a área clicável de cada ponto.
intervalo_passo = 600  # Reserva seis décimos de segundo para preparar, executar e terminar cada salto.
altura_salto = 24  # Define a altura máxima do pequeno pulo, em pixels.
duracao_giro_dado = 700  # Reserva 700 milissegundos para a rotação vertical do dado.
duracao_resultado = 900  # Exibe o fim do turno por 900 milissegundos.
estado = 'menu'  # Começa na escolha da quantidade de pessoas.
jogo_ativo = True  # Mantém o loop principal em funcionamento.
relogio = pygame.time.Clock()  # Limita a velocidade de atualização da janela.
confetes = []  # Guarda as partículas de confete da tela de vitória.
nome_digitado = ''  # Guarda o nome sendo digitado antes de começar o tabuleiro.
indice_jogador_nome = 0  # Indica de qual jogador é a vez de digitar o nome.
limite_nome_caracteres = 14  # Limita o nome do jogador para não estourar o painel.

# ===== Loop principal =====
while jogo_ativo:  # Mantém eventos, lógica e saídas em um único loop.
    # ----- Prepara os pedidos deste frame
    pedido_inicio = 0  # Guarda uma escolha de um ou dois jogadores; zero significa nenhuma.
    pedido_dado = False  # Guarda se houve clique válido no dado neste frame.
    pedido_confirmacao = False  # Guarda a confirmação do aviso ou o pedido de jogar novamente.

    cliques_atividade = []  # Guarda os cliques recebidos no desafio deste frame.
    pedido_desistir = False  # Guarda se a pessoa escolheu abandonar o desafio.
    acoes_texto = []  # Guarda digitação, apagamentos e confirmações na ordem dos eventos deste frame.

    # ----- Trata eventos
    for evento in pygame.event.get():  # Recebe os eventos pendentes da janela.
        if evento.type == pygame.QUIT:  # Verifica se a janela deve ser fechada.
            jogo_ativo = False  # Solicita o encerramento sem processar novos movimentos.
        elif evento.type == pygame.MOUSEBUTTONDOWN:  # Verifica se houve clique do mouse.
            if evento.button == 1:  # Aceita apenas o botão esquerdo.
                posicao_mouse = evento.pos  # Usa diretamente as coordenadas do clique na janela original.
                if botao_sair.collidepoint(posicao_mouse):  # Verifica a saída antes dos controles de qualquer tela.
                    jogo_ativo = False  # Encerra o jogo mesmo durante uma animação ou um aviso.
                elif estado == 'menu':  # Trata as opções da tela inicial.
                    if pedido_inicio == 0:  # Aceita somente a primeira escolha deste frame.
                        if botao_um_jogador.collidepoint(posicao_mouse):  # Verifica a opção individual.
                            pedido_inicio = 1  # Solicita uma partida com uma pessoa.
                        elif botao_dois_jogadores.collidepoint(posicao_mouse):  # Verifica a opção em dupla.
                            pedido_inicio = 2  # Solicita uma partida com duas pessoas.
                elif estado == 'tabuleiro':  # Permite lançar somente quando não existe outra ação em andamento.
                    if retangulo_dado.collidepoint(posicao_mouse):  # Confere a área clicável do dado.
                        pedido_dado = True  # Registra um único pedido, mesmo com vários cliques no frame.
                elif estado == 'atividade':  # Recebe os controles da atividade atual.
                    if botao_desistir.collidepoint(posicao_mouse):  # Verifica a desistência da atividade.
                        pedido_desistir = True  # Solicita a penalidade e o encerramento do turno.
                    else:  # Guarda os outros cliques para as atividades que usam o mouse.
                        cliques_atividade.append(posicao_mouse)  # Mantém a ordem dos cliques recebidos.
                elif estado in ['aviso', 'fim', 'aviso_atividade']:  # Trata somente o botão da caixa aberta.
                    if botao_confirmar.collidepoint(posicao_mouse):  # Verifica se o botão foi atingido.
                        pedido_confirmacao = True  # Solicita a ação do botão: continuar ou jogar novamente.
                elif estado == 'digitando_nome':  # Trata o botão da tela de nome.
                    if botao_confirmar_nome.collidepoint(posicao_mouse):  # Verifica se o botão de confirmar foi atingido.
                        pedido_confirmacao = True  # Solicita a confirmação do nome digitado.
        elif evento.type == pygame.TEXTINPUT:  # Recebe caracteres já compostos pelo teclado, incluindo acentos.
            if estado == 'atividade':  # Aceita texto somente durante um desafio ativo.
                if partida['atividade']['tipo'] in ['ditado', 'calculo', 'enigma']:  # Verifica se o desafio atual possui campo de resposta.
                    acoes_texto.append(('digitar', evento.text))  # Guarda as letras sem duplicá-las no evento KEYDOWN.
            elif estado == 'digitando_nome':  # Aceita texto enquanto o nome está sendo escolhido.
                if len(nome_digitado) < limite_nome_caracteres:  # Respeita o limite de catorze caracteres.
                    nome_digitado += evento.text  # Acrescenta o caractere digitado, incluindo espaços e acentos.
        elif evento.type == pygame.KEYDOWN:  # Verifica o pressionamento de uma tecla.
            if evento.key == pygame.K_ESCAPE:  # Reconhece Esc em qualquer estado do jogo.
                jogo_ativo = False  # Solicita o fechamento da janela em tela cheia.
            elif evento.key == pygame.K_RETURN:  # Reconhece a tecla Enter.
                if estado in ['aviso', 'fim', 'aviso_atividade', 'digitando_nome']:  # Aceita Enter nas caixas e na tela de nome.
                    pedido_confirmacao = True  # Faz o mesmo que clicar no botão.
                elif estado == 'atividade':  # Verifica se Enter deve confirmar uma resposta.
                    if partida['atividade']['tipo'] in ['ditado', 'calculo', 'enigma']:  # Restringe a confirmação ao desafio de texto.
                        acoes_texto.append(('confirmar', ''))  # Registra a confirmação depois dos caracteres anteriores.
            elif evento.key == pygame.K_BACKSPACE:  # Reconhece a tecla de apagar.
                if estado == 'atividade':  # Permite editar somente uma atividade em andamento.
                    if partida['atividade']['tipo'] in ['ditado', 'calculo', 'enigma']:  # Restringe a edição ao desafio de texto.
                        acoes_texto.append(('apagar', ''))  # Solicita a remoção do último caractere.
                elif estado == 'digitando_nome':  # Permite apagar enquanto o nome está sendo escolhido.
                    nome_digitado = nome_digitado[:-1]  # Remove o último caractere digitado.

    # ----- Atualiza a lógica do jogo
    if jogo_ativo:  # Evita atualizar os dados após um pedido de fechamento.
        agora = pygame.time.get_ticks()  # Consulta o tempo transcorrido desde a inicialização.
        if estado == 'menu':  # Prepara a partida depois da escolha.
            if pedido_inicio != 0:  # Verifica se uma quantidade foi selecionada.
                partida = cria_partida(pedido_inicio)  # Cria participantes e sorteia efeitos escondidos.
                indice_jogador_nome = 0  # Começa perguntando o nome do primeiro jogador.
                nome_digitado = ''  # Garante que o campo comece vazio.
                pygame.key.set_text_input_rect(campo_nome)  # Informa onde fica o campo de nome.
                pygame.key.start_text_input()  # Começa a receber texto já na tela de nome.
                estado = 'digitando_nome'  # Pergunta o nome antes de liberar o tabuleiro.
        elif estado == 'digitando_nome':  # Aguarda a confirmação do nome de um jogador.
            if pedido_confirmacao:  # Verifica se a pessoa confirmou o nome, mesmo em branco.
                if nome_digitado.strip() != '':  # Só substitui o nome padrão se algo foi digitado.
                    partida['jogadores'][indice_jogador_nome]['nome'] = nome_digitado  # Guarda o nome escolhido.
                indice_jogador_nome += 1  # Passa para o próximo jogador, se houver.
                nome_digitado = ''  # Limpa o campo para o próximo nome.
                if indice_jogador_nome >= len(partida['jogadores']):  # Verifica se todos os nomes já foram pedidos.
                    pygame.key.stop_text_input()  # Encerra a captura de texto da tela de nome.
                    estado = 'tabuleiro'  # Libera o primeiro lançamento.
        elif estado == 'tabuleiro':  # Aguarda um lançamento do participante da vez.
            if pedido_dado:  # Verifica o pedido recebido nos eventos.
                partida['proximo_valor_dado'] = rola_dado()  # Sorteia uma única vez um resultado entre um e quatro.
                partida['inicio_giro_dado'] = agora  # Registra o início da rotação.
                partida['mensagem'] = 'Aguarde o giro...'  # Mantém o resultado pendente durante a animação.
                estado = 'rolando_dado'  # Bloqueia novos lançamentos até terminar o giro.
        elif estado == 'rolando_dado':  # Aguarda a animação do dado sem pausar os eventos.
            if agora - partida['inicio_giro_dado'] >= duracao_giro_dado:  # Verifica se a nova face já chegou à frente.
                partida['valor_dado'] = partida['proximo_valor_dado']  # Confirma o número que foi sorteado no começo do giro.
                partida['mensagem'] = 'Dado: ' + str(partida['valor_dado'])  # Mostra o resultado definitivo.
                inicia_movimento(partida, partida['valor_dado'], 'dado', agora)  # Prepara o primeiro salto da peça.
                estado = 'movimento'  # Só começa a locomoção depois de o dado parar.
        elif estado == 'movimento':  # Executa os passos sem pausar o programa.
            if atualiza_movimento(partida, agora):  # Verifica se a peça terminou de andar.
                estado = resolve_parada(partida, agora)  # Decide entre aviso, fim do turno ou vitória.
                if estado == 'fim':  # Verifica se essa parada foi a chegada.
                    confetes = cria_confetes(90)  # Cria a chuva de confetes para a tela de vitória.
                    toca_som(som_vitoria)  # Toca o som de vitória uma única vez.
        elif estado == 'aviso':  # Mantém o efeito pendente enquanto a caixa está aberta.
            if pedido_confirmacao:  # Verifica se a pessoa leu e fechou o aviso.
                estado = aplica_casa_especial(partida, agora)  # Revela a casa e aplica seu efeito.
        elif estado == 'aviso_atividade':  # Aguarda a confirmação sem mostrar o enunciado.
            if pedido_confirmacao:  # Recebe o botão Começar ou Enter.
                estado = inicia_atividade(partida, agora)  # Só agora começa a contar o prazo.
        elif estado == 'atividade':  # Atualiza cliques e prazo sem bloquear a janela.
            estado = atualiza_atividade(partida, cliques_atividade, acoes_texto, pedido_desistir, agora)  # Decide se o desafio continua ou acabou.
        elif estado == 'resultado_atividade':  # Exibe brevemente o desafio concluído ou a falha antes de voltar ao tabuleiro.
            if agora - partida['inicio_resultado'] >= duracao_resultado:  # Aguarda a leitura da mensagem.
                if partida['atividade']['resultado'] == 'sucesso':  # Verifica se o desafio foi resolvido.
                    troca_turno(partida)  # Passa a vez ou libera novamente o jogador individual.
                    estado = 'tabuleiro'  # Volta ao tabuleiro sem penalidade.
                else:  # Aplica a consequência do tempo esgotado ou da desistência.
                    inicia_movimento(partida, -1, 'penalidade', agora)  # Prepara um recuo de uma casa sem outro desafio no destino.
                    partida['mensagem'] = 'Voltando uma casa...'  # Explica o recuo no painel.
                    estado = 'movimento'  # Anima a penalidade antes de encerrar o turno.
        elif estado == 'resultado':  # Mantém a mensagem de fim do turno por um pequeno intervalo.
            if agora - partida['inicio_resultado'] >= duracao_resultado:  # Verifica se a espera terminou.
                troca_turno(partida)  # Alterna a pessoa ou mantém o jogador individual.
                estado = 'tabuleiro'  # Libera o dado para o novo turno.
        elif estado == 'fim':  # Mantém a partida encerrada após a chegada.
            if pedido_confirmacao:  # Verifica se a pessoa escolheu jogar novamente.
                partida = {}  # Só ao jogar novamente descarta as casas reveladas da partida encerrada.
                estado = 'menu'  # Volta à escolha de participantes sem fechar a janela.

        # ----- Gera saídas
        if jogo_ativo:  # Desenha somente enquanto a janela deve permanecer aberta.
            if estado == 'menu':  # Verifica se ainda está na tela inicial, antes de a partida começar.
                toca_musica(caminho_recurso('assets/sons/musica_tabuleiro.wav'))  # Toca a música do tabuleiro apenas na tela inicial.
            else:  # Cobre a digitação do nome, o tabuleiro e os cinco desafios.
                toca_musica(caminho_recurso('assets/sons/musica_desafio.wav'))  # Toca a música do desafio durante todo o restante do jogo.
            if estado == 'menu':  # Verifica se a escolha de participantes deve aparecer.
                janela.fill(cor_fundo_cinza)  # Usa o fundo cinza na tela inicial.
                desenha_menu()  # Mostra os botões do menu.
            elif estado == 'digitando_nome':  # Verifica se a tela de nome deve aparecer.
                janela.fill(cor_fundo_cinza)  # Usa o fundo cinza na tela de nome.
                desenha_tela_nome(partida, indice_jogador_nome, nome_digitado, agora)  # Mostra o bonequinho e o campo de digitação.
            elif estado == 'aviso_atividade':  # Exibe somente o aviso, sem revelar a resposta ou a pergunta.
                janela.fill(cor_fundo_cinza)  # Usa o fundo cinza na tela de desafio.
                tempo_aviso = partida['atividade']['limite'] // 1000  # Consulta o prazo real desta faixa.
                mensagem_aviso = 'Você possui apenas ' + str(tempo_aviso) + ' segundos para concluir o desafio.'  # Dá destaque ao prazo.
                titulo_aviso = 'PREPARE-SE PARA O DITADO'  # Identifica o desafio que será iniciado.
                if partida['atividade']['tipo'] == 'enigma':  # Distingue as duas atividades com aviso.
                    titulo_aviso = 'PREPARE-SE PARA O ENIGMA'  # Não revela a pergunta antes de começar.
                desenha_caixa(titulo_aviso, mensagem_aviso, 'Começar', fonte_aviso_atividade)  # Aguarda uma ação voluntária, com fonte menor para o aviso caber na caixa.
                desenha_texto_centralizado('O tempo começa ao clicar em Começar ou pressionar Enter.', fonte_pequena, cor_texto, largura_janela // 2, 475)  # Explica quando começa a contagem.
            elif estado == 'atividade' or estado == 'resultado_atividade':  # Verifica se a atividade ou seu resultado deve aparecer.
                janela.fill(cor_fundo_cinza)  # Usa o fundo cinza na tela de desafio.
                desenha_atividade(partida, agora)  # Desenha a atividade atual e seu cronômetro.
            else:  # Desenha o tabuleiro nos demais estados.
                janela.fill(cor_fundo_cinza)  # Usa o fundo cinza na tela do tabuleiro.
                desenha_texto('TRILHA DOS DESAFIOS', fonte_titulo, cor_texto, 35, 25)  # Mostra o título do tabuleiro.
                desenha_texto('Avance pelo tabuleiro e supere cada desafio!', fonte_subtitulo, cor_texto, 37, 85)  # Mostra o subtítulo divertido, alinhado ao título, agora maior.
                desenha_tabuleiro(partida)  # Mostra casas comuns e efeitos já revelados.
                desenha_pecas(partida, estado, agora)  # Mostra as peças nas posições atuais.
                desenha_painel(partida, estado, agora)  # Mostra o participante da vez e as instruções.
                if estado == 'aviso':  # Verifica se há uma casa especial aguardando confirmação.
                    desenha_caixa('CASA ESPECIAL', partida['mensagem_aviso'], 'Continuar')  # Sobrepõe o aviso.
                elif estado == 'fim':  # Verifica se alguém alcançou a última casa.
                    atualiza_confetes(confetes, 1 / 60)  # Anima a queda dos confetes a cada frame.
                    desenha_confetes(confetes)  # Desenha os confetes atrás da caixa de vitória.
                    desenha_caixa('CHEGADA!', partida['vencedor'] + ' venceu!', 'Jogar novamente')  # Mostra a vitória e permite começar outra partida.
            desenha_botao_sair()  # Mantém a saída visível por cima de qualquer tela ou caixa.
            pygame.display.update()  # Apresenta o frame completo na janela.
            relogio.tick(60)  # Limita o loop a sessenta atualizações por segundo.

# ===== Finalização =====
pygame.quit()  # Libera os recursos do pygame e fecha a janela.