"""
Interview service for the server-driven questionnaire.

This service manages the step-by-step interview flow, returning
one question at a time based on previous answers.
"""

from typing import Optional, Dict, Any, List
from ..schemas.responses import (
    QuestionResponse,
    QuestionOption,
    InterviewStateResponse,
)


# =============================================================================
# INTERVIEW QUESTIONS DEFINITION
# Questions are ordered by the interview flow for early exit optimization
# =============================================================================

QUESTIONS: List[QuestionResponse] = [
    # Q1: VAT Registration (hard stop)
    QuestionResponse(
        id="vat_registration",
        type="boolean",
        question="Are you registered for VAT?",
        question_az="ƏDV qeydiyyatınız varmı?",
        tooltip="VAT-registered taxpayers cannot use the simplified tax regime. If you're VAT registered, you must use the general tax system.",
        tooltip_az="ƏDV qeydiyyatında olan vergi ödəyiciləri sadələşdirilmiş vergi rejimindən istifadə edə bilməzlər.",
        legal_basis="Tax Code 218.1.1",
        required=True,
    ),

    # Q2: Route selection (fast pass)
    QuestionResponse(
        id="route_selection",
        type="multi_select",
        question="Select any activities that apply to you:",
        question_az="Aşağıdakı fəaliyyətlərdən hansılar sizə aiddir?",
        tooltip="These special categories are automatically eligible for simplified tax regardless of turnover threshold.",
        tooltip_az="Bu xüsusi kateqoriyalar dövriyyə həddindən asılı olmayaraq avtomatik olaraq sadələşdirilmiş vergiyə uyğundur.",
        legal_basis="Tax Code 218.4",
        options=[
            QuestionOption(
                value="route_auto_transport",
                label="Passenger transport/taxi",
                label_az="Sərnişin daşıma/taksi",
                description="Including taxi services and regular passenger transport",
            ),
            QuestionOption(
                value="route_auto_betting_lottery",
                label="Betting/lottery",
                label_az="Mərc/lotereya",
                description="Betting or lottery organization activities",
            ),
            QuestionOption(
                value="route_auto_property",
                label="Transfer/sale of own real estate",
                label_az="Özümə məxsus daşınmaz əmlakın satışı/ötürülməsi",
                description="Selling or transferring property you own",
            ),
            QuestionOption(
                value="route_auto_fixed_220_10",
                label="Fixed activity under 220.10 without employees",
                label_az="220.10 üzrə işçisi olmayan sabit fəaliyyət",
                description="Specific fixed activities listed in Article 220.10",
            ),
            QuestionOption(
                value="route_auto_land",
                label="Sale/transfer of own land",
                label_az="Özümə məxsus torpağın satışı/ötürülməsi",
                description="Selling or transferring land you own",
            ),
        ],
        required=False,
    ),

    # Q2.C (PATCH 1): Property exemption subquestion
    QuestionResponse(
        id="property_exemption",
        type="select",
        question="Is this residential property exempt under Tax Code 218-1.1.5?",
        question_az="Bu yaşayış sahəsi Vergi Məcəlləsinin 218-1.1.5-ci maddəsinə əsasən vergidən azaddırmı?",
        tooltip="Certain property transfers are completely exempt from simplified tax.",
        tooltip_az="Müəyyən əmlak köçürmələri sadələşdirilmiş vergidən tam azaddır.",
        legal_basis="Tax Code 218-1.1.5",
        condition="route_auto_property == true",
        options=[
            QuestionOption(
                value="registered_3yr",
                label="I was registered at that address for at least 3 calendar years",
                label_az="Həmin ünvanda ən azı 3 təqvim ili qeydiyyatda olmuşam",
                description="218-1.1.5.1: Registered residence for 3+ years",
            ),
            QuestionOption(
                value="proof_3yr_one_home",
                label="I can prove I lived there 3+ years AND I own only one residential property",
                label_az="3+ il yaşadığımı sübut edə bilirəm VƏ yalnız bir yaşayış sahəm var",
                description="218-1.1.5.1-1: Proof of residence via utility subscriber certificates",
            ),
            QuestionOption(
                value="family_gift_inheritance",
                label="This is a gift/inheritance from a family member",
                label_az="Bu ailə üzvündən bağışlama və ya vərəsəlikdir",
                description="Tax Code 102.1.3.2 referenced by 218-1.1.5.2",
            ),
            QuestionOption(
                value="none",
                label="None of the above apply",
                label_az="Yuxarıdakılardan heç biri uyğun deyil",
                description="30 m² exemption will still apply to residential property",
            ),
        ],
        required=True,
    ),

    # Q2.C.2: Property details
    QuestionResponse(
        id="property_details",
        type="object",
        question="Enter property transfer details:",
        question_az="Əmlak köçürməsi detallarını daxil edin:",
        legal_basis="Tax Code 220.8",
        condition="route_auto_property == true && property_exemption == 'none'",
        required=True,
    ),

    # Q3: Trade/catering activity
    QuestionResponse(
        id="trade_catering",
        type="multi_select",
        question="Are you engaged in trade and/or public catering?",
        question_az="Ticarət və/və ya ictimai iaşə ilə məşğulsunuzmu?",
        tooltip="Trade and catering activities above 200k turnover have different tax rates.",
        tooltip_az="200 min manatdan yuxarı dövriyyəsi olan ticarət və iaşə fəaliyyətlərinin fərqli vergi dərəcələri var.",
        legal_basis="Tax Code 218.1.2, 220.1-1",
        options=[
            QuestionOption(
                value="does_trade",
                label="Trade (retail or wholesale)",
                label_az="Ticarət (pərakəndə və ya topdan)",
            ),
            QuestionOption(
                value="does_catering",
                label="Public catering",
                label_az="İctimai iaşə",
            ),
        ],
        required=False,
    ),

    # Q4: Turnover (PATCH 2)
    QuestionResponse(
        id="turnover",
        type="object",
        question="Enter your turnover details for the last 12 months:",
        question_az="Son 12 ay üçün dövriyyə detallarınızı daxil edin:",
        tooltip="The 200,000 AZN test uses VAT-taxable ('vergi tutulan') operations under VAT chapter rules. Do NOT include VAT-exempt streams such as financial services (Art 164.1.2) or textbook production-related publishing/printing (Art 164.1.8). POS non-cash turnover from retail/services to unregistered persons is counted with coefficient 0.5.",
        tooltip_az="200.000 AZN testi ƏDV fəsli qaydaları əsasında ƏDV-yə cəlb olunan ('vergi tutulan') əməliyyatlardan istifadə edir. Maliyyə xidmətləri (Maddə 164.1.2) və ya dərslik istehsalı ilə bağlı nəşriyyat/çap (Maddə 164.1.8) kimi ƏDV-dən azad axınları DAXİL ETMƏYİN. Qeydiyyatsız şəxslərə pərakəndə satış/xidmət üzrə POS nağdsız dövriyyə 0,5 əmsalı ilə hesablanır.",
        legal_basis="Tax Code 218.1.1, 218.1-1, 164",
        required=True,
    ),

    # Q5: Excise/mandatory marking production
    QuestionResponse(
        id="excise_production",
        type="boolean",
        question="Do you produce excise or mandatory-label goods?",
        question_az="Aksizli və ya mütləq markalanan mallar istehsal edirsinizmi?",
        tooltip="Producers of excise goods (alcohol, tobacco, etc.) or goods requiring mandatory labeling cannot use simplified tax.",
        tooltip_az="Aksizli malların (spirtli içkilər, tütün və s.) və ya mütləq markalanma tələb edən malların istehsalçıları sadələşdirilmiş vergidən istifadə edə bilməzlər.",
        legal_basis="Tax Code 218.5.1",
        required=True,
    ),

    # Q6: Financial sector
    QuestionResponse(
        id="financial_sector",
        type="multi_select",
        question="Are you any of the following?",
        question_az="Aşağıdakılardan birisinizmi?",
        legal_basis="Tax Code 218.5.2",
        options=[
            QuestionOption(
                value="is_credit_org",
                label="Credit organization",
                label_az="Kredit təşkilatı",
            ),
            QuestionOption(
                value="is_insurance_market_participant",
                label="Insurance market professional participant",
                label_az="Sığorta bazarının peşəkar iştirakçısı",
            ),
            QuestionOption(
                value="is_investment_fund",
                label="Investment fund or manager",
                label_az="İnvestisiya fondu və ya meneceri",
            ),
            QuestionOption(
                value="is_securities_licensed",
                label="Securities market licensed person",
                label_az="Qiymətli kağızlar bazarının lisenziyalı iştirakçısı",
            ),
            QuestionOption(
                value="is_pawnshop",
                label="Pawnshop",
                label_az="Lombard",
            ),
        ],
        required=False,
    ),

    # Q7: Pension fund
    QuestionResponse(
        id="pension_fund",
        type="boolean",
        question="Are you a non-state pension fund?",
        question_az="Qeyri-dövlət pensiya fondusunuzmu?",
        legal_basis="Tax Code 218.5.3",
        required=True,
    ),

    # Q8: Rental/royalty income
    QuestionResponse(
        id="rental_royalty",
        type="multi_select",
        question="Do you earn any of the following types of income?",
        question_az="Aşağıdakı gəlir növlərindən hər hansı birini əldə edirsinizmi?",
        legal_basis="Tax Code 218.5.4",
        options=[
            QuestionOption(
                value="has_rental_income",
                label="Rental income",
                label_az="İcarə gəliri",
            ),
            QuestionOption(
                value="has_royalty_income",
                label="Royalty income",
                label_az="Royalti gəliri",
            ),
        ],
        required=False,
    ),

    # Q9: Natural monopoly
    QuestionResponse(
        id="natural_monopoly",
        type="boolean",
        question="Are you a designated natural monopoly?",
        question_az="Təbii inhisarçı olaraq müəyyən edilmisinizmi?",
        tooltip="Natural monopolies (utilities, etc.) cannot use simplified tax.",
        tooltip_az="Təbii inhisarçılar (kommunal xidmətlər və s.) sadələşdirilmiş vergidən istifadə edə bilməzlər.",
        legal_basis="Tax Code 218.5.5",
        required=True,
    ),

    # Q10: Fixed assets threshold
    QuestionResponse(
        id="fixed_assets",
        type="decimal",
        question="What is your fixed assets residual value at the start of the year (AZN)?",
        question_az="İlin əvvəlinə əsas vəsaitlərinizin qalıq dəyəri nədir (AZN)?",
        tooltip="If your fixed assets residual value exceeds 1,000,000 AZN at the start of the year, you cannot use simplified tax (with some carve-outs).",
        tooltip_az="İlin əvvəlinə əsas vəsaitlərinizin qalıq dəyəri 1.000.000 AZN-dən artıq olarsa, sadələşdirilmiş vergidən istifadə edə bilməzsiniz.",
        legal_basis="Tax Code 218.5.6",
        required=True,
    ),

    # Q11: Licensed activities (PATCH 3)
    QuestionResponse(
        id="licensed_activities",
        type="multi_select",
        question="Do you perform any activity that requires a license (lisenziya)?",
        question_az="Lisenziya tələb edən hər hansı fəaliyyətlə məşğulsunuzmu?",
        tooltip="Licensed activities generally cannot use simplified tax, except for services provided under compulsory insurance contracts.",
        tooltip_az="Lisenziyalı fəaliyyətlər ümumiyyətlə sadələşdirilmiş vergidən istifadə edə bilməz, icbari sığorta müqavilələri üzrə göstərilən xidmətlər istisna olmaqla.",
        legal_basis="Tax Code 218.5.13, License Law Annex 1",
        options=[
            QuestionOption(
                value="private_medical",
                label="Private medical activity",
                label_az="Özəl tibb fəaliyyəti",
            ),
            QuestionOption(
                value="education",
                label="Education activity (universities, vocational, etc.)",
                label_az="Təhsil fəaliyyəti (universitetlər, peşə və s.)",
            ),
            QuestionOption(
                value="communications",
                label="Communications services (telecom/post)",
                label_az="Rabitə xidmətləri (telekommunikasiya/poçt)",
            ),
            QuestionOption(
                value="fire_protection",
                label="Fire protection activity",
                label_az="Yanğından mühafizə fəaliyyəti",
            ),
            QuestionOption(
                value="construction_survey",
                label="Engineering surveys (permit-required buildings)",
                label_az="Mühəndis axtarışları (icazə tələb olunan binalar)",
            ),
            QuestionOption(
                value="construction_install",
                label="Construction-installation (permit-required buildings)",
                label_az="Tikinti-quraşdırma işləri (icazə tələb olunan binalar)",
            ),
            QuestionOption(
                value="construction_design",
                label="Design (permit-required buildings)",
                label_az="Layihələndirmə (icazə tələb olunan binalar)",
            ),
            QuestionOption(
                value="other_licensed",
                label="Other licensed activity",
                label_az="Digər lisenziyalı fəaliyyət",
            ),
        ],
        required=False,
    ),

    # Q11.1: Compulsory insurance carve-out
    QuestionResponse(
        id="compulsory_insurance_carveout",
        type="boolean",
        question="Do you ONLY provide services under compulsory insurance contracts?",
        question_az="Yalnız icbari sığorta müqavilələri üzrə xidmət göstərirsinizmi?",
        tooltip="If you only provide services under compulsory insurance contracts, the licensed activity disqualification does not apply.",
        tooltip_az="Yalnız icbari sığorta müqavilələri üzrə xidmət göstərirsinizsə, lisenziyalı fəaliyyət məhdudiyyəti tətbiq edilmir.",
        legal_basis="Tax Code 218.5.13, 218.5.2-1",
        condition="licensed_activities.length > 0",
        required=True,
    ),

    # Q12: Production + employees
    QuestionResponse(
        id="production_employees",
        type="object",
        question="Production activity details:",
        question_az="İstehsal fəaliyyəti detalları:",
        tooltip="Production activities with more than 10 average quarterly employees cannot use simplified tax.",
        tooltip_az="Rüblük orta işçi sayı 10 nəfərdən çox olan istehsal fəaliyyətləri sadələşdirilmiş vergidən istifadə edə bilməz.",
        legal_basis="Tax Code 218.5.8",
        subquestions=[
            QuestionResponse(
                id="does_production",
                type="boolean",
                question="Do you conduct production activity?",
                question_az="İstehsal fəaliyyəti göstərirsinizmi?",
                required=True,
            ),
            QuestionResponse(
                id="avg_quarterly_employees",
                type="number",
                question="Average quarterly employee count:",
                question_az="Rüblük orta işçi sayı:",
                condition="does_production == true",
                required=True,
            ),
        ],
        required=True,
    ),

    # Q13: Wholesale
    QuestionResponse(
        id="wholesale",
        type="object",
        question="Wholesale trade details:",
        question_az="Topdan ticarət detalları:",
        tooltip="Wholesale trade is generally disqualified, but if e-invoiced wholesale operations are ≤30% of quarterly trade operations (excluding non-operating income), simplified tax is preserved.",
        tooltip_az="Topdan ticarət ümumiyyətlə uyğun deyil, lakin e-qaimə-faktura ilə topdan satış əməliyyatları rüblük ticarət əməliyyatlarının 30%-dən çox olmadıqda sadələşdirilmiş vergi qorunur.",
        legal_basis="Tax Code 218.5.9, 218.6.1",
        subquestions=[
            QuestionResponse(
                id="does_wholesale",
                type="boolean",
                question="Do you conduct wholesale trade?",
                question_az="Topdan ticarət edirsinizmi?",
                required=True,
            ),
            QuestionResponse(
                id="wholesale_einvoice_ratio",
                type="decimal",
                question="E-invoiced wholesale ratio (0-1):",
                question_az="E-qaimə-faktura ilə topdan satış nisbəti (0-1):",
                tooltip="Ratio of e-invoiced wholesale operations to total quarterly trade operations (excluding non-operating income)",
                condition="does_wholesale == true",
                required=True,
            ),
        ],
        required=True,
    ),

    # Q14: B2B works/services
    QuestionResponse(
        id="b2b_works_services",
        type="object",
        question="B2B works/services details:",
        question_az="B2B iş/xidmət detalları:",
        tooltip="Performing works/services for legal entities or registered individuals is generally disqualified, but if e-invoiced B2B operations are ≤30% of quarterly works/services operations (excluding non-operating income), simplified tax is preserved.",
        tooltip_az="Hüquqi şəxslərə və ya qeydiyyatda olan şəxslərə iş görülməsi/xidmət göstərilməsi ümumiyyətlə uyğun deyil, lakin e-qaimə-faktura ilə B2B əməliyyatları rüblük iş/xidmət əməliyyatlarının 30%-dən çox olmadıqda sadələşdirilmiş vergi qorunur.",
        legal_basis="Tax Code 218.5.10, 218.6.2",
        subquestions=[
            QuestionResponse(
                id="does_b2b_works_services",
                type="boolean",
                question="Do you perform works/services for legal entities or registered individuals?",
                question_az="Hüquqi şəxslərə və ya qeydiyyatda olan şəxslərə iş görür və ya xidmət göstərirsinizmi?",
                required=True,
            ),
            QuestionResponse(
                id="b2b_einvoice_ratio",
                type="decimal",
                question="E-invoiced B2B ratio (0-1):",
                question_az="E-qaimə-faktura ilə B2B nisbəti (0-1):",
                tooltip="Ratio of e-invoiced B2B operations to total quarterly works/services operations (excluding non-operating income)",
                condition="does_b2b_works_services == true",
                required=True,
            ),
        ],
        required=True,
    ),

    # Q15: Precious goods / fur
    QuestionResponse(
        id="precious_fur",
        type="multi_select",
        question="Do you sell any of the following?",
        question_az="Aşağıdakılardan hər hansı birini satırsınızmı?",
        legal_basis="Tax Code 218.5.11-218.5.12",
        options=[
            QuestionOption(
                value="sells_gold_jewelry_diamonds",
                label="Gold, jewelry, or diamonds",
                label_az="Qızıl, zərgərlik məmulatları və ya almaz",
            ),
            QuestionOption(
                value="sells_fur_leather",
                label="Fur or leather products",
                label_az="Xəz və ya dəri məmulatları",
            ),
        ],
        required=False,
    ),
]


