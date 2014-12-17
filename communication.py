import socket

def send_request(message):
  # 1) Définition du serveur auquel on s'adresse
  mySocket = socket.socket() 
  HOST = socket.gethostname() #A changer en fonction du serveur
  PORT = 12345 #A changer en fonction du serveur
     
  # 2) envoi d'une requête de connexion au serveur : 
  #On tente une connexion, message d'erreur si elle n'aboutie pas
  try: 
    mySocket.connect((HOST, PORT)) 
  except socket.error: 
    print("La connexion a échoué.") 
    sys.exit() 
  print("Connexion établie avec le serveur.") 
    
  # 3) Communication client serveur
  msgServeur = mySocket.recv(1024).decode("Utf8") 
  print("S>", msgServeur) 
  
  #envoi du message (message = parametre de la fonction)
  print("Message client : ", message)

  #Récupération de la réponse du serveur (si elle existe, a virer sinon)
  mySocket.send(message.encode("Utf8")) 
  print("S>", msgServeur) 

  # 4) Fermeture de la connexion : 
  print("Connexion interrompue.") 
  mySocket.close() 

def register(uid):
  send_request(uid)

def order(userId, pourcentage, origine, dest):
  userId = "[" + userId + "]"
  action = "MOV" + pourcentage
  origine = "FROM" + origine
  dest = "TO" + dest

  msg = userId + action + origine + dest
  send_request(msg)

def retrieve_from_server():
  """
  Fonction qui va boucler (dans un Thread de préference) pour ressortir les informations envoyées par le serveur
  Types d'informations envoyées : 
  -INIT : Chaine d'initialisation du terrain et des différents éléments contenus
  INIT<matchid>TO<#players>[<me>];<speed>;\
       <#cells>CELLS:<cellid>(<x>,<y>)'<radius>'<offsize>'<defsize>'<prod>,...;\
       <#lines>LINES:<cellid>@<dist>OF<cellid>,...

  -STATE : Chaine contenant les informations mises à jour des informations
  STATE20ac18ab-6d18-450e-94af-bee53fdc8fcaIS2;3CELLS:1[2]12'4,2[2]15'2,3[1]33'6;4MOVES:1<5[2]@232'>6[2]@488'>3[1]@4330'2,1<10[1]@2241'3
  """
  while 1:
    mySocket = socket.socket() 
    HOST = socket.gethostname() #A changer en fonction du serveur
    PORT = 12345 #A changer en fonction du serveur

    try: 
      mySocket.connect((HOST, PORT)) 
    except socket.error: 
      print("La connexion a échoué.") 
      sys.exit() 
    print("Connexion établie avec le serveur.") 

    msgServeur = mySocket.recv(1024).decode("Utf8") 
    print("S>", msgServeur) 

    if(msgServeur.contains("INIT")):
      #traitement de la string d'initialisation
      firstSplit = msgServeur.split(';')
      
    else if(msgServeur.contains("STATE"))
      #traitement de la string de mise à jour des informations



