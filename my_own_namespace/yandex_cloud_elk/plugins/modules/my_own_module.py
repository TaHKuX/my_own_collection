#!/usr/bin/python

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: my_own_module

version_added: "1.0.0"

description: my_own_module

options:
    path:
        description: Путь к файлу
        required: true
        type: str
    content:
        description: Содержимое
        required: true
        type: str
'''

EXAMPLES = r'''
# Создать файл с содержимым
- name: Записать в файл
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/example.txt
    content: "Hello, world!"

# Перезаписать файл
- name: Обновить конфигурацию
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /etc/myapp/config.cfg
    content: "setting=true"
'''

RETURN = r'''
path:
    description: Путь к файлу
    type: str
    returned: always
    sample: "/tmp/example.txt"
content:
    description: Содержимое
    type: str
    returned: always
    sample: "Hello, world!"
'''

import os
from ansible.module_utils.basic import AnsibleModule

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True)
    )

    result = dict(
        changed=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']

    # Проверяем существование файла
    if os.path.exists(path):
        try:
            with open(path, 'r') as f:
                existing = f.read()
            if existing != content:
                result['changed'] = True
        except Exception as e:
            module.fail_json(msg=f"Cannot read file {path}: {str(e)}")
    else:
        result['changed'] = True
        # Создаём родительскую директорию при необходимости
        dirname = os.path.dirname(path)
        if dirname and not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except Exception as e:
                module.fail_json(msg=f"Cannot create directory {dirname}: {str(e)}")

    # В check_mode только возвращаем результат
    if module.check_mode:
        result['path'] = path
        result['content'] = content
        module.exit_json(**result)

    # Если нужно изменить - пишем файл
    if result['changed']:
        try:
            with open(path, 'w') as f:
                f.write(content)
        except Exception as e:
            module.fail_json(msg=f"Cannot write file {path}: {str(e)}")

    result['path'] = path
    result['content'] = content
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()