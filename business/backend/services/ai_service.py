import os
import json

class AIService:
    @staticmethod
    def generate_chat_reply(user_prompt, profile_data=None):
        """
        Generates personalized AI advisor responses based on the user's business & financial profile.
        Supports quick-action templates and fallback rule engine.
        """
        prompt_lower = user_prompt.lower().strip()
        profile = profile_data or {}
        
        name = profile.get('name', 'Entrepreneur')
        village = profile.get('village_town', 'your village')
        district = profile.get('district', 'your region')
        b_type = profile.get('business_type', 'business')
        rev = profile.get('monthly_revenue', 0)
        exp = profile.get('monthly_expenses', 0)
        savings = profile.get('current_savings', 0)
        investment = profile.get('initial_investment', 0)

        # 1. Budget based queries e.g. "I have ₹50,000"
        if "50,000" in prompt_lower or "50000" in prompt_lower or "budget" in prompt_lower or "start" in prompt_lower and ("50" in prompt_lower or "small" in prompt_lower):
            return (
                f"Namaste {name}! With an investment of around ₹50,000 in {village} ({district}), here are the top 3 viable rural business ideas:\n\n"
                "1. **Spices & Flour Processing Mill**: Purchase a small 3-5 HP pulverizer machine (₹30,000) and raw spices/grains (₹15,000). High demand in local households.\n"
                "2. **Custom Garment & School Uniform Sewing Unit**: 2 commercial sewing machines (₹25,000) + cloth materials (₹20,000). Rapid payback period.\n"
                "3. **Dairy & Milk Collection Outlet**: Start with 2 milch cows or act as an aggregator for local farmers to supply nearest dairy chilling center.\n\n"
                "💡 *Tip: Keep 15% (approx ₹7,500) as cash reserve for working capital!*"
            )

        # 2. Increase sales query
        if "increase sales" in prompt_lower or "grow" in prompt_lower or "more customers" in prompt_lower or "increase my sales" in prompt_lower:
            return (
                f"To boost sales for your **{b_type}** business in {district}, try these 4 proven hyperlocal strategies:\n\n"
                "1. **Weekly Haat & Festival Stall**: Set up direct pop-up displays at weekly local village markets (Haats) where foot traffic is high.\n"
                "2. **WhatsApp Group Catalog**: Create a dedicated WhatsApp Business group for your local village customers to post new stock arrivals every Monday.\n"
                "3. **Bundle Offers**: Combine slow-selling items with high-demand daily essentials at a slight combined discount.\n"
                "4. **Local B2B Supply**: Partner with nearby school canteens, tea stalls, or hotels for bulk recurring deliveries."
            )

        # 3. High expenses query
        if "expenses" in prompt_lower or "too high" in prompt_lower or "reduce costs" in prompt_lower or "cut expenses" in prompt_lower:
            net_p = float(rev) - float(exp)
            return (
                f"Analysis for your business (Current Revenue: ₹{rev:,.0f}, Expenses: ₹{exp:,.0f}, Net: ₹{net_p:,.0f}):\n\n"
                "1. **Bulk Raw Material Procurement**: Join hands with 2-3 neighbouring micro-entrepreneurs to buy raw materials directly from wholesale mandis, saving 12-18% on transport and unit prices.\n"
                "2. **Energy Audit**: Switch high-usage lighting to LED and check if your equipment qualifies for subsidized agricultural electricity tariffs.\n"
                "3. **Minimize Credit Sales (Udhar)**: Set a strict cap of max 7 days on customer credit terms to prevent cash flow choke points.\n"
                "4. **Transport Sharing**: Group delivery trips to the nearby district town twice a week instead of daily individual trips."
            )

        # 4. Suitable business for village query
        if "suitable business" in prompt_lower or "which business" in prompt_lower or "idea" in prompt_lower:
            return (
                f"Based on economic trends in **{village}, {district}**, the most profitable micro-businesses are:\n\n"
                "• **Agri-Equipment Rental Hub**: Renting sprayers, weeders, and tillers per hour.\n"
                "• **Solar & Mobile Repair Service**: Great demand as solar lanterns and mobile phones expand.\n"
                "• **Clean Packed Bio-Fertilizer / Vermicompost**: Organic farming products sell at premium prices to regional nurseries.\n\n"
                "Would you like me to calculate the Break-even point for any of these options?"
            )

        # 5. Funding / Loan query
        if "funding" in prompt_lower or "loan" in prompt_lower or "capital" in prompt_lower:
            return (
                f"For funding your {b_type} enterprise in {district}:\n\n"
                "1. **Own Contribution (Equity)**: Aim to cover at least 25-30% of your total requirement from personal savings.\n"
                "2. **Micro-Finance & Co-operative Banks**: Approach local Regional Rural Banks (RRBs) or District Co-operative Banks with a structured business plan.\n"
                "3. **Working Capital Management**: Use trade credit terms (30 days to pay suppliers) to reduce immediate loan needs.\n\n"
                "⚠️ *Note: Always verify eligibility directly with formal banking branches or authorized credit officers.*"
            )

        # Default smart response using profile context
        return (
            f"Hello {name}! As your AI Business Advisor for {b_type} in {village}, I am here to help.\n\n"
            f"Based on your current numbers (Monthly Revenue: ₹{rev:,.0f}, Expenses: ₹{exp:,.0f}), "
            "you can ask me about:\n"
            "• Strategies to cut operating costs\n"
            "• Ways to increase your monthly profit margin\n"
            "• Step-by-step guidance for expanding your business\n"
            "• Financial structure for seeking additional capital"
        )

    @staticmethod
    def generate_business_plan(data):
        """
        Generates a complete, structured 11-section business plan document.
        """
        b_name = data.get('business_name', 'GramBiz Enterprise')
        b_type = data.get('business_type', 'Micro Manufacturing')
        location = data.get('location', 'Rural India')
        investment = data.get('investment', 100000)
        target_cust = data.get('target_customers', 'Local Village Households & Regional Retailers')
        products = data.get('products_services', 'High-quality locally processed food products')
        expected_sales = data.get('expected_monthly_sales', 45000)

        inv_num = float(investment or 100000)
        sales_num = float(expected_sales or 45000)
        exp_est = sales_num * 0.65
        net_est = sales_num - exp_est

        sections = {
            "title": f"Business Plan: {b_name}",
            "generated_date": "Current Date",
            "1_executive_summary": (
                f"{b_name} is a rural micro-enterprise based in {location}, operating in the {b_type} sector. "
                f"The business aims to generate ₹{sales_num:,.0f} in monthly revenue with an initial capital setup of ₹{inv_num:,.0f}. "
                f"It fulfills an essential market gap in {location} by providing reliable products and services directly to consumers."
            ),
            "2_business_description": (
                f"{b_name} specializes in {products}. The enterprise focuses on quality consistency, "
                f"affordable pricing, and local rural customer satisfaction. It utilizes local raw materials and skilled community labor."
            ),
            "3_target_customers": (
                f"Primary customers include {target_cust}. Secondary target groups include regional wholesalers, weekly market (Haat) visitors, "
                f"and neighboring village institutions."
            ),
            "4_local_market_opportunity": (
                f"The market demand in {location} for {b_type} products is currently underserved by distant urban suppliers. "
                f"Establishing local production eliminates high regional freight costs and ensures fresher inventory delivery."
            ),
            "5_products_and_services": (
                f"Core Offerings: {products}.\n"
                f"Value Proposition: Fresh local availability, competitive rural pricing, customized unit sizing, and trustworthy customer relations."
            ),
            "6_revenue_model": (
                f"Main Revenue Source: Direct retail sales & wholesale distribution of {products}.\n"
                f"Target Monthly Revenue: ₹{sales_num:,.0f}\n"
                f"Average Unit Price Margin: 30% - 35% above direct input costs."
            ),
            "7_cost_structure": (
                f"Estimated Initial Capex: ₹{inv_num * 0.60:,.0f} (Equipment & Setup)\n"
                f"Estimated Initial Opex: ₹{inv_num * 0.40:,.0f} (Raw material stock & working capital)\n"
                f"Monthly Operating Expense: ₹{exp_est:,.0f} (Raw materials, power, labor, packaging, logistics)."
            ),
            "8_marketing_strategy": (
                "1. Word-of-mouth promotion through village council and local community leaders.\n"
                "2. Live demonstration and product trials during weekly Haats.\n"
                "3. WhatsApp Business direct messaging for repeat order placement."
            ),
            "9_financial_projection": (
                f"Monthly Revenue (Year 1 Avg): ₹{sales_num:,.0f}\n"
                f"Monthly Operating Cost: ₹{exp_est:,.0f}\n"
                f"Estimated Monthly Net Profit: ₹{net_est:,.0f}\n"
                f"Estimated Payback Period: {round(inv_num / (net_est if net_est > 0 else 1), 1)} months."
            ),
            "10_risks_and_mitigation": (
                "Risk 1: Raw material price fluctuation -> Mitigation: Maintain 1-month buffer stock.\n"
                "Risk 2: Cash flow delays from credit sales -> Mitigation: Limit customer credit to 7 days maximum."
            ),
            "11_growth_plan": (
                "Phase 1 (Months 1-6): Stabilize local village retail sales.\n"
                "Phase 2 (Months 7-12): Expand distribution to 5 neighboring villages and regional district mandi."
            )
        }

        return sections
