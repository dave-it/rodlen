import requests

vmix_api_url = "http://192.168.1.111:8088/api"

def trigger_overlay(overlay_name):
    # Ersetzen Sie "Your-Overlay-Trigger-Endpoint" durch den tatsächlichen Endpunkt zum Auslösen des Overlays
    trigger_url = f"{vmix_api_url}?Function=OverlayInput1In&Input=3"
    
    # Fügen Sie ggf. erforderliche Parameter oder Authentifizierungsinformationen hinzu
    payload = {
        'overlay_name': overlay_name
    }

    try:
        response = requests.post(trigger_url, json=payload)
        if response.status_code == 200:
            print(f"Overlay '{overlay_name}' erfolgreich ausgelöst.")
        else:
            print(f"Fehler beim Auslösen des Overlays. Statuscode: {response.status_code}")
    except requests.RequestException as e:
        print(f"Fehler bei der Anfrage: {e}")

# Beispielaufruf
trigger_overlay("YourOverlayName")