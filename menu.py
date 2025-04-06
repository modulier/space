import pygame
import mine3

pygame.init()

#Создаем окно
window = pygame.display.set_mode((700, 500))

#Загружаем фон
bg = pygame.image.load("galaxy.jpg")
bg = pygame.transform.scale(bg, (700, 500))

fps = pygame.time.Clock()

#Создаем кнопки
button_rect = pygame.Rect(250,200,200,50)#Начать игру
button_exit = pygame.Rect(250, 270, 200, 50)#Выход

font = pygame.font.Font(None, 35)
text_start = font.render("Начать игру",True,(255, 255, 255))
text_exit = font.render("Выход",True,(255, 255, 255))

running = True
while running:
    window.blit(bg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False #Выход из игры

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos() #Получаем координаты мыши

            if button_rect.collidepoint(mouse_pos): #Проверяем нажата ли кнопка "Начать игру"
                mine3.start() #Запускаем игру
                running = False #Выход из главного меню

            if button_exit.collidepoint(mouse_pos): #Проверяем нажата ли кнопка "Выход"
                running = False #Завершаем игру

    #Рисуем кнопки
    pygame.draw.rect(window,(22, 66, 168), button_rect)
    pygame.draw.rect(window,(22, 66, 168), button_exit)

    window.blit(text_start, (275,215))
    window.blit(text_exit, (300,285))

    pygame.display.update()
    fps.tick(60)

pygame.quit()


