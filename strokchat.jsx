import { useState, useRef, useEffect } from 'react';

export default function StrokeAssistBot() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm StrokeAssist, your healthcare companion for stroke information. How can I help you today?",
      sender: 'bot'
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  // Knowledge base for stroke information
  const strokeKnowledge = {
    // Symptoms and warning signs
    symptoms: [
      "Sudden numbness or weakness in the face, arm, or leg, especially on one side of the body",
      "Sudden confusion, trouble speaking, or difficulty understanding speech",
      "Sudden trouble seeing in one or both eyes",
      "Sudden trouble walking, dizziness, loss of balance, or lack of coordination",
      "Sudden severe headache with no known cause"
    ],
    
    // FAST warning signs
    fast: [
      "F - Face Drooping: Does one side of the face droop or is it numb?",
      "A - Arm Weakness: Is one arm weak or numb?",
      "S - Speech Difficulty: Is speech slurred, are they unable to speak, or are they hard to understand?",
      "T - Time to Call Emergency Services: If someone shows any of these symptoms, even if they go away, call emergency services and get them to the hospital immediately"
    ],
    
    // Types of strokes
    types: [
      "Ischemic Stroke: Caused by a blockage in a blood vessel supplying the brain",
      "Hemorrhagic Stroke: Caused by bleeding in or around the brain",
      "Transient Ischemic Attack (TIA): Sometimes called a 'mini-stroke', these are temporary blockages"
    ],
    
    // Risk factors
    riskFactors: [
      "High blood pressure",
      "Smoking",
      "Diabetes",
      "High cholesterol",
      "Physical inactivity and obesity",
      "Heart disease",
      "Age (risk increases with age)",
      "Family history of stroke",
      "Previous stroke or TIA"
    ],
    
    // Prevention measures
    prevention: [
      "Manage high blood pressure",
      "Control cholesterol and blood sugar",
      "Quit smoking",
      "Maintain a healthy weight",
      "Exercise regularly (at least 30 minutes daily)",
      "Eat a diet rich in fruits, vegetables, whole grains and low in saturated fat",
      "Limit alcohol consumption",
      "Take medication as prescribed by your doctor"
    ],
    
    // Treatment options
    treatment: [
      "Emergency procedures: Clot-busting drugs (for ischemic stroke) or surgery (for hemorrhagic stroke)",
      "Medication: Blood thinners, anti-hypertensives, cholesterol-lowering drugs",
      "Rehabilitation: Physical therapy, occupational therapy, speech therapy",
      "Lifestyle changes: Diet, exercise, smoking cessation"
    ],
    
    // Recovery information
    recovery: [
      "Recovery time varies widely depending on stroke severity and location",
      "Most recovery happens in the first 3-6 months, but can continue for years",
      "Rehabilitation is crucial for maximum recovery",
      "Support from family and healthcare providers plays a key role",
      "Depression is common after stroke and should be addressed",
      "Setting realistic goals and celebrating small victories is important"
    ],
    
    // Caregiving tips
    caregiving: [
      "Educate yourself about stroke and recovery",
      "Create a safe home environment",
      "Help with medication management",
      "Encourage independence when possible",
      "Assist with rehabilitation exercises",
      "Watch for signs of depression or frustration",
      "Take care of your own health and seek support when needed"
    ]
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const processUserInput = (userInput) => {
    // Convert to lowercase for easier matching
    const input = userInput.toLowerCase();
    
    // Check for different types of questions and provide appropriate responses
    if (input.includes('symptom') || input.includes('warning sign') || input.includes('sign') || 
        input.includes('how do i know') || input.includes('how to tell')) {
      return {
        text: `The warning signs of a stroke include:\n\n${strokeKnowledge.symptoms.join('\n\n')}`,
        sender: 'bot'
      };
    }
    else if (input.includes('fast')) {
      return {
        text: `The FAST method is a quick way to identify stroke symptoms:\n\n${strokeKnowledge.fast.join('\n\n')}`,
        sender: 'bot'
      };
    }
    else if (input.includes('type') || input.includes('kind')) {
      return {
        text: `There are three main types of stroke:\n\n${strokeKnowledge.types.join('\n\n')}`,
        sender: 'bot'
      };
    }
    else if (input.includes('risk') || input.includes('cause')) {
      return {
        text: `Common risk factors for stroke include:\n\n${strokeKnowledge.riskFactors.join('\n\n')}`,
        sender: 'bot'
      };
    }
    else if (input.includes('prevent') || input.includes('avoid') || input.includes('reduce risk')) {
      return {
        text: `Here are ways to prevent stroke or reduce your risk:\n\n${strokeKnowledge.prevention.join('\n\n')}`,
        sender: 'bot'
      };
    }
    else if (input.includes('treat') || input.includes('medicine') || input.includes('drug') || 
             input.includes('surgery') || input.includes('therapy')) {
      return {
        text: `Stroke treatment options include:\n\n${strokeKnowledge.treatment.join('\n\n')}`,
        sender: 'bot'
      };
    }
    else if (input.includes('recover') || input.includes('healing') || input.includes('getting better')) {
      return {
        text: `Important information about stroke recovery:\n\n${strokeKnowledge.recovery.join('\n\n')}`,
        sender: 'bot'
      };
    }
    else if (input.includes('care') || input.includes('help someone') || input.includes('family member')) {
      return {
        text: `Tips for caregivers supporting stroke survivors:\n\n${strokeKnowledge.caregiving.join('\n\n')}`,
        sender: 'bot'
      };
    }
    else if (input.includes('hello') || input.includes('hi') || input.includes('hey')) {
      return {
        text: "Hello! I'm here to provide information about stroke prevention, symptoms, treatment, and recovery. How can I help you today?",
        sender: 'bot'
      };
    }
    else if (input.includes('thank')) {
      return {
        text: "You're welcome! I'm here to help. Is there anything else you'd like to know about stroke?",
        sender: 'bot'
      };
    }
    else if (input.includes('bye') || input.includes('goodbye')) {
      return {
        text: "Take care! Remember to prioritize your health and don't hesitate to reach out if you have more questions about stroke.",
        sender: 'bot'
      };
    }
    else if (input.includes('blood pressure') || input.includes('hypertension')) {
      return {
        text: "High blood pressure is the most significant controllable risk factor for stroke. Regular monitoring and management through medication, diet, exercise, and stress reduction are essential. Aim to keep your blood pressure below 120/80 mmHg.",
        sender: 'bot'
      };
    }
    else if (input.includes('diet') || input.includes('food') || input.includes('eat')) {
      return {
        text: "A heart-healthy diet can reduce stroke risk. Focus on:\n\n- Fruits and vegetables\n- Whole grains\n- Lean proteins\n- Low-fat dairy\n- Limited salt (sodium)\n- Limited saturated and trans fats\n\nThe Mediterranean and DASH diets are particularly beneficial for stroke prevention.",
        sender: 'bot'
      };
    }
    else if (input.includes('exercise') || input.includes('physical activity') || input.includes('workout')) {
      return {
        text: "Regular physical activity reduces stroke risk by:\n\n- Lowering blood pressure\n- Improving cholesterol levels\n- Managing weight\n- Controlling diabetes\n\nAim for at least 150 minutes of moderate-intensity exercise per week (about 30 minutes daily, 5 days a week).",
        sender: 'bot'
      };
    }
    else {
      return {
        text: "I'm here to provide information about stroke. You can ask me about symptoms, risk factors, prevention, treatment, recovery, or caregiving. How can I assist you with stroke-related information?",
        sender: 'bot'
      };
    }
  };

  const handleSubmit = () => {
    if (input.trim() === '') return;
    
    // Add user message
    const userMessage = {
      id: messages.length + 1,
      text: input,
      sender: 'user'
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);
    
    // Simulate bot thinking time
    setTimeout(() => {
      const botResponse = processUserInput(input);
      botResponse.id = messages.length + 2;
      
      setMessages(prev => [...prev, botResponse]);
      setIsTyping(false);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-screen max-w-md mx-auto bg-gray-100 shadow-xl rounded-lg overflow-hidden">
      <div className="bg-blue-600 px-4 py-3 flex items-center">
        <div className="bg-white p-1 rounded-full">
          <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
          </svg>
        </div>
        <div className="ml-3">
          <h1 className="text-white font-bold text-lg">StrokeAssist Bot</h1>
          <p className="text-blue-200 text-sm">Your stroke healthcare companion</p>
        </div>
      </div>
      
      <div className="flex-1 p-4 overflow-y-auto bg-gray-50">
        <div className="space-y-4">
          {messages.map(msg => (
            <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div 
                className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                  msg.sender === 'user' 
                    ? 'bg-blue-600 text-white rounded-br-none' 
                    : 'bg-gray-200 text-gray-800 rounded-bl-none'
                }`}
              >
                <p className="whitespace-pre-line">{msg.text}</p>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="bg-gray-200 px-4 py-2 rounded-lg rounded-bl-none">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce"></div>
                  <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce delay-100"></div>
                  <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce delay-200"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>
      
      <div className="bg-white px-4 py-3 border-t flex">
        <input
          type="text"
          placeholder="Ask about stroke symptoms, prevention, etc..."
          className="flex-1 bg-gray-100 rounded-full px-6 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              handleSubmit();
            }
          }}
        />
        <button 
          onClick={handleSubmit}
          className="ml-3 bg-blue-600 text-white rounded-full p-2 hover:bg-blue-700 transition focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
          </svg>
        </button>
      </div>
    </div>
  );
}