#!/usr/bin/env python3
"""Ein Scheinserver fuer onlinedeutertest: spielt die Messages-API nach.

Bindet an 127.0.0.1 auf einen freien Port, druckt die Portnummer auf
stdout (eine Zeile) und bleibt dann still.  Drei Endpunkte:

  /v1/messages  prueft Kopfzeilen und Rumpf (samt Werkzeug und
                tool_choice); stimmt alles, kommt eine Antwort mit einem
                Nachdenk-Block und dem Urteil als tool_use-Block -- so, wie
                die API es bei erzwungenem Werkzeug liefert.  Stimmt etwas
                nicht, 400 mit einer Meldung, die sagt, was fehlte.
  /text         dasselbe, aber das Urteil als JSON zwischen Prosa im
                Textblock (der alte Weg; der Leser muss ihn noch koennen).
  /prosa        nur Prosa ohne Urteil -- "Antwort nicht lesbar".
  /abgeschnitten
                stop_reason max_tokens mit halbem JSON -- "abgeschnitten".
  /fehler       401 mit dem Fehlerrumpf, den die API bei falschem
                Schluessel schickt.
  /langsam      wartet zwei Sekunden, dann dasselbe wie /v1/messages --
                fuer den Abbruchtest.
"""
import base64
import json
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ANTWORT_TEXT = (
    "Here is my assessment of the photo:\n"
    '{"klasse": "cirrus", "sicherheit": "high", '
    '"begruendung": "Feine, faserige Schleier hoch oben – '
    'der Tag bleibt thermisch brauchbar, aber die Front naht."}\n'
    "Hope that helps."
)


def pruefen(handler, rumpf):
    """Gibt None zurueck, wenn die Anfrage so aussieht, wie der Deuter sie
    schicken soll; sonst den Grund."""
    k = handler.headers
    if not k.get("x-api-key"):
        return "x-api-key fehlt"
    if k.get("anthropic-version") != "2023-06-01":
        return "anthropic-version fehlt oder falsch"
    if not (k.get("content-type") or "").startswith("application/json"):
        return "content-type ist nicht application/json"
    try:
        daten = json.loads(rumpf)
    except ValueError:
        return "Rumpf ist kein JSON"
    if not isinstance(daten.get("model"), str) or not daten["model"]:
        return "model fehlt"
    if not isinstance(daten.get("max_tokens"), int):
        return "max_tokens fehlt"
    if not isinstance(daten.get("system"), str) or "cirrus" not in daten["system"]:
        return "system fehlt oder nennt die Klassen nicht"
    nachrichten = daten.get("messages")
    if not isinstance(nachrichten, list) or len(nachrichten) != 1:
        return "messages hat nicht genau einen Eintrag"
    inhalt = nachrichten[0].get("content")
    if nachrichten[0].get("role") != "user" or not isinstance(inhalt, list):
        return "messages[0] ist keine user-Nachricht mit Bloecken"
    bilder = [b for b in inhalt if b.get("type") == "image"]
    texte = [b for b in inhalt if b.get("type") == "text"]
    if len(bilder) != 1 or len(texte) != 1:
        return "erwartet genau einen image- und einen text-Block"
    quelle = bilder[0].get("source") or {}
    if quelle.get("type") != "base64" or quelle.get("media_type") != "image/jpeg":
        return "image.source ist nicht base64/jpeg"
    try:
        roh = base64.b64decode(quelle.get("data", ""), validate=True)
    except ValueError:
        return "image.source.data ist kein base64"
    if roh[:2] != b"\xff\xd8":
        return "image.source.data ist kein JPEG"
    if not texte[0].get("text"):
        return "text-Block ist leer"
    werkzeuge = daten.get("tools")
    if not isinstance(werkzeuge, list) or len(werkzeuge) != 1:
        return "erwartet genau ein Werkzeug"
    w = werkzeuge[0]
    if w.get("name") != "urteil" or not isinstance(w.get("input_schema"), dict):
        return "Werkzeug urteil mit input_schema fehlt"
    felder = w["input_schema"].get("properties") or {}
    if set(felder) != {"klasse", "sicherheit", "begruendung"}:
        return "Schema hat nicht die drei Felder"
    if "" not in (felder["klasse"].get("enum") or []):
        return "leere Kennung fehlt in der Aufzaehlung der Klassen"
    wahl = daten.get("tool_choice") or {}
    if wahl.get("type") != "tool" or wahl.get("name") != "urteil":
        return "tool_choice erzwingt das Werkzeug nicht"
    if daten.get("max_tokens", 0) < 600:
        return "max_tokens zu knapp"
    return None


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass        # stumm; die Portzeile ist das einzige, was wir drucken

    def antworten(self, status, daten):
        rumpf = json.dumps(daten).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(rumpf)))
        self.end_headers()
        self.wfile.write(rumpf)

    def do_POST(self):
        laenge = int(self.headers.get("content-length") or 0)
        rumpf = self.rfile.read(laenge)
        if self.path == "/fehler":
            self.antworten(401, {
                "type": "error",
                "error": {"type": "authentication_error",
                          "message": "invalid x-api-key"},
            })
            return
        if self.path == "/langsam":
            time.sleep(2)
        grund = pruefen(self, rumpf)
        if grund:
            self.antworten(400, {
                "type": "error",
                "error": {"type": "invalid_request_error",
                          "message": "Pruefung: " + grund},
            })
            return
        if self.path == "/text":
            inhalt = [{"type": "thinking", "thinking": "", "signature": ""},
                      {"type": "text", "text": ANTWORT_TEXT}]
            ende = "end_turn"
        elif self.path == "/prosa":
            inhalt = [{"type": "text", "text": "Hope that helps, lovely sky today."}]
            ende = "end_turn"
        elif self.path == "/abgeschnitten":
            inhalt = [{"type": "text", "text": 'Sure: {"klasse": "cirr'}]
            ende = "max_tokens"
        else:
            inhalt = [{"type": "thinking", "thinking": "", "signature": ""},
                      {"type": "tool_use", "id": "toolu_schein", "name": "urteil",
                       "input": {"klasse": "cirrus", "sicherheit": "hoch",
                                 "begruendung": "Feine, faserige Schleier hoch oben – "
                                                "der Tag bleibt thermisch brauchbar."}}]
            ende = "tool_use"
        self.antworten(200, {
            "id": "msg_schein",
            "type": "message",
            "role": "assistant",
            "model": "claude-sonnet-5",
            "content": inhalt,
            "stop_reason": ende,
            "stop_sequence": None,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        })


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    print(server.server_address[1], flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
