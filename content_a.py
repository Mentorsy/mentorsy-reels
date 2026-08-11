"""
Mentorsy - content bank, part one (days 1-15)

Two pieces a day: a feed post at 09:00 IST and a reel at 20:30 IST.

09:00 IST is 07:30 in Dubai, which is the school run - the window where a
parent is holding a phone and thinking about their child's day. 20:30 IST is
19:00 Dubai, 16:00 London and 11:00 New York, the one slot that is a
reasonable hour in all three markets at once.

Voice rules, applied throughout:
  - never first person singular. Mentorsy has hired teachers; the page is the
    company, not one person
  - name the specific year group, board or topic. "Year 9 tier entry" earns
    trust that "we help students succeed" cannot
  - the hook states a claim, the body pays it off. no cliffhangers that go
    nowhere
"""

DAYS_A = [

# -- 1 -------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Mathematics", "pillar": "Parent Scripts",
    "hook": "What a maths report tells you, and what it hides.",
    "points": [
        {"heading": "A percentage is an average of averages"},
        {"heading": "'Could apply himself' usually means one topic"},
        {"heading": "Effort grades measure compliance, not learning"},
        {"heading": "Ask for the question-level breakdown"},
    ],
    "cta": "Save this before the next report evening.",
    "caption": "A maths report is an average of averages.\n\n62 percent might be strong algebra and collapsed geometry, or steady mediocrity across everything. Those need opposite responses, and the number cannot tell them apart.\n\nAsk for the question-level breakdown. Most schools have it and rarely send it unprompted.\n\nThat one request changes the whole conversation.",
    "hashtags": ["#IGCSE", "#ParentTips", "#CambridgeCurriculum", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d01_report_number",
    "subject": "Mathematics", "pillar": "Parent Scripts",
    "hook": "The number on the report is the least useful thing on it.",
    "beats": ["62 percent could be two completely different children.",
              "Strong algebra, collapsed geometry.",
              "Or steady mediocrity in everything.",
              "Same number. Opposite problem.",
              "Ask which questions cost the marks."],
    "cta": "Follow for the questions that work.",
    "caption": "The number on the report is the least useful thing on it.\n\n62 percent could be strong algebra with collapsed geometry, or steady mediocrity across the board. Same number, opposite problem, opposite fix.\n\nAsk which questions cost the marks. That is the only part you can act on.",
    "hashtags": ["#IGCSE", "#MathsTutoring", "#ParentTips", "#Mentorsy"]}},

# -- 2 -------------------------------------------------------------------
{"post": {
    "kind": "statement", "subject": "Public Speaking", "pillar": "Confidence",
    "hook": "Your child is not shy.", "sub": "They are unrehearsed.",
    "caption": "Your child is not shy. They are unrehearsed.\n\nShyness sounds like a personality, which makes it sound permanent. Unrehearsed is a state, and states change with repetition.\n\nNobody is fluent the first time they say a sentence out loud in front of people. They are fluent the ninth time.\n\nThe gap between those two is not courage. It is practice nobody scheduled.",
    "hashtags": ["#PublicSpeaking", "#ChildConfidence", "#Mentorsy", "#DubaiSchools"]},
 "reel": {
    "kind": "reel", "slug": "d02_unrehearsed",
    "subject": "Public Speaking", "pillar": "Confidence",
    "hook": "Nobody is confident the first time.",
    "beats": ["Shyness is a personality. Unrehearsed is a state.",
              "One sounds permanent. The other takes four weeks.",
              "Nobody is fluent the first time they speak in front of people.",
              "They are fluent the ninth time.",
              "The gap is not courage. It is practice nobody scheduled."],
    "cta": "Follow for the rest.",
    "caption": "Nobody is confident the first time.\n\nShyness sounds like a personality, which makes it sound permanent. Unrehearsed is a state, and states change.\n\nThe difference between a child who freezes and a child who presents is usually eight rehearsals nobody scheduled.",
    "hashtags": ["#PublicSpeaking", "#ChildConfidence", "#Mentorsy", "#ParentTips"]}},

