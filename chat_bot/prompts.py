import random

prompts = {
    "environment": {
        "transport": "This is a conversation between two friends about the environment and transport. \n\nFriend_a: It is so important to reduce our carbon footprint these days.\nFriend_q: Yes, do you take public transport often?\n\nYou: I try to, but it's not always possible with my work schedule. \nFriend_q: Do you live close to where you work?\n\nYou: Yes, I'm only a few blocks away. \nFriend_q: Well, that's good. You're already doing your part by living close to where you work. \n\nFriend_a: Cycling can also be a great alternative.\nYou: I do cycle sometimes, but the weather can be a bit unpredictable.",
        "recycling": "This is a conversation between two friends about the recycling.\n\nFriend_q: Hey, have you been recycling lately?\n\nYou: Yeah, I've been trying to do my part to help the environment.\n\nFriend_q: What kind of things do you recycle?\n\nYou: I recycle paper, plastic, and metal. I try to recycle as much as possible.\n\nYou: What about you?\n\nFriend_a: I recycle paper, plastic, and metal too.\n\nYou: How frequently do you go?\n\nFriend_a:  I usually go every other week.\n\nYou:  I try to go every week, but sometimes I forget.",
        "food_waste": "This is a conversation between two friends about environment and food.\n\nFriend_a: There is so much food waste on our planet. \n\nYou: The situation is very bad. \n\nFriend_q: How come? \n\nYou: We have so much food, but we don't eat it all. \n\nFriend_a: Supermarkets have so much spare food they don't sell.\n\nFriend_q: What can we do about it? \n\nYou: We can redistribute food to soup kitchens and food banks. \n\nFriend_a: We can also compost food waste.\n\nYou: That's a great idea. Even restaurants have a lot of waste. \n\nFriend_q: What can we do about that? \n\nYou: We can ask them to donate their leftover food too. \n\n"
    },
    "culture": {
        "england": "This is a conversation between two friends about English culture.\n\nFriend_q: Have you ever been to England?\n\nYou: Yes, I've been a few times. I really love the culture there. The people are so polite and the food is amazing.\n\nFriend_a: Yeah, I've been there a few times too. I love the pubs and the history.\n\nYou: I love having a pint of beer in the pub. \n\nFriend_q: Have you visited Buckingham Palace?\n\nYou: Yes, I have. It's really beautiful and the history is fascinating. Are you a fan of the Royal family?\n\nFriend_a: I am. I think they're a great representation of England.",
        "movies": "This is a conversation between two friends about movies.\n\nFriend_q: What is your favourite movie?\n\nYou: I absolutely love The Shawshank Redemption. It's one of my all-time favourites!\n\nFriend_q: What do you like about it?\n\nYou: It's a really well-done movie with great acting and an interesting plot. I also like the setting and the characters.\n\nYou: What is your favourite movie?\n\nFriend_a:  I would have to say my favourite movie is Forrest Gump. I love the humour and the sentiment in the movie.\n\nYou: Do you want to go see the new spiderman with me tomorrow?\n\nFriend_a:  Sure, that sounds like fun!",
        "music": "This is a conversation between two friends about music. \n\nFriend_q: What kind of music do you listen to?\n\nYou: I like to listen to a variety of music, but my favorite type of music is country.\n\nFriend_q: Why do you like country music?\n\nYou: I like the sound of the instruments and the lyrics.\n\nYou: How often do you listen to music?\n\nFriend_a: I listen to music every day.\n\nYou: Do you listen to music while working? \n\nFriend_a: No, I usually listen to music when I'm relaxing or working out."
    },
    "lifestyle": {
        "hobbies": "This is a conversation between friends about hobbies. \n\nFriend_q: What do you like to do in your spare time?\n\nYou: I like to play video games, watch TV, and read. What about you?\n\nFriend_a: I like to cook and hang out with my friends. \n\nYou: That sounds like fun.\n\nFriend_q: What do you watch on TV?\n\nYou:  I like to watch action movies and comedies.\n\nYou: Do you get a lot of free time?\n\nFriend_a: I usually have a few hours each day to myself.\n\n",
        "home": "This is a conversation between two friends and their homes.\n\nFriend_q: Where do you live?\n\nYou: I live in a village, 30 minutes from the centre of town. \n\nFriend_a: That sounds so nice!\n\nYou: Yes, I have a quaint cottage and the neighbours are lovely. \n\nFriend_q: How many bedrooms does your house have? \n\nYou: Only 2 bedrooms, but the garden is huge. What is your house like? \n\nFriend_a: I live in an apartment in the city centre. It's small, but I love it.",
        "food":"The following is a conversation between friends about food.\n\nFriend_q: What is your favourite pizza?\nYou: Ham and pineapple.\nFriend_q: What is your favourite type of chocolate?\nYou: Milk chocolate.\nYou: What is your favourite sandwich?\nFriend_a: I love a good BLT. \nYou: Why?\nFriend_a: The bacon, lettuce and tomato are the perfect combination."
    }
}

counts = {
    "environment": {
        "transport": 1,
        "recycling": 1,
        "food_waste":1
    },
    "culture": {
        "england": 1,
        "movies": 1,
        "music": 1
    },
    "lifestyle": {
        "hobbies": 1,
        "home": 1,
        "food": 1
    }
}


def inc_count(topic, subtopic):
    subtopics = counts.get(topic)
    st_count = subtopics.get(subtopic)
    st_count += 1
    subtopics.update({subtopic: st_count})
    counts.update({topic: subtopics})


def get_prompt(topic):
    subtopic = choose_subtopic(topic)
    inc_count(topic, subtopic)
    return prompts.get(topic).get(subtopic)


def get_ranges(topic):
    subtopics = counts.get(topic)
    inverses = {}
    for subtopic in subtopics.keys():
        inverses.update({subtopic: 1 / float(subtopics.get(subtopic))})
    norm_constant = 0
    for s in inverses.keys():
        norm_constant += inverses.get(s)
    probs = {}
    for s in inverses.keys():
        probs.update({s: inverses.get(s) / norm_constant})
    lower_bound = 0
    ranges = {}
    count = 1

    for subtopic in probs.keys():
        if count == len(probs):
            ranges.update({subtopic: (lower_bound, 1)})
        else:
            ranges.update({subtopic: (lower_bound, lower_bound + probs.get(subtopic))})
            lower_bound += probs.get(subtopic)
        count += 1

    return ranges


def choose_subtopic(topic):
    ranges = get_ranges(topic)
    rand_val = random.random()
    while rand_val == 0:
        rand_val = random.random()
    for subtopic in ranges.keys():
        lower = ranges.get(subtopic)[0]
        higher = ranges.get(subtopic)[1]
        if lower < rand_val <= higher:
            return subtopic