class InterviewService:
    """
    Service for managing the server-driven interview flow.
    """

    def __init__(self):
        self.questions = QUESTIONS

    def get_questions(self) -> List[QuestionResponse]:
        """Get all interview questions."""
        return self.questions

    def get_question_by_id(self, question_id: str) -> Optional[QuestionResponse]:
        """Get a specific question by ID."""
        for q in self.questions:
            if q.id == question_id:
                return q
            # Check subquestions
            if q.subquestions:
                for sq in q.subquestions:
                    if sq.id == question_id:
                        return sq
        return None

    def get_next_question(
        self,
        answers: Dict[str, Any]
    ) -> Optional[QuestionResponse]:
        """
        Determine the next question based on current answers.

        Returns None if all questions are answered.
        """
        for question in self.questions:
            # Check if this question is already answered
            if question.id in answers:
                continue

            # Check if this question has a condition
            if question.condition:
                if not self._evaluate_condition(question.condition, answers):
                    continue

            return question

        return None

    def _evaluate_condition(
        self,
        condition: str,
        answers: Dict[str, Any]
    ) -> bool:
        """
        Evaluate a condition string against current answers.

        Simple condition parser for expressions like:
        - "route_auto_property == true"
        - "licensed_activities.length > 0"
        """
        # Simple equality check
        if " == " in condition:
            key, value = condition.split(" == ")
            key = key.strip()
            value = value.strip()

            if value == "true":
                return answers.get(key, False) is True
            elif value == "false":
                return answers.get(key, False) is False
            elif value.startswith("'") and value.endswith("'"):
                return answers.get(key) == value[1:-1]
            else:
                return answers.get(key) == value

        # Length check
        if ".length > " in condition:
            key = condition.split(".length > ")[0].strip()
            threshold = int(condition.split(".length > ")[1].strip())
            arr = answers.get(key, [])
            return len(arr) > threshold

        # AND condition
        if " && " in condition:
            parts = condition.split(" && ")
            return all(self._evaluate_condition(p.strip(), answers) for p in parts)

        return True

    def calculate_progress(self, answers: Dict[str, Any]) -> float:
        """Calculate interview progress (0-1)."""
        total = len(self.questions)
        answered = sum(1 for q in self.questions if q.id in answers)
        return answered / total if total > 0 else 0.0
