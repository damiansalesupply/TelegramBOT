# Replit Dev Mode Setup (Recommended)

## Problem z Autoscale
- Cloud Run Deploy tworzy wiele instancji
- Każda instancja próbuje używać polling
- Telegram API pozwala tylko jednej instancji na polling
- Wynik: ciągłe konflikty "terminated by other getUpdates request"

## Rozwiązanie: Replit Dev Mode

### 1. Użyj Run (nie Deploy)
- Kliknij przycisk **Run** w Replit (nie Deploy)
- Jedna instancja = zero konfliktów
- Bot działa stabilnie w polling mode

### 2. Konfiguracja Workflow
```bash
# Usuń z Build command w Deploy
# Zamiast tego użyj prostego workflow:
ALLOWED_USERS=7668792787 python simple_bot.py
```

### 3. Zalety Dev Mode
- Jedna instancja - zero konfliktów polling
- Natychmiastowe uruchomienie
- Idealne dla botów z polling
- Bezpłatne w Replit

### 4. Kiedy używać Deploy Autoscale?
- Tylko dla botów z webhook mode
- Aplikacje webowe (nie boty polling)
- Serwisy API wymagające skalowania

## Instrukcje

1. **Stop current deployment** (już zrobione)
2. **Kliknij Run w Replit** zamiast Deploy
3. **Bot będzie działać stabilnie** bez konfliktów

## Alternatywa: Webhook Mode
Jeśli chcesz używać Deploy Autoscale:
- Przeróbka na webhook mode (start.py)
- Webhook URL endpoint
- Telegram wysyła messages do webhook
- Wtedy autoscale będzie działać