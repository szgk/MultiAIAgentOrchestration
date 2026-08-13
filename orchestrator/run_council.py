"""AI Council フルフロー実行: Proposal → Review → Decision"""
import sys

from orchestrator import decision, proposal, review


def main():
    print("=== Phase 1: Proposal ===")
    proposal.run()

    print("\n=== Phase 2: Review ===")
    review.run()

    print("\n=== Phase 3: Decision ===")
    result = decision.run()

    print("\n=== Complete ===")
    print(result)


if __name__ == "__main__":
    sys.exit(main())
