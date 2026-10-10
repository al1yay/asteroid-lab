import pygame
import random
import math
import asyncio

async def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("hello")
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    RED = (128, 0, 128)
    GRAY = (100,100,100)
    score_font = pygame.font.SysFont(None, 20) 

    def display_dot(x, y, dot_number):
        dot_text = "Dot Product = " + str(round(dot_number, 2))
        dot_render = score_font.render(dot_text, True, WHITE)

        # 4. Draw the score text surface onto the screen at (x, y) coordinates
        screen.blit(dot_render, (20, 20))

    def display_dist(x, y, dist_number):
        dot_text = "Distance = " + str(round(dist_number, 2))
        dot_render = score_font.render(dot_text, True, WHITE)

        # 4. Draw the score text surface onto the screen at (x, y) coordinates
        screen.blit(dot_render, (20, 40))

    def display_state(x, y, state_num):
        dot_text = "Enemy State: " + state_num
        dot_render = score_font.render(dot_text, True, WHITE)

        # 4. Draw the score text surface onto the screen at (x, y) coordinates
        screen.blit(dot_render, (20, 60))

    circle_pos = pygame.math.Vector2(100,100)
    circle_radius = 20

    vector_a = pygame.math.Vector2(4, 3)
    circle_radius = 10

    asteroid_list = []

    for (i) in range(6):
        position = pygame.math.Vector2(random.randint(20, 580), random.randint(20, 380))

        vx = 0

        while vx == 0:
            vx = random.randint(-1, 1)

        vy = 0
        while vy == 0:
            vy = random.randint(-1, 1)

        velocity = pygame.math.Vector2(vx, vy)

        radius = random.randint(10, 40)

        asteroid_list.append([position, velocity, radius])




    # draw spaceship


    point1 = (300, 180) # starting point of missiles
    point2 = (280, 220)
    point3 = (320, 220)
    vertices = [point1, point2, point3]
    ship_pos = pygame.math.Vector2(point1)
    angle = 90


    vertices = [point1, point2, point3]


    x = int(position.x)
    y = int(position.y)

    missile_pos = pygame.math.Vector2(point1)
    missile_velocity = pygame.math.Vector2(0, 0)
    missile = True

    ship_velocity = pygame.math.Vector2(0, 0)
    acceleration = pygame.math.Vector2(0,0)
    THRUST = 0.15
    DRAG = 0.95
    MAX_SPEED = 7

    enemy_pos = pygame.math.Vector2(300, 200)
    enemy_angle = 0          # Faces right (0 degrees)
    RANGE = 120    # Max vision distance
    dot_max = 0.7      # Dot product threshold (~45-degree cone)
    state = "PATROL"

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((20, 20, 30))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            angle += 3

        if keys[pygame.K_RIGHT]:
            angle -= 3


        radians = math.radians(angle)

        forward = pygame.Vector2(
            math.cos(radians),
            -math.sin(radians)
    )

        if not missile:
            missile_pos = pygame.math.Vector2(point1)
        
        acceleration = pygame.Vector2(0, 0)

        if keys[pygame.K_UP]:
            acceleration = forward * THRUST
        
        ship_velocity*=DRAG
        ship_velocity += acceleration

        if velocity.length() > MAX_SPEED:
            velocity.scale_to_length(MAX_SPEED)


        ship_pos += ship_velocity

        if ship_pos.x > 600:
            ship_pos.x = 0
        if ship_pos.x < 0:
            ship_pos.x = 600

        if ship_pos.y > 400:
            ship_pos.y = 0
        if ship_pos.y < 0:
            ship_pos.y = 400

        point1 = ship_pos + forward * 20
        point2 = ship_pos + forward.rotate(135) * 28.28
        point3 = ship_pos + forward.rotate(-135) * 28.28
        vertices = [point1, point2, point3]

        enemy_rad = math.radians(enemy_angle)
        enemy_forward = pygame.Vector2(math.cos(enemy_rad), -math.sin(enemy_rad))

    # 2. Calculate Distance to Player
        distance = enemy_pos.distance_to(ship_pos)

        # 3. Calculate Direction Vector to Player & Normalize
        to_player = ship_pos - enemy_pos
        if to_player.length() > 0:
            to_player = to_player.normalize()

        # 4. Calculate Dot Product
        dot = enemy_forward.dot(to_player)

        if dot > dot_max:
            print("PLAYER DETECTED")

        display_dot(20,20,dot)
        display_dist(20,40,distance)
        display_state(20,60,state)

        enemy_angle += 0.5
        enemy_angle %= 360

        # 5. AI Decision State Machine
        if distance < RANGE and dot > dot_max:
            state = "ATTACK"
            enemy_color = RED
        else:
            state = "PATROL"
            enemy_color = WHITE


        pygame.draw.polygon(screen, "white", vertices, 1)

        for asteroid in asteroid_list:
            position = asteroid[0]
            radius = asteroid[2]

            pygame.draw.circle(
                screen,
                (180, 180, 180),
                (int(position.x), int(position.y)),
                radius
        )

        missile_pos+= missile_velocity

        pygame.draw.circle(
                screen,
                ("green"),
                (missile_pos),
                5
        )

        
        pygame.draw.polygon(screen, "white", vertices, 5)

        pygame.draw.circle(screen, GRAY, (int(enemy_pos.x), int(enemy_pos.y)), RANGE, 1)

        # Draw Enemy Body
        pygame.draw.circle(screen, enemy_color, (int(enemy_pos.x), int(enemy_pos.y)), 15)

        # Draw Facing Direction Line
        pygame.draw.line(screen, RED, enemy_pos, enemy_pos + enemy_forward * 40, 3)





        for a in asteroid_list:
            a[0]+=a[1]

        

        # collision between asteroids

        for c in range(len(asteroid_list)):
            for (d) in range(c+1, len(asteroid_list)):
                current = asteroid_list[c]
                extra = asteroid_list[d]
                p1 = current[0]
                p2 = extra[0]
                v1 = current[1]
                v2 = extra[1]
                r1 = current[2]
                r2 = extra[2]
                m1 = r1 ** 2
                m2 = r2 ** 2
                d = p1.distance_to(p2)

                if(d) <= r1+r2:
                    pos_diff = p1 - p2
                    vel_diff = v1 - v2

                    if pos_diff.length_squared() != 0:
                        factor = vel_diff.dot(pos_diff) / pos_diff.length_squared()

                        vf1 = v1 - (2 * m2 / (m1 + m2)) * factor * pos_diff
                        vf2 = v2 - (2 * m1 / (m1 + m2)) * (-factor) * pos_diff

                    else:
                        vf1 = -v1
                        vf2 = -v2

                    current[1] = vf1
                    extra[1] = vf2

        # wall collision

        for c in range(len(asteroid_list)):
            current = asteroid_list[c]
            if current[0].x <= 0 + current[2] or current[0].x >= 600 - current[2]:
                current[1].x = -current[1].x
            if current[0].y <= 0+current[2] or current[0].y >= 400 - current[2]:
                current[1].y = -current[1].y

        if keys[pygame.K_SPACE]:
            missile = True
            direction = forward
            missile_pos = pygame.math.Vector2(ship_pos)
            missile_velocity = pygame.math.Vector2(direction * 5)

        for d in range(len(asteroid_list) - 1, -1, -1):
            if missile_pos.distance_to(asteroid_list[d][0]) < (5 + asteroid_list[d][2]):
                if (asteroid_list[d][2] < 23):
                    asteroid_list.remove(asteroid_list[d])
                else:
            
                    p = asteroid_list[d][0] + pygame.math.Vector2(-50,50)
                    p2 = asteroid_list[d][0]
                
                    v = pygame.math.Vector2(random.randint(-1, 1), random.randint(-1, 1))
                    v2 = pygame.math.Vector2(random.randint(-1, 1), random.randint(-1, 1))
                
                    r = (asteroid_list[d][2])/2
                
                    asteroid_list.append([p, v, r])
                    asteroid_list.append([p2,v2,r])

                    asteroid_list.remove(asteroid_list[d])

            
            
        
        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0) # 3. VERY IMPORTANT: Yield control to the browser

# 4. Run the async main function
asyncio.run(main())
