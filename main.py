#!/usr/bin/env python3
"""
main.py - Instagram Automator COMPLETO
✅ IMAGENS: Feed, Stories, Reels
✅ VÍDEOS: Feed, Stories, Reels
✅ SEM distorção de imagens
✅ Métodos FIT e CROP
"""

import os
import sys

print("=" * 60)
print("         INSTAGRAM AUTOMATOR - VERSÃO COMPLETA")
print("=" * 60)
print("✅ IMAGENS: Feed, Stories, Reels")
print("✅ VÍDEOS: Feed, Stories, Reels")
print("✅ SEM distorção de imagens")
print("=" * 60)

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

try:
    from src.image_processor import ImageProcessor
    from src.video_processor import VideoProcessor
    from src.core import INPUT_DIR, OUTPUT_DIR, FORMATS
    print("✅ Módulos carregados com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar: {e}")
    print("\n📦 Instale dependências: pip install Pillow opencv-python")
    sys.exit(1)

def criar_pastas():
    """Cria pastas necessárias"""
    pastas = [INPUT_DIR, OUTPUT_DIR, 
              os.path.join(OUTPUT_DIR, 'feed'),
              os.path.join(OUTPUT_DIR, 'stories'),
              os.path.join(OUTPUT_DIR, 'reels')]
    
    for pasta in pastas:
        if not os.path.exists(pasta):
            os.makedirs(pasta)
            print(f"📂 Criada: {pasta}")

def verificar_arquivos():
    """Verifica todos os arquivos disponíveis"""
    if not os.path.exists(INPUT_DIR):
        return [], []
    
    arquivos = os.listdir(INPUT_DIR)
    imagens = [f for f in arquivos if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))]
    videos = [f for f in arquivos if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))]
    
    return imagens, videos

def mostrar_menu_formatos(tipo='ambos'):
    """Menu de formatos para escolha manual"""
    print("\n" + "=" * 50)
    print("🎯 ESCOLHA O FORMATO")
    print("=" * 50)
    print()
    
    if tipo in ['imagens', 'ambos']:
        print("📱 FEED (para postagens):")
        print("  1. 📐 Quadrado (1080x1080)")
        print("  2. 📱 Retrato (1080x1350)")
        print("  3. 🏞️  Paisagem (1080x566)")
        print()
        print("📲 VERTICAL (tela cheia):")
        print("  4. 📖 Stories (1080x1920)")
        print("  5. 🎬 Reels (1080x1920)")
        print()
    
    if tipo in ['videos', 'ambos']:
        print("🎥 VÍDEOS (mesmas opções acima)")
        print()
    
    print("⚡ OPÇÕES AVANÇADAS:")
    print("  6. 🔄 Converter TUDO para Feed (força conversão)")
    print("  7. 🔄 Converter TUDO para Stories/Reels")
    print("  8. 🎯 Escolher formato ESPECÍFICO")
    print()
    print("  0. ↩️  Voltar")
    print()

def mostrar_menu_principal():
    """Menu principal completo"""
    print("\n" + "=" * 60)
    print("🚀 MENU PRINCIPAL - INSTAGRAM AUTOMATOR")
    print("=" * 60)
    print()
    print("1. 📸 Processar apenas IMAGENS")
    print("2. 🎥 Processar apenas VÍDEOS")
    print("3. 🔄 Processar TUDO (imagens + vídeos)")
    print("4. 📊 Ver arquivos disponíveis")
    print("5. ⚙️  Configurações")
    print("6. 🚪 Sair")
    print()
    
    imagens, videos = verificar_arquivos()
    
    if imagens or videos:
        print("📁 ARQUIVOS DISPONÍVEIS:")
        if imagens:
            print(f"   📸 Imagens: {len(imagens)}")
        if videos:
            print(f"   🎥 Vídeos: {len(videos)}")
        print()
    else:
        print("📁 Pasta 'inputs/': VAZIA (coloque arquivos primeiro)")
        print()

def mostrar_menu_qualidade():
    """Menu de qualidade"""
    print("\n🎚️  NÍVEL DE QUALIDADE:")
    print("1. 🟢 Baixa (80) - Web rápido")
    print("2. 🟡 Média (88) - Padrão")
    print("3. 🔴 Alta (92) - Recomendado")
    print("4. 💎 Ultra (96) - Máxima")
    print("5. ⚡ Padrão (Alta)")

