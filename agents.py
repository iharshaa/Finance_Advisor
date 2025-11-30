"""
agents.py - LangChain Multi-Agent System for Hindi Finance Advisory
=====================================================================

LangChain-powered multi-agent system with message-based interactions.
Uses LangChain's message types for structured communication.

Classes:
- Agent: Base LangChain agent with message handling
- AdvisorAgent: सलाहकार - Initial financial advisor
- RiskAnalystAgent: जोखिम विश्लेषक - Risk analysis
- PlannerAgent: योजनाकर्त्ता - Final planning

Functions:
- run_multi_agent_flow(): Orchestrate agents with LangChain
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any
from datetime import datetime
from langchain_core.messages import HumanMessage, SystemMessage


@dataclass
class Agent:
    """
    Base agent class for Hindi-speaking financial agents.
    
    All agents inherit from this class and override the analyze() method.
    Each agent maintains conversation history and speaks only in Hindi.
    
    Attributes:
        role: Agent's role in Hindi (e.g., "वित्तीय सलाहकार")
        llm: Language model instance
        conversation_history: List of all interactions
        system_prompt: Base instructions for the agent
    """
    role: str
    llm: Any
    conversation_history: List[Dict] = field(default_factory=list)
    system_prompt: str = ""
    
    def __post_init__(self):
        """Set default system prompt after initialization"""
        if not self.system_prompt:
            self.system_prompt = f"आप एक {self.role} हैं। केवल हिंदी में उत्तर दें।"
    
    def respond(self, prompt: str, context: str = "") -> str:
        """
        Generate Hindi response using LangChain messages.
        
        Args:
            prompt: The question/task for the agent
            context: Additional context or instructions
        
        Returns:
            Agent's response in Hindi
        """
        # Build messages using LangChain message types
        system_message = SystemMessage(content=f"""
नियम: केवल देवनागरी में और सिर्फ़ हिंदी में उत्तर दें। अंग्रेजी का उपयोग न करें।

{self.system_prompt}

{context}
""")
        
        human_message = HumanMessage(content=f"""
प्रश्न: {prompt}

उत्तर (केवल हिंदी में):
""")
        
        try:
            # Invoke LangChain LLM with messages
            llm_response = self.llm.invoke([system_message, human_message])
            
            # Extract content from LangChain response
            if hasattr(llm_response, 'content'):
                response = llm_response.content
            else:
                response = str(llm_response)
            
            # Store in conversation history
            self.conversation_history.append({
                "role": self.role,
                "prompt": prompt,
                "context": context,
                "response": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return response.strip()
        
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            print(f"❌ Agent Error Details:\n{error_detail}")
            error_msg = f"त्रुटि: {str(e)}"
            self.conversation_history.append({
                "role": self.role,
                "error": str(e),
                "traceback": error_detail,
                "timestamp": datetime.now().isoformat()
            })
            return error_msg


class AdvisorAgent(Agent):
    """
    सलाहकार (Advisor Agent)
    
    The first agent in the pipeline. Provides initial financial advice
    based on user's income, target, and risk profile.
    
    Responsibilities:
    - Assess if goal is achievable
    - Suggest investment types
    - Recommend saving ratios
    """
    
    def __init__(self, llm):
        super().__init__(
            role="वित्तीय सलाहकार",
            llm=llm,
            system_prompt="आप एक अनुभवी वित्तीय सलाहकार हैं जो भारतीय निवेशकों को सलाह देते हैं।"
        )
    
    def analyze(self, user_data: Dict, sip_calc: Dict) -> str:
        """
        Provide initial financial advice in Hindi.
        
        Args:
            user_data: User's financial information
            sip_calc: SIP calculation results
        
        Returns:
            Advisor's suggestions in Hindi
        """
        prompt = f"""
उपयोगकर्ता की जानकारी:
- मासिक आय: ₹{user_data['monthly_income']:,}
- लक्ष्य राशि: ₹{user_data['target_amount']:,}
- समय सीमा: {user_data['years']} वर्ष
- जोखिम प्रोफाइल: {user_data['risk_profile']}

गणना परिणाम:
- आवश्यक मासिक SIP: ₹{sip_calc['monthly_sip']:,}
- कुल निवेश: ₹{sip_calc['total_investment']:,}
- अपेक्षित रिटर्न: ₹{sip_calc['expected_returns']:,}

कृपया उपयोगकर्ता को प्रारंभिक वित्तीय सलाह दें। निम्नलिखित बातों का उल्लेख करें:
1. क्या यह लक्ष्य उनकी आय के अनुसार संभव है?
2. किस प्रकार के निवेश की सिफारिश करेंगे?
3. बचत और खर्च का अनुपात क्या होना चाहिए?

