import bs4
from bs4 import BeautifulSoup
import re

html_file = "index.html"
with open(html_file, "r", encoding="utf-8") as f:
    content = f.read()

tamil_dict = {
    # ABC Malt
    "Rejuvenates skin and boosts hemoglobin.": "சருமத்தை பொலிவாக்கி, இரத்த அணுக்களை அதிகரிக்கிறது.",
    "Packed with Vitamin A, B & C": "வைட்டமின் ஏ, பி மற்றும் சி நிறைந்தது",
    "Purifies blood naturally": "இரத்தத்தை இயற்கையாகவே சுத்தப்படுத்துகிறது",
    "Promotes healthy glowing skin": "ஆரோக்கியமான மற்றும் ஒளிரும் சருமத்தை வழங்குகிறது",
    "Improves overall stamina": "உடல் வலிமையை அதிகரிக்கிறது",

    # Beetroot Malt
    "Natural energy booster and blood purifier.": "இயற்கையான ஆற்றல் மற்றும் இரத்த சுத்திகரிப்பான்.",
    "Rich in Iron and Folic Acid": "இரும்புச்சத்து மற்றும் ஃபோலிக் அமிலம் நிறைந்தது",
    "Prevents anemia naturally": "இரத்த சோகையை இயற்கையாகவே தடுக்கிறது",
    "Improves blood circulation": "இரத்த ஓட்டத்தை மேம்படுத்துகிறது",
    "Healthy drink for kids & pregnant women": "குழந்தைகள் மற்றும் கர்ப்பிணிகளுக்கு ஆரோக்கியமான பானம்",

    # Carrot Malt
    "Improves vision and immunity.": "கண்பார்வை மற்றும் நோய் எதிர்ப்பு சக்தியை மேம்படுத்துகிறது.",
    "High in Vitamin A for eye health": "கண் ஆரோக்கியத்திற்கான வைட்டமின் ஏ நிறைந்தது",
    "Boosts immune system": "நோய் எதிர்ப்பு சக்தியை அதிகரிக்கிறது",
    "Promotes healthy digestion": "ஆரோக்கியமான செரிமானத்தை ஊக்குவிக்கிறது",
    "Delicious alternative to synthetic drinks": "செயற்கை பானங்களுக்கு சுவையான மாற்று",

    # Ragi Malt
    "Powerhouse of calcium for strong bones.": "வலுவான எலும்புகளுக்கு தேவையான கால்சியம் நிறைந்தது.",
    "Rich in Calcium and Vitamin D": "கால்சியம் மற்றும் வைட்டமின் டி நிறைந்தது",
    "Excellent for bone development": "எலும்பு வளர்ச்சிக்கு சிறந்தது",
    "Keeps you full & aids weight loss": "பசியைக் கட்டுப்படுத்தி, எடை குறைப்பிற்கு உதவுகிறது",
    "Perfect cooling drink for summer": "கோடைக்காலத்திற்கு ஏற்ற குளிர்ச்சியான பானம்",

    # Papaya Malt
    "Enhances digestion and skin health.": "செரிமானம் மற்றும் சரும ஆரோக்கியத்தை மேம்படுத்துகிறது.",
    "Rich source of antioxidants": "ஆன்டி-ஆக்ஸிடன்ட்கள் நிறைந்தது",
    "Aids in healthy digestion": "ஆரோக்கியமான செரிமானத்திற்கு உதவுகிறது",
    "Improves skin texture": "சரும அமைப்பை மேம்படுத்துகிறது",
    "Natural detoxifier": "உடலில் உள்ள நச்சுகளை நீக்குகிறது",

    # Red Banana Malt
    "Rich in potassium for heart health.": "இதய ஆரோக்கியத்திற்கான பொட்டாசியம் நிறைந்தது.",
    "Regulates blood pressure": "இரத்த அழுத்தத்தை சீராக்குகிறது",
    "High in Vitamin B6": "வைட்டமின் பி6 நிறைந்தது",
    "Provides instant energy": "உடனடி ஆற்றலை வழங்குகிறது",
    "Improves male & female fertility": "ஆண் மற்றும் பெண் கருவுறுதலை மேம்படுத்துகிறது",

    # Black Gram Porridge Mix
    "Strengthens muscles and joints.": "தசைகள் மற்றும் மூட்டுகளை வலுப்படுத்துகிறது.",
    "Excellent protein source": "சிறந்த புரதச் சத்து நிறைந்தது",
    "Strengthens bones and joints": "எலும்புகள் மற்றும் மூட்டுகளை வலுப்படுத்துகிறது",
    "Relieves back pain": "முதுகு வலியைப் போக்குகிறது",
    "Nourishing for growing children": "வளரும் குழந்தைகளுக்கு ஊட்டமளிக்கிறது",

    # Women's Rice Mix
    "Traditional nourishment for women's wellness.": "பெண்களின் ஆரோக்கியத்திற்கான பாரம்பரிய ஊட்டச்சத்து.",
    "Balances hormones naturally": "ஹார்மோன்களை இயற்கையாகவே சீராக்குகிறது",
    "Rich in iron and zinc": "இரும்பு மற்றும் துத்தநாகம் நிறைந்தது",
    "Supports maternal health": "தாய்மைக்கால ஆரோக்கியத்தை ஆதரிக்கிறது",
    "Provides sustained energy": "நீண்ட நேர ஆற்றலை வழங்குகிறது",

    # Black Rice Mix
    "Rich in antioxidants and detoxifying.": "ஆன்டி-ஆக்ஸிடன்ட்கள் நிறைந்தது மற்றும் நச்சு நீக்கியாக செயல்படுகிறது.",
    "Highest antioxidant properties": "அதிகபட்ச ஆன்டி-ஆக்ஸிடன்ட் பண்புகள் கொண்டது",
    "Aids in liver detoxification": "கல்லீரல் நச்சு நீக்கத்திற்கு உதவுகிறது",
    "Good for diabetic management": "நீரிழிவு நோயைக் கட்டுப்படுத்த சிறந்தது",
    "Promotes heart health": "இதய ஆரோக்கியத்தை மேம்படுத்துகிறது",

    # Kuruvai Rice Mix
    "Revitalizes the body and boosts immunity.": "உடலை புத்துணர்ச்சியாக்கி நோய் எதிர்ப்பு சக்தியை அதிகரிக்கிறது.",
    "Traditional immunity booster": "பாரம்பரிய நோய் எதிர்ப்பு சக்தி ஊக்கி",
    "Improves stamina": "உடல் வலிமையை மேம்படுத்துகிறது",
    "Rich in essential minerals": "அத்தியாவசிய தாதுக்கள் நிறைந்தது",
    "Supports healthy digestion": "ஆரோக்கியமான செரிமானத்தை ஆதரிக்கிறது",

    # Spicy Garlic Pickle
    "Aids digestion and lowers cholesterol.": "செரிமானத்திற்கு உதவுகிறது மற்றும் கொலஸ்ட்ராலை குறைக்கிறது.",
    "Helps lower bad cholesterol": "கெட்ட கொழுப்பை குறைக்க உதவுகிறது",
    "Improves cardiovascular health": "இதய ஆரோக்கியத்தை மேம்படுத்துகிறது",
    "Natural antibacterial properties": "இயற்கையான பாக்டீரியா எதிர்ப்பு பண்புகள்",
    "Enhances taste of any meal": "உணவின் சுவையை அதிகரிக்கிறது",

    # Spicy Onion Pickle
    "Cooling effect with antioxidant boost.": "ஆன்டி-ஆக்ஸிடன்ட் மற்றும் உடலுக்கு குளிர்ச்சியைத் தருகிறது.",
    "Rich in antioxidants": "ஆன்டி-ஆக்ஸிடன்ட்கள் நிறைந்தது",
    "Improves immunity": "நோய் எதிர்ப்பு சக்தியை மேம்படுத்துகிறது",
    "Aids in digestion": "செரிமானத்திற்கு உதவுகிறது",
    "Traditional homemade taste": "பாரம்பரிய வீட்டு முறை சுவை",

    # Tangy Ginger Pickle
    "Relieves nausea and improves digestion.": "குமட்டலைப் போக்கி செரிமானத்தை மேம்படுத்துகிறது.",
    "Soothes digestive system": "செரிமான மண்டலத்தை சாந்தப்படுத்துகிறது",
    "Relieves cold and cough symptoms": "சளி மற்றும் இருமல் அறிகுறிகளைப் போக்குகிறது",
    "Natural anti-inflammatory": "இயற்கையான அழற்சி எதிர்ப்பு பண்புகள்",
    "Authentic tangy flavor": "பாரம்பரிய புளிப்புச் சுவை",

    # Cissus Pickle
    "Strengthens bones and joints naturally.": "எலும்புகள் மற்றும் மூட்டுகளை இயற்கையாகவே வலுப்படுத்துகிறது.",
    "Known as Bone-setter (Pirandai)": "எலும்பு முறிவு மற்றும் மூட்டு வலிக்கு சிறந்தது",
    "Rich in calcium": "கால்சியம் நிறைந்தது",
    "Relieves joint pain": "மூட்டு வலியைப் போக்குகிறது",
    "Improves bone density": "எலும்பு அடர்த்தியை அதிகரிக்கிறது",

    # Gongura Pickle
    "Rich in iron and tangy goodness.": "இரும்புச்சத்து மற்றும் சுவையான புளிப்புத் தன்மை கொண்டது.",
    "Excellent source of Iron": "சிறந்த இரும்புச்சத்து நிறைந்தது",
    "High in Vitamin C": "வைட்டமின் சி நிறைந்தது",
    "Boosts immune system": "நோய் எதிர்ப்பு சக்தியை அதிகரிக்கிறது",
    "Authentic traditional recipe": "உண்மையான பாரம்பரிய செய்முறை",

    # Gooseberry Pickle
    "Vitamin C powerhouse for immunity.": "நோய் எதிர்ப்பு சக்திக்கான வைட்டமின் சி நிறைந்தது.",
    "Highest source of Vitamin C": "அதிகபட்ச வைட்டமின் சி நிறைந்தது",
    "Promotes hair and skin health": "முடி மற்றும் சரும ஆரோக்கியத்தை மேம்படுத்துகிறது",
    "Boosts immunity": "நோய் எதிர்ப்பு சக்தியை அதிகரிக்கிறது",
    "Aids in digestion": "செரிமானத்திற்கு உதவுகிறது",

    # Drumstick Leaves Powder
    "Moringa superfood for overall vitality.": "ஒட்டுமொத்த ஆரோக்கியத்திற்கான முருங்கை சூப்பர்ஃபுட்.",
    "Packed with 90+ nutrients": "90க்கும் மேற்பட்ட ஊட்டச்சத்துக்கள் நிறைந்தது",
    "Increases energy levels": "ஆற்றல் நிலைகளை அதிகரிக்கிறது",
    "Improves hemoglobin": "இரத்த சிவப்பணுக்களை அதிகரிக்கிறது",
    "Good for diabetic management": "நீரிழிவு நோயைக் கட்டுப்படுத்த சிறந்தது",

    # Amla Curry Leaves Powder
    "Promotes hair growth and clear vision.": "முடி வளர்ச்சி மற்றும் தெளிவான பார்வைக்கு உதவுகிறது.",
    "Reduces hair fall and greying": "முடி உதிர்தல் மற்றும் நரைத்தலைக் குறைக்கிறது",
    "Improves eyesight": "கண்பார்வையை மேம்படுத்துகிறது",
    "Rich in iron and vitamins": "இரும்பு மற்றும் வைட்டமின்கள் நிறைந்தது",
    "Enhances memory": "நினைவாற்றலை அதிகரிக்கிறது",

    # Balloon Vine Leaves Powder
    "Natural remedy for joint pain.": "மூட்டு வலிக்கான இயற்கையான தீர்வு.",
    "Relieves arthritis and joint pain": "கீல்வாதம் மற்றும் மூட்டு வலியைப் போக்குகிறது",
    "Natural anti-inflammatory": "இயற்கையான அழற்சி எதிர்ப்பு பண்புகள்",
    "Improves mobility": "உடல் அசைவை மேம்படுத்துகிறது",
    "Traditional medicinal herb": "பாரம்பரிய மூலிகை",

    # Cissus Powder
    "Strengthens bones and improves digestion.": "எலும்புகளை வலுவாக்கி செரிமானத்தை மேம்படுத்துகிறது.",
    "Excellent for bone health": "எலும்பு ஆரோக்கியத்திற்கு சிறந்தது",
    "Relieves gastric issues": "வாயுத் தொல்லையைப் போக்குகிறது",
    "Improves appetite": "பசியைத் தூண்டுகிறது",
    "Rich in natural calcium": "இயற்கை கால்சியம் நிறைந்தது",

    # Garlic Powder
    "Heart-friendly and flavor-packed.": "இதயத்திற்கு உகந்தது மற்றும் சுவை நிறைந்தது.",
    "Regulates blood pressure": "இரத்த அழுத்தத்தை சீராக்குகிறது",
    "Lowers cholesterol levels": "கொலஸ்ட்ரால் அளவைக் குறைக்கிறது",
    "Boosts immune system": "நோய் எதிர்ப்பு சக்தியை அதிகரிக்கிறது",
    "Perfect for daily cooking": "அன்றாட சமையலுக்கு ஏற்றது",

    # Sambar Powder
    "Authentic aroma and flavor for daily meals.": "அன்றாட உணவிற்கான உண்மையான நறுமணம் மற்றும் சுவை.",
    "Made with traditional spices": "பாரம்பரிய மசாலாக்களால் ஆனது",
    "Aids in digestion": "செரிமானத்திற்கு உதவுகிறது",
    "Rich in antioxidants": "ஆன்டி-ஆக்ஸிடன்ட்கள் நிறைந்தது",
    "No artificial colors or flavors": "செயற்கை நிறங்கள் அல்லது சுவைகள் இல்லை",

    # Raw Nendran Banana Powder
    "Nutritious first food for babies and adults.": "குழந்தைகள் மற்றும் பெரியவர்களுக்கான சத்தான உணவு.",
    "Excellent for healthy weight gain": "ஆரோக்கியமான எடை அதிகரிப்பிற்கு சிறந்தது",
    "Easily digestible": "எளிதில் செரிமானமாகக்கூடியது",
    "Rich in potassium": "பொட்டாசியம் நிறைந்தது",
    "Great alternative to processed cereals": "பதப்படுத்தப்பட்ட தானியங்களுக்கு சிறந்த மாற்று",

    # Pure Kerala Honey
    "100% natural immunity booster.": "100% இயற்கையான நோய் எதிர்ப்பு சக்தி ஊக்கி.",
    "Soothes throat and cough": "தொண்டை மற்றும் இருமலைத் தணிக்கிறது",
    "Rich in antioxidants": "ஆன்டி-ஆக்ஸிடன்ட்கள் நிறைந்தது",
    "Natural energy source": "இயற்கையான ஆற்றல் ஆதாரம்",
    "Perfect healthy sweetener": "சரியான ஆரோக்கியமான இனிப்பு",

    # Mudavatukkal Soup
    "Revitalizing soup for joint strength.": "மூட்டுகளை வலுவாக்கும் புத்துணர்ச்சியான சூப்.",
    "Excellent for joint and knee pain": "மூட்டு மற்றும் முழங்கால் வலிக்கு சிறந்தது",
    "Rich in calcium and minerals": "கால்சியம் மற்றும் தாதுக்கள் நிறைந்தது",
    "Warms the body": "உடலை வெப்பப்படுத்துகிறது",
    "Traditional herbal remedy": "பாரம்பரிய மூலிகை தீர்வு",

    # Kollu Soup Mix
    "Aids in weight loss and reduces cholesterol.": "எடை குறைப்பு மற்றும் கொலஸ்ட்ராலை குறைக்க உதவுகிறது.",
    "Burns excess fat": "அதிகப்படியான கொழுப்பை எரிக்கிறது",
    "High in protein and fiber": "அதிக புரதம் மற்றும் நார்ச்சத்து",
    "Relieves cold and congestion": "சளி மற்றும் நெரிசலைப் போக்குகிறது",
    "Keeps you active": "உங்களை சுறுசுறுப்பாக வைத்திருக்கிறது",

    # Mango Thokku
    "Tangy delight that boosts appetite.": "பசியைத் தூண்டும் புளிப்புச் சுவை.",
    "Stimulates digestion": "செரிமானத்தைத் தூண்டுகிறது",
    "Rich in Vitamin C": "வைட்டமின் சி நிறைந்தது",
    "Authentic traditional taste": "உண்மையான பாரம்பரிய சுவை",
    "Perfect side dish for meals": "உணவுக்கு ஏற்ற சிறந்த துணை உணவு",

    # Kulambu Chilli Powder
    "All-in-one spice mix for authentic curries.": "பாரம்பரிய குழம்பிற்கான பலவகை மசாலா கலவை.",
    "Perfect blend of traditional spices": "பாரம்பரிய மசாலாக்களின் சரியான கலவை",
    "Saves cooking time": "சமையல் நேரத்தை மிச்சப்படுத்துகிறது",
    "No artificial preservatives": "செயற்கை பதப்படுத்திகள் இல்லை",
    "Enhances flavor naturally": "சுவையை இயற்கையாகவே அதிகரிக்கிறது"
}

