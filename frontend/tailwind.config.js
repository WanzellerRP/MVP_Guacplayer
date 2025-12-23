/**
 * Configuração do Tailwind CSS para GuacPlayer
 * Autor: GuacPlayer Team
 * Data: 2025
 * Descrição: Tema customizado com cores CAIXA
 */

export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        'caixa-primary': '#0643AA',    // Azul CAIXA
        'caixa-accent': '#E4781A',     // Laranja CAIXA
        'caixa-light': '#F5F5F5',      // Cinza claro
        'caixa-dark': '#1A1A1A'        // Cinza escuro
      },
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif']
      },
      spacing: {
        'safe-top': 'env(safe-area-inset-top)',
        'safe-bottom': 'env(safe-area-inset-bottom)'
      }
    }
  },
  plugins: []
}