def escolher_qualidade():
    """Permite escolher a qualidade"""
    mostrar_menu_qualidade()
    escolha = input("\n👉 Qualidade (1-5, padrão=3): ").strip()
    qualidades = {'1': 'low', '2': 'medium', '3': 'high', '4': 'ultra'}
    return qualidades.get(escolha, 'high')

def mostrar_menu_metodo():
    """Menu para escolher método de redimensionamento"""
    print("\n🎯 MÉTODO DE REDIMENSIONAMENTO")
    print("=" * 30)
    print()
    print("1. 🔲 FIT - Mantém proporção original")
    print("   • Adiciona bordas se necessário")
    print("   • NUNCA distorce a imagem")
    print("   • Recomendado para fotos importantes")
    print()
    print("2. ✂️  CROP - Corta para encaixar perfeitamente")
    print("   • Remove bordas da imagem")
    print("   • Encaixa exatamente no formato")
    print("   • Pode cortar partes da imagem")
    print()
    print("3. 🔄 Auto (FIT para feed, CROP para vertical)")
    print("   • Escolhe automaticamente o melhor método")
    print()

def escolher_metodo():
    """Permite escolher o método de redimensionamento"""
    mostrar_menu_metodo()
    
    while True:
        escolha = input("👉 Escolha o método (1-3): ").strip()
        
        if escolha == '1':
            return 'fit'
        elif escolha == '2':
            return 'crop'
        elif escolha == '3':
            return 'auto'
        else:
            print("❌ Escolha inválida")

