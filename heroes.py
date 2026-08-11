"""
Mentorsy - hero reel scripts

Two a month, dated. The builder gives each one the evening slot on its day,
overwriting the ordinary reel rather than adding a third piece.

Why two and not more: the hero is the reel with a human face in it, and a face
is only an event while it is rare. Twice a month it still reads as "the one
where someone talks". Weekly and it becomes the format, at which point the
face has to be the same person every time or the brand looks unstable.

Writing rules specific to these:

  - the SPOKEN line is under 25 words. Ten seconds is shorter than it sounds,
    and a rushed delivery loses the calm that makes a face worth showing
  - the spoken line and the first b-roll caption must not repeat each other.
    The face opens the argument, the type continues it
  - no first person singular, same as everywhere else
  - spend the face on the claim that most needs trusting. A fact can be read;
    a judgement is worth hearing someone say
"""

HEROES = {

# -- September ------------------------------------------------------------

"hero_2026_09a": {
    "date": "2026-09-15",
    "subject": "Mathematics",
    "pillar": "Curriculum Decoded",
    "hook": "Your child is not behind in maths.",
    "spoken": ("Your child is not behind in maths. A topic was left "
               "unfinished, and everything after it inherited the gap."),
    "broll": [
        {"query": "student exam paper hands desk",
         "caption": "Fractions in Year 7. Negative numbers in Year 8."},
        {"query": "empty classroom chair afternoon light",
         "caption": "Ratio, algebra and trigonometry all sit on top of them."},
        {"query": "classroom wall clock",
         "caption": "Neither is ever formally revisited."},
        {"query": "notebook pen close up study",
         "caption": "So a thin Year 7 becomes a difficult Year 11."},
        {"query": "teenager studying window light",
         "caption": "It looks like they got worse. The building got taller."},
    ],
    "cta": "Sequence problems have solutions.",
    "caption": "Your child is not behind in maths.\n\nA topic was left unfinished, and everything built on top of it inherited the gap. Fractions in Year 7, negative numbers in Year 8 - ratio, algebra and trigonometry all sit on those two, and neither is ever formally revisited.\n\nSo a thin Year 7 becomes a difficult Year 11, and it looks like the student got worse. They did not. The foundation was always thin and the building got taller.\n\nThat is a sequence problem, not an ability problem. Sequence problems have solutions.",
    "hashtags": ["#IGCSE", "#CambridgeCurriculum", "#MathsTutoring", "#Mentorsy"],
},

"hero_2026_09b": {
    "date": "2026-09-29",
    "subject": "Mentorsy",
    "pillar": "Parent Scripts",
    "hook": "Ask a tutor one question before you pay them.",
    "spoken": ("Ask a tutor one question before you pay them. What will you "
               "do in the first session? The answer tells you everything."),
    "broll": [
        {"query": "notebook pen desk close up",
         "caption": "If the answer is 'start the syllabus', walk away."},
        {"query": "student exam paper marked",
         "caption": "That assumes the problem is coverage."},
        {"query": "empty desk classroom quiet",
         "caption": "It almost never is."},
        {"query": "teenager studying alone",
         "caption": "Nobody can teach a gap they have not located."},
    ],
    "cta": "The first hour should be diagnosis.",
    "caption": "Ask a tutor one question before you pay them anything.\n\n\"What will you do in the first session?\"\n\nIf the answer is \"start the syllabus\", walk away. Starting the syllabus on day one assumes the problem is coverage, and it almost never is. It is usually one unfinished topic somewhere behind, quietly making everything above it harder.\n\nNobody can teach a gap they have not located. The first hour should be diagnosis, not chapter one.",
    "hashtags": ["#MathsTutoring", "#ParentTips", "#IGCSE", "#Mentorsy"],
},

# -- October --------------------------------------------------------------

"hero_2026_10a": {
    "date": "2026-10-13",
    "subject": "Public Speaking",
    "pillar": "Confidence",
    "hook": "Your child is not shy. They are unrehearsed.",
    "spoken": ("Your child is not shy. They are unrehearsed. And one of "
               "those two things changes in about four weeks."),
    "broll": [
        {"query": "empty school hall stage",
         "caption": "Shyness sounds like a personality."},
        {"query": "microphone stand empty room",
         "caption": "Unrehearsed is a state."},
        {"query": "student notes paper hands",
         "caption": "Nobody is fluent the first time they speak to a room."},
        {"query": "school corridor students",
         "caption": "They are fluent the ninth time."},
        {"query": "teenager presenting classroom",
         "caption": "The gap is not courage. It is practice nobody scheduled."},
    ],
    "cta": "Start earlier than feels necessary.",
    "caption": "Your child is not shy. They are unrehearsed.\n\nShyness sounds like a personality, which makes it sound permanent. Unrehearsed is a state, and states change with repetition.\n\nNobody is fluent the first time they say a sentence out loud in front of people. They are fluent the ninth time. The difference between a child who freezes and a child who presents is usually eight rehearsals nobody scheduled.\n\nSpeaking also improves faster than almost anything else on a timetable.",
    "hashtags": ["#PublicSpeaking", "#ChildConfidence", "#ParentTips", "#Mentorsy"],
},

"hero_2026_10b": {
    "date": "2026-10-27",
    "subject": "AI",
    "pillar": "Future Skills",
    "hook": "Should my child still learn maths if AI can do it?",
    "spoken": ("Parents keep asking whether maths still matters now that AI "
               "can do it. It matters more. Here is why."),
    "broll": [
        {"query": "laptop screen student working",
         "caption": "The skill now is telling when the answer is wrong."},
        {"query": "notebook calculations hand written",
         "caption": "That is subject knowledge, not technology."},
        {"query": "student thinking desk window",
         "caption": "You cannot audit an answer in a subject you do not know."},
        {"query": "books stacked quiet study",
         "caption": "The tool raises the value of knowing things."},
    ],
    "cta": "It does not lower it.",
    "caption": "Should my child still learn maths if AI can do it?\n\nYes, and more urgently than before.\n\nThe durable skill is catching a confident wrong answer - knowing where it came from, and knowing when to close the tab. That is not a technology skill. It is subject knowledge, held firmly enough to push back against a fluent sentence.\n\nYou cannot audit an answer in a subject you do not understand. The tool raises the value of knowing things. It does not lower it.",
    "hashtags": ["#AIForKids", "#FutureSkills", "#MathsTutoring", "#Mentorsy"],
},

# -- November -------------------------------------------------------------

"hero_2026_11a": {
    "date": "2026-11-10",
    "subject": "Mathematics",
    "pillar": "Curriculum Decoded",
    "hook": "The ceiling is set earlier than results day.",
    "spoken": ("The grade your child can get is decided long before the exam. "
               "Usually in Year 9, by a timetable."),
    "broll": [
        {"query": "school timetable noticeboard",
         "caption": "Set placement decides which tier they are entered for."},
        {"query": "exam paper blank desk",
         "caption": "The tier caps the grade available."},
        {"query": "empty school corridor",
         "caption": "That narrows what is open at A Level."},
        {"query": "student writing exam hall",
         "caption": "Most families find out on results day."},
    ],
    "cta": "Ask which tier. Ask in Year 9.",
    "caption": "The ceiling is set earlier than results day.\n\nSet placement in Year 9 decides which tier your child is entered for, and the tier caps the grade available. That quietly narrows what they can take at A Level, years before anyone mentions A Levels.\n\nMost families find out when the results arrive.\n\nAsk which tier your child is on track for. Ask in Year 9, not Year 11 - there is still time to change the answer.",
    "hashtags": ["#IGCSE", "#CambridgeCurriculum", "#ParentTips", "#Mentorsy"],
},

"hero_2026_11b": {
    "date": "2026-11-24",
    "subject": "Coding",
    "pillar": "Future Skills",
    "hook": "Nine finished tutorials is not learning to code.",
    "spoken": ("Copying a tutorial teaches typing. The learning happens when "
               "something breaks, and tutorials never break."),
    "broll": [
        {"query": "laptop code screen close up",
         "caption": "Ask what your child does in week three."},
        {"query": "hands keyboard typing desk",
         "caption": "When the code will not run."},
        {"query": "student frustrated laptop",
         "caption": "Getting stuck is the subject, not an interruption to it."},
        {"query": "notebook sketch planning",
         "caption": "Every developer spends most of the day with something broken."},
    ],
    "cta": "That answer is the whole course.",
    "caption": "Nine finished tutorials is not learning to code.\n\nCopying a tutorial line by line teaches typing. The learning happens when something breaks and a child has to work out why - and nothing in a finished tutorial ever breaks.\n\nAsk what happens in week three when the code will not run. Getting stuck is the subject, not an interruption to it, and a child who thinks being stuck means being bad at it quits around then.\n\nThat answer is the whole course.",
    "hashtags": ["#CodingForKids", "#STEM", "#FutureSkills", "#Mentorsy"],
},

}
