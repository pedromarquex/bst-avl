from tkinter import *
import pygame
import os

White = 255, 255, 255
Black = 0, 0, 0
Red = 255, 0, 0
Blue = 0, 0, 255
Green = 0, 0, 255
Cyan = 0, 180, 105
Gray = 190, 190, 190

RAIZ = False
nodes = []
fatores = []
localizado = " "
removerOk = 0
tree_print = ''

XDMI = 800
YDMI = 600


class Node:
    def __init__(self, chave=None, dados=None):
        if chave is not None:
            self.chave = str(chave)
        else:
            self.chave = chave
        self.dados = dados
        self.filhos(None, None)
        self.posicao = (None, None)
        self.nivel = None

    def filhos(self, esquerda, direita):  # privado
        self.esquerda = esquerda
        self.direita = direita

    def FB(self):  # public
        alturaE = 0
        if self.esquerda is not None:
            alturaE = self.esquerda.altura()
        alturaD = 0
        if self.direita is not None:
            alturaD = self.direita.altura()
        return alturaD - alturaE

    def altura(self):  # privado
        # Calcula a altura dos lados da arvore (esquerdo ou direito)
        # entra recursivamente na arvore ate achar o fim. Sao duas variaveis sendo incrementadas.
        # Como o calculo da altura pode envolver lado oposto(no caso do esquerdo, se nao haver mais esquerdo, pode se procurar filho direito pra continuar calculando)
        # E no final eh retornado 1 + o que incrementou (que e o que realmente vale)
        alturaE = 0
        if self.esquerda:
            alturaE = self.esquerda.altura()
        alturaD = 0
        if self.direita:
            alturaD = self.direita.altura()
        return 1 + max(alturaE, alturaD)  # Retorna 1 + a mais incrementada

    def rot_E(self):  # privado
        # Realiza a operacao de rotacao simples a esquerda
        self.chave, self.direita.chave = self.direita.chave, self.chave  # atribuicao multipla: atribui respectivamente
        self.dados, self.direita.dados = self.direita.dados, self.dados
        old_esquerda = self.esquerda  # passa o no a direita pra uma variavel auxiliar
        self.filhos(self.direita, self.direita.direita)  # configura os filhos pro no
        self.esquerda.filhos(old_esquerda, self.esquerda.esquerda)  # configura os filhos pro no

    def rot_D(self):  # privado
        # Realiza a operacao de rotacao simples a direita
        self.chave, self.esquerda.chave = self.esquerda.chave, self.chave  # atribuicao multipla: atribui respectivamente
        self.dados, self.esquerda.dados = self.esquerda.dados, self.dados
        old_direita = self.direita  # passa o no a direita pra uma variavel auxiliar
        self.filhos(self.esquerda.esquerda, self.esquerda)  # configura os filhos pro no
        self.direita.filhos(self.direita.direita, old_direita)  # configura os filhos pro no

    def rot_dup_D(self):  # privado
        # Realiza a operacao de rotacao dupla a direita - reaproveita as funcoes anteriores
        self.esquerda.rot_E()  # Chama uma rotacao a esquerda
        self.rot_D()  # depois uma a direita (assim como eh feito manualmente)

    def rot_dup_E(self):  # privado
        # Realiza a operacao de rotacao dupla a esquerda - reaproveita as funcoes anteriores
        self.direita.rot_D()  # Chama uma rotacao a direita
        self.rot_E()  # depois uma a esquerda (assim como eh feito manualmente)

    def executaBalanco(self):  # privado
        # Executa o balanceamento de um no recem inserido. Usa os fatores de balanceamento, e as operacoes de rotacao
        bal = self.FB()  # bal recebe o fator de balanceamento do no na qual vai sofrer balanceamento
        if bal > 1:  # se for maior que um teremos uma operacao de rotacao (dupla) a esquerda
            if self.direita.FB() > 0:  # se caso o FB do no ah direita for maior que 0, sera uma rotacao simples
                self.rot_E()
            else:  # caso contrario, sera dupla
                self.rot_dup_E()
        elif bal < -1:  # se caso for menor que -1 teremos uma operacao de rotacao (dupla) a direita
            if self.esquerda.FB() < 0:  # se caso o FB do no ah esquerda for maior que 0, sera uma rotacao simples
                self.rot_D()
            else:  # caso contrario, sera dupla
                self.rot_dup_D()

    def insere(self, chave, dados):  # public
        # Realiza a insercao de um no com chave. Usa o __init__ e a a propria funcao recursivamente
        chave = str(chave)
        if chave < self.chave:  # Se a chave a ser inserida for menor que a chave atual, continua o algoritmo a esquerda ou insere a esquerda
            if not self.esquerda:
                self.esquerda = Node(chave, dados)
            else:
                self.esquerda.insere(chave, dados)
        elif chave > self.chave:  # Se a chave inserida for maior ou igual que a chave atual, continua o algoritmo a direita ou insere a direita
            if not self.direita:
                self.direita = Node(chave, dados)
            else:
                self.direita.insere(chave, dados)
        self.executaBalanco()  # Apos inserir executa o balanceamento do no inserido

    def localizar(self, chave, pai="-"):  # public
        global localizado
        global removerOk
        localizado = "Não Localizado!"
        removerOk = 0
        chave = str(chave)
        if chave < self.chave:  # se a chave procurada foi menor que a chave atual, vai pra esquerda, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave)  # guarda o pai pro caso de ser o proximo no o desejado
            if self.esquerda is not None:
                self.esquerda.localizar(chave, pai)
        elif chave > self.chave:  # se a chave procurada foi maior que a chave atual, vai pra direita, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave)  # guarda o pai pro caso de ser o proximo no o desejado
            if self.direita is not None:
                self.direita.localizar(chave, pai)
        elif chave == self.chave:  # Se chegar num caso de chave igual, eh porque encontramos. Assim printamos as informacoes
            filhoesq = " "
            filhodir = " "
            fb = " "
            if self.esquerda is not None:
                filhoesq = str(self.esquerda.chave)
            if self.direita is not None:
                filhodir = str(self.direita.chave)
            dados = str(self.dados)
            fb = self.FB()
            localizado = "{\'" + str(self.chave) + "\': [\'" + str(filhoesq) + "\', \'" + str(filhodir) + "]\', " + str(
                dados) + "}"
            # localizado = ('{' + str(self.chave) + '' + 'Pai: ' + str(pai) + '\nFilho da Esquerda: ' + str(
            #   filhoesq) + '\nFilho da Direita: ' + str(filhodir) + '\nFB: ' + str(self.FB()) + '}')
            removerOk = 1

    def localizar_fb(self, chave):
        global localizado_fb
        global removerOk
        localizado_fb = "Não Localizado!"
        removerOk = 0
        chave = str(chave)
        if chave < self.chave:  # se a chave procurada foi menor que a chave atual, vai pra esquerda, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave)  # guarda o pai pro caso de ser o proximo no o desejado
            if self.esquerda is not None:
                self.esquerda.localizar_fb(chave)
        elif chave > self.chave:  # se a chave procurada foi maior que a chave atual, vai pra direita, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave)  # guarda o pai pro caso de ser o proximo no o desejado
            if self.direita is not None:
                self.direita.localizar_fb(chave)
        elif chave == self.chave:  # Se chegar num caso de chave igual, eh porque encontramos. Assim printamos as informacoes
            fb = self.FB()
            localizado_fb = "{\'" + str(self.chave) + "\': [\'" + str(fb) + "\']}"
            removerOk = 1

    def remover(self, chave):  # public
        global RAIZ
        # avalia o caso especial de remocao e depois manda pra remocao
        # o caso especial é quando temos apenas dois nos, e a raiz deve ser excluida
        chave = str(chave)
        if chave == self.chave:
            if self.esquerda is None and self.direita is not None:
                # se tiver apenas a raiz e um no na direita
                self.chave = self.direita.chave
                self.dados = self.direita.dados
                self.filhos = self.direita.filhos
                self.direita = self.direita.direita
            elif self.direita is None and self.esquerda is not None:
                # se tiver apenas a raiz e um no na esquerda
                self.chave = self.esquerda.chave
                self.dados = self.esquerda.dados
                self.filhos = self.esquerda.filhos
                self.esquerda = self.esquerda.esquerda
            elif self.direita is None and self.esquerda is None:
                # se tiver restando apenas a raiz, ele troca a raiz por uma mensagem de arvore vazia
                self.__init__('Vazio')
                RAIZ = False
            else:
                # se nao for nenhum dos casos acima, faz a remocao com os outros casos no outro metodo
                # nesse caso, se o no a ser removido for uma raiz mas nao dos casos espciais acima
                self.remocao(chave)
        else:
            # qualquer outro no ou caso de remocao
            self.remocao(chave)

    def remocao(self, chave):  # privado
        # remocao de no folha ou no com apenas um filho, recursivamente. usa os retornos a cada recursao pra percorrer e substituir o no apagado
        chave = str(chave)
        if chave < self.chave:
            self.esquerda = self.esquerda.remocao(chave)
        elif chave > self.chave:
            self.direita = self.direita.remocao(chave)
        else:
            if self.direita is None:
                return self.esquerda
            if self.esquerda is None:
                return self.direita
            # remocao de no com dois filhos. substitui o no removido pelo menor no da subarvore da direita. tem dois metodos auxiliarres
            # o metodo menor busca o menor no da subarvore da direita. o metodo deletamenor deleta esse no, pois ele ja foi substiuir o no removido
            aux = self.direita.menor()
            self.chave = aux.chave
            self.dados = aux.dados
            self.direita = self.direita.deletamenor()
        return self

    def menor(self):  # privado
        # busca o menor no da subarvore direita do no removido
        if self.esquerda is None:
            return self
        else:
            return self.esquerda.menor()

    def deletamenor(self):  # privado
        # exclui o menor no da subarvore da direita, pois esse no foi substituir o no removido
        if self.esquerda is None:
            return self.direita
        self.esquerda = self.esquerda.deletamenor()
        return self

    def rebalanceamento(self):  # public
        # Apos uma remocao, este metodo busca nos com FBs maiores que um ou menores que -1 para realizar o balanceamento. Utiliza logica semelhante a da funcao
        # de rebalanceamento ao inserir um no
        if self.esquerda is not None:
            self.esquerda.rebalanceamento()
        bal = self.FB()  # bal recebe o FB do no acessado atualmente
        if bal > 1:
            # FBs>1 fazem rotacoes a esquerda
            if self.direita.direita is not None:
                # se o no da direita da direita existir, entao sera uma rotacao simples a esquerda
                print('Rebalanceamento: Rotacao a esquerda em ' + str(self.chave) + ' que tinha o FB ' + str(self.FB()))
                self.rot_E()
            else:
                # caso nao, sera dupla a esquerda
                print('Rebalanceamento: Rotacao dupla a esquerda em ' + str(self.chave) + ' que tinha o FB ' + str(
                    self.FB()))
                self.rot_dup_E()
        elif bal < -1:
            # FBs<-1 fazem rotacoes a direita
            if self.esquerda.esquerda is not None:
                # se o no da direita da direita existir, entao sera uma rotacao simples a direita
                print('Rebalanceamento: Rotacao a direita em ' + str(self.chave) + ' que tinha o FB ' + str(self.FB()))
                self.rot_D()
            else:
                # caso nao, sera dupla a direita
                print('\nRebalanceamento: Rotacao dupla a direita em \n' + str(self.chave) + ' que tinha o FB ' + str(
                    self.FB()))
                self.rot_dup_D()

        if self.direita is not None:
            self.direita.rebalanceamento()

    def get_value(self):
        dados = "[]"
        chave = " "
        filhoesq = " "
        filhodir = " "
        if self.esquerda is not None:
            filhoesq = str(self.esquerda.chave)
        if self.direita is not None:
            filhodir = str(self.direita.chave)
        if self.chave is not None:
            chave = self.chave
        if self.dados is not None:
            dados = self.dados
        return str('\'' + str(chave) +
                   '\': [\'' + str(filhoesq) +
                   '\', \'' + str(filhodir) +
                   '\', ' + str(dados) + ']')

    def set_printable(self):  # public
        global tree_print

        if self.esquerda is not None:
            self.esquerda.set_printable()
        if self.chave is not None:
            tree_print += self.get_value()
            tree_print += ', '
            # if self.esquerda is not None:
            #     tree_print += ', '
            # elif self.direita is not None:
            #     tree_print += ', '
            # else:
            #     pass
        if self.direita is not None:
            self.direita.set_printable()

    def imprime(self):
        global tree_print
        tree_print = ''
        data = ''
        self.set_printable()
        data = 'Dict_AVL = {' + tree_print + '}'
        return data

        # if self.esquerda:
        #     self.esquerda.imprime()
        # elif self.direita:
        #     self.direita.imprime()
        # else:
        #     filhoesq = " "
        #     filhodir = " "
        #     if self.esquerda is not None:
        #         filhoesq = str(self.esquerda.chave)
        #     if self.direita is not None:
        #         filhodir = str(self.direita.chave)
        #     dados = str(self.dados)
        #     # ['MA': ['ESQ', 'DIR', [DADOS]]]
        #     # data +=
        #     return data + str(
        #         '{\'' + str(self.chave) + '\': [\'' + str(filhoesq) + '\', \'' + str(filhodir) + '\', ' + str(
        #             dados) + ']}, ')

    def calculaNiveis(self, rootOk=0, nivelRoot=0):  # public
        # calcula os niveis dos nos pra ajudar no calculo da posicao
        # coloca dentro de cada no o seu nivel (ou nivel aproximado em alguns casos), apenas para auxiliar na orientacao da apresentacao grafica da arvore
        # note que os niveis comecam com 1 e nao representam o conceito de niveis. Isso e apenas o nome do metodo, que apenas auxilia a interface grafica.
        rootOk = rootOk + 1
        if rootOk == 1:
            # a altura toda da arvore e o nivel dela
            nivelRoot = self.altura()
        else:
            self.nivel = nivelRoot - self.altura() + 1
        if self.esquerda:
            self.esquerda.calculaNiveis(rootOk + 2, nivelRoot=nivelRoot)
        if self.direita:
            self.direita.calculaNiveis(rootOk + 2, nivelRoot=nivelRoot)

    def calcposicao(self, rootOk=0, posPai=[0, 0], lado=0):  # public
        rootOk = rootOk + 1
        node = ()
        if rootOk == 1:
            self.posicao = (XDMI, 100)
            node = (self.chave, self.posicao)
            nodes.append(node)
            fatores.append(self.FB())
        else:
            if lado == 1:
                aux = 2 ** self.nivel
                aux = aux // 2
                deslocamento = XDMI // aux
                self.posicao = [posPai[0] - deslocamento, posPai[1] + 100]
                node = (self.chave, self.posicao, posPai)
                nodes.append(node)
                fatores.append(self.FB())
            else:
                aux = 2 ** self.nivel
                aux = aux // 2
                deslocamento = XDMI // aux
                self.posicao = [posPai[0] + deslocamento, posPai[1] + 100]
                node = (self.chave, self.posicao, posPai)
                nodes.append(node)
                fatores.append(self.FB())

        if self.esquerda:
            self.esquerda.calcposicao(rootOk + 2, posPai=[self.posicao[0], self.posicao[1]], lado=1)
        if self.direita:
            self.direita.calcposicao(rootOk + 2, posPai=[self.posicao[0], self.posicao[1]], lado=2)
        # retorna o vetor de nos.

    def direct_acess(self, chave, index):
        global direct_a
        global removerOk
        localizado_dir = "Não Localizado!"
        removerOk = 0
        chave = str(chave)
        if chave < self.chave:  # se a chave procurada foi menor que a chave atual, vai pra esquerda, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave)  # guarda o pai pro caso de ser o proximo no o desejado
            if self.esquerda is not None:
                self.esquerda.direct_acess(chave, index)
        elif chave > self.chave:  # se a chave procurada foi maior que a chave atual, vai pra direita, recursivamente, salvando a chave atual no caso de este ser o pai do procurado
            pai = str(self.chave)  # guarda o pai pro caso de ser o proximo no o desejado
            if self.direita is not None:
                self.direita.direct_acess(chave, index)
        elif chave == self.chave:  # Se chegar num caso de chave igual, eh porque encontramos. Assim printamos as informacoes
            try:
                index = int(index)
                string = '\'' + str(self.dados[index]) + '\''
                # >>> RN[0]
                # >>> 'Rio'
                direct_a = string
            except:
                direct_a = str('erro ao acessar!')