def processar_imagens():
    """Processa imagens com escolha manual - INCLUI STORIES E REELS"""
    imagens, _ = verificar_arquivos()
    
    if not imagens:
        print("\n❌ Nenhuma imagem encontrada")
        print(f"💡 Coloque imagens em: {INPUT_DIR}")
        return
    
    print(f"\n📸 {len(imagens)} imagem(ns) encontrada(s)")
    
    while True:
        mostrar_menu_formatos('imagens')
        escolha = input("👉 Escolha (0-8): ").strip()
        
        if escolha == '0':
            return
        
        formatos = {
            '1': 'feed_square',
            '2': 'feed_portrait',
            '3': 'feed_landscape',
            '4': 'stories',
            '5': 'reels',
            '6': 'force_feed',
            '7': 'force_stories',
            '8': 'especifico'
        }
        
        formato = formatos.get(escolha)
        
        if formato:
            break
        print("❌ Escolha inválida")
    
    # Opção especial: converter tudo para feed
    if formato == 'force_feed':
        print("\n⚡ CONVERSÃO FORÇADA PARA FEED")
        print("Escolha o formato do feed:")
        print("1. Quadrado (1080x1080)")
        print("2. Retrato (1080x1350) - Recomendado")
        print("3. Paisagem (1080x566)")
        
        feed_escolha = input("👉 Escolha (1-3): ").strip()
        feed_map = {'1': 'feed_square', '2': 'feed_portrait', '3': 'feed_landscape'}
        feed_format = feed_map.get(feed_escolha, 'feed_portrait')
        
        # Escolher método
        metodo = escolher_metodo()
        
        qualidade = escolher_qualidade()
        processor = ImageProcessor()
        
        if metodo == 'auto':
            # FIT para feed
            metodo_para_usar = 'fit'
        else:
            metodo_para_usar = metodo
        
        processor.convert_all_images(feed_format, qualidade, metodo_para_usar)
        return
    
    # Opção especial: converter tudo para stories/reels
    if formato == 'force_stories':
        print("\n⚡ CONVERSÃO FORÇADA PARA STORIES/REELS")
        print("Escolha o formato vertical:")
        print("1. Stories (1080x1920)")
        print("2. Reels (1080x1920)")
        
        vert_escolha = input("👉 Escolha (1-2): ").strip()
        vert_map = {'1': 'stories', '2': 'reels'}
        vert_format = vert_map.get(vert_escolha, 'stories')
        
        # Escolher método
        metodo = escolher_metodo()
        
        qualidade = escolher_qualidade()
        processor = ImageProcessor()
        
        if metodo == 'auto':
            # CROP para vertical
            metodo_para_usar = 'crop'
        else:
            metodo_para_usar = metodo
        
        processor.convert_all_images(vert_format, qualidade, metodo_para_usar)
        return
    
    # Formato específico
    if formato == 'especifico':
        print("\n🎯 FORMATOS DISPONÍVEIS:")
        for key, (w, h) in FORMATS.items():
            print(f"  • {key}: {w}x{h}")
        
        formato_input = input("\n👉 Digite o formato (ex: stories, reels): ").strip()
        if formato_input not in FORMATS:
            print("❌ Formato inválido")
            return
        formato = formato_input
    
    # Escolher método
    metodo = escolher_metodo()
    
    # Escolher qualidade
    qualidade = escolher_qualidade()
    
    # Decidir método final
    if metodo == 'auto':
        # FIT para feed, CROP para vertical (stories/reels)
        if 'feed' in formato:
            metodo_final = 'fit'
        else:
            metodo_final = 'crop'
    else:
        metodo_final = metodo
    
    # Processar
    print(f"\n🎯 Formato: {formato}")
    print(f"📏 Dimensões: {FORMATS[formato][0]}x{FORMATS[formato][1]}")
    print(f"⚙️  Método: {metodo_final.upper()}")
    print(f"💎 Qualidade: {qualidade}")
    
    processor = ImageProcessor()
    resultados = []
    
    print(f"\n🚀 PROCESSANDO {len(imagens)} IMAGEM(NES)...")
    
    for i, img_nome in enumerate(imagens, 1):
        print(f"\n[{i}/{len(imagens)}] {img_nome}")
        caminho = os.path.join(INPUT_DIR, img_nome)
        
        resultado = processor.resize_with_format(caminho, formato, qualidade, metodo_final)
        if resultado:
            resultados.append(resultado)
    
    # Relatório
    print(f"\n{'='*60}")
    print("📊 RELATÓRIO FINAL - IMAGENS")
    print(f"{'='*60}")
    print(f"✅ Processadas: {len(resultados)}/{len(imagens)}")
    print(f"⚙️  Método usado: {metodo_final}")
    
    if resultados:
        if formato in ['stories', 'reels']:
            print(f"📁 Salvas em: {os.path.join(OUTPUT_DIR, 'stories' if formato == 'stories' else 'reels')}")
        else:
            print(f"📁 Salvas em: {os.path.join(OUTPUT_DIR, 'feed')}")

