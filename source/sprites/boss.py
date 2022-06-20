'''
Big boss, meo.
'''
from source.sprites.monster import Monster


class Boss(Monster):
    '''
    Boss class.
    '''

    def __init__(self, groups, obstacles, pos, player, summon_ghosts):
        super().__init__(groups, obstacles, pos, "abrobra")
        self.player = player
        self.summon_ghosts = summon_ghosts
        self.last_hp = self.health
        self.phase = 1

    def update(self):
        '''
        Overrides basic update method.
        '''
        if self.last_hp != self.health:
            self.last_hp = self.health
            self._drop_ammo(self.rect.center, 1)
        if self.health <= self.stats["health"]["max"] // 2 and self.phase < 2:
            self.phase = 2
            self.speed += 1
            print("Phase 2")
            self.__spawn_minions()
        elif self.health == 1 and self.phase < 3:
            self.phase = 3
            self.speed += 1
            self.damage += 1
            self.health += 2
            print("Phase 3")
        super().update()

    def __spawn_minions(self):
        '''
        Spawns minions.
        '''
        self.summon_ghosts(self.rect.center, 4)

    def is_alive(self):
        '''
        Checks if boss is alive.
        '''
        return self.health > 0