tree = Node()


def get_file():
    with open('INPUT.txt') as file:
        return file.read()


def get_list(data):
    l_data = []
    data = data.replace(" ", "").replace("\n", "").strip("Dict_ALV=").strip("{").strip("}")
    data = data.strip("]").split("]")
    for i in range(len(data)):
        lista = data[i].strip(",").replace("\'", "").replace("[", "").replace("]", "").split(":")
        lista[0] = str(lista[0])
        lista[1] = lista[1].split(",")
        l_data.append(lista)
    return l_data


def file_button():
    global tree
    global RAIZ
    file = get_file()
    nos = get_list(file)

    for line in nos:
        if RAIZ is False:
            tree = Node(line[0], line[1])
            RAIZ = True
        else:
            tree.insere(line[0], line[1])

    notification = Tk()

    lb = Label(notification, text="Arquivo lido com sucesso!", width=30)
    lb.pack()
    bt = Button(notification, text="Ok", width=30, command=notification.destroy)
    bt.pack()

    notification.title("Info!")
    notification.geometry("300x50")


def manual_button():
    global Ed1
    ManualInsert = Tk()  # cria uma janela
    ManualInsert.title('Inserção Manual')  # seta o titulo da janela
    ManualInsert.geometry('300x200')  # seta o tamanho da janela
    Ed1 = Entry(ManualInsert, width=30, justify='center')  # cria uma entrada de texto
    Ed1.insert(0, '')  # seta o texto
    Ed1.pack()  # gerenciador de geometria
    Ed1.focus_set()  # obtm o foco para a entrada de texto
    insert_btn = Button(ManualInsert, text='Inserir', width=20, command=insert_btn_func)
    insert_btn.pack()


