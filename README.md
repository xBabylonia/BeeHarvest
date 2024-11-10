Channel: [Yog's Channel](https://t.me/yogschannel)

Bot: [BeeHarvest](https://t.me/beeharvestbot?start=6635604468_V8Xmx96E)

# BeeHarvestBot

An automated bot for the **BeeHarvest** application, performing various tasks like spinning, staking, and mining upgrades autonomously, with structured logging.

## Features

- **Daily Login**
- **Random Combo**
- **Auto Spin**
- **Auto Task**: Not all
- **Auto Join Squad**
- **Auto Stake**
- **Mining Upgrade**
- **Multi Accounts**

## Configuration

The bot’s settings can be customized through configuration options: [line 12 to 16]
- **enable_spin**: Enables or disables the auto-spin feature.
- **enable_stake**: Enables or disables the staking feature.
- **enable_mining_upgrade**: Enables or disables automatic mining upgrades.

## Note

This script is intended for educational and research purposes only. Use at your own risk.

--------------

# Cara Menjalankan Script

Script ini dapat dijalankan di berbagai platform, termasuk Windows, Linux/VPS, dan Termux. Berikut adalah langkah-langkah untuk menjalankan script ini.

## Persyaratan

Pastikan Anda memiliki Python versi 3.7 atau lebih baru. Anda juga perlu menginstal `pip`, yang biasanya sudah termasuk dalam instalasi Python.

## Langkah Instalasi

### 1. Clone Repository
Clone repository ini terlebih dahulu:

```bash
git clone https://github.com/xBabylonia/BeeHarvest.git
cd BeeHarvest
```

### 2. Install Dependensi
Jalankan perintah berikut untuk menginstal semua dependensi yang dibutuhkan.

```bash
pip install aiohttp colorama loguru
```

## Cara Menjalankan di Windows

1. Buka Command Prompt atau Terminal di folder project.
2. Jalankan script dengan perintah berikut:

   ```bash
   python main.py
   ```

## Cara Menjalankan di Linux atau VPS

1. Buka terminal.
2. Arahkan ke folder tempat Anda meng-clone repository.
3. Jalankan perintah berikut:

   ```bash
   python3 main.py
   ```

## Cara Menjalankan di Termux

1. Pastikan Termux Anda sudah diperbarui:

   ```bash
   pkg update && pkg upgrade
   ```

2. Install Python di Termux jika belum terpasang:

   ```bash
   pkg install python
   ```

3. Clone repository dan masuk ke folder project:

   ```bash
   git clone https://github.com/xBabylonia/BeeHarvest.git
   cd BeeHarvest
   ```

4. Install dependensi:

   ```bash
   pip install aiohttp colorama loguru
   ```

5. Jalankan script:

   ```bash
   python main.py
   ```
   
--------------
## Note

This script is intended for educational and research purposes only. Use at your own risk.
