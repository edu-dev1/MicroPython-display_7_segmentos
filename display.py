'''
Librería display de 7 segmentos.
'''
from machine import Pin
from time import sleep

class Display:
    '''Una clase del Display de 7 segmentos; los argumentos `a`-`g` deben ser números enteros (GPIO, pines).
       El argumento `common_cathode` indica si el display
       es cátodo común (True) o ánodo común (False).\n
       Funciones extra disponibles para los objetos Display:
            all_displays_on()
            all_displays_off()'''
    __displays_counter = 0
    __list_of_displays = []
    
    def __init__(self, a:int, b:int, c:int, d:int, e:int, f:int, g:int, common_cathode = True):
        Display.__displays_counter += 1
        Display.__list_of_displays.append(self)
        self.__common_cathode = common_cathode
        self.__state_on, self.__state_off = (1, 0) if self.__common_cathode else (0, 1)
        
        if all(isinstance(pin, int) for pin in [a, b, c, d, e, f, g]):
            self.__a = Pin(a, Pin.OUT)
            self.__b = Pin(b, Pin.OUT)
            self.__c = Pin(c, Pin.OUT)
            self.__d = Pin(d, Pin.OUT)
            self.__e = Pin(e, Pin.OUT)
            self.__f = Pin(f, Pin.OUT)
            self.__g = Pin(g, Pin.OUT)
            self.__SEGMENTS = [self.__a, self.__b, self.__c, self.__d, self.__e, self.__f, self.__g]
        else:
            raise ValueError("Todos los pines deben ser enteros.")
        
    @classmethod
    def total_displays(cls):
        return cls.__displays_counter
    
    def __str__(self):
        return "Display de 7 segmentos."
        
    def print_int(self, number:int) -> None:
        '''Muestra números del 0 al 9 (enteros).'''
        N0 = [self.__a, self.__b, self.__c, self.__d, self.__e, self.__f]
        N1 = [self.__b, self.__c]
        N2 = [self.__a, self.__b, self.__g, self.__e, self.__d]
        N3 = [self.__a, self.__b, self.__c, self.__g, self.__d]
        N4 = [self.__b, self.__c, self.__f, self.__g]
        N5 = [self.__a, self.__c, self.__d, self.__f, self.__g]
        N6 = [self.__a, self.__c, self.__d, self.__e, self.__f, self.__g]
        N7 = [self.__a, self.__b, self.__c]
        N8 = [self.__a, self.__b, self.__c, self.__d, self.__e, self.__f, self.__g]
        N9 = [self.__a, self.__b, self.__c, self.__f, self.__g]
        NUMBERS = {0:N0, 1:N1, 2:N2, 3:N3, 4:N4, 5:N5, 6:N6, 7:N7, 8:N8, 9:N9}
        if number in NUMBERS:
            for segment in self.__SEGMENTS:
                segment.value(self.__state_on if segment in NUMBERS[number] else self.__state_off)
        else:
            raise ValueError(f'Númbero {number} fuera del rango disponible (0-9).')
            
    def print_str(self, string:str, seconds:int|float = 1) -> None:
        '''Muestra las letras de una cadena (o una sola letra).
           Como una secuencia de letras de la cadena con el intervalo de tiempo
           entre letras determinado por el argumento `seconds` dado (default 1s).\n
           Nota: si una letra no está disponible, un guión (-) será mostrado. Si existe un espacio entre
           la cadena, el display lo mostrará apagándose.'''
        L_A = [self.__a, self.__b, self.__c, self.__e, self.__f, self.__g]
        L_b = [self.__c, self.__d, self.__e, self.__f, self.__g]
        L_c = [self.__d, self.__e, self.__g]
        L_d = [self.__b, self.__c, self.__d, self.__e, self.__g]
        L_E = [self.__a, self.__d, self.__e, self.__f, self.__g]
        L_F = [self.__a, self.__e, self.__f, self.__g]
        L_g = [self.__a, self.__b, self.__c, self.__d, self.__f, self.__g]
        L_H = [self.__b, self.__c, self.__e, self.__f, self.__g]
        L_h = [self.__c, self.__e, self.__f, self.__g]
        L_I = [self.__e, self.__f]
        L_i = [self.__e]
        L_J = [self.__b, self.__c, self.__d, self.__e]
        L_L = [self.__d, self.__e, self.__f]
        L_o = [self.__c, self.__d, self.__e, self.__g]
        L_P = [self.__a, self.__b, self.__e, self.__f, self.__g]
        L_u = [self.__c, self.__d, self.__e]
        L_U = [self.__b, self.__c, self.__d, self.__e, self.__f]
        L_r = [self.__e, self.__f, self.__g]
        L_S = [self.__a, self.__c, self.__d, self.__f, self.__g]
        if isinstance(string, str):
            AVAILABLE_CHARS = {'A':L_A, 'a':L_A, 'B':L_b, 'b':L_b,'C':L_c, 'c':L_c,'D':L_d, 'd':L_d, 'E':L_E,
                               'e':L_E, 'F':L_F, 'f':L_F, 'G':L_g,'g':L_g, 'H':L_H,'h':L_h, 'I':L_I,'i':L_i,
                               'J':L_J, 'j':L_J, 'L':L_L,'l':L_L, 'O':L_o, 'o':L_o, 'P':L_P, 'p':L_P,'R':L_r,
                               'r':L_r,'S':L_S,'s':L_S, 'U':L_U, 'u':L_u}
            for char in string:
                if char.isspace():
                    self.display_off()
                    sleep(seconds)
                else:
                    segments_on = AVAILABLE_CHARS.get(char, [self.__g]) 
                    for segment in self.__SEGMENTS:
                        segment.value(self.__state_on if segment in segments_on else self.__state_off)
                    sleep(seconds)
        else:
            raise ValueError("El argumento deve ser una cadena.")
        
    def print_custom_char(self, custom_char:list[Pin]) -> None:
        '''Muestra un caracter personalizado.\n
           El argumento `custom_char` debe ser una lista de objetos (segmentos) de la clase Pin.\n
           >>> from machine import Pin 
           >>> a = Pin(0, Pin.OUT)
           >>> g = Pin(1, Pin.OUT)
           >>> d = Pin(2, Pin.OUT)
           >>> custom_char = [a, g, d]'''
        for segment in self.__SEGMENTS:
                    segment.value(self.__state_on if segment in custom_char else self.__state_off)
                    
    def display_off(self, segment:list[str]|str = "all") -> None:
        '''Apaga todos los segmentos si no se especifica ninguno de estos.\n
           Si quiere especificar un segmento o varios debe hacerlo en forma de caracter o lista (string).\n
           Ejemplo:
           >>> segment = 'a'
           >>> segment = "abc"
           >>> segment = ['a', 'b', 'c']
           '''
        if segment == "all":
            for seg in self.__SEGMENTS:
                seg.value(self.__state_off)
        else:
            if isinstance(segment, str) or isinstance(segment, list):
                LOW_SEGMENTS = {'a':self.__a, 'b':self.__b, 'c':self.__c, 'd':self.__d, 'e':self.__e, 'f':self.__f, 'g':self.__g}
                if all(s.lower() in LOW_SEGMENTS for s in segment):
                    for s in segment:
                        seg = LOW_SEGMENTS[s.lower()]
                        seg.value(self.__state_off)
                else:
                    raise ValueError('Segmento no válido.')
            else:
                raise ValueError('El argumento segment debe ser una lista o una cadena.')
        
    def display_on(self, segment:list[str]|str = 'all') -> None:
        '''Enciende todos los segmentos si no se especifica ninguno de estos.\n
           Si quiere especificar un segmento o varios debe hacerlo en forma de cadena o lista (string).\n
           Ejemplo:
           >>> segment = 'a'
           >>> segment = "abc"
           >>> segment = ['a', 'b', 'c']
           '''
        if segment == 'all':
            for seg in self.__SEGMENTS:
                seg.value(self.__state_on)
        else:
            if isinstance(segment, (str, list)):
                HIGH_SEGMENTS = {'a':self.__a, 'b':self.__b, 'c':self.__c, 'd':self.__d, 'e':self.__e, 'f':self.__f, 'g':self.__g}
                if all(s.lower() in HIGH_SEGMENTS for s in segment):
                    for s in segment:
                        seg = HIGH_SEGMENTS[s.lower()]
                        seg.value(self.__state_on)
                else:
                    raise ValueError('Segmento no válido.')
            else:
                raise ValueError('El argumento segment debe ser una lista o una cadena.')
            
        
    def display_spiral(self, seconds:float|int = .1, reverse = False) -> None:
        '''Los segmentos encienden en forma de espiral.\n
           El argumento `reverse` determina si inicia de reversa (True) o no (False).
           El argumento `seconds` determina el tiempo de encendido entre los segmentos (default 0.1s).'''
        SPIRAL_SEGMENTS = [self.__g, self.__f, self.__a, self.__b, self.__c, self.__d, self.__e]
        if not reverse:
            for segment in SPIRAL_SEGMENTS:
                segment.value(self.__state_on)
                sleep(seconds)
        else:
            for segment in reversed(SPIRAL_SEGMENTS):
                segment.value(self.__state_on)
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
