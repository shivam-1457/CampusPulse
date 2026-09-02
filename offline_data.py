"""
Offline verified medical first-aid protocols & campus safety guidelines.
Follows standard Red Cross, AHA (American Heart Association), and OSHA laboratory safety protocols.
"""

PROTOCOLS = {
    "burn": {
        "title": "Thermal / Heat Burn",
        "severity": "moderate",
        "severity_badge": "Amber - Needs Immediate Action",
        "immediate_action": "Cool immediately with cool (not freezing) running tap water for at least 15 to 20 minutes.",
        "steps": [
            "Remove patient from heat source immediately.",
            "Hold the burned area under cool, gentle running water for 15-20 minutes. DO NOT use ice or ice water.",
            "Gently remove tight items (rings, watches, belts, tight clothing) around the burn before swelling begins.",
            "DO NOT pop or puncture blisters, as this increases severe infection risk.",
            "Cover the burn loosely with a clean, sterile, non-adherent gauze bandage or clean plastic cling wrap.",
            "Keep the patient calm and warm to prevent shock.",
            "If burn is on face, hands, groin, major joints, or covers > 3 inches, seek immediate emergency medical care."
        ],
        "dos": [
            "Use cool running water for 15-20 minutes",
            "Loosely cover with sterile, non-stick dressing",
            "Elevate burned limb if possible to reduce swelling"
        ],
        "donts": [
            "DO NOT apply ice, iced water, butter, oils, or toothpaste",
            "DO NOT break or drain blisters",
            "DO NOT peel off clothing stuck to the burn tissue"
        ],
        "red_flags": [
            "Burn is larger than 3 inches (size of patient's palm)",
            "Burn appears white, charred, leathery, or painless (3rd degree)",
            "Burn is on face, neck, hands, feet, groin, or major joint",
            "Patient inhaled smoke/fumes or exhibits wheezing/coughing",
            "Victim is an infant, elderly, or immunocompromised"
        ],
        "recommended_equipment": ["Cool Running Water", "Sterile Non-Adherent Gauze", "Burn Dressing", "Medical Tape"],
        "timer_type": "burn_rinse",
        "timer_duration_seconds": 900
    },
    "chemical_splash": {
        "title": "Chemical Splash / Lab Hazard",
        "severity": "severe",
        "severity_badge": "Red - Critical Emergency",
        "immediate_action": "Flush affected skin or eyes with continuous water at an emergency eyewash/safety shower for 15 continuous minutes.",
        "steps": [
            "Guide victim immediately to nearest Safety Shower or Eyewash Station.",
            "Hold eyelids wide open while rotating eyes in all directions under water stream for at least 15 continuous minutes.",
            "While flushing skin, rapidly remove contaminated clothing, lab coats, and jewelry under running water.",
            "Have someone locate Safety Data Sheet (SDS) / chemical bottle label to identify substance for medics.",
            "DO NOT attempt to neutralize acids with bases or vice-versa (causes exothermic thermal burns).",
            "Notify Campus Lab Safety Officer and Campus Emergency Services (Ext 5555 / 911) immediately."
        ],
        "dos": [
            "Flush continuously for a minimum of 15-20 minutes",
            "Keep eyes held open with fingers under eyewash",
            "Locate Chemical Name / SDS sheet for responders"
        ],
        "donts": [
            "DO NOT rub eyes or scratch affected skin",
            "DO NOT try to chemically neutralize acid or alkali",
            "DO NOT use neutralizing chemical ointments without poison control guidance"
        ],
        "red_flags": [
            "Involvement of strong acids (Hydrofluoric, Sulfuric) or strong bases (Sodium Hydroxide)",
            "Any eye exposure causing intense pain, vision blurring, or clouding",
            "Inhalation of toxic gas, fumes, or vapors"
        ],
        "recommended_equipment": ["Emergency Eyewash Station", "Safety Shower", "Chemical Spill Kit", "SDS Sheet"],
        "timer_type": "eyewash",
        "timer_duration_seconds": 900
    },
    "cpr": {
        "title": "Unresponsive & Not Breathing (Cardiac Arrest / CPR)",
        "severity": "severe",
        "severity_badge": "Red - Critical Life Threat",
        "immediate_action": "Call 911 / Campus EMS immediately, get an AED, and begin Hands-Only CPR at 100-120 BPM.",
        "steps": [
            "Check scene safety. Tap patient's shoulders and shout loudly: 'Are you okay?'",
            "If unresponsive and not breathing normally (or only gasping): Point to a specific bystander: 'Call 911 and bring the nearest AED!'",
            "Place patient flat on their back on a firm, hard surface.",
            "Position heel of one hand in the center of the chest (lower half of breastbone); place other hand on top and interlock fingers.",
            "Push HARD and FAST: Compress at least 2 inches (5 cm) deep at a rate of 100-120 beats per minute (sync with metronome or song 'Stayin' Alive').",
            "Allow complete chest recoil between compressions without bouncing off chest.",
            "As soon as AED arrives, turn it ON and follow its voice prompts immediately."
        ],
        "dos": [
            "Push hard and fast in center of chest (100-120 BPM)",
            "Allow full chest recoil after every compression",
            "Apply AED pads as soon as device arrives"
        ],
        "donts": [
            "DO NOT stop compressions for more than 10 seconds",
            "DO NOT place hands over stomach or lower tip of breastbone",
            "DO NOT touch patient while AED is analyzing or shocking"
        ],
        "red_flags": [
            "Patient is unresponsive to voice and pain",
            "No normal breathing, agonal gasping, or blue lips/fingertips"
        ],
        "recommended_equipment": ["AED (Defibrillator)", "CPR Face Shield", "Gloves"],
        "timer_type": "cpr_metronome",
        "timer_duration_seconds": 120
    },
    "choking": {
        "title": "Choking (Airway Obstruction)",
        "severity": "severe",
        "severity_badge": "Red - Critical Emergency",
        "immediate_action": "Perform Heimlich maneuver (abdominal thrusts) immediately if victim cannot speak, cough, or breathe.",
        "steps": [
            "Ask: 'Are you choking?' If person can cough forcefully or speak, encourage them to keep coughing.",
            "If victim nods, cannot speak, makes high-pitched wheezing, or gives universal choking sign (hands at throat): Act immediately.",
            "Stand behind victim. Place one foot slightly forward for balance. Wrap your arms around their waist.",
            "Make a fist with one hand; place thumb side just above victim's navel and well below ribcage.",
            "Grasp fist with your other hand. Perform quick, upward and inward abdominal thrusts.",
            "Repeat thrusts until object is expelled or victim becomes unconscious.",
            "If victim becomes unresponsive, lower carefully to the ground, call 911, and begin CPR."
        ],
        "dos": [
            "Perform inward and upward abdominal thrusts",
            "For pregnant or obese victims, perform chest thrusts instead",
            "Call 911 immediately if airway remains blocked"
        ],
        "donts": [
            "DO NOT perform blind finger sweeps in mouth (may push object deeper)",
            "DO NOT slap back while person is upright if standing alone (can lodge food)",
            "DO NOT give water or fluids to a choking person"
        ],
        "red_flags": [
            "Inability to breathe, speak, or make sound",
            "Face turning blue / cyanotic",
            "Loss of consciousness"
        ],
        "recommended_equipment": ["None - Immediate Bystander Action Required"],
        "timer_type": "none",
        "timer_duration_seconds": 0
    },
    "bleeding": {
        "title": "Severe Bleeding / Deep Laceration",
        "severity": "severe",
        "severity_badge": "Red - Urgent Bleeding Control",
        "immediate_action": "Apply firm, direct continuous pressure on the wound with sterile gauze or clean cloth for at least 5 continuous minutes.",
        "steps": [
            "Ensure personal safety; put on medical gloves if available.",
            "Apply direct, steady pressure over the bleeding site using sterile gauze, trauma pad, or clean cloth.",
            "Maintain uninterrupted pressure for 5 full minutes without lifting pad to check.",
            "If blood soaks through, DO NOT remove original dressing—add more pads on top and press harder.",
            "If bleeding is arterial (spurting) or limb bleeding won't stop with direct pressure, apply a commercial Tourniquet 2-3 inches above wound (never on joint) and tighten until bleeding ceases. Note exact time applied.",
            "Keep patient lying down and warm to combat shock."
        ],
        "dos": [
            "Apply continuous firm pressure without lifting dressing",
            "Elevate wounded limb above heart level if no fracture is suspected",
            "Use tourniquet if life-threatening limb hemorrhage cannot be stopped"
        ],
        "donts": [
            "DO NOT remove embedded objects (stabilize in place instead)",
            "DO NOT remove soaked bandages—layer more over top",
            "DO NOT loosen tourniquet once applied until emergency medical team takes over"
        ],
        "red_flags": [
            "Spurting, pulsating, or rapid continuous pooling of blood",
            "Signs of hemorrhagic shock (pale, cold, clammy skin, dizziness, confusion)",
            "Deep wound exposing fat, muscle, tendon, or bone"
        ],
        "recommended_equipment": ["Sterile Gauze", "Trauma Bandage", "Medical Gloves", "Tourniquet"],
        "timer_type": "bleeding_pressure",
        "timer_duration_seconds": 300
    },
    "seizure": {
        "title": "Seizure / Convulsion",
        "severity": "moderate",
        "severity_badge": "Amber - Protect and Monitor",
        "immediate_action": "Protect the person from injury, cushion their head, clear surrounding furniture, and time the seizure.",
        "steps": [
            "Stay calm and start a timer / note the exact start time of the seizure.",
            "Ease the person to the floor. Place a soft folded jacket or pillow under their head.",
            "Move away sharp objects, chairs, tables, and hazardous items.",
            "Loosen tight neckwear (ties, collars) and remove eyeglasses.",
            "DO NOT hold the person down, restrain their movements, or put anything into their mouth.",
            "When convulsions stop, gently roll the person onto their side into the Recovery Position to keep airway open.",
            "Stay with them until fully conscious, calm, and reoriented."
        ],
        "dos": [
            "Cushion head with soft padding",
            "Turn onto side (recovery position) once jerking stops",
            "Track exact duration with stopwatch"
        ],
        "donts": [
            "DO NOT put anything in mouth (they will NOT swallow tongue)",
            "DO NOT restrain or forcibly hold limbs",
            "DO NOT offer food, drink, or medication until fully alert"
        ],
        "red_flags": [
            "Seizure lasts longer than 5 minutes (Status Epilepticus - 911 urgent)",
            "Repeated seizures occur without waking between episodes",
            "Person was injured, pregnant, in water, or has diabetes",
            "First known seizure in patient's life"
        ],
        "recommended_equipment": ["Soft Cushion/Jacket", "Stopwatch Timer"],
        "timer_type": "seizure_tracker",
        "timer_duration_seconds": 0
    },
    "anaphylaxis": {
        "title": "Severe Allergic Reaction (Anaphylaxis)",
        "severity": "severe",
        "severity_badge": "Red - Critical Life Threat",
        "immediate_action": "Administer Epinephrine Auto-Injector (EpiPen) into outer mid-thigh immediately and call 911.",
        "steps": [
            "Recognize symptoms: sudden difficulty breathing, throat tightness, facial/lip swelling, hives, dizziness.",
            "Call 911 / Campus Emergency immediately.",
            "If victim has an EpiPen / Auvi-Q: Remove safety cap, press firmly into outer mid-thigh until it clicks, hold in place for 3 full seconds.",
            "Massage injection site for 10 seconds.",
            "Have victim lie flat with legs elevated (unless breathing is difficult, then allow sitting upright).",
            "If symptoms persist and EMS has not arrived within 5-10 minutes, a second dose may be administered.",
            "Save used injector to hand over to EMS team."
        ],
        "dos": [
            "Administer epinephrine into outer mid-thigh promptly",
            "Keep patient calm and lying down",
            "Call 911 even if symptoms improve (rebound reaction possible)"
        ],
        "donts": [
            "DO NOT delay epinephrine injection in suspected anaphylaxis",
            "DO NOT force patient to stand or walk around",
            "DO NOT rely only on oral antihistamines for airway compromise"
        ],
        "red_flags": [
            "Stridor, wheezing, or feeling of throat closing",
            "Swelling of tongue, lips, or uvula",
            "Rapid drop in blood pressure, fainting, or confusion"
        ],
        "recommended_equipment": ["EpiPen (Epinephrine Auto-Injector)", "Antihistamine"],
        "timer_type": "epipen_dose",
        "timer_duration_seconds": 300
    },
    "heat_stroke": {
        "title": "Heat Stroke / Heat Exhaustion",
        "severity": "severe",
        "severity_badge": "Red - Medical Emergency",
        "immediate_action": "Move victim to air-conditioned area or shade, call 911, and cool aggressively with ice packs/water.",
        "steps": [
            "Differentiate: Heat Stroke involves body temp > 103°F (39.4°C), hot/red/dry or sweaty skin, confusion, or loss of consciousness.",
            "Call 911 / Campus EMS immediately.",
            "Move victim into shade, cool vehicle, or air-conditioned campus building.",
            "Rapid cooling: Sponge or mist body with cold water and fan vigorously.",
            "Place ice packs wrapped in towels on neck, armpits, and groin where major blood vessels pass.",
            "If conscious and alert, offer sips of cool water or electrolyte drink. DO NOT give drinks if confused or vomiting."
        ],
        "dos": [
            "Cool body rapidly with mist, fans, and cold towels",
            "Apply ice packs to neck, armpits, and groin",
            "Elevate feet slightly if showing heat exhaustion symptoms"
        ],
        "donts": [
            "DO NOT give fluids if patient is drowsy, confused, or vomiting",
            "DO NOT give aspirin or acetaminophen (does not work for heat stroke)",
            "DO NOT leave patient unattended"
        ],
        "red_flags": [
            "Altered mental status, slurred speech, delirium, or coma",
            "Vomiting or seizures",
            "Body temperature above 103°F / 39.5°C"
        ],
        "recommended_equipment": ["Cold Water", "Ice Packs", "Electrolytes", "Fan"],
        "timer_type": "none",
        "timer_duration_seconds": 0
    },
    "sprain_fracture": {
        "title": "Sprain, Strain, or Suspected Fracture",
        "severity": "moderate",
        "severity_badge": "Amber - Stabilize & Protect",
        "immediate_action": "Immobilize the limb, do not bear weight, and apply R.I.C.E. (Rest, Ice, Compression, Elevation).",
        "steps": [
            "Keep the injured limb still. DO NOT attempt to realign or push back a deformed bone or joint.",
            "Rest: Stop activity and do not put weight on the limb.",
            "Ice: Apply cold pack wrapped in a cloth for 15-20 minutes every 2 hours to minimize swelling.",
            "Compression: Wrap lightly with an elastic bandage from distal to proximal; ensure it is not too tight (check pulse/warmth).",
            "Elevation: Prop limb up above heart level if comfortable.",
            "If bone has pierced skin (compound fracture), cover with sterile gauze and call emergency services."
        ],
        "dos": [
            "Apply R.I.C.E. protocol (Rest, Ice, Compress, Elevate)",
            "Support joint in comfortable position with pillow/splint",
            "Check circulation in fingers/toes after wrapping"
        ],
        "donts": [
            "DO NOT apply ice directly onto bare skin (causes frostbite)",
            "DO NOT try to straighten a crooked or dislocated joint",
            "DO NOT massage an acutely injured or swollen area"
        ],
        "red_flags": [
            "Visible bone deformity, open wound with exposed bone",
            "Loss of sensation, tingling, or blue/cold fingers or toes",
            "Inability to move digits or severe intractable pain"
        ],
        "recommended_equipment": ["Cold Pack", "Elastic Bandage (Ace wrap)", "Splint / Sling", "Pillow"],
        "timer_type": "ice_pack",
        "timer_duration_seconds": 900
    },
    "fainting_syncope": {
        "title": "Fainting (Syncope) / Sudden Dizziness",
        "severity": "low",
        "severity_badge": "Green - Mild / Monitor",
        "immediate_action": "Lay person flat on their back and elevate legs about 12 inches (30 cm) to restore blood flow to brain.",
        "steps": [
            "Ensure the person is lying flat on their back in a cool, well-ventilated space.",
            "Elevate legs approximately 12 inches (30 cm) above heart level.",
            "Loosen tight collars, belts, or restrictive clothing.",
            "Check breathing and responsiveness. Most faints resolve within 30-60 seconds.",
            "When alert, allow person to sit up gradually over several minutes before standing.",
            "Offer water or juice once fully awake and sitting securely."
        ],
        "dos": [
            "Elevate legs 12 inches above heart level",
            "Ensure adequate fresh air circulation",
            "Keep patient lying down for at least 10-15 minutes after waking"
        ],
        "donts": [
            "DO NOT force patient to get up or walk too quickly",
            "DO NOT slap face or splash water on victim",
            "DO NOT give food or drink while patient is unconscious"
        ],
        "red_flags": [
            "Loss of consciousness lasting more than 1 minute",
            "Head injury or concussion sustained from the fall",
            "Fainting accompanied by chest pain, shortness of breath, or palpitations"
        ],
        "recommended_equipment": ["Elevated Support / Chair", "Cool Water", "Electrolyte drink"],
        "timer_type": "none",
        "timer_duration_seconds": 0
    }
}

