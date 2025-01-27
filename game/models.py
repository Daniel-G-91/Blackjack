from django.db import models

class Game(models.Model):
    
    deck            = models.JSONField()
    player_hand     = models.JSONField(default=list)
    dealer_hand     = models.JSONField(default=list)
    player_score    = models.IntegerField(default=0)
    dealer_score    = models.IntegerField(default=0)
    
    player_chips    = models.JSONField(default=list)
    player_chips_v  = models.IntegerField(default=500)
    dealer_chips    = models.JSONField(default=list)
    dealer_chips_v  = models.IntegerField(default=500)
    
    player_bet_v    = models.IntegerField(default=0)
    player_bet      = models.JSONField(default=list)
    dealer_bet_v    = models.IntegerField(default=0)
    dealer_bet      = models.JSONField(default=list)
    round_bet_v     = models.IntegerField(default=0)
    round_bet       = models.JSONField(default=list)
    
    game_result     = models.CharField(max_length=50, default='')
    is_active       = models.BooleanField(default=True)
