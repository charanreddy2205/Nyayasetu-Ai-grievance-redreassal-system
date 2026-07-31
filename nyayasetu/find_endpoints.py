
import os
import re

print('--- FRONTEND API CALLS ---')
for root, _, files in os.walk('frontend/src'):
    for file in files:
        if file.endswith(('.js', '.jsx')):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                for line_idx, line in enumerate(f):
                    if 'apiFetch' in line or 'fetch(' in line:
                        print(f'{path}:{line_idx+1}: {line.strip()}')

print('\n--- BACKEND ENDPOINTS ---')
for root, _, files in os.walk('api'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                for line_idx, line in enumerate(f):
                    if 'url_path' in line or 'path(' in line or 'router.register' in line:
                        print(f'{path}:{line_idx+1}: {line.strip()}')

