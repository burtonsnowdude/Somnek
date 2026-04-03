import pygame as pyg
import random
pyg.font.init() # initialiser le module font de pygame

# class qui gère et défini le projectile du joueur
class Projectile(pyg.sprite.Sprite):
    #definir le créateur de la classe
    def __init__(self,player):
        super().__init__()
        self.velocity = 5
        self.player = player
        self.image = pyg.image.load("Images/projectile_pistolet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = player.pos.center
        self.origin_image = self.image
        self.angle = 0
        
        
    def rotate(self): 
         #tourner le projectile
         self.angle +=16
         self.image = pyg.transform.rotozoom(self.origin_image, self.angle, 1)
         self.rect = self.image.get_rect(center = self.rect.center)
    def remove(self):
         self.kill()
        
    def check_collision(self, sprite, group):
        """Vérifier les collisions avec un groupe de sprites"""
        return pyg.sprite.spritecollide(sprite, group, False, pyg.sprite.collide_mask)
    def move(self):
            self.rect.y -= self.velocity  
            #self.rotate()
            """for monster in self.check_collision(self,monstres_presents):"""
            """self.remove()"""
            # infliger des degats
            """monster.degats(self.player.attack)"""
            #verifier si le projectile est présent
            if self.rect.y <0:
                 #suppprimer le projectile en dehors de l'écran
                 self.remove()
    
                
         
    


    
                
         
    

