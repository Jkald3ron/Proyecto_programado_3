import pygame
from Menu_class import *
from funcionalidad import *

pygame.init()

#Iniciando clock
clock = pygame.time.Clock()

#Iniciando pantalla
pantalla = pygame.display.set_mode((500,300))
pygame.display.set_caption("Advice Machine")

#crear_texto
#E: texto, font, color, tamaño, posicion,posicion de rectangulo de referencia,superficie
#S: Se imprime el texto en la superficie con el font, color, tamaño y posicion
#R: -
def crear_texto(texto, tipo_font, color,tamano,posicion,posicion_rect,superficie):
    font = pygame.font.SysFont(tipo_font,tamano)
    impresion = font.render(texto, True, color)
    impresion_rect = impresion.get_rect()
    if posicion_rect.upper() == "CENTRO":
        impresion_rect.midtop = posicion
    elif posicion_rect.upper() == "DERECHA":
        impresion_rect.topright = posicion
    else:
        impresion_rect.topleft = posicion
    superficie.blit(impresion,impresion_rect)

#Iniciando font de consola
consola_font = "lucidaconsole"
    
#Advice Machine
running = True

#Iniciando Idioma 
idioma = 'esp'

#Cargando mensajes
mensajes = abrir_mensajes()
chistes = []
dichos = []
consejos = []
jokes = []
sayings = []
advices = []
for mensaje in mensajes:
    if mensaje:
        tipo = mensaje[0]
        if tipo == "1":
            chistes.append(mensaje)
        elif tipo == "2":
            dichos.append(mensaje)
        elif tipo == "3":
            consejos.append(mensaje)
        elif tipo == "4":
            jokes.append(mensaje)
        elif tipo == "5":
            sayings.append(mensaje)
        elif tipo == "6":
            advices.append(mensaje)
        else:
            pass


#Iniciando comandos
lista_comandos = [Menu("Administracion",["Ctrñ:","Resetear","Reporte","Apagar"]),
                  Menu("Idioma",["Español","English"]),
                  Menu("Mensaje",["Consejo","Chiste","Dicho"])]

seleccionando = False
comando_actual = 1
estado_actual = 0
monto = 50

#Funcionalidades
#apagar():para el ciclo
def apagar():
    global running
    running= False
#traducir_ingles(): cambia a lenguaje de los comandos a ingles
def traducir_ingles():
    global lista_comandos
    global idioma
    idioma = 'ing'
    lista_comandos = [Menu("Administration",["Pswd:","Reset","Report","Shut Down"]),
                      Menu("Language",["Español","English"]),
                      Menu("Message",["Advice","Joke","Saying"])]
    lista_comandos[0].buscar_estado("Shut Down").set_funcionalidad(apagar,[])
    lista_comandos[1].buscar_estado("Español").set_funcionalidad(traducir_espanol,[])
    lista_comandos[1].buscar_estado("English").set_funcionalidad(traducir_ingles,[])
    lista_comandos[0].buscar_estado("Pswd:").set_funcionalidad(contrasena,[])
    lista_comandos[2].buscar_estado("Joke").set_funcionalidad(imprimir,jokes)
    lista_comandos[2].buscar_estado("Advice").set_funcionalidad(imprimir,advices)
    lista_comandos[2].buscar_estado("Saying").set_funcionalidad(imprimir,sayings)
#traducir_espanol(): cambia a lenguaje de los comandos a espanol
def traducir_espanol():
    global lista_comandos
    global idioma
    idioma = 'esp'
    lista_comandos = [Menu("Administracion",["Ctrñ:","Resetear","Reporte","Apagar"]),
                  Menu("Idioma",["Español","English"]),
                  Menu("Mensaje",["Consejo","Chiste","Dicho"])]
    lista_comandos[0].buscar_estado("Apagar").set_funcionalidad(apagar,[])
    lista_comandos[1].buscar_estado("Español").set_funcionalidad(traducir_espanol,[])
    lista_comandos[1].buscar_estado("English").set_funcionalidad(traducir_ingles,[])
    lista_comandos[0].buscar_estado("Ctrñ:").set_funcionalidad(contrasena,[])
    lista_comandos[2].buscar_estado("Chiste").set_funcionalidad(imprimir,chistes)
    lista_comandos[2].buscar_estado("Dicho").set_funcionalidad(imprimir,dichos)
    lista_comandos[2].buscar_estado("Consejo").set_funcionalidad(imprimir,consejos)