# -- 3 -------------------------------------------------------------------
{"post": {
    "kind": "compare", "subject": "Coding", "pillar": "Future Skills",
    "hook": "Two ways to teach a child to code.",
    "left_title": "Looks like progress",
    "left": ["Finishing a course", "Copying a tutorial exactly",
             "Certificates", "Learning six languages"],
    "right_title": "Is progress",
    "right": ["Finishing a thing that works", "Fixing it when it breaks",
              "Explaining it to someone", "Getting good at one language"],
    "cta": "Ask which column their class is in.",
    "caption": "Two ways to teach a child to code, and only one of them compounds.\n\nCourse completion is easy to measure, which is why it gets measured. But a child who has finished nine tutorials and never debugged anything has not learned to program. They have learned to type.\n\nThe skill is what happens after it breaks.\n\nAsk any coding class what a student does in week three when their code does not run. The answer tells you which column you are buying.",
    "hashtags": ["#CodingForKids", "#FutureSkills", "#STEM", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d03_after_it_breaks",
    "subject": "Coding", "pillar": "Future Skills",
    "hook": "Nine finished tutorials is not learning to code.",
    "beats": ["Copying a tutorial teaches typing.",
              "The learning happens when it breaks.",
              "And nothing in a finished tutorial ever breaks.",
              "Ask what your child does in week three when the code fails.",
              "That answer is the whole course."],
    "cta": "Follow for the rest.",
    "caption": "Nine finished tutorials is not learning to code.\n\nCopying a tutorial line by line teaches typing. The learning happens when something breaks and a child has to work out why, and nothing in a finished tutorial ever breaks.\n\nAsk what happens in week three when the code will not run.",
    "hashtags": ["#CodingForKids", "#STEM", "#FutureSkills", "#Mentorsy"]}},

# -- 4 -------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Mathematics", "pillar": "Curriculum Decoded",
    "hook": "The Year 9 decision most parents make by accident.",
    "points": [
        {"heading": "Set placement in Year 9 shapes Year 12"},
        {"heading": "Foundation tier caps the grade, quietly"},
        {"heading": "Moving up is possible, but the evidence has to exist"},
        {"heading": "The window is roughly eighteen months"},
    ],
    "cta": "Send this to a parent with a child in Year 9.",
    "caption": "The Year 9 decision most parents make by accident.\n\nSet placement decides which tier your child is entered for, and the tier caps the grade available. That narrows what they can take at A Level, years before anyone mentions A Levels.\n\nMost families find out on results day.\n\nAsk which tier your child is on track for. Ask in Year 9, not Year 11.",
    "hashtags": ["#IGCSE", "#CambridgeCurriculum", "#DubaiSchools", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d04_tier_ceiling",
    "subject": "Mathematics", "pillar": "Curriculum Decoded",
    "hook": "The ceiling is set long before results day.",
    "beats": ["Tier entry is decided in Year 9.",
              "Foundation tier caps the grade available.",
              "That decides what is possible at A Level.",
              "Most families find out when the results arrive.",
              "Ask which tier. Ask now."],
    "cta": "Follow for the rest.",
    "caption": "The ceiling is set long before results day.\n\nTier entry gets decided around Year 9, often on one year of marks, and the tier caps the grade available. That quietly decides what is open at A Level.\n\nAsk which tier your child is on track for. There is still time to change the answer.",
    "hashtags": ["#IGCSE", "#CambridgeCurriculum", "#ParentTips", "#Mentorsy"]}},

# -- 5 -------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "AI", "pillar": "Future Skills",
    "hook": "What to actually teach a child about AI.",
    "points": [
        {"heading": "How to check whether an answer is true"},
        {"heading": "Where the answer came from"},
        {"heading": "What it is confidently wrong about"},
        {"heading": "When not to use it at all"},
    ],
    "cta": "Save this for the next homework argument.",
    "caption": "What to actually teach a child about AI.\n\nNot prompting. Prompting will be obsolete in two years and it was never the hard part.\n\nThe durable skill is judgement: knowing when the answer is wrong, where it came from, and when the tool should stay closed. A child who can spot a confident wrong answer is more employable than one who can write a clever prompt.\n\nThat skill is just critical thinking with a new surface. Which is good news, because we already know how to teach it.",
    "hashtags": ["#AIForKids", "#FutureSkills", "#DigitalLiteracy", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d05_ai_judgement",
    "subject": "AI", "pillar": "Future Skills",
    "hook": "Stop teaching children to prompt.",
    "beats": ["Prompting will be obsolete in two years.",
              "It was never the hard part.",
              "The hard part is knowing when the answer is wrong.",
              "A child who can catch a confident mistake is employable.",
              "That is not a tech skill. It is thinking."],
    "cta": "Follow for the rest.",
    "caption": "Stop teaching children to prompt.\n\nPrompting will be obsolete in two years and it was never the hard part. The durable skill is catching a confident wrong answer, knowing where it came from, and knowing when to close the tab.\n\nThat is critical thinking with a new surface.",
    "hashtags": ["#AIForKids", "#DigitalLiteracy", "#FutureSkills", "#Mentorsy"]}},

