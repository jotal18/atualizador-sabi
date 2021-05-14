import PySimpleGUI as sg
import shutil
import os
from pathlib import Path
from unidecode import unidecode
import sys
import threading
import logging
import platform
import webbrowser

# Atalhos x86 criados em C:\Users\Public\Área de Trabalho Pública:
# Controle Operacional.lnk
# Atendimento Médico.lnk
# Atendimento ao Cliente.lnk
# Atualizador da Estação.lnk

# Pastas criadas em C:\Program Files (x86)\Sabi:
# Atendimento ao Cliente
# Atendimento Medico
# atualizador
# Controle Operacional
# Manuais

# Link para download das versões do Sabi
# http://www-sabi/versao.asp

logging.basicConfig(handlers=[logging.FileHandler('Log.log', 'a+', 'utf-8')],
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

icon = 'sabi_application.ico'

def check_folder_exists(name_folder):
    return os.path.exists(name_folder)


def copy_folder():
    folder_source = 'C:\Program Files (x86)\Sabi'
    folder_destination = 'C:\Program Files\Sabi'

    try:
        if os.path.exists(folder_destination):
            shutil.rmtree(folder_destination)
        shutil.copytree(folder_source, folder_destination)
    except OSError:
        raise


def delete_shortcuts():
    shortcuts_x86 = [
        'Apoio.lnk', 'Apoio (2).lnk', 'Apoio (3).lnk', 'Atendimento ao Cliente.lnk',
        'Atendimento ao Cliente (2).lnk', 'Atendimento ao Cliente (3).lnk',
        'Atendimento Médico.lnk', 'Atendimento Médico (2).lnk', 'Atendimento Médico (3).lnk',
        'Atualizador da Estação.lnk', 'Atualizador da Estação (2).lnk', 'Atualizador da Estação (3).lnk',
        'Clinica Medica.lnk', 'Clinica Medica (2).lnk', 'Clinica Medica (3).lnk',
        'Controle Operacional.lnk', 'Controle Operacional (2).lnk', 'Controle Operacional (3).lnk',
        'Sads.lnk', 'Sads (2).lnk', 'Sads (3).lnk',
    ]

    folder_destination_desktop_public = r'C:\Users\Public\Desktop'
    folder_destination_desktop_user = os.path.join(str(Path.home()), 'Desktop')

    for shortcut_x86 in shortcuts_x86:
        shortcuts_x86_list = [shortcut_x86.lower(), unidecode(shortcut_x86)]
        for shortcut_x86_list in shortcuts_x86_list:
            file_destination_desktop_public = os.path.join(
                folder_destination_desktop_public, shortcut_x86_list)
            file_destination_desktop_user = os.path.join(
                folder_destination_desktop_user, shortcut_x86_list)

            if os.path.exists(file_destination_desktop_public):
                os.remove(file_destination_desktop_public)

            if os.path.exists(file_destination_desktop_user):
                os.remove(file_destination_desktop_user)


def verify_folder_name(file):
    file_name = file.split('.')
    folder_source = 'C:\Program Files (x86)\Sabi'

    if file_name[0] == 'Clinica Medica':
        return os.path.join(folder_source, 'Atendimento Medico')

    return os.path.join(folder_source, file_name[0])


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
            if os.path.exists(verify_folder_name(file)):
                shutil.copyfile(file_source, file_destination)


def make_main_window_x64():
    # menu_def = [['&Aplicação', ['E&xit']], ['&Ajuda', ['&Sobre']]]

    buttons = [
        [sg.Button('IR PARA A PÁGINA DE ATUALIZAÇÃO DO SABI', key='-WEBVIEW-', size=(25, 2), font=("Helvetica", 12)), 
        sg.Button('CORRIGIR ATUALIZAÇÃO', key='-ATUALIZA-', size=(22, 2), font=("Helvetica", 12))]
    ]

    texts = [
        [sg.Text('Programa para auxiliar na atualização do Sabi', font=("Helvetica", 17), justification='center', 
                relief=sg.RELIEF_RIDGE, text_color='white')],
        [sg.Text('1 - Clique no botão IR PARA A PÁGINA DE ATUALIZAÇÃO DO SABI,'
                 + ' para acessar a página com as versões do Sabi.', size=(50, 3), 
                font=("Helvetica", 11), text_color='white')],
        [sg.Text('2 - Depois de baixar e instalar as versões do Sabi é preciso clicar no botão '
                + 'CORRIGIR ATUALIZAÇÃO, para concluir a atualização.', size=(50, 3), 
                font=("Helvetica", 11), text_color='white', key='-ITEM2-')],
        [sg.Text('Obs.: Após baixar e instalar as versões do Sabi é imprescindível clicar no botão '
                + 'CORRIGIR ATUALIZAÇÃO para realizar o procedimento correto de atualização do Sabi no computador.',
                key='-OBS-', 
                size=(65, 3), font=("Helvetica", 9), text_color='white')]
    ]

    # layout = [[sg.Menu(menu_def, key='-MENU-')], [texts], [buttons]]
    layout = [[texts], [buttons]]

    return sg.Window('Atualizar Sabi', layout, finalize=True, 
                icon=find_data_file() + f'/{icon}')


def make_main_window_x86():
    buttons = [
        [sg.Button('IR PARA A PÁGINA DE ATUALIZAÇÃO DO SABI', key='-WEBVIEW-', size=(50, 2), font=("Helvetica", 12))]
    ]

    texts = [
        [sg.Text('Atualize o Sabi', font=("Helvetica", 18), justification='center', size=(31,1), 
                relief=sg.RELIEF_RIDGE, text_color='black', background_color='white')],
        [sg.Text('1 - Clique no botão IR PARA A PÁGINA DE ATUALIZAÇÃO DO SABI,'
                 + ' para acessar a página com as versões do Sabi.', size=(55, 2), 
                font=("Helvetica", 10), text_color='black', background_color='white')]
    ]

    layout = [[texts] ,[buttons]]

    return sg.Window('Atualizar Sabi', layout, finalize=True, 
                icon=find_data_file() + f'/{icon}', background_color='white')


def make_modal_sim_nao():
    layout = [
        [sg.Text('Você baixou e instalou as versões mais novas do Sabi?', size=(27,2))],
        [sg.Button('Sim'), sg.Button('Não')]
    ]
    return sg.Window('Atualizou o Sabi?', layout, finalize=True, modal=True, icon=icon, font=("Helvetica", 12))


def thread_with_logging(window):
    try:
        copy_folder()
        delete_shortcuts()
        copy_shortcuts()
        logging.debug("Sabi atualizado com sucesso!!!")
        return window.write_event_value('-THREAD DONE-', '')
    except OSError as err:
        logging.error('Erro na atualização do Sabi: %s',  err)
        return window.write_event_value('-ERRO-', '')


def check_windows_architecture():
    return platform.architecture()[0]


def main():
    main_window = None
    architecture = check_windows_architecture()
    main_window = make_main_window_x86() if architecture != '64bit' else make_main_window_x64()
    modal_sim_nao = None
    work_id = 0
        
    while True:
        window, event, values = sg.read_all_windows(
            timeout=100, timeout_key=10)
        
        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            if window == modal_sim_nao:
                modal_sim_nao = None
            elif window == main_window:
                break

        if event == '-WEBVIEW-':
            # main_window.hide()
            # create_webview = webview.create_window(
            #     'Atualização do Sabi', 'http://www-sabi/versao.asp')
            # webview_window = webview.start()

            # if create_webview.closed:
            #     webview_window = None
            #     main_window.un_hide()
            webbrowser.open_new('http://www-sabi/versao.asp')

        elif event == '-ATUALIZA-':
            if not check_folder_exists('C:\Program Files (x86)\Sabi'):
                sg.popup('O Sabi não está instalado no computador!!!',
                         icon=icon, font=("Helvetica", 12))
            else:
                modal_sim_nao = make_modal_sim_nao()

        elif event == 'Sim':
            modal_sim_nao.hide()

            work_id = work_id + 1 if work_id < 19 else 0
            threading.Thread(target=thread_with_logging,
                             args=(window,), daemon=True).start()
        elif event == 'Não':
            print('ok')
            window.close()

        elif event == '-ERRO-':
            work_id = 0
            sg.popup_animated(None)
            sg.popup('Não foi possível atualizar o Sabi!!!',
                     title='Erro!!!', icon=icon, font=("Helvetica", 12), button_color='red')

        elif event == '-THREAD DONE-':
            work_id = 0
            sg.popup_animated(None)
            sg.popup('Sabi atualizado com sucesso!!!',
                     title='Sucesso', icon=icon, font=("Helvetica", 12))

        elif work_id:
            sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF,
                              message='Aguarde a atualização do Sabi!!!',
                              background_color='white',
                              time_between_frames=100,
                              no_titlebar=False,
                              text_color='black',
                              icon=icon,
                              font=("Helvetica", 12))
    main_window.close()


if __name__ == '__main__':
    main()
