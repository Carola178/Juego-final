        #     # Manejar eventos de teclado solo si el juego no está pausado
        #     if not self.paused:
        #         if event.type == KEYDOWN:
        #             if event.key == K_UP:
        #                 self.player.jump()
        #             if event.key == pygame.K_SPACE:
        #                 self.toggle_pause()
        #             if event.key == K_e:
        #                 if self.enemy.alive():
        #                     new_star = Stars([self.all_sprites, self.enemy.stars_group], self.enemy.rect.midtop, self.shoot_sound)
        #                     self.all_sprites.add(new_star)
        #                     self.enemy_shooting = True

        #         if event.type == KEYUP:
        #             if event.key == K_e:
        #                 self.enemy_shooting = False

        # # Actualizar el juego si no está pausado
        # if not self.paused:
        #     self.update()

        # self.draw()
        # if self.paused:
        #     self.draw_pause_screen()