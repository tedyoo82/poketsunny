#!/usr/bin/env python3
"""
Fetch Pokémon GO data from the public API and save as pokemon.json.
Organized by generation (region): Kanto, Johto, Hoenn, Sinnoh, Unova, Alola, Kalos, Galar, Paldea.
"""

import json
import sys
import urllib.request
import ssl

# Pokémon GO API endpoint for each generation
GENERATIONS = {
    1: "kanto",
    2: "johto",
    3: "hoenn",
    4: "sinnoh",
    5: "unova",
    6: "alola",
    7: "kalos",
    8: "galar",
    9: "paldea",
}

# Korean region names
REGION_KOREAN = {
    1: "관동",
    2: "도쿠소",
    3: "호연",
    4: "신오",
    5: "율려",
    6: "알로라",
    7: "가리아",
    8: "지후",
    9: "파르다",
}

# Korean type names
TYPE_KOREAN = {
    "POKEMON_TYPE_FIGHTING": "격투",
    "POKEMON_TYPE_FLYING": "비행",
    "POKEMON_TYPE_POISON": "독",
    "POKEMON_TYPE_GROUND": "땅",
    "POKEMON_TYPE_ROCK": "바위",
    "POKEMON_TYPE_BUG": "벌레",
    "POKEMON_TYPE_GHOST": "고스트",
    "POKEMON_TYPE_ICE": "얼음",
    "POKEMON_TYPE_DRAGON": "드래곤",
    "POKEMON_TYPE_STEEL": "강철",
    "POKEMON_TYPE_FIRE": "불꽃",
    "POKEMON_TYPE_WATER": "물",
    "POKEMON_TYPE_GRASS": "풀",
    "POKEMON_TYPE_ELECTRIC": "전기",
    "POKEMON_TYPE_psychic": "에스퍼",
    "POKEMON_TYPE_PSYCHIC": "에스퍼",
    "POKEMON_TYPE_NORMAL": "노말",
    "POKEMON_TYPE_FAIRY": "페어리",
}

# Type emoji mapping
TYPE_EMOJI = {
    "격투": "🥊",
    "비행": "🕊️",
    "독": "☠️",
    "땅": "🏔️",
    "바위": "🪨",
    "벌레": "🐛",
    "고스트": "👻",
    "얼음": "❄️",
    "드래곤": "🐉",
    "강철": "⚙️",
    "불꽃": "🔥",
    "물": "💧",
    "풀": "🌿",
    "전기": "⚡",
    "에스퍼": "🔮",
    "노말": "⚪",
    "페어리": "🧚",
}

# Type color mapping for UI
TYPE_COLORS = {
    "격투": "#FF8000",
    "비행": "#A890FF",
    "독": "#A838F8",
    "땅": "#E8CB68",
    "바위": "#B8A038",
    "벌레": "#A8B820",
    "고스트": "#705898",
    "얼음": "#98D8D8",
    "드래곤": "#7038F8",
    "강철": "#B8B8D0",
    "불꽃": "#F08030",
    "물": "#6890F0",
    "풀": "#78C850",
    "전기": "#F8D030",
    "에스퍼": "#F85888",
    "노말": "#A8A878",
    "페어리": "#EE99AC",
}


def fetch_generation(gen_num):
    """Fetch Pokémon data for a specific generation from the API."""
    url = f"https://pokemon-go-api.github.io/pokemon-go-api/api/pokedex/generation/{gen_num}.json"
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(url, timeout=30, context=ctx) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"  ✗ Generation {gen_num} failed: {e}", file=sys.stderr)
        return []


def get_korean_name(pokemon):
    """Get Korean name from Pokémon data."""
    names = pokemon.get("names", {})
    return names.get("Korean", names.get("English", pokemon.get("id", "Unknown")))


def get_korean_type(type_info):
    """Get Korean type name."""
    if not type_info:
        return None
    type_key = type_info.get("type", "")
    return TYPE_KOREAN.get(type_key, type_key.replace("POKEMON_TYPE_", ""))


def normalize_type_name(type_name):
    """Normalize type name for display."""
    if not type_name:
        return None
    # Clean up type name
    cleaned = type_name.strip()
    if cleaned in TYPE_KOREAN.values():
        return cleaned
    # Try to match
    for key, val in TYPE_KOREAN.items():
        if cleaned.lower() in val.lower() or val.lower() in cleaned.lower():
            return val
    return cleaned


