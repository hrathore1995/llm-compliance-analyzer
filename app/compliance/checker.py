import re
import json
from app.compliance.rules import ComplianceRules
from langchain_openai import ChatOpenAI


class ComplianceChecker:
    def __init__(self):
        self.rules = ComplianceRules().get_rules()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def _rule_based_check(self, text: str):
        findings = {}
        for law, rules in self.rules.items():
            law_findings = []
            for rule in rules:
                if re.search(rule["pattern"], text, re.IGNORECASE):
                    law_findings.append(rule["description"])
            findings[law] = law_findings if law_findings else ["Not Detected"]
        return findings

    def _llm_check(self, text: str):
        """Ask LLM to semantically check compliance mentions."""
        prompt = f"""
        You are a compliance auditor. Given the text below, determine if it relates to
        HIPAA (health data), FERPA (student data), or SOX (financial reporting).
        Respond ONLY in JSON with this structure:
        {{
            "HIPAA": "Relevant" | "Not Relevant",
            "FERPA": "Relevant" | "Not Relevant",
            "SOX": "Relevant" | "Not Relevant"
        }}

        Text:
        {text}
        """
        response = self.llm.predict(prompt)

        # Try parsing JSON
        try:
            return json.loads(response)
        except:
            return {"HIPAA": "Unknown", "FERPA": "Unknown", "SOX": "Unknown"}

    def check(self, text: str):
        # Run both checks
        rule_results = self._rule_based_check(text)
        llm_results = self._llm_check(text)

        # Compare results for agreement/disagreement
        status = []
        for law in ["HIPAA", "FERPA", "SOX"]:
            if llm_results.get(law) == "Relevant" and (
                rule_results.get(law) != ["Not Detected"]
            ):
                status.append(f"{law}: Rules + LLM agree")
            elif llm_results.get(law) == "Relevant" and (
                rule_results.get(law) == ["Not Detected"]
            ):
                status.append(f"{law}: LLM flagged but rules missed")
            elif llm_results.get(law) == "Not Relevant" and (
                rule_results.get(law) != ["Not Detected"]
            ):
                status.append(f"{law}: Rules flagged but LLM disagreed")
            else:
                status.append(f"{law}: Not flagged")

        return {
            "rules": rule_results,
            "llm": llm_results,
            "status": status
        }
