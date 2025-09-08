# Procedura Acquisizione Forense iOS con Checkm8 - Strumenti Open Source

## Panoramica
L'exploit **checkm8** è una vulnerabilità del bootrom permanente e non patchabile che colpisce centinaia di milioni di dispositivi iOS. Questa guida presenta gli strumenti open source disponibili su GitHub per l'acquisizione forense di dispositivi iOS.

## Dispositivi Supportati
- **iPhone**: 4s, 5, 5c, 5s, 6, 6 Plus, 6s, 6s Plus, 7, 7 Plus, 8, 8 Plus, X
- **iPad**: 2, 3, 4, 5a gen, 6a gen, 7a gen, Air, Air 2, mini 2, mini 3, mini 4, Pro 9.7", Pro 10.5", Pro 12.9" 1a e 2a gen
- **iPod Touch**: 5a, 6a, 7a generazione
- **Apple TV**: 4a generazione e precedenti

## Principali Strumenti Open Source

### 1. **ipwndfu** - Tool Principale per checkm8
**Repository**: https://github.com/axi0mX/ipwndfu

Strumento principale che implementa l'exploit checkm8 e altri exploits per dispositivi iOS.

#### Funzionalità:
- Exploit checkm8 per dispositivi A5-A11
- Dump del SecureROM
- Decriptazione delle keybag
- Demoting del dispositivo per JTAG
- Supporto per DFU Mode pwned

#### Installazione:
```bash
git clone https://github.com/axi0mX/ipwndfu.git
cd ipwndfu
# Su macOS: installare libusb con Homebrew
brew install libusb
# Su Linux: installare libusb tramite package manager
sudo apt-get install libusb-1.0-0-dev  # Ubuntu/Debian
```

#### Utilizzo Base:
```bash
# Mettere il dispositivo in DFU mode e connettere via USB
./ipwndfu -p  # Eseguire l'exploit checkm8
./ipwndfu --dump-rom  # Dump del SecureROM
./ipwndfu --decrypt-gid KEYBAG  # Decriptare keybag
```

### 2. **pymobiledevice3** - Libreria Python Completa
**Repository**: https://github.com/doronz88/pymobiledevice3

Implementazione Python completa per lavorare con dispositivi iOS.

#### Installazione:
```bash
pip install pymobiledevice3
```

#### Funzionalità Principali:
- Backup e restore
- Gestione applicazioni
- Accesso al filesystem
- Diagnostica e debugging
- Sniffing del traffico di rete
- Screenshot e controllo UI

#### Comandi Essenziali:
```python
# Backup del dispositivo
pymobiledevice3 backup2 backup /percorso/backup

# Lista applicazioni installate
pymobiledevice3 apps list

# Accesso file system (richiede jailbreak)
pymobiledevice3 afc ls /

# Screenshot
pymobiledevice3 developer dvt screenshot /path/screenshot.png
```

### 3. **UFADE** - Wrapper Python per Acquisizioni
**Repository**: https://github.com/prosch88/UFADE

Tool Python con interfaccia grafica che automatizza l'acquisizione di dispositivi Apple.

#### Installazione:
```bash
git clone https://github.com/prosch88/UFADE --recurse-submodules
cd UFADE
pip install -r requirements.txt
```

#### Funzionalità:
- Backup stile iTunes
- Advanced Logical Backup
- Interfaccia grafica CustomTkinter
- Supporto multipiattaforma (Windows, Linux, macOS)

### 4. **MEAT** - Mobile Evidence Acquisition Toolkit
**Repository**: https://github.com/jfarley248/MEAT

Tool Python specializzato per acquisizioni forensi iOS.

#### Installazione:
```bash
git clone https://github.com/jfarley248/MEAT.git
cd MEAT
pip3 install -r requirements.txt
```

#### Utilizzo:
```bash
# Acquisizione logica (dispositivi jailed)
python3 MEAT.py -iOS -logical -o /path/output

# Acquisizione filesystem completa (richiede jailbreak)
python3 MEAT.py -iOS -filesystem -o /path/output

# Con hash MD5
python3 MEAT.py -iOS -filesystem -md5 -o /path/output
```

