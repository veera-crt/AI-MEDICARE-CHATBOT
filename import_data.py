import csv

new_data = [
    
        ["Common Day-to-Day Ailments and Natural Treatments"],
        ["Ailment", "Natural Treatment", "Dosage/Frequency"],
        ["Headache", 
         "Peppermint oil + Ginger tea", 
         "2 drops on temples + 1 cup ginger tea (1-inch root) 2x/day"],
        ["Common Cold", 
         "Turmeric milk + Steam inhalation", 
         "½ tsp turmeric in warm milk at night + Steam with 2 drops eucalyptus oil 2x/day"],
        ["Indigestion", 
         "Ajwain water + Ginger", 
         "1 tsp ajwain soaked overnight (morning) + 1-inch ginger chew before meals"],
        ["Insomnia", 
         "Chamomile tea + Warm milk", 
         "1 cup chamomile tea + 1 cup milk with ¼ tsp nutmeg at bedtime"],
        ["Muscle Pain", 
         "Epsom salt bath + Turmeric paste", 
         "2 cups salts in bath water + 1 tsp turmeric paste on affected area"],
        ["Stress/Anxiety", 
         "Ashwagandha + Meditation", 
         "½ tsp ashwagandha in milk at night + 10 mins meditation daily"],
        ["Seasonal Allergies", 
         "Local honey + Nettle tea", 
         "1 tsp raw local honey daily + 1 cup nettle tea 2x/day"],
        ["Mouth Ulcers", 
         "Coconut oil + Turmeric", 
         "1 tbsp oil pulling 10 mins + turmeric-honey paste applied 3x/day"],
        ["Work Fatigue", 
         "Ginseng tea + Walnuts", 
         "1 cup ginseng tea morning + 5-6 soaked walnuts daily"],
        ["Eye Strain", 
         "Rose water + Cucumber", 
         "2 drops rose water in eyes + cool slices for 10 mins 2x/day"],
        ["Travel Sickness", 
         "Ginger + Peppermint", 
         "1-inch ginger chew before travel + peppermint oil sniffing during trip"],
        ["Hangover", 
         "Coconut water + Banana", 
         "500ml coconut water + 2 ripe bananas on empty stomach"],
        ["Acid Reflux", 
         "Aloe vera juice + Fennel", 
         "¼ cup aloe juice before meals + 1 tsp fennel seeds after eating"],
        ["Dry Skin", 
         "Coconut oil + Honey mask", 
         "1 tbsp oil massage daily + honey mask (1 tsp) 2x/week"],
        ["Hair Fall", 
         "Onion juice + Fenugreek", 
         "2 tbsp onion juice scalp massage 3x/week + fenugreek paste 1x/week"],
        ["Menstrual Cramps", 
         "Ginger tea + Heat pad", 
         "1 cup ginger tea 3x/day + warm compress on abdomen"],
        ["Low Immunity", 
         "Chyawanprash + Citrus fruits", 
         "1 tsp chyawanprash morning + 1 citrus fruit daily"],
        ["Bloating", 
         "Peppermint tea + Fennel", 
         "1 cup peppermint tea 2x/day + ½ tsp fennel seeds after meals"],
        ["Sunburn", 
         "Aloe vera + Coconut water", 
         "Fresh aloe gel applied 3x/day + 2 glasses coconut water daily"],
        ["Bad Breath", 
         "Cloves + Parsley", 
         "2 cloves chewed after meals + parsley leaves as garnish"]
    ]


# File path to your existing CSV
file_path = "medical_data.csv"

# Append mode ('a'), newline to avoid extra blank lines
with open(file_path, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(new_data)

print("✅ New data appended to your CSV successfully.")