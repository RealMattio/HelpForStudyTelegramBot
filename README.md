# Help For Study Telegram Bot 📚🤖
![Build](https://img.shields.io/badge/build-passing-brightgreen?logo=githubactions)
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
[![Licenza: AGPL v3.0](https://img.shields.io/badge/⚖️%20License-AGPL_v3.0-yellow.svg)](./LICENSE)

![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=googlegemini&logoColor=white)

Un **Telegram Bot** (Python) pensato per facilitare il ripasso di esami universitari:  
ti fa domande pescate randomicamente da dataset testuali e – prossimamente – mostrerà flash-cards riassuntive delle materie. Il codice è volutamente semplice: basta un file di **token**, qualche file `.txt` di domande e sei subito operativo!

---

## ✨ Caratteristiche principali
| Funzione | Dettagli |
|----------|----------|
| **Quiz random** | Estrae domande da file testo (uno per materia) e le invia con pulsante “Nuova domanda” |
| **Scelta guidata materia** | UI inline con tre materie pre-caricate (Cybersecurity, Innovazione e Trasformazione Digitale, Fondamenti di Inteligenza Artificiale)|
| **Persistenza utenti** | Salva `chat_id` e nickname in JSON (`users.json`, `nicknames.json`) per statistiche future |
| **Supporto emoji** | Risposte più “amichevoli” grazie al pacchetto `emoji` |
| **Flash-cards** | Sezione già presente nei menu, pronta per l’integrazione di file `json` |

---

## 📂 Struttura progetto
```
.
├── data/                               # Cartella per contenere le domande
│   ├── domande_cybersecurity_it.txt  
│   ├── domande_itd_it.txt
│   └── domande_fia_it.txt
├── HelpForStudyTelegramBot.py          # Entry-point
├── LICENSE                             # Licensa
├── requirements.txt
└── token_file.txt                      # Non versionato: inserisci qui il token del tuo bot
````

---

## 🚀 Quick start

> Requisiti: **Python 3.10+** e un bot creato via [@BotFather](https://t.me/botfather).

```bash
# 1) Clona il repo
git clone https://github.com/RealMattio/HelpForStudyTelegramBot.git
cd HelpForStudyTelegramBot
```
```bash
# 2) Crea e attiva l'ambiente
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt           # python-telegram-bot, emoji, …
```
```bash
# 3) Inietta il token
echo "123456:ABC-DEF..." > token_file.txt
```
```bash
# 4) Avvia il bot
python HelpForStudyTelegramBot.py
```

Il bot partirà in modalità polling. Scrivigli `/start` su Telegram,
poi `/iniziaStudio` per scegliere la materia e cominciare il quiz.

---

## 🛠️ Aggiungere nuove materie

1. Metti le domande (una per riga) in `data/domande_<materia>_it.txt`.
2. Nel file `HelpForStudyTelegramBot.py`, aggiungi un nuovo `InlineKeyboardButton` dentro `choose_subject()` e un `elif` corrispondente in `set_subject()` che punti al tuo file.
3. Riavvia il bot: la materia comparirà nel menu.

Le flash-cards funzioneranno in modo simile ma con file `json`
strutturati (chiave → lista di keyword).

---

## 🤖 Comandi disponibili

| Comando         | Descrizione                          |
| --------------- | ------------------------------------ |
| `/start`        | Messaggio di benvenuto e linea guida |
| `/iniziaStudio` | Selezione materia e modalità         |
| `/cosapuoifare` | Riepilogo funzionalità bot           |
| `/info`         | Crediti e contatti autore            |

*(messaggi di testo non riconosciuti vengono gestiti da un eco di fallback)*

---

## ▶️ Esempio di sessione

```
/start
🤖 Ciao alice! ... Usa /iniziaStudio per iniziare a studiare.

/iniziaStudio
➡️  Scegli una materia da studiare
[Cybersecurity] [Innovazione ...] [Fondamenti IA]

# dopo la scelta
➡️  Scegli una modalità di studio
[Domande] [Flashcards] [Cambia materia]

# modalità Domande
Che cos'è una SQL Injection?
[Nuova domanda] [Indietro]
```

---

## 📈 Roadmap

* [ ] Rendere il codice modulare all'aggiunta di file con domande
* [ ] Implementare gestione flash-cards da JSON
* [ ] Supporto multilingua (IT / EN)
* [ ] Deploy su Heroku / Railway con webhook HTTPS
* [ ] Report statistico (domande viste, percentuale ripasso) per ogni utente

---

## 💡 Contribuire

Contributi, segnalazioni di bug e nuove liste di domande sono benvenuti!

1. Fai un **fork**, crea una branch feature, apri la PR.
2. Segui **`black`** e **`ruff`** per lo stile del codice.
3. Aggiorna `README` e aggiungi eventuali tuoi dataset nella cartella `data/`.

---

## 📄 Licenza


Questo progetto è rilasciato sotto i termini della licenza **GNU Affero General Public License v3.0**.

L'uso di questo software implica l'accettazione di tutti i termini e le condizioni di questa licenza. Una copia completa della licenza è disponibile nel file [LICENSE](LICENSE) di questo repository.

---

> *“Studiare senza desiderio rovina la memoria e non conserva nulla di ciò che si prende.”* — **Leonardo da Vinci**