### 5. **MVT** - Mobile Verification Toolkit
**Repository**: https://github.com/mvt-project/mvt

Toolkit di verifica mobile sviluppato da Amnesty International per rilevare compromissioni.

#### Installazione:
```bash
pip install mvt
```

#### Utilizzo:
```bash
# Analisi backup iOS
mvt-ios check-backup --output /path/results /path/backup

# Con IOC specifici
mvt-ios check-backup --iocs /path/indicators.stix2 /path/backup
```

## Procedura Completa di Acquisizione

### Fase 1: Preparazione
1. **Preparare l'ambiente**:
   ```bash
   # Installare dipendenze principali
   sudo apt-get install libusb-1.0-0-dev python3 python3-pip git
   
   # Clonare repository principali
   git clone https://github.com/axi0mX/ipwndfu.git
   git clone https://github.com/doronz88/pymobiledevice3.git
   pip install pymobiledevice3
   ```

2. **Verificare compatibilità dispositivo**: Controllare che il dispositivo sia supportato da checkm8

### Fase 2: Exploit e Accesso
1. **Attivare DFU Mode**:
   - iPhone 8 e successivi: Volume Su + Volume Giù + Power
   - iPhone 7/7 Plus: Volume Giù + Power  
   - iPhone 6s e precedenti: Home + Power

2. **Eseguire exploit checkm8**:
   ```bash
   cd ipwndfu
   ./ipwndfu -p
   ```

3. **Verificare successo exploit**: Il dispositivo dovrebbe essere in "pwned DFU mode"

### Fase 3: Acquisizione Dati
1. **Acquisizione completa con UFADE**:
   ```bash
   cd UFADE
   python ufade.py
   # Seguire GUI per selezionare tipo di acquisizione
   ```

2. **Acquisizione mirata con MEAT**:
   ```bash
   # Per dispositivi jailbroken
   python3 MEAT.py -iOS -filesystem -md5 -sha1 -o /path/evidence/
   
   # Per dispositivi standard
   python3 MEAT.py -iOS -logical -md5 -sha1 -o /path/evidence/
   ```

3. **Backup forense con pymobiledevice3**:
   ```bash
   pymobiledevice3 backup2 backup /path/forensic_backup/
   ```

### Fase 4: Verifica e Analisi
1. **Verifica integrità**:
   ```bash
   # Calcolare hash dell'acquisizione
   sha256sum /path/evidence/* > evidence_hashes.txt
   ```

2. **Analisi con MVT**:
   ```bash
   mvt-ios check-backup --output /path/analysis/ /path/forensic_backup/
   ```

## Considerazioni Legali e Etiche
- ⚠️ **Utilizzare solo su dispositivi di cui si ha legale proprietà o autorizzazione**
- ⚠️ **Documentare accuratamente la chain of custody**
- ⚠️ **Mantenere l'integrità delle prove digitali**
- ⚠️ **Rispettare le normative locali sulla privacy e sicurezza**

## Note Tecniche Importanti
- checkm8 richiede accesso fisico al dispositivo
- L'exploit non è persistente (scompare al riavvio)
- Alcuni metodi richiedono il jailbreak del dispositivo
- Non funziona in macchine virtuali
- Richiede cavi USB di qualità per stabilità

## Strumenti Aggiuntivi Utili
- **iOSbackup**: Analisi backup iTunes criptati
- **OpenBackupExtractor**: Estrazione dati da backup iPhone/iPad
- **iOS Frequent Locations Dumper**: Estrazione dati posizione
- **libimobiledevice**: Libreria cross-platform per comunicazione con dispositivi iOS

## Documentazione e Risorse
- [Awesome Forensics](https://github.com/cugu/awesome-forensics): Lista curata di tool forensi
- [ForensicsTools](https://github.com/mesquidar/ForensicsTools): Risorse e tool per analisi forense
- [Mobile Incident Response](https://github.com/nowsecure/mobile-incident-response): Guida risposta agli incidenti mobile

---
**Disclaimer**: Questo documento è destinato esclusivamente a ricercatori, investigatori forensi e professionisti della sicurezza per scopi educativi e legali. L'uso improprio di questi strumenti può violare le leggi sulla privacy e sicurezza.
