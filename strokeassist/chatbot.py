import re

# Define a knowledge base for the chatbot
stroke_knowledge = {
    "what is stroke": 
        "A stroke occurs when blood supply to part of the brain is interrupted or reduced, "
        "preventing brain tissue from getting oxygen and nutrients. Brain cells begin to die "
        "within minutes. A stroke is a medical emergency that requires immediate treatment.",
    
    "types of stroke": 
        "There are three main types of stroke: 1) Ischemic stroke - caused by a blocked artery, "
        "2) Hemorrhagic stroke - caused by a leaking or burst blood vessel, and "
        "3) Transient ischemic attack (TIA) - a temporary period of symptoms similar to a stroke.",
    
    "stroke symptoms": 
        "Remember the acronym FAST: Face drooping, Arm weakness, Speech difficulty, Time to call emergency. "
        "Other symptoms include sudden numbness, confusion, trouble seeing, trouble walking, "
        "severe headache with no known cause.",
    
    "stroke risk factors": 
        "Major risk factors include high blood pressure, smoking, diabetes, high cholesterol, obesity, "
        "physical inactivity, heavy alcohol use, family history, age (risk increases with age), "
        "and certain medical conditions like atrial fibrillation.",
    
    "stroke prevention": 
        "To prevent stroke: control blood pressure, manage diabetes, maintain healthy cholesterol levels, "
        "quit smoking, maintain a healthy weight, exercise regularly, eat a diet rich in fruits and vegetables, "
        "limit alcohol consumption, and treat obstructive sleep apnea if present.",
    
    "stroke treatment": 
        "Treatment depends on type of stroke. For ischemic stroke, medicines to dissolve clots and procedures "
        "to remove clots are used. For hemorrhagic stroke, controlling blood pressure and surgery may be needed. "
        "Rehabilitation is important for recovery.",
    
    "stroke recovery": 
        "Recovery varies by person and stroke severity. Rehabilitation can include physical therapy, "
        "occupational therapy, speech therapy, and psychological support. Recovery can continue for months or years.",
    
    "stroke statistics": 
        "Stroke is a leading cause of death and serious long-term disability. "
        "Approximately 795,000 people in the United States have a stroke each year. "
        "Someone in the United States has a stroke every 40 seconds.",
    
    "tia": 
        "A Transient Ischemic Attack (TIA) or 'mini-stroke' causes temporary symptoms similar to a stroke. "
        "While these symptoms resolve within 24 hours, a TIA is a serious warning sign and "
        "should not be ignored as it indicates a high risk for a future stroke.",
    
    "stroke in young people": 
        "While stroke risk increases with age, strokes can occur at any age. "
        "In younger people, they're often related to risk factors like high blood pressure, smoking, "
        "diabetes, obesity, heart disorders, or use of certain medications or drugs."
}

# Define greeting responses
greetings = [
    "hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening", "howdy"
]

greeting_responses = [
    "Hello! I'm your stroke information chatbot. How can I help you learn about strokes today?",
    "Hi there! I can provide information about strokes. What would you like to know?",
    "Hey! I'm here to answer your questions about strokes. What can I help you with?"
]

# Define farewell responses
farewells = [
    "bye", "goodbye", "see you", "farewell", "take care", "later", "end", "quit", "exit"
]

farewell_responses = [
    "Goodbye! Remember to take care of your health.",
    "Farewell! If you have more questions about strokes later, I'll be here.",
    "Take care! Remember the FAST acronym for stroke symptoms: Face drooping, Arm weakness, Speech difficulty, Time to call emergency."
]

# Define thank you responses
thanks = [
    "thank you", "thanks", "thank", "appreciate", "grateful"
]

thank_responses = [
    "You're welcome! Is there anything else you'd like to know about strokes?",
    "Happy to help! Do you have any other questions about stroke prevention or symptoms?",
    "No problem! Remember that awareness is key in stroke prevention."
]

def get_chatbot_response(message):
    """
    Generate a response to the user's message
    """
    message = message.lower().strip()
    
    # Check for greetings
    if any(greeting in message for greeting in greetings):
        import random
        return random.choice(greeting_responses)
    
    # Check for farewells
    if any(farewell in message for farewell in farewells):
        import random
        return random.choice(farewell_responses)
    
    # Check for thank you
    if any(thank in message for thank in thanks):
        import random
        return random.choice(thank_responses)
    
    # Check if any of the knowledge base keys are in the message
    for key, response in stroke_knowledge.items():
        if key in message or any(word in message for word in key.split()):
            return response
    
    # Default response for queries about stroke
    if "stroke" in message:
        return ("I'm not sure I understand your question about strokes. "
                "You can ask me about stroke types, symptoms, risk factors, prevention, "
                "treatment, recovery, or statistics.")
    
    # Default response
    return ("I'm here to provide information about strokes. You can ask me about stroke types, "
            "symptoms, risk factors, prevention, treatment, recovery, or statistics.")