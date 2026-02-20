import pandas as pd
import numpy as np
import re
from .constants import CATEGORIES, RULES, KEYWORD_RULES


class Eyo:
    def __init__(self, raw_input_data, categories=CATEGORIES, model: str = "paraphrase-multilingual-MiniLM-L12-v2"):
        from .utils import load_csv, normalize_columns

        df = load_csv(raw_input_data)
        self._input_data = normalize_columns(df)
        self._input_data = self._input_data.reset_index(drop=True)

  

        if "amount" not in self._input_data.columns:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                self._input_data["amount"] = df[numeric_cols[0]]
            else:
                raise ValueError("CRITICAL: None column with amount.")

        for col in ["contractor", "title"]:
            if col not in self._input_data.columns:
                self._input_data[col] = ""

        self._categories = categories
        self._model_to_use = model

    def keyword_classify(self, text: str) -> str | None:
    
        text_lower = text.lower()
        for category, keywords in KEYWORD_RULES.items():
            for kw in keywords:
                if kw in text_lower:
                    return category
        return None

    def clean_text(self, text):
        text = str(text)
        text = re.sub(r'\d{5,}', '', text)
        text = re.sub(r'\b(SP\.\s?Z\s?O\.O\.|S\.A\.|LTD|GMBH|CORP|INC)\b', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\b\d{1,4}[./-]\d{1,2}[./-]\d{1,4}\b', '', text)
        return " ".join(text.split()).lower()

    def _parse_amounts(self, series):
        """Correctly parses amounts in any locale format:
           - 1 234,56  (PL: space thousands, comma decimal)
           - 1.234,56  (EU: dot thousands, comma decimal)
           - 1,234.56  (US: comma thousands, dot decimal)
           - 1234.56   (standard)
        """
        def _parse_one(val):
            s = str(val).strip().replace('\xa0', '').replace('\u00a0', '').replace(' ', '')
            has_dot = '.' in s
            has_comma = ',' in s
            if has_dot and has_comma:
                # whichever comes last is the decimal separator
                if s.rindex(',') > s.rindex('.'):
                    # EU format: 1.234,56
                    s = s.replace('.', '').replace(',', '.')
                else:
                    # US format: 1,234.56
                    s = s.replace(',', '')
            elif has_comma:
                # only comma — treat as decimal: 1234,56
                s = s.replace(',', '.')
            # strip anything left that isn't a digit, dot, or leading minus
            s = re.sub(r'[^\d.-]', '', s)
            try:
                return float(s)
            except (ValueError, TypeError):
                return 0.0

        return series.apply(_parse_one)

    def calc_policy_verdict(self, results, values_to_check=RULES):
        df_ml = pd.DataFrame(results)

        df_ml["amount"] = self._parse_amounts(self._input_data["amount"].astype(str))


        salary_matches = df_ml[(df_ml['category'] == 'salary') & (df_ml['amount'] > 0)]
        total_income = salary_matches['amount'].sum()

        fallback_income = False
        if total_income <= 0:
            all_income = df_ml[df_ml['amount'] > 0]
            if len(all_income) > 0:
                salary_matches = all_income
                total_income = salary_matches['amount'].sum()
                fallback_income = True


        summary = {"status": "POSITIVE", "flags": [], "details": {}}

        if total_income <= 0:
            summary["status"] = "NEGATIVE"
            summary["flags"].append("Blad walidacji: Brak wykrytych wplywow (Salary/Income).")
        elif fallback_income:
            summary["flags"].append("Info: Dochod wykryty jako przychod ogolny (model nie wykryl kategorii Salary).")

        for rule in values_to_check:
            cat = rule["name"]
            limit = rule["conf_limit"]
            max_ratio = rule.get("max_ratio", 0.0)

            matches = df_ml[(df_ml['category'] == cat) & (df_ml['confidence'] >= limit)]

            if cat == "salary":
                total_cat_amount = total_income
                count = len(salary_matches)
            else:
                category_expenses = matches[matches["amount"] < 0]
                total_cat_amount = abs(category_expenses["amount"].sum())
                count = len(category_expenses)

            ratio = total_cat_amount / total_income if total_income > 0 else 0
            summary["details"][cat] = {
                "amount": float(total_cat_amount),
                "ratio": round(float(ratio), 4),
                "count": int(count)
            }
            

            if ratio > max_ratio or (cat == "debt_collection" and count > 0 and max_ratio == 0):
               
                summary["status"] = "NEGATIVE"
                summary["flags"].append(f"Ryzyko: {cat.replace('_', ' ').capitalize()} przekracza limit.")

        return summary

    def build_tensor(self, eyo_summary, context_data):
        vector = []
        # TODO: refactor - make more reusable variables.
        vector.extend([
            float(context_data.age), float(context_data.employment_months),
            float(context_data.dependents), float(context_data.declared_income),
            float(context_data.loan_amount), float(context_data.monthly_costs)
        ])

       
        for cat in self._categories.keys():
            data = eyo_summary['details'].get(cat, {"ratio": 0, "amount": 0, "count": 0})
            vector.extend([float(data['ratio']), float(data['amount']), float(data['count'])])

    
        income = eyo_summary['details'].get('salary', {}).get('amount', 0)
    
 
        clean_amounts = self._parse_amounts(self._input_data["amount"].astype(str))
    

        total_real_expenses = abs(clean_amounts[clean_amounts < 0].sum())

        declared_costs = float(context_data.monthly_costs)
    

        disposable_income = income - total_real_expenses - declared_costs
    
        vector.append(float(disposable_income))
        vector.append(float(eyo_summary.get('northhaven_score', 0)))

        return np.array(vector).reshape(1, -1)

    def run(self):
        from .model import Model
        model_engine = Model(self._categories, self._model_to_use)

        text_cols = [col for col in ["contractor", "title"] if col in self._input_data.columns]
        if not text_cols:
            text_cols = list(self._input_data.select_dtypes(include=['object']).columns)

   

        text_for_ml = []
        for i in range(len(self._input_data)):
            row = self._input_data.iloc[i]
            combined = " ".join([str(row[col]) for col in text_cols if str(row[col]).strip()])
            text_for_ml.append(self.clean_text(combined if combined else "brak opisu"))

        self._input_data['text_for_ml'] = text_for_ml

    
        keyword_results = []
        needs_ml = []  

        for i, text in enumerate(text_for_ml):
            kw_cat = self.keyword_classify(text)
            if kw_cat:
                keyword_results.append((i, {"category": kw_cat, "confidence": 1.0}))
            else:
                needs_ml.append(i)

  
        ml_results = {}
        if needs_ml:
            ml_texts = [text_for_ml[i] for i in needs_ml]
            embeddings = model_engine._model.encode(
                ml_texts,
                convert_to_tensor=True,
                show_progress_bar=False
            )
            ml_classified = model_engine.classify(embeddings)
            for i, result in zip(needs_ml, ml_classified):
                ml_results[i] = result

  
        final_results = []
        kw_dict = {i: r for i, r in keyword_results}
        for i in range(len(text_for_ml)):
            if i in kw_dict:
                final_results.append(kw_dict[i])
            else:
                final_results.append(ml_results[i])

      
        return final_results