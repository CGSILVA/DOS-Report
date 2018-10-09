import argparse
import os
import re
import time
from multiprocessing import Process
import file_writer, send_email, settings
from version import get_version


class Ddos_reporter():

    def print_monitoring(self):

        print('\nMonitorando...')
        print('\n\033[1;31m ATENÇÃO - EXECUTE COMO SUPERUSUÁRIO (ROOT)\033[0;33m\n')
        print('\033[0;36m Versão:\033[0;33m', get_version())
        print('\033[0;36m Arquivo de log:\033[0;33m', settings.ARQUIVO_DE_LOG)
        print('\033[0;36m Limite de requisições para um único IP:\033[0;33m', settings.LIMITE_REQUISICOES_POR_IP)
        print('\033[0;36m Limite de requisições distintas para o servidor:\033[0;33m',settings.LIMITE_REQUISICOES_TOTAL)
        print('\033[0m')

        fileBytePos = os.path.getsize(settings.ARQUIVO_DE_LOG)

        email_sender = send_email.Send_Email()

        fw = file_writer.File_writer()

        ipsBloqueados = {}

        ultimoDoS = ''
        ultimoDDoS = ''

        regex = re.compile(r'(.+?) .+?\n')

        while True:
            with open(settings.ARQUIVO_DE_LOG, 'r') as _file:

                _file.seek(fileBytePos)

                data = _file.read()

                #Capturando somente o(s) IP(s) de cada cliente
                access_list = re.findall(regex, data)

                #Verifica se house um estouro no limite de requisições
                #possíveis por segundo
                if len(set(access_list)) > settings.LIMITE_REQUISICOES_TOTAL:
                    ips = []
                    for ip in set(access_list):
                        ips.append(ip)
                    ips = ', '.join(ips)
                    print ('\033[1;31mATENÇÃO\033[0m - Estouro do limite de {} requisições por segundo (Ataque DDoS)\nIPs:'.format(
                        settings.LIMITE_REQUISICOES_TOTAL), ips)

                #Contando numero de requisições para cada IP
                ipcounter = []
                for ip in set(access_list):
                    total = access_list.count(ip)
                    if total > settings.LIMITE_REQUISICOES_POR_IP:
                        if args.verbose:
                            print (ip, '- Total:', total, '\033[0;31m(Ataque detectado)\033[0m')
                        ipcounter.append(ip)
                    else:
                        if args.verbose:
                            print (ip, '- Total:', total)

                #Define tipo de ataque
                if len(ipcounter) > 0:
                    #Ataque DDoS---------------------------
                    if len(ipcounter) > 1:
                        ips = []
                        for ip in set(ipcounter):
                            ips.append(ip)
                        ips = ', '.join(ips)
                        if settings.BLOQUEAR_ATAQUES:
                            if ultimoDDoS != ips:
                                print ('\033[1;31mAlerta de ataque DDoS\033[0m - \033[1;32mIPs:', ips, '\033[0m')
                        else:
                            print ('\033[1;31mAlerta de ataque DDoS\033[0m - \033[1;32mIPs:', ips, '\033[0m')
                        ultimoDDoS = ips

                        #Bloqueando Ataque
                        if settings.BLOQUEAR_ATAQUES:
                            for ip in ipcounter:
                                if not (ip in ipsBloqueados):
                                    if os.system(re.sub(r'<ip>', ip, settings.IPTABLES)) == 0:
                                        ipsBloqueados[ip] = 'Bloqueando'
                                        print ('IP {} bloqueado'.format(ip))
                                        Process(target=fw.logAppend, args=('IP {} bloqueado\n'.format(ip), )).start()

                        #Enviando Email
                        if settings.SEND_EMAIL:
                            print ('Enviando email para o(s) SYSADM(s)...')
                            if len(settings.SYSADM) == 0:
                                print ('Nenhum email de SYSADM cadastrado')
                            else:
                                for email in settings.SYSADM:
                                    Process(target=email_sender.send_email, args=(email, ipcounter, 1)).start()
                    else:
                        #Ataque DoS------------------------
                        if settings.BLOQUEAR_ATAQUES:
                            if ultimoDoS != ipcounter[0]:
                                print ('\033[1;31mAlerta de ataque DoS\033[0m - \033[1;32mIP:', ipcounter[0], '\033[0m')
                        else:
                            print ('\033[1;31mAlerta de ataque DoS\033[0m - \033[1;32mIP:', ipcounter[0], '\033[0m')
                        ultimoDoS = ipcounter[0]

                        #Bloqueando Ataque
                        if settings.BLOQUEAR_ATAQUES:
                            if not (ipcounter[0] in ipsBloqueados):
                                if os.system(re.sub(r'<ip>', ipcounter[0], settings.IPTABLES)) == 0:
                                    ipsBloqueados[ipcounter[0]] = 'Bloqueando'
                                    print ('IP {} bloqueado'.format(ipcounter[0]))
                                    Process(target=fw.logAppend, args=('IP {} bloqueado\n'.format(ipcounter[0]), )).start()

                        #Enviando Email
                        if settings.SEND_EMAIL:
                            print ('Enviando email para o(s) SYSADM(s)...')
                            if len(settings.SYSADM) == 0:
                                print ('Nenhum email de SYSADM cadastrado')
                            else:
                                for email in settings.SYSADM:
                                    Process(target=email_sender.send_email, args=(email, ipcounter[0], 0)).start()

                if data != '' and args.verbose:
                    print ('')

                fileBytePos = _file.tell()

                try:
                    time.sleep(settings.INTERVALO_TEMPO)
                except KeyboardInterrupt:
                    print ('\nMonitoramento finalizado\n')
                    exit()
        print ('\n\033[1;31m ATENÇÃO - EXECUTE COMO SUPERUSUÁRIO (ROOT)\033[0;33m\n')
        print ('\033[0;36m Versão:\033[0;33m', get_version())
        print ('\033[0;36m Arquivo de log:\033[0;33m', settings.ARQUIVO_DE_LOG)
        sysadms = []
        for email in settings.SYSADM:
            sysadms.append(email)
        sysadms = ', '.join(sysadms)
        print ('\033[0;36m SYSADMs:\033[0;33m', sysadms)
        print ('\033[0;36m Enviar emails de alerta:\033[0;33m', settings.SEND_EMAIL)
        print ('\033[0;36m Limite de requisições para um único IP:\033[0;33m', settings.LIMITE_REQUISICOES_POR_IP)
        print ('\033[0;36m Limite de requisições distintas para o servidor:\033[0;33m', settings.LIMITE_REQUISICOES_TOTAL)
        print ('\033[0;36m Bloquear ataques:\033[0;33m', settings.BLOQUEAR_ATAQUES)
        if settings.BLOQUEAR_ATAQUES:
            print ('\033[0;36m Regra iptables:\033[0;33m', settings.IPTABLES)
        print ('\033[0m')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', dest='verbose', action="store_true", help='Prints every access', default=False)
    args = parser.parse_args()

    monitor = Ddos_reporter()
    monitor.print_monitoring()