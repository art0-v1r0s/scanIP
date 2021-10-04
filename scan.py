import socket
import threading

""" Dictionnaire permettant de recueillir les hosnames des machines connectées
    sur un réseau """

host = {}
""" classe définissant le thread de scan d'adresse Ip servant à récupérer """
""" le hostname du périphérique réseau                                    """

class NetscanThread(threading.Thread):

    """ Constructeur de la classe prend en argument les paramètres suivants: """
    """ address : adresse IP à scanner                                       """
    def __init__(self, address):

        self.address = address
        threading.Thread.__init__(self)

    """ Définition de la méthode Run de notre classe de scan """
    def run(self):
        self.lookup(self.address)

    """ Méthode de classe permettant de récupérer le hostname du périphérique           """
    """ connecté au réseau. Elle prend en paramètrre la variable de classe représentant """
    """ l'adresse IP à recherchée                                                       """
    def lookup(self, address):

        """ On gère l'exception en cas de périphérique non connecté à l'adresse IP à scanner """
        try:
            """ On récupère le hostname et l'alias de la machine connectée """
            hostname, alias, _ = socket.gethostbyaddr(address)
            global host
            """ On associe le hostname à l'adresse IP et on les sauve dans le dictionnaire """
            host[address] = hostname
        except socket.herror:
            host[address] = None

""" programme principal """
if __name__ == '__main__':
    addresses = []

    """ On définit une plage d'adresses IP à scanner """
    for ping in range(1, 254):
        addresses.append("10.33.5." + str(ping))

    threads = []

    """ On créée autant de threads qu'il y à d'adresses IP à scanner """
    netscanthreads = [NetscanThread(address) for address in addresses]
    for thread in netscanthreads :
        """ Chaque thread est démarré en même temps """
        thread.start()
        threads.append(thread)

    for t in threads:
        t.join()

    """ On affiche le résultat qui affiche pour chaque machine connectée son nom d'hôte """
    for address, hostname in host.items():
        if (hostname != None):
            print(address, '=>', hostname)