import sys
with open('templates/resume/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded colors with theme variables
content = content.replace('[#0F172A]', 'themeBg')
content = content.replace('[#111827]', 'themeSurface')

# Update tailwind config script
new_tailwind = """<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          themeBg: 'var(--color-bg, #0F172A)',
          themeSurface: 'var(--color-surface, #111827)',
          primary: { DEFAULT: 'var(--color-accent, #6C5CE7)', light: 'var(--color-accent-2, #A29BFE)', dark: 'var(--color-accent, #5546d6)' },
          secondary: { DEFAULT: 'var(--color-accent-2, #00CEC9)', dark: 'var(--color-accent, #00b8b3)' },
        },
        fontFamily: { sans: ['Inter', 'system-ui', 'sans-serif'] },
        boxShadow: {
          soft: '0 18px 45px -15px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.06)',
          glow: '0 0 80px -20px var(--color-accent, rgba(108, 92, 231, 0.45))',
        },
        borderRadius: { xl: '12px', '2xl': '16px', '3xl': '24px' },
      },
    },
  };
</script>"""

import re
content = re.sub(r'<script>\s*tailwind\.config = \{.*?\};\s*</script>', new_tailwind, content, flags=re.DOTALL)

with open('templates/resume/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
