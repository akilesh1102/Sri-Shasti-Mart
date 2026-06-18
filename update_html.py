import re

with open("index.html", "r") as f:
    content = f.read()

# Replace the logo
logo_old = """      <a href="#" class="logo">
        Sri Shasti Mart
      </a>"""
logo_new = """      <a href="#" class="logo" style="display: flex; flex-direction: column; align-items: flex-start; line-height: 1.2;">
        <span>Sri Shasti Mart</span>
        <span style="font-size: 0.8rem; font-weight: normal;">ஸ்ரீ சஷ்டி மார்ட்</span>
      </a>"""
content = content.replace(logo_old, logo_new)

# A list of tuples (old_html_chunk, new_html_chunk)
replacements = [
    # ABC Malt
    (
        """<h3 class="product-title">ABC Malt</h3>
              <p class="product-desc">Apple Beetroot Carrot Nuts Nutritional Mix</p>""",
        """<h3 class="product-title">ABC Malt</h3>
              <p class="product-desc">ஏபிசி மால்ட் (ABC Malt)</p>"""
    ),
    # Beetroot Malt
    (
        """<h3 class="product-title">Beetroot Malt</h3>
              <p class="product-desc">Beetroot & Nuts Nutritional Mix</p>""",
        """<h3 class="product-title">Beetroot Malt</h3>
              <p class="product-desc">பீட்ரூட் மால்ட் (Beetroot Malt)</p>"""
    ),
    # Carrot Malt
    (
        """<h3 class="product-title">Carrot Malt</h3>
              <p class="product-desc">Carrot & Nuts Nutritional Mix</p>""",
        """<h3 class="product-title">Carrot Malt</h3>
              <p class="product-desc">கேரட் மால்ட் (Carrot Malt)</p>"""
    ),
    # Ragi Malt
    (
        """<h3 class="product-title">Ragi Malt</h3>
              <p class="product-desc">Sprouted Ragi & Nuts Nutritional Mix</p>""",
        """<h3 class="product-title">Ragi Malt</h3>
              <p class="product-desc">ராகி மால்ட் (Ragi Malt)</p>"""
    ),
    # Papaya Malt
    (
        """<h3 class="product-title">Papaya Malt</h3>
              <p class="product-desc">Papaya & Nuts Nutritional Mix</p>""",
        """<h3 class="product-title">Papaya Malt</h3>
              <p class="product-desc">பப்பாளி மால்ட் (Papaya Malt)</p>"""
    ),
    # Red Banana Malt
    (
        """<h3 class="product-title">Red Banana Malt</h3>
              <p class="product-desc">Red Banana & Nuts Nutritional Mix</p>""",
        """<h3 class="product-title">Red Banana Malt</h3>
              <p class="product-desc">செவ்வாழை மால்ட் (Red Banana Malt)</p>"""
    ),
    # Karuppu Ulundhu Kanji
    (
        """<h3 class="product-title">Karuppu Ulundhu Kanji</h3>
              <p class="product-desc">Black Gram Porridge & Nuts Nutritional Mix</p>
              <span class="product-tag">Millet Mix</span>
              <p class="product-english-name">Black Gram Porridge Mix</p>""",
        """<h3 class="product-title">Black Gram Porridge Mix</h3>
              <p class="product-desc">கருப்பு உளுந்து கஞ்சி (Karuppu Ulundhu Kanji)</p>
              <span class="product-tag">Millet Mix</span>"""
    ),
    # Poongar Rice Kanji Mix
    (
        """<h3 class="product-title">Poongar Rice Kanji Mix</h3>
              <p class="product-desc">Traditional Poongar Rice Porridge Mix.</p>
              <span class="product-tag">Millet Mix</span>
              <p class="product-english-name">Women's Rice Mix</p>""",
        """<h3 class="product-title">Women's Rice Mix</h3>
              <p class="product-desc">பூங்கார் அரிசி கஞ்சி (Poongar Rice Kanji)</p>
              <span class="product-tag">Millet Mix</span>"""
    ),
    # Karuppu Kavuni Kanji Mix
    (
        """<h3 class="product-title">Karuppu Kavuni Kanji Mix</h3>
              <p class="product-desc">Black Rice Porridge Mix - The Forbidden Rice.</p>
              <span class="product-tag">Millet Mix</span>
              <p class="product-english-name">Black Rice Mix</p>""",
        """<h3 class="product-title">Black Rice Mix</h3>
              <p class="product-desc">கருப்பு கவுனி கஞ்சி (Karuppu Kavuni Kanji)</p>
              <span class="product-tag">Millet Mix</span>"""
    ),
    # Karunguruvai Kanji Mix
    (
        """<h3 class="product-title">Karunguruvai Kanji Mix</h3>
              <p class="product-desc">Traditional Red Rice Porridge Mix.</p>
              <span class="product-tag">Millet Mix</span>
              <p class="product-english-name">Kuruvai Rice Mix</p>""",
        """<h3 class="product-title">Kuruvai Rice Mix</h3>
              <p class="product-desc">கருங்குறுவை கஞ்சி (Karunguruvai Kanji)</p>
              <span class="product-tag">Millet Mix</span>"""
    ),
    # Garlic Pickle
    (
        """<h3 class="product-title">Garlic Pickle</h3>
              <p class="product-desc">Homemade Garlic Pickle - Poondu Oorugai.</p>
              <span class="product-tag">Pickles</span>
              <p class="product-english-name">Spicy Garlic Pickle</p>""",
        """<h3 class="product-title">Spicy Garlic Pickle</h3>
              <p class="product-desc">பூண்டு ஊறுகாய் (Poondu Oorugai)</p>
              <span class="product-tag">Pickles</span>"""
    ),
    # Onion Thokku
    (
        """<h3 class="product-title">Onion Thokku</h3>
              <p class="product-desc">Traditional Onion Pickle - Vengayam Thokku.</p>
              <span class="product-tag">Pickles</span>
              <p class="product-english-name">Spicy Onion Pickle</p>""",
        """<h3 class="product-title">Spicy Onion Pickle</h3>
              <p class="product-desc">வெங்காயம் தொக்கு (Vengayam Thokku)</p>
              <span class="product-tag">Pickles</span>"""
    ),
    # Ginger Pickle
    (
        """<h3 class="product-title">Ginger Pickle</h3>
              <p class="product-desc">Homemade Ginger Pickle - Inji Thokku.</p>
              <span class="product-tag">Pickles</span>
              <p class="product-english-name">Tangy Ginger Pickle</p>""",
        """<h3 class="product-title">Tangy Ginger Pickle</h3>
              <p class="product-desc">இஞ்சி தொக்கு (Inji Thokku)</p>
              <span class="product-tag">Pickles</span>"""
    ),
    # Pirandai Thokku
    (
        """<h3 class="product-title">Pirandai Thokku</h3>
              <p class="product-desc">Traditional Pirandai Thokku - Bone Setter Pickle.</p>
              <span class="product-tag">Pickles</span>
              <p class="product-english-name">Cissus Pickle</p>""",
        """<h3 class="product-title">Cissus Pickle</h3>
              <p class="product-desc">பிரண்டை தொக்கு (Pirandai Thokku)</p>
              <span class="product-tag">Pickles</span>"""
    ),
    # Pulicha Kirai Thokku
    (
        """<h3 class="product-title">Pulicha Kirai Thokku</h3>
              <p class="product-desc">Traditional Gongura Thokku - Sorrel Leaves Pickle.</p>
              <span class="product-tag">Pickles</span>
              <p class="product-english-name">Gongura Pickle</p>""",
        """<h3 class="product-title">Gongura Pickle</h3>
              <p class="product-desc">புளிச்சக்கீரை தொக்கு (Pulicha Keerai Thokku)</p>
              <span class="product-tag">Pickles</span>"""
    ),
    # Amla Pickle
    (
        """<h3 class="product-title">Amla Pickle</h3>
              <p class="product-desc">Traditional Amla Pickle - Nellikai Oorugai.</p>
              <span class="product-tag">Pickles</span>
              <p class="product-english-name">Gooseberry Pickle</p>""",
        """<h3 class="product-title">Gooseberry Pickle</h3>
              <p class="product-desc">நெல்லிக்காய் ஊறுகாய் (Nellikai Oorugai)</p>
              <span class="product-tag">Pickles</span>"""
    ),
    # Murungai Keerai Podi
    (
        """<h3 class="product-title">Murungai Keerai Podi</h3>
              <p class="product-desc">Drumstick Leaves Spiced Powder.</p>
              <span class="product-tag">Rice Mix / Podi</span>
              <p class="product-english-name">Drumstick Leaves Powder</p>""",
        """<h3 class="product-title">Drumstick Leaves Powder</h3>
              <p class="product-desc">முருங்கைக்கீரை பொடி (Murungai Keerai Podi)</p>
              <span class="product-tag">Rice Mix / Podi</span>"""
    ),
    # Nellikai Karuveppilai Podi
    (
        """<h3 class="product-title">Nellikai Karuveppilai Podi</h3>
              <p class="product-desc">Amla & Curry Leaves Spiced Powder.</p>
              <span class="product-tag">Rice Mix / Podi</span>
              <p class="product-english-name">Amla Curry Leaves Powder</p>""",
        """<h3 class="product-title">Amla Curry Leaves Powder</h3>
              <p class="product-desc">நெல்லிக்காய் கறிவேப்பிலை பொடி (Nellikai Karuveppilai Podi)</p>
              <span class="product-tag">Rice Mix / Podi</span>"""
    ),
    # Mudakathan Keerai Podi
    (
        """<h3 class="product-title">Mudakathan Keerai Podi</h3>
              <p class="product-desc">Balloon Vine Leaves Spiced Powder.</p>
              <span class="product-tag">Rice Mix / Podi</span>
              <p class="product-english-name">Balloon Vine Leaves Powder</p>""",
        """<h3 class="product-title">Balloon Vine Leaves Powder</h3>
              <p class="product-desc">முடக்கத்தான் கீரை பொடி (Mudakathan Keerai Podi)</p>
              <span class="product-tag">Rice Mix / Podi</span>"""
    ),
    # Pirandai Podi (the old one)
    (
        """<h3 class="product-title">Pirandai Podi</h3>
              <p class="product-desc">Adamant Creeper Spiced Powder.</p>
              <span class="product-tag">Rice Mix / Podi</span>
              <p class="product-english-name">Cissus Powder</p>""",
        """<h3 class="product-title">Cissus Powder</h3>
              <p class="product-desc">பிரண்டை பொடி (Pirandai Podi)</p>
              <span class="product-tag">Rice Mix / Podi</span>"""
    ),
    # Poondu Podi
    (
        """<h3 class="product-title">Poondu Podi</h3>
              <p class="product-desc">Garlic Spiced Powder.</p>
              <span class="product-tag">Rice Mix / Podi</span>
              <p class="product-english-name">Garlic Powder</p>""",
        """<h3 class="product-title">Garlic Powder</h3>
              <p class="product-desc">பூண்டு பொடி (Poondu Podi)</p>
              <span class="product-tag">Rice Mix / Podi</span>"""
    )
]

for old, new in replacements:
    content = content.replace(old, new)

with open("index.html", "w") as f:
    f.write(content)

print("Updates applied.")