# Supported campus facilities
CAMPUS_FACILITIES = [
    {
        "id": "aed_science_1",
        "name": "Science Complex AED Station",
        "building": "Science Complex",
        "floor": "1st Floor Main Lobby (Next to Lab 101)",
        "type": "AED",
        "icon": "zap",
        "distance": "45m",
        "phone": "+1 (555) 019-2831"
    },
    {
        "id": "eyewash_chem_3",
        "name": "Organic Chem Safety Shower & Eyewash",
        "building": "Chemistry Hall",
        "floor": "3rd Floor Corridor (Opposite Lab 304)",
        "type": "Eyewash & Shower",
        "icon": "droplets",
        "distance": "15m",
        "phone": "+1 (555) 019-2832"
    },
    {
        "id": "firstaid_student_center",
        "name": "Student Center First Aid & Trauma Kit",
        "building": "Student Union",
        "floor": "Ground Floor Information Desk",
        "type": "First Aid Kit",
        "icon": "cross",
        "distance": "80m",
        "phone": "+1 (555) 019-2833"
    },
    {
        "id": "infirmary_main",
        "name": "Campus Health & Wellness Center (Infirmary)",
        "building": "Health Services Pavilion",
        "floor": "Bldg 4, Suite 100",
        "type": "Infirmary / Clinic",
        "icon": "hospital",
        "distance": "180m",
        "phone": "+1 (555) 019-2800"
    },
    {
        "id": "aed_library",
        "name": "Main Library Central AED Station",
        "building": "University Library",
        "floor": "2nd Floor Reference Desk",
        "type": "AED",
        "icon": "zap",
        "distance": "120m",
        "phone": "+1 (555) 019-2834"
    },
    {
        "id": "safety_sports",
        "name": "Athletics Fieldhouse First-Aid Station",
        "building": "Sports Arena",
        "floor": "Locker Room Concourse Entrance",
        "type": "First Aid Kit & AED",
        "icon": "activity",
        "distance": "220m",
        "phone": "+1 (555) 019-2835"
    }
]

