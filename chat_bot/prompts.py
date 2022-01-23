import random

prompts = {
    "food": {
        "food": "The following is a conversation between friends about food.\n\nFriend_q: What is your favourite pizza?\nYou: Ham and pineapple.\nFriend_q: What is your favourite type of chocolate?\nYou: Milk chocolate. What is your favourite sandwich?\nFriend_a: I love a good BLT. \nYou: Why?\nFriend_a: The bacon, lettuce and tomato are the perfect combination."
    },
    "sustainability": {
        "transport": "This is a conversation between two friends about the environment and transport.\n\nFriend_q: Do you take public transport often?\nYou: I try to, but it's not always possible with my work schedule.\nFriend_q: Do you live close to where you work?\nYou: Yes, I'm only a few blocks away. Do you cycle?\nFriend_a: I do cycle sometimes, but the weather can be a bit unpredictable.\nYou: Well, that's good. You're already doing your part by living close to where you work. What do you think about carbon footprints?\nFriend_a: It is so important to reduce our carbon footprint these days.",
        "recycling": "This is a conversation between two friends about recycling.\n\nFriend_q: Have you been recycling lately?\nYou: Yeah, I've been trying to do my part to help the environment.\nFriend_q: What kind of things do you recycle?\nYou: I recycle paper, plastic, and metal. What about you?\nFriend_a: I recycle paper, plastic, and metal too.\nYou: How frequently do you do it?\nFriend_a: I usually recycle every other week.",
        "food_waste": "This is a conversation between two friends about food and the environment.\n\nFriend_q: What can we do about it food waste?\nYou: We can redistribute food to soup kitchens and food banks. Even restaurants have a lot of waste.\nFriend_q: What can we do about that?\nYou: We can ask them to donate their leftover food too. Why is there so much food waste on our planet?\nFriend_a: We have so much food, but we don't eat it all.\nYou: How come?\nFriend_a: Supermarkets have so much spare food they don't sell."
    },
    "environment": {
        "climate change": "This is a conversation between two friends and climate change. \n\nFriend_q: Hey, have you heard about climate change?\n\nYou:  Yeah, I've been hearing about it a lot lately.\n\nFriend_q: Did you hear that it causes all sorts of problems like sea level rise, tropical storms and freak weather. \n\nYou: It's definitely something to be concerned about. It's only going to get worse in the future. What can we do to address it?\n\nFriend_a: We can reduce our fossil fuel consumption and use more renewable energy sources.\n\nYou: Really? What are some examples?\n\nFriend_a: There are a lot of different ways to reduce fossil fuel consumption. You can drive less, use less energy in your home, and switch to renewable energy sources like solar and wind power.\n\nYou:  I think I will definitely be smarter in my fuel consumption now.  Thank you for enlightening me on this important issue.",
        "deforestation": "This is a conversation between two friends about deforestation. \n\nFriend_q: What are your thoughts on deforestation?\n\nYou:  I think it's a huge problem. Deforestation is responsible for about 20% of global greenhouse gas emissions, so it's a major contributor to climate change. It's also responsible for the loss of habitat for millions of animals, and it's a major contributor to global warming.\n\nFriend_a:  Yeah, I know. It's really sad.\n\nYou: What can we do to help the situation?\n\nFriend_a: I'm not sure. I think we need to be more conscious about the things we buy and how they're made. We also need to demand that companies use sustainable practices.\n\nFriend_q: Do you try to save paper whenever you can? \n\nYou:  Yes, I do try to save paper whenever I can. For example, I print documents on both sides of the paper whenever possible.\n\nFriend_a: That's a great idea!\n\nYou: I also  try to recycle paper whenever I can.",
        "extinction" : "This is a conversation between two friends about endangered species. \n\nFriend_q:  Did you hear that the dinosaurs went extinct?\n\nYou: I know, it's so sad. They were such cool animals.\n\nFriend_a: There are so many endangered species in today's age too. \n\nFriend_q: Really, like what?\n\nYou: There are so many animals that are in danger of becoming extinct. Some of the animals that are in the most danger are the Tigers, Pandas, and the Gorillas.\n\nFriend_a: \n\nIt's really sad that so many animals are in danger of becoming extinct. We need to do something to help protect them.\n\nYou: We can protect the environment, and conserve forests and land, to conserve their habitats. \n\nFriend_a:\n\nThat's a great idea! We can also create awareness about the importance of these animals, and the danger they are in."
    },
    "culture": {
        "england": "This is a conversation between two friends about English culture.\n\nFriend_q: Have you ever been to England?\nYou: Yes, I've been a few times. I really love the culture there.\nFriend_q: Why do you love it?\nYou: The people are so polite and the food is amazing. Have you been?\nFriend_a: Yeah, I've been there a few times too. I love the pubs and the history.\nYou: Have you visited Buckingham Palace?\nFriend_a: Yes, I have. It's really beautiful and the history is fascinating.",
        "movies": "This is a conversation between two friends about movies.\n\nFriend_q: What is your favourite movie?\nYou: I absolutely love The Shawshank Redemption. It's one of my all-time favourites!\nFriend_q: What do you like about it?\nYou: It's a really well-done movie with great acting and an interesting plot. I also like the setting and the characters. What is your favourite movie?\nFriend_a:  I would have to say my favourite movie is Forrest Gump. I love the humour and the sentiment in the movie.\nYou: Do you want to go see the new Spiderman movie with me tomorrow?\nFriend_a:  Sure, that sounds like fun!",
        "music": "This is a conversation between two friends about music.\n\nFriend_q: What kind of music do you listen to?\nYou: I like to listen to a variety of music, but my favourite type of music is country.\nFriend_q: Why do you like country music?\nYou: I like the sound of the instruments and the lyrics. How often do you listen to music?\nFriend_a: I listen to music every day.\nYou: Do you listen to music while working?\nFriend_a: No, I usually listen to music when I'm relaxing or working out."
    },
    "lifestyle": {
        "hobbies": "This is a conversation between friends about hobbies.\n\nFriend_q: What do you like to do in your spare time?\nYou: I like to play video games, watch TV, and read. What about you?\nFriend_a: I like to cook and hang out with my friends.\nYou: That sounds like fun.\nFriend_q: What do you watch on TV?\nYou:  I like to watch action movies and comedies. Do you get a lot of free time?\nFriend_a: I usually have a few hours each day to myself.",
        "home": "This is a conversation between two friends about their homes.\n\nFriend_q: Where do you live?\nYou: I live in a village, 30 minutes from the centre of town.\nFriend_q: How many bedrooms does your house have?\nYou: Only 2 bedrooms, but the garden is huge. What is your house like?\nFriend_a: I live in an apartment in the city centre. It's small, but I love it.\nYou: What are your neighbours like?\nFriend_a: The neighbours are lovely.",
        "daily routine": "This is a conversation between two friends about daily routine.\n\nFriend_q: What do you usually do in the day?\n\nYou: I usually wake up, check my phone and then go for a run. After that, I'll come home, shower and eat breakfast. Then I'll either work on the computer or do some housework. In the evening, I'll usually watch TV or read before going to bed. \n\nFriend_q: That sounds like a pretty busy day! Do you have any time for yourself?\n\nYou:  I usually try to take some time for myself in the evening, either by reading or watching TV. I also like to go for walks when the weather is nice. What about you?\n\nFriend_a:  I usually just relax at home in the evenings. I don't really have time for anything else.\n\nYou: What time do you get up in the morning? Maybe you could go for a morning walk.\n\nFriend_a: I usually get up at around 7am. I guess I could go then. \n\nYou: Great! It's a good way to start the day."
    }
}

counts = {
    "food": {
        "food": 1
    },
    "sustainability": {
        "transport": 1,
        "recycling": 1,
        "food_waste": 1
    },
    "environment": {
        "climate change": 1,
        "deforestation": 1,
        "extinction": 1
    },
    "culture": {
        "england": 1,
        "movies": 1,
        "music": 1
    },
    "lifestyle": {
        "hobbies": 1,
        "home": 1,
        "daily routine": 1
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


