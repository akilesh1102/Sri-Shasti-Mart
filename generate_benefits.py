import re

html_file = "index.html"
with open(html_file, "r") as f:
    content = f.read()

# 1. Fix Logo
logo_old = """      <a href="#" class="logo" style="display: flex; flex-direction: column; align-items: flex-start; line-height: 1.2;">
        <span>Sri Shasti Mart</span>
        <span style="font-size: 0.8rem; font-weight: normal;">ஸ்ரீ சஷ்டி மார்ட்</span>
      </a>"""
logo_new = """      <a href="#" class="logo" style="display: flex; align-items: baseline; gap: 8px;">
        <span>Sri Shasti Mart</span>
        <span style="font-size: 1rem; font-weight: normal;">(ஸ்ரீ சஷ்டி மார்ட்)</span>
      </a>"""
content = content.replace(logo_old, logo_new)

# 2. Define benefits for each product
# Format: "Title": ("Short Benefit", ["Hover 1", "Hover 2", "Hover 3", "Hover 4"])
benefits_map = {
    "ABC Malt": (
        "Rejuvenates skin and boosts hemoglobin.",
        ["Packed with Vitamin A, B & C", "Purifies blood naturally", "Promotes healthy glowing skin", "Improves overall stamina"]
    ),
    "Beetroot Malt": (
        "Natural energy booster and blood purifier.",
        ["Rich in Iron and Folic Acid", "Prevents anemia naturally", "Improves blood circulation", "Healthy drink for kids & pregnant women"]
    ),
    "Carrot Malt": (
        "Improves vision and immunity.",
        ["High in Vitamin A for eye health", "Boosts immune system", "Promotes healthy digestion", "Delicious alternative to synthetic drinks"]
    ),
    "Ragi Malt": (
        "Powerhouse of calcium for strong bones.",
        ["Rich in Calcium and Vitamin D", "Excellent for bone development", "Keeps you full & aids weight loss", "Perfect cooling drink for summer"]
    ),
    "Papaya Malt": (
        "Enhances digestion and skin health.",
        ["Rich source of antioxidants", "Aids in healthy digestion", "Improves skin texture", "Natural detoxifier"]
    ),
    "Red Banana Malt": (
        "Rich in potassium for heart health.",
        ["Regulates blood pressure", "High in Vitamin B6", "Provides instant energy", "Improves male & female fertility"]
    ),
    "Black Gram Porridge Mix": (
        "Strengthens muscles and joints.",
        ["Excellent protein source", "Strengthens bones and joints", "Relieves back pain", "Nourishing for growing children"]
    ),
    "Women's Rice Mix": (
        "Traditional nourishment for women's wellness.",
        ["Balances hormones naturally", "Rich in iron and zinc", "Supports maternal health", "Provides sustained energy"]
    ),
    "Black Rice Mix": (
        "Rich in antioxidants and detoxifying.",
        ["Highest antioxidant properties", "Aids in liver detoxification", "Good for diabetic management", "Promotes heart health"]
    ),
    "Kuruvai Rice Mix": (
        "Revitalizes the body and boosts immunity.",
        ["Traditional immunity booster", "Improves stamina", "Rich in essential minerals", "Supports healthy digestion"]
    ),
    "Spicy Garlic Pickle": (
        "Aids digestion and lowers cholesterol.",
        ["Helps lower bad cholesterol", "Improves cardiovascular health", "Natural antibacterial properties", "Enhances taste of any meal"]
    ),
    "Spicy Onion Pickle": (
        "Cooling effect with antioxidant boost.",
        ["Rich in antioxidants", "Improves immunity", "Aids in digestion", "Traditional homemade taste"]
    ),
    "Tangy Ginger Pickle": (
        "Relieves nausea and improves digestion.",
        ["Soothes digestive system", "Relieves cold and cough symptoms", "Natural anti-inflammatory", "Authentic tangy flavor"]
    ),
    "Cissus Pickle": (
        "Strengthens bones and joints naturally.",
        ["Known as Bone-setter (Pirandai)", "Rich in calcium", "Relieves joint pain", "Improves bone density"]
    ),
    "Gongura Pickle": (
        "Rich in iron and tangy goodness.",
        ["Excellent source of Iron", "High in Vitamin C", "Boosts immune system", "Authentic traditional recipe"]
    ),
    "Gooseberry Pickle": (
        "Vitamin C powerhouse for immunity.",
        ["Highest source of Vitamin C", "Promotes hair and skin health", "Boosts immunity", "Aids in digestion"]
    ),
    "Drumstick Leaves Powder": (
        "Moringa superfood for overall vitality.",
        ["Packed with 90+ nutrients", "Increases energy levels", "Improves hemoglobin", "Good for diabetic management"]
    ),
    "Amla Curry Leaves Powder": (
        "Promotes hair growth and clear vision.",
        ["Reduces hair fall and greying", "Improves eyesight", "Rich in iron and vitamins", "Enhances memory"]
    ),
    "Balloon Vine Leaves Powder": (
        "Natural remedy for joint pain.",
        ["Relieves arthritis and joint pain", "Natural anti-inflammatory", "Improves mobility", "Traditional medicinal herb"]
    ),
    "Cissus Powder": (
        "Strengthens bones and improves digestion.",
        ["Excellent for bone health", "Relieves gastric issues", "Improves appetite", "Rich in natural calcium"]
    ),
    "Garlic Powder": (
        "Heart-friendly and flavor-packed.",
        ["Regulates blood pressure", "Lowers cholesterol levels", "Boosts immune system", "Perfect for daily cooking"]
    ),
    "Sambar Powder": (
        "Authentic aroma and flavor for daily meals.",
        ["Made with traditional spices", "Aids in digestion", "Rich in antioxidants", "No artificial colors or flavors"]
    ),
    "Raw Nendran Banana Powder": (
        "Nutritious first food for babies and adults.",
        ["Excellent for healthy weight gain", "Easily digestible", "Rich in potassium", "Great alternative to processed cereals"]
    ),
    "Pure Kerala Honey": (
        "100% natural immunity booster.",
        ["Soothes throat and cough", "Rich in antioxidants", "Natural energy source", "Perfect healthy sweetener"]
    ),
    "Mudavatukkal Soup": (
        "Revitalizing soup for joint strength.",
        ["Excellent for joint and knee pain", "Rich in calcium and minerals", "Warms the body", "Traditional herbal remedy"]
    ),
    "Kollu Soup Mix": (
        "Aids in weight loss and reduces cholesterol.",
        ["Burns excess fat", "High in protein and fiber", "Relieves cold and congestion", "Keeps you active"]
    ),
    "Mango Thokku": (
        "Tangy delight that boosts appetite.",
        ["Stimulates digestion", "Rich in Vitamin C", "Authentic traditional taste", "Perfect side dish for meals"]
    ),
    "Kulambu Chilli Powder": (
        "All-in-one spice mix for authentic curries.",
        ["Perfect blend of traditional spices", "Saves cooking time", "No artificial preservatives", "Enhances flavor naturally"]
    )
}