def processar_videos():
    """Processa vídeos com escolha manual - INCLUI STORIES E REELS"""
    _, videos = verificar_arquivos()
    
    if not videos:
        print("\n❌ Nenhum vídeo encontrado")
        print(f"💡 Coloque vídeos em: {INPUT_DIR}")
        return
    
    print(f"\n🎥 {len(videos)} vídeo(s) encontrado(s)")
    
    while True:
        mostrar_menu_formatos('videos')
        escolha = input("👉 Escolha (0-8): ").strip()
        
        if escolha == '0':
            return
        
        formatos = {
            '1': 'feed_square',
            '2': 'feed_portrait',
            '3': 'feed_landscape',
            '4': 'stories',
            '5': 'reels',
            '6': 'force_feed',
            '7': 'force_stories',
            '8': 'especifico'
        }
        
        formato = formatos.get(escolha)
        
        if formato:
            break
        print("❌ Escolha inválida")
    
    # Opção especial: converter tudo para feed
    if formato == 'force_feed':
        print("\n⚡ CONVERSÃO FORÇADA PARA FEED")
        print("Escolha o formato do feed:")
        print("1. Quadrado (1080x1080)")
        print("2. Retrato (1080x1350)")
        print("3. Paisagem (1080x566)")
        
        feed_escolha = input("👉 Escolha (1-3): ").strip()
        feed_map = {'1': 'feed_square', '2': 'feed_portrait', '3': 'feed_landscape'}
        feed_format = feed_map.get(feed_escolha, 'feed_portrait')
        
        qualidade = escolher_qualidade()
        processor = VideoProcessor()
        processor.convert_all_videos(feed_format, qualidade)
        return
    
    # Opção especial: converter tudo para stories/reels
    if formato == 'force_stories':
        print("\n⚡ CONVERSÃO FORÇADA PARA STORIES/REELS")
        print("Escolha o formato vertical:")
        print("1. Stories (1080x1920)")
        print("2. Reels (1080x1920)")
        
        vert_escolha = input("👉 Escolha (1-2): ").strip()
        vert_map = {'1': 'stories', '2': 'reels'}
        vert_format = vert_map.get(vert_escolha, 'stories')
        
        qualidade = escolher_qualidade()
        processor = VideoProcessor()
        processor.convert_all_videos(vert_format, qualidade)
        return
    
    # Formato específico
    if formato == 'especifico':
        print("\n🎯 FORMATOS DISPONÍVEIS:")
        for key, (w, h) in FORMATS.items():
            print(f"  • {key}: {w}x{h}")
        
        formato_input = input("\n👉 Digite o formato (ex: stories): ").strip()
        if formato_input not in FORMATS:
            print("❌ Formato inválido")
            return
        formato = formato_input
    
    # Qualidade
    qualidade = escolher_qualidade()
    
    # Processar
    print(f"\n🎯 Formato: {formato}")
    print(f"📏 Dimensões: {FORMATS[formato][0]}x{FORMATS[formato][1]}")
    print(f"💎 Qualidade: {qualidade}")
    
    processor = VideoProcessor()
    resultados = []
    
    print(f"\n🚀 PROCESSANDO {len(videos)} VÍDEO(S)...")
    print("⚠️  Processamento de vídeo pode demorar. Aguarde.")
    
    for i, vid_nome in enumerate(videos, 1):
        print(f"\n[{i}/{len(videos)}] {vid_nome}")
        caminho = os.path.join(INPUT_DIR, vid_nome)
        
        resultado = processor.resize_with_format(caminho, formato, qualidade)
        if resultado:
            resultados.append(resultado)
    
    # Relatório
    print(f"\n{'='*60}")
    print("📊 RELATÓRIO FINAL - VÍDEOS")
    print(f"{'='*60}")
    print(f"✅ Processados: {len(resultados)}/{len(videos)}")
    
    if resultados:
        if formato == 'stories':
            print(f"📁 Salvos em: {os.path.join(OUTPUT_DIR, 'stories')}")
        elif formato == 'reels':
            print(f"📁 Salvos em: {os.path.join(OUTPUT_DIR, 'reels')}")
        else:
            print(f"📁 Salvos em: {os.path.join(OUTPUT_DIR, 'feed')}")

