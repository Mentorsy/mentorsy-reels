"""
Mentorsy - hero reel scripts

One a month. Each has a spoken line for the presenter and a set of b-roll
beats that carry the argument in typography once the face has gone.

Writing rules specific to these:

  - the SPOKEN line is under 25 words. Ten seconds is shorter than it sounds,
    and a rushed delivery loses the calm that makes a face worth showing
  - the spoken line and the first b-roll caption must not repeat each other.
    The face opens the argument, the type continues it
  - no first person singular, same as everywhere else
"""

HEROES = {

"hero_2026_09": {
    "date": "2026-09-15",
    "subject": "Mathematics",
    "pillar": "Curriculum Decoded",
    # Spoken by the presenter. Paste this into the Gemini prompt.
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

"hero_2026_10": {
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
         "caption": "Nobody is fluent the first time they speak in front of people."},
        {"query": "school corridor students",
         "caption": "They are fluent the ninth time."},
        {"query": "teenager presenting classroom",
         "caption": "The gap is not courage. It is practice nobody scheduled."},
    ],
    "cta": "Start earlier than feels necessary.",
    "caption": "Your child is not shy. They are unrehearsed.\n\nShyness sounds like a personality, which makes it sound permanent. Unrehearsed is a state, and states change with repetition.\n\nNobody is fluent the first time they say a sentence out loud in front of people. They are fluent the ninth time. The difference between a child who freezes and a child who presents is usually eight rehearsals nobody scheduled.\n\nSpeaking also improves faster than almost anything else on a timetable. Four weeks of deliberate work changes how a child sounds.",
    "hashtags": ["#PublicSpeaking", "#ChildConfidence", "#ParentTips", "#Mentorsy"],
},

}