#contrasena():
#E: lista de rectangulos
#S: Recibe contraseña por medio de colisiones con los rectangulos con el mouse y retorna un bool
#R: -
def contrasena(args):#argumentos:recs,menu,estado
    recs,menu,estado = args
    tmp = menu.get_estado(estado).get_nombre()
    ctrn_surface = pygame.Surface((275,75))
    ctrn_surface.fill((33,150,243))
    ctrn_rect = ctrn_surface.get_rect()
    ctrn_rect.topleft=(5,5)
    ctrn = ''
    correcta = False
    menu.set_estado(estado,menu.get_estado(estado).get_nombre()+ctrn)
    while len(ctrn) <= 5 and correcta == False:
        crear_texto(menu.get_estado(estado).get_nombre(),consola_font,(255,255,255),28,(1,1)," ",ctrn_surface)
        comandos.blit(ctrn_surface,ctrn_rect)
        contenedor.blit(comandos,comandos_rect)
        pantalla.blit(contenedor,contenedor_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if recs[0].collidepoint(mouse_pos):
                    ctrn += '1'
                    menu.set_estado(estado,tmp+ctrn)
                    break
                if recs[1].collidepoint(mouse_pos):
                    ctrn += '0'
                    menu.set_estado(estado,tmp+ctrn)
                    break
                
        if ctrn == '10110':
            correcta = True
            
        pygame.display.update()
        clock.tick(60)
 
    menu.set_estado(estado,tmp)
    ctrn_surface.fill((33,150,243))
    comandos.blit(ctrn_surface,ctrn_rect)
    return correcta

#imprimir(tipo,monto)
def imprimir(args):#argumentos: tipo
    global monto
    tipo = args
    #Conseguir mensaje: hacer una lista de los precios, comparar los precios
    precios = []
    for ele in tipo:
        if ele[3].isnumeric():
            if int(ele[3]) >= monto:
                precios.append(int(ele[3]))
    if len(precios) != 1:
        precio = comparar_precios(monto,precios)
    else:
        precio = precios[0]-monto
    indice = precios.index(precio+monto)
    mensaje = tipo[indice]
    print(mensaje)
    return mensaje
    #Imprimir mensaje

#comparar_precio(monto,lista)
def comparar_precios(monto,lista):
    #Hacer una pila de comparaciones
    if lista[1:] == []:
        return lista[0]
    else:
        return comparar_menor(lista[0]-monto,comparar_precios(monto,lista[1:]))
#comparar_menor
def comparar_menor(x,y):
    if x > y:
        return y
    else:
        return x
                
#Asignando funcionalidades
lista_comandos[0].buscar_estado("Ctrñ:").set_funcionalidad(contrasena,[])
lista_comandos[0].buscar_estado("Apagar").set_funcionalidad(apagar,[])
lista_comandos[1].buscar_estado("Español").set_funcionalidad(traducir_espanol,[])
lista_comandos[1].buscar_estado("English").set_funcionalidad(traducir_ingles,[])

#Maquina de Consejos
while running:

    pantalla.fill((255,153,51))

    #Creando contenedor
    contenedor = pygame.Surface((480,280))
    contenedor.fill((38,50,56))
    contenedor_rect = contenedor.get_rect()
    contenedor_rect.topleft = (10,10)

    #Creando Espacio Monedas
    espacio_monedas =  pygame.Surface((150,260))
    espacio_monedas.fill((189,189,189))
    espacio_monedas_rect = espacio_monedas.get_rect()
    espacio_monedas_rect.topleft = (10,10)
    pygame.draw.circle(espacio_monedas,(224,224,224),(75,60),50,0)
    pygame.draw.rect(espacio_monedas,(0,0,0),(70,15,10,90))

    #Creando Impresora
    impresora = pygame.Surface((300,170))
    impresora.fill((189,189,189))
    impresora_rect = impresora.get_rect()
    impresora_rect.topleft = (170,100)
    
    #Creando Ranura de impresión
    pygame.draw.rect(impresora,(0,0,0),(20,35,260,25))

    #Creando ranura de vueltos
    pygame.draw.rect(espacio_monedas,(66,66,66),(5,120,140,130))

    #Creando linea de comandos
    comandos = pygame.Surface((280,80))
    comandos.fill((33,150,243))
    comandos_rect = comandos.get_rect()
    comandos_rect.topleft = (170,10)

    #Creando Botones
    boton0 = pygame.Surface((20,30))
    boton0.fill((255,51,0))
    boton0_rect = comandos.get_rect()
    boton0_rect.topleft = (455,15)

    boton1 = pygame.Surface((20,30))
    boton1.fill((0,255,51))
    boton1_rect = comandos.get_rect()
    boton1_rect.topleft = (455,55)

    #Colocando Texto
    crear_texto(lista_comandos[comando_actual].get_nombre(),
                consola_font,
                (255,255,255),
                28,(5,5),
                " ",comandos)
    
    crear_texto(lista_comandos[comando_actual].get_estado(estado_actual).get_nombre(),
                consola_font,
                (255,255,255),
                28,(5,45),
                " ",comandos)

    #Poniendo en pantalla
    contenedor.blit(boton1,boton1_rect)
    contenedor.blit(boton0,boton0_rect)
    contenedor.blit(impresora,impresora_rect)
    contenedor.blit(comandos,comandos_rect)
    contenedor.blit(espacio_monedas,espacio_monedas_rect)
    pantalla.blit(contenedor,contenedor_rect)

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if boton1_rect.collidepoint(mouse_pos):
                if seleccionando == False:
                    seleccionando = True
                    estado_tmp = estado_actual
                    estado_actual = 0
                    if idioma == 'esp':
                        lista_comandos[comando_actual].transicion1()
                    else:
                        lista_comandos[comando_actual].transicion2()
                    break
                else:
                    seleccionando = False
                    estado_actual = 0
                    lista_comandos[comando_actual].reset()
                    nombre_estado = lista_comandos[comando_actual].get_estado(estado_tmp).get_nombre()
                    if nombre_estado == "Ctrñ:" or nombre_estado == "Pswd:":
                        lista_comandos[0].buscar_estado(nombre_estado).set_funcionalidad(contrasena,[[boton1_rect,boton0_rect],
                                                                       lista_comandos[comando_actual],
                                                                       estado_tmp])
                        valor = lista_comandos[comando_actual].get_estado(estado_tmp).do_funcionalidad()
                        if valor:
                            estado_actual += 1
                            break
                    elif lista_comandos[comando_actual].get_estado(estado_tmp).get_funcionalidad() != None:
                       lista_comandos[comando_actual].get_estado(estado_tmp).do_funcionalidad()
                    if comando_actual != len(lista_comandos)-1:
                           comando_actual += 1
                    break
            if boton0_rect.collidepoint(mouse_pos):
                if seleccionando == False:
                    if comando_actual > 0:
                        comando_actual -= 1
                    else:
                        comando_actual += 1
                    estado_actual = 0
                    break
                else:
                    seleccionando = False
                    valor = len(lista_comandos[comando_actual].get_tmp()[1])
                    lista_comandos[comando_actual].reset()
                    nombre_estado = lista_comandos[comando_actual].get_estado(estado_tmp).get_nombre()
                    if nombre_estado == "Ctrñ:" or nombre_estado == "Pswd:":
                        pass
                    else:
                        if estado_tmp == valor-1:
                            estado_actual = 0
                        else:
                            estado_actual = estado_tmp + 1
                    break
              
    pygame.display.update()
    clock.tick(60)
    
pygame.display.quit()