संक्षिप्त और स्पष्ट उत्तर दें।
"""
        
        context = "भारतीय बाजार और निवेश विकल्पों के बारे में सलाह दें।"
        return self.respond(prompt, context)


class RiskAnalystAgent(Agent):
    """
    जोखिम विश्लेषक (Risk Analyst Agent)
    
    The second agent in the pipeline. Analyzes the advisor's suggestions
    and identifies potential risks.
    
    Responsibilities:
    - Assess financial feasibility
    - Identify risks
    - Suggest safer alternatives
    - Recommend emergency fund
    """
    
    def __init__(self, llm):
        super().__init__(
            role="जोखिम विश्लेषक",
            llm=llm,
            system_prompt="आप एक जोखिम विश्लेषण विशेषज्ञ हैं जो वित्तीय सुरक्षा पर ध्यान देते हैं।"
        )
    
    def analyze(self, user_data: Dict, sip_calc: Dict, advisor_suggestion: str) -> str:
        """
        Analyze risks and provide safer alternatives.
        
        Args:
            user_data: User's financial information
            sip_calc: SIP calculation results
            advisor_suggestion: The advisor's recommendations
        
        Returns:
            Risk analysis and suggestions in Hindi
        """
        # Calculate SIP to income ratio
        sip_to_income_ratio = (sip_calc['monthly_sip'] / user_data['monthly_income']) * 100
        
        prompt = f"""
सलाहकार का सुझाव:
{advisor_suggestion}

वित्तीय विश्लेषण:
- आय का {sip_to_income_ratio:.1f}% SIP में जाएगा
- जोखिम स्तर: {user_data['risk_profile']}
- निवेश अवधि: {user_data['years']} वर्ष
- मासिक आय: ₹{user_data['monthly_income']:,}
- आवश्यक SIP: ₹{sip_calc['monthly_sip']:,}

कृपया जोखिम विश्लेषण करें:
1. क्या यह योजना सुरक्षित है?
2. क्या कोई जोखिम हैं?
3. सुरक्षित विकल्प क्या हैं?
4. आपातकालीन निधि की सिफारिश (आय का 6-12 महीने)

संक्षिप्त और स्पष्ट उत्तर दें।
"""
        
        context = "वित्तीय सुरक्षा और जोखिम प्रबंधन पर ध्यान दें।"
        return self.respond(prompt, context)


class PlannerAgent(Agent):
    """
    योजनाकर्त्ता (Planner Agent)
    
    The final agent in the pipeline. Creates a comprehensive,
    structured financial plan based on inputs from previous agents.
    
    Responsibilities:
    - Create monthly budget breakdown
    - Define investment strategy
    - Create 3/6/12-month action plan
    - Add risk disclaimer
    """
    
    def __init__(self, llm):
        super().__init__(
            role="वित्तीय योजनाकर्त्ता",
            llm=llm,
            system_prompt="आप एक व्यापक वित्तीय योजनाकार हैं जो व्यावहारिक योजनाएं बनाते हैं।"
        )
    
    def create_plan(self, user_data: Dict, sip_calc: Dict, 
                   advisor_advice: str, risk_analysis: str) -> str:
        """
        Create final structured financial plan.
        
        Args:
            user_data: User's financial information
            sip_calc: SIP calculation results
            advisor_advice: Advisor's recommendations
            risk_analysis: Risk analyst's findings
        
        Returns:
            Complete financial plan in Hindi
        """
        prompt = f"""
सलाहकार की राय:
{advisor_advice}

जोखिम विश्लेषक की राय:
{risk_analysis}

उपयोगकर्ता डेटा:
- मासिक आय: ₹{user_data['monthly_income']:,}
- लक्ष्य: ₹{user_data['target_amount']:,} ({user_data['years']} वर्ष में)
- आवश्यक SIP: ₹{sip_calc['monthly_sip']:,}
- जोखिम स्तर: {user_data['risk_profile']}

कृपया एक विस्तृत वित्तीय योजना बनाएं जिसमें शामिल हो:

1. मासिक बजट विभाजन (आय का प्रतिशत):
   - आवश्यक खर्च (किराया, भोजन, बिल): __% (₹__)
   - बचत/निवेश (SIP): __% (₹__)
   - आपातकालीन निधि: __% (₹__)
   - विवेकाधीन खर्च: __% (₹__)