def fetch_pokemon():
    """Fetch all Pokémon data organized by generation."""
    all_pokemon = []
    
    for gen_num, region_name in GENERATIONS.items():
        print(f"Fetching Generation {gen_num} ({REGION_KOREAN[gen_num]})...")
        data = fetch_generation(gen_num)
        
        for p in data:
            primary_type = get_korean_type(p.get("primaryType"))
            secondary_type = get_korean_type(p.get("secondaryType"))
            
            # Build Korean type string
            types_ko = []
            if primary_type:
                types_ko.append(primary_type)
            if secondary_type:
                types_ko.append(secondary_type)
            
            # Build English type string
            types_en = []
            pt = p.get("primaryType", {})
            if pt:
                types_en.append(pt.get("names", {}).get("English", ""))
            st = p.get("secondaryType", {})
            if st:
                types_en.append(st.get("names", {}).get("English", ""))
            
            # Extract moves (handle both dict and list formats)
            qm = p.get("quickMoves")
            quick_moves = list(qm.keys()) if isinstance(qm, dict) else list(qm) if isinstance(qm, list) else []
            cm = p.get("cinematicMoves")
            cinematic_moves = list(cm.keys()) if isinstance(cm, dict) else list(cm) if isinstance(cm, list) else []
            elite_quick = p.get("eliteQuickMoves", [])
            elite_cinematic = p.get("eliteCinematicMoves", [])
            
            # Extract evolution info
            evolutions = []
            for evo in p.get("evolutions", []):
                evolutions.append({
                    "id": evo.get("id", ""),
                    "candies": evo.get("candies", 0),
                })
            
            # Pokemon class
            pokemon_class = p.get("pokemonClass", "")
            class_ko = ""
            if pokemon_class == "POKEMON_CLASS_LEGENDARY":
                class_ko = "전설"
            elif pokemon_class == "POKEMON_CLASS_MYTHIC":
                class_ko = "신비"
            elif pokemon_class == "POKEMON_CLASS_ULTRA_BEAST":
                class_ko = "울트라비스트"
            
            # Build image URL
            assets = p.get("assets") or {}
            image_url = assets.get("image", "")
            shiny_url = assets.get("shinyImage", "")
            
            # Build YouTube search URL
            korean_name = get_korean_name(p)
            youtube_url = f"https://www.youtube.com/@Poke_Sunny/search?query={korean_name}"
            
            entry = {
                "id": p.get("id", ""),
                "dexNr": p.get("dexNr", 0),
                "name": korean_name,
                "nameEn": p.get("names", {}).get("English", ""),
                "nameJa": p.get("names", {}).get("Japanese", ""),
                "types": types_ko,
                "typesEn": types_en,
                "stats": p.get("stats", {}),
                "image": image_url,
                "shinyImage": shiny_url,
                "pokemonClass": class_ko,
                "hasMega": p.get("hasMegaEvolution", False),
                "hasGigantamax": p.get("hasGigantamaxEvolution", False),
                "evolutions": evolutions,
                "quickMoves": quick_moves,
                "cinematicMoves": cinematic_moves,
                "eliteQuickMoves": elite_quick,
                "eliteCinematicMoves": elite_cinematic,
                "generation": gen_num,
                "region": region_name,
                "regionKorean": REGION_KOREAN[gen_num],
                "youtubeUrl": youtube_url,
            }
            all_pokemon.append(entry)
        
        print(f"  ✓ Got {len(data)} Pokémon")
    
    # Sort by dex number
    all_pokemon.sort(key=lambda x: x["dexNr"])
    
    return all_pokemon


def main():
    print("=" * 50)
    print("Pokémon GO Data Fetcher")
    print("=" * 50)
    
    all_pokemon = fetch_pokemon()
    
    # Organize by region
    by_region = {}
    for p in all_pokemon:
        region = p["region"]
        if region not in by_region:
            by_region[region] = {
                "region": region,
                "regionKorean": p["regionKorean"],
                "generation": p["generation"],
                "count": 0,
                "pokemon": [],
            }
        by_region[region]["pokemon"].append(p)
        by_region[region]["count"] += 1
    
    # Build output structure
    output = {
        "updatedAt": "2026-11-22T00:00:00Z",
        "total": len(all_pokemon),
        "regions": [],
        "all": all_pokemon,
    }
    
    for gen_num in sorted(by_region.keys()):
        r = by_region[gen_num]
        output["regions"].append({
            "generation": r["generation"],
            "region": r["region"],
            "regionKorean": r["regionKorean"],
            "count": r["count"],
        })
    
    # Save to file
    output_file = "pokemon.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Saved {len(all_pokemon)} Pokémon to {output_file}")
    print(f"   Regions: {len(output['regions'])}")
    for r in output["regions"]:
        print(f"   Gen {r['generation']} {r['regionKorean']}({r['region']}): {r['count']}")


if __name__ == "__main__":
    main()