def insert_btn_func():
    notification = Tk()
    notification.title("Inserção")
    notification.geometry("300x50")
    global tree
    global RAIZ

    if not Ed1.get():  # [] entrada vazia
        label = Label(notification, text="Digite O Nó a ser inserido", height=0, width=100)
        btn = Button(notification, text="ok", width=20, command=notification.destroy)
        label.pack()
        btn.pack(side='bottom', padx=0, pady=0)
    else:
        try:
            raw = get_list(Ed1.get())  # recebe uma lista de listas a partir da string
            line = raw[0]  # atribui a posição 1 da lista para outra lista
            if tree.chave is not None:
                tree.insere(str(line[0]), line[1])
                label = Label(notification, text="Nó " + str(line[0]) + " inserido", height=0, width=100)
            else:
                tree = Node(str(line[0]), line[1])
                label = Label(notification, text="Nó " + str(line[0]) + " inserido", height=0, width=100)
                RAIZ = True

            btn = Button(notification, text="ok", width=20, command=notification.destroy)
            label.pack()
            btn.pack(side='bottom', padx=0, pady=0)
        except Exception:
            label = Label(notification, text='ERRO! Utilizar notação de dicionários.')
            btn = Button(notification, text="OK", width=30, command=notification.destroy)
            label.pack()
            btn.pack(side='bottom', padx=0, pady=0)


