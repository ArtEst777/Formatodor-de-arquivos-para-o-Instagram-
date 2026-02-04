"""
image_processor.py - Processador de imagens COMPLETO
"""

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import os
from datetime import datetime

from .core import FORMATS, QUALITY_LEVELS, INPUT_DIR, OUTPUT_DIR, BACKGROUND_COLORS

class ImageProcessor:
    """Processador de imagens com TODOS os formatos"""
    
    def resize_with_format(self, image_path, output_format, quality_level='high', method='fit'):
        """
        Redimensiona imagem SEM DISTORÇÃO para formato escolhido
        """
        try:
            filename = os.path.basename(image_path)
            print(f"\n📸 Processando: {filename}")
            
            with Image.open(image_path) as img:
                original_size = (img.width, img.height)
                original_ratio = img.width / img.height
                
                print(f"   📏 Original: {original_size[0]}x{original_size[1]}")
                print(f"   📐 Proporção: {original_ratio:.2f}:1")
                
                # Converter para RGB se necessário
                if img.mode != 'RGB':
                    if img.mode == 'RGBA':
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    else:
                        img = img.convert('RGB')
                
                # Obter tamanho alvo
                target_size = FORMATS.get(output_format, (1080, 1080))
                target_ratio = target_size[0] / target_size[1]
                
                print(f"   🎯 Alvo: {target_size[0]}x{target_size[1]} ({output_format})")
                print(f"   📐 Proporção alvo: {target_ratio:.2f}:1")
                print(f"   ⚙️  Método: {method}")
                
                # Método 1: FIT - Mantém proporção, adiciona bordas
                if method == 'fit':
                    print("   🔄 Método FIT: Mantendo proporção com bordas")
                    
                    # Calcular novo tamanho mantendo proporção
                    if original_ratio > target_ratio:
                        # Imagem é mais larga que o alvo
                        new_width = target_size[0]
                        new_height = int(target_size[0] / original_ratio)
                    else:
                        # Imagem é mais alta que o alvo
                        new_height = target_size[1]
                        new_width = int(target_size[1] * original_ratio)
                    
                    # Redimensionar mantendo proporção
                    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Criar imagem final com fundo
                    bg_color = BACKGROUND_COLORS['instagram']
                    final_img = Image.new('RGB', target_size, bg_color)
                    
                    # Centralizar imagem no fundo
                    offset = ((target_size[0] - new_width) // 2,
                             (target_size[1] - new_height) // 2)
                    final_img.paste(img_resized, offset)
                    
                    img = final_img
                
                # Método 2: CROP - Corta para encaixar perfeitamente
                elif method == 'crop':
                    print("   🔄 Método CROP: Cortando para encaixar perfeitamente")
                    
                    # Calcular área de corte
                    if original_ratio > target_ratio:
                        # Imagem é mais larga - cortar laterais
                        new_height = img.height
                        new_width = int(img.height * target_ratio)
                        left = (img.width - new_width) // 2
                        top = 0
                    else:
                        # Imagem é mais alta - cortar topo/baixo
                        new_width = img.width
                        new_height = int(img.width / target_ratio)
                        left = 0
                        top = (img.height - new_height) // 2
                    
                    # Aplicar corte
                    img_cropped = img.crop((left, top, left + new_width, top + new_height))
                    
                    # Redimensionar para tamanho exato
                    img = img_cropped.resize(target_size, Image.Resampling.LANCZOS)
                
                # Melhorar qualidade
                if quality_level in ['high', 'ultra']:
                    print("   ✨ Aplicando melhorias de qualidade")
                    img = self.enhance_image(img, quality_level)
                
                # Preparar pasta de saída
                if output_format == 'stories':
                    output_folder = os.path.join(OUTPUT_DIR, 'stories')
                elif output_format == 'reels':
                    output_folder = os.path.join(OUTPUT_DIR, 'reels')
                else:
                    output_folder = os.path.join(OUTPUT_DIR, 'feed')
                
                os.makedirs(output_folder, exist_ok=True)
                
                # Gerar nome do arquivo
                name, ext = os.path.splitext(filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_name = f"{name}_{output_format}_{quality_level}_{method}_{timestamp}.jpg"
                output_path = os.path.join(output_folder, output_name)
                
                # Salvar com qualidade
                quality_value = QUALITY_LEVELS.get(quality_level, 92)
                img.save(output_path, 'JPEG', 
                        quality=quality_value, 
                        optimize=True,
                        progressive=True)
                
                print(f"   ✅ CONVERTIDO: {output_name}")
                print(f"   📁 Salvo em: {output_folder}")
                
                return output_path
                
        except Exception as e:
            print(f"   ❌ ERRO: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def enhance_image(self, img, quality_level='high'):
        """Melhora qualidade da imagem"""
        if quality_level in ['high', 'ultra']:
            img = img.filter(ImageFilter.UnsharpMask(
                radius=1.5, percent=120, threshold=2
            ))
            
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.05)
            
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.02)
            
            if quality_level == 'ultra':
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.03)
        
        return img
    
    def convert_all_images(self, output_format, quality_level='high', method='fit'):
        """Converte TODAS as imagens para formato especificado"""
        imagens = [f for f in os.listdir(INPUT_DIR) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))]
        
        if not imagens:
            print("📭 Nenhuma imagem encontrada")
            return []
        
        print(f"\n📸 CONVERTENDO TODAS AS {len(imagens)} IMAGENS")
        print(f"   Formato: {output_format}")
        print(f"   Método: {method}")
        print(f"   Qualidade: {quality_level}")
        
        resultados = []
        falhas = []
        
        for i, filename in enumerate(imagens, 1):
            print(f"\n[{i}/{len(imagens)}] {filename}")
            caminho = os.path.join(INPUT_DIR, filename)
            
            resultado = self.resize_with_format(caminho, output_format, quality_level, method)
            if resultado:
                resultados.append(resultado)
            else:
                falhas.append(filename)
        
        # Relatório
        print(f"\n{'='*50}")
        print("📊 RELATÓRIO DE IMAGENS")
        print(f"{'='*50}")
        print(f"✅ Convertidas: {len(resultados)}/{len(imagens)}")
        
        if output_format == 'stories':
            print(f"📁 Salvas em: {os.path.join(OUTPUT_DIR, 'stories')}")
        elif output_format == 'reels':
            print(f"📁 Salvas em: {os.path.join(OUTPUT_DIR, 'reels')}")
        else:
            print(f"📁 Salvas em: {os.path.join(OUTPUT_DIR, 'feed')}")
        
        if falhas:
            print(f"❌ Falhas: {len(falhas)}")
            for f in falhas:
                print(f"   - {f}")
        
        return resultados