# -- 6 -------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "French", "pillar": "Inside the Method",
    "hook": "Why your child can pass French and still not speak it.",
    "points": [
        {"heading": "Written exams reward recall, not retrieval"},
        {"heading": "Vocabulary lists are stored, never used"},
        {"heading": "Grammar is taught before anything is said"},
        {"heading": "Nobody has ever had to answer quickly"},
    ],
    "cta": "Ask when your child last spoke French unscripted.",
    "caption": "Why a child can score well in French and still freeze in Paris.\n\nWritten exams reward recall. Speaking requires retrieval under time pressure, which is a different skill using a different part of the memory, and almost nothing in a school term practises it.\n\nA vocabulary list learned on Sunday and tested on Friday is stored, not owned.\n\nAsk when your child last had to answer a question in French without knowing it was coming.",
    "hashtags": ["#FrenchLearning", "#LanguageLearning", "#IGCSE", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d06_french_freeze",
    "subject": "French", "pillar": "Inside the Method",
    "hook": "Good at French. Cannot speak French.",
    "beats": ["Written exams reward recall.",
              "Speaking requires retrieval, under time pressure.",
              "Different skill. Different part of the memory.",
              "A list learned Sunday and tested Friday is stored, not owned.",
              "When did they last answer without warning?"],
    "cta": "Follow for the rest.",
    "caption": "Good at French. Cannot speak French.\n\nWritten exams reward recall. Speaking requires retrieval under time pressure, and almost nothing in a school term practises it.\n\nAsk when your child last answered a question in French without knowing it was coming.",
    "hashtags": ["#FrenchLearning", "#LanguageLearning", "#Mentorsy", "#ParentTips"]}},

# -- 7 -------------------------------------------------------------------
{"post": {
    "kind": "quote", "subject": "Mentorsy", "pillar": "Confidence",
    "hook": "A child who says they are bad at maths is usually describing one afternoon in Year 6.",
    "attrib": None,
    "caption": "A child who says they are bad at maths is usually describing one afternoon in Year 6.\n\nAlmost every 'I'm just not a maths person' traces back to a specific moment: a topic that arrived before the last one closed, a question asked in front of people, a comment that landed harder than the teacher meant.\n\nThe belief outlives the incident by a decade.\n\nIt is worth asking when they first decided it. The answer is often surprisingly precise, and things you can date are things you can undo.",
    "hashtags": ["#MathsConfidence", "#ChildConfidence", "#ParentTips", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d07_one_afternoon",
    "subject": "Mentorsy", "pillar": "Confidence",
    "hook": "Ask when they decided they were bad at it.",
    "beats": ["'I'm not a maths person' is not an assessment.",
              "It is a memory.",
              "Usually one topic, one question, one afternoon.",
              "The belief outlives the incident by ten years.",
              "Things you can date are things you can undo."],
    "cta": "Follow for the rest.",
    "caption": "Ask when they decided they were bad at it.\n\nAlmost every 'I'm not a maths person' traces to a specific moment. The belief outlives the incident by a decade.\n\nThings you can date are things you can undo.",
    "hashtags": ["#MathsConfidence", "#ChildConfidence", "#Mentorsy", "#ParentTips"]}},

# -- 8 -------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Science", "pillar": "Inside the Method",
    "hook": "Four science questions that reveal whether a child understands.",
    "points": [
        {"heading": "What would change if this were not true?"},
        {"heading": "Where have you seen this outside the book?"},
        {"heading": "What is this a special case of?"},
        {"heading": "What would you measure to test it?"},
    ],
    "cta": "Try one tonight. It takes two minutes.",
    "caption": "Four questions that reveal whether a child understands science or has memorised it.\n\nNone of them ask for a definition. A definition can be recited by a child who has understood nothing, which is why exams stopped rewarding them.\n\nThese four ask what the idea is connected to. Understanding is a shape, not a fact, and you can only see the shape from the edges.\n\nTry one tonight over dinner. Two minutes, no marking, and you will know more than the last report told you.",
    "hashtags": ["#ScienceEducation", "#IGCSE", "#ParentTips", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d08_understanding_shape",
    "subject": "Science", "pillar": "Inside the Method",
    "hook": "Definitions prove nothing.",
    "beats": ["A child can recite a definition having understood nothing.",
              "Ask instead: what would change if this were not true?",
              "Where have you seen it outside the book?",
              "What would you measure to test it?",
              "Understanding is a shape. You see it from the edges."],
    "cta": "Follow for the rest.",
    "caption": "Definitions prove nothing.\n\nA child can recite one having understood nothing, which is why exams stopped rewarding them.\n\nAsk what would change if it were not true. Ask what they would measure. Understanding is a shape, and you can only see it from the edges.",
    "hashtags": ["#ScienceEducation", "#IGCSE", "#Mentorsy", "#ParentTips"]}},

