import asyncio
import random
from models import Client, Point, SEXES


names = ['Liam', 'Olivia', 'Noah', 'Emma', 'Oliver', 'Charlotte', 'Elijah', 'Amelia', 'James', 'Ava', 'William', 'Sophia', 'Benjamin', 'Isabella', 'Lucas', 'Mia', 'Henry', 'Evelyn', 'Theodore', 'Harper']
surnames = ['Cody', 'Allison', 'Bradley', 'Samuel', 'Shawn', 'April', 'Derek', 'Kathryn', 'Kristin', 'Chad', 'Jenna', 'Tara', 'Maria', 'Krystal', 'Jared', 'Anna', 'Edward', 'Julie', 'Peter', 'Holly', 'Marcus', 'Kristina', 'Natalie', 'Jordan', 'Victoria', 'Jacqueline', 'Corey']
words = ['almost', 'already', 'although', 'always', 'American', 'amount', 'analysis', 'animal', 'another', 'answer', 'anyone', 'anything', 'appear', 'approach', 'around', 'arrive', 'article', 'artist', 'assume', 'attack', 'attention', 'attorney', 'audience', 'author', 'authority', 'available', 'beautiful', 'because', 'become', 'before', 'behavior', 'behind', 'believe', 'benefit', 'better', 'between', 'beyond', 'billion', 'brother', 'budget', 'building', 'business', 'camera', 'campaign', 'cancer', 'candidate', 'capital', 'career', 'center', 'central', 'century', 'certain', 'certainly', 'challenge', 'chance', 'change', 'character', 'charge', 'choice', 'choose', 'church', 'citizen', 'clearly', 'collection', 'college', 'commercial', 'common', 'community', 'company', 'compare', 'computer', 'concern', 'condition', 'conference', 'Congress', 'consider', 'consumer', 'contain', 'continue', 'control', 'country', 'couple', 'course', 'create', 'cultural', 'culture', 'current', 'customer', 'daughter', 'debate', 'decade', 'decide', 'decision', 'defense', 'degree', 'Democrat', 'democratic', 'describe', 'design', 'despite', 'detail', 'determine', 'develop', 'development', 'difference', 'different', 'difficult', 'dinner', 'direction', 'director', 'discover', 'discuss', 'discussion', 'disease', 'doctor', 'during', 'economic', 'economy', 'education', 'effect', 'effort', 'either', 'election', 'employee', 'energy', 'enough', 'entire', 'environment', 'environmental', 'especially', 'establish', 'evening', 'everybody', 'everyone', 'everything', 'evidence', 'exactly', 'example', 'executive', 'expect', 'experience', 'expert', 'explain', 'factor', 'family', 'father', 'federal', 'feeling', 'figure', 'finally', 'financial', 'finger', 'finish', 'follow', 'foreign', 'forget', 'former', 'forward', 'friend', 'future', 'garden', 'general', 'generation', 'government', 'ground', 'growth', 'happen', 'health', 'herself', 'himself', 'history', 'hospital', 'however', 'hundred', 'husband', 'identify', 'imagine', 'impact', 'important', 'improve', 'include', 'including', 'increase', 'indeed', 'indicate', 'individual', 'industry', 'information', 'inside', 'instead', 'institution', 'interest', 'interesting', 'international']


async def get_random_surname() -> str:
    return random.choice(surnames)


async def get_random_age() -> int:
    return random.randint(15, 25)


async def get_random_sex() -> str:
    return random.choice(SEXES)


async def get_random_point() -> Point:
    return Point(lon=random.random() + 28.093555, lat=random.random() + -16.721514)


async def create_random_description() -> str:
    random_words = [random.choice(words) for i in range(random.randint(5, 20))]
    return " ".join(random_words)


async def generate_random_clients():
    last_telegram_id_client = await Client.all().order_by("-telegram_id").first()
    last_telegram_id = last_telegram_id_client.telegram_id
    for name in names:
        last_telegram_id += 1
        await Client.create(
            telegram_id=last_telegram_id,
            name=name,
            surname=await get_random_surname(),
            age=await get_random_age(),
            sex=await get_random_sex(),
            target=await get_random_sex(),
            location=await get_random_point(),
            description=await create_random_description()
        )

