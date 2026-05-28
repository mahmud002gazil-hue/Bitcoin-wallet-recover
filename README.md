# Bitcoin-wallet-recover
Bitcoin wallet recover 
# BIP39 Missing Word Finder

This open-source Python tool helps you recover a lost Bitcoin/Crypto BIP39 seed phrase when you have **missing words** (1 or 2 words maximum) or if you forgot the correct word order.

## Features
- Brute-forces missing words using the official 2048 BIP39 English wordlist.
- Validates checksums before deriving addresses to ensure speed.
- Supports BIP44 standard Bitcoin address derivation.

## Installation
```bash
pip install -r requirements.txt
pip install bip-utils



Eksik olan kelime sayısı birden fazlaysa (örneğin 2 veya 3 kelime), kodun içine iç içe geçmiş `for` döngüleri eklemeniz gerekir. Ancak unutmayın, eksik kelime sayısı arttıkça denenecek kombinasyon sayısı geometrik olarak artar ($2048^2 = 4.19$ milyon, $2048^3 = 8.5$ milyar kombinasyon).
