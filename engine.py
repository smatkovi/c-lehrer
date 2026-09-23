# -*- coding: utf-8 -*-
"""Progress, repetition, and deciding what to do next.

Two ideas carry the whole thing:

* **After the placement test the course carries on where the test left
  off.** The result is a level, the chapters carry the same levels, so the
  next lesson is simply the first unfinished one at that level. Everything
  below stays reachable but is marked as already known -- nobody should have
  to click past ten chapters they proved they can do.

* **What was answered right comes back later anyway.** Every lesson names
  the concepts it teaches, and each concept is a card with a due date, in
  the usual spaced pattern: right pushes the next showing further out, wrong
  brings it back to tomorrow. Retrieval after a delay is what makes
  something stick; re-reading is not.
"""
import time

import config
import curriculum

DAY = 24 * 3600

EASE_START = 2.3
EASE_MIN = 1.3
EASE_MAX = 2.8


def now():
    return time.time()


class Engine(object):
    def __init__(self):
        self.data = config.load()

    def save(self):
        config.save(self.data)

    # -- placement ---------------------------------------------------------

    def level(self):
        return int(self.data.get("level", 0))

    def needs_placement(self):
        return self.level() <= 0

    def apply_placement(self, result):
        """Take the test result and set the course up from it."""
        self.data["level"] = int(result["level"])
        self.data["profil"] = result["profil"]
        self.data["einstufung"] = {
            "zeit": now(),
            "level": result["level"],
            "richtig": result["richtig"],
            "gesamt": result["gesamt"],
            "rueckblick": result["rueckblick"],
        }
        # Everything below the reached level counts as known: still open to
        # read, but not in the way of the next lesson.
        lessons = self.data.setdefault("lektionen", {})
        for chapter, lesson in curriculum.all_lessons():
            if chapter["level"] < result["level"]:
                entry = lessons.setdefault(lesson["id"], {})
                if entry.get("stand") not in ("fertig",):
                    entry["stand"] = "bekannt"
        nxt = self.next_lesson()
        self.data["letzte"] = nxt[1]["id"] if nxt[1] else ""
        self.save()

    def placement_review(self):
        record = self.data.get("einstufung")
        return record.get("rueckblick", []) if record else []

    def weak_topics(self):
        """Topics the placement test found wanting, worst first."""
        profile = self.data.get("profil") or {}
        import placement
        pairs = []
        for topic in profile:
            pairs.append((profile[topic], placement.TOPICS.get(topic, topic)))
        pairs.sort()
        return [name for score, name in pairs if score < 0.75]

    # -- lessons -----------------------------------------------------------

    def lesson_state(self, lesson_id):
        entry = (self.data.get("lektionen") or {}).get(lesson_id) or {}
        return entry.get("stand", "neu")

    def next_lesson(self):
        """The lesson to carry on with: (chapter, lesson) or (None, None).

        At or above the placement level first, because that is where the
        learner actually is; only if all of that is done does it fall back
        to anything left over below.
        """
        level = max(1, self.level())
        pending = []
        for chapter, lesson in curriculum.all_lessons():
            state = self.lesson_state(lesson["id"])
            if state == "fertig":
                continue
            pending.append((chapter, lesson, state))
        at_level = [p for p in pending if p[0]["level"] >= level]
        if at_level:
            at_level.sort(key=lambda p: (p[0]["level"], p[0]["id"]))
            return at_level[0][0], at_level[0][1]
        if pending:
            pending.sort(key=lambda p: (p[0]["level"], p[0]["id"]))
            return pending[0][0], pending[0][1]
        return None, None

    def finish_lesson(self, lesson_id, right, total):
        lessons = self.data.setdefault("lektionen", {})
        entry = lessons.setdefault(lesson_id, {})
        entry["stand"] = "fertig"
        entry["richtig"] = right
        entry["gesamt"] = total
        entry["zeit"] = now()
        chapter, lesson = curriculum.lesson_by_id(lesson_id)
        if lesson:
            share = right / float(total) if total else 1.0
            for concept in lesson["concepts"]:
                self.schedule(concept, share >= 0.6)
        self.data["letzte"] = lesson_id
        self.save()

    def save_solution(self, lesson_id, index, text):
        store = self.data.setdefault("loesungen", {})
        store["%s/%d" % (lesson_id, index)] = text
        self.save()

    def solution(self, lesson_id, index):
        return (self.data.get("loesungen") or {}).get("%s/%d" % (lesson_id, index), "")

    # -- spaced repetition --------------------------------------------------

    def schedule(self, concept, right):
        cards = self.data.setdefault("begriffe", {})
        card = cards.setdefault(concept, {"ease": EASE_START, "tage": 0,
                                          "faellig": 0, "wdh": 0})
        if right:
            card["wdh"] = card.get("wdh", 0) + 1
            if card["wdh"] == 1:
                card["tage"] = 1
            elif card["wdh"] == 2:
                card["tage"] = 3
            else:
                card["tage"] = max(1, int(round(card["tage"] * card["ease"])))
            card["ease"] = min(EASE_MAX, card.get("ease", EASE_START) + 0.1)
        else:
            card["wdh"] = 0
            card["tage"] = 1
            card["ease"] = max(EASE_MIN, card.get("ease", EASE_START) - 0.2)
        card["faellig"] = now() + card["tage"] * DAY

    def due_concepts(self):
        cards = self.data.get("begriffe") or {}
        out = []
        for concept in cards:
            if cards[concept].get("faellig", 0) <= now():
                out.append(concept)
        return out

    def due_lessons(self):
        """Lessons worth going through again, because a concept is due."""
        due = self.due_concepts()
        if not due:
            return []
        out = []
        for chapter, lesson in curriculum.all_lessons():
            if self.lesson_state(lesson["id"]) != "fertig":
                continue
            for concept in lesson["concepts"]:
                if concept in due:
                    out.append((chapter, lesson))
                    break
        return out

    # -- overview -----------------------------------------------------------

    def stats(self):
        total = len(curriculum.all_lessons())
        done = 0
        for _, lesson in curriculum.all_lessons():
            if self.lesson_state(lesson["id"]) == "fertig":
                done += 1
        return {"fertig": done, "gesamt": total,
                "faellig": len(self.due_lessons()),
                "level": self.level()}
