from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    id: str
    stage: int
    conditions: tuple      
    then: str = ""         
    advice: str = ""       



_RAW = [
    (1, ["rain_heavy", "long_rain"], "severe_rainfall", ""),
    (1, ["rain_extreme"], "severe_rainfall", ""),
    (1, ["rain_moderate", "long_rain"], "sustained_rainfall", ""),
    (1, ["area_nullah", "rain_heavy"], "nullah_overflow_possible", ""),
    (1, ["area_nullah", "rain_extreme"], "nullah_overflow_likely", ""),
    (1, ["area_coastal", "tide_high", "rain_heavy"], "sea_drainage_blocked", ""),
    (1, ["area_coastal", "tide_high", "rain_extreme"], "sea_drainage_blocked", ""),
    (1, ["area_lowlying", "rain_heavy"], "waterlogging_likely", ""),
    (1, ["area_lowlying", "rain_extreme"], "waterlogging_likely", ""),
    (1, ["drain_blocked", "rain_moderate"], "waterlogging_likely", ""),
    (1, ["drain_blocked", "rain_heavy"], "waterlogging_likely", ""),
    (1, ["drain_overflow"], "waterlogging_likely", ""),
    (1, ["drain_partial", "rain_heavy"], "waterlogging_likely", ""),
    (1, ["flood_often", "rain_moderate"], "repeat_flood_pattern", ""),
    (1, ["flood_once", "rain_heavy"], "repeat_flood_pattern", ""),
    (1, ["severe_rainfall", "waterlogging_likely"], "high_flood_hazard", ""),
    (1, ["nullah_overflow_likely"], "high_flood_hazard", ""),
    (1, ["sea_drainage_blocked", "waterlogging_likely"], "high_flood_hazard", ""),
    (1, ["repeat_flood_pattern", "waterlogging_likely"], "high_flood_hazard", ""),
    (1, ["sustained_rainfall", "waterlogging_likely"], "medium_flood_hazard", ""),
    (1, ["nullah_overflow_possible"], "medium_flood_hazard", ""),
    (1, ["rain_heavy", "waterlogging_likely"], "medium_flood_hazard", ""),
    (1, ["rain_extreme"], "medium_flood_hazard", ""),

    (2, ["~high_flood_hazard", "~medium_flood_hazard"], "low_flood_hazard", ""),
    (2, ["floor_ground", "house_lower"], "water_entry_likely", ""),
    (2, ["floor_basement"], "water_entry_likely", ""),
    (2, ["floor_ground", "house_same"], "water_entry_possible", ""),
    (2, ["house_kacha", "floor_ground"], "water_entry_likely", ""),
    (2, ["floor_upper"], "water_entry_unlikely", ""),
    (2, ["house_higher"], "water_entry_unlikely", ""),
    (2, ["house_kacha"], "structure_vulnerable", ""),
    (2, ["exposed_wiring", "floor_ground"], "electric_shock_risk", ""),
    (2, ["exposed_wiring", "floor_basement"], "electric_shock_risk", ""),
    (2, ["vulnerable_people"], "high_care_need", ""),
    (2, ["vulnerable_people", "floor_ground"], "evacuation_priority", ""),
    (2, ["vulnerable_people", "floor_basement"], "evacuation_priority", ""),
    (2, ["has_vehicle_low"], "vehicle_at_risk", ""),
    (2, ["roof_leak", "rain_heavy"], "roof_seepage_risk", ""),
    (2, ["roof_leak", "rain_extreme"], "roof_seepage_risk", ""),
    (2, ["~has_backup_power"], "blackout_risk", ""),
    (2, ["~has_kit"], "unprepared", ""),
    (2, ["~has_water_storage"], "drinking_water_risk", ""),
    (2, ["has_kit", "has_backup_power", "has_water_storage"], "well_prepared", ""),
    (2, ["has_barriers"], "partial_protection", ""),

    (3, ["high_flood_hazard", "water_entry_likely"], "CRITICAL_RISK", ""),
    (3, ["high_flood_hazard", "water_entry_possible"], "HIGH_RISK", ""),
    (3, ["high_flood_hazard", "water_entry_unlikely"], "MODERATE_RISK", ""),
    (3, ["medium_flood_hazard", "water_entry_likely"], "HIGH_RISK", ""),
    (3, ["medium_flood_hazard", "water_entry_possible"], "MODERATE_RISK", ""),
    (3, ["medium_flood_hazard", "water_entry_unlikely"], "LOW_RISK", ""),
    (3, ["low_flood_hazard"], "LOW_RISK", ""),
    (3, ["structure_vulnerable", "high_flood_hazard"], "CRITICAL_RISK", ""),

    (4, ["high_care_need", "HIGH_RISK"], "CRITICAL_RISK", ""),
    (4, ["CRITICAL_RISK"], "",
     "Plan to leave BEFORE the rain peaks. Move to a relative's place on higher ground. Take ID, phone, power bank, medicines and documents in a waterproof bag."),
    (4, ["HIGH_RISK"], "",
     "Move valuables, documents and electronics to an upper shelf or floor now, and keep an evacuation bag ready."),
    (4, ["MODERATE_RISK"], "",
     "Keep watching the weather. Prepare basic supplies and know your exit route."),
    (4, ["LOW_RISK"], "",
     "Risk is low right now. Stay updated with PMD weather alerts and keep drains near your home clear."),
    (4, ["electric_shock_risk"], "",
     "If water enters, switch off the main power supply first. Never touch wires or switches with wet hands."),
    (4, ["vehicle_at_risk"], "",
     "Move your car or bike to higher ground before the rain. Never park in low spots or underpasses."),
    (4, ["blackout_risk"], "",
     "Charge phones and power banks and keep a torch ready. Power cuts are common in heavy rain."),
    (4, ["unprepared"], "",
     "Make an emergency kit: torch, first-aid, dry food, medicines, copies of documents, and some cash."),
    (4, ["drinking_water_risk"], "",
     "Store clean drinking water (at least 3 litres per person per day). Boil water after floods."),
    (4, ["evacuation_priority", "HIGH_RISK"], "",
     "Move children and elderly to an upper floor or safe place first. Keep their medicines ready."),
    (4, ["evacuation_priority", "CRITICAL_RISK"], "",
     "Move children and elderly out first, and early. Do not wait for water to enter the house."),
    (4, ["nullah_overflow_possible"], "",
     "Stay away from the nullah. Do not cross or walk near flowing water, even if it looks shallow."),
    (4, ["nullah_overflow_likely"], "",
     "Nullah overflow is likely. Keep away from its banks and be ready to leave quickly. Call Rescue 1122 if trapped."),
    (4, ["sea_drainage_blocked"], "",
     "High tide stops rainwater from draining into the sea, so water will stay longer. Avoid coastal roads."),
    (4, ["drain_blocked"], "",
     "Your drain is blocked. Clear garbage from it now and report it to the local municipal authority."),
    (4, ["drain_partial"], "",
     "Clear leaves and plastic from your drain before the rain starts."),
    (4, ["roof_seepage_risk"], "",
     "Fix roof leaks with sealant or cover with a tarpaulin to stop water damage and ceiling collapse."),
    (4, ["structure_vulnerable"], "",
     "Mud or weak walls can collapse in heavy rain. Move to a stronger building during the worst hours."),
    (4, ["repeat_flood_pattern"], "",
     "Your area has flooded before, so expect it again. Raise appliances and keep sandbags ready."),
    (4, ["water_entry_likely"], "",
     "Lift fridge, TV and other appliances off the floor. Put sockets and valuables up high."),
    (4, ["water_entry_likely", "~partial_protection"], "",
     "Get sandbags or a door barrier to slow water at the entrance."),
    (4, ["partial_protection"], "",
     "Good that you have flood barriers. Place them before the water level rises."),
    (4, ["severe_rainfall"], "",
     "Avoid non-essential travel. Never drive or walk through flooded roads or underpasses."),
    (4, ["waterlogging_likely"], "",
     "Expect standing water on nearby roads. Plan your trips around it."),
    (4, ["well_prepared"], "",
     "Great job: your kit, water and backup power are ready. Just stay alert."),
]