def processar_tudo():
    """Processa TUDO (imagens + vídeos) automaticamente"""
    imagens, videos = verificar_arquivos()
    
    if not imagens and not videos:
        print("\n❌ Nenhum arquivo encontrado")
        return
    
    print(f"\n🚀 PROCESSANDO TUDO AUTOMATICAMENTE")
    print("=" * 50)
    
    total_imagens = len(imagens)
    total_videos = len(videos)
    
    print(f"📸 Imagens: {total_imagens}")
    print(f"🎥 Vídeos: {total_videos}")
    print(f"📊 Total: {total_imagens + total_videos} arquivos")
    
    # Perguntar formato
    print("\n🎯 ESCOLHA O FORMATO PARA TUDO:")
    print("1. Auto-detect (recomendado para cada arquivo)")
    print("2. Feed Quadrado (1080x1080)")
    print("3. Feed Retrato (1080x1350)")
    print("4. Feed Paisagem (1080x566)")
    print("5. Stories (1080x1920)")
    print("6. Reels (1080x1920)")
    
    escolha = input("\n👉 Escolha (1-6): ").strip()
    
    formatos_opcoes = {
        '1': 'auto',
        '2': 'feed_square',
        '3': 'feed_portrait',
        '4': 'feed_landscape',
        '5': 'stories',
        '6': 'reels'
    }
    
    formato = formatos_opcoes.get(escolha, 'auto')
    
    if formato == 'auto':
        print("\n🔍 Usando auto-detect para cada arquivo")
    else:
        print(f"\n🎯 Convertendo tudo para: {formato}")
    
    # Processar imagens
    if imagens:
        print(f"\n📸 PROCESSANDO {total_imagens} IMAGEM(NES)...")
        processor_img = ImageProcessor()
        
        for i, img in enumerate(imagens, 1):
            print(f"\n[{i}/{total_imagens}] {img}")
            caminho = os.path.join(INPUT_DIR, img)
            
            # Se formato='auto', detectar automaticamente
            if formato == 'auto':
                from PIL import Image
                with Image.open(caminho) as img_obj:
                    ratio = img_obj.width / img_obj.height
                    if ratio < 0.7:
                        formato_img = 'stories'
                    elif ratio < 0.9:
                        formato_img = 'feed_portrait'
                    elif ratio < 1.2:
                        formato_img = 'feed_square'
                    else:
                        formato_img = 'feed_landscape'
                
                # Método automático: FIT para feed, CROP para vertical
                if 'feed' in formato_img:
                    metodo_img = 'fit'
                else:
                    metodo_img = 'crop'
                
                print(f"   📐 Detectado: {formato_img} | Método: {metodo_img}")
                resultado = processor_img.resize_with_format(caminho, formato_img, 'high', metodo_img)
            else:
                # Método automático baseado no formato
                if 'feed' in formato:
                    metodo_img = 'fit'
                else:
                    metodo_img = 'crop'
                resultado = processor_img.resize_with_format(caminho, formato, 'high', metodo_img)
    
    # Processar vídeos
    if videos:
        print(f"\n🎥 PROCESSANDO {total_videos} VÍDEO(S)...")
        processor_vid = VideoProcessor()
        
        for i, vid in enumerate(videos, 1):
            print(f"\n[{i}/{total_videos}] {vid}")
            caminho = os.path.join(INPUT_DIR, vid)
            
            # Se formato='auto', detectar automaticamente
            if formato == 'auto':
                import cv2
                cap = cv2.VideoCapture(caminho)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                cap.release()
                
                ratio = width / height
                if ratio < 0.7:
                    formato_vid = 'stories'
                elif ratio < 0.9:
                    formato_vid = 'feed_portrait'
                elif ratio < 1.2:
                    formato_vid = 'feed_square'
                else:
                    formato_vid = 'feed_landscape'
                
                print(f"   📐 Detectado: {formato_vid} ({ratio:.2f}:1)")
                resultado = processor_vid.resize_with_format(caminho, formato_vid, 'high')
            else:
                resultado = processor_vid.resize_with_format(caminho, formato, 'high')
    
    print(f"\n✅ PROCESSAMENTO COMPLETO!")
    print(f"📁 Todos os arquivos em: {OUTPUT_DIR}")

def mostrar_arquivos():
    """Mostra todos os arquivos disponíveis"""
    imagens, videos = verificar_arquivos()
    
    if not imagens and not videos:
        print("\n📭 Pasta 'inputs/' vazia")
        print(f"💡 Coloque arquivos em: {INPUT_DIR}")
        return
    
    print(f"\n📁 ARQUIVOS DISPONÍVEIS")
    print("=" * 50)
    
    # Imagens
    if imagens:
        print(f"\n📸 IMAGENS ({len(imagens)}):")
        print("-" * 30)
        for i, img in enumerate(imagens[:10], 1):
            caminho = os.path.join(INPUT_DIR, img)
            tamanho_kb = os.path.getsize(caminho) / 1024 if os.path.exists(caminho) else 0
            print(f"{i:2d}. {img} ({tamanho_kb:.1f} KB)")
        
        if len(imagens) > 10:
            print(f"... e mais {len(imagens) - 10} imagens")
    
    # Vídeos
    if videos:
        print(f"\n🎥 VÍDEOS ({len(videos)}):")
        print("-" * 30)
        for i, vid in enumerate(videos[:5], 1):
            caminho = os.path.join(INPUT_DIR, vid)
            tamanho_mb = os.path.getsize(caminho) / (1024 * 1024) if os.path.exists(caminho) else 0
            print(f"{i:2d}. {vid} ({tamanho_mb:.1f} MB)")
        
        if len(videos) > 5:
            print(f"... e mais {len(videos) - 5} vídeos")
    
    # Estatísticas
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total arquivos: {len(imagens) + len(videos)}")
    print(f"   Pasta 'inputs/': {INPUT_DIR}")
    print(f"   Pasta 'outputs/': {OUTPUT_DIR}")

