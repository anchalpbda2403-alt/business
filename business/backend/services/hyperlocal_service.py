class HyperlocalService:
    OPPORTUNITIES = [
        {
            "id": "dairy",
            "title": "Dairy & Milk Collection Unit",
            "category": "Agriculture & Allied",
            "demand": "High",
            "investment_range": "₹50,000 - ₹2,000,000",
            "difficulty": "Medium",
            "target_segment": "Local Dairy Co-operatives, Urban Sweet Shops, Household Consumers",
            "reason": "Consistent daily cash flow and assured demand from local dairy co-operative hubs with government fodder subsidies available.",
            "suitable_districts": ["All Rural Districts", "Anand", "Kolhapur", "Mandya", "Ludhiana", "Baramati"]
        },
        {
            "id": "food_processing",
            "title": "Mini Agro Food Processing & Packaging",
            "category": "Food Processing",
            "demand": "High",
            "investment_range": "₹75,000 - ₹3,000,000",
            "difficulty": "Medium",
            "target_segment": "Regional Wholesale Markets, Local Grocery Chains, Weekly Haats",
            "reason": "Adds 3x value to raw crops (dal milling, spice grinding, pickle making, flour milling) reducing post-harvest wastage.",
            "suitable_districts": ["Guntur", "Nashik", "Indore", "Jaipur", "Karnal", "Varanasi"]
        },
        {
            "id": "tailoring",
            "title": "Custom Garment Tailoring & Boutique",
            "category": "Handicrafts & Textiles",
            "demand": "High",
            "investment_range": "₹15,000 - ₹80,000",
            "difficulty": "Easy",
            "target_segment": "Village Residents, School Uniform Suppliers, Festival Markets",
            "reason": "Low initial capital, high repeat orders during festival and wedding seasons, suitable for micro-budget setups.",
            "suitable_districts": ["All Rural & Semi-Urban Areas"]
        },
        {
            "id": "handicrafts",
            "title": "Local Artisan Handicrafts & E-commerce",
            "category": "Crafts & Export",
            "demand": "Medium",
            "investment_range": "₹20,000 - ₹100,000",
            "difficulty": "Medium",
            "target_segment": "Urban Tourists, Export Aggregators, Online Handloom Platforms",
            "reason": "High profit margins leveraging unique local traditional skills (bamboo, terracotta, embroidery, brassware).",
            "suitable_districts": ["Kutch", "Madhubani", "Bastar", "Channapatna", "Moradabad", "Srinagar"]
        },
        {
            "id": "agri_services",
            "title": "Agricultural Machinery Rental & Drone Spraying",
            "category": "Agri-Tech Services",
            "demand": "High",
            "investment_range": "₹150,000 - ₹500,000",
            "difficulty": "Hard",
            "target_segment": "Smallholder Farmers (1-5 acres), Farming Groups, FPOs",
            "reason": "Solves acute rural labor shortages; farmers prefer renting tractors/sprayers per hour over buying expensive equipment.",
            "suitable_districts": ["Prakasam", "Bathinda", "Godavari", "Belagavi", "Koli", "Ahmednagar"]
        },
        {
            "id": "grocery",
            "title": "Smart Village Kirana & Essential Store",
            "category": "Retail",
            "demand": "High",
            "investment_range": "₹40,000 - ₹250,000",
            "difficulty": "Easy",
            "target_segment": "Local Village Households, Daily Wage Laborers",
            "reason": "Essential daily commodity velocity ensures steady inventory turnover and margin predictability.",
            "suitable_districts": ["All Villages & Towns"]
        },
        {
            "id": "repair_services",
            "title": "Solar Light, Pump & Mobile Repair Hub",
            "category": "Technical Services",
            "demand": "High",
            "investment_range": "₹25,000 - ₹120,000",
            "difficulty": "Medium",
            "target_segment": "Rural Households, Farmers, Motorcyclists",
            "reason": "Growing adoption of solar water pumps and smartphones creates urgent local repair needs.",
            "suitable_districts": ["All Rural Blocks"]
        }
    ]

    @classmethod
    def get_opportunities(cls, location="", budget=0):
        """Filters opportunities based on user budget and location string."""
        budget = float(budget or 0)
        results = []
        for opp in cls.OPPORTUNITIES:
            # Simple matching tag
            item = opp.copy()

            # Add area match score calculation
            if location and (location.lower() in [d.lower() for d in opp.get("suitable_districts", [])] or "All" in opp["suitable_districts"][0]):
                item["match_level"] = "Highly Recommended for " + location
            else:
                item["match_level"] = "Recommended"

            item["is_demo_data"] = True
            results.append(item)
        return results

    @classmethod
    def analyze_area(cls, village_town, district, state):
        """Generates a hyperlocal report for a specific rural location."""
        loc_str = f"{village_town or 'Village'}, {district or 'District'}, {state or 'State'}"
        
        return {
            "location_name": loc_str,
            "demographic_profile": "Rural / Semi-Urban Agricultural Cluster",
            "key_drivers": ["Agriculture", "Dairy Husbandry", "Local Haat Commerce", "Micro-scale Services"],
            "recommended_sectors": [
                "Dairy Collection & Chilling",
                "Agro-processing (Flour, Spices, Oil Extraction)",
                "Custom Machinery Rental",
                "Solar Pump & Electronics Repair"
            ],
            "market_demand_summary": f"High consumer demand in {district or 'local region'} for daily essential goods and post-harvest crop processing.",
            "disclaimer": "Demo hyperlocal market analysis generated based on regional micro-economic data."
        }
