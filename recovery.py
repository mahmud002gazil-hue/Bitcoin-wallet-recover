import sys
from bip_utils import Bip39MnemonicValidator, Bip39SeedGenerator, Bip39WordsNum, Bip44, Bip44Coins, Bip44Changes

# 1. BIP-39 Resmi İngilizce Kelime Listesini Yükle (2048 Kelime)
from bip_utils import Bip39WordsList
BIP39_WORDS = Bip39WordsList.GetWords()

# 2. BURAYI DÜZENLEYİN: Bildiğiniz kelimeleri yazın, eksik/unutulan kelime yerine "UNKNOWN" koyun
EKSIK_SEED = [
    "abandon", "ability", "able", "about", "UNKNOWN", "academic", 
    "accept", "accident", "account", "accuse", "achieve", "acid"
]

# 3. BURAYI DÜZENLEYİN: Bulmaya çalıştığınız cüzdan adresi (Doğrulama için)
# Not: Cüzdan türünüze göre (Legacy, SegWit, Native SegWit) türetme yolu değişebilir.
HEDEF_ADRES = "1111111111111111111114oLvT2" # Örnek adres

def cüzdan_ara():
    # "UNKNOWN" kelimesinin hangi indekste olduğunu bul
    try:
        eksik_index = EKSIK_SEED.index("UNKNOWN")
        print(f"[-] Eksik kelime {eksik_index + 1}. sırada aranıyor...")
    except ValueError:
        print("[!] Kelime listesinde 'UNKNOWN' bulunamadı. Lütfen eksik kelimeyi belirtin.")
        return

    geçiçi_seed = list(EKSIK_SEED)
    
    # 2048 kelimenin hepsini tek tek dene
    for i, kelime in enumerate(BIP39_WORDS):
        geçiçi_seed[eksik_index] = kelime
        seed_cumlesi = " ".join(geçiçi_seed)
        
        # BIP-39 Checksum (Kontrol basamağı) doğrulaması yap
        if not Bip39MnemonicValidator().IsValid(seed_cumlesi):
            continue # Checksum tutmuyorsa adresi türetmeye gerek yok, sonraki kelimeye geç
            
        try:
            # Seed'den private key ve adres türet (BIP44 standart Bitcoin yolu: m/44'/0'/0'/0/0)
            seed_bytes = Bip39SeedGenerator(seed_cumlesi).Generate()
            bip44_mst_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.BITCOIN)
            bip44_acc_ctx = bip44_mst_ctx.Purpose().Coin().Account(0)
            bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.EXTERNAL)
            bip44_addr_ctx = bip44_chg_ctx.AddressIndex(0)
            
            turetilen_adres = bip44_addr_ctx.PublicKey().ToAddress()
            
            # Adres eşleşti mi kontrol et
            if turetilen_adres == HEDEF_ADRES:
                print("\n" + "="*50)
                print("[+] BINGO! EKSİK KELİME BULUNDU!")
                print(f"[+] Bulunan Kelime: {kelime}")
                print(f"[+] Tam Seed Cümlesi: {seed_cumlesi}")
                print("="*50)
                return
                
        except Exception as e:
            continue
            
        # İlerlemeyi göster
        if i % 200 == 0:
            print(f"[*] {i}/2048 kelime denendi...")

    print("\n[!] Maalesef eşleşen bir kelime bulunamadı. Lütfen hedef adresi veya diğer kelimeleri kontrol edin.")

if __name__ == "__main__":
    cüzdan_ara()
