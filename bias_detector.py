import re
from collections import Counter

class BiasDetector:
    """Main class for detecting various types of bias in text."""

    def __init__(self):
        #Keyword dictionaries for different bias types
        self.religious_ethnic_keywords = {
        # Religious Terms
        "christian", "muslim", "jewish", "hindu", "buddhist", "catholic",
        "protestant", "islam", "christianity", "judaism", "hinduism",
        "atheist", "religious", "religion", "faith", "believer", "infidel",

        # Religious Bias
        "crusade", "jihad", "holy war", "heretic", "blasphemy", "sacrilege",
        "godless", "heathen", "pagan", "cult", "extremist", "fundamentalist",
        "radical islam", "islamist", "terrorist", "sharia",

        # Ethnic Terms
        "ethnic", "ethnicity", "race", "racial", "tribe", "tribal",
        "immigrant", "foreigner", "alien", "outsider", "native",
        "minority", "majority", "diversity", "multicultural",

        # Ethnic Stereotypes
        "ghetto", "hood", "barrio", "reservation", "inner city",
        "exotic", "primitive", "civilized", "backward", "third world",
        "developing nation", "oriental", "latino", "hispanic"
        }

        self.age_keywords = {
        # Age Terms
        "old", "young", "elderly", "senior", "youth", "teenager",
        "millennial", "boomer", "gen z", "generation", "aged",
        "ancient", "aging", "youthful", "mature", "immature",

        # Age Stereotypes
        "too old", "too young", "over the hill", "past their prime",
        "out of touch", "outdated", "old-fashioned", "senile",
        "inexperienced", "naive", "immature", "childish", "juvenile",
        "retirement age", "middle-aged", "midlife crisis",

        # Ageist Language
        "dinosaur", "fossil", "relic", "has-been", "washed up",
        "young blood", "fresh face", "new generation", "old guard",
        "entitled millennials", "ok boomer", "snowflake generation",
        "lazy millennials", "entitled youth", "grumpy old"
        }

        self.racial_keywords = {
        # Racial/Ethnic Groups (neutral terms that may indicate bias in context)
        "black", "white", "asian", "hispanic", "latino", "african",
        "caucasian", "european", "american", "mexican", "chinese",
        "arab", "middle eastern", "indigenous", "native american",

        # Racial Issues
        "racism", "racist", "racial profiling", "discrimination",
        "prejudice", "stereotype", "stereotyping", "bigotry", "bigot",
        "segregation", "integration", "apartheid", "supremacy",

        # Problematic Terms
        "thug", "gangster", "criminal", "illegal", "illegals",
        "anchor baby", "welfare queen", "inner city", "urban",
        "articulate", "well-spoken", "exotic", "where are you from",
        "go back", "diversity hire", "affirmative action",

        # Racial Bias Indicators
        "white privilege", "reverse racism", "race card", "identity politics",
        "all lives matter", "blue lives matter", "black on black",
        "model minority", "perpetual foreigner"
        }

        self.political_keywords = {
            "government", "president", "party", "democrat", "republican",
        "policy", "liberal", "conservative", "left-wing", "right-wing",
        "administration", "congress", "senate", "politician", "politics",
        "election", "vote", "campaign", "legislation", "law", "bill",
        "senate", "house", "representative", "senator", "governor",
        "mayor", "council", "parliament", "minister", "regime",
        "socialist", "capitalism", "communism", "fascism", "democracy",
        "dictatorship", "freedom", "tyranny", "oppression", "liberty"
        }

        self.emotional_keywords = {
            # Extremely Negative
        "horrible", "terrible", "disgusting", "appalling", "horrific",
        "atrocious", "dreadful", "awful", "abysmal", "horrendous",
        "ghastly", "hideous", "vile", "revolting", "repulsive",
        "despicable", "detestable", "abhorrent", "loathsome", "nasty",
        "gross", "foul", "rotten", "wretched", "miserable",
        "pathetic", "pitiful", "deplorable", "lamentable",

        # Extremely Positive
        "amazing", "wonderful", "brilliant", "phenomenal", "magnificent",
        "fantastic", "incredible", "spectacular", "marvelous", "superb",
        "excellent", "outstanding", "remarkable", "fabulous", "splendid",
        "glorious", "sublime", "divine", "perfect", "flawless",
        "breathtaking", "stunning", "gorgeous", "beautiful", "lovely",

        # Intense Emotions
        "tragic", "shocking", "outrageous", "devastating", "heartbreaking",
        "alarming", "disturbing", "terrifying", "horrifying", "frightening"
        }

        self.gender_keywords = {
            # Gender Terms
        "men", "women", "girls", "boys", "male", "female",
        "man", "woman", "girl", "boy", "guy", "gal",
        "gentleman", "lady", "ladies", "gentlemen",

        # Gender Stereotypes & Issues
        "feminist", "feminism", "patriarchy", "matriarchy",
        "masculine", "feminine", "manly", "womanly",
        "tomboy", "girly", "macho", "effeminate",
        "housewife", "working mother", "career woman",
        "breadwinner", "stay-at-home", "sexist", "sexism",
        "gender roles", "glass ceiling", "mansplaining"
        }

        self.exaggeration_keywords = {
            # Absolutes
        "always", "never", "everyone", "nobody", "everything", "nothing",
        "all", "none", "every", "any", "impossible", "certain",

        # Intensifiers
        "completely", "totally", "absolutely", "utterly", "entirely",
        "fully", "wholly", "thoroughly", "perfectly", "infinitely",

        # Certainty Claims
        "definitely", "certainly", "guaranteed", "undoubtedly", "unquestionably",
        "indisputably", "irrefutably", "undeniably", "surely", "inevitably",

        # Universal Claims
        "universal", "unanimous", "everywhere", "nowhere", "anybody",
        "somebody", "anything", "something", "whole world", "entire",
        "forever", "eternity", "ultimate", "extreme", "total"
        }

        self.negativity_keywords = {
            # Conflict & Danger
        "hate", "hatred", "despise", "loathe", "detest",
        "danger", "dangerous", "threat", "threatening", "menace",
        "risk", "risky", "hazard", "peril", "jeopardy",
        "fear", "afraid", "scared", "terrified", "frightened",
        "terror", "terrorism", "panic", "alarm", "dread",

        # Failure & Decline
        "fail", "failure", "failing", "failed", "unsuccessful",
        "disaster", "catastrophe", "calamity", "tragedy", "crisis",
        "collapse", "collapsing", "decline", "declining", "deteriorate",
        "worsen", "worse", "worst", "degrade", "corrupt", "corruption",

        # Negative Outcomes
        "problem", "issue", "trouble", "difficulty", "hardship",
        "damage", "harm", "hurt", "injury", "wound",
        "destroy", "destruction", "ruin", "devastate", "wreck",
        "doom", "doomed", "nightmare", "hellish", "chaos",
        "broken", "shattered", "crushed", "defeated", "lost"
        }

        self.confirmation_keywords = {
            # Assumed Agreement
        "obviously", "clearly", "evidently", "undeniably", "plainly",
        "everyone knows", "as we all know", "everybody knows",
        "it's common sense", "common knowledge", "well-known fact",
        "goes without saying", "needless to say", "it's clear that",

        # False Certainty
        "without a doubt", "without question", "no doubt", "no question",
        "of course", "naturally", "certainly", "surely",
        "it's obvious", "it's evident", "self-evident", "speaks for itself",

        # Authority Claims
        "truth is", "fact is", "reality is", "simple truth",
        "anyone can see", "any fool can see", "blind can see",
        "proven fact", "established fact", "undisputed"
        }

        self.explanations = {
            "Political Bias": "Contains political terms or opinions that may favor one perspective.",
       "Emotional Bias": "Uses emotionally charged language designed to trigger strong reactions.",
       "Gender Bias": "References or stereotypes based on gender that may reinforce assumptions.",
       "Exaggeration Bias": "Uses absolute or extreme language that overstates situations.",
       "Negativity Bias": "Focuses disproportionately on negative aspects or outcomes.",
       "Confirmation Bias": "Assumes agreement or dismisses alternative perspectives.",
       "Religious/Ethnic Bias": "References religious or ethnic groups with potential stereotypes or prejudice.",
       "Age Bias": "Contains age-related stereotypes or discriminatory language about different generations.",
       "Racial Bias": "References race or ethnicity in ways that may perpetuate stereotypes or discrimination."
        }

    def preprocess_text(self, text):
        """Clean and prepare text for analysis"""
        if not text or not isinstance(text, str):
            return ""

        #Convert to lowercase and strip whitespace
        text = text.lower().strip()
        return text

    def find_keyword_matches(self, text, keywords):
        """Find all matching keywords in text and return them with positions"""
        matches = []
        for keyword in keywords:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            for match in re.finditer(pattern, text):
                matches.append({
                    'keyword': keyword,
                    'position': match.start()
                })
        return matches

    def calculate_bias_score(self, text, matches):
        """Calculate a bias intensity score based on frequency and text length."""
        if not text:
            return 0

        word_count = len(text.split())
        if word_count == 0:
            return 0

        # Score increases with frequency, normalized by text length
        score = (len(matches) / word_count) * 100
        return min(score, 100)  # Cap at 100

    def detect_bias(self, text):
        """
        Main detection function that analyzes text for various bias types.
        Returns a dictionary with detected biases and details.
        """
        # Validate input
        if not text or not isinstance(text, str):
            return {
                'error': 'Invalid input. Please provide a text string.',
                'biases': []
            }

        if len(text.strip()) < 3:
            return {
                'error': 'Text too short to analyze. Please provide at least 3 characters.',
                'biases': []
            }

        # Preprocess
        processed_text = self.preprocess_text(text)
        biases = []

        # Check each bias category
        bias_checks = [
            ("Political Bias", self.political_keywords),
            ("Emotional Bias", self.emotional_keywords),
            ("Gender Bias", self.gender_keywords),
            ("Exaggeration Bias", self.exaggeration_keywords),
            ("Negativity Bias", self.negativity_keywords),
            ("Confirmation Bias", self.confirmation_keywords),
            ("Religious/Ethnic Bias", self.religious_ethnic_keywords),
            ("Age Bias", self.age_keywords),
            ("Racial Bias", self.racial_keywords)
            ]

        for bias_name, keywords in bias_checks:
            matches = self.find_keyword_matches(processed_text, keywords)
            if matches:
                score = self.calculate_bias_score(processed_text, matches)
                biases.append({
                    'type': bias_name,
                    'explanation': self.explanations[bias_name],
                    'matches': [m['keyword'] for m in matches],
                    'count': len(matches),
                    'score': round(score, 2)
                })

        # Calculate overall bias score
        overall_score = 0
        if biases:
            overall_score = sum(b['score'] for b in biases) / len(biases)

        return {
            'text': text,
            'biases': biases,
            'overall_score': round(overall_score, 2),
            'word_count': len(text.split()),
            'is_neutral': len(biases) == 0
        }