# -- 9 -------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Mathematics", "pillar": "Inside the Method",
    "hook": "The five-minute check that finds the gap.",
    "points": [
        {"heading": "Ask them to explain, not to solve"},
        {"heading": "Go back two years, not two weeks"},
        {"heading": "Watch where they stop, not what they answer"},
        {"heading": "Do it without a grade attached"},
    ],
    "cta": "Try this tonight.",
    "caption": "Five minutes, and no marking.\n\nGive your child a question they already got right, and ask why the method works. Fluency without understanding shows up in seconds, and it is the best early warning there is.\n\nThen set one from two years earlier. Watch where they pause, not what they answer.\n\nThe hesitation is the diagnosis.",
    "hashtags": ["#IGCSE", "#MathsTutoring", "#ParentTips", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d09_five_minute",
    "subject": "Mathematics", "pillar": "Inside the Method",
    "hook": "Five minutes. No marking.",
    "beats": ["Take a question they already got right.",
              "Ask why the method works.",
              "Fluency without understanding shows up immediately.",
              "Then set one from two years earlier.",
              "Watch the pause. The pause is the diagnosis."],
    "cta": "Follow for the rest.",
    "caption": "Five minutes, no marking.\n\nGive your child a question they got right and ask why the method works. Then set one from two years earlier.\n\nWatch where they pause, not what they answer. The hesitation is the diagnosis.",
    "hashtags": ["#IGCSE", "#MathsTutoring", "#ParentTips", "#Mentorsy"]}},

