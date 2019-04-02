# -*- coding: utf8 -*-

# author = Pedro Marques da Silva Junior
# principal

from helpers import *

root = Tk()
root.title('BST - AVL')
root.geometry('375x300')

file_btn = Button(root, text='Ler Arquivo', width=40, height=2, command=file_button)
manual_btn = Button(root, text='Inserir ', width=20, height=2, command=manual_button)
remove_btn = Button(root, text='Remover Nó', width=20, height=2, command=remove_button)
search_btn = Button(root, text='Localizar Nó', width=20, height=2, command=search_button)
print_fb_btn = Button(root, text='Fator de Balanceamento', width=20, height=2, command=print_fb_button)
print_btn = Button(root, text='Imprimir Árvore', width=40, height=2, command=print_button)
direct_btn = Button(root, text='Acesso direto', width=40, height=2, command=direct_acess_button)
btn_limpConsole = Button(root, text='Limpar Console', width=20, height=2, command=limparConsole_button)

file_btn.grid(row=0, column=0, columnspan=2, sticky=W+E)
manual_btn.grid(row=1, column=0, sticky=W+E)
remove_btn.grid(row=1, column=1, sticky=W+E)
search_btn.grid(row=2, column=0, sticky=W+E)
print_fb_btn.grid(row=2, column=1, sticky=W+E)
print_btn.grid(row=3, column=0, columnspan=2, sticky=W+E)
direct_btn.grid(row=4, column=0, columnspan=2, sticky=W+E)
btn_limpConsole.grid(row=5, column=0, columnspan=2, sticky=W+E)

root.mainloop()
