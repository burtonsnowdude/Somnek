import pygame

# class du projectile
class Projectile(pygame.sprite.Sprite):

    def __init__(self, player):
        super().__init__()
        self.velocity = 2
        self.player = player
        self.image = pygame.image.load('assets/projectile.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x + 120
        self.rect.y = player.rect.y + 80
        self.origin_image = self.image
        self.angle = 0

    def rotate(self):
        # faire tourner le projectile
        self.angle += 8
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def remove(self):
        self.player.all_projectiles.remove(self)

    def check_collision(self, sprite, group):
        """Vérifier les collisions avec un groupe de sprites"""
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)
    
    def move(self,monstres_presents):
        self.rect.x += self.velocity
        self.rotate()

        # verifie si le projectile entre en collision avec un monstre
        for monster in self.check_collision(self,monstres_presents):
            self.remove()
            # infliger des degats
            monster.degats(self.player.attack)

        # verifie si le projectile n'est plus present sur l'ecran
        if self.rect.x > 1080:
            # supprimer le projectile (en dehors de l'ecran)
            self.remove()