# -- 10 ------------------------------------------------------------------
{"post": {
    "kind": "statement", "subject": "Coding", "pillar": "Confidence",
    "hook": "Getting stuck is the subject.", "sub": "Not an interruption to it.",
    "caption": "In coding, getting stuck is the subject. It is not an interruption to it.\n\nEvery professional developer spends most of the day with something not working. That is not a sign of failing, it is the actual job, and a child who thinks being stuck means being bad will quit somewhere around week three.\n\nWorth saying out loud early: this is meant to be hard, everyone's code breaks, and finding out why is the part you are learning.",
    "hashtags": ["#CodingForKids", "#ChildConfidence", "#STEM", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d10_stuck_is_the_subject",
    "subject": "Coding", "pillar": "Confidence",
    "hook": "Getting stuck is the subject.",
    "beats": ["Every developer spends most of the day with something broken.",
              "That is not failing. That is the job.",
              "A child who thinks stuck means bad will quit in week three.",
              "Say it out loud early.",
              "This is meant to be hard."],
    "cta": "Follow for the rest.",
    "caption": "Getting stuck is the subject, not an interruption to it.\n\nEvery professional developer spends most of the day with something not working. A child who thinks being stuck means being bad at it quits around week three.\n\nSay it out loud early.",
    "hashtags": ["#CodingForKids", "#STEM", "#ChildConfidence", "#Mentorsy"]}},

# -- 11 ------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Public Speaking", "pillar": "Parent Scripts",
    "hook": "What to say the night before they present.",
    "points": [
        {"heading": "'You know this bit best' - name the bit"},
        {"heading": "'Nobody can tell you are nervous'"},
        {"heading": "'Slow is the only trick that works'"},
        {"heading": "Not: 'just be confident'"},
    ],
    "cta": "Save this for the next one.",
    "caption": "What to say the night before your child presents.\n\n'Just be confident' asks them to produce a feeling on demand, which nobody can do. It reads as pressure, not support.\n\nWhat works is specific and physical. Name the part they know best, so they have somewhere solid to start. Tell them nobody can see nerves, because it is true and they assume otherwise. And tell them to go slower than feels right, because speed is what nerves do to a voice and slowing down is the only lever they can actually pull mid-sentence.",
    "hashtags": ["#PublicSpeaking", "#ParentTips", "#ChildConfidence", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d11_night_before",
    "subject": "Public Speaking", "pillar": "Parent Scripts",
    "hook": "Never say 'just be confident'.",
    "beats": ["It asks for a feeling on demand. Nobody can do that.",
              "Say this instead.",
              "'You know this part best.' Name the part.",
              "'Nobody can tell you are nervous.' They cannot.",
              "'Go slower than feels right.' That one always works."],
    "cta": "Follow for the rest.",
    "caption": "Never say 'just be confident'.\n\nIt asks a child to produce a feeling on demand and reads as pressure.\n\nName the part they know best. Tell them nerves are invisible. Tell them to go slower than feels right - it is the only lever they can pull mid-sentence.",
    "hashtags": ["#PublicSpeaking", "#ParentTips", "#ChildConfidence", "#Mentorsy"]}},

# -- 12 ------------------------------------------------------------------
{"post": {
    "kind": "compare", "subject": "Mathematics", "pillar": "School Choice",
    "hook": "IGCSE or IB Maths: what actually matters.",
    "left_title": "What parents compare",
    "left": ["Which is harder", "Which universities prefer",
             "Reputation of the board", "What friends chose"],
    "right_title": "What decides the grade",
    "right": ["Periods per week for maths", "Who teaches the top set",
              "How the school handles falling behind",
              "Whether your child likes closing or connecting"],
    "cta": "Send this to a parent choosing right now.",
    "caption": "IGCSE or IB Maths?\n\nNeither opens more doors on its own. Admissions read the grade and the depth, not the acronym.\n\nThe column on the right predicts outcomes far better than the column on the left, and almost nobody asks about it on an open day.\n\nOne genuinely useful signal: a child who likes closing a problem cleanly tends to thrive in IGCSE. One who enjoys connecting ideas across subjects usually prefers IB. Choose for the child you have.",
    "hashtags": ["#IGCSE", "#IBMaths", "#DubaiSchools", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d12_igcse_or_ib",
    "subject": "Mathematics", "pillar": "School Choice",
    "hook": "IGCSE or IB? Wrong question.",
    "beats": ["Admissions read the grade and the depth. Not the acronym.",
              "Ask how many periods a week the school gives maths.",
              "Ask who teaches the top set.",
              "Ask what happens when a student falls behind.",
              "Those three predict the grade. The badge does not."],
    "cta": "Follow for the rest.",
    "caption": "IGCSE or IB? It is the wrong question.\n\nAdmissions read the grade and the depth, not the acronym. Ask how many periods a week the school gives to maths and who teaches the top set.\n\nThose predict outcomes. The badge does not.",
    "hashtags": ["#IGCSE", "#IBMaths", "#DubaiSchools", "#Mentorsy"]}},

# -- 13 ------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "AI", "pillar": "Parent Scripts",
    "hook": "Your child used AI for their homework. Now what?",
    "points": [
        {"heading": "Ask them to explain it without the screen"},
        {"heading": "Find the one sentence they cannot defend"},
        {"heading": "Agree what it is allowed to do next time"},
        {"heading": "Do not ban it. It will just go underground"},
    ],
    "cta": "Save this before the argument.",
    "caption": "Your child used AI for their homework. The ban does not work.\n\nIt only moves the behaviour somewhere you cannot see, and removes your ability to teach anything about it.\n\nWhat works is asking them to explain the work without the screen. The gap shows up in about ninety seconds, and it shows up to them, not just to you. That is a far better lesson than a rule.\n\nThen agree what the tool is allowed to do next time. Explain a concept, yes. Write the paragraph, no. Children keep rules they helped write.",
    "hashtags": ["#AIForKids", "#ParentTips", "#DigitalLiteracy", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d13_ai_homework",
    "subject": "AI", "pillar": "Parent Scripts",
    "hook": "Banning AI does not work.",
    "beats": ["It moves the behaviour somewhere you cannot see.",
              "Instead: ask them to explain it without the screen.",
              "The gap shows up in ninety seconds.",
              "And it shows up to them, not just to you.",
              "Then agree the rules together. They keep those."],
    "cta": "Follow for the rest.",
    "caption": "Banning AI does not work. It moves the behaviour somewhere you cannot see.\n\nAsk them to explain the work without the screen. The gap shows up in ninety seconds, and it shows up to them.\n\nThen agree the rules together. Children keep rules they helped write.",
    "hashtags": ["#AIForKids", "#ParentTips", "#DigitalLiteracy", "#Mentorsy"]}},

