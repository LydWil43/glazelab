def seed(db, Glaze, Ingredient, Material):
    glazes = [
        # ── BATCH 7/1/25 ────────────────────────────────────────────────────
        {
            "studio_number": "studio-liner", "name": "Studio Liner Glaze", "glazy_id": "645006",
            "batch_date": "7/1/25", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation, Salt & Soda, Wood",
            "surface": "Semi-glossy", "transparency": "Translucent", "status": "testing",
            "notes": "Adjusted for no wollastonite. Does not craze on Peters stoneware or Takamori. Water 100%.",
            "ingredients": [("EP Kaolin", 28.60, False), ("Gerstley Borate", 20.50, False), ("Custer Feldspar", 18.50, False), ("Silica", 17.70, False), ("Dolomite", 14.70, False)]
        },
        {
            "studio_number": "3", "name": "Malcolm Davis Carbon Trap", "glazy_id": "4180",
            "batch_date": "7/1/25", "cone": "Cone 10", "atmosphere": "Reduction", "status": "production",
            "notes": "From Steve Davis. NC-4 substituted for F-4.",
            "ingredients": [("Nepheline Syenite", 38.60, False), ("EP Kaolin", 17.00, False), ("Soda Ash", 16.30, False), ("Kentucky OM #4 Ball Clay", 13.00, False), ("Kona F-4 Feldspar (NC-4 sub)", 9.30, False), ("Redart", 5.70, False)]
        },
        {
            "studio_number": "7", "name": "Lavender Crackle", "glazy_id": "582126",
            "batch_date": "7/1/25", "cone": "Cone 10", "atmosphere": "Oxidation", "surface": "Matte", "transparency": "Opaque", "status": "testing",
            "ingredients": [("Custer Feldspar", 44.40, False), ("Silica", 29.40, False), ("Magnesium Carbonate", 17.10, False), ("Grolleg Kaolin", 10.10, False), ("Cobalt Carbonate", 0.75, True)]
        },
        {
            "studio_number": "16", "name": "Galactic Indifference", "glazy_id": "20466",
            "batch_date": "7/1/25", "cone": "Cone 6–10", "atmosphere": "Oxidation, Neutral, Reduction, Wood, Salt & Soda", "status": "production",
            "notes": "Mike Stumbras recipe, cone 10 soda. Steven Hill Strontium Crystal Magic version. Has run crazy in the past.",
            "ingredients": [("NC-4 Feldspar", 42.40, False), ("Whiting", 17.90, False), ("EP Kaolin", 12.00, False), ("Titanium Dioxide", 12.00, False), ("Dolomite", 7.30, False), ("Ferro Frit 3124", 4.00, False), ("Lithium Carbonate", 4.00, False), ("Bentonite", 2.00, False)]
        },
        {
            "studio_number": "17", "name": "John Britt Snowflake Crackle 13", "glazy_id": "428144",
            "batch_date": "7/1/25", "cone": "Cone 10", "atmosphere": "Reduction", "surface": "Semi-glossy", "status": "testing",
            "notes": "SNF #8. From John Britt Ceramics Monthly 2011.",
            "ingredients": [("Nepheline Syenite", 81.67, False), ("Talc", 7.43, False), ("EP Kaolin", 5.45, False), ("Bone Ash", 3.96, False), ("Ferro Frit 3124", 1.49, False)]
        },
        {
            "studio_number": "18", "name": "Smithereens", "glazy_id": "186292",
            "batch_date": "7/1/25", "cone": "Cone 10", "atmosphere": "Oxidation, Neutral, Reduction", "surface": "Glossy", "status": "testing",
            "notes": "50/50 blend of Ice Ice Baby and Snowflake Crackle 13.",
            "ingredients": [("Nepheline Syenite", 61.50, False), ("Custer Feldspar", 22.50, False), ("Talc", 5.60, False), ("EP Kaolin", 4.50, False), ("Bone Ash", 4.00, False), ("Ferro Frit 3134", 1.90, False)]
        },
        {
            "studio_number": "19", "name": "Jungle Green but also purple", "glazy_id": "673536",
            "batch_date": "7/1/25", "cone": "Cone 10", "atmosphere": "Oxidation", "status": "testing",
            "notes": "Double dipped test tile.",
            "ingredients": [("Potash Feldspar", 30.48, False), ("Silica", 23.39, False), ("Manganese Carbonate", 18.61, False), ("Whiting", 14.80, False), ("EP Kaolin", 8.60, False), ("Copper Carbonate", 3.36, True), ("Tin Oxide", 0.76, True)]
        },
        {
            "studio_number": "20", "name": "Magnesium Matte", "glazy_id": "646910",
            "batch_date": "7/1/25", "cone": "Cone unknown", "atmosphere": "Oxidation", "status": "testing",
            "notes": "Apply thick. Use Custer instead of G-200.",
            "ingredients": [("Whiting", 31.91, False), ("Dolomite", 23.40, False), ("EP Kaolin", 21.28, False), ("Spodumene", 21.28, False), ("Tin Oxide", 6.38, True), ("G-200 Feldspar", 2.13, False)]
        },
        {
            "studio_number": "21", "name": "Bray Shino", "glazy_id": "646911",
            "batch_date": "7/1/25", "cone": "Cone 10", "atmosphere": "Oxidation", "status": "testing",
            "notes": "Use hot water to dissolve soda ash. Dec 2015 Ceramics Monthly.",
            "ingredients": [("Nepheline Syenite", 45.50, False), ("Minspar 200", 18.40, False), ("Kentucky OM #4 Ball Clay", 16.60, False), ("Spodumene", 15.40, False), ("Soda Ash", 4.10, False)]
        },
        {
            "studio_number": "22", "name": "White Salt", "glazy_id": "646913",
            "batch_date": "7/1/25", "cone": "Cone 10", "atmosphere": "Reduction", "status": "testing",
            "notes": "Base for yellow salt. Best under a very dark clay body in reduction.",
            "ingredients": [("Nepheline Syenite", 71.60, False), ("Dolomite", 23.60, False), ("Zircopax", 18.80, True), ("Kentucky OM #4 Ball Clay", 4.80, False), ("Bentonite", 4.00, True), ("Rutile", 1.10, True)]
        },
        {
            "studio_number": "23", "name": "Tom Turner Non Running Crystalline Glaze", "glazy_id": "165946",
            "batch_date": "7/1/25", "cone": "Cone 9–11", "atmosphere": "Oxidation", "status": "testing",
            "notes": "Firing schedule: 200F/hr to 250F hold 20 min; 350F/hr to 1800F hold 30 min; 350F/hr to 2295F; drop 1000F/hr to 2245F hold 1 hr.",
            "ingredients": [("Minspar 200", 48.21, False), ("Zinc Oxide", 22.32, False), ("Silica", 14.29, False), ("Whiting", 5.36, False), ("Copper Carbonate", 3.57, True), ("Rutile", 3.57, True), ("Bentonite", 1.79, True), ("Titanium Dioxide", 0.89, True)]
        },
        # ── BATCH 8/26/25 ───────────────────────────────────────────────────
        {
            "studio_number": "24", "name": "Barium Matte", "glazy_id": "99273",
            "batch_date": "8/26/25", "cone": "Cone 8–11", "atmosphere": "Oxidation", "surface": "Matte", "status": "testing",
            "notes": "Runs. Fires cone 8–10. Nice complement over glossy glazes.",
            "ingredients": [("Custer Feldspar", 46.80, False), ("Barium Carbonate", 18.70, False), ("Kentucky OM #4 Ball Clay", 8.93, False), ("Zinc Oxide", 6.86, False), ("Whiting", 6.86, False), ("Titanium Dioxide", 6.58, True), ("Bone Ash", 4.79, False), ("Cobalt Carbonate", 0.47, True)]
        },
        {
            "studio_number": "26", "name": "Hayley's Light Blue and Green Swirl", "glazy_id": "420729",
            "batch_date": "8/26/25", "cone": "Cone 9–11", "atmosphere": "Reduction", "status": "testing",
            "notes": "Fall 2023 Hayley Feary. Crystal formation in deep blue areas.",
            "ingredients": [("Custer Feldspar", 53.00, False), ("Talc", 12.00, False), ("Whiting", 12.00, False), ("Silica", 9.00, False), ("EP Kaolin", 8.00, False), ("Titanium Dioxide", 4.00, True), ("Borax", 2.00, False), ("Cobalt Carbonate", 1.00, True)]
        },
        {
            "studio_number": "27", "name": "Copper Salt", "glazy_id": "44283",
            "batch_date": "8/26/25", "cone": "Cone 9–12", "atmosphere": "Oxidation, Neutral, Reduction, Salt & Soda, Wood", "status": "testing",
            "ingredients": [("Nepheline Syenite A270", 71.50, False), ("Dolomite", 23.50, False), ("Kentucky OM #4 Ball Clay", 5.00, False), ("Zircopax", 16.00, True), ("Bentonite", 2.00, True), ("Copper Carbonate", 1.00, True)]
        },
        {
            "studio_number": "28", "name": "Yellow Salt (John Britt)", "glazy_id": "3152",
            "batch_date": "8/26/25", "cone": "Cone 10", "atmosphere": "Reduction", "surface": "Glossy", "transparency": "Opaque", "status": "production",
            "notes": "As listed in John Britt High-Fire Glazes.",
            "ingredients": [("Nepheline Syenite", 71.60, False), ("Dolomite", 23.60, False), ("Ball Clay", 4.80, False), ("Zircopax", 17.90, True), ("Bentonite", 4.00, True), ("Red Iron Oxide", 1.10, True)]
        },
        {
            "studio_number": "29", "name": "Bronze Chinese", "glazy_id": "201",
            "batch_date": "8/26/25", "cone": "Cone 10", "atmosphere": "Oxidation, Reduction", "surface": "Matte", "status": "production",
            "notes": "Bright matt green copper patina. From Ayumi Horie.",
            "ingredients": [("Nepheline Syenite", 42.70, False), ("Barium Carbonate", 38.80, False), ("Ball Clay", 10.70, False), ("Silica", 7.80, False), ("Titanium Dioxide", 4.00, True), ("Red Iron Oxide", 3.00, True), ("Copper Carbonate", 1.00, True)]
        },
        {
            "studio_number": "31", "name": "Pete Pinnell Strontium Matte", "glazy_id": "504",
            "batch_date": "8/26/25", "cone": "Cone 9–11", "atmosphere": "Oxidation, Reduction", "surface": "Satin-matte", "status": "production",
            "notes": "Green: copper carb 5 + titanium diox 5. Grey: titanium diox 5. Turquoise: copper carb 5. Flocculate with Epsom salts or Muriatic Acid.",
            "ingredients": [("Nepheline Syenite", 60.00, False), ("Strontium Carbonate", 20.00, False), ("Ball Clay", 10.00, False), ("Silica", 9.00, False), ("Lithium Carbonate", 1.00, False), ("Bentonite", 2.00, True)]
        },
        {
            "studio_number": "32", "name": "Blue Acero", "glazy_id": "6",
            "batch_date": "8/26/25", "cone": "Cone 9–11", "atmosphere": "Wood", "surface": "Satin-matte", "status": "production",
            "notes": "From Doug Casebeer, used at Curaumilla. Muted blue-green.",
            "ingredients": [("Custer Feldspar", 50.90, False), ("EP Kaolin", 24.00, False), ("Whiting", 21.30, False), ("Talc", 3.80, False), ("Bentonite", 1.90, True), ("Red Iron Oxide", 1.70, True), ("Cobalt Carbonate", 0.20, True)]
        },
        {
            "studio_number": "33", "name": "Blue Robin's Egg Spot", "glazy_id": "174",
            "batch_date": "8/26/25", "cone": "Cone 10", "atmosphere": "Reduction", "surface": "Satin-matte", "transparency": "Opaque", "status": "production",
            "notes": "Medium blue with olive spots.",
            "ingredients": [("Custer Feldspar", 51.00, False), ("Strontium Carbonate", 15.50, False), ("Ball Clay", 9.80, False), ("Whiting", 8.80, False), ("Zinc Oxide", 7.60, False), ("Bone Ash", 2.20, False), ("Rutile", 8.70, True), ("Bentonite", 2.00, True), ("Cobalt Carbonate", 1.00, True)]
        },
        # ── BATCH 9/2/25 ────────────────────────────────────────────────────
        {
            "studio_number": "34", "name": "Indigo Matte", "glazy_id": "673235",
            "batch_date": "9/2/25", "cone": "Cone 8–11", "atmosphere": "Wood, Salt & Soda, Reduction, Neutral, Oxidation", "surface": "Semi-glossy", "status": "testing",
            "notes": "Adjusted for no ilmenite and sub barium.",
            "ingredients": [("Nepheline Syenite A270", 45.13, False), ("Strontium Carbonate", 27.05, False), ("Silica", 9.45, False), ("Tennessee Ball Clay", 7.18, False), ("Lithium Carbonate", 1.10, False), ("Copper Carbonate", 4.00, True), ("Titanium Dioxide", 0.98, True)]
        },
        {
            "studio_number": "35", "name": "No1 MG1 Base (matte white)", "glazy_id": "44685",
            "batch_date": "9/2/25", "cone": "Cone 6", "atmosphere": "Oxidation", "surface": "Satin", "transparency": "Opaque", "status": "testing",
            "ingredients": [("Nepheline Syenite", 34.00, False), ("Kaolin", 21.00, False), ("Dolomite", 18.00, False), ("Silica", 16.00, False), ("Gerstley Borate", 9.00, False), ("Whiting", 4.00, False), ("Bentonite", 2.00, True)]
        },
        {
            "studio_number": "36", "name": "Galactic Indifference Rx", "glazy_id": "30518",
            "batch_date": "9/2/25", "cone": "Cone 10", "atmosphere": "Oxidation, Neutral, Reduction, Wood, Salt & Soda", "status": "production",
            "notes": "Tweaked to run less by GL. Adaptation of Galactic Indifference (#16).",
            "lineage_notes": "Adaptation of #16 Galactic Indifference.",
            "ingredients": [("NC-4 Feldspar", 44.40, False), ("Whiting", 16.90, False), ("EP Kaolin", 13.00, False), ("Titanium Dioxide", 12.00, True), ("Dolomite", 6.30, False), ("Silica", 6.00, False), ("Ferro Frit 3124", 5.00, False), ("Lithium Carbonate", 4.00, False), ("Bentonite", 1.00, True)]
        },
        {
            "studio_number": "37", "name": "Shaner Green (Copy)", "glazy_id": "674021",
            "batch_date": "9/2/25", "cone": "Cone 10", "atmosphere": "Reduction", "status": "testing",
            "ingredients": [("Custer Feldspar", 46.50, False), ("EP Kaolin", 22.10, False), ("Whiting", 18.80, False), ("Bone Ash", 9.10, False), ("Talc", 3.50, False), ("Copper Carbonate", 2.90, True)]
        },
        {
            "studio_number": "38", "name": "Nuka like ash glaze", "glazy_id": "674022",
            "batch_date": "9/2/25", "cone": "Cone 6–10", "atmosphere": "Reduction", "surface": "Satin", "status": "testing",
            "ingredients": [("Custer Feldspar", 45.00, False), ("Wood Ash", 35.00, False), ("Silica", 20.00, False), ("Titanium Dioxide", 4.00, True), ("Bentonite", 2.00, True)]
        },
        {
            "studio_number": "39", "name": "Satin Rust — Finnerty", "glazy_id": "611",
            "batch_date": "9/2/25", "cone": "Cone 9–10", "atmosphere": "Reduction", "surface": "Satin-matte", "transparency": "Opaque", "status": "production",
            "notes": "From Kathryn Finnerty.",
            "ingredients": [("Spodumene", 27.40, False), ("Kaolin", 19.00, False), ("Wollastonite", 18.80, False), ("Strontium Carbonate", 16.40, False), ("Silica", 12.40, False), ("Zinc Oxide", 6.00, False), ("Red Iron Oxide", 2.00, True), ("Chrome Oxide", 0.50, True)]
        },
        {
            "studio_number": "40", "name": "Sunshine Yellow", "glazy_id": "420078",
            "batch_date": "9/2/25", "cone": "Cone 10", "atmosphere": "Reduction", "surface": "Semi-matte", "transparency": "Opaque", "status": "testing",
            "ingredients": [("Nepheline Syenite", 53.29, False), ("Strontium Carbonate", 18.96, False), ("Dolomite", 10.65, False), ("EP Kaolin", 8.90, False), ("Zircopax", 8.20, True), ("Red Iron Oxide", 2.45, True), ("Bentonite", 2.00, True)]
        },
        {
            "studio_number": "41", "name": "Emerald Teal", "glazy_id": "601150",
            "batch_date": "9/2/25", "cone": "Cone 9–11", "atmosphere": "Reduction", "surface": "Glossy", "transparency": "Opaque", "status": "testing",
            "notes": "EPK substituted for China Clay. Green to blue-black. SG 1.40.",
            "ingredients": [("Nepheline Syenite", 74.60, False), ("Silica", 8.70, False), ("EP Kaolin", 6.90, False), ("Dolomite", 4.90, False), ("Whiting", 2.70, False), ("Rutile", 3.00, True), ("Zinc Oxide", 2.20, True), ("Cobalt Carbonate", 2.00, True), ("Bentonite", 1.50, True)]
        },
        {
            "studio_number": "43", "name": "Coleman Yellow Crystal", "glazy_id": "674023",
            "batch_date": "9/2/25", "cone": "Cone 10", "atmosphere": "Reduction", "surface": "Satin-matte", "status": "testing",
            "notes": "Exterior/decorative surfaces only. Yields butter-smooth glaze with crystals. Yellow gold: add 2% yellow iron oxide. From Ceramics Monthly Jan 2003.",
            "ingredients": [("Custer Feldspar", 44.73, False), ("Whiting", 16.93, False), ("EP Kaolin", 13.90, False), ("Strontium Carbonate", 11.75, False), ("Gerstley Borate", 7.26, False), ("Lithium Carbonate", 4.83, False), ("Zinc Oxide", 0.60, False), ("Titanium Dioxide", 16.93, True)]
        },
        {
            "studio_number": "46", "name": "Ginger's Green Crackle", "glazy_id": "46456",
            "batch_date": "9/2/25", "cone": "Cone 6–10", "atmosphere": "Oxidation", "status": "production",
            "notes": "Wanted a green crackle, made a green crackle.",
            "ingredients": [("Nepheline Syenite", 80.50, False), ("Whiting", 11.50, False), ("Silica", 5.50, False), ("Lithium Carbonate", 2.50, False), ("Epsom Salts", 2.00, True), ("Copper Carbonate", 1.50, True), ("Chrome Oxide", 0.50, True)]
        },
        {
            "studio_number": "47", "name": "Cobalt Pink/Mauve/Lilac", "glazy_id": "3564",
            "batch_date": "9/2/25", "cone": "Cone 10", "atmosphere": "Oxidation", "surface": "Matte", "status": "production",
            "notes": "Not a liner glaze. Frosty lavender where very thick, breaks soft blue. Deflocculate for ease of application. Recipe may have changed — may need more zinc for the pink.",
            "ingredients": [("EP Kaolin", 33.00, False), ("Talc (amtalc c98/pioneer)", 31.00, False), ("Strontium Carbonate", 17.50, False), ("Silica", 16.00, False), ("Zinc Oxide", 10.00, False), ("Lithium Carbonate", 3.00, False), ("Cobalt Carbonate", 2.00, True)]
        },
        {
            "studio_number": "48", "name": "Haynes Satin V2 (Copy)", "glazy_id": "673548",
            "batch_date": "9/2/25", "cone": "Cone 9–10", "atmosphere": "Oxidation, Reduction, Neutral, Salt & Soda, Wood", "surface": "Satin-matte", "status": "testing",
            "notes": "Added 8% clay for suspension and more silica to return to satin. Altered to retain chemistry but replace talc.",
            "ingredients": [("Nepheline Syenite A270", 56.83, False), ("Dolomite", 21.19, False), ("Silica", 8.15, False), ("EP Kaolin", 7.09, False), ("Whiting", 5.30, False), ("Magnesium Carbonate", 1.44, False), ("Bentonite", 3.00, True)]
        },
        {
            "studio_number": "49", "name": "Jaded Green", "glazy_id": "594103",
            "batch_date": "9/2/25", "cone": "Cone 10", "atmosphere": "Reduction", "surface": "Smooth Matte", "status": "testing",
            "notes": "SG 1.50. Salt is Dead Sea salt.",
            "ingredients": [("Nepheline Syenite", 53.00, False), ("Strontium Carbonate", 31.00, False), ("Ball Clay", 8.00, False), ("Silica", 8.00, False), ("Rutile", 5.00, True), ("Salt (Dead Sea)", 3.00, True), ("Bentonite", 2.00, True), ("Copper Carbonate", 2.00, True)]
        },
        {
            "studio_number": "50", "name": "Pumpkin", "glazy_id": "674015",
            "batch_date": "9/2/25", "cone": "Cone unknown", "atmosphere": "Oxidation", "status": "testing",
            "ingredients": [("G-200 Feldspar", 51.17, False), ("EP Kaolin", 24.26, False), ("Whiting", 20.68, False), ("Talc", 3.88, False), ("Red Iron Oxide", 3.88, True), ("Rutile", 3.88, True), ("Bone Ash", 2.90, True), ("Bentonite", 1.94, True)]
        },
        {
            "studio_number": "51", "name": "Pinnell Celadon", "glazy_id": "673998",
            "batch_date": "9/2/25", "cone": "Cone unknown", "atmosphere": "Oxidation", "status": "testing",
            "ingredients": [("Silica", 35.00, False), ("G-200 Feldspar", 25.00, False), ("Grolleg Kaolin", 20.00, False), ("Whiting", 20.00, False), ("Red Iron Oxide", 1.00, True)]
        },
        {
            "studio_number": "52", "name": "Ash Glaze", "glazy_id": "674019",
            "batch_date": "9/2/25", "cone": "Cone unknown", "atmosphere": "Oxidation", "status": "testing",
            "ingredients": [("Wood Ash", 50.00, False), ("Minspar 200", 50.00, False), ("Ball Clay", 5.00, False), ("Silica", 5.00, False)]
        },
        {
            "studio_number": "53", "name": "Coleman Kaki", "glazy_id": "2977",
            "batch_date": "9/2/25", "cone": "Cone 8–10", "atmosphere": "Reduction", "surface": "Satin", "transparency": "Opaque", "status": "production",
            "notes": "From John Britt The Complete Guide to High Fire Glazes.",
            "ingredients": [("Custer Feldspar", 48.00, False), ("Silica", 16.00, False), ("Bone Ash", 11.00, False), ("Talc", 9.00, False), ("Whiting", 9.00, False), ("Kaolin", 7.00, False), ("Red Iron Oxide", 11.50, True)]
        },
        # ── BATCH 10/22/25 ──────────────────────────────────────────────────
        {
            "studio_number": "54", "name": "PCSSB 1.0", "glazy_id": "622291",
            "batch_date": "10/22/25", "cone": "Cone 10", "atmosphere": "Oxidation, Reduction", "status": "testing",
            "notes": "Additional water: 85%. Tested with extensive colorant progressions: copper carb (1/3/5%), copper+nickel, cobalt+nickel, chrome+copper combinations.",
            "lineage_notes": "Has colorant progressions — see test records.",
            "ingredients": [("Mahavir Feldspar", 49.00, False), ("EP Kaolin", 21.00, False), ("Strontium Carbonate", 13.00, False), ("Whiting", 12.00, False), ("Silica", 5.00, False)]
        },
        {
            "studio_number": "55", "name": "Studio Liner Glaze (Copy)", "glazy_id": "699670",
            "batch_date": "10/22/25", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation, Salt & Soda, Wood", "surface": "Semi-glossy", "transparency": "Translucent", "status": "testing",
            "notes": "Adjusted to get a creamy white. Adaptation of Studio Liner Glaze.",
            "lineage_notes": "Adaptation of Studio Liner Glaze.",
            "ingredients": [("EP Kaolin", 28.60, False), ("Gerstley Borate", 20.50, False), ("Custer Feldspar", 18.50, False), ("Silica", 15.00, False), ("Dolomite", 14.70, False), ("Zircopax", 10.00, True), ("Rutile", 1.00, True)]
        },
        {
            "studio_number": "56", "name": "White Liner", "glazy_id": "699657",
            "batch_date": "10/22/25", "cone": "Cone 10", "atmosphere": "Oxidation, Reduction", "status": "testing",
            "notes": "Also named 22. Optimized for R2O:RO and SiO2:Al2O3 ratios — satin that does not craze and is durable.",
            "ingredients": [("Nepheline Syenite", 70.00, False), ("Dolomite", 23.60, False), ("Zircopax", 18.80, True), ("Silica", 12.00, False), ("Kentucky OM #4 Ball Clay", 4.80, False), ("Bentonite", 4.00, True), ("Rutile", 1.10, True)]
        },
        {
            "studio_number": "57", "name": "Cobalt Pink", "glazy_id": "673495",
            "batch_date": "10/22/25", "cone": "Cone 10", "atmosphere": "Oxidation", "surface": "Matte", "status": "testing",
            "ingredients": [("EP Kaolin", 29.86, False), ("Talc (amtalc c98/pioneer)", 28.06, False), ("Strontium Carbonate", 15.84, False), ("Silica", 14.48, False), ("Zinc Oxide", 9.05, False), ("Lithium Carbonate", 2.72, False), ("Cobalt Carbonate", 1.81, True)]
        },
        {
            "studio_number": "58", "name": "Magic White", "glazy_id": "523759",
            "batch_date": "10/22/25", "cone": "Cone 6–10", "atmosphere": "Oxidation, Reduction", "surface": "Glossy", "transparency": "Opaque", "status": "testing",
            "notes": "Brad Sondahl standard liner posted 1997. Works on white and brown stoneware with no crazing. Cone 6–10 oxidation and reduction.",
            "ingredients": [("Custer Feldspar", 22.00, False), ("Silica", 20.00, False), ("Whiting", 20.00, False), ("Zirconium Dioxide", 17.00, True), ("Ball Clay", 10.00, False), ("Zinc Oxide", 6.00, False), ("Spodumene", 5.00, False), ("Epsom Salts", 1.00, True)]
        },
        {
            "studio_number": "59", "name": "G2571A — Cone 10 Silky Dolomite Matte Base", "glazy_id": "159925",
            "batch_date": "10/22/25", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation, Salt & Soda, Wood", "status": "testing",
            "ingredients": [("Custer Feldspar", 28.50, False), ("EP Kaolin", 28.00, False), ("Dolomite", 19.00, False), ("Silica", 15.00, False), ("Wollastonite", 5.50, False), ("Gerstley Borate", 4.00, False)]
        },
        {
            "studio_number": "60", "name": "Liner White Test #2", "glazy_id": "708996",
            "batch_date": "10/22/25", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation, Salt & Soda, Wood", "surface": "Semi-glossy", "status": "testing",
            "notes": "Adjusted for creamy white. Frit 3134 substituted for Gerstley Borate. Adaptation of Studio Liner.",
            "lineage_notes": "Adaptation of Studio Liner lineage with Frit 3134 substitution.",
            "ingredients": [("EP Kaolin", 29.20, False), ("Dolomite", 16.58, False), ("Ferro Frit 3134", 14.19, False), ("Silica", 13.49, False), ("Custer Feldspar", 10.40, False), ("Zircopax", 9.23, True), ("Rutile", 0.93, True), ("Red Iron Oxide", 0.06, True)]
        },
        {
            "studio_number": "61", "name": "Liner White Test #3", "glazy_id": "708997",
            "batch_date": "10/22/25", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation, Salt & Soda, Wood", "surface": "Semi-glossy", "status": "testing",
            "notes": "Frit 3134 substituted for Gerstley Borate. Pearl Ash replaces Custer.",
            "lineage_notes": "Adaptation of Studio Liner lineage.",
            "ingredients": [("EP Kaolin", 35.51, False), ("Silica", 19.25, False), ("Dolomite", 17.34, False), ("Ferro Frit 3134", 15.02, False), ("Zircopax", 9.67, True), ("Pearl Ash", 2.26, False), ("Rutile", 0.96, True)]
        },
        {
            "studio_number": "62", "name": "Titanium Green (Copy 4)", "glazy_id": "709373",
            "batch_date": "10/22/25", "cone": "Cone 10", "atmosphere": "Oxidation", "surface": "Matte", "status": "testing",
            "notes": "Handwritten note: 1/21/26 tiles.",
            "ingredients": [("EP Kaolin", 37.47, False), ("Silica", 26.26, False), ("Dolomite", 17.16, False), ("Strontium Carbonate", 10.26, False), ("Titanium Dioxide", 4.81, True), ("Pearl Ash", 4.00, False), ("Lithium Carbonate", 2.07, False), ("Cobalt Carbonate", 0.98, True)]
        },
        {
            "studio_number": "63", "name": "30/30 Ash Glaze", "glazy_id": "711517",
            "batch_date": "10/22/25", "cone": "Cone unknown", "atmosphere": "Reduction", "status": "testing",
            "notes": "Barely less crazing than #94 on Takamori. Different proportions from standard 30/30.",
            "ingredients": [("Wood Ash", 50.00, False), ("Minspar 200", 50.00, False), ("Silica", 40.00, False), ("Kentucky OM #4 Ball Clay", 30.00, False)]
        },
        # ── BATCH 1/2/26 ────────────────────────────────────────────────────
        {
            "studio_number": "64", "name": "Opaque Liner — Pumpkin", "glazy_id": "734284",
            "batch_date": "1/2/26", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation", "surface": "Semi-glossy", "transparency": "Semi-opaque", "status": "draft",
            "notes": "Attempting pumpkin colour on Takamori and stoneware. Hopefully satin.",
            "lineage_notes": "Adaptation of the Opaque Liner lineage.",
            "ingredients": [("Tile #6 Kaolin", 31.36, False), ("Dolomite", 17.81, False), ("Ferro Frit 3134", 15.25, False), ("Silica", 14.49, False), ("Mahavir Feldspar", 11.17, False), ("Zircopax", 9.92, True), ("Rutile", 4.88, True), ("Red Iron Oxide", 3.87, True)]
        },
        {
            "studio_number": "65", "name": "Clear Liner (Test using 3134)", "glazy_id": "734267",
            "batch_date": "1/2/26", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation, Salt & Soda, Wood", "surface": "Semi-glossy", "transparency": "Translucent", "status": "draft",
            "notes": "Clear base. Parent recipe of the #107 Opaque Liner lineage.",
            "lineage_notes": "Parent of #107 Opaque Liner lineage. Zircopax and Rutile added in later versions for opacity. Also parent of #109 (updated dolomite/silica ratios).",
            "umf_expansion": 6.4,
            "ingredients": [("EP Kaolin", 34.26, False), ("Silica", 19.28, False), ("Dolomite", 19.13, False), ("Ferro Frit 3134", 16.64, False), ("Mahavir Feldspar", 10.70, False)]
        },
        {
            "studio_number": "66", "name": "PCSSB 1.0 — Pumpkin Variation", "glazy_id": "734307",
            "batch_date": "1/2/26", "cone": "Cone 10", "atmosphere": "Oxidation, Reduction", "status": "draft",
            "lineage_notes": "Color variation of #54 PCSSB 1.0.",
            "ingredients": [("Mahavir Feldspar", 49.00, False), ("EP Kaolin", 21.00, False), ("Strontium Carbonate", 13.00, False), ("Whiting", 12.00, False), ("Silica", 5.00, False), ("Red Iron Oxide", 4.00, True), ("Rutile", 4.00, True)]
        },
        {
            "studio_number": "67a", "name": "PCSSB 1.0 — Titanium Green Variation", "glazy_id": "734308",
            "batch_date": "1/2/26", "cone": "Cone 10", "atmosphere": "Oxidation, Reduction", "status": "draft",
            "notes": "NOTE: #67 number collision — see also #67b. To be renumbered.",
            "lineage_notes": "Color variation of #54 PCSSB 1.0.",
            "ingredients": [("Mahavir Feldspar", 47.57, False), ("EP Kaolin", 20.39, False), ("Strontium Carbonate", 12.62, False), ("Whiting", 11.65, False), ("Silica", 4.85, False), ("Titanium Dioxide", 2.91, True), ("Lithium Carbonate", 1.94, True), ("Cobalt Carbonate", 1.75, True)]
        },
        # ── BATCH 1/26/26 ───────────────────────────────────────────────────
        {
            "studio_number": "67b", "name": "Satin Base For Alkaline Colors", "glazy_id": "734979",
            "batch_date": "1/26/26", "cone": "Cone 10", "atmosphere": "Oxidation", "surface": "Matte", "status": "draft",
            "notes": "NOTE: #67 number collision — to be renumbered.",
            "ingredients": [("Tile #6 Kaolin", 36.73, False), ("Silica", 25.74, False), ("Dolomite", 16.82, False), ("Strontium Carbonate", 10.05, False), ("Titanium Dioxide", 4.72, True), ("Pearl Ash", 3.92, False), ("Lithium Carbonate", 2.03, False)]
        },
        {
            "studio_number": "68", "name": "Satin Base Calcium Matte", "glazy_id": "734982",
            "batch_date": "1/26/26", "cone": "Cone 10", "atmosphere": "Oxidation, Reduction", "status": "draft",
            "notes": "Additional water: 85%.",
            "ingredients": [("Mahavir Feldspar", 49.00, False), ("Tile #6 Kaolin", 21.00, False), ("Strontium Carbonate", 13.00, False), ("Whiting", 12.00, False), ("Silica", 5.00, False)]
        },
        {
            "studio_number": "69", "name": "Cone 10 Bright Clear", "glazy_id": "734986",
            "batch_date": "1/26/26", "cone": "Cone 10", "atmosphere": "Reduction, Oxidation, Neutral", "surface": "Glossy", "transparency": "Transparent", "status": "draft",
            "ingredients": [("Mahavir Feldspar", 49.60, False), ("Kentucky OM #4 Ball Clay", 20.10, False), ("Whiting", 20.03, False), ("Ferro Frit 3134", 5.82, False), ("Silica", 5.38, False), ("Magnesium Carbonate", 0.07, False)]
        },
        {
            "studio_number": "70", "name": "Glossy Clear — Chemical Match", "glazy_id": "734989",
            "batch_date": "1/26/26", "cone": "Cone 6–10", "atmosphere": "Oxidation", "surface": "Semi-glossy", "transparency": "Transparent", "status": "draft",
            "notes": "Used over mason stained slips at cone 6 and cone 10. Slightly cloudy where thick, very clear thin to medium.",
            "ingredients": [("Tile #6 Kaolin", 20.23, False), ("Ferro Frit 3134", 20.00, False), ("Mahavir Feldspar", 19.74, False), ("Silica", 19.10, False), ("Wollastonite", 15.08, False), ("Talc", 5.75, False), ("Bone Ash", 0.12, False)]
        },
        {
            "studio_number": "71", "name": "Shaner Clear (FR) — Transparent", "glazy_id": "734990",
            "batch_date": "1/26/26", "cone": "Cone 10", "atmosphere": "Oxidation, Reduction", "surface": "Semi-glossy", "transparency": "Transparent", "status": "draft",
            "notes": "Alfred University version. Very clear, like glass. CoE 59.5. Calculated temp 1254C.",
            "ingredients": [("Silica", 32.33, False), ("Kaolin", 26.07, False), ("Wollastonite", 22.36, False), ("Pearl Ash", 5.35, False), ("Zinc Oxide", 5.00, False), ("Talc", 3.32, False), ("Red Iron Oxide", 0.24, True), ("Titanium Dioxide", 0.03, True)]
        },
        {
            "studio_number": "72", "name": "Oribe", "glazy_id": "734991",
            "batch_date": "1/26/26", "cone": "Cone 6–10", "atmosphere": "Oxidation, Reduction", "surface": "Semi-glossy", "transparency": "Semi-opaque", "status": "draft",
            "notes": "Green semi-transparent. Breaks from green to teal. Stable applied thinly, runs if thick. SG 1.57. Water 80%.",
            "ingredients": [("Mahavir Feldspar", 20.46, False), ("Ferro Frit 3134", 20.19, False), ("Tile #6 Kaolin", 18.52, False), ("Silica", 17.46, False), ("Whiting", 14.67, False), ("Copper Carbonate", 7.15, True), ("Rutile", 1.56, True)]
        },
        {
            "studio_number": "73", "name": "Mermaid Tail (Copy)", "glazy_id": "743243",
            "batch_date": "1/26/26", "cone": "Cone 6–10", "atmosphere": "Oxidation, Neutral", "surface": "Matte", "transparency": "Semi-opaque", "status": "draft",
            "notes": "Soft satin matte. Titanium nucleates crystals — thicker coat causes smaller crystals. Stable at hot cone 6. Water 100%.",
            "ingredients": [("Nepheline Syenite", 27.36, False), ("Strontium Carbonate", 21.63, False), ("EP Kaolin", 18.87, False), ("Ferro Frit 3195", 18.75, False), ("Silica", 8.89, False), ("Whiting", 4.51, False), ("Copper Carbonate", 5.00, True), ("Titanium Dioxide", 4.00, True)]
        },
        {
            "studio_number": "74", "name": "Yellow Salt", "glazy_id": "745197",
            "batch_date": "1/26/26", "cone": "Cone unknown", "status": "draft",
            "ingredients": [("Nepheline Syenite", 58.46, False), ("Dolomite", 19.30, False), ("Ultrox", 14.64, True), ("Kentucky OM #4 Ball Clay", 3.94, False), ("Bentonite", 3.66, True), ("Red Iron Oxide", 0.92, True)]
        },
        {
            "studio_number": "75", "name": "Spotted Green", "glazy_id": "745200",
            "batch_date": "1/26/26", "cone": "Cone unknown", "status": "draft",
            "ingredients": [("Silica", 26.79, False), ("Zinc Oxide", 25.00, False), ("EP Kaolin", 19.64, False), ("Dolomite", 14.29, False), ("Spodumene", 14.29, False), ("Copper Carbonate", 10.71, True), ("Titanium Dioxide", 8.93, True)]
        },
        {
            "studio_number": "76", "name": "DCR Tenmoku Green (Copy)", "glazy_id": "745201",
            "batch_date": "1/26/26", "cone": "Cone 10", "atmosphere": "Reduction, Salt & Soda, Wood", "surface": "Semi-matte", "transparency": "Semi-opaque", "status": "draft",
            "notes": "NZ origin. SG 1.54. 51 Hydrometer.",
            "ingredients": [("Silica", 24.00, False), ("Whiting", 24.00, False), ("China Clay Ultrafine", 24.00, False), ("Soda Feldspar 200# NZ", 24.00, False), ("Talc", 4.00, False), ("Red Iron Oxide", 9.00, True), ("Bentonite", 1.00, True)]
        },
        {
            "studio_number": "77", "name": "Rutile Green", "glazy_id": "745929",
            "batch_date": "1/26/26", "cone": "Cone 10", "atmosphere": "Reduction", "surface": "Semi-glossy", "transparency": "Semi-opaque", "status": "draft",
            "notes": "Green, variable. Runs where thick, semi-transparent where thin. Breaks well over texture.",
            "ingredients": [("Custer Feldspar", 27.78, False), ("Silica", 24.35, False), ("EP Kaolin", 15.56, False), ("Dolomite", 14.63, False), ("Whiting", 10.28, False), ("Rutile", 7.41, True), ("Copper Carbonate", 2.55, True)]
        },
        {
            "studio_number": "78", "name": "Liz Kraus Shino (Copy)", "glazy_id": "745203",
            "batch_date": "1/26/26", "cone": "Cone 9–13", "atmosphere": "Reduction, Wood", "surface": "Semi-glossy", "transparency": "Opaque", "status": "draft",
            "notes": "Very dependable shino. Orange where thin, yellowish/white where thick.",
            "ingredients": [("Nepheline Syenite", 40.00, False), ("Spodumene", 30.00, False), ("Kentucky OM #4 Ball Clay", 17.04, False), ("Soda Ash", 7.96, False), ("EP Kaolin", 5.00, False), ("Bentonite", 2.04, True)]
        },
        {
            "studio_number": "79", "name": "Flashing Slip A", "glazy_id": "745936",
            "batch_date": "1/26/26", "cone": "Cone unknown", "status": "draft",
            "ingredients": [("EP Kaolin", 55.00, False), ("Silica", 20.00, False), ("Kentucky OM #4 Ball Clay", 10.00, False), ("Nepheline Syenite", 10.00, False), ("Red Iron Oxide", 0.25, True)]
        },
        {
            "studio_number": "80", "name": "Flashing Slip B", "glazy_id": "745940",
            "batch_date": "1/26/26", "cone": "Cone unknown", "status": "draft",
            "ingredients": [("EP Kaolin", 60.00, False), ("Nepheline Syenite", 30.00, False), ("Redart", 10.00, False)]
        },
        {
            "studio_number": "81", "name": "Green Tenmoku / no Minspar DCR Tenmoku Green", "glazy_id": "745267",
            "batch_date": "1/26/26", "cone": "Cone 10", "atmosphere": "Reduction, Salt & Soda, Wood", "surface": "Semi-matte", "status": "draft",
            "notes": "SG 1.54. Adaptation of DCR Tenmoku Green without Minspar.",
            "lineage_notes": "Adaptation of #76 without Minspar.",
            "ingredients": [("Silica", 54.83, False), ("Whiting", 25.06, False), ("Red Iron Oxide", 9.48, True), ("Pearl Ash", 6.32, False), ("Talc", 4.29, False), ("Titanium Dioxide", 0.02, True)]
        },
        {
            "studio_number": "82", "name": "BCM Green — With Variations", "glazy_id": "745947",
            "batch_date": "1/26/26", "cone": "Cone 10", "atmosphere": "Oxidation, Reduction, Neutral", "surface": "Semi-matte", "transparency": "Opaque", "status": "draft",
            "notes": "BCM Green from Sherman Hall Cone 10 Glaze book. Variations: V1 Rutile 5%/CuCO 1%, V1A adds BCuO 2%, V8 Rutile 10.5%/CuCO 2%/Soda Ash 5%.",
            "lineage_notes": "Has multiple colorant variations — see test records.",
            "ingredients": [("Silica", 30.00, False), ("Nepheline Syenite", 20.00, False), ("Talc", 20.00, False), ("Whiting", 20.00, False), ("EP Kaolin", 10.00, False)]
        },
        {
            "studio_number": "83", "name": "Key Lime Pie (Copy)", "glazy_id": "746318",
            "batch_date": "1/26/26", "cone": "Cone 9–10", "atmosphere": "Oxidation", "surface": "Glossy", "transparency": "Semi-opaque", "status": "draft",
            "ingredients": [("Nepheline Syenite", 38.00, False), ("Silica", 26.00, False), ("Whiting", 14.00, False), ("Gerstley Borate", 12.00, False), ("Kaolin", 10.00, False), ("Copper Carbonate", 9.50, True), ("Tin Oxide", 3.50, True), ("Black Iron Oxide", 1.00, True)]
        },
        {
            "studio_number": "84", "name": "Hayley's Light Blue Green (Copy)", "glazy_id": "746340",
            "batch_date": "1/26/26", "cone": "Cone 9–11", "atmosphere": "Reduction", "surface": "Matte", "transparency": "Opaque", "status": "draft",
            "notes": "Light blue and green blends show tiny crystals forming.",
            "ingredients": [("Nepheline Syenite", 41.00, False), ("Silica", 20.00, False), ("Bentonite", 11.00, True), ("Talc", 9.00, False), ("Whiting", 9.00, False), ("Dolomite", 5.00, False), ("Rutile", 5.00, True), ("Cobalt Carbonate", 2.00, True)]
        },
        {
            "studio_number": "85", "name": "Wood Ash Glaze Test (chemistry based)", "glazy_id": "746359",
            "batch_date": "1/26/26", "cone": "Cone unknown", "status": "draft",
            "ingredients": [("Silica", 31.00, False), ("Wood Ash", 23.00, False), ("Mahavir Feldspar", 23.00, False), ("EP Kaolin", 15.00, False), ("Wollastonite", 8.00, False)]
        },
        {
            "studio_number": "86", "name": "Wood Ash Sub More Calcium", "glazy_id": "746365",
            "batch_date": "1/26/26", "cone": "Cone unknown", "atmosphere": "Reduction", "status": "draft",
            "notes": "Currently being tested as accent glaze in reduction (March 2026).",
            "ingredients": [("Wood Ash", 50.00, False), ("Mahavir Feldspar", 30.00, False), ("Wollastonite", 20.00, False)]
        },
        {
            "studio_number": "87", "name": "Amber Celadon McKenzie Smith", "glazy_id": "746556",
            "batch_date": "1/26/26", "cone": "Cone 9–10", "atmosphere": "Reduction", "surface": "Glossy", "transparency": "Transparent", "status": "draft",
            "notes": "Very shiny, medium value, good transparency. Golden brown. Runs thick. Used by Kent McLaughlin.",
            "ingredients": [("Custer Feldspar", 41.00, False), ("Wood Ash", 22.00, False), ("Silica", 17.00, False), ("Whiting", 17.00, False), ("Ball Clay", 4.00, False), ("Red Iron Oxide", 8.00, True), ("Bentonite", 2.00, True)]
        },
        {
            "studio_number": "88", "name": "Coleman's Patina Green (Copy)", "glazy_id": "746568",
            "batch_date": "1/26/26", "cone": "Cone 9–10", "atmosphere": "Reduction", "surface": "Satin", "transparency": "Opaque", "status": "draft",
            "notes": "BARIUM CARBONATE IS TOXIC — wear respirator when dry mixing.",
            "ingredients": [("Custer Feldspar", 52.00, False), ("Barium Carbonate", 38.00, False), ("EP Kaolin", 10.00, False), ("Rutile", 8.00, True), ("Copper Carbonate", 4.00, True)]
        },
        {
            "studio_number": "89", "name": "Joe's Green (Copy)", "glazy_id": "746570",
            "batch_date": "1/26/26", "cone": "Cone 9–10", "atmosphere": "Oxidation, Reduction", "surface": "Matte", "transparency": "Semi-opaque", "status": "draft",
            "ingredients": [("Custer Feldspar (2000-2012 Ron Roy)", 46.00, False), ("Whiting", 34.00, False), ("EP Kaolin", 20.00, False), ("Copper Carbonate", 5.00, True)]
        },
        # ── BATCH 2/3/26 ────────────────────────────────────────────────────
        {
            "studio_number": "91", "name": "Ellies Ash Test — Highest Silica", "glazy_id": "751265",
            "batch_date": "2/3/26", "cone": "Cone unknown", "atmosphere": "Reduction", "status": "draft",
            "notes": "Ash glaze silica progression. Crazed on Takamori despite high silica — confirmed silica alone cannot fix crazing.",
            "lineage_notes": "Part of ash glaze silica progression series with #92, #93, #94.",
            "ingredients": [("Silica", 33.33, False), ("Wood Ash", 23.81, False), ("G-200 Feldspar", 23.81, False), ("Ball Clay", 19.05, False)]
        },
        {
            "studio_number": "92", "name": "Ellies Ash Test — Lowest Silica", "glazy_id": "751264",
            "batch_date": "2/3/26", "cone": "Cone unknown", "atmosphere": "Reduction", "status": "draft",
            "notes": "Crazed on Takamori.",
            "lineage_notes": "Part of ash glaze silica progression series with #91, #93, #94.",
            "ingredients": [("Wood Ash", 33.33, False), ("G-200 Feldspar", 33.33, False), ("Silica", 26.67, False), ("Ball Clay", 6.67, False)]
        },
        {
            "studio_number": "93", "name": "Ellies Ash Test — Highest Ball Clay", "glazy_id": "751263",
            "batch_date": "2/3/26", "cone": "Cone unknown", "atmosphere": "Reduction", "status": "draft",
            "lineage_notes": "Part of ash glaze ball clay progression series with #91, #92, #94.",
            "ingredients": [("Ball Clay", 36.84, False), ("Wood Ash", 26.32, False), ("G-200 Feldspar", 26.32, False), ("Silica", 10.53, False)]
        },
        {
            "studio_number": "94", "name": "Ellies Ash Test — Lowest Alumina (Base)", "glazy_id": "751267",
            "batch_date": "2/3/26", "cone": "Cone 9–10", "atmosphere": "Reduction", "status": "draft",
            "notes": "Base ash glaze for active testing. Expansion 9.7. Crazed deeply on Takamori — target expansion ~6.1–6.4.",
            "lineage_notes": "Active test base. Has progression tests: dolomite/whiting swap (108A–D), lithium carbonate wet progression (Test D), Frit 3134 wet addition (Test E), Frit 3134 substitution series (#110–#113). Pull up detailed notes for full UMF analysis.",
            "umf_expansion": 9.7, "umf_r2o_ro": "0.48:0.52", "umf_al2o3": 0.34, "umf_sio2": 2.27,
            "ingredients": [("Wood Ash (spruce/birch, unwashed)", 34.48, False), ("G-200 Feldspar", 34.48, False), ("Ball Clay", 24.14, False), ("Silica", 6.90, False)]
        },
        {
            "studio_number": "95", "name": "Phil Rogers Ash (G-200)", "glazy_id": "751269",
            "batch_date": "2/3/26", "cone": "Cone 10", "atmosphere": "Reduction", "surface": "Semi-glossy", "transparency": "Translucent", "status": "draft",
            "notes": "Added a little bentonite for glaze suspension.",
            "ingredients": [("Wood Ash", 53.00, False), ("G-200 Feldspar", 29.00, False), ("Silica", 7.00, False), ("Tile #6 Kaolin", 6.00, False), ("Whiting", 5.00, False)]
        },
        {
            "studio_number": "96", "name": "Fake Ash 1", "glazy_id": "751271",
            "batch_date": "2/3/26", "cone": "Cone unknown", "status": "draft",
            "ingredients": [("Redart", 46.80, False), ("Dolomite", 36.68, False), ("Kentucky OM #4 Ball Clay", 16.00, False), ("Soda Ash", 0.52, False)]
        },
        # ── BATCH 2/17/26 ───────────────────────────────────────────────────
        {
            "studio_number": "97", "name": "Rutile B-1", "glazy_id": "753640",
            "batch_date": "2/17/26", "cone": "Cone unknown", "status": "draft",
            "ingredients": [("G-200 Feldspar", 30.10, False), ("Silica", 26.90, False), ("EP Kaolin", 16.00, False), ("Dolomite", 15.10, False), ("Whiting", 11.30, False), ("Bentonite", 2.28, True), ("Yellow Iron Oxide", 2.28, True), ("Zircopax", 1.14, True)]
        },
        {
            "studio_number": "98", "name": "Durable Satin", "glazy_id": "754812",
            "batch_date": "2/17/26", "cone": "Cone 10", "atmosphere": "Oxidation, Reduction, Neutral", "surface": "Semi-matte", "transparency": "Opaque", "status": "draft",
            "notes": "BCM Green from Sherman Hall Cone 10 Glaze book.",
            "ingredients": [("Silica", 30.00, False), ("Nepheline Syenite", 20.00, False), ("Talc", 20.00, False), ("Whiting", 20.00, False), ("EP Kaolin", 10.00, False), ("Rutile", 5.00, True)]
        },
        {
            "studio_number": "99", "name": "Crowbalt (Spodumene Var.)", "glazy_id": "252497",
            "batch_date": "2/17/26", "cone": "Cone 10", "atmosphere": "Oxidation", "surface": "Glossy", "transparency": "Transparent", "status": "testing",
            "notes": "Lithium substituted in place of KNaO. Slightly brighter than Crowbalt. Additional water: 80%.",
            "ingredients": [("Barium Carbonate", 34.00, False), ("Silica", 34.00, False), ("Spodumene", 25.00, False), ("EP Kaolin", 7.00, False), ("Chrome Oxide", 1.00, True), ("Cobalt Carbonate", 1.00, True)]
        },
        {
            "studio_number": "100", "name": "Tea Dust", "glazy_id": "18289",
            "batch_date": "2/17/26", "cone": "Cone 9–11", "atmosphere": "Neutral, Reduction, Oxidation", "surface": "Glossy", "transparency": "Translucent", "status": "production",
            "notes": "Golden West College Tea Dust. Gloss black with olive speckles. Finicky with application. In reduction cooling only by closing damper when temperature is hit. Can go completely pond scum green and shiny metallic.",
            "ingredients": [("Custer Feldspar", 39.81, False), ("Silica", 25.00, False), ("Whiting", 15.74, False), ("Kentucky OM #4 Ball Clay", 12.04, False), ("Amtalc-C98 Talc", 7.41, False), ("Red Iron Oxide", 9.30, True)]
        },
        {
            "studio_number": "101", "name": "Triini Winter Forest", "glazy_id": "737029",
            "batch_date": "2/3/26", "cone": "Cone 6–9", "atmosphere": "Oxidation", "surface": "Glossy", "transparency": "Translucent", "status": "testing",
            "notes": "Bristol glaze. Fired to 1230C. From Triin Lehismets, Estonia.",
            "ingredients": [("Nepheline Syenite Spectrum N45", 38.27, False), ("Silica", 27.75, False), ("Zinc Oxide", 16.26, False), ("Whiting", 9.09, False), ("Grolleg Kaolin", 4.78, False), ("Tin Oxide", 2.40, True), ("Copper Carbonate", 1.44, True)]
        },
        {
            "studio_number": "102", "name": "Crystal Blue #383 Emmanuel Cooper's", "glazy_id": "385",
            "batch_date": "2/3/26", "cone": "Cone 10", "atmosphere": "Oxidation, Reduction", "surface": "Glossy", "transparency": "Opaque", "status": "production",
            "notes": "Crystalline. Slate blue with small crystals, green centers with white halo. Slightly fluid, narrow firing range.",
            "ingredients": [("G-200 Feldspar", 36.84, False), ("Silica", 31.58, False), ("Dolomite", 21.05, False), ("Whiting", 10.53, False), ("Rutile", 10.53, True), ("Bentonite", 5.26, True), ("Cobalt Carbonate", 1.58, True)]
        },
        {
            "studio_number": "103", "name": "CJ Frosty Crystal", "glazy_id": "18051",
            "batch_date": "2/3/26", "cone": "Cone 6–10", "atmosphere": "Oxidation", "status": "production",
            "notes": "Micro crystalline. Handwritten note: copper carbs.",
            "ingredients": [("Nepheline Syenite", 40.00, False), ("Silica", 29.00, False), ("Zinc Oxide", 19.00, False), ("Whiting", 9.50, False), ("EP Kaolin", 5.00, False), ("Bentonite", 3.00, True), ("Rutile", 2.00, True)]
        },
        {
            "studio_number": "104", "name": "Verde Cobre", "glazy_id": "661922",
            "batch_date": "2/3/26", "cone": "Cone 6–10", "atmosphere": "Oxidation, Neutral", "surface": "Glossy", "transparency": "Semi-opaque", "status": "testing",
            "notes": "From William Chau, Australia. Currently being tested at cone 10 (March 2026).",
            "ingredients": [("G-200 Feldspar", 39.00, False), ("Silica", 34.00, False), ("Dolomite", 20.00, False), ("Gerstley Borate", 13.00, False), ("Zinc Oxide", 7.00, False), ("Black Copper Oxide", 5.00, True), ("Bentonite", 2.00, True)]
        },
        {
            "studio_number": "105", "name": "Triini Bog Green", "glazy_id": "737030",
            "batch_date": "2/3/26", "cone": "Cone 6–8", "atmosphere": "Oxidation", "surface": "Semi-matte", "transparency": "Opaque", "status": "testing",
            "notes": "Bristol glaze. Fired to 1230C. From Triin Lehismets, Estonia.",
            "ingredients": [("Minspar 200", 61.57, False), ("Whiting", 14.21, False), ("Zinc Oxide", 10.66, False), ("Grolleg Kaolin", 5.92, False), ("Rutile", 4.74, True), ("Copper Carbonate", 2.91, True)]
        },
        {
            "studio_number": "106", "name": "Satin Liner V.3", "glazy_id": "756883",
            "batch_date": "2/3/26", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation", "surface": "Semi-glossy", "transparency": "Semi-opaque", "status": "draft",
            "ingredients": [("Mahavir Feldspar", 26.90, False), ("Tile #6 Kaolin", 26.47, False), ("Dolomite", 16.22, False), ("Silica", 15.21, False), ("Wollastonite", 10.14, False), ("Zircopax", 5.07, True)]
        },
        # ── BATCH 2/20/26 ───────────────────────────────────────────────────
        {
            "studio_number": "107", "name": "Opaque Liner — Decreased Dolomite, Increased Silica", "glazy_id": "761728",
            "batch_date": "2/20/26", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation", "surface": "Semi-glossy", "transparency": "Semi-opaque", "status": "draft",
            "notes": "Active glaze in development. Phase separation on slow cool (MgO-driven). Cutlery marking improving. Crawling is Zircopax-driven — clear base fires clean. Never crazed on Takamori.",
            "lineage_notes": "Ed.1 #645006 GB clear. Ed.2 #782375 added Zircopax. Ed.3 #734041 GB to Frit 3134. Ed.4 #107 dolomite reduced, silica increased. Has active Rutile+Zircopax, Wood Ash, and Neodymium progression tests (Test B, 17 tiles). Pull up detailed notes for full lineage and test designs.",
            "umf_expansion": 6.1, "umf_r2o_ro": "0.17:0.83", "umf_sio2_al2o3": 6.14,
            "umf_na2o": 0.12, "umf_k2o": 0.05, "umf_cao": 0.51, "umf_mgo": 0.32,
            "umf_al2o3": 0.52, "umf_sio2": 3.2, "umf_b2o3": 0.19, "umf_zro2": 0.2,
            "ingredients": [("Tile #6 Kaolin", 31.05, False), ("Silica", 19.34, False), ("Ferro Frit 3134", 15.09, False), ("Dolomite", 15.00, False), ("Mahavir Feldspar", 11.06, False), ("Zircopax", 9.82, True), ("Rutile", 1.00, True)]
        },
        {
            "studio_number": "108", "name": "Opaque Liner — Dolomite/Whiting Swap Series", "glazy_id": None,
            "batch_date": "2/20/26", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation", "surface": "Semi-glossy", "status": "draft",
            "notes": "4-batch series (108A–D) testing dolomite/whiting swap to reduce MgO-driven phase separation. Each batch also has a 7-tile Rutile+Zircopax wet progression.",
            "lineage_notes": "Adaptation of #107 base. Part of Test A. Pull up detailed notes for batch weights and progression tables.",
            "ingredients": [("Tile #6 Kaolin", 15.21, False), ("Silica", 9.48, False), ("Ferro Frit 3134", 7.40, False), ("Dolomite (varies 108A–D)", 7.35, False), ("Mahavir Feldspar", 5.42, False), ("Whiting (varies 108A–D)", 0.00, False)]
        },
        {
            "studio_number": "109", "name": "Opaque Liner Clear Base (#107 without opacifiers)", "glazy_id": "783128",
            "batch_date": "3/27/26", "cone": "Cone 9–10", "atmosphere": "Reduction, Neutral, Oxidation", "surface": "Semi-glossy", "transparency": "Semi-opaque", "status": "draft",
            "notes": "#107 with Zircopax and Rutile removed, normalized to 100g. Used as base for Test B 17-tile progression.",
            "lineage_notes": "#107 with opacifiers removed. Has 17-tile progression test (Test B): Phase 1 Rutile+Zircopax (tiles 1-7), Phase 2 Wood Ash +2.5g (tiles 8-12), Phase 3 Neodymium +1.5g (tiles 13-17). Pull up detailed notes for full progression tables.",
            "umf_expansion": 6.4, "umf_r2o_ro": "0.17:0.83",
            "ingredients": [("Tile #6 Kaolin", 33.92, False), ("Silica", 21.13, False), ("Ferro Frit 3134", 16.48, False), ("Dolomite", 16.39, False), ("Mahavir Feldspar", 12.08, False)]
        },
        # ── BATCH 2/18/26 — ASH GLAZE FRIT SERIES ───────────────────────────
        {
            "studio_number": "110", "name": "Ash Glaze — 10% G200 to Frit 3134", "glazy_id": "783139",
            "batch_date": "2/18/26", "cone": "Cone unknown", "atmosphere": "Reduction", "status": "testing",
            "notes": "Part of frit substitution series on #94 base. Expansion 9.7.",
            "lineage_notes": "Adaptation of #94 ash base. Part of Test C frit substitution series (#110–#113). UMF confirms Frit 3134 substitution alone cannot fix crazing — expansion stays flat despite R2O:RO improving.",
            "umf_expansion": 9.7,
            "ingredients": [("Wood Ash (spruce/birch, unwashed)", 34.48, False), ("G-200 Feldspar", 31.03, False), ("Ball Clay", 24.14, False), ("Silica", 6.90, False), ("Ferro Frit 3134", 3.45, False)]
        },
        {
            "studio_number": "111", "name": "Ash Glaze — 25% G200 to Frit 3134", "glazy_id": "783140",
            "batch_date": "2/18/26", "cone": "Cone unknown", "atmosphere": "Reduction", "status": "testing",
            "notes": "Part of frit substitution series on #94 base. Expansion 9.8.",
            "lineage_notes": "Adaptation of #94 ash base. Part of Test C (#110–#113).",
            "umf_expansion": 9.8,
            "ingredients": [("Wood Ash (spruce/birch, unwashed)", 34.48, False), ("G-200 Feldspar", 25.86, False), ("Ball Clay", 24.14, False), ("Silica", 6.90, False), ("Ferro Frit 3134", 8.62, False)]
        },
        {
            "studio_number": "112", "name": "Ash Glaze — 50% G200 to Frit 3134", "glazy_id": "783143",
            "batch_date": "2/18/26", "cone": "Cone unknown", "atmosphere": "Reduction", "status": "testing",
            "notes": "Part of frit substitution series on #94 base. Expansion 9.8. Key reference — equal parts ash/feldspar/frit.",
            "lineage_notes": "Adaptation of #94 ash base. Part of Test C (#110–#113).",
            "umf_expansion": 9.8,
            "ingredients": [("Wood Ash (spruce/birch, unwashed)", 34.48, False), ("G-200 Feldspar", 17.24, False), ("Ball Clay", 24.14, False), ("Silica", 6.90, False), ("Ferro Frit 3134", 17.24, False)]
        },
        {
            "studio_number": "113", "name": "Ash Glaze — 75% G200 to Frit 3134", "glazy_id": "783147",
            "batch_date": "2/18/26", "cone": "Cone unknown", "atmosphere": "Reduction", "status": "testing",
            "notes": "Expansion 9.9. Not suitable as standalone liner — Al2O3 0.19, SiO2 1.65. Intended as drippy accent over #107.",
            "lineage_notes": "Adaptation of #94 ash base. Part of Test C (#110–#113). Repurposed as accent glaze over #107 rather than standalone liner.",
            "umf_expansion": 9.9,
            "ingredients": [("Wood Ash (spruce/birch, unwashed)", 34.48, False), ("G-200 Feldspar", 8.62, False), ("Ball Clay", 24.14, False), ("Silica", 6.90, False), ("Ferro Frit 3134", 25.86, False)]
        },
        {
            "studio_number": "114", "name": "Blue Salt (Carbondale Clay Center)", "glazy_id": "265775",
            "batch_date": "2/18/26", "cone": "Cone 10", "atmosphere": "Reduction", "status": "testing",
            "notes": "From Ceramics Monthly October 2022.",
            "ingredients": [("Nepheline Syenite", 71.60, False), ("Dolomite", 23.60, False), ("Ball Clay", 4.80, False), ("Zircopax", 18.80, True), ("Bentonite", 4.00, True), ("Cobalt Carbonate", 1.10, True)]
        },
        {
            "studio_number": "115", "name": "Sheryl's Blue Sparkle Town", "glazy_id": "25570",
            "batch_date": "2/18/26", "cone": "Cone 9–11", "atmosphere": "Reduction", "surface": "Glossy", "transparency": "Transparent", "status": "production",
            "notes": "Blue to green to gray transparent gloss with white to green crystals. Sheryl Harty, Fall 2018.",
            "ingredients": [("Silica", 36.00, False), ("Nepheline Syenite A270", 28.00, False), ("Dolomite", 12.00, False), ("EP Kaolin", 10.00, False), ("Whiting", 7.00, False), ("Strontium Carbonate", 4.00, False), ("Bentonite", 2.00, True), ("Lithium Carbonate", 1.00, False), ("Copper Carbonate", 3.00, True), ("Cobalt Carbonate", 0.25, True)]
        },
    ]

    materials_data = [
        {"name": "Ferro Frit 3134", "price_per_lb": 3.56, "invoice_date": "March 2026"},
        {"name": "Silica", "price_per_lb": 1.24, "invoice_date": "March 2026"},
        {"name": "Dolomite", "price_per_lb": 0.78, "invoice_date": "March 2026"},
        {"name": "Zircopax", "price_per_lb": 5.64, "invoice_date": "March 2026"},
        {"name": "Whiting", "price_per_lb": 0.40, "invoice_date": "March 2026"},
        {"name": "Strontium Carbonate", "price_per_lb": 3.68, "invoice_date": "March 2026"},
        {"name": "Titanium Dioxide", "price_per_lb": 7.30, "invoice_date": "March 2026"},
        {"name": "Takamori Clay", "price_per_lb": 0.836, "invoice_date": "March 2026"},
        {"name": "Tile #6 Kaolin", "notes": "No price on file — add when next order placed"},
        {"name": "Mahavir Feldspar", "notes": "Potash feldspar, Laguna Clay import. No price on file."},
        {"name": "Rutile", "notes": "No price on file — add when next order placed"},
        {"name": "G-200 Feldspar", "notes": "No price on file — add when next order placed"},
        {"name": "Ball Clay (Kentucky OM #4)", "notes": "No price on file — add when next order placed"},
        {"name": "Neodymium Oxide", "notes": "Confirm stock on hand before testing"},
        {"name": "Ferro Frit 3110", "notes": "Needed for Driftwood Dreams. Not on current invoice — confirm stock."},
        {"name": "Lithium Carbonate", "notes": "Confirm it is carbonate specifically, not lithosil"},
        {"name": "Wood Ash (spruce/birch, unwashed)", "notes": "Studio material. Sift to 60-80 mesh before use. High alkali, variable batch to batch."},
    ]

    for m_data in materials_data:
        m = Material(name=m_data["name"], price_per_lb=m_data.get("price_per_lb"), notes=m_data.get("notes",""), invoice_date=m_data.get("invoice_date",""))
        db.session.add(m)

    for g_data in glazes:
        ingredients = g_data.pop("ingredients")
        g = Glaze(**{k: v for k, v in g_data.items() if k != "ingredients"})
        db.session.add(g)
        db.session.flush()
        for i, (mat, amt, is_add) in enumerate(ingredients):
            ing = Ingredient(glaze_id=g.id, material=mat, amount=amt, is_additive=is_add, sort_order=i)
            db.session.add(ing)

    db.session.commit()
    print(f"Seeded {len(glazes)} glazes and {len(materials_data)} materials.")
