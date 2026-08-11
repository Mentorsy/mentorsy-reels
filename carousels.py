"""
Mentorsy - carousel upgrades

Six of the thirty feed posts get the swipe treatment. Not more, for two
reasons: a carousel only earns its slides when each point genuinely needs a
sentence of its own, and a feed of nothing but carousels asks the reader to
work every single time they scroll past.

Roughly one in five is the ratio that makes the swipe feel like an event.

Keyed by slug of the day's reel, because that is the stable identifier for a
day in the bank.
"""

CAROUSEL_POINTS = {

# day 1 - report card
"d01_report_number": [
    {"heading": "A percentage is an average of averages",
     "body": "62 percent could be strong algebra and collapsed geometry, or steady mediocrity across everything. The two need completely different responses, and the number cannot tell them apart."},
    {"heading": "'Could apply himself' means one specific thing",
     "body": "Ask which topic the teacher was picturing when they wrote it. Nine times out of ten there is one concrete lesson behind that sentence."},
    {"heading": "Effort grades measure compliance",
     "body": "A child who is quietly lost often scores well on effort. They are working hard on the wrong thing, which is the most expensive kind of hard work there is."},
    {"heading": "Ask for the question-level breakdown",
     "body": "Most schools hold it and rarely send it. It shows exactly which topics cost the marks, which is the only part of a report you can actually act on."},
],

# day 4 - Year 9
"d04_tier_ceiling": [
    {"heading": "Set placement in Year 9 shapes Year 12",
     "body": "The tier a child is entered for narrows what they can take at A Level. That decision is often made on one year of marks, quietly, by a timetable."},
    {"heading": "Foundation tier caps the grade",
     "body": "Many parents do not realise a ceiling exists until results day. Ask which tier your child is on track for, and ask in Year 9, not Year 11."},
    {"heading": "Moving up is possible but rare",
     "body": "Schools will move a child if the evidence is loud enough. That means closing gaps early enough for the evidence to have somewhere to appear."},
    {"heading": "The window is about eighteen months",
     "body": "From the start of Year 9 to the tier decision. Long enough to change the outcome, short enough that drifting through it costs you the option."},
],

# day 12 - IGCSE vs IB
"d12_igcse_or_ib": [
    {"heading": "Neither opens more doors on its own",
     "body": "Admissions read the grade and the depth, not the acronym. A strong IGCSE record beats a scraped IB one at every desk we have dealt with."},
    {"heading": "The real question is teaching depth",
     "body": "Ask how many periods a week the school gives to maths, and who teaches the top set. That predicts outcomes far better than the curriculum badge."},
    {"heading": "IB rewards breadth, IGCSE rewards precision",
     "body": "A child who likes closing a problem cleanly often thrives in IGCSE. One who enjoys connecting ideas across subjects tends to prefer IB."},
    {"heading": "Switching later costs more than parents expect",
     "body": "The two build sequence differently. A mid-stream move usually costs a term of catching up, so choose for the child you have, not the one you hope for."},
],

# day 14 - tutor questions
"d14_tutor_questions": [
    {"heading": "What will you do in the first session?",
     "body": "If the answer is 'start the syllabus', walk away. The first session should be diagnosis. Nobody can teach a gap they have not located."},
    {"heading": "How will I know it is working?",
     "body": "A good tutor names a measure before they start. 'More confident' is not a measure. 'She will close negative numbers in three weeks' is."},
    {"heading": "What happens when she gets stuck?",
     "body": "Listen for whether they explain again louder, or go backwards to find the missing step. Only one of those two things is teaching."},
    {"heading": "Who else have you taught at this level?",
     "body": "IGCSE and A Level are specific. General tutoring is not the same job, and the difference starts showing somewhere around week three."},
],

# day 22 - school tour
"d22_school_tour": [
    {"heading": "What happens when a student falls behind?",
     "body": "Listen for a system, not a sentiment. 'We keep an eye on them' is not a system. A named intervention with a timescale is."},
    {"heading": "How many dropped this subject last year?",
     "body": "Ask about A Level Maths specifically. A school that loses half its cohort between Year 11 and Year 12 has a teaching problem, not a student one."},
    {"heading": "Who teaches the bottom set?",
     "body": "A school that gives its strongest teacher to the students who are struggling believes ability can move. One that gives it to whoever is free has already decided otherwise."},
],

# day 29 - what a good session looks like
"d29_good_session": [
    {"heading": "The student talks more than the tutor",
     "body": "That single ratio separates teaching from lecturing, and it takes one question to check: ask your child who did most of the talking."},
    {"heading": "Something goes wrong on purpose",
     "body": "A student who has only ever seen worked examples has never practised the actual skill. The skill is recovering, and it needs something to recover from."},
    {"heading": "It ends with something they can do alone",
     "body": "Not something they watched, and not something they followed along with. Something they can now produce on a blank page with nobody in the room."},
    {"heading": "The next gap is already named",
     "body": "A tutor who knows what is coming next has a map. One who decides at the start of each session is working through a textbook, which you already own."},
],

# -- September batch ------------------------------------------------------

# day 33 - one language
"d33_one_language_deeply": [
    {"heading": "Syntax is the cheapest part",
     "body": "A reference page hands it over in thirty seconds. Six languages means six sets of punctuation and no more engineering than one."},
    {"heading": "What transfers is the thinking",
     "body": "Breaking a problem into parts, naming things clearly, testing an assumption. Those move between languages untouched, and they are the slow things to learn."},
    {"heading": "Finishing is the skill nobody teaches",
     "body": "A child with nine abandoned projects has practised starting. Getting one thing all the way to working teaches the last ten percent, which is where the real difficulty lives."},
    {"heading": "Ask what they built, not what they covered",
     "body": "Coverage is a list of topics. A build is evidence. If nothing runs at the end of a term, the term did not happen."},
],

# day 43 - A Level starts earlier
"d43_alevel_starts_earlier": [
    {"heading": "The first term assumes automatic algebra",
     "body": "Rearranging, factorising, surds and indices are treated as tools rather than topics. They are used in the first lesson and not taught again."},
    {"heading": "Slow and careful reads as cannot",
     "body": "At that pace a student who can do the algebra with effort is functionally a student who cannot, because the effort is needed elsewhere in the question."},
    {"heading": "This is why strong grades meet a hard October",
     "body": "The IGCSE measured whether they could get there. A Level measures whether they can get there without thinking about it. Those are different tests."},
    {"heading": "The summer between is the fix",
     "body": "Narrow, unglamorous fluency work on algebra they already understand. Not new content, just the same content until it stops costing attention."},
],

# day 47 - method marks
"d47_show_the_line": [
    {"heading": "Examiners mark a process",
     "body": "Method marks exist because the working is the evidence. A wrong final value with three correct visible steps can outscore a bare answer that happened to be right."},
    {"heading": "Mental arithmetic hides the evidence",
     "body": "Students who work in their heads produce tidy books and inexplicable marks. Nothing on the page shows the examiner what was understood."},
    {"heading": "Write the line before the confident one",
     "body": "Substitution before evaluation, rearrangement before solving. The step that feels too obvious to write is usually the one carrying the mark."},
    {"heading": "It costs about four seconds a question",
     "body": "Which makes it the cheapest grade improvement available, and the one most likely to be dismissed as unnecessary by the student who needs it most."},
],

# day 49 - speaking assessment
"d49_speaking_is_structure": [
    {"heading": "Structure beats charisma",
     "body": "Open with a position, give two reasons, close on the position. That shape sounds prepared even when the answer is invented on the spot."},
    {"heading": "The follow-up is the real test",
     "body": "Most students fold and agree with the examiner the moment they are challenged. Holding a position politely under pressure is a separate, trainable skill."},
    {"heading": "Volume and pause are physical",
     "body": "Both are trainable in a fortnight because both are mechanical. A pause used deliberately reads as authority; the same silence unplanned reads as panic."},
    {"heading": "None of this is personality",
     "body": "Every item here is a drill, which is why children who look naturally good at speaking are almost always children who have simply done it more often."},
],

# day 52 - club versus course
"d52_club_versus_course": [
    {"heading": "A club is exposure, and that is fine",
     "body": "Most children should meet programming through something enjoyable and low-stakes. The mistake is expecting exposure to produce progression."},
    {"heading": "Clubs are built to survive absence",
     "body": "A child who missed last week still has to enjoy this week, so nothing can depend on last week. That single constraint caps the difficulty forever."},
    {"heading": "A course has an order",
     "body": "There is a next thing, and a point at which the previous thing is assumed rather than repeated. That assumption is what progress actually looks like."},
    {"heading": "Ask what week eight assumes",
     "body": "If week eight assumes nothing from week one, you have bought eight enjoyable afternoons. Worth having, but do not confuse it with a curriculum."},
],

# day 57 - fractions
"d57_fractions_upstream": [
    {"heading": "Fractions arrive early and never leave",
     "body": "They get marked as done in Year 7 and then quietly underpin ratio, probability, rates of change and every algebraic fraction that follows."},
    {"heading": "The topic changes its name",
     "body": "Algebraic fractions are the same skill with letters in. A student who is shaky on one is shaky on the other, but only the second one gets noticed."},
    {"heading": "Scattered losses, single cause",
     "body": "A Year 11 dropping marks across several unrelated topics is often losing them all to one gap sitting four years upstream of the paper."},
    {"heading": "Nothing in the timetable will catch it",
     "body": "Fractions are not retaught after Year 8. Ask for three-quarters divided by two-fifths on paper, with the reasoning said out loud. Two minutes."},
],
}
