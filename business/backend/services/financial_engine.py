import math

class FinancialEngine:
    @staticmethod
    def calculate_health_score(monthly_revenue, monthly_expenses, current_savings, existing_loan):
        """
        Calculates an AI Financial Health Score (0-100) based on rural financial indicators.
        Returns a dictionary with score, rating label, strengths, improvement areas, and next steps.
        """
        revenue = float(monthly_revenue or 0)
        expenses = float(monthly_expenses or 0)
        savings = float(current_savings or 0)
        loan = float(existing_loan or 0)

        if revenue <= 0:
            net_profit = -expenses
            profit_margin = 0.0
        else:
            net_profit = revenue - expenses
            profit_margin = (net_profit / revenue) * 100.0

        # 1. Profitability Factor (30 pts)
        if profit_margin >= 35:
            profit_score = 30
        elif profit_margin >= 20:
            profit_score = 25
        elif profit_margin >= 10:
            profit_score = 18
        elif profit_margin > 0:
            profit_score = 10
        else:
            profit_score = 0

        # 2. Expense Control Factor (25 pts)
        expense_ratio = (expenses / revenue) if revenue > 0 else 1.0
        if expense_ratio <= 0.50:
            expense_score = 25
        elif expense_ratio <= 0.70:
            expense_score = 20
        elif expense_ratio <= 0.85:
            expense_score = 12
        else:
            expense_score = 5

        # 3. Cash Reserve / Emergency Fund Factor (20 pts)
        months_runway = (savings / expenses) if expenses > 0 else 0
        if months_runway >= 6:
            cash_score = 20
        elif months_runway >= 3:
            cash_score = 15
        elif months_runway >= 1:
            cash_score = 10
        else:
            cash_score = 4

        # 4. Debt Burden Factor (15 pts)
        monthly_est_emi = (loan * 0.02) if loan > 0 else 0
        debt_to_income = (monthly_est_emi / revenue) if revenue > 0 else (0.5 if loan > 0 else 0)
        if debt_to_income <= 0.15:
            debt_score = 15
        elif debt_to_income <= 0.30:
            debt_score = 10
        elif debt_to_income <= 0.45:
            debt_score = 5
        else:
            debt_score = 0

        # 5. Business Stability Base (10 pts)
        stability_score = 8 if revenue > 15000 else 5

        total_score = min(100, max(10, round(profit_score + expense_score + cash_score + debt_score + stability_score)))

        if total_score >= 80:
            rating = "Excellent"
        elif total_score >= 65:
            rating = "Good"
        elif total_score >= 50:
            rating = "Fair"
        else:
            rating = "Needs Attention"

        # Strengths & Improvement Areas
        strengths = []
        improvements = []
        next_steps = []

        if profit_margin > 20:
            strengths.append(f"Healthy profit margin of {profit_margin:.1f}%.")
        else:
            improvements.append("Profit margin is tight. Explore higher margin products or direct customer sales.")

        if expense_ratio < 0.70:
            strengths.append("Expenses are well-controlled relative to revenue.")
        else:
            improvements.append("Monthly expenses exceed 70% of total sales.")

        if months_runway >= 3:
            strengths.append(f"Strong cash buffer estimated at {months_runway:.1f} months of expenses.")
        else:
            improvements.append("Low emergency cash reserve. Build at least 3 months of operational expenses.")

        if loan == 0:
            strengths.append("Zero existing debt burden.")
        elif debt_to_income > 0.35:
            improvements.append("Debt repayment places significant pressure on monthly cash flow.")

        if not strengths:
            strengths.append("Active business operational structure established.")

        # Recommendations
        if net_profit > 0:
            next_steps.append("Reinvest 20% of net profits into inventory or machinery upgrade.")
        next_steps.append("Maintain strict digital logging of daily raw material costs.")
        if loan > 0:
            next_steps.append("Prioritize clearing high-interest unorganized loans before taking new credit.")

        return {
            "score": total_score,
            "rating": rating,
            "net_profit": round(net_profit, 2),
            "profit_margin": round(profit_margin, 2),
            "strengths": strengths,
            "areas_for_improvement": improvements,
            "recommended_next_steps": next_steps,
            "disclaimer": "AI-generated informational indicator, not an official credit score."
        }

    @staticmethod
    def calculate_emi(principal, annual_interest_rate=10.5, tenure_months=24):
        """Calculates monthly EMI using standard compounding formula."""
        P = float(principal or 0)
        if P <= 0:
            return 0.0
        r = (float(annual_interest_rate) / 12.0) / 100.0
        n = int(tenure_months or 24)

        if r == 0:
            return round(P / n, 2)

        emi = P * r * (math.pow(1 + r, n)) / (math.pow(1 + r, n) - 1)
        return round(emi, 2)

    @staticmethod
    def perform_financial_structuring(data):
        """
        Takes inputs:
        - initial_investment
        - monthly_revenue
        - monthly_fixed_costs
        - monthly_variable_costs
        - expected_growth_pct
        - loan_amount
        - loan_interest_rate
        - loan_tenure_months
        """
        inv = float(data.get('initial_investment') or 0)
        rev = float(data.get('monthly_revenue') or 0)
        fc = float(data.get('monthly_fixed_costs') or 0)
        vc = float(data.get('monthly_variable_costs') or 0)
        growth_pct = float(data.get('expected_growth_pct') or 5.0)
        loan = float(data.get('loan_amount') or 0)
        rate = float(data.get('loan_interest_rate') or 10.5)
        tenure = int(data.get('loan_tenure_months') or 24)

        total_monthly_expense = fc + vc
        estimated_profit = rev - total_monthly_expense
        profit_margin = ((estimated_profit / rev) * 100.0) if rev > 0 else 0.0

        # EMI calculation
        monthly_emi = FinancialEngine.calculate_emi(loan, rate, tenure)

        # Funding Gap (Initial investment required vs available savings/loan)
        savings = float(data.get('current_savings') or 0)
        funding_gap = max(0.0, inv - (savings + loan))

        # Break-even point (revenue needed to cover fixed costs assuming current gross margin)
        # Gross margin = (Revenue - Variable Costs) / Revenue
        gross_margin_ratio = ((rev - vc) / rev) if rev > 0 and rev > vc else 0.40
        break_even_revenue = (fc / gross_margin_ratio) if gross_margin_ratio > 0 else (fc * 2)

        # 12-Month Projections
        projections = []
        current_m_rev = rev
        current_m_exp = total_monthly_expense

        for m in range(1, 13):
            # Compound growth applied quarterly or monthly
            monthly_g = (growth_pct / 100.0) / 12.0
            m_rev = round(current_m_rev * math.pow(1 + monthly_g, m - 1), 2)
            m_exp = round(current_m_exp * math.pow(1 + (monthly_g * 0.5), m - 1), 2) # Expenses grow slower
            m_profit = round(m_rev - m_exp, 2)
            projections.append({
                "month": f"Month {m}",
                "revenue": m_rev,
                "expense": m_exp,
                "profit": m_profit
            })

        return {
            "total_monthly_expense": round(total_monthly_expense, 2),
            "estimated_profit": round(estimated_profit, 2),
            "profit_margin": round(profit_margin, 2),
            "break_even_revenue": round(break_even_revenue, 2),
            "monthly_emi": monthly_emi,
            "funding_gap": round(funding_gap, 2),
            "projections": projections
        }