def remove_button():
    global Ed1
    remover = Tk()  # cria uma janela
    remover.title('Remover')  # seta o titulo da janela
    remover.geometry('300x200')  # seta o tamanho da janela
    Ed1 = Entry(remover, width=25, justify='center')  # cria uma entrada de texto
    Ed1.insert(0, '')  # seta o texto
    Ed1.pack()  # gerenciador de geometria
    Ed1.focus_set()  # obtm o foco para a entrada de texto
    remove_btn = Button(remover, text='Remover Nó', width=20, command=remove_btn_func)
    remove_btn.pack()


def remove_btn_func():
    global tree
    global RAIZ

    if not Ed1.get():  # [] entrada vazia
        notify2 = Tk()
        notify2.title("Remover!")
        notify2.geometry("300x50")
        resultado = Label(notify2, text='Digite um nó.')
        resultado.pack()
        b = Button(notify2, text="ok", width=20, command=notify2.destroy)
        b.pack()
        b.pack(side='bottom', padx=0, pady=0)
    else:
        if RAIZ is False:
            vazia = Tk()
            vazia.title("Remover!")
            vazia.geometry("300x50")
            resultado = Label(vazia, text='Árvore vazia.')
            resultado.pack()
            b = Button(vazia, text="ok", width=20, command=vazia.destroy)
            b.pack()
            b.pack(side='bottom', padx=0, pady=0)
        else:
            remover = str(Ed1.get())
            tree.localizar(remover)
            if removerOk is 1:
                tree.remover(str(Ed1.get()))
                tree.rebalanceamento()
                encontrado = Tk()
                encontrado.title("Remoção")
                encontrado.geometry('300x50')
                resultado = Label(encontrado, text='Nó removido com sucesso.')
                resultado.pack()
                b = Button(encontrado, text="ok", width=20, command=encontrado.destroy)
                b.pack()
                b.pack(side='bottom', padx=0, pady=0)
            elif removerOk is 0:
                naoencontrado = Tk()
                naoencontrado.title("Remoção")
                naoencontrado.geometry('300x50')
                resultado = Label(naoencontrado, text='Nó não encontrado.')
                resultado.pack()
                b = Button(naoencontrado, text="ok", width=20, command=naoencontrado.destroy)
                b.pack()
                b.pack(side='bottom', padx=0, pady=0)