2. निवेश रणनीति:
   - SIP राशि: ₹{sip_calc['monthly_sip']:,}
   - निवेश प्रकार (इक्विटी/डेट/हाइब्रिड)
   - अन्य निवेश साधन

3. कार्य योजना:
   - पहले 3 महीने में क्या करें
   - 6 महीने की योजना
   - 12 महीने की योजना

4. जोखिम चेतावनी

संक्षिप्त, स्पष्ट और व्यावहारिक योजना बनाएं।
"""
        
        context = "एक संरचित और कार्यान्वयन योग्य योजना बनाएं।"
        return self.respond(prompt, context)


def run_multi_agent_flow(
    llm,
    user_data: Dict[str, Any],
    sip_calc: Dict[str, float]
) -> Tuple[str, str, str]:
    """
    Orchestrate the multi-agent workflow.
    
    This function runs all three agents sequentially:
    1. Advisor provides initial suggestions
    2. Risk Analyst evaluates and suggests safer alternatives
    3. Planner creates final structured plan
    
    Args:
        llm: Language model instance
        user_data: Dictionary with user inputs:
            - monthly_income: float
            - target_amount: float
            - years: int
            - risk_profile: str
            - annual_return: float (optional)
            - notes: str (optional)
        sip_calc: Dictionary with SIP calculations:
            - monthly_sip: float
            - total_investment: float
            - expected_returns: float
            - total_value: float
    
    Returns:
        Tuple of (advisor_output, risk_output, planner_output)
    
    Example:
        >>> from llm import get_llm
        >>> from calc import calculate_sip
        >>> 
        >>> llm = get_llm()
        >>> user_data = {
        ...     'monthly_income': 50000,
        ...     'target_amount': 1000000,
        ...     'years': 5,
        ...     'risk_profile': 'मध्यम जोखिम'
        ... }
        >>> sip_calc = calculate_sip(1000000, 5, 12.0)
        >>> 
        >>> advisor, risk, planner = run_multi_agent_flow(llm, user_data, sip_calc)
        >>> print(advisor)  # Advisor's suggestions in Hindi
        >>> print(risk)     # Risk analysis in Hindi
        >>> print(planner)  # Final plan in Hindi
    """
    # Initialize all agents
    advisor = AdvisorAgent(llm)
    risk_analyst = RiskAnalystAgent(llm)
    planner = PlannerAgent(llm)
    
    # Step 1: Advisor provides initial analysis
    advisor_output = advisor.analyze(user_data, sip_calc)
    
    # Step 2: Risk Analyst evaluates advisor's suggestions
    risk_output = risk_analyst.analyze(user_data, sip_calc, advisor_output)
    
    # Step 3: Planner creates final comprehensive plan
    planner_output = planner.create_plan(user_data, sip_calc, advisor_output, risk_output)
    
    return advisor_output, risk_output, planner_output


def get_agent_conversation_history(agent: Agent) -> List[Dict]:
    """
    Get the full conversation history of an agent.
    
    Args:
        agent: Agent instance
    
    Returns:
        List of conversation entries
    """
    return agent.conversation_history


if __name__ == "__main__":
    # Test the multi-agent system
    print("Testing Multi-Agent System...\n")
    
    try:
        from llm import get_llm
        from calc import calculate_sip
        
        # Initialize LLM
        print("Initializing LLM...")
        llm = get_llm()
        
        # Test data
        user_data = {
            'monthly_income': 50000,
            'target_amount': 1000000,
            'years': 5,
            'risk_profile': 'मध्यम जोखिम (Medium)',
            'annual_return': 12.0
        }
        
        # Calculate SIP
        print("Calculating SIP...")
        sip_calc = calculate_sip(1000000, 5, 12.0)
        print(f"Required SIP: ₹{sip_calc['monthly_sip']:,}\n")
        
        # Run multi-agent flow
        print("Running multi-agent flow...\n")
        advisor_out, risk_out, planner_out = run_multi_agent_flow(llm, user_data, sip_calc)
        
        print("=" * 60)
        print("ADVISOR OUTPUT:")
        print("=" * 60)
        print(advisor_out)
        
        print("\n" + "=" * 60)
        print("RISK ANALYST OUTPUT:")
        print("=" * 60)
        print(risk_out)
        
        print("\n" + "=" * 60)
        print("PLANNER OUTPUT:")
        print("=" * 60)
        print(planner_out)
        
        print("\n✅ Multi-agent flow completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure you have:")
        print("1. Set up .env with HUGGINGFACEHUB_API_TOKEN")
        print("2. Installed all dependencies")
