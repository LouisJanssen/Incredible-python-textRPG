# IMPORTS
from DiceSystem import DiceRoll
from Level import LevelUp
from Stats import *
from Inventory import Objects, Inventory
from Tools import promptSlow
Player = PlayerStats()

# SAVE PLAYER STATS
class SavePlayerStats:
    def __init__(self):
        self.Hp = 10
SaveHp = Player.Hp
SavePlayer = SavePlayerStats()
SavePlayer.Hp = SaveHp

# COMBAT
PlayerTurn = True

def Combat(PlayerTurn, ennemy, playerdefense):

    PlayerDefense = playerdefense

    def useObject():
        SLOT = 'SLOT'
        promptSlow("Quel objet souhaitez vous utiliser ?")
        InventoryList = ['','','','','']
        for i in range(0,5):
            InventoryList[i] = Inventory[('slot' + str(i + 1))][SLOT]
        print(InventoryList)
        ask = input(' > ')
        if ask in InventoryList:
            if ask.lower() == 'ambrosia':
                promptSlow('Vous buvez l\'ambroisie')
                Player.Hp += 10
            elif ask.lower() == 'fire':
                promptSlow('Vous lancer le feu sacré')
                ennemy.Hp -= 10
            else:
                print('Veuillez choisir un consommable')
                useObject()

    print('-----------------------------------------------------------------------')

    if (Player.Hp > 0) and (ennemy.Hp > 0) :

        if PlayerTurn == False : # TOUR DE L'ADVERSAIRE
            print('Tour de l\'adversaire')
            PlayerTurn = True
            if ennemy.Hp > 0 :
                print('L\'ennemi fait son action')
                
                # Action de l'adversaire
                # L'ennemi attaque
                MobAttack = DiceRoll()
                print('Lancer de dé ennemi :', MobAttack) # Est-ce qu'on l'affiche ?
                if MobAttack >= 10 : # Modifier plus tard en fonction des stats du joueur (AGI...)
                    if PlayerDefense == False :
                        Player.Hp -= ennemy.Atk # Ajouter plus tard les bonus relatifs à la STR
                    elif PlayerDefense == True :
                        InventoryList = ['','','','','']
                        SLOT = 'SLOT'
                        for i in range(0,5):
                            InventoryList[i] = Inventory[('slot' + str(i + 1))][SLOT]
                        if 'shield' not in InventoryList:
                            Player.Hp -= (3/4)*(ennemy.Atk) # Les dégâts sont réduits de 3/4 si le joueur se défend
                else :
                    print('Loupé !')

            else :
                print('L\'ennemi est K.O.')
            
            Combat(PlayerTurn, ennemy, playerdefense)

        elif PlayerTurn == True : # TOUR DU JOUEUR
            print('Joueur :', Player.name, '-', Player.Hp, 'PV')
            print('ENNEMI :', ennemy.name, '-', ennemy.Hp, 'PV')
            print(']===================================[')
            print('1 - ATTAQUER')
            print('2 - SE DÉFENDRE')
            print('3 - OBJETS')
            print(']===================================[')
            Action = input()

            if Action == '1' :
                print('Le Joueur attaque')
                PlayerDefense = False
                playerdefense = PlayerDefense
                PlayerTurn = False
                Attack = DiceRoll()
                print('Lancer de dé :', Attack)
                if Attack >= 10 : # Modifier plus tard en fonction des stats du joueur
                    ennemy.Hp -= Player.Atk # Ajouter plus tard les bonus relatifs à la STR
                else :
                    print('Loupé !')
                Combat(PlayerTurn, ennemy, playerdefense)

            elif Action == '2' :
                print('Se défendre')
                PlayerDefense = True
                playerdefense = PlayerDefense
                PlayerTurn = False
                # Se défendre : Diminue de 3/4 la prochaine attaque ennemie
                Combat(PlayerTurn, ennemy, playerdefense)

            elif Action == '3' :
                print('Objets')
                # Afficher liste des objets présents dans l'inventaire
                useObject()
                PlayerTurn = False
                Combat(PlayerTurn, ennemy, playerdefense)
            else:
                print("ERREUR : Veuillez entrer le chiffre correspondant à l\'une des questions posées.")
                Combat(PlayerTurn, ennemy, playerdefense)
    
    elif Player.Hp <= 0 :
        print('GAME OVER')
    
    elif (Player.Hp > 0) and (ennemy.Hp <= 0) :
        print('VICTOIRE')

def StartCombat(currentennemy):

    # SAVE MOB STATS
    class EnnemyStats:
        def __init__(self):
            self.name = MobStats[currentennemy][NAME]
            self.Hp = MobStats[currentennemy][HP]
            self.Atk = MobStats[currentennemy][ATK]
            self.loot = MobStats[currentennemy][LOOT]
    
    # COMBAT
    Combat(PlayerTurn, EnnemyStats(), False)

    # RESET PLAYER STATS (Mob stats reset automatically)
    Player.Hp = SavePlayer.Hp
    PlayerXP = Player.xp
    MobXP = MobStats[currentennemy][XP]
    LevelUp(PlayerXP, MobXP)

StartCombat('SpiderStats')
# StartCombat('ChickenStats')