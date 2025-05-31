#!/usr/bin/env python3
"""
James Bland: ACME Edition - Intel Deck Generator
Generates shuffled intel deck for gameplay
"""

import json
import os
import random
import sys
from pathlib import Path

# Default intel card definitions
DEFAULT_INTEL_DEFINITIONS = [
    {
        "id": "IDENTITY_REVEAL",
        "type": "identity",
        "uses": 1,
        "description": "Reveals the true identity of target player",
        "copies": 8
    },
    {
        "id": "NEXT_OFFENSE",
        "type": "tactical",
        "uses": 1,
        "description": "Learn target's next planned offense",
        "copies": 6
    },
    {
        "id": "NEXT_DEFENSE", 
        "type": "tactical",
        "uses": 1,
        "description": "Learn target's next planned defense",
        "copies": 6
    },
    {
        "id": "GADGET_INVENTORY",
        "type": "equipment",
        "uses": 1,
        "description": "Reveals all gadgets owned by target",
        "copies": 5
    },
    {
        "id": "LOCATION_INTEL",
        "type": "surveillance",
        "uses": 1,
        "description": "Discover target's current safe house location",
        "copies": 4
    },
    {
        "id": "ALLIANCE_NETWORK",
        "type": "political",
        "uses": 1,
        "description": "Reveals all of target's current alliances",
        "copies": 4
    },
    {
        "id": "MASTER_PLAN_HINT",
        "type": "strategic",
        "uses": 1,
        "description": "Gain a clue about target's master plan objective",
        "copies": 3
    },
    {
        "id": "FULL_DOSSIER",
        "type": "comprehensive",
        "uses": 3,
        "description": "Complete intelligence profile - reveals identity, gadgets, and next action",
        "copies": 2
    },
    {
        "id": "ASSET_CONTROL",
        "type": "strategic",
        "uses": 1,
        "description": "Learn which strategic assets target controls",
        "copies": 3
    },
    {
        "id": "IP_RESERVES",
        "type": "financial",
        "uses": 1,
        "description": "Discover target's exact IP count",
        "copies": 5
    },
    {
        "id": "COMMUNICATION_LOG",
        "type": "surveillance",
        "uses": 1,
        "description": "Intercept target's recent communications",
        "copies": 4
    },
    {
        "id": "WEAKNESS_ANALYSIS",
        "type": "tactical",
        "uses": 1,
        "description": "Reveals target's most vulnerable defense type",
        "copies": 3
    },
    {
        "id": "DOUBLE_AGENT",
        "type": "infiltration",
        "uses": 2,
        "description": "Place a double agent - learn target's actions for 2 rounds",
        "copies": 2
    },
    {
        "id": "BLACKMAIL_MATERIAL",
        "type": "leverage",
        "uses": 1,
        "description": "Compromising information that can force target cooperation",
        "copies": 2
    },
    {
        "id": "SAFE_HOUSE_NETWORK",
        "type": "infrastructure",
        "uses": 1,
        "description": "Map of all safe houses in target's network",
        "copies": 3
    }
]

def load_intel_definitions():
    """Load intel definitions from file or use defaults"""
    assets_data_path = Path(__file__).parent.parent / "assets" / "data" / "intel_definitions.json"
    
    if assets_data_path.exists():
        try:
            with open(assets_data_path, 'r') as f:
                definitions = json.load(f)
                print(f"Loaded intel definitions from {assets_data_path}")
                return definitions
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading intel definitions: {e}")
            print("Using default definitions instead")
    else:
        print(f"Intel definitions file not found at {assets_data_path}")
        print("Using default definitions")
    
    return DEFAULT_INTEL_DEFINITIONS

def build_intel_deck(definitions):
    """Build shuffled intel deck from definitions"""
    deck = []
    
    for definition in definitions:
        copies = definition.get('copies', 1)
        for _ in range(copies):
            card = {
                'id': definition['id'],
                'type': definition['type'],
                'usesLeft': definition['uses'],
                'description': definition['description']
            }
            deck.append(card)
    
    # Shuffle the deck
    random.shuffle(deck)
    
    print(f"Built intel deck with {len(deck)} cards")
    print(f"Card types: {set(card['type'] for card in deck)}")
    
    return deck

