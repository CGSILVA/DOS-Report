#Envia emails para os SYSADMs cadastrados a cada alerta de ataque detectado
#True para enviar emails, False para não enviar
SEND_EMAIL = False

#Email(gmail) e senha do email que enviará o alerta de ataques (servidor)
EMAIL_PASSWORD = ('devmedia@gmail.com', '@Fbvmedia@')

#Lista de emails de SYSADMs
SYSADM = ('carlosgabrieldasilvasantana@gmail.com', 'rodrigo.melo199@gmail.com')

#Limite de requisições para um único IP
LIMITE_REQUISICOES_POR_IP = 5

#Limite de requisições distintas que o servidor pode suportar
LIMITE_REQUISICOES_TOTAL = 10

#Localização do arquivo de log do apache (Padrão->/var/log/apache2/access.log)
ARQUIVO_DE_LOG = '/var/log/apache2/access.log'

#Bloquear IPs para que não mais receber requisições
#True para bloquear, False para não bloquear
BLOQUEAR_ATAQUES = False

#Regra de iptables para bloquear IPs
#(Padrão -> iptables -D INPUT -s <ip> -j DROP)
IPTABLES = 'iptables -I INPUT -s <ip> -j DROP'

#Intervalo de tempo para releitura do log (tempo em segundos)
INTERVALO_TEMPO = 1

# Listar IPs bloqueados:
# iptables -L INPUT -n --line-numbers
# Liberar IPs usando número de identificação da lista:
# iptables -D INPUT <numero>