def menu_configuracoes():
    """Menu de configurações"""
    print("\n" + "=" * 50)
    print("⚙️  CONFIGURAÇÕES")
    print("=" * 50)
    print()
    print("1. 📁 Abrir pasta de inputs")
    print("2. 📁 Abrir pasta de outputs")
    print("3. 🧹 Limpar pasta de outputs")
    print("4. 📋 Informações do sistema")
    print("5. ↩️  Voltar")
    print()
    
    escolha = input("👉 Escolha (1-5): ").strip()
    
    if escolha == '1':
        os.system(f'explorer "{INPUT_DIR}"')
        print("✅ Pasta de inputs aberta")
    
    elif escolha == '2':
        os.system(f'explorer "{OUTPUT_DIR}"')
        print("✅ Pasta de outputs aberta")
    
    elif escolha == '3':
        confirmar = input("⚠️  Tem certeza? Isso apagará TODOS os arquivos processados! (s/n): ").strip().lower()
        if confirmar == 's':
            import shutil
            if os.path.exists(OUTPUT_DIR):
                shutil.rmtree(OUTPUT_DIR)
                os.makedirs(os.path.join(OUTPUT_DIR, 'feed'))
                os.makedirs(os.path.join(OUTPUT_DIR, 'stories'))
                os.makedirs(os.path.join(OUTPUT_DIR, 'reels'))
                print("✅ Pasta de outputs limpa")
    
    elif escolha == '4':
        print("\n📋 INFORMAÇÕES DO SISTEMA:")
        print(f"   Python: {sys.version}")
        print(f"   Diretório: {current_dir}")
        print(f"   Inputs: {INPUT_DIR}")
        print(f"   Outputs: {OUTPUT_DIR}")
        
        try:
            from PIL import Image, __version__ as pil_version
            print(f"   PIL/Pillow: {pil_version}")
        except:
            print("   PIL/Pillow: Não instalado")
        
        try:
            import cv2
            print(f"   OpenCV: {cv2.__version__}")
        except:
            print("   OpenCV: Não instalado")

def main():
    """Função principal"""
    criar_pastas()
    
    # Verificar dependências
    try:
        from PIL import Image
        import cv2
    except ImportError:
        print("❌ Dependências não instaladas!")
        print("📦 Instale: pip install Pillow opencv-python")
        return
    
    # Boas-vindas
    print("\n" + "=" * 60)
    print("BEM-VINDO AO INSTAGRAM AUTOMATOR COMPLETO!")
    print("=" * 60)
    print("\n✨ FORMATOS DISPONÍVEIS PARA IMAGENS:")
    print("• 📐 Feed Quadrado (1080x1080)")
    print("• 📱 Feed Retrato (1080x1350)")
    print("• 🏞️  Feed Paisagem (1080x566)")
    print("• 📖 Stories (1080x1920)")
    print("• 🎬 Reels (1080x1920)")
    print()
    
    while True:
        mostrar_menu_principal()
        
        try:
            opcao = input("👉 Escolha (1-6): ").strip()
            
            if opcao == '1':
                processar_imagens()
            elif opcao == '2':
                processar_videos()
            elif opcao == '3':
                processar_tudo()
            elif opcao == '4':
                mostrar_arquivos()
            elif opcao == '5':
                menu_configuracoes()
            elif opcao == '6':
                print("\n" + "=" * 60)
                print("👋 Instagram Automator - Versão Completa")
                print("✅ IMAGENS: Feed, Stories, Reels")
                print("✅ VÍDEOS: Feed, Stories, Reels")
                print("✅ SEM distorção de imagens")
                print("=" * 60)
                break
            else:
                print("❌ Opção inválida")
            
            if opcao != '6':
                input("\n↵ Pressione Enter para continuar...")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Programa interrompido")
            break
        except Exception as e:
            print(f"\n❌ Erro: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()