def ensure_static_data_dir():
    """Ensure static/data directory exists"""
    static_data_path = Path(__file__).parent.parent / "static" / "data"
    static_data_path.mkdir(parents=True, exist_ok=True)
    return static_data_path

def save_intel_deck(deck, output_dir):
    """Save intel deck to JSON file"""
    output_file = output_dir / "intel_deck.json"
    
    with open(output_file, 'w') as f:
        json.dump(deck, f, indent=2)
    
    print(f"Intel deck saved to {output_file}")
    return output_file

def generate_intel_deck_pdf(deck, output_dir):
    """Generate PDF version of intel deck (optional)"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        
        pdf_file = output_dir / "intel_deck.pdf"
        doc = SimpleDocTemplate(str(pdf_file), pagesize=letter)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        card_id_style = ParagraphStyle(
            'CardID',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=10
        )
        
        story = []
        
        # Title page
        story.append(Paragraph("James Bland: ACME Edition", title_style))
        story.append(Paragraph("Intel Deck Reference", title_style))
        story.append(Spacer(1, 0.5*inch))
        
        # Group cards by type for better organization
        cards_by_type = {}
        for card in deck:
            card_type = card['type']
            if card_type not in cards_by_type:
                cards_by_type[card_type] = []
            cards_by_type[card_type].append(card)
        
        # Add cards organized by type
        for card_type, cards in sorted(cards_by_type.items()):
            story.append(Paragraph(f"{card_type.title()} Intel", styles['Heading2']))
            story.append(Spacer(1, 0.2*inch))
            
            # Group identical cards
            unique_cards = {}
            for card in cards:
                card_id = card['id']
                if card_id not in unique_cards:
                    unique_cards[card_id] = {'card': card, 'count': 0}
                unique_cards[card_id]['count'] += 1
            
            for card_id, data in sorted(unique_cards.items()):
                card = data['card']
                count = data['count']
                
                story.append(Paragraph(f"{card['id']} (×{count})", card_id_style))
                story.append(Paragraph(f"Uses: {card['usesLeft']}", styles['Normal']))
                story.append(Paragraph(card['description'], styles['Normal']))
                story.append(Spacer(1, 0.3*inch))
        
        doc.build(story)
        print(f"Intel deck PDF generated: {pdf_file}")
        return pdf_file
        
    except ImportError:
        print("ReportLab not available - skipping PDF generation")
        print("Install with: pip install reportlab")
        return None
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

def print_deck_statistics(deck):
    """Print statistics about the generated deck"""
    print("\n=== Intel Deck Statistics ===")
    print(f"Total cards: {len(deck)}")
    
    # Count by type
    type_counts = {}
    for card in deck:
        card_type = card['type']
        type_counts[card_type] = type_counts.get(card_type, 0) + 1
    
    print("\nCards by type:")
    for card_type, count in sorted(type_counts.items()):
        print(f"  {card_type}: {count}")
    
    # Count by uses
    uses_counts = {}
    for card in deck:
        uses = card['usesLeft']
        uses_counts[uses] = uses_counts.get(uses, 0) + 1
    
    print("\nCards by uses:")
    for uses, count in sorted(uses_counts.items()):
        print(f"  {uses} use(s): {count}")
    
    # Unique card types
    unique_cards = set(card['id'] for card in deck)
    print(f"\nUnique card types: {len(unique_cards)}")

def main():
    """Main function to generate intel deck"""
    print("James Bland: ACME Edition - Intel Deck Generator")
    print("=" * 50)
    
    # Load intel definitions
    definitions = load_intel_definitions()
    
    # Build the deck
    deck = build_intel_deck(definitions)
    
    # Ensure output directory exists
    output_dir = ensure_static_data_dir()
    
    # Save JSON deck
    json_file = save_intel_deck(deck, output_dir)
    
    # Generate PDF (optional)
    pdf_file = generate_intel_deck_pdf(deck, output_dir)
    
    # Print statistics
    print_deck_statistics(deck)
    
    print("\n=== Generation Complete ===")
    print(f"JSON deck: {json_file}")
    if pdf_file:
        print(f"PDF reference: {pdf_file}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nGeneration cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1) 