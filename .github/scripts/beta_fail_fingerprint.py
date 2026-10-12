"""Beta validation CI helper: extract the failure fingerprint from the run's
JSONL log. Prints two shell-safe lines:  FINGERPRINT=...  and  COUNT=...

Kept as a file (not an inline heredoc) because YAML run blocks mangle
indented heredocs.
"""

import glob
import json
import sys


def main() -> int:
    events = []
    for path in glob.glob("beta-out/beta-log-*.jsonl"):
        with open(path, encoding="utf-8") as fh:
            events += [json.loads(line) for line in fh]
    fails = sorted({f"{e['cenario']}/{e['acao']}" for e in events
                    if e["veredito"] == "reprova"})
    print("FINGERPRINT=" + (";".join(fails)[:180] or "infra: run did not complete"))
    print("COUNT=" + str(len(fails)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
