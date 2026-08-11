"""
Mentorsy - content bank, September batch (8 September - 7 October 2026)

Two pieces a day: a feed post at 09:00 IST and a reel at 20:30 IST.

Written fresh rather than cycled. Same voice rules as parts one and two:

  - never first person singular. Mentorsy has hired teachers; the page is the
    company, not one person
  - name the specific year group, board, paper or topic
  - the hook states a claim, the body pays it off
  - British spelling
  - no invented statistics, exam board rules or admissions policy. Where a
    claim would need a number, the line is rewritten so it does not

Subject spread: Mathematics 8, Coding 5, AI 5, Public Speaking 5, French 4,
Science 3.
"""

DAYS_C = [

# -- 1 -------------------------------------------------------------------
{"post": {
    "kind": "compare", "subject": "Mathematics", "pillar": "Inside the Method",
    "hook": "Two ways to revise for a maths paper.",
    "left_title": "Feels like revision",
    "left": ["Reading through worked examples",
             "Highlighting the textbook",
             "Watching a topic video",
             "Copying out the mark scheme"],
    "right_title": "Is revision",
    "right": ["Closing the book and starting a question",
              "Getting it wrong and finding out where",
              "Redoing the same question days later",
              "Marking honestly, in red"],
    "cta": "Ask which column tonight looked like.",
    "caption": "Two ways to revise for a maths paper, and only one of them moves a grade.\n\nReading a worked example is comfortable because the answer is already there. Nothing is at risk, so nothing is learned. The brain files it under 'seen', not under 'can do'.\n\nA blank page is uncomfortable for exactly the reason it works. It forces retrieval, and retrieval is the thing the exam actually tests.\n\nOne honest question, closed-book, is worth an hour of highlighting.",
    "hashtags": ["#IGCSE", "#MathsRevision", "#ParentTips", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d31_closed_book",
    "subject": "Mathematics", "pillar": "Inside the Method",
    "hook": "Reading worked examples is not revision.",
    "beats": ["The answer is already on the page.",
              "Nothing is at risk, so nothing is learned.",
              "The brain files it under 'seen', not 'can do'.",
              "A blank page is uncomfortable for the reason it works.",
              "One closed-book question beats an hour of highlighting."],
    "cta": "Follow for the rest.",
    "caption": "Reading worked examples is not revision.\n\nThe answer is already on the page, so nothing is retrieved and nothing sticks. It gets filed under 'seen', which is not the same as 'can do'.\n\nClose the book. Start the question. Being stuck is the part that teaches.",
    "hashtags": ["#IGCSE", "#MathsRevision", "#StudySkills", "#Mentorsy"]}},

# -- 2 -------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Public Speaking", "pillar": "Parent Scripts",
    "hook": "What to say the night before a presentation.",
    "points": [
        {"heading": "Ask them to say the first line out loud"},
        {"heading": "Do not offer to rewrite it at 9pm"},
        {"heading": "Name the fear instead of denying it"},
        {"heading": "Agree what happens if they lose their place"},
    ],
    "cta": "Save this for the night before.",
    "caption": "What to say the night before a presentation.\n\n'You'll be fine' closes the conversation. It sounds like reassurance and lands like a door shutting, because the child still has the fear and now has nowhere to put it.\n\nName it instead. 'Most people go blank somewhere in the middle. What do you do if that happens?' turns a vague dread into one thing with a plan attached.\n\nThen ask for the first line out loud, once. The opening is where the nerves live, and hearing it in a kitchen makes the classroom quieter.",
    "hashtags": ["#PublicSpeaking", "#ParentTips", "#ChildConfidence", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d32_night_before_talk",
    "subject": "Public Speaking", "pillar": "Parent Scripts",
    "hook": "'You'll be fine' is the least useful thing to say.",
    "beats": ["It sounds like reassurance and lands like a door shutting.",
              "The fear is still there. Now it has nowhere to go.",
              "Try: most people go blank somewhere in the middle.",
              "What do you do if that happens?",
              "A named fear with a plan stops being dread."],
    "cta": "Follow for the rest.",
    "caption": "'You'll be fine' is the least useful thing to say the night before.\n\nIt closes the conversation while the fear is still in the room. Naming it works better: most people go blank somewhere in the middle, so what happens if that happens?\n\nA fear with a plan attached is just a step in the talk.",
    "hashtags": ["#PublicSpeaking", "#ParentTips", "#ChildConfidence", "#Mentorsy"]}},

# -- 3 -------------------------------------------------------------------
{"post": {
    "kind": "statement", "subject": "Coding", "pillar": "Future Skills",
    "hook": "Your child does not need six languages.",
    "sub": "They need one, deeply, and the habit of finishing.",
    "caption": "Your child does not need six programming languages. They need one, deeply, and the habit of finishing things.\n\nA child who has touched Python, Java, C++, JavaScript and two block editors has learned six kinds of syntax and no engineering. Syntax is the cheapest part. It is the part a reference page can hand you in thirty seconds.\n\nWhat transfers between languages is the thinking: breaking a problem into parts, naming things clearly, testing an assumption, reading an error properly.\n\nOne language, held long enough to build something that actually runs, teaches all four. A tour of six teaches none of them.",
    "hashtags": ["#CodingForKids", "#FutureSkills", "#STEM", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d33_one_language_deeply",
    "subject": "Coding", "pillar": "Future Skills",
    "hook": "Six languages is not six times the learning.",
    "beats": ["Syntax is the cheapest part of programming.",
              "A reference page hands it to you in thirty seconds.",
              "What transfers is breaking a problem into parts.",
              "Naming things. Testing. Reading the error properly.",
              "One language, held long enough to finish something, teaches all of it."],
    "cta": "Follow for the rest.",
    "caption": "Six languages is not six times the learning.\n\nSyntax is the cheapest part of programming and the easiest to look up. What transfers between languages is decomposition, naming, testing and reading an error properly.\n\nOne language, held long enough to finish something that runs, teaches every one of those.",
    "hashtags": ["#CodingForKids", "#STEM", "#FutureSkills", "#Mentorsy"]}},

# -- 4 -------------------------------------------------------------------
{"post": {
    "kind": "quote", "subject": "AI", "pillar": "Curriculum Decoded",
    "hook": "AI can draft the essay. It cannot sit in the chair and defend it.",
    "attrib": None,
    "caption": "AI can draft the essay. It cannot sit in the chair and defend it.\n\nThat gap is where school assessment is quietly moving. Anything a child produces unsupervised is becoming weaker evidence, and anything they produce in a room with a teacher is becoming stronger: the spoken answer, the timed paper, the follow-up question nobody prepared for.\n\nSo the honest question about AI at home is not whether it was used. It is whether your child could still hold the argument if the laptop were shut.\n\nThat is a skill, and it is trainable. It just is not trained by a finished document.",
    "hashtags": ["#AIForKids", "#IGCSE", "#DigitalLiteracy", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d34_defend_it",
    "subject": "AI", "pillar": "Curriculum Decoded",
    "hook": "AI can draft the essay. It cannot defend it.",
    "beats": ["Unsupervised work is becoming weaker evidence.",
              "Work produced in a room with a teacher is becoming stronger.",
              "The spoken answer. The timed paper. The follow-up question.",
              "So the question is not whether AI was used.",
              "It is whether your child could hold the argument with the laptop shut."],
    "cta": "Follow for the rest.",
    "caption": "AI can draft the essay. It cannot defend it.\n\nThe useful question at home is not whether a tool was used. It is whether your child could still hold the argument with the laptop shut.\n\nThat is trainable. A finished document does not train it.",
    "hashtags": ["#AIForKids", "#IGCSE", "#ParentTips", "#Mentorsy"]}},

# -- 5 -------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "French", "pillar": "Confidence",
    "hook": "Four reasons French vocabulary will not stick.",
    "points": [
        {"heading": "Word lists are learned in one direction only"},
        {"heading": "Nothing is ever said out loud"},
        {"heading": "The words arrive without a sentence around them"},
        {"heading": "Revision happens once, the night before"},
    ],
    "cta": "Send this to a parent of a Year 9.",
    "caption": "Four reasons French vocabulary will not stick.\n\nMost lists get learned French to English, because that is the direction the test runs. Then the speaking assessment asks for the opposite and the word is not there.\n\nWords also arrive stripped of context. 'Chercher' on a list is a translation. 'Je cherche mes clés' is a memory, and memories survive longer than translations.\n\nAnd almost none of it is said aloud, so the mouth has never made the sound under pressure.\n\nSame twenty words. Both directions, in sentences, out loud, twice across a week. That is the whole change.",
    "hashtags": ["#FrenchLearning", "#IGCSE", "#LanguageLearning", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d35_vocab_both_ways",
    "subject": "French", "pillar": "Confidence",
    "hook": "The word list is being learned in one direction.",
    "beats": ["French to English, because that is how the test runs.",
              "Then speaking asks for the opposite and it is not there.",
              "'Chercher' on a list is a translation.",
              "'Je cherche mes cles' is a memory.",
              "Both directions, in sentences, out loud. That is the change."],
    "cta": "Follow for the rest.",
    "caption": "The word list is being learned in one direction.\n\nFrench to English is how the vocabulary test runs, so that is how it gets revised. Then the speaking assessment asks for the reverse and the word is missing.\n\nBoth directions, inside a sentence, said out loud. Same twenty words, completely different result.",
    "hashtags": ["#FrenchLearning", "#LanguageLearning", "#IGCSE", "#Mentorsy"]}},

# -- 6 -------------------------------------------------------------------
{"post": {
    "kind": "statement", "subject": "Mathematics", "pillar": "Parent Scripts",
    "hook": "Telling a child you were bad at maths gives them permission to stop.",
    "sub": "It is meant as comfort. It arrives as a diagnosis.",
    "caption": "Telling a child you were bad at maths gives them permission to stop.\n\nIt is almost always meant kindly. The intention is 'you are not alone' and the message received is 'this runs in the family, so there is no point pushing'.\n\nChildren take inherited limits seriously. Nobody keeps working at something their own parent has described as impossible for people like them.\n\nThere is a version that helps. 'That topic took a long time to click for a lot of people, including here' says the same thing without closing the door.\n\nOne sentence is a shared identity. The other is a shared timeline.",
    "hashtags": ["#MathsConfidence", "#ParentTips", "#ChildConfidence", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d36_permission_to_stop",
    "subject": "Mathematics", "pillar": "Parent Scripts",
    "hook": "That sentence was meant as comfort.",
    "beats": ["Telling a child you were bad at maths lands as a diagnosis.",
              "The intention is 'you are not alone'.",
              "What arrives is 'this runs in the family'.",
              "Children take inherited limits very seriously.",
              "Try: that topic took a long time to click for a lot of people."],
    "cta": "Follow for the rest.",
    "caption": "That sentence was meant as comfort.\n\nTelling a child you were bad at maths sounds like solidarity and lands like a diagnosis. Nobody keeps pushing at something their own parent has called impossible for people like them.\n\nSwap the identity for a timeline: that topic took a long time to click, and then it clicked.",
    "hashtags": ["#MathsConfidence", "#ParentTips", "#Mentorsy", "#DubaiSchools"]}},

# -- 7 -------------------------------------------------------------------
{"post": {
    "kind": "compare", "subject": "Science", "pillar": "Inside the Method",
    "hook": "Two ways to prepare for the practical.",
    "left_title": "Learning the experiment",
    "left": ["Memorising the method",
             "Copying the results table",
             "Learning the expected outcome",
             "Reading someone else's conclusion"],
    "right_title": "Learning the thinking",
    "right": ["Naming the variable being changed",
              "Saying why the control matters",
              "Explaining an anomalous reading",
              "Improving the method out loud"],
    "cta": "Ask which one the revision guide teaches.",
    "caption": "Two ways to prepare for the practical, and the paper only rewards one.\n\nMemorising a method gets you through the description and nothing else. Practical questions rarely stop at what happened; they ask why the control was there, what the anomalous reading means, how the method could be improved.\n\nThose are the marks that separate a middling script from a strong one, and they cannot be revised from a results table.\n\nWhether your child sits a practical paper or the written alternative, the questions come from the same place: not what the experiment did, but why it was built that way.",
    "hashtags": ["#IGCSEScience", "#CambridgeCurriculum", "#STEM", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d37_practical_thinking",
    "subject": "Science", "pillar": "Inside the Method",
    "hook": "Memorising the method gets almost none of the marks.",
    "beats": ["Practical questions rarely stop at what happened.",
              "Why was the control there?",
              "What does the anomalous reading mean?",
              "How would you improve the method?",
              "None of that can be revised from a results table."],
    "cta": "Follow for the rest.",
    "caption": "Memorising the method gets almost none of the marks.\n\nPractical questions ask why the control was there, what an anomalous reading means, and how the method could be improved. Those marks separate a middling script from a strong one.\n\nA results table cannot teach any of them.",
    "hashtags": ["#IGCSEScience", "#STEM", "#CambridgeCurriculum", "#Mentorsy"]}},

# -- 8 -------------------------------------------------------------------
{"post": {
    "kind": "quote", "subject": "Mathematics", "pillar": "Confidence",
    "hook": "Speed is not understanding. It is familiarity wearing understanding's coat.",
    "attrib": None,
    "caption": "Speed is not understanding. It is familiarity wearing understanding's coat.\n\nThe fast child in Year 7 is usually the one who met the topic before. That advantage is real, and it is temporary, and it says nothing about capacity.\n\nThe cost lands later. Children who were fast early often stall around Year 10, because they were rewarded for recall at a point where the subject started asking for reasoning, and nobody flagged the switch.\n\nMeanwhile the slow, careful child who asks why has been building the thing that survives.\n\nSpeed is worth having. It is just a terrible thing to measure a twelve year old by.",
    "hashtags": ["#MathsConfidence", "#ParentTips", "#CambridgeCurriculum", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d38_speed_is_not_understanding",
    "subject": "Mathematics", "pillar": "Confidence",
    "hook": "The fast child is not always the strong one.",
    "beats": ["Speed in Year 7 usually means they met the topic before.",
              "Real advantage. Temporary one.",
              "Fast children often stall around Year 10.",
              "Recall was rewarded. Then the subject asked for reasoning.",
              "The careful child who asks why was building the durable thing."],
    "cta": "Follow for the rest.",
    "caption": "The fast child is not always the strong one.\n\nSpeed early usually means prior exposure, not capacity. The stall tends to come around Year 10, when the subject stops rewarding recall and starts asking for reasoning.\n\nThe child who works slowly and asks why has been building the part that lasts.",
    "hashtags": ["#MathsConfidence", "#ChildConfidence", "#ParentTips", "#Mentorsy"]}},

# -- 9 -------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Coding", "pillar": "Inside the Method",
    "hook": "What week one of a real coding course looks like.",
    "points": [
        {"heading": "Something runs on day one"},
        {"heading": "Something breaks on day one too"},
        {"heading": "The error message gets read, not skipped"},
        {"heading": "The student changes it into their own thing"},
    ],
    "cta": "Ask what week one looks like before you enrol.",
    "caption": "What week one of a real coding course looks like.\n\nSomething should run on the first day. Not a slide about what programming is, not an hour of theory about variables. Working code, on screen, that the student can point at.\n\nAnd something should break on the first day, deliberately, while there is a teacher in the room. A child who has only ever seen code work has never practised the actual job.\n\nThen the error message gets read out loud rather than scrolled past. Most beginners never learn that the computer already told them what was wrong.\n\nBy the end of week one, they should have changed the thing into something that was not in the plan.",
    "hashtags": ["#CodingForKids", "#STEM", "#FutureSkills", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d39_week_one",
    "subject": "Coding", "pillar": "Inside the Method",
    "hook": "Something should run on day one. And something should break.",
    "beats": ["Not a slide about what programming is.",
              "Working code, on screen, that the student can point at.",
              "Then break it on purpose, with a teacher in the room.",
              "Read the error out loud. The computer already said what was wrong.",
              "By Friday they should have changed it into their own thing."],
    "cta": "Follow for the rest.",
    "caption": "Something should run on day one. And something should break.\n\nA child who has only seen code work has never practised the actual job. Breaking it deliberately, with a teacher present, is the lesson.\n\nMost beginners never learn that the error message already told them the answer.",
    "hashtags": ["#CodingForKids", "#STEM", "#Mentorsy", "#FutureSkills"]}},

# -- 10 ------------------------------------------------------------------
{"post": {
    "kind": "compare", "subject": "Public Speaking", "pillar": "School Choice",
    "hook": "Two answers at an open evening.",
    "left_title": "Sounds good",
    "left": ["'We build confidence'",
             "'Every child is encouraged to contribute'",
             "'We have a debating society'",
             "'Presentation skills are embedded'"],
    "right_title": "Means something",
    "right": ["'Every student presents twice a term'",
              "'Here is the assessment rubric'",
              "'Thirty of six hundred are in it'",
              "'Ask to see a Year 8 lesson'"],
    "cta": "Take the right-hand column to the next tour.",
    "caption": "Two answers at an open evening, and only one of them is checkable.\n\n'We build confidence' cannot be wrong, which is exactly the problem. Nothing in that sentence can be verified, compared or held to later.\n\n'Every student presents twice a term' can be. So can the size of the debating society against the size of the year group, and so can a rubric you are allowed to read.\n\nThe test is simple. If an answer could not turn out to be false, it has not told you anything.\n\nAsk for the number, the frequency, or the document.",
    "hashtags": ["#PublicSpeaking", "#SchoolChoice", "#DubaiSchools", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d40_checkable_answer",
    "subject": "Public Speaking", "pillar": "School Choice",
    "hook": "'We build confidence' cannot be wrong. That is the problem.",
    "beats": ["Nothing in that sentence can be verified.",
              "'Every student presents twice a term' can be.",
              "So can the size of the debating society against the year group.",
              "If an answer could not turn out to be false, it told you nothing.",
              "Ask for the number, the frequency, or the document."],
    "cta": "Follow for the rest.",
    "caption": "'We build confidence' cannot be wrong. That is the problem.\n\nAn answer that could never turn out to be false has not told you anything. 'Every student presents twice a term' can be checked. So can a rubric you are allowed to read.\n\nAsk for the number, the frequency, or the document.",
    "hashtags": ["#SchoolChoice", "#PublicSpeaking", "#DubaiSchools", "#Mentorsy"]}},

# -- 11 ------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "AI", "pillar": "Parent Scripts",
    "hook": "How to ask about the AI without starting a row.",
    "points": [
        {"heading": "Ask what it got wrong, not whether it was used"},
        {"heading": "Ask them to explain one paragraph aloud"},
        {"heading": "Ask what they typed to get it"},
        {"heading": "Agree the line before the next deadline, not during"},
    ],
    "cta": "Save this before the next assignment.",
    "caption": "How to ask about the AI without starting a row.\n\n'Did you use AI for this?' is an accusation with a yes-or-no exit, and both answers end the conversation.\n\n'What did it get wrong?' does not. It assumes use, skips the confession, and lands straight on the only skill that matters: whether your child can spot a confident sentence that is untrue.\n\n'What did you type to get that?' is the second good question. The prompt shows the thinking. A vague prompt means the tool did the work; a specific one means your child did.\n\nAnd set the rule between deadlines. Nobody negotiates well at eleven at night.",
    "hashtags": ["#AIForKids", "#ParentTips", "#DigitalLiteracy", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d41_what_did_it_get_wrong",
    "subject": "AI", "pillar": "Parent Scripts",
    "hook": "Do not ask whether they used AI.",
    "beats": ["'Did you use AI?' is an accusation with a yes-or-no exit.",
              "Both answers end the conversation.",
              "Ask what it got wrong instead.",
              "That skips the confession and lands on the real skill.",
              "Then ask what they typed. The prompt shows the thinking."],
    "cta": "Follow for the rest.",
    "caption": "Do not ask whether they used AI.\n\nIt is an accusation with a yes-or-no exit, and both answers close the conversation. Ask what it got wrong instead, and then ask what they typed to get it.\n\nA vague prompt means the tool did the work. A specific one means your child did.",
    "hashtags": ["#AIForKids", "#ParentTips", "#DigitalLiteracy", "#Mentorsy"]}},

# -- 12 ------------------------------------------------------------------
{"post": {
    "kind": "statement", "subject": "Public Speaking", "pillar": "Inside the Method",
    "hook": "Eye contact is a technique, not a personality trait.",
    "sub": "It is taught in about twenty minutes.",
    "caption": "Eye contact is a technique, not a personality trait.\n\nChildren are told to make eye contact and given no method, which is roughly as useful as telling someone to be taller. So they sweep the room, land on nobody, and look more nervous than when they started.\n\nThe method is boring and it works. One face, one sentence. Finish the sentence, then move. Three or four faces spread across the room, used in rotation.\n\nIt gives the eyes a job, so they stop searching. It paces the talk, because sentences get finished before the head turns. And from the audience it reads as calm.\n\nTwenty minutes to teach. A term to make automatic.",
    "hashtags": ["#PublicSpeaking", "#ChildConfidence", "#Mentorsy", "#ParentTips"]},
 "reel": {
    "kind": "reel", "slug": "d42_one_face_one_sentence",
    "subject": "Public Speaking", "pillar": "Inside the Method",
    "hook": "'Make eye contact' is not an instruction.",
    "beats": ["It is like telling someone to be taller.",
              "So they sweep the room and land on nobody.",
              "The method: one face, one sentence.",
              "Finish the sentence, then move. Three or four faces, in rotation.",
              "It gives the eyes a job, so they stop searching."],
    "cta": "Follow for the rest.",
    "caption": "'Make eye contact' is not an instruction.\n\nWithout a method children sweep the room, land on nobody and look more nervous than when they started.\n\nOne face, one sentence. Finish the sentence, then move. Three or four faces in rotation. It paces the talk and it reads as calm.",
    "hashtags": ["#PublicSpeaking", "#ChildConfidence", "#Mentorsy", "#DubaiSchools"]}},

# -- 13 ------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Mathematics", "pillar": "Curriculum Decoded",
    "hook": "A Level Maths does not start in Year 12.",
    "points": [
        {"heading": "It starts with algebraic fluency in Year 10"},
        {"heading": "Rearranging is assumed, not taught again"},
        {"heading": "Surds and indices arrive with no warm-up"},
        {"heading": "The first term is the fastest term"},
    ],
    "cta": "Send this to a parent with a child in Year 11.",
    "caption": "A Level Maths does not start in Year 12. It starts with algebraic fluency in Year 10.\n\nThe first term assumes rearranging, factorising, surds and indices are automatic, and moves at a pace that does not allow for relearning them. A student who can do that algebra slowly and carefully is, in that room, a student who cannot do it.\n\nThis is why strong IGCSE grades sometimes turn into a difficult October. The grade measured whether they could get there. A Level measures whether they can get there without thinking about it.\n\nThe fix belongs to the summer between, and it is narrow: fluency drills on the algebra they already know.",
    "hashtags": ["#ALevel", "#IGCSE", "#MathsTutoring", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d43_alevel_starts_earlier",
    "subject": "Mathematics", "pillar": "Curriculum Decoded",
    "hook": "A Level Maths does not start in Year 12.",
    "beats": ["The first term assumes the algebra is automatic.",
              "Rearranging, factorising, surds, indices.",
              "Slow and careful reads as cannot, at that pace.",
              "Which is why strong IGCSE grades meet a hard October.",
              "The fix belongs to the summer between, and it is narrow."],
    "cta": "Follow for the rest.",
    "caption": "A Level Maths does not start in Year 12.\n\nThe first term assumes rearranging, factorising, surds and indices are automatic and moves too fast to relearn them. A student who does that algebra slowly is, at that pace, a student who cannot.\n\nThe summer between is where that gets fixed.",
    "hashtags": ["#ALevel", "#IGCSE", "#MathsTutoring", "#Mentorsy"]}},

# -- 14 ------------------------------------------------------------------
{"post": {
    "kind": "compare", "subject": "French", "pillar": "Curriculum Decoded",
    "hook": "Reading French and speaking French are different subjects.",
    "left_title": "Reading builds",
    "left": ["Recognition of a word on a page",
             "Time to work it out",
             "Context from the sentence around it",
             "A silent, private answer"],
    "right_title": "Speaking needs",
    "right": ["Recall with nothing to look at",
              "An answer inside two seconds",
              "A verb ending chosen live",
              "A voice that other people hear"],
    "cta": "Ask which one is being practised at home.",
    "caption": "Reading French and speaking French are different subjects that share a vocabulary.\n\nReading is recognition with time attached. The word is on the page, the sentence around it helps, and nobody is waiting. Speaking is recall against a clock, with a verb ending chosen live and an audience.\n\nA child can be genuinely good at one and stuck in the other, and the reading mark will hide it right up until the speaking assessment.\n\nHomework is almost always reading and writing, because those can be marked in a pile. So the speaking practice has to be deliberate, and it has to happen out loud, somewhere other than the exam room.",
    "hashtags": ["#FrenchLearning", "#IGCSE", "#LanguageLearning", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d44_reading_is_not_speaking",
    "subject": "French", "pillar": "Curriculum Decoded",
    "hook": "Good at French on paper, stuck out loud.",
    "beats": ["Reading is recognition, with time attached.",
              "Speaking is recall against a clock, with an audience.",
              "Different subjects that happen to share a vocabulary.",
              "The reading mark hides the gap until the speaking assessment.",
              "Homework is written because written can be marked in a pile."],
    "cta": "Follow for the rest.",
    "caption": "Good at French on paper, stuck out loud.\n\nReading is recognition with time attached. Speaking is recall against a clock, choosing a verb ending live, in front of someone. A child can be strong in one and lost in the other.\n\nSpeaking practice has to be deliberate, because homework will never be it.",
    "hashtags": ["#FrenchLearning", "#LanguageLearning", "#IGCSE", "#Mentorsy"]}},

# -- 15 ------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Science", "pillar": "Curriculum Decoded",
    "hook": "Combined or separate sciences: what actually changes.",
    "points": [
        {"heading": "Separate sciences cover more content, not harder content"},
        {"heading": "Three sciences means three slots on the timetable"},
        {"heading": "Combined keeps a language or a humanity alive"},
        {"heading": "Neither closes A Level Sciences by itself"},
    ],
    "cta": "Ask the school what their sixth form expects.",
    "caption": "Combined or separate sciences: what actually changes.\n\nSeparate sciences are usually more content rather than harder content, and they cost a timetable slot that has to come from somewhere. Often that somewhere is a language or a humanity your child would have enjoyed.\n\nThe decision that matters is not prestige, it is what your child wants at A Level and what your specific sixth form asks for. Entry requirements differ between schools, so the only reliable answer comes from the school itself.\n\nAsk that question directly, in Year 9, and take the answer in writing. It converts an anxious guess into a scheduling decision.",
    "hashtags": ["#IGCSEScience", "#CambridgeCurriculum", "#SchoolChoice", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d45_combined_or_separate",
    "subject": "Science", "pillar": "Curriculum Decoded",
    "hook": "Separate sciences are not harder. They are bigger.",
    "beats": ["More content, and a timetable slot that comes from somewhere.",
              "Usually a language or a humanity.",
              "The real question is what the sixth form asks for.",
              "Entry requirements differ between schools.",
              "So ask your school, in Year 9, and get it in writing."],
    "cta": "Follow for the rest.",
    "caption": "Separate sciences are not harder. They are bigger.\n\nMore content, and a timetable slot taken from something else. The decision that matters is what your child wants at A Level and what your specific sixth form asks for.\n\nThose requirements differ by school, so ask yours directly and take the answer in writing.",
    "hashtags": ["#IGCSEScience", "#SchoolChoice", "#CambridgeCurriculum", "#Mentorsy"]}},

# -- 16 ------------------------------------------------------------------
{"post": {
    "kind": "quote", "subject": "Coding", "pillar": "Confidence",
    "hook": "A child who can read an error message is already ahead of most adults.",
    "attrib": None,
    "caption": "A child who can read an error message is already ahead of most adults.\n\nThe instinct, at every age, is to see red text and feel caught. Eyes slide off it. The line number, the file, the actual sentence describing the problem, all of it goes unread while the child asks someone what to do.\n\nBut the error is not a telling-off. It is the most specific piece of help in the entire session, written by the machine, for free, at the exact moment it is needed.\n\nTeaching a child to stop and read it takes one deliberate habit: say the message out loud before touching the keyboard.\n\nThat one habit turns being stuck from an emergency into a procedure.",
    "hashtags": ["#CodingForKids", "#ChildConfidence", "#STEM", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d46_read_the_error",
    "subject": "Coding", "pillar": "Confidence",
    "hook": "Red text is not a telling-off.",
    "beats": ["The instinct is to feel caught and look away.",
              "The line number goes unread. The message goes unread.",
              "But that message is the most specific help in the session.",
              "Written by the machine, free, at the exact moment it is needed.",
              "The habit: say it out loud before touching the keyboard."],
    "cta": "Follow for the rest.",
    "caption": "Red text is not a telling-off.\n\nThe error message is the most specific piece of help available, and most beginners never read it. Eyes slide off, hands go up.\n\nOne habit fixes it: say the message out loud before touching the keyboard. Being stuck becomes a procedure instead of an emergency.",
    "hashtags": ["#CodingForKids", "#STEM", "#ChildConfidence", "#Mentorsy"]}},

# -- 17 ------------------------------------------------------------------
{"post": {
    "kind": "statement", "subject": "Mathematics", "pillar": "Inside the Method",
    "hook": "Most lost marks are not wrong answers.",
    "sub": "They are correct thinking nobody wrote down.",
    "caption": "Most lost marks are not wrong answers. They are correct thinking nobody wrote down.\n\nMethod marks exist because examiners are marking a process, not a number. A student who arrives at the wrong final value with three visible, correct steps often scores more than one who writes a bare answer and gets it right by luck.\n\nStudents who work in their heads lose this quietly and repeatedly. Their books look tidy. Their marks look inexplicable.\n\nThe habit is small and it is unpopular: write the line before the one you are confident about. Substitution before evaluation. Rearrangement before solving.\n\nIt costs four seconds a question and it is the cheapest grade improvement available.",
    "hashtags": ["#IGCSE", "#MathsTutoring", "#ExamTechnique", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d47_show_the_line",
    "subject": "Mathematics", "pillar": "Inside the Method",
    "hook": "The marks were lost in the working, not the answer.",
    "beats": ["Examiners mark a process, not a number.",
              "Three visible correct steps can outscore a bare right answer.",
              "Students who work in their heads lose this quietly.",
              "Tidy books. Inexplicable marks.",
              "Write the substitution. Write the rearrangement. Four seconds."],
    "cta": "Follow for the rest.",
    "caption": "The marks were lost in the working, not the answer.\n\nMethod marks reward a visible process. A wrong final value with three correct written steps can outscore a bare answer that happened to be right.\n\nWrite the substitution. Write the rearrangement. It costs four seconds a question.",
    "hashtags": ["#IGCSE", "#ExamTechnique", "#MathsTutoring", "#Mentorsy"]}},

# -- 18 ------------------------------------------------------------------
{"post": {
    "kind": "compare", "subject": "AI", "pillar": "Future Skills",
    "hook": "Two children using the same AI tool.",
    "left_title": "Ends up weaker",
    "left": ["Asks for the answer",
             "Pastes it in unread",
             "Cannot say what it claimed",
             "Learns the tool is smarter than them"],
    "right_title": "Ends up stronger",
    "right": ["Asks for three approaches",
              "Picks one and says why",
              "Finds the line that is wrong",
              "Learns their own judgement is the product"],
    "cta": "Ask which column your child is in.",
    "caption": "Two children using the same AI tool, and it makes one weaker and one stronger.\n\nThe difference is not the software. It is the shape of the request. 'Answer this' hands over the thinking. 'Give three approaches, then compare them' keeps it.\n\nThe second child is doing something schools will keep rewarding: evaluating options, defending a choice, catching an error in a confident paragraph. That is judgement, and judgement is the part no tool supplies.\n\nBanning it at home mostly moves the usage somewhere unsupervised. Shaping the request works better, and it takes one sentence.\n\nAsk for options, not answers.",
    "hashtags": ["#AIForKids", "#FutureSkills", "#DigitalLiteracy", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d48_options_not_answers",
    "subject": "AI", "pillar": "Future Skills",
    "hook": "Same tool. One child gets weaker, one gets stronger.",
    "beats": ["The difference is the shape of the request.",
              "'Answer this' hands over the thinking.",
              "'Give three approaches, then compare them' keeps it.",
              "One learns the tool is smarter. One learns judgement is the product.",
              "Ask for options, not answers."],
    "cta": "Follow for the rest.",
    "caption": "Same tool. One child gets weaker, one gets stronger.\n\nThe difference is the request. 'Answer this' hands over the thinking. 'Give three approaches, then compare them' keeps it, and keeps the child practising the part no tool supplies.\n\nBanning it usually just moves it somewhere unsupervised.",
    "hashtags": ["#AIForKids", "#FutureSkills", "#ParentTips", "#Mentorsy"]}},

# -- 19 ------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Public Speaking", "pillar": "Future Skills",
    "hook": "What a speaking assessment is really testing.",
    "points": [
        {"heading": "Whether an answer has a structure"},
        {"heading": "Whether an opinion survives a follow-up"},
        {"heading": "Whether the voice carries to the back"},
        {"heading": "Whether a pause is used or feared"},
    ],
    "cta": "Save this before the next one.",
    "caption": "What a speaking assessment is really testing, in any subject.\n\nNot charisma. Structure. An answer that opens with a position, gives two reasons and closes on the position sounds prepared even when it is invented on the spot.\n\nThen it tests whether that position survives one follow-up question, which is the moment most students fold and agree with the examiner.\n\nAnd it tests volume and pause, both of which are physical and both of which are trainable in a fortnight.\n\nNone of that list is a personality. Every item on it is a drill, which is exactly why some children look naturally good at this and are simply practised.",
    "hashtags": ["#PublicSpeaking", "#IGCSE", "#FutureSkills", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d49_speaking_is_structure",
    "subject": "Public Speaking", "pillar": "Future Skills",
    "hook": "A speaking assessment is not testing charisma.",
    "beats": ["Position, two reasons, back to the position.",
              "That sounds prepared even when it is invented on the spot.",
              "Then: does the position survive one follow-up?",
              "That is where most students fold and agree with the examiner.",
              "None of it is personality. All of it is a drill."],
    "cta": "Follow for the rest.",
    "caption": "A speaking assessment is not testing charisma.\n\nIt tests structure: a position, two reasons, back to the position. Then whether that position survives a follow-up question, which is where most students fold.\n\nChildren who look naturally good at this are simply practised.",
    "hashtags": ["#PublicSpeaking", "#IGCSE", "#ChildConfidence", "#Mentorsy"]}},

# -- 20 ------------------------------------------------------------------
{"post": {
    "kind": "quote", "subject": "Mathematics", "pillar": "Parent Scripts",
    "hook": "'She just needs to practise more' is the wrong prescription for a misunderstanding.",
    "attrib": None,
    "caption": "'She just needs to practise more' is the wrong prescription for a misunderstanding.\n\nPractice makes a correct method faster. It also makes an incorrect method faster, and considerably harder to remove, because the wrong step has now been rehearsed forty times.\n\nA child who consistently gets the same kind of question wrong is not under-practised. She is confidently doing something that does not work, and no amount of repetition will point that out.\n\nThe useful move is to watch one question being done out loud. The error is almost always in one specific step, and it is usually visible within ninety seconds.\n\nFind the step first. Then practise.",
    "hashtags": ["#MathsTutoring", "#ParentTips", "#IGCSE", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d50_practice_makes_permanent",
    "subject": "Mathematics", "pillar": "Parent Scripts",
    "hook": "More practice will not fix a misunderstanding.",
    "beats": ["Practice makes a correct method faster.",
              "It makes an incorrect method faster too.",
              "And much harder to remove, because it has been rehearsed.",
              "Watch one question being done out loud instead.",
              "The broken step is usually visible in ninety seconds."],
    "cta": "Follow for the rest.",
    "caption": "More practice will not fix a misunderstanding.\n\nRepetition makes a wrong method faster and harder to unlearn. A child getting the same kind of question wrong is not under-practised, she is confidently doing something that does not work.\n\nWatch one question out loud. Find the step. Then practise.",
    "hashtags": ["#MathsTutoring", "#ParentTips", "#IGCSE", "#Mentorsy"]}},

# -- 21 ------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "French", "pillar": "Inside the Method",
    "hook": "Ten minutes of French on four days beats an hour on Sunday.",
    "points": [
        {"heading": "Language memory decays daily, not weekly"},
        {"heading": "Short sessions keep the sound in the mouth"},
        {"heading": "An hour is mostly re-warming what was lost"},
        {"heading": "Four contacts a week is the floor"},
    ],
    "cta": "Try it for a fortnight.",
    "caption": "Ten minutes of French on four days beats an hour on Sunday.\n\nLanguage sits in memory differently from a maths method. It fades on a daily clock, so a week-long gap means the Sunday hour opens with twenty minutes of recovering ground that was already covered.\n\nFour short contacts keep the sound in the mouth. Pronunciation is muscular as much as mental, and muscles are not maintained weekly.\n\nTen minutes is small enough that nobody negotiates about it, which is the real reason it works. The plan that survives a difficult Tuesday beats the better plan that does not.\n\nSame total time. Different subject by half term.",
    "hashtags": ["#FrenchLearning", "#LanguageLearning", "#StudySkills", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d51_ten_minutes_four_days",
    "subject": "French", "pillar": "Inside the Method",
    "hook": "The Sunday hour is mostly recovery.",
    "beats": ["Language fades on a daily clock, not a weekly one.",
              "So twenty minutes go on ground already covered.",
              "Four short contacts keep the sound in the mouth.",
              "Pronunciation is muscular. Muscles are not maintained weekly.",
              "Ten minutes is small enough that nobody argues about it."],
    "cta": "Follow for the rest.",
    "caption": "The Sunday hour is mostly recovery.\n\nLanguage memory fades daily, so a week-long gap means opening with twenty minutes of re-warming. Four ten-minute contacts keep the sound in the mouth.\n\nSame total time. Different subject by half term.",
    "hashtags": ["#FrenchLearning", "#LanguageLearning", "#StudySkills", "#Mentorsy"]}},

# -- 22 ------------------------------------------------------------------
{"post": {
    "kind": "statement", "subject": "Coding", "pillar": "School Choice",
    "hook": "A coding club is not a coding course.",
    "sub": "Both are worth having. Only one has a sequence.",
    "caption": "A coding club is not a coding course. Both are worth having, and only one of them has a sequence.\n\nA club is exposure. A child turns up, something fun happens, they leave pleased. That is genuinely valuable at eleven, and it is why most children's first contact with programming should be one.\n\nBut a club can run for two years without the difficulty ever rising, because a club is designed so that a child who missed last week can still enjoy this week. That constraint makes progression impossible.\n\nA course has an order, a next thing, and a point at which the previous thing is assumed.\n\nAsk one question: what does week eight assume that week one taught?",
    "hashtags": ["#CodingForKids", "#SchoolChoice", "#STEM", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d52_club_versus_course",
    "subject": "Coding", "pillar": "School Choice",
    "hook": "A coding club is not a coding course.",
    "beats": ["A club is exposure, and that is worth having at eleven.",
              "But a club is built so that missing a week costs nothing.",
              "Which means the difficulty can never rise.",
              "A course has an order and a next thing.",
              "Ask what week eight assumes that week one taught."],
    "cta": "Follow for the rest.",
    "caption": "A coding club is not a coding course.\n\nA club is designed so a child who missed last week still enjoys this week. That constraint is exactly what makes progression impossible.\n\nAsk what week eight assumes that week one taught. If nothing, it is exposure, not a course.",
    "hashtags": ["#CodingForKids", "#SchoolChoice", "#STEM", "#Mentorsy"]}},

# -- 23 ------------------------------------------------------------------
{"post": {
    "kind": "quote", "subject": "Science", "pillar": "Confidence",
    "hook": "A prediction that turned out wrong is the most useful page in the book.",
    "attrib": None,
    "caption": "A prediction that turned out wrong is the most useful page in the book.\n\nStudents learn quickly that predictions are graded socially even when they are not graded formally, so they start writing the safe one, or worse, writing it after the results are in.\n\nAt that point the experiment has stopped being an experiment. Nothing can surprise anyone, and surprise is where the understanding was hiding.\n\nA wrong prediction forces the only question that builds a scientist: what did the model get wrong? That question is the entire subject in six words.\n\nWorth saying out loud at home. A wrong prediction, honestly recorded, is better work than a right one copied off the board.",
    "hashtags": ["#IGCSEScience", "#STEM", "#ChildConfidence", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d53_wrong_prediction",
    "subject": "Science", "pillar": "Confidence",
    "hook": "The wrong prediction is the useful one.",
    "beats": ["Students learn to write the safe prediction.",
              "Or to write it after the results arrive.",
              "At that point nothing can surprise anyone.",
              "And surprise is where the understanding was hiding.",
              "What did the model get wrong? That is the whole subject."],
    "cta": "Follow for the rest.",
    "caption": "The wrong prediction is the useful one.\n\nWhen predictions get written after the results, the experiment stops being an experiment. Nothing can surprise anyone, and surprise is where the learning was.\n\nA wrong prediction honestly recorded is better work than a right one copied off the board.",
    "hashtags": ["#IGCSEScience", "#STEM", "#ChildConfidence", "#Mentorsy"]}},

# -- 24 ------------------------------------------------------------------
{"post": {
    "kind": "compare", "subject": "Mathematics", "pillar": "Future Skills",
    "hook": "Two students with the same maths grade.",
    "left_title": "Grade held together by",
    "left": ["Remembered procedures",
             "Question types seen before",
             "Formulae recalled under pressure",
             "Hoping the paper looks familiar"],
    "right_title": "Grade held together by",
    "right": ["Knowing why the procedure works",
              "Recognising the structure underneath",
              "Deriving what they cannot recall",
              "Coping when the paper looks strange"],
    "cta": "The gap shows up in Year 12, not Year 11.",
    "caption": "Two students with the same maths grade, and two completely different next years.\n\nA grade can be built on remembered procedures or on understood ones, and at IGCSE the paper often cannot tell the difference. Both students walk out with the same letter.\n\nThe gap opens the moment a question arrives in an unfamiliar shape. One student recognises the structure underneath and adapts. The other is waiting to be told which method this is.\n\nThat is why some strong grades turn into a difficult Year 12 and others do not.\n\nThe test at home is small: ask why the method works. If the answer is 'that's just how you do it', the grade is more fragile than it looks.",
    "hashtags": ["#IGCSE", "#ALevel", "#MathsTutoring", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d54_same_grade_different_year",
    "subject": "Mathematics", "pillar": "Future Skills",
    "hook": "Same grade. Completely different next year.",
    "beats": ["A grade can be built on remembered procedures or understood ones.",
              "The paper often cannot tell the difference.",
              "Then a question arrives in an unfamiliar shape.",
              "One student adapts. One waits to be told which method this is.",
              "Ask why the method works. The answer tells you which you have."],
    "cta": "Follow for the rest.",
    "caption": "Same grade. Completely different next year.\n\nA grade built on remembered procedures and one built on understood procedures look identical on results day. They stop looking identical the first time a question arrives in an unfamiliar shape.\n\nAsk why the method works. 'That's just how you do it' is the fragile answer.",
    "hashtags": ["#IGCSE", "#ALevel", "#MathsTutoring", "#Mentorsy"]}},

# -- 25 ------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "AI", "pillar": "Inside the Method",
    "hook": "How AI gets used in a Mentorsy lesson.",
    "points": [
        {"heading": "To generate variations of a question, fast"},
        {"heading": "To play the student the child has to teach"},
        {"heading": "To produce a wrong answer worth arguing with"},
        {"heading": "Never to produce work that gets handed in"},
    ],
    "cta": "Ask any tutor how they use it.",
    "caption": "How AI gets used in a Mentorsy lesson.\n\nMostly as a supply of practice. A tutor who has found a broken step needs eight versions of one question type, and generating those in seconds means the lesson stays on the gap instead of on photocopying.\n\nSometimes as a student. The child explains a topic to it, and the questions that come back expose exactly what they have not understood. Teaching something is the hardest test of knowing it.\n\nSometimes as an opponent, producing a confident wrong solution that the student has to locate the error in.\n\nNever to produce work that gets handed in. That inverts the entire point.",
    "hashtags": ["#AIForKids", "#Mentorsy", "#EdTech", "#IGCSE"]},
 "reel": {
    "kind": "reel", "slug": "d55_ai_in_the_lesson",
    "subject": "AI", "pillar": "Inside the Method",
    "hook": "How AI actually gets used in a lesson.",
    "beats": ["As a supply of practice: eight versions of one question type.",
              "As a student the child has to teach.",
              "The questions it asks back expose what they missed.",
              "As an opponent, producing a confident wrong solution.",
              "Never to produce work that gets handed in."],
    "cta": "Follow for the rest.",
    "caption": "How AI actually gets used in a lesson.\n\nTo generate eight variations of the question that exposed the gap. To play the student a child has to teach. To produce a confident wrong answer worth arguing with.\n\nNever to produce work that gets handed in. That inverts the point.",
    "hashtags": ["#AIForKids", "#EdTech", "#Mentorsy", "#IGCSE"]}},

# -- 26 ------------------------------------------------------------------
{"post": {
    "kind": "statement", "subject": "Public Speaking", "pillar": "Confidence",
    "hook": "The quiet child in class is often the loudest at home.",
    "sub": "That is not personality. That is audience.",
    "caption": "The quiet child in class is often the loudest one at home. That is not personality. That is audience.\n\nA child who talks non-stop across dinner and says nothing in a seminar has all the fluency required. What changes is the cost of being wrong in front of thirty peers, and that cost is real, not imagined.\n\nSo the goal is not to make them talkative. They already are. The goal is to lower the cost, and that is done by making the first contribution small and rehearsed rather than spontaneous and brave.\n\nOne prepared sentence, offered early in the lesson, does more than a term of being told to speak up.\n\nCourage is a bad plan. A prepared opening is a good one.",
    "hashtags": ["#PublicSpeaking", "#ChildConfidence", "#ParentTips", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d56_loudest_at_home",
    "subject": "Public Speaking", "pillar": "Confidence",
    "hook": "The quiet child in class is often the loudest at home.",
    "beats": ["That is not personality. That is audience.",
              "The fluency is already there.",
              "What changed is the cost of being wrong in front of thirty peers.",
              "So do not aim for brave. Aim for rehearsed.",
              "One prepared sentence, offered early, beats a term of 'speak up'."],
    "cta": "Follow for the rest.",
    "caption": "The quiet child in class is often the loudest at home.\n\nNot personality. Audience. The fluency is already there; what changed is the cost of being wrong in front of thirty peers.\n\nOne prepared sentence offered early in the lesson does more than a term of being told to speak up.",
    "hashtags": ["#PublicSpeaking", "#ChildConfidence", "#ParentTips", "#Mentorsy"]}},

# -- 27 ------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Mathematics", "pillar": "Curriculum Decoded",
    "hook": "The Year 7 topic that keeps costing marks in Year 11.",
    "points": [
        {"heading": "Fractions arrive early and never leave"},
        {"heading": "Algebraic fractions are the same skill, renamed"},
        {"heading": "Probability, ratio and rates all sit on top of it"},
        {"heading": "Nobody reteaches it after Year 8"},
    ],
    "cta": "Test it tonight in two minutes.",
    "caption": "The Year 7 topic that keeps costing marks in Year 11: fractions.\n\nThey arrive early, get marked as done, and then quietly underpin ratio, probability, rates of change, rearranging and every algebraic fraction that follows. The topic never leaves. It just stops being called fractions.\n\nWhich is why a Year 11 losing marks across several apparently unrelated topics is often losing them to one thing, four years upstream.\n\nAnd nothing in the timetable will catch it, because nobody reteaches fractions after Year 8.\n\nTest it tonight. Ask for three-quarters divided by two-fifths, on paper, with the reasoning said out loud. Two minutes, and it is a genuinely useful two minutes.",
    "hashtags": ["#IGCSE", "#MathsTutoring", "#ParentTips", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d57_fractions_upstream",
    "subject": "Mathematics", "pillar": "Curriculum Decoded",
    "hook": "The Year 11 problem started in Year 7.",
    "beats": ["Fractions arrive early and get marked as done.",
              "Then they hold up ratio, probability, rates and rearranging.",
              "The topic never leaves. It stops being called fractions.",
              "Marks lost across unrelated topics are often one gap, upstream.",
              "Nobody reteaches it after Year 8."],
    "cta": "Follow for the rest.",
    "caption": "The Year 11 problem started in Year 7.\n\nFractions get marked as done and then quietly underpin ratio, probability, rates and every algebraic fraction that follows. Marks lost across several unrelated topics are often one gap, four years upstream.\n\nAsk for three-quarters divided by two-fifths tonight, with the reasoning out loud.",
    "hashtags": ["#IGCSE", "#MathsTutoring", "#ParentTips", "#Mentorsy"]}},

# -- 28 ------------------------------------------------------------------
{"post": {
    "kind": "quote", "subject": "French", "pillar": "Parent Scripts",
    "hook": "Correcting the accent at the dinner table costs more than it fixes.",
    "attrib": None,
    "caption": "Correcting the accent at the dinner table costs more than it fixes.\n\nA child trying French out loud at home is doing the single most difficult and most valuable thing in the subject: producing language with no script, in front of people whose opinion matters more than any examiner's.\n\nInterrupt that to fix a vowel and the calculation changes. Speaking now carries a risk that silence does not, and the sentence stops coming.\n\nCorrection belongs in the lesson, where it is expected and where it is the job. At home the useful response is to reply in French if you can, or to ask what the sentence meant if you cannot.\n\nKeep the sentences coming. Accuracy has a whole term to arrive.",
    "hashtags": ["#FrenchLearning", "#ParentTips", "#LanguageLearning", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d58_dont_correct_at_dinner",
    "subject": "French", "pillar": "Parent Scripts",
    "hook": "Do not correct the accent at the dinner table.",
    "beats": ["A child speaking French at home is doing the hardest thing there is.",
              "No script, in front of people whose opinion actually matters.",
              "Fix a vowel and speaking now carries a risk silence does not.",
              "So the sentence stops coming.",
              "Correction belongs in the lesson. At home, keep it coming."],
    "cta": "Follow for the rest.",
    "caption": "Do not correct the accent at the dinner table.\n\nA child speaking French at home is producing language with no script, in front of the audience that matters most. Interrupting to fix a vowel makes speaking riskier than silence.\n\nCorrection belongs in the lesson. Accuracy has a whole term to arrive.",
    "hashtags": ["#FrenchLearning", "#ParentTips", "#LanguageLearning", "#Mentorsy"]}},

# -- 29 ------------------------------------------------------------------
{"post": {
    "kind": "compare", "subject": "AI", "pillar": "School Choice",
    "hook": "Two schools answering the same question about AI.",
    "left_title": "Has a slogan",
    "left": ["'We've banned it'",
             "'We embrace innovation'",
             "'Our policy is under review'",
             "'Teachers use their judgement'"],
    "right_title": "Has a policy",
    "right": ["'Allowed for research, not for drafting'",
              "'Declared at the top of the work'",
              "'More assessment done in class'",
              "'Here it is in writing'"],
    "cta": "Ask for the policy, not the position.",
    "caption": "Two schools answering the same question about AI.\n\nA ban is a position, not a policy. It tells you what the school disapproves of and nothing about what happens to a specific piece of homework on a specific Tuesday.\n\nA policy names what is allowed, what has to be declared, and how the school is changing assessment in response. That last part is the one worth listening for, because it is the only one that costs the school something.\n\nSchools that have moved more assessment into the classroom have actually thought about this. Schools with a strong opinion and unchanged coursework have not.\n\nAsk for the document. A school that has one will be glad to hand it over.",
    "hashtags": ["#AIForKids", "#SchoolChoice", "#DubaiSchools", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d59_policy_not_position",
    "subject": "AI", "pillar": "School Choice",
    "hook": "A ban is a position, not a policy.",
    "beats": ["It says what the school disapproves of.",
              "Not what happens to a piece of homework on a Tuesday.",
              "A policy names what is allowed and what must be declared.",
              "And how assessment has changed in response.",
              "That last part is the only one that costs the school something."],
    "cta": "Follow for the rest.",
    "caption": "A ban is a position, not a policy.\n\nAsk what is allowed, what must be declared, and how assessment has changed in response. The last one matters most, because it is the only answer that costs the school something.\n\nAsk for the document. A school that has one will hand it over.",
    "hashtags": ["#SchoolChoice", "#AIForKids", "#DubaiSchools", "#Mentorsy"]}},

# -- 30 ------------------------------------------------------------------
{"post": {
    "kind": "statement", "subject": "Coding", "pillar": "Curriculum Decoded",
    "hook": "Scratch is not a toy that gets outgrown.",
    "sub": "It is the same ideas without the punctuation.",
    "caption": "Scratch is not a toy that gets outgrown. It is the same ideas without the punctuation.\n\nLoops, conditionals, variables, events, sequence: those are the concepts a first-year computer science course teaches, and a nine year old can hold all of them while dragging blocks. What text adds is syntax, and syntax is not the difficult part.\n\nParents often push a child out of blocks early, worried it looks unserious. The usual result is a child fighting missing semicolons instead of thinking about structure, and concluding they are bad at coding.\n\nThe right moment to move across is when the blocks become the slow part, not when the calendar says so.\n\nA child who can debug a Scratch project can debug anything. The rest is typing.",
    "hashtags": ["#CodingForKids", "#STEM", "#FutureSkills", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d60_scratch_is_not_a_toy",
    "subject": "Coding", "pillar": "Curriculum Decoded",
    "hook": "Scratch is not a toy that gets outgrown.",
    "beats": ["Loops, conditionals, variables, events, sequence.",
              "Those are first-year computer science concepts.",
              "What text adds is syntax, and syntax is not the hard part.",
              "Push a child out early and they fight semicolons instead of structure.",
              "Move across when the blocks become the slow part."],
    "cta": "Follow for the rest.",
    "caption": "Scratch is not a toy that gets outgrown.\n\nLoops, conditionals, variables and events are the same concepts a first computer science course teaches. Text adds syntax, and syntax is the cheap part.\n\nMove across when the blocks become the slow part, not when the calendar says so.",
    "hashtags": ["#CodingForKids", "#STEM", "#FutureSkills", "#Mentorsy"]}},

]
