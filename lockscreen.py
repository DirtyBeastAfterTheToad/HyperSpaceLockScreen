import pygame
import sys
import time
import random

# --- CONFIGURATION ---
CORRECT_PASSWORD = "4521432"
PLANET_NAME = "THIEFFRUS" 
MAX_ATTEMPTS = 3

COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (50, 205, 50) 
COLOR_RED   = (220, 20, 60)
COLOR_WHITE = (255, 255, 255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Système de Navigation")
    pygame.mouse.set_visible(False)
    
    font_large = pygame.font.Font(None, 120) 
    font_small = pygame.font.Font(None, 50) 

    app_running = True

    while app_running:
        success = run_lock_screen(screen, font_large, font_small)
        
        if not success:
            app_running = False
            break

        run_hyperspace_animation(screen)

        should_restart = run_end_menu(screen, font_small)
        
        if not should_restart:
            app_running = False

    pygame.quit()
    sys.exit()

def run_lock_screen(screen, font_large, font_small):
    """Handles the password input and validation sequence"""
    width, height = screen.get_size()
    
    input_text = ""
    attempts_left = MAX_ATTEMPTS
    bg_color = COLOR_BLACK
    status_message = "ENTREZ LES COORDONNÉES"
    
    input_locked = False 
    waiting_for_confirmation = False
    
    def draw_ui(current_bg, current_text, current_status, show_attempts, blink_enter):
        screen.fill(current_bg)
        
        msg_surface = font_small.render(current_status, True, COLOR_WHITE)
        msg_rect = msg_surface.get_rect(center=(width // 2, height // 2 - 150))
        screen.blit(msg_surface, msg_rect)

        display_string = ""
        for i in range(len(CORRECT_PASSWORD)):
            if i < len(current_text):
                display_string += current_text[i] + " " 
            else:
                display_string += "_ " 
        
        code_surface = font_large.render(display_string.strip(), True, COLOR_WHITE)
        code_rect = code_surface.get_rect(center=(width // 2, height // 2))
        screen.blit(code_surface, code_rect)

        if show_attempts and current_bg != COLOR_GREEN:
            attempts_text = f"ESSAIS RESTANTS : {attempts_left}"
            attempts_surface = font_small.render(attempts_text, True, COLOR_WHITE)
            attempts_rect = attempts_surface.get_rect(center=(width // 2, height // 2 + 150))
            screen.blit(attempts_surface, attempts_rect)

        if blink_enter:
            if int(time.time() * 2) % 2 == 0: 
                text_surf = font_small.render("[APPUYEZ SUR ENTRÉE POUR LANCER]", True, COLOR_WHITE) 
                text_rect = text_surf.get_rect(center=(width // 2, height // 2 + 250))
                screen.blit(text_surf, text_rect)

        pygame.display.flip()

    while True:
        draw_ui(bg_color, input_text, status_message, True, waiting_for_confirmation)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                # CONFIRMATION PHASE
                if waiting_for_confirmation:
                    if event.key == pygame.K_RETURN: 
                        return True

                elif not input_locked:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    
                    elif event.unicode.isdigit() and len(input_text) < len(CORRECT_PASSWORD):
                        input_text += event.unicode
                        
                        draw_ui(bg_color, input_text, status_message, True, False)
                        
                        if len(input_text) == len(CORRECT_PASSWORD):
                            time.sleep(0.4)

                            if input_text == CORRECT_PASSWORD:
                                # SUCCESS
                                input_locked = True
                                bg_color = COLOR_GREEN
                                
                                # Sequence
                                sequence_messages = [
                                    (f"COORDONNÉES DE LA PLANÈTE {PLANET_NAME} RENTRÉES", 2.0),
                                    ("CALIBRAGE DES FUSÉES...", 2.0),
                                    ("CALCUL DE L'ITINÉRAIRE (VITESSE SUPRALIMINALE)...", 2.5),
                                ]
                                
                                for msg, duration in sequence_messages:
                                    status_message = msg
                                    draw_ui(bg_color, input_text, status_message, False, False)
                                    time.sleep(duration)
                                
                                status_message = "GPS INTERSTELLAIRE PRÊT. CONFIRMER ?"
                                waiting_for_confirmation = True

                            else:
                                # FAIL
                                attempts_left -= 1
                                bg_color = COLOR_RED
                                if attempts_left <= 0:
                                    status_message = "SYSTÈME VERROUILLÉ"
                                    input_locked = True
                                    draw_ui(bg_color, input_text, status_message, True, False)
                                else:
                                    status_message = "COORDONNÉES INCORRECTES"
                                    draw_ui(bg_color, input_text, status_message, True, False)
                                    time.sleep(1.0)
                                    input_text = ""
                                    bg_color = COLOR_BLACK
                                    status_message = "ENTREZ LES COORDONNÉES"
        
        pygame.time.Clock().tick(30)

def run_hyperspace_animation(screen):
    width, height = screen.get_size()
    clock = pygame.time.Clock()
    stars = []
    num_stars = 500
    speed = 2
    
    for _ in range(num_stars):
        stars.append([random.randint(-width, width), random.randint(-height, height), random.randint(1, width), random.randint(1, width)])

    start_time = time.time()
    duration = 7.0 
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > duration:
            break

        screen.fill(COLOR_BLACK)
        cx, cy = width // 2, height // 2

        speed *= 1.02 
        if speed > 150: speed = 150

        for star in stars:
            star[3] = star[2]
            star[2] -= speed

            if star[2] <= 0:
                star[0] = random.randint(-width, width)
                star[1] = random.randint(-height, height)
                star[2] = width
                star[3] = star[2]

            k = 128.0 / star[2]
            px = star[0] * k + cx
            py = star[1] * k + cy
            
            k_prev = 128.0 / star[3]
            px_prev = star[0] * k_prev + cx
            py_prev = star[1] * k_prev + cy

            if 0 <= px < width and 0 <= py < height:
                color_val = min(255, int(100 + speed * 2))
                pygame.draw.line(screen, (color_val, color_val, color_val), (px_prev, py_prev), (px, py), int(speed/10) + 1)

        if elapsed > duration - 1.0:
            alpha = int(((elapsed - (duration - 1.0)) / 1.0) * 255)
            fade_s = pygame.Surface((width, height))
            fade_s.fill(COLOR_WHITE)
            fade_s.set_alpha(alpha)
            screen.blit(fade_s, (0,0))

        pygame.display.flip()
        clock.tick(60)

def run_end_menu(screen, font):
    """Displays the final choice: Restart or Exit"""
    width, height = screen.get_size()
    screen.fill(COLOR_WHITE)
    pygame.display.flip()
    time.sleep(0.5)

    while True:
        screen.fill(COLOR_BLACK)
        
        msg1 = font.render("ARRIVÉE À DESTINATION", True, COLOR_GREEN)
        msg2 = font.render("ENTRÉE : NOUVELLE MISSION", True, COLOR_WHITE)
        msg3 = font.render("ECHAP  : QUITTER LE SYSTÈME", True, COLOR_RED)
        
        r1 = msg1.get_rect(center=(width // 2, height // 2 - 50))
        r2 = msg2.get_rect(center=(width // 2, height // 2 + 50))
        r3 = msg3.get_rect(center=(width // 2, height // 2 + 120))
        
        screen.blit(msg1, r1)
        screen.blit(msg2, r2)
        screen.blit(msg3, r3)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
        
        pygame.time.Clock().tick(30)

if __name__ == "__main__":
    main()