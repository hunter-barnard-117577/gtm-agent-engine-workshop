import os
import unittest
from types import SimpleNamespace

os.environ.setdefault("OPENAI_API_KEY", "test")

from gtm_agent.gtm_agent import SYSTEM_PROMPT, send_prospect_email


class SendProspectEmailTest(unittest.TestCase):
    def setUp(self):
        self.runtime = SimpleNamespace(config={"metadata": {"user_id": "rep_amills"}})
        self.from_rep = {"name": "Ava Mills", "email": "ava@example.com"}

    def test_disqualified_prospect_is_withheld_without_override(self):
        result = send_prospect_email.func(
            prospect={"prospect_id": "LEAD-50001", "name": "Priya Nair", "email": "priya@example.com"},
            subject="Intro",
            body="Let us connect.",
            runtime=self.runtime,
            from_rep=self.from_rep,
        )

        self.assertEqual(result["status"], "withheld")
        self.assertNotEqual(result["status"], "sent")
        self.assertIn("disqualified", result["message"])

    def test_disqualified_prospect_can_be_sent_with_explicit_override(self):
        result = send_prospect_email.func(
            prospect={"prospect_id": "LEAD-50001", "name": "Priya Nair", "email": "priya@example.com"},
            subject="Intro",
            body="Let us connect.",
            override=True,
            runtime=self.runtime,
            from_rep=self.from_rep,
        )

        self.assertEqual(result["status"], "sent")

    def test_ordinary_prospect_still_sends(self):
        result = send_prospect_email.func(
            prospect={"prospect_id": "LEAD-90003", "name": "Grace Adeyemi", "email": "grace@example.com"},
            subject="Intro",
            body="Let us connect.",
            runtime=self.runtime,
            from_rep=self.from_rep,
        )

        self.assertEqual(result["status"], "sent")

    def test_system_prompt_requires_disclosure_and_confirmation(self):
        self.assertIn("surface any record-level eligibility flag", SYSTEM_PROMPT)
        self.assertIn("ask the rep to confirm an override", SYSTEM_PROMPT)


if __name__ == "__main__":
    unittest.main()