# -- 14 ------------------------------------------------------------------
{"post": {
    "kind": "list", "subject": "Mentorsy", "pillar": "Parent Scripts",
    "hook": "Four questions before you pay a tutor anything.",
    "points": [
        {"heading": "What will you do in the first session?"},
        {"heading": "How will I know it is working?"},
        {"heading": "What happens when she gets stuck?"},
        {"heading": "Who else have you taught at this level?"},
    ],
    "cta": "Ask these before the first invoice.",
    "caption": "Four questions before you pay a tutor anything.\n\nThe first one does most of the work. If the answer is 'start the syllabus', walk away - it assumes the problem is coverage, and it almost never is.\n\nA good tutor names a measure before they begin. 'More confident' is not a measure. 'She will close negative numbers in three weeks' is.\n\nAnd listen carefully to the third answer. Explaining again, louder, is not teaching. Going backwards to find the missing step is.",
    "hashtags": ["#MathsTutoring", "#ParentTips", "#IGCSE", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d14_tutor_questions",
    "subject": "Mentorsy", "pillar": "Parent Scripts",
    "hook": "Four questions before you pay a tutor.",
    "beats": ["What will you do in the first session?",
              "If the answer is 'start the syllabus', walk away.",
              "How will I know it is working? Make them name a measure.",
              "What happens when she gets stuck?",
              "Explaining louder is not teaching."],
    "cta": "Follow for the rest.",
    "caption": "Four questions before you pay a tutor anything.\n\nThe first one does most of the work. If the answer is 'start the syllabus', walk away - it assumes the problem is coverage, and it almost never is.\n\nA good tutor names a measure before they begin.",
    "hashtags": ["#MathsTutoring", "#ParentTips", "#IGCSE", "#Mentorsy"]}},

# -- 15 ------------------------------------------------------------------
{"post": {
    "kind": "statement", "subject": "Mathematics", "pillar": "Confidence",
    "hook": "Working hard on the wrong topic is still working hard.",
    "sub": "It just does not move the grade.",
    "caption": "Working hard on the wrong topic is still working hard.\n\nIt is the most expensive kind of effort, because the child pays for it in confidence and gets nothing back. Three months of revision, no movement, and the only conclusion available to a fourteen year old is that they must be the problem.\n\nThey are not. The sequence is.\n\nFind the gap first. Then the hours count.",
    "hashtags": ["#MathsConfidence", "#IGCSE", "#ALevelMaths", "#Mentorsy"]},
 "reel": {
    "kind": "reel", "slug": "d15_wrong_topic",
    "subject": "Mathematics", "pillar": "Confidence",
    "hook": "Three months of revision. No movement.",
    "beats": ["Working hard on the wrong topic is still working hard.",
              "It is just the most expensive kind.",
              "The child pays in confidence and sees nothing back.",
              "And concludes they are the problem.",
              "They are not. The sequence is."],
    "cta": "Follow for the rest.",
    "caption": "Three months of revision, no movement.\n\nWorking hard on the wrong topic is still working hard. It is just the most expensive kind, because the child pays in confidence and gets nothing back.\n\nFind the gap first. Then the hours count.",
    "hashtags": ["#MathsConfidence", "#IGCSE", "#ParentTips", "#Mentorsy"]}},
]
