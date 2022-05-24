
from tkinter import  Tk, Button, Entry, Label, messagebox, PhotoImage
from tkinter import  StringVar,Frame
import random


class Wordle(Frame):
    def __init__(self, master):
        super().__init__(master)
        #variables
        self.fila = 0 #filas
        #colores de la interface
        self.verde = "#19C065"
        self.naranajado = "#E3B30E"
        self.gris = "#8F8E8C"
        self.texto = StringVar() #texto a ingresar
        self.texto.trace("w",lambda *args: self.limitar(self.texto)) #llamada a la funcio para limitar la cantidad de letras
        self.create_widgets() #metodo para los 3 frames (titulo, letras(framewokrs), botones)
        self.palabra_aleatoria() #metodo para generar palabra a buscar

    def create_widgets(self):
        #frames
        self.frame_titulo = Frame(self.master, bg='black', width=400, height=100)#frame titulo
        self.frame_titulo.grid_propagate(0)
        self.frame_titulo.grid(column=0, row=0, sticky='snew')
        self.frame_cuadros = Frame(self.master, bg='black', width=500, height=500)#frame cuadros de las letras
        self.frame_cuadros.grid_propagate(0)
        self.frame_cuadros.grid(column=0, row=1, sticky='snew')
        self.frame_control = Frame(self.master, bg='black', width=400, height=100)#frame abajo, botones y texto
        self.frame_control.grid_propagate(0)
        self.frame_control.grid(column=0, row=2, sticky='snew')
        
        
        #label titulo
        Label(self.frame_titulo, bg='black', fg='white', text= 'WORDLE', width=30 ,font=('Arial',25,'bold')).pack(side='top') 

        #WIDGETS
        #Verifica si la palabra esta en la BD
        self.signal = Label(self.frame_control, bg='black', fg='white', text='Palabra: ', font=('Arial',12))
        self.signal.pack(side = 'left',expand=True)#posicion
        #Ingreso de palabra
        self.palabra = Entry(self.frame_control, font=('Arial',15), justify='center', textvariable= self.texto, fg='black', highlightcolor="green2", 
        highlightthickness=2, width=7)
        self.palabra.pack(side='left', expand=True)
        #Boton Enviar
        self.enviar = Button(self.frame_control, text='Enviar', bg='gray50', activebackground='green2', fg='white', font=('Arial',12,'bold'),
        command=self.verificar_palabra)#ejecutar metodo verificar palabra
        self.enviar.pack(side='left', expand=True)
        #Boton Borrar
        self.limpiar = Button(self.frame_control, text= '⌫', bg='gray50',activebackground='green2', fg = 'white', 
        font=('Arial', 12,'bold'), width=4, command= lambda:self.texto.set(''))
        self.limpiar.pack(side='left', expand=True) 
        #Boton Reglas
        self.reglas = Button(self.frame_control, text='?', bg='gray50', activebackground='green2', fg='white', font=('Arial',12,'bold'),
        command=self.verificar_reglas)#ejecutar metodo mostrar reglas
        self.reglas.pack(side='left', expand=True)
    
    def limitar(self,texto): #delimitar letras
        if len(texto.get()) > 0:
            texto.set(texto.get()[:5]) #solo 5 letras
    
    def palabra_aleatoria(self): #seleccionar palabra de la bd
        archivo = open('lista.txt','r', encoding="utf-8") #permite la ñ , r = leer archivo
        self.lista = archivo.readlines() #objt para crear una lista del archivo
        self.p_a = random.choice(self.lista).rstrip('\n') #obj para obtener la palabra
    
    def verificar_palabra(self): #compara las palabras
        palabra = self.texto.get().upper() #extrae la palabra a buscar y mayusculas
        x = list(filter(lambda x: palabra in x, self.lista)) #verifica que la palabra ingresada este en la BBDD
        if len(x)==1 and len(palabra)==5: #se encuentre y tamaño 5
            self.signal['text'] = ''
            print(self.p_a, palabra)
            if self.fila <= 6: #solo 6 intentos
                for i, letra in enumerate (palabra): #letra por letra
                    self.cuadros = Label(self.frame_cuadros, width=4, fg='white',
                        bg=self.gris, text= letra, font=('Geometr706 BlkCn BT', 25, 'bold'))#label de los cuadraditos de cada letra
                    self.cuadros.grid(column=i, row=self.fila, padx=5, pady=5)
                    
                    if letra == self.p_a[i]: # si la letra esta en la posicion correcta VERDE
                        self.cuadros['bg'] = self.verde
                    
                    if letra in self.p_a and not letra == self.p_a[i]: # si la letra se encuentra pero no esta en su posicion NARANJA
                        self.cuadros['bg'] = self.naranajado
                    
                    if letra not in self.p_a: #no se encuentra la letra GRIS
                        self.cuadros['bg'] = self.gris

            self.fila = self.fila + 1 #de 0 a 4
            if self.fila <= 6 and self.p_a == palabra: #condicion de ganador
                messagebox.showinfo('GANASTE', '¡FELICIDADES!')
                self.master.destroy()
                self.master.quit()

            if self.fila == 6 and self.p_a != palabra:#condicion de perdio
                messagebox.showinfo('PERDISTE', 'INTENTALO DE NUEVO')
                self.master.destroy()
                self.master.quit()
        else: #la palabra ingreseada no se encuentra en la BBDD
            self.signal['text'] = 'No esta en la BD'
            
    def verificar_reglas(self):
        print ("Reglas")
        newWindow = Tk()
        newWindow.resizable(0,0) #no redimensionar
        newWindow.config(bg='black') #bkg
        newWindow.title("Reglas") 
        newWindow.geometry("450x450") 
        self.rules = Label(self.frame_control, bg='black', fg='white', text='Adivina la palabra oculta en seis intentos\nCada intento debe ser una palabra válida de 5 letras\nDespués de cada intento el color de las letras cambia para mostrar qué tan cerca estás de acertar la palabra.', font=('Arial',12))
        self.rules.pack(side = 'left',expand=True)#posicion
        
        

if __name__ == "__main__":
	ventana = Tk()
	ventana.config(bg='black') #bkg
	ventana.call('wm', 'iconphoto', ventana._w, PhotoImage(file='logo.png'))#logo
	ventana.geometry('610x640+700+80') #tamaño ventana
	ventana.resizable(0,0) #no redimensionar
	ventana.title('Wordle')
	app = Wordle(ventana)
	app.mainloop()