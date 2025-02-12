# serpent
Компилятор подмножества языка программирования Eiffel

## Сборка из исходников
Для создания билда (требуется gcc, flex, bison):
```bash
make
```
Запуск последующих тестов требует наличия python:
```bash
python -m venv venv
./venv/Scripts/activate
python -m pip install -r requirements_dev.txt
make test
```
