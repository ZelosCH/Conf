# Практическое задание №4. Системы автоматизации сборки

Работа с утилитой Make.

## Задача 1

Написать программу на Питоне, которая транслирует граф зависимостей civgraph в makefile в духе примера выше.

```
import re

with open("cpg.txt", "r") as file:
    content = file.read()

dependency_pattern = re.compile(r"(\w+)\s*->\s*(\w+)")

dependencies = {}
all_targets = set()

for source, target in dependency_pattern.findall(content):
    source = source.lower()
    target = target.lower()
    all_targets.add(source)
    all_targets.add(target)
    
    if target in dependencies:
        dependencies[target].append(source)
    else:
        dependencies[target] = [source]

with open("Makefile", "w") as makefile:
    for target in all_targets:
        sources = dependencies.get(target, [])
        makefile.write(f"{target}: {' '.join(sources)}\n")
        makefile.write(f"\t@echo \"{target}\"\n")
    
    makefile.write("\nall: " + " ".join(all_targets) + "\n")

print("Makefile успешно создан.")
```
![image](https://github.com/user-attachments/assets/93b0bb04-3248-498d-bc63-71c5e91e001b)


## Задача 2

Реализовать вариант трансляции, при котором повторный запуск make не выводит для civgraph на экран уже выполненные "задачи".

> Добавляется строка makefile.write(f"\t@touch {target}\n") для создания или обновления целевого файла с временной меткой

```
import re

with open("cpg.txt", "r") as file:
    content = file.read()

dependency_pattern = re.compile(r"(\w+)\s*->\s*(\w+)")

dependencies = {}
all_targets = set()

for source, target in dependency_pattern.findall(content):
    source = source.lower()
    target = target.lower()
    all_targets.add(source)
    all_targets.add(target)

    if target in dependencies:
        dependencies[target].append(source)
    else:
        dependencies[target] = [source]

with open("Makefile", "w") as makefile:
    for target in all_targets:
        sources = dependencies.get(target, [])
        makefile.write(f"{target}: {' '.join(sources)}\n")
        makefile.write(f"\t@echo \"{target}\"\n")
        makefile.write(f"\t@touch {target}\n")

    makefile.write("\nall: " + " ".join(all_targets) + "\n")

print("Makefile успешно создан.")
```

![image](https://github.com/user-attachments/assets/b389bf36-413f-427a-b57a-0780a8e0faaf)

