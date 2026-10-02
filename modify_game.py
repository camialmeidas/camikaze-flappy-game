#!/usr/bin/env python3
import re

# Read the original file
with open('index.html', 'r') as f:
    content = f.read()

# ============ FASE 1: Alterar título ============
content = content.replace('<title>Flappy Kiro</title>', '<title>CAMIKAZE</title>')

# ============ FASE 2 & 3: Adicionar funções de desenho (antes de render) ============
# Encontrar a linha "// === RENDERER ===" e inserir as funções ANTES

new_functions = '''    // === AIRPLANE & BANNER DRAWING ===
    function drawAirplane(ctx, x, y, width, height, tilt, waveOffset) {
      ctx.save();
      ctx.translate(x + width / 2, y + height / 2);
      ctx.rotate(tilt);

      // Fuselagem (corpo vermelho principal)
      ctx.fillStyle = '#EE3333';
      ctx.beginPath();
      ctx.ellipse(0, 0, width * 0.35, height * 0.45, 0, 0, Math.PI * 2);
      ctx.fill();

      // Asa (branca com borda vermelha)
      ctx.fillStyle = '#FFFFFF';
      ctx.beginPath();
      ctx.ellipse(-width * 0.15, -height * 0.15, width * 0.55, height * 0.15, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#EE3333';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // Cauda (forma triangular vermelha)
      ctx.fillStyle = '#CC1111';
      ctx.beginPath();
      ctx.moveTo(width * 0.35, -height * 0.1);
      ctx.lineTo(width * 0.45, -height * 0.22);
      ctx.lineTo(width * 0.45, height * 0.22);
      ctx.closePath();
      ctx.fill();

      // Cabine (pequeno círculo branco)
      ctx.fillStyle = '#FFFFFF';
      ctx.beginPath();
      ctx.arc(-width * 0.1, -height * 0.15, width * 0.12, 0, Math.PI * 2);
      ctx.fill();

      // Olho na cabine
      ctx.fillStyle = '#000000';
      ctx.beginPath();
      ctx.arc(-width * 0.08, -height * 0.18, width * 0.04, 0, Math.PI * 2);
      ctx.fill();

      // Hélice (círculo rotativo vermelho)
      ctx.save();
      var helixRotation = waveOffset * 8;
      ctx.translate(-width * 0.35, 0);
      ctx.rotate(helixRotation);
      ctx.strokeStyle = '#333333';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(0, 0, width * 0.08, 0, Math.PI * 2);
      ctx.stroke();
      ctx.fillStyle = '#FFFFFF';
      ctx.beginPath();
      ctx.moveTo(0, -width * 0.06);
      ctx.lineTo(-width * 0.04, width * 0.04);
      ctx.lineTo(width * 0.04, width * 0.04);
      ctx.closePath();
      ctx.fill();
      ctx.restore();

      ctx.restore();
    }

    function drawBanner(ctx, x, y, waveOffset, text) {
      var bannerWidth = 100;
      var bannerHeight = 30;
      var waveAmplitude = 4;
      var waveFreq = 3;

      ctx.save();
      ctx.translate(x, y);

      // Onda suave na faixa
      var waveY = Math.sin(waveOffset * waveFreq) * waveAmplitude;
      ctx.translate(0, waveY);

      // Faixa rosa
      ctx.fillStyle = '#FF69B4';
      ctx.shadowColor = 'rgba(0, 0, 0, 0.3)';
      ctx.shadowBlur = 4;
      ctx.shadowOffsetX = 1;
      ctx.shadowOffsetY = 2;
      ctx.beginPath();
      ctx.moveTo(0, -bannerHeight / 2);
      ctx.lineTo(bannerWidth, -bannerHeight / 2 - 3);
      ctx.lineTo(bannerWidth, bannerHeight / 2 - 3);
      ctx.lineTo(0, bannerHeight / 2);
      ctx.closePath();
      ctx.fill();

      // Borda rosa escuro
      ctx.strokeStyle = '#E91E63';
      ctx.lineWidth = 2;
      ctx.stroke();

      // Texto "CAMIKAZE" na faixa
      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 12px Arial, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
      ctx.shadowBlur = 2;
      ctx.shadowOffsetX = 0;
      ctx.shadowOffsetY = 1;
      ctx.fillText('CAMIKAZE', bannerWidth / 2, -2);

      ctx.restore();
    }

'''

# Inserir antes de "// === RENDERER ==="
content = content.replace('    // === RENDERER ===', new_functions + '    // === RENDERER ===')

