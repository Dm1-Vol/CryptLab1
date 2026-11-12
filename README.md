# CryptoPic

Шифрование изображений и статистическое сравнение методов.

## Реализованные алгоритмы

- Потоковый XOR (xorshift32)
- AES-ECB
- AES-CTR

## Зависимости

```bash
pip install Pillow numpy pycryptodome matplotlib
```

## Структура

```
CryptoPic/
├── src/
│   ├── stream_cipher.py
│   ├── aes_cipher.py
│   └── metrics.py
├── imgs/
│   ├── original/
│   ├── encrypted/
│   └── decrypted/
├── results/
└── report.md
```

## Пример использования

### Потоковый XOR

```python
from src.stream_cipher import process_image

process_image("imgs/original/gradient.png", "imgs/encrypted/gradient_xor.png", "my_secret_key")
process_image("imgs/encrypted/gradient_xor.png", "imgs/decrypted/gradient_xor.png", "my_secret_key")
```

### AES-ECB

```python
from src.aes_cipher import process_image_ecb

process_image_ecb("imgs/original/gradient.png", "imgs/encrypted/gradient_ecb.png", "my_secret_key", encrypt=True)
process_image_ecb("imgs/encrypted/gradient_ecb.png", "imgs/decrypted/gradient_ecb.png", "my_secret_key", encrypt=False)
```

### AES-CTR

```python
from src.aes_cipher import process_image_ctr

process_image_ctr("imgs/original/gradient.png", "imgs/encrypted/gradient_ctr.png", "my_secret_key", encrypt=True)
process_image_ctr("imgs/encrypted/gradient_ctr.png", "imgs/decrypted/gradient_ctr.png", "my_secret_key", encrypt=False)
```

### Метрики

```python
from src.metrics import entropy, correlation, npcr_uaci

print(entropy("imgs/encrypted/gradient_xor.png"))
print(correlation("imgs/encrypted/gradient_xor.png", "horizontal"))
print(correlation("imgs/encrypted/gradient_xor.png", "vertical"))
print(npcr_uaci("imgs/encrypted/gradient_xor.png", "imgs/encrypted/gradient_xor_k2.png"))
```

## Параметры

- Ключ/пароль: строка (для AES преобразуется в 16 байт через SHA-256)
- Для CTR nonce сохраняется в файл `*.nonce` рядом с изображением
- Для ECB шифротекст дополнительно пишется в `*.bin`