# Emergency Contacts Directory
DEFAULT_CONTACTS = [
    {
        "id": "campus_police",
        "name": "Campus Police & Security Dispatch",
        "role": "Immediate Physical Safety & 911 Bridge",
        "phone": "911 / (555) 019-9111",
        "speed_dial": "tel:911",
        "priority": 1,
        "available_24_7": True
    },
    {
        "id": "health_center",
        "name": "Campus Health Center / Infirmary",
        "role": "Medical Staff & Triage Care",
        "phone": "(555) 019-2800",
        "speed_dial": "tel:5550192800",
        "priority": 2,
        "available_24_7": True
    },
    {
        "id": "lab_safety",
        "name": "Environmental Health & Lab Safety Officer (EHS)",
        "role": "Chemical, Biological & Fire Hazards",
        "phone": "(555) 019-4321",
        "speed_dial": "tel:5550194321",
        "priority": 3,
        "available_24_7": True
    },
    {
        "id": "dorm_ra",
        "name": "Residential Life / Head Dorm RA",
        "role": "Dormitory & Student Housing Support",
        "phone": "(555) 019-7788",
        "speed_dial": "tel:5550197788",
        "priority": 4,
        "available_24_7": True
    }
]

# Multilingual Translations for standard safety protocols
LANGUAGE_TRANSLATIONS = {
    "es": {
        "name": "Español (Spanish)",
        "call_emergency": "Llamar a Emergencias",
        "immediate_action": "Acción Inmediata",
        "step_by_step": "Protocolo Paso a Paso",
        "dos": "Qué Hacer",
        "donts": "Qué NO Hacer",
        "red_flags": "Señales de Alerta Crítica (911)",
        "start_timer": "Iniciar Temporizador",
        "burn_action": "Enfríe inmediatamente con agua corriente fría durante 15 a 20 minutos.",
        "chemical_action": "Lave la piel o los ojos con agua continua durante 15 minutos en la estación de lavado.",
        "cpr_action": "Llame al 911, traiga el DEA y comience RCP a 100-120 compresiones por minuto.",
        "choking_action": "Realice la maniobra de Heimlich (empujes abdominales) inmediatamente.",
        "bleeding_action": "Aplique presión firme y directa continua sobre la herida durante 5 minutos."
    },
    "hi": {
        "name": "हिन्दी (Hindi)",
        "call_emergency": "आपातकालीन सेवा को कॉल करें",
        "immediate_action": "तत्काल कार्रवाई",
        "step_by_step": "चरण-दर-चरण प्राथमिक उपचार",
        "dos": "क्या करें",
        "donts": "क्या न करें",
        "red_flags": "गंभीर खतरे के संकेत (911)",
        "start_timer": "टाइमर शुरू करें",
        "burn_action": "तुरंत 15 से 20 मिनट तक ठंडे बहते पानी से धोएं।",
        "chemical_action": "आंखों या त्वचा को आपातकालीन आईवॉश स्टेशन पर लगातार 15 मिनट तक धोएं।",
        "cpr_action": "तुरंत 911 पर कॉल करें, AED लाएं और 100-120 प्रति मिनट की गति से CPR शुरू करें।",
        "choking_action": "गले में फंसा होने पर तुरंत हीमलिच तकनीक (पेट पर दबाव) अपनाएं।",
        "bleeding_action": "घाव पर 5 मिनट तक लगातार मजबूती से सीधा दबाव बनाए रखें।"
    },
    "zh": {
        "name": "中文 (Mandarin)",
        "call_emergency": "呼叫紧急救援",
        "immediate_action": "立即行动",
        "step_by_step": "分步急救方案",
        "dos": "应当做",
        "donts": "切勿做",
        "red_flags": "危急警报信号 (911)",
        "start_timer": "启动计时器",
        "burn_action": "立即用流动的冷水冲洗至少15至20分钟。",
        "chemical_action": "在紧急洗眼器或安全淋浴下连续冲洗15分钟以上。",
        "cpr_action": "立即拨打911，获取AED除颤器，并以每分钟100-120次节奏进行心肺复苏。",
        "choking_action": "立即实施海姆立克急救法（腹部冲击法）。",
        "bleeding_action": "用干净纱布对伤口进行持续5分钟的直接用力按压止血。"
    },
    "fr": {
        "name": "Français (French)",
        "call_emergency": "Appeler les Secours",
        "immediate_action": "Action Immédiate",
        "step_by_step": "Protocole Étape par Étape",
        "dos": "À Faire",
        "donts": "À Ne Pas Faire",
        "red_flags": "Signes d'Alerte Majeurs (911)",
        "start_timer": "Démarrer le Minuteur",
        "burn_action": "Refroidir immédiatement sous l'eau courante fraîche pendant 15 à 20 minutes.",
        "chemical_action": "Rincer les yeux ou la peau au lave-yeux d'urgence pendant 15 minutes en continu.",
        "cpr_action": "Appeler le 911 / SAMU, apporter un DAE et débuter le massage cardiaque (100-120 bpm).",
        "choking_action": "Pratiquer immédiatement la méthode de Heimlich (compressions abdominales).",
        "bleeding_action": "Appliquer une pression ferme et directe sur la plaie pendant au moins 5 minutes."
    },
    "ar": {
        "name": "العربية (Arabic)",
        "call_emergency": "اتصل بالطوارئ",
        "immediate_action": "الإجراء الفوري",
        "step_by_step": "بروتوكول الإسعافات خطوة بخطوة",
        "dos": "ما يجب فعله",
        "donts": "ما يُحظر فعله",
        "red_flags": "علامات الخطر الشديد (911)",
        "start_timer": "بدء المؤقت",
        "burn_action": "برد الحرق فوراً بماء جارٍ بارد لمدة 15 إلى 20 دقيقة متواصلة.",
        "chemical_action": "اغسل العين أو الجلد في محطة غسيل الطوارئ بماء متدفق لمدة 15 دقيقة.",
        "cpr_action": "اتصل بالإسعاف فوراً، أحضر جهاز الصدمات (AED) وابدأ الإنعاش القلبي 100-120 ضغطة/دقيقة.",
        "choking_action": "قم بإجراء مناورة هيمليك (ضغطات البطن السريعة) فوراً للشخص الغاص.",
        "bleeding_action": "اضغط مباشرة وبقوة وبشكل مستمر على الجرح لمدة 5 دقائق على الأقل."
    },
    "de": {
        "name": "Deutsch (German)",
        "call_emergency": "Notruf wählen",
        "immediate_action": "Sofortmaßnahme",
        "step_by_step": "Schritt-für-Schritt-Protokoll",
        "dos": "Richtiges Verhalten",
        "donts": "Zu Vermeiden",
        "red_flags": "Kritische Warnzeichen (112/911)",
        "start_timer": "Timer starten",
        "burn_action": "Sofort mit kühlem fließendem Wasser für mindestens 15 bis 20 Minuten kühlen.",
        "chemical_action": "Betroffene Haut oder Augen sofort 15 Minuten lang an der Notdusche spülen.",
        "cpr_action": "Notruf absetzen, AED holen und Herzdruckmassage mit 100-120 BPM starten.",
        "choking_action": "Sofort das Heimlich-Manöver (Oberbauchkompressionen) durchführen.",
        "bleeding_action": "Wunde mindestens 5 Minuten lang mit direktem, festem Druck abdrücken."
    }
}
