'''
Librería display.
'''
from machine import Pin
from time import sleep

class Display:
    '''Una clase del Display de 7 segmentos; los argumentos `a`-`g` deben ser números enteros (GPIO, pines).
       El argumento `common_cathode` indica si el display
       es cátodo común (True) o ánodo común (False).\n
       Funciones extra disponibles para los objetos Display:
       >>> \tall_displays_on()
       >>> \tall_displays_off()'''
    __displays_counter = 0
    __list_of_displays = []
    def __init__(self, a:int, b:int, c:int, d:int, e:int, f:int, g:int, common_cathode = True):
        Display.__displays_counter += 1
        Display.__list_of_displays.append(self)
        self.common_cathode = common_cathode
        self.state_on, self.state_off = (1, 0) if self.common_cathode else (0, 1)
        if all(isinstance(pin, int) for pin in [a, b, c, d, e, f, g]):
            self.a = Pin(a, Pin.OUT)
            self.b = Pin(b, Pin.OUT)
            self.c = Pin(c, Pin.OUT)
            self.d = Pin(d, Pin.OUT)
            self.e = Pin(e, Pin.OUT)
            self.f = Pin(f, Pin.OUT)
            self.g = Pin(g, Pin.OUT)
            self.SEGMENTS = [self.a, self.b, self.c, self.d, self.e, self.f, self.g]
        else:
            raise ValueError("Todos los pines deben ser enteros.")
        
    @classmethod
    def total_displays(cls):
        return cls.__displays_counter
    
    def __str__(self):
        return "Display de 7 segmentos."
        
    def print_int(self, number:int) -> None:
        '''Muestra números del 0 al 9 (enteros).'''
        N0 = [self.a, self.b, self.c, self.d, self.e, self.f]
        N1 = [self.b, self.c]
        N2 = [self.a, self.b, self.g, self.e, self.d]
        N3 = [self.a, self.b, self.c, self.g, self.d]
        N4 = [self.b, self.c, self.f, self.g]
        N5 = [self.a, self.c, self.d, self.f, self.g]
        N6 = [self.a, self.c, self.d, self.e, self.f, self.g]
        N7 = [self.a, self.b, self.c]
        N8 = [self.a, self.b, self.c, self.d, self.e, self.f, self.g]
        N9 = [self.a, self.b, self.c, self.f, self.g]
        NUMBERS = {0:N0, 1:N1, 2:N2, 3:N3, 4:N4, 5:N5, 6:N6, 7:N7, 8:N8, 9:N9}
        if number in NUMBERS:
            for segment in self.SEGMENTS:
                segment.value(self.state_on if segment in NUMBERS[number] else self.state_off)
        else:
            raise ValueError(f'Númbero {number} fuera del rango disponible (0-9).')
            
    def print_str(self, string:str, seconds:int|float = 1) -> None:
        '''Muestra las letras de una cadena (o una sola letra).
           Como una secuencia de letras de la cadena con el intervalo de tiempo
           entre letras determinado por el argumento `seconds` dado (default 1s).\n
           Nota: si una letra no está disponible, un guión (-) será mostrado. Si existe un espacio entre
           la cadena, el display lo mostrará apagándose.'''
        L_A = [self.a, self.b, self.c, self.e, self.f, self.g]
        L_b = [self.c, self.d, self.e, self.f, self.g]
        L_c = [self.d, self.e, self.g]
        L_d = [self.b, self.c, self.d, self.e, self.g]
        L_E = [self.a, self.d, self.e, self.f, self.g]
        L_F = [self.a, self.e, self.f, self.g]
        L_g = [self.a, self.b, self.c, self.d, self.f, self.g]
        L_H = [self.b, self.c, self.e, self.f, self.g]
        L_h = [self.c, self.e, self.f, self.g]
        L_I = [self.e, self.f]
        L_i = [self.e]
        L_J = [self.b, self.c, self.d, self.e]
        L_L = [self.d, self.e, self.f]
        L_o = [self.c, self.d, self.e, self.g]
        L_P = [self.a, self.b, self.e, self.f, self.g]
        L_u = [self.c, self.d, self.e]
        L_U = [self.b, self.c, self.d, self.e, self.f]
        L_r = [self.e, self.f, self.g]
        L_S = [self.a, self.c, self.d, self.f, self.g]
        if isinstance(string, str):
            available_chars = {'A':L_A, 'a':L_A, 'B':L_b, 'b':L_b,'C':L_c, 'c':L_c,'D':L_d, 'd':L_d, 'E':L_E,
                               'e':L_E, 'F':L_F, 'f':L_F, 'G':L_g,'g':L_g, 'H':L_H,'h':L_h, 'I':L_I,'i':L_i,
                               'J':L_J, 'j':L_J, 'L':L_L,'l':L_L, 'O':L_o, 'o':L_o, 'P':L_P, 'p':L_P,'R':L_r,
                               'r':L_r,'S':L_S,'s':L_S, 'U':L_U, 'u':L_u}
            for char in string:
                if char.isspace():
                    self.display_off()
                    sleep(seconds)
                else:
                    segments_on = available_chars.get(char, [self.g]) 
                    for segment in self.SEGMENTS:
                        segment.value(self.state_on if segment in segments_on else self.state_off)
                    sleep(seconds)
        else:
            raise ValueError("El argumento debe ser una cadena.")
        
    def print_custom_char(self, custom_char:list[Pin]) -> None:
        '''Muestra un caracter personalizado.\n
           El argumento `custom_char` debe ser una lista de objetos (segmentos) de la clase Pin.\n
           >>> from machine import Pin 
           >>> a = Pin(0, Pin.OUT)
           >>> g = Pin(1, Pin.OUT)
           >>> d = Pin(2, Pin.OUT)
           >>> custom_char = [a, g, d]'''
        for segment in self.SEGMENTS:
            segment.value(self.state_on if segment in custom_char else self.state_off)
                    
    def display_off(self, segment:list[str]|str = 'all') -> None:
        '''Apaga todos los segmentos si no se especifica ninguno de estos.\n
           Si quiere especificar un segmento o varios debe hacerlo en forma de caracter o lista (string).\n
           Ejemplo:
           >>> segment = 'a'
           >>> segment = 'abc'
           >>> segment = ['a', 'b', 'c']
           '''
        if segment == 'all':
            for seg in self.SEGMENTS:
                seg.value(self.state_off)
        else:
            if isinstance(segment, str) or isinstance(segment, list):
                LOW_SEGMENTS = {'a':self.a, 'b':self.b, 'c':self.c, 'd':self.d, 'e':self.e, 'f':self.f, 'g':self.g}
                if all(s.lower() in LOW_SEGMENTS for s in segment):
                    for s in segment:
                        seg = LOW_SEGMENTS[s.lower()]
                        seg.value(self.state_off)
                else:
                    raise ValueError('Segmento no válido.')
            else:
                raise ValueError('El argumento segment debe ser una lista o una cadena.')
        
    def display_on(self, segment:list[str]|str = 'all') -> None:
        '''Enciende todos los segmentos si no se especifica ninguno de estos.\n
           Si quiere especificar un segmento o varios debe hacerlo en forma de cadena o lista (string).\n
           Ejemplo:
           >>> segment = 'a'
           >>> segment = 'abc'
           >>> segment = ['a', 'b', 'c']
           '''
        if segment == 'all':
            for seg in self.SEGMENTS:
                seg.value(self.state_on)
        else:
            if isinstance(segment, (str, list)):
                HIGH_SEGMENTS = {'a':self.a, 'b':self.b, 'c':self.c, 'd':self.d, 'e':self.e, 'f':self.f, 'g':self.g}
                if all(s.lower() in HIGH_SEGMENTS for s in segment):
                    for s in segment:
                        seg = HIGH_SEGMENTS[s.lower()]
                        seg.value(self.state_on)
                else:
                    raise ValueError('Segmento no válido.')
            else:
                raise ValueError('El argumento segment debe ser una lista o una cadena.')
            
        
    def display_spiral(self, seconds:float|int = .1, reverse = False) -> None:
        '''Los segmentos encienden en forma de espiral.\n
           El argumento `reverse` determina si inicia de reversa (True) o no (False).
           El argumento `seconds` determina el tiempo de encendido entre los segmentos (default 0.1s).'''
        SPIRAL_SEGMENTS = [self.g, self.f, self.a, self.b, self.c, self.d, self.e]
        if not reverse:
            for segment in SPIRAL_SEGMENTS:
                segment.value(self.state_on)
                sleep(seconds)
        else:
            for segment in reversed(SPIRAL_SEGMENTS):
                segment.value(self.state_on)
                sleep(seconds)
    
def all_displays_off() -> None:
    '''Apaga todos los displays.\n
        Raises:
            RuntimeError: Si no hay objectos Display creados.'''
    if Display.__list_of_displays:
        for display in Display.__list_of_displays:
            display.display_off()
    else:
        raise RuntimeError('No hay objetos Display.')

def all_displays_on() ->  None:
    '''Enciende todos los displays.\n
       Raises:
            RuntimeError: Si no hay objectos Display creados.'''
    if Display.__list_of_displays:
        for display in Display.__list_of_displays:
            display.display_on()
    else:
        raise RuntimeError('No hay objetos Display.')

if __name__ == "__main__":
    display1 = Display(11, 10, 20, 21, 22, 9, 8, True) #Cátodo común
    display2 = Display(15, 14, 16, 19, 17, 13, 12, True) #Cátodo común

    try:
        while True:
            all_displays_on()
            sleep(.5)
            all_displays_off()
            sleep(.5)
    except KeyboardInterrupt:

        all_displays_off()
