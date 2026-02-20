from fpdf import FPDF
from datetime import datetime
from pathlib import Path
import uuid

class Reporter:
    def __init__(self, delivery_id: str):
        self._staging_path = Path.home() / '.northhaveneyo' / 'reports'
        self._staging_path.mkdir(parents=True, exist_ok=True)
        self._delivery_id = delivery_id

    def clean_pl(self, text: str) -> str:
        """Zapobiega FPDFUnicodeEncodingException przez konwersję polskich znaków."""
        if not text:
            return ""
        replacements = {
            'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N', 'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
        }
        return "".join(replacements.get(c, c) for c in text)

    def generate(self, summary: dict, context_data: object, filename: str):
        pdf = FPDF()
        pdf.add_page()
        
        # --- HEADER ---
        pdf.set_font("Helvetica", "B", 20)
        pdf.set_text_color(40, 40, 40)
        pdf.cell(0, 15, "NORTHHAVEN AI - CREDIT RISK REPORT", ln=True)
        
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(120, 120, 120)
        pdf.cell(0, 5, f"Report ID: {str(uuid.uuid4())[:13].upper()} | Delivery: {self._delivery_id}", ln=True)
        pdf.cell(0, 5, f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.ln(10)

    
        score = summary.get("northhaven_score", 0)
        status = summary.get("status", "UNKNOWN")
        
        if status == "POSITIVE":
            color = (76, 175, 80) # Green
            verdict = "APPROVED"
        else:
            color = (244, 67, 54) # Red
            verdict = "REJECTED"

        pdf.set_fill_color(*color)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 26)
        pdf.cell(0, 25, f"SCORE: {score}/100 - {verdict}", ln=True, fill=True, align='C')
        
        # Visual Progress Bar
        pdf.set_fill_color(200, 200, 200)
        pdf.rect(10, pdf.get_y(), 190, 2, 'F')
        pdf.set_fill_color(*color)
        pdf.rect(10, pdf.get_y(), 190 * (score/100), 2, 'F')
        pdf.ln(12)

      
        pdf.set_text_color(40, 40, 40)
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "1. Executive Financial Metrics", ln=True)
        
        pdf.set_font("Helvetica", "", 10)
        dti = summary.get('dti_ratio', 0)
        stability = summary.get('stability_index', 0)
        disposable = summary.get('disposable_income', 0)
        
        pdf.cell(55, 8, "Debt-to-Income Ratio:")
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(40, 8, f"{dti:.1%}")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(60, 8, "Income Stability Index:")
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, f"{stability:.1f}%", ln=True)
        
        pdf.set_font("Helvetica", "", 10)
        pdf.cell(55, 8, "Disposable Income:")
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 8, f"{disposable:,.2f} PLN (Net Monthly Surplus)", ln=True)
        pdf.ln(5)


        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "2. AI Expert Insight & Recommendation", ln=True)
        
        pdf.set_font("Helvetica", "I", 10)
        insight = summary.get('expert_insight', "No qualitative insight available.")
 
        safe_insight = self.clean_pl(insight)
        
        pdf.set_fill_color(250, 250, 250)
        pdf.multi_cell(0, 7, f"\"{safe_insight}\"", border="L", fill=True)
        pdf.ln(5)

        # --- SECTION 3: TRANSACTIONAL ANALYSIS ---
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, "3. Categorized Cash-Flow Analysis", ln=True)
        
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(245, 245, 245)
        pdf.cell(65, 10, "Transaction Category", border=1, fill=True)
        pdf.cell(45, 10, "Total Amount (PLN)", border=1, fill=True)
        pdf.cell(45, 10, "Income Ratio", border=1, fill=True)
        pdf.cell(35, 10, "Op. Count", border=1, fill=True, ln=True)

        pdf.set_font("Helvetica", "", 10)
        details = summary.get("details", {})
        target_cats = ["salary", "gambling", "credit", "debt_collection", "operating_expenses"]
        
        for cat in target_cats:
            d = details.get(cat, {"amount": 0, "ratio": 0, "count": 0})
            pdf.cell(65, 8, cat.replace('_', ' ').title(), border=1)
            pdf.cell(45, 8, f"{d['amount']:,.2f}", border=1)
            pdf.cell(45, 8, f"{d['ratio']:.1%}", border=1)
            pdf.cell(35, 8, str(d['count']), border=1, ln=True)

        # --- SECTION 4: AI LOGIC ---
        pdf.ln(5)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 10, "4. Explainable AI (XAI) Decision Logic", ln=True)
        
        pdf.set_font("Helvetica", "I", 10)
        risk = summary.get('risk_probability', 0)
        thr = summary.get('threshold_used', 0.5)
        logic_text = (
            f"Model XGBoost v2 evaluated the transactional patterns with a risk weight of {risk:.2%}. "
            f"Decision compared against sensitivity threshold of {thr:.0%}. "
            f"Drivers: Income consistency ({stability:.0f}%) and surplus balance."
        )
        pdf.multi_cell(0, 6, logic_text)

        # --- FLAGS ---
        flags = summary.get("flags", [])
        if flags:
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(200, 0, 0)
            pdf.cell(0, 8, "SYSTEM RISK ALERTS:", ln=True)
            pdf.set_font("Helvetica", "", 9)
            for flag in flags:
                pdf.cell(0, 5, f"- {self.clean_pl(flag)}", ln=True)

        # Footer
        pdf.set_y(-20)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(160, 160, 160)
        pdf.cell(0, 10, "CONFIDENTIAL - Northhaven Analytics Proprietary AI Scoring Engine", align='C')

        # Save & Cloud Upload
        file_path = self._staging_path / filename
        pdf.output(str(file_path))
        
        try:
            from northhavenanalytics_cloudy_driver import upload_new_file
            upload_new_file(str(file_path), self._delivery_id)
        except Exception:
            pass # Silently fail if cloud driver is missing
            
        return str(file_path)