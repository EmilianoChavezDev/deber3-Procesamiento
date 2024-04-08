import numpy as np
import cv2

class ImageProcessingManager():
  """
    Esta libreria contiene la implementación de los procesos internos del
    Editor de Imagenes.
    Desarrollador por: 
  """

  DEFAULT_WIDTH = 512
  DEFAULT_HEIGHT = 512

  def __init__(self):
    super(ImageProcessingManager, self).__init__()

    # Por defecto tenemos una imagen blanca en la pila.
    initial_matrix = np.ones((self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT, 3), np.uint8) * 255
    
    # Estructura de imagenes
    self.stack_images = [initial_matrix]
    
    # Estructura de puntos/lineas
    self.stack_lines = []

  
  def rgb_to_hex(self, rgb):
    """
      Conversor de un string hexadecimal a arreglos.
      Fuente: https://www.codespeedy.com/convert-rgb-to-hex-color-code-in-python/
    """
    return '%02x%02x%02x' % rgb

  def last_image(self):
    """
      NO ALTERAR ESTA FUNCION
      Obtenemos la ultima imagen de nuestra estructura.
    """
    return self.stack_images[-1]

  def can_undo(self):
    """
      NO ALTERAR ESTA FUNCION
      Determinamos si la aplicación puede eliminar
      elementos de la pila.
      Debe haber por lo menos más de un elemento para que 
      se pueda deshacer la imagen
    """
    return len(self.stack_images) > 1

  def has_changes(self):
    """
      NO ALTERAR ESTA FUNCION
      Determinamos si la aplicación contiene
      elementos de la pila.
    """
    return len(self.stack_images) > 1

  def add_image(self, image_path):
      self.stack_images.clear();
      imagen = cv2.imread(image_path)
      imagen_redimensionada = cv2.resize(imagen, (self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT))
      self.stack_images.append(imagen_redimensionada)
      
    
  def save_image(self, filename):
    cv2.imwrite(filename, self.stack_images[-1])
    pass

  def undo_changes(self):
    """
      Eliminamos el ultimo elemento guardado.
    """
    self.stack_images.pop()
    pass


  def save_points(self, x1, y1, x2, y2, line_width, color):
    """
      Guardamos informacion de los puntos aqui en self.stack_lines.
    """
    self.stack_lines.append((x1, y1, x2, y2, line_width, color))
    pass

  def add_lines_to_image(self):
        """
        Creamos una matriz, con un conjunto de lineas.
        Estas lineas se obtienen de self.stack_lines.

        Finalmente guardamos a nuestra pila de imagenes: self.stack_images.

        Ayuda: ver documentacion de "cv2.line" para dibujar lineas en una matriz
        Ayuda 2: no se olviden de limpiar self.stack_lines
        Ayuda 3: utilizar el metodo rgb_to_hex para convertir los colores
        """
        image = self.stack_images[-1].copy()
        for x1, y1, x2, y2, line_width, color in self.stack_lines:
            cv2.line(image, (x1, y1), (x2, y2), self.rgb_to_hex(color), line_width)
        self.stack_images.append(image)      
        self.stack_lines.clear()

  def black_and_white_image(self):
        """
        Hacemos una copia de la ultima imagen.
        La Convertimos a blanco y negro.
        Guardamos a la estructura self.stack_images
        Retornamos la imagen procesada.
        """
        last = self.stack_images[-1].copy()
        gray = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY) 
        self.stack_images.append(gray)
        return gray




  def negative_image(self):
    """
      Hacemos una copia de la ultima imagen.
      Calculamos el negativo de la imagen.
      Guardamos a la estructura self.stack_images
      Retornamos la imagen procesada.
    """

    last = self.stack_images[-1].copy()
    # Calculamos el negativo de la imagen
    negative_image = 255 - last
    self.stack_images.append(negative_image)
    return negative_image

  def global_equalization_image(self):
    """
      Hacemos una copia de la ultima imagen.
      Equalizamos la imagen.
      Guardamos a la estructura self.stack_images
      Retornamos la imagen procesada.
    """

    last = self.stack_images[-1].copy()
    # Convertimos la imagen a escala de grises si no lo está
    gray_image = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY)
    # Equalizamos la imagen
    equalized_image = cv2.equalizeHist(gray_image)
    self.stack_images.append(cv2.cvtColor(equalized_image, cv2.COLOR_GRAY2BGR))
    return equalized_image
  
  
  
  def CLAHE_equalization_image(self, grid=(8, 8), clipLimit=2.0):
    """
      Hacemos una copia de la ultima imagen.
      Equalizamos la imagen usando el algoritmo de CLAHE.
      Guardamos a la estructura self.stack_images
      Retornamos la imagen procesada.
    """
    last = self.stack_images[-1].copy()
    # Convertimos la imagen a escala de grises si no lo está
    gray_image = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY)
    # Creamos el objeto CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=grid)
    # Aplicamos la equalización adaptativa del histograma con CLAHE
    clahe_equalized_image = clahe.apply(gray_image)
    # Convertimos la imagen de nuevo a color
    colored_clahe_equalized_image = cv2.cvtColor(clahe_equalized_image, cv2.COLOR_GRAY2BGR)
    self.stack_images.append(colored_clahe_equalized_image)
    return colored_clahe_equalized_image


  def contrast_and_brightness_processing_image(self, alpha, beta):
    """
      Hacemos una copia de la ultima imagen.
      Ajustamos la imagen segun parametros alpha y beta.
      Guardamos a la estructura self.stack_images
      Retornamos la imagen procesada.
    """

    last = self.stack_images[-1].copy()
    # Ajustamos el contraste y brillo de la imagen
    adjusted_image = cv2.convertScaleAbs(last, alpha=alpha, beta=beta)
    self.stack_images.append(adjusted_image)
    return adjusted_image