RULES = [Rule(f"R{i:02d}", st, tuple(c), t, a) for i, (st, c, t, a) in enumerate(_RAW, 1)]

RISK_ORDER = ["CRITICAL_RISK", "HIGH_RISK", "MODERATE_RISK", "LOW_RISK"]


def facts_from_inputs(i: dict) -> set:
    """Turn raw form answers into starting facts."""
    f = set()
    mm = i["rain_mm"]
    if mm < 30:
        f.add("rain_light")
    elif mm < 65:
        f.add("rain_moderate")
    elif mm < 115:
        f.add("rain_heavy")
    else:
        f.add("rain_extreme")
    if i["hours"] >= 6:
        f.add("long_rain")
    f.add({"Elevated / well-drained": "area_elevated", "Low-lying": "area_lowlying",
           "Near a nullah (drain/stream)": "area_nullah", "Coastal": "area_coastal"}[i["area"]])
    f.add({"Ground floor": "floor_ground", "Basement": "floor_basement",
           "First floor or above": "floor_upper"}[i["floor"]])
    f.add({"Higher than the road": "house_higher", "Same level as the road": "house_same",
           "Lower than the road": "house_lower"}[i["road_level"]])
    f.add({"Pukka (concrete)": "house_pukka", "Kacha (mud / weak)": "house_kacha"}[i["house_type"]])
    f.add({"Clean and working": "drain_clean", "Partly blocked": "drain_partial",
           "Fully blocked": "drain_blocked", "Overflows even in light rain": "drain_overflow"}[i["drain"]])
    f.add({"Never": "flood_never", "Once": "flood_once", "Often": "flood_often"}[i["past_flood"]])
    for key, fact in [("tide_high", "tide_high"), ("vulnerable", "vulnerable_people"),
                      ("vehicle", "has_vehicle_low"), ("wiring", "exposed_wiring"),
                      ("roof_leak", "roof_leak"), ("kit", "has_kit"), ("water", "has_water_storage"),
                      ("power", "has_backup_power"), ("barriers", "has_barriers")]:
        if i.get(key):
            f.add(fact)
    return f


def _holds(cond: str, facts: set) -> bool:
    return (cond[1:] not in facts) if cond.startswith("~") else (cond in facts)


def run_engine(start_facts: set):
    """Forward chaining. Returns (facts, fired_rules, advice_list, risk_level)."""
    facts, fired, done = set(start_facts), [], set()
    for stage in (1, 2, 3, 4):
        changed = True
        while changed:
            changed = False
            for r in RULES:
                if r.stage != stage or r.id in done:
                    continue
                if all(_holds(c, facts) for c in r.conditions):
                    done.add(r.id)
                    fired.append(r)
                    if r.then and r.then not in facts:
                        facts.add(r.then)
                        changed = True
    advice = [r.advice for r in fired if r.advice]
    risk = next((x for x in RISK_ORDER if x in facts), "LOW_RISK")
    return facts, fired, advice, risk
