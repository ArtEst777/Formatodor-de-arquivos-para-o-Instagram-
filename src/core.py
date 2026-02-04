"""
core.py - Configurações essenciais COMPLETAS
"""

import os

# Configurações do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "inputs")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Formatos do Instagram COMPLETOS
FORMATS = {
    # Feed Principal
    'feed_square': (1080, 1080),        # 1:1
    'feed_portrait': (1080, 1350),      # 4:5
    'feed_landscape': (1080, 566),      # 1.91:1
    
    # Stories & Reels
    'stories': (1080, 1920),            # 9:16
    'reels': (1080, 1920),              # 9:16
    
    # IGTV (agora integrado)
    'igtv_portrait': (1080, 1920),      # 9:16
    'igtv_landscape': (1920, 1080),     # 16:9
    
    # Carrossel (pode variar, usar primeiro slide como referência)
    'carousel_square': (1080, 1080),
    'carousel_portrait': (1080, 1350),
    'carousel_landscape': (1080, 566),
    
    # Perfil
    'profile_pic': (360, 360),          # Aparece como 110x110
    'profile_cover': (1080, 1920),      # Destaques
}

# Níveis de qualidade
QUALITY_LEVELS = {
    'low': 80,      # Para web rápida
    'medium': 88,   # Balanço qualidade/tamanho
    'high': 92,     # Para impressão/mostrar detalhes
    'ultra': 96     # Qualidade máxima
}

# Configurações de processamento
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff', '.gif']
SUPPORTED_VIDEO_FORMATS = ['.mp4', '.mov', '.avi', '.mkv', '.webm', '.flv']

# Cores de fundo padrão (RGB)
BACKGROUND_COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'instagram': (250, 250, 250),  # Branco do Instagram
    'dark_mode': (18, 18, 18),     # Para modo escuro
}

# Configurações de vídeo
VIDEO_CODECS = {
    'mp4': 'mp4v',
    'avi': 'XVID',
    'mov': 'mp4v'
}

# Configurações de FPS
DEFAULT_FPS = 30
MIN_FPS = 15
MAX_FPS = 60