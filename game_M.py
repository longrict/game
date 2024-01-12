import pygame
import random

pygame.init()

from setup import *

turn = -1
inCombat = True
action_cooldown = 0
action_delay = 40
clicked = False
cursor_sword = pygame.image.load("images/terrain/sword.png").convert_alpha()
cursor_x = pygame.image.load("images/terrain/x.png")
game_over = 0

# game loop
while run:
    #set framerate, get mouse position
    clock.tick(FRAMES)
    pos = pygame.mouse.get_pos()

    if inCombat:
        if player.alive:
            action_cooldown+=1 

            #display background, panel and player 
            draw_Combat()
            draw_panel()
            player.drawPerson()
            player.health_bar.draw(player.hp)

            #display enemies, if they have been dead for a while keep death animation at last frame
            for enemy in enemy_list:
                if not enemy.longdead:
                    if not enemy.alive:
                        enemy.longdead = True
                    enemy.health_bar.draw(enemy.hp)
                if enemy.longdead:
                    enemy.image = enemy.animation_list[3][3]
                if enemy.alive:
                    enemy.update()
                enemy.drawPerson()

            #display damage and healing numbers
            damage_text_group.update()
            damage_text_group.draw(screen)

            pygame.mouse.set_visible(True)

            #combat
            if action_cooldown >= action_delay:
                
                #if player's turn
                if turn == -1:

                    #check cursor collision with enemy "hitboxes"
                    for enemy in enemy_list:
                        if enemy.rect.collidepoint(pos):
                            if enemy.alive: #if valid target for attack
                                pygame.mouse.set_visible(False)
                                screen.blit(cursor_sword,pos)
                                if clicked: #attack on click, next fighter's turn
                                    player.attack(enemy)
                                    turn = 0
                                    action_cooldown = 0
                            elif not enemy.alive: #if not valid target for attack
                                pygame.mouse.set_visible(False)
                                screen.blit(cursor_x,pos)

                    # check collision with use potion button
                    if player_heal.isClicked(pos,clicked):
                        if player.heal(): # if player can heal, heal and then next fighter's turn
                            turn = 0
                            action_cooldown = 0
                        else: # otherwise still player's turn
                            turn = -1
                
                # enemy turn
                else: 
                    # if reached end of enemy list, player's turn
                    if turn >= len(enemy_list):
                        turn = -1
                    
                    else:
                        current = enemy_list[turn]

                        # if current enemy can attack
                        if current.alive:
                            if action_cooldown >= action_delay:
                                # choose between attacking or healing if using a potion is possible
                                if current.cur_potions > 0 and current.hp/current.max_health <= 0.5:
                                    choice = random.choice([enemy.attack(player), enemy.heal()])
                                #otherwise just attack player
                                else:
                                    current.attack(player)
                                action_cooldown = 0  
                        # if current enemy is dead, play death animation
                        if not current.alive:
                            current.die()
                        turn += 1 #next turn
            
            #check if any bandits are still alive
            if not enemy_alive():
                #if not, end game with victory screen
                inCombat = False
                game_over = 1

            #check if player is alive           
            elif not player.alive:
                # if not, end game with defeat screen
                inCombat = False
            player_heal.draw()
            player.update()

    # game over
    else:
        pygame.mouse.set_visible(True)
        draw_bg()

        #if player is dead (defeat)
        if game_over == 0:
            #play death animation
            if not player.longdead:
                player.longdead = True
            elif player.longdead:
                player.image = player.animation_list[3][8]
        
        #display gameover screen depending on who won
        GameOver(game_over)
        
    player.update()
    player.drawPerson()  

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
        
    pygame.display.update()

pygame.quit()