soup = BeautifulSoup(content, 'html.parser')

product_cards = soup.find_all('div', class_='product-card')
for card in product_cards:
    # 1. Main benefit (.product-benefit)
    benefit_elem = card.find('p', class_='product-benefit')
    if benefit_elem and benefit_elem.string:
        en_text = benefit_elem.string.strip()
        if en_text in tamil_dict:
            ta_text = tamil_dict[en_text]
            benefit_elem.clear()
            benefit_elem.append(en_text)
            benefit_elem.append(soup.new_tag('br'))
            ta_span = soup.new_tag('span', style="font-size: 0.85em; font-weight: normal;")
            ta_span.string = ta_text
            benefit_elem.append(ta_span)

    # 2. Key benefits hover overlay
    overlay = card.find('div', class_='product-hover-overlay')
    if overlay:
        ul_elem = overlay.find('ul')
        if ul_elem:
            for li in ul_elem.find_all('li'):
                # Handle cases where we might have already added Tamil translation
                if li.find('br'):
                    continue
                en_text = li.text.strip()
                if en_text in tamil_dict:
                    ta_text = tamil_dict[en_text]
                    li.clear()
                    li.append(en_text)
                    li.append(soup.new_tag('br'))
                    ta_span = soup.new_tag('span', style="font-size: 0.9em; opacity: 0.9; display: block; padding-top: 2px;")
                    ta_span.string = ta_text
                    li.append(ta_span)

# Write it back
with open(html_file, "w", encoding="utf-8") as f:
    f.write(str(soup))

print("Tamil translations successfully injected!")
