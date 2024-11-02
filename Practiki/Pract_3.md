
## Задача 1

Реализовать на Jsonnet приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.
```
local groupPrefix = "ИКБО-";
local groupSuffix = "-20";

local generateGroups(start, end) = [
  groupPrefix + std.toString(i) + groupSuffix
  for i in std.range(start, end)
];

{
  groups: generateGroups(1, 24),
  students: [
    {
      age: 19,
      group: "ИКБО-4-20",
      name: "Иванов И.И."
    },
    {
      age: 18,
      group: "ИКБО-5-20",
      name: "Петров П.П."
    },
    {
      age: 18,
      group: "ИКБО-5-20",
      name: "Сидоров С.С."
    },
    {
      age: 18,
      group: "ИКБО-23-20",
      name: "Попов А.В."
    }
  ],
  subject: "Конфигурационное управление"
}
```
Что получаем на выходе:
```
{
   "groups": [
      "ИКБО-1-20",
      "ИКБО-2-20",
      "ИКБО-3-20",
      "ИКБО-4-20",
      "ИКБО-5-20",
      "ИКБО-6-20",
      "ИКБО-7-20",
      "ИКБО-8-20",
      "ИКБО-9-20",
      "ИКБО-10-20",
      "ИКБО-11-20",
      "ИКБО-12-20",
      "ИКБО-13-20",
      "ИКБО-14-20",
      "ИКБО-15-20",
      "ИКБО-16-20",
      "ИКБО-17-20",
      "ИКБО-18-20",
      "ИКБО-19-20",
      "ИКБО-20-20",
      "ИКБО-21-20",
      "ИКБО-22-20",
      "ИКБО-23-20",
      "ИКБО-24-20"
   ],
   "students": [
      {
         "age": 19,
         "group": "ИКБО-4-20",
         "name": "Иванов И.И."
      },
      {
         "age": 18,
         "group": "ИКБО-5-20",
         "name": "Петров П.П."
      },
      {
         "age": 18,
         "group": "ИКБО-5-20",
         "name": "Сидоров С.С."
      },
      {
         "age": 18,
         "group": "ИКБО-23-20",
         "name": "Попов А.В."
      }
   ],
   "subject": "Конфигурационное управление"
}
```
## Задача 2

Реализовать на Dhall приведенный ниже пример в формате JSON. Использовать в реализации свойство программируемости и принцип DRY.
```
let generateGroup : Natural → Text
= λ(i : Natural) → "ИКБО-" ++ Text/show i ++ "-20"

let groups : List Text
= List/generate 24 generateGroup

let Student
    : Type
= { age : Natural, group : Text, name : Text }

let students : List Student
= [ { age = 19, group = "ИКБО-4-20", name = "Иванов И.И." }
  , { age = 18, group = "ИКБО-5-20", name = "Петров П.П." }
  , { age = 18, group = "ИКБО-5-20", name = "Сидоров С.С." }
  , { age = 20, group = "ИКБО-6-20", name = "Новиков Н.Н." }
  ]

let config
    : { groups : List Text, students : List Student, subject : Text }
= { groups = groups
  , students = students
  , subject = "Конфигурационное управление"
  }

in  config
```
Вывод:

```
{
  "groups": [
    "ИКБО-1-20",
    "ИКБО-2-20",
    "ИКБО-3-20",
    "ИКБО-4-20",
    "ИКБО-5-20",
    "ИКБО-6-20",
    "ИКБО-7-20",
    "ИКБО-8-20",
    "ИКБО-9-20",
    "ИКБО-10-20",
    "ИКБО-11-20",
    "ИКБО-12-20",
    "ИКБО-13-20",
    "ИКБО-14-20",
    "ИКБО-15-20",
    "ИКБО-16-20",
    "ИКБО-17-20",
    "ИКБО-18-20",
    "ИКБО-19-20",
    "ИКБО-20-20",
    "ИКБО-21-20",
    "ИКБО-22-20",
    "ИКБО-23-20",
    "ИКБО-24-20"
  ],
  "students": [
    {
      "age": 19,
      "group": "ИКБО-4-20",
      "name": "Иванов И.И."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Петров П.П."
    },
    {
      "age": 18,
      "group": "ИКБО-5-20",
      "name": "Сидоров С.С."
    },
    <добавьте ваши данные в качестве четвертого студента>
  ],
  "subject": "Конфигурационное управление"
} 
```

Для решения дальнейших задач потребуется программа на Питоне, представленная ниже. Разбираться в самом языке Питон при этом необязательно.

```Python
import random


def parse_bnf(text):
    '''
    Преобразовать текстовую запись БНФ в словарь.
    '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar


def generate_phrase(grammar, start):
    '''
    Сгенерировать случайную фразу.
    '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)


BNF = '''
E = a
'''

for i in range(10):
    print(generate_phrase(parse_bnf(BNF), 'E'))

```

Реализовать грамматики, описывающие следующие языки (для каждого решения привести БНФ). Код решения должен содержаться в переменной BNF:

## Задача 3

Язык нулей и единиц.

```
10
100
11
101101
000
```
```
BNF = '''
E = 0 E | 1 E | 1 | 0
'''
```
Пример вывода:
![image](https://github.com/user-attachments/assets/c16cbc18-ad27-4720-951c-cf04cf14366d)


## Задача 4

Язык правильно расставленных скобок двух видов.

```
(({((()))}))
{}
{()}
()
{}
```
```
BNF = '''
E = ε | ( E ) | { E }
'''
```
Пример вывода:![image](https://github.com/user-attachments/assets/c887947e-4b1f-4a73-8495-16be9893a8ff)



## Задача 5

Язык выражений алгебры логики.

```
((~(y & x)) | (y) & ~x | ~x) & x
y & ~(y)
(~(y) & y & ~y)
~x
~((x) & y | (y) | (x)) & x | x | (y & ~y)
```
```
BNF = '''
E = S T S | S
S = A | ( E )
T = | / & / ε
A = x / y / ~ x / ~ y
'''

```
Пример вывода:![image](https://github.com/user-attachments/assets/77e27b79-bf35-43c2-a580-c2fe5cc99910)


