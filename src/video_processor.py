"""
video_processor.py - Processamento de vídeos ATUALIZADO
"""

import cv2
import os
from datetime import datetime
import subprocess
import sys

from .core import FORMATS, OUTPUT_DIR, INPUT_DIR

class VideoProcessor:
    """Processador de vídeos para Instagram"""
    
    def resize_with_format(self, video_path, output_format, quality='high'):
        """
        Redimensiona vídeo para o formato ESCOLHIDO
        """
        try:
            filename = os.path.basename(video_path)
            print(f"\n🎥 Processando: {filename}")
            
            # Abrir vídeo
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print("   ❌ Não foi possível abrir o vídeo")
                return None
            
            # Obter informações
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            print(f"   📏 Original: {width}x{height}")
            print(f"   🎞️  FPS: {fps} | Frames: {total_frames}")
            
            # Obter tamanho alvo
            target_size = FORMATS.get(output_format, (1080, 1920))
            print(f"   🎯 Alvo: {target_size[0]}x{target_size[1]} ({output_format})")
            
            # Preparar pasta de saída
            if output_format == 'stories':
                output_folder = os.path.join(OUTPUT_DIR, 'stories')
            elif output_format == 'reels':
                output_folder = os.path.join(OUTPUT_DIR, 'reels')
            else:
                output_folder = os.path.join(OUTPUT_DIR, 'feed')
            
            os.makedirs(output_folder, exist_ok=True)
            
            # Gerar nome do arquivo
            name, _ = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_name = f"{name}_{output_format}_{quality}_{timestamp}.mp4"
            output_path = os.path.join(output_folder, output_name)
            
            # Configurar codec
            if sys.platform == 'win32':
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            else:
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            
            # Configurar writer
            out = cv2.VideoWriter(output_path, fourcc, fps, target_size)
            
            frame_count = 0
            print("   🔄 Processando", end="", flush=True)
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Redimensionar frame
                resized = cv2.resize(frame, target_size, cv2.INTER_LINEAR)
                out.write(resized)
                
                frame_count += 1
                if frame_count % 30 == 0:
                    print(".", end="", flush=True)
            
            # Finalizar
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            
            print(f"\n   ✅ VÍDEO CONVERTIDO: {output_name}")
            print(f"   📊 Frames processados: {frame_count}")
            
            # Verificar tamanho do arquivo
            if os.path.exists(output_path):
                size_mb = os.path.getsize(output_path) / (1024 * 1024)
                print(f"   💾 Tamanho final: {size_mb:.1f} MB")
            
            return output_path
            
        except Exception as e:
            print(f"\n   ❌ ERRO: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def convert_all_videos(self, output_format, quality='high'):
        """Converte TODOS os vídeos para o formato escolhido"""
        videos = [f for f in os.listdir(INPUT_DIR) 
                 if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))]
        
        if not videos:
            print("📭 Nenhum vídeo encontrado")
            return []
        
        print(f"\n🎥 CONVERTENDO TODOS OS {len(videos)} VÍDEOS")
        print(f"   Formato: {output_format}")
        print(f"   Qualidade: {quality}")
        
        resultados = []
        falhas = []
        
        for i, filename in enumerate(videos, 1):
            print(f"\n[{i}/{len(videos)}] {filename}")
            caminho = os.path.join(INPUT_DIR, filename)
            
            resultado = self.resize_with_format(caminho, output_format, quality)
            if resultado:
                resultados.append(resultado)
            else:
                falhas.append(filename)
        
        # Relatório
        print(f"\n{'='*50}")
        print("📊 RELATÓRIO DE VÍDEOS")
        print(f"{'='*50}")
        print(f"✅ Convertidos: {len(resultados)}/{len(videos)}")
        
        if output_format == 'stories':
            print(f"📁 Salvos em: {os.path.join(OUTPUT_DIR, 'stories')}")
        elif output_format == 'reels':
            print(f"📁 Salvos em: {os.path.join(OUTPUT_DIR, 'reels')}")
        else:
            print(f"📁 Salvos em: {os.path.join(OUTPUT_DIR, 'feed')}")
        
        if falhas:
            print(f"❌ Falhas: {len(falhas)}")
            for f in falhas:
                print(f"   - {f}")
        
        return resultados