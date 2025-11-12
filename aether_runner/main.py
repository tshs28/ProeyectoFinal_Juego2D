# main.py - ARCHIVO PRINCIPAL
# Aether Runner - Juego de Plataforma 2D
# Día 4: Sistema de Niveles y Enemigos Funcionales

from game import Game

if __name__ == "__main__":
    print("=" * 50)
    print("AETHER RUNNER - INICIANDO")
    print("=" * 50)
    print("CONTROLES:")
    print("   ← → / A D: Moverse")
    print("   ESPACIO: Saltar (Doble salto disponible)")
    print("   S / ↓: Deslizarse")
    print("   R: Reiniciar nivel actual")
    print("   N: Siguiente nivel (modo debug)")
    print("")
    print("OBJETIVO:")
    print("   • Recolecta todos los FRAGMENTOS AZULES")
    print("   • Evita enemigos MORADOS y ROJOS")
    print("   • Usa power-ups para ayudarte")
    print("   • Completa los 3 niveles")
    print("")
    print("POWER-UPS:")
    print("   🟡 Dorado: Invencibilidad temporal")
    print("   🟢 Verde: Salto mejorado")
    print("   🔴 Rosa: Imán (atrae fragmentos)")
    print("")
    print("ENEMIGOS:")
    print("Morados: Flotantes (se mueven en ondas)")
    print("Rojos: Tiradores (disparan proyectiles)")
    print("=" * 50)
    
    # Iniciar el juego
    game = Game()

    game.run()