# Add Pirandai Podi again because it's listed twice (line 339 and line 431)
# Wait, the second one might just be named Pirandai Podi
benefits_map["Pirandai Podi"] = benefits_map["Cissus Powder"]

# We will iterate over the HTML, find product cards, and inject the benefit and overlay
new_cards = []
import bs4
from bs4 import BeautifulSoup

soup = BeautifulSoup(content, 'html.parser')

product_cards = soup.find_all('div', class_='product-card')
for card in product_cards:
    title_elem = card.find('h3', class_='product-title')
    if not title_elem:
        continue
    
    title = title_elem.text.strip()
    
    # Do we have benefits for this?
    if title in benefits_map:
        short_benefit, hovers = benefits_map[title]
    else:
        # fallback
        short_benefit = "Delicious and healthy."
        hovers = ["100% Natural", "No Preservatives", "Healthy Choice"]
    
    # Check if benefit already added
    if card.find('p', class_='product-benefit'):
        continue
    
    # 1. Insert short benefit under product-desc
    desc_elem = card.find('p', class_='product-desc')
    if desc_elem:
        benefit_tag = soup.new_tag('p')
        benefit_tag['class'] = 'product-benefit'
        benefit_tag.string = short_benefit
        desc_elem.insert_after(benefit_tag)
    
    # 2. Insert hover overlay at the end of the card
    overlay_tag = soup.new_tag('div')
    overlay_tag['class'] = 'product-hover-overlay'
    
    h4_tag = soup.new_tag('h4')
    h4_tag.string = "Key Benefits:"
    overlay_tag.append(h4_tag)
    
    ul_tag = soup.new_tag('ul')
    for h in hovers:
        li_tag = soup.new_tag('li')
        li_tag.string = h
        ul_tag.append(li_tag)
        
    overlay_tag.append(ul_tag)
    card.append(overlay_tag)

with open("index.html", "w") as f:
    f.write(str(soup))
