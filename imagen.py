import sys
import math
import pygame
import time
from pygame.locals import *
import random


def tiempoEnQueSeDesocupaLaEstacion(estacion):
    return estacion[1]

T_E = int(raw_input("Tiempo entre las llegadas de clientes: "))
T_min = int(raw_input("ingrese el tiempo minimo de corte: "))
T_max = int(raw_input("ingrese el tiempo maximo de corte: "))
C = int(raw_input("ingrese el numero de clientes: "))
n_estaciones = int(raw_input("Numero de estaciones de peluqueros: "))


estaciones = []
servicios = []

t_llegada = 0
e_t  = 0
e_tn = 0
T_ll = 0
for e in range(0, n_estaciones):
    estaciones.append([e+1, 0])

rango = range(0,C)
for i in rango:
	R=random.random()
	T_ll += int(-T_E*math.log(R))	
	R=random.random()
	t_c = int(T_min + T_max - T_min*R)
	t_s = T_ll+ t_c
	estaciones.sort(key=tiempoEnQueSeDesocupaLaEstacion)
	e_t = estaciones[0][1] - T_ll
	
	if e_t < 0:
		e_t = 0

	s_a = t_s
	e_tn = e_t+ e_tn

	t_s += e_t
        estaciones[0][1] = t_s
	

	
    	servicios.append([i+1, T_ll, t_s, estaciones[0][0], e_t])
   	print "Cliente %s Llegada: %s Espera: %s Corte: %s Salida: %s Peluquero: %s" %(i+1, T_ll, e_t, t_c, t_s,estaciones[0][0])

	

fila = e_tn/s_a
e_pro = e_tn/C
uso = e_tn/s_a


print "\nlongitud de fila: ",fila
print "tiempo de espera: ",e_pro
print "uso de la instalacion: ",uso


raw_input("Iniciar simulacion ")#(%s segundos)..." %(t_salida_ultimo))
##INICIA SIMULACION EN pygames
pygame.init()

FPS = 10
fpsClock = pygame.time.Clock()

fondo = pygame.image.load('barberia.png')
peluquero = pygame.image.load('peluquero.png')
cliente = pygame.image.load('cliente.png')
pygame.display.set_caption("barberia")
screen = pygame.display.set_mode((819,460))
screen = pygame.display.set_mode((850,480))


def main():

    
    estaciones.sort(key=tiempoEnQueSeDesocupaLaEstacion)
    t_salida_ultimo = estaciones[-1][1]
    n_estaciones_ocupadas = 0
    n_clientes_en_espera = 0

    t = 0
    fps_contador = 0

    clientes_en_pantalla = []

    while True:
        fps_contador += 1

        screen.blit(fondo, (0, 0))
        screen.blit(peluquero, (200, 100))#se imprime primer peluquero
        screen.blit(peluquero, (1, 100))

        # mostrar clientes
        for c in clientes_en_pantalla:
            if c[3] == True:
                screen.blit(cliente, (c[1], c[2]))

                if c[4] == 1:
                    limite = 1
                else:
                    limite = 300

                if c[1] < limite and c[5] <=0:
                    c[1]+=10
                
                print "%s:%s" %(c[0], c[5])


        pygame.display.update()

        if fps_contador == 10:
            t += 1
            fps_contador = 0

            print t                    
    #for t in range (0,t_salida_ultimo+1):  
        #mensaje = "%s: (%s/%s) Peluqueros ocupados, %s En espera" %(t, n_estaciones_ocupadas, n_estaciones, n_clientes_en_espera)

            for servicio in servicios:
                if servicio[1] == t:
                    #mensaje += "\n >>> Llega: cliente #%s Atendido por Peluquero: #%s" %(servicio[0],servicio[3])
                    #          N_cliente, posX, posY, Mostrar
                    c = [servicio[0], 0, 100, True, servicio[3], servicio[4]]
                    clientes_en_pantalla.append(c)
                    if n_estaciones_ocupadas < n_estaciones:
                        n_estaciones_ocupadas += 1

                    if servicio[4] > 0:
                        n_clientes_en_espera += 1

                elif servicio[2] == t:
                    #mensaje += "\n <<< Sale:  cliente #%s %s min de espera, Se desocupa Peluquero: #%s" %(servicio[0], servicio[4], servicio[3])
                    for c in clientes_en_pantalla:
                        if servicio[0] == c[0]:
                            c[3] = False

                    if n_estaciones_ocupadas > 0 and n_clientes_en_espera == 0:
                        n_estaciones_ocupadas -= 1

                    if n_clientes_en_espera > 0:
                        n_clientes_en_espera -= 1
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        fpsClock.tick(FPS)
main()


    	