def search_button():
    global Ed1
    localizar = Tk()  # cria uma janela
    localizar.title('Localizar')  # seta o titulo da janela
    localizar.geometry('300x200')  # seta o tamanho da janela
    Ed1 = Entry(localizar, width=25, justify='center')  # cria uma entrada de texto
    Ed1.insert(0, '')  # seta o texto
    Ed1.pack()  # gerenciador de geometria
    Ed1.focus_set()  # obtm o foco para a entrada de texto
    remove_btn = Button(localizar, text='Localizar', width=20, command=localizar_button_func)
    remove_btn.pack()


def localizar_button_func():
    global localizado
    if not Ed1.get():  # [] entrada vazia
        notify2 = Tk()
        notify2.title("Remover!")
        notify2.geometry("300x50")
        resultado = Label(notify2, text='Digite um nó.')
        resultado.pack()
        b = Button(notify2, text="ok", width=20, command=notify2.destroy)
        b.pack()
        b.pack(side='bottom', padx=0, pady=0)
    else:
        if RAIZ is False:
            vazia = Tk()
            vazia.title("Remover!")
            vazia.geometry("300x50")
            resultado = Label(vazia, text='Árvore vazia.')
            resultado.pack()
            b = Button(vazia, text="ok", width=20, command=vazia.destroy)
            b.pack()
            b.pack(side='bottom', padx=0, pady=0)
        else:
            tree.localizar(str(Ed1.get()))
            localizar = Tk()
            localizar.title("Localizar")
            localizar.geometry('300x100')
            resultado = Label(localizar, text=localizado);
            resultado.pack()


