import PySimpleGUI as sg
import webview
import shutil
import os
from pathlib import Path
from unidecode import unidecode
import sys

# x86
# Controle Operacional.lnk
# Atendimento Médico.lnk
# Atendimento ao Cliente.lnk
# Atualizador da Estação.lnk
# C:\Users\Public\Área de Trabalho Pública

def delete_shortcuts():
    shortcuts_x86 = [
        'Apoio.lnk',
        'Apoio (2).lnk',
        'Apoio (3).lnk',
        'Atendimento ao Cliente.lnk',
        'Atendimento ao Cliente (2).lnk',
        'Atendimento ao Cliente (3).lnk',
        'Atendimento Médico.lnk',
        'Atendimento Médico (2).lnk',
        'Atendimento Médico (3).lnk',
        'Atualizador da Estação.lnk',
        'Atualizador da Estação (2).lnk',
        'Atualizador da Estação (3).lnk',
        'Clinica Medica.lnk',
        'Clinica Medica (2).lnk',
        'Clinica Medica (3).lnk',
        'Controle Operacional.lnk',
        'Controle Operacional (2).lnk',
        'Controle Operacional (3).lnk',
        'Sads.lnk',
        'Sads (2).lnk',
        'Sads (3).lnk',
    ]
    folder_destination_desktop_public = r'C:\Users\Public\Desktop'
    folder_destination_desktop_user = os.path.join(str(Path.home()), 'Desktop')

    for shortcut_x86 in shortcuts_x86:
        shortcuts_x86_list = [shortcut_x86.lower(), unidecode(shortcut_x86)] 
        for shortcut_x86_list in shortcuts_x86_list:
            file_destination_desktop_public = os.path.join(folder_destination_desktop_public, shortcut_x86_list)
            file_destination_desktop_user = os.path.join(folder_destination_desktop_user, shortcut_x86_list)

            if os.path.exists(file_destination_desktop_public):
                os.remove(file_destination_desktop_public)

            if os.path.exists(file_destination_desktop_user):
                os.remove(file_destination_desktop_user)
                

def find_data_file():
    if getattr(sys, "frozen", False):
        datadir = os.path.dirname(sys.executable)
    else:
        datadir = os.path.dirname(__file__)
    return datadir


def copy_shortcuts():
    folder_shortcuts = find_data_file() + '/shortcuts/'
    folder_destination = os.path.join(str(Path.home()), 'Desktop')

    for root, dirs, files in os.walk(folder_shortcuts):
        for file in files:
            file_source = root + file
            file_destination = os.path.join(folder_destination, file)
            shutil.copyfile(file_source, file_destination)



def make_main_window():
    sg.theme('default')
    buttons = [
        [
            sg.Button('Ir para a página de atualização do Sabi',
                      button_color=('#d8e3e7', '#126e82'), key='-WEBVIEW-'),
            sg.Button('Atualizar Sabi', button_color=(
                '#132c33', '#51c4d3'), key='-ATUALIZA-')
        ]
    ]
    layout = [[sg.Column(buttons, justification='center')]]
    return sg.Window('Atualizar Sabi', layout, finalize=True)


def main():
    main_window = make_main_window()
    webview_window = None

    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED and window == main_window:
            break

        if event == '-WEBVIEW-' and not webview_window:
            print('ok')

            main_window.hide()
            create_webview = webview.create_window(
                'Atualização do Sabi', 'https://www.python.org/downloads/windows/')
            webview_window = webview.start()

            if create_webview.closed:
                webview_window = None
                main_window.un_hide()

        if event == '-ATUALIZA-' and not webview_window:
            copy_paste()
            # delete_shortcuts()
            # copy_shortcuts()

    main_window.close()


if __name__ == '__main__':
    main()
    