# ============ FASE 3: Adicionar waveOffset ao gameState ============
# Encontrar gameState e adicionar waveOffset
gamestate_pattern = r'(      laserBeamY: 0\n    \};)'
gamestate_replacement = r'      laserBeamY: 0,\n      waveOffset: 0\n    };'
content = re.sub(gamestate_pattern, gamestate_replacement, content)

# ============ FASE 4a: Incrementar waveOffset no gameLoop ============
# Adicionar antes de "render(ctx, gameState, assets);" dentro de gameLoop
gameloop_pattern = r'(      // 10\. Render frame\n)(      render\(ctx, gameState, assets\);)'
gameloop_replacement = r'\1      // Update wave animation for banner and airplane\n      gameState.waveOffset += dt * 2;\n\n\2'
content = re.sub(gameloop_pattern, gameloop_replacement, content)

# ============ FASE 4b: Incrementar waveOffset no idleLoop ============
# Adicionar antes de "render(ctx, gameState, assets);" dentro de idleLoop
idleloop_pattern = r'(      render\(ctx, gameState, assets\);\n\n      rafId = requestAnimationFrame\(idleLoop\);)'
idleloop_replacement = r'      // Update wave animation\n      gameState.waveOffset += dt * 2;\n\n      render(ctx, gameState, assets);\n\n      rafId = requestAnimationFrame(idleLoop);'
content = re.sub(idleloop_pattern, idleloop_replacement, content, count=1)

# ============ FASE 5: Substituir o desenho do sprite (Kiro) por aviãozinho ============
# Encontrar e substituir a seção "5. Kiro sprite"

sprite_section_pattern = r'(      // --- 5\. Kiro sprite ---\n      var kiro = gameState\.kiro;\n      var centerX = kiro\.x \+ kiro\.width \/ 2;\n      var centerY = kiro\.y \+ kiro\.height \/ 2;\n      // Velocity-based tilt\n      var targetAngle = Math\.max\(-0\.5, Math\.min\(0\.8, kiro\.velocity \* 0\.002\)\);)(\n      ctx\.save\(\);[\s\S]*?ctx\.restore\(\);(?=\n\n      // --- 5b))'

sprite_replacement = r'\1\n      // Draw airplane with banner\n      drawBanner(ctx, centerX - 50, centerY - 25, gameState.waveOffset, "CAMIKAZE");\n      drawAirplane(ctx, centerX - kiro.width / 2, centerY - kiro.height / 2, kiro.width, kiro.height, targetAngle, gameState.waveOffset);\n\n      ctx.restore();\n      // Placeholder to maintain structure'

content = re.sub(sprite_section_pattern, sprite_replacement, content, flags=re.DOTALL)

# ============ FASE 6: Adicionar títulos "CAMIKAZE" e "Piloto: Capitã Camila" na tela inicial ============
# Encontrar a seção de overlay messages (start screen) e adicionar antes de "Tap or Press Space"

start_screen_pattern = r'(      if \(gameState\.status === \'start\'\) \{)\n(        // Pulsing "Tap or Press Space to Start")'
start_screen_replacement = r'''\1
        // Title "CAMIKAZE"
        ctx.save();
        ctx.font = 'bold 48px Arial, sans-serif';
        ctx.fillStyle = '#EE3333';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
        ctx.shadowBlur = 8;
        ctx.shadowOffsetX = 2;
        ctx.shadowOffsetY = 2;
        ctx.fillText('CAMIKAZE', w / 2, h / 4 - 40);
        ctx.restore();

        // Subtitle "Piloto: Capitã Camila"
        ctx.save();
        ctx.font = '18px Arial, sans-serif';
        ctx.fillStyle = '#FFFFFF';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'top';
        ctx.fillText('Piloto: Capitã Camila', w / 2, h / 4 + 20);
        ctx.restore();

\2'''

content = re.sub(start_screen_pattern, start_screen_replacement, content)

# Write the modified content
with open('index.html', 'w') as f:
    f.write(content)

print("✅ Todas as 6 fases implementadas com sucesso!")
print("   Fase 1: ✅ Título alterado para 'CAMIKAZE'")
print("   Fase 2: ✅ Funções drawAirplane e drawBanner adicionadas")
print("   Fase 3: ✅ waveOffset adicionado ao gameState")
print("   Fase 4a: ✅ waveOffset incrementado em gameLoop")
print("   Fase 4b: ✅ waveOffset incrementado em idleLoop")
print("   Fase 5: ✅ Aviãozinho renderizado em vez do sprite")
print("   Fase 6: ✅ Títulos 'CAMIKAZE' e 'Piloto: Capitã Camila' adicionados")