def natural_button():
    del nodes[:]
    del fatores[:]
    WindowSize = [XDMI, YDMI]
    tree.calculaNiveis()
    tree.calcposicao()
    pygame.init()
    pygame.display.set_caption('AVL: Notação Natural')
    screen = pygame.display.set_mode(WindowSize)
    font = pygame.font.SysFont("Arial", 13)
    screen.fill(Gray)
    for i in range(len(nodes)):
        pygame.draw.circle(screen, Blue, (nodes[i][1][0] // 2, nodes[i][1][1]), 20, 2)
        text = font.render(str(nodes[i][0]), True, Black)
        screen.blit(text, (nodes[i][1][0] / 2 - 10, nodes[i][1][1] - 10))
        text = font.render(str(fatores[i]), True, Black)
        screen.blit(text, (nodes[i][1][0] / 2 + 25, nodes[i][1][1] - 10))
        for i in range(1, len(nodes)):
            pygame.draw.aaline(screen, Cyan, (nodes[i][2][0] / 2, nodes[i][2][1] + 20),
                               (nodes[i][1][0] / 2, nodes[i][1][1] - 20), 3)
    fpsClock = pygame.time.Clock()
    pygame.display.update()
    while 1:
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break
    pygame.quit()


def print_button():
    window = Tk()
    window.title('Visualização')
    window.geometry("200x50")
    print(tree.imprime())
    lb1 = Label(window, text='Verificar Console!')
    lb1.pack()
    b = Button(window, text="ok", width=20, command=window.destroy)
    b.pack()
    b.pack(side='bottom', padx=0, pady=0)


def print_fb_button():
    global Ed_fb
    localizar = Tk()  # cria uma janela
    localizar.title('Localizar')  # seta o titulo da janela
    localizar.geometry('300x200')  # seta o tamanho da janela
    Ed_fb = Entry(localizar, width=25, justify='center')  # cria uma entrada de texto
    Ed_fb.insert(0, '')  # seta o texto
    Ed_fb.pack()  # gerenciador de geometria
    Ed_fb.focus_set()  # obtm o foco para a entrada de texto
    remove_btn = Button(localizar, text='Localizar', width=20, command=print_fb_button_func)
    remove_btn.pack()


def print_fb_button_func():
    global localizado_fb
    if not Ed_fb.get():  # [] entrada vazia
        notify2 = Tk()
        notify2.title("Fator de balanceamento")
        notify2.geometry("300x50")
        resultado = Label(notify2, text='Digite um nó.')
        resultado.pack()
        b = Button(notify2, text="ok", width=20, command=notify2.destroy)
        b.pack()
        b.pack(side='bottom', padx=0, pady=0)
    else:
        if RAIZ is False:
            vazia = Tk()
            vazia.title("Fator de balanceamento")
            vazia.geometry("300x50")
            resultado = Label(vazia, text='Árvore vazia.')
            resultado.pack()
            b = Button(vazia, text="ok", width=20, command=vazia.destroy)
            b.pack()
            b.pack(side='bottom', padx=0, pady=0)
        else:
            tree.localizar_fb(str(Ed_fb.get()))
            localizar = Tk()
            localizar.title("Localizar")
            localizar.geometry('300x100')
            resultado = Label(localizar, text=localizado_fb);
            resultado.pack()
            b = Button(localizar, text="ok", width=20, command=localizar.destroy)
            b.pack()
            b.pack(side='bottom', padx=0, pady=0)


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def limparConsole_button():
    cls()


def direct_acess_button():
    global Ed_direct
    direct = Tk()  # cria uma janela
    direct.title('Localizar')  # seta o titulo da janela
    direct.geometry('300x200')  # seta o tamanho da janela
    Ed_direct = Entry(direct, width=25, justify='center')  # cria uma entrada de texto
    Ed_direct.insert(0, '')  # seta o texto
    Ed_direct.pack()  # gerenciador de geometria
    Ed_direct.focus_set()  # obtm o foco para a entrada de texto
    acess_btn = Button(direct, text='Localizar', width=20, command=direct_acess_func)
    acess_btn.pack()


def direct_acess_func():
    s = Ed_direct.get()
    try:
        s = s.strip(']')
        s = s.split('[')
        key = s[0]
        index = s[1]
        tree.direct_acess(key, index)
        text = direct_a
        notify = Tk()
        notify.geometry('300x100')
        notify.title('Acesso direto')
        lb = Label(notify, text=text)
        lb.pack()
        b = Button(notify, text="ok", width=20, command=notify.destroy)
        b.pack(side='bottom', padx=0, pady=0)

    except:
        notify = Tk()
        notify.geometry('300x100')
        notify.title('Acesso direto')
        lb = Label(notify, text='ERRO!')
        lb.pack()
        b = Button(notify, text="ok", width=20, command=notify.destroy)
        b.pack(side='bottom', padx=0, pady=0)