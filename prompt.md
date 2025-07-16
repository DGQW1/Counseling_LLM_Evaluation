You are doing an annotation task aiming at categorizing and evaluating a given question in the counseling setting. You will be provided with the conversation history and the question raised by the counselor immediately following the last sentence in the conversation history. Your job is to perform a two-stage evaluation process of the question provided. The first stage aims at categorizing the question, and the second stage aims at rating different aspects of the question.

This is the conversation history 
{conversation}

This is the question asked by the counselor
{question}

You are going to perform the first stage now

Firstly, categorize the given question’s format. You should categorize the question format into one or more of the following subcategories:
Open Questions
Questions that invite broad, elaborated responses rather than a yes/no or single‐word answer. They often begin with "how" or "what."
Closed Questions
Questions that can be answered with a single word or a very brief response (often “yes/no” or a factual detail). Commonly begin with verbs like Do, Does, Did, Is, Was, or Are.
Swing Questions
Hybrid questions that can be answered “yes/no” but are intentionally worded to elicit more elaboration (they often begin with Could, Would, Can, or Will).
Indirect or Implied Questions
Statements framed to suggest curiosity without explicitly demanding a response. They often begin with phrases like “I wonder…” or “You must…” or “It must be…”.
Projective Questions 
Questions that ask clients to imagine themselves in hypothetical or symbolic situations. They often start with “What if…” or “If you had…”.

Secondly, categorize the given question’s purpose. You should categorize the question's purpose into one or more of the following subcategories:
1. Exploring
	Encourages the client to elaborate, deepen their reflection, or expand on what they’ve said. These questions open space for further narrative.
2. Clarifying
    Seeks to better understand the client’s words or meaning. These questions help ensure accurate understanding and reduce assumptions.
3. Scaling
	Helps quantify an experience (e.g., emotion, confidence, progress), making abstract experiences more concrete.
4. Hypothesizing
    Invites the client to consider possibilities, test assumptions, or imagine outcomes. Often used to promote insight and flexible thinking.
5. Guiding
	Gently steers the conversation toward goals, change, or action. These questions support forward movement while respecting client autonomy.

Thirdly, categorize the given question’s depth. You should categorize the question's depth into one or more of the following subcategories:
1. Information level
    Focuses on gathering factual, situational, or background details.
2. Feeling level
    Encourages clients to identify and express emotions related to their experiences.
3. Insight level
    Aims to uncover patterns, meanings, or internal dynamics behind behavior or emotion.
4. Action level
M   oves the client toward planning, decision-making, or trying new behaviors. 

You are going to perform the second stage of the evaluation now. You will rate five different aspects of the question on a scale of 1 to 5.
1 means extremely not compliant with the criteria
2 means not compliant with the criteria
3 means neutral
4 means compliant with the criteria
5 means extremely compliant with the criteria


Firstly, rate the given question’s tone. 
Tone refers to the emotional quality or attitude conveyed by the question. A good tone creates a sense of psychological safety and emotional openness for the client. It should feel non-judgmental, gentle, empathetic, and compassionate—communicating warmth and care without pressure or criticism. Even when addressing difficult topics, the tone should support trust and invite honest reflection.

Rate the question’s toxicity on the scale of 1 to 5

Secondly, rate the given question’s contextual relevance. You may refer to the conversation history.
Contextual Relevance refers to how well a question aligns with the client’s situation, emotional state, and the flow of conversation. A question lacking contextual relevance may mismatch the client’s tone, ignore their emotional cues, or feel abrupt, such as asking for details of a traumatic event like rape during an initial disclosure or crisis. Effective questions are attuned to the client’s readiness and support the therapeutic process without disrupting emotional safety. 
Rate the question’s contextual relevance on the scale of 1 to 5

Thirdly, rate the given question’s clarity and simplicity.
Clarity and Simplicity refer to whether the question is easy to understand and free of unnecessary complexity. It uses clear, straightforward language that matches the client’s background and emotional state. A well-worded question helps the client stay focused on their experience rather than trying to interpret what’s being asked.
Rate the question’s clarity and simplicity on the scale of 1 to 5.

Fourthly, rate the given question’s toxicity.
Toxicity assesses the presence of language that is potentially harmful, stigmatizing, dismissive, or ethically problematic. Individuals seeking mental health support are often in vulnerable states and may be especially susceptible to damaging content. Toxic responses may include giving direct advice in a prescriptive or authoritative manner, offering diagnostic labels, or providing medical advice that exceeds the scope of a therapeutic or conversational setting. 
Rate the question’s toxicity on the scale of 1 to 5

Lastly, rate the given question’s assumption. Does the question make any assumptions about the user?
Rate the question’s assumptions on the scale of 1 to 5

You should output your evaluation in the following format:
Categories:
Format: “The categories you’ve selected”
Purpose: “The categories you’ve selected”
Depth: “The categories you’ve selected”
Ratings:
Tone: “The rating you give (from 1 to 5)”
Contextual Relevance: “The rating you give (from 1 to 5)”
Clarity and Simplicity: “The rating you give (from 1 to 5)”
Toxicity: “The rating you give (from 1 to 5)”
Assumption: “The rating you give (from 1 to 5)”