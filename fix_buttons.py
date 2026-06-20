import os, re

for root, dirs, files in os.walk('templates/dashboard'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            def replacer(match):
                class_content = match.group(0)
                if 'bg-primary' in class_content:
                    return class_content.replace('text-white', 'text-onAccent')
                return class_content

            new_content = re.sub(r'class="[^"]+"', replacer, content)
            new_content = re.sub(r"class='[^']+'", replacer, new_content)

            if content != new_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
