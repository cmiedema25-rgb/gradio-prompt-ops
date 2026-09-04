"""Template-based mock LLM that reacts to prompt instructions (no API key)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Style:
    concise: bool
    creative: bool
    json_mode: bool
    numbered: bool
    cite: bool
    must_include: tuple[str, ...]
    forbid_promise: bool


def detect_style(system: str) -> Style:
    s = system.lower()
    must = tuple(
        part.strip()
        for match in re.findall(r"must include ([^.]+)", s)
        for part in re.split(r",| and ", match)
        if part.strip()
    )
    return Style(
        concise="concise" in s or "short" in s,
        creative="creative" in s or "punchy" in s,
        json_mode="json" in s,
        numbered="step by step" in s or "numbered" in s,
        cite="cite" in s or "citation" in s,
        must_include=must,
        forbid_promise="do not promise" in s or "do not invent" in s or "no guarantee" in s,
    )


def extract_facts(user: str) -> dict[str, str]:
    facts: dict[str, str] = {}
    id_match = re.search(r"\b(LW-[\d]+|INV-[\d]+|PO-[\d]+)\b", user, re.I)
    if id_match:
        facts["id"] = id_match.group(1).upper()
    hours = re.search(r"(\d+)\s*hours?", user, re.I)
    if hours:
        facts["delay_hours"] = hours.group(1)
    cause = re.search(r"cited ([^.]+)", user, re.I)
    if cause:
        facts["cause"] = cause.group(1).strip()
    customer = re.search(r"customer is ([^.]+)", user, re.I)
    if customer:
        facts["customer"] = customer.group(1).strip()
    total = re.search(r"total[:\s]+\$?(\d+(?:\.\d+)?)", user, re.I)
    if total:
        facts["total"] = total.group(1)
    vendor = re.search(r"vendor[:\s]+([A-Za-z0-9 &-]+)", user, re.I)
    if vendor:
        facts["vendor"] = vendor.group(1).strip()
    from_to = re.search(r"from ([A-Za-z ]+) to ([A-Za-z ]+)", user, re.I)
    if from_to:
        facts["origin"] = from_to.group(1).strip()
        facts["destination"] = from_to.group(2).strip()
    if "past due" in user.lower():
        facts["status"] = "past_due"
    return facts


def generate(system: str, user: str) -> str:
    style = detect_style(system)
    facts = extract_facts(user)
    if style.json_mode:
        payload = dict(facts)
        if style.cite:
            payload["source"] = "[1]"
        return json.dumps(payload, sort_keys=True)

    bits: list[str] = []
    if facts.get("id"):
        bits.append(f"Record {facts['id']}")
    if facts.get("customer"):
        bits.append(f"for {facts['customer']}")
    if facts.get("delay_hours"):
        bits.append(f"is {facts['delay_hours']} hours delayed")
    if facts.get("cause"):
        bits.append(f"because {facts['cause']}")
    if facts.get("origin") and facts.get("destination"):
        bits.append(f"on the {facts['origin']} to {facts['destination']} lane")
    if facts.get("vendor") and facts.get("total"):
        bits.append(f"vendor {facts['vendor']} billed {facts['total']}")
    if facts.get("status"):
        bits.append(f"status {facts['status']}")

    core = " ".join(bits).strip() or "No structured facts were found in the input."
    if not core.endswith("."):
        core += "."

    if style.must_include:
        missing = [item for item in style.must_include if item.lower() not in core.lower()]
        if missing:
            core += " Includes: " + ", ".join(style.must_include) + "."

    if style.numbered:
        sentences = [s.strip() for s in re.split(r"(?<=\.)\s+", core) if s.strip()]
        core = "\n".join(f"{i}. {s}" for i, s in enumerate(sentences, start=1))

    if style.cite:
        core += " [1]"

    if style.creative and not style.forbid_promise:
        core += " We guarantee arrival tonight."

    if style.concise:
        core = core.split(" We guarantee")[0]
        if len(core) > 220:
            core = core[:217].rstrip() + "..."
    elif not style.json_mode and not style.numbered:
        core += " Please advise if you need a follow-up from dispatch."

    return core.strip()
