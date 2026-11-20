// Prepared examples for the GitHub Pages sample. No API or model calls are made.
const lessons = {
  "machine learning": {
    explanation: `## What is machine learning?

Machine learning is a way to build programs that learn patterns from examples. Instead of writing a rule for every situation, we give a model data and let it adjust its internal parameters.

### A simple example

Imagine showing a program many emails labeled **spam** or **not spam**. It may learn that certain words and sender patterns are common in spam. When a new email arrives, it uses those learned patterns to predict a label.

The examples used for learning are **training data**. Separate **test data** helps check whether the model works on examples it has not seen. A model that memorizes training examples but performs poorly on new ones is **overfitting**.

Machine learning is useful for predictions, recommendations, and classification, but its results depend on the quality of the data and should be checked by people.`,
    simpler: `## Learn it step by step

Imagine teaching a friend to recognize apples. You show them many pictures labeled **apple** or **not an apple**. They start noticing useful clues, such as shape, color, and texture. A machine learning **model** does something similar: it finds patterns in examples and uses them to make a prediction about a new example.

1. **Practice with training data.** These are examples the model learns from. For an email filter, the examples are emails labeled **spam** or **not spam**. The model may notice that some words or sender patterns occur more often in spam.
2. **Try unseen test data.** Set aside different emails that the model did not use for practice. Ask it to classify them, then compare its predictions with the correct labels. This checks whether it learned a pattern that works beyond its practice set.
3. **Watch for overfitting.** Suppose the model remembers the exact training emails. It may score well on those emails but fail when a new spam email uses different wording. That is **overfitting**: memorizing details instead of learning a useful general pattern.

### Put the pieces together

A spam filter is a **classification** example because it chooses between labels. It learns from labeled training emails, predicts a label for a new email, and is checked using separate test emails. A test score tells us how well it handled those examples; it does not guarantee that every future prediction will be right.

**Remember:** training data is for learning; test data is for checking; overfitting means the model does well on practice examples but struggles with new ones.`,
    questions: [
      ["What does a machine learning model learn from?", ["Examples in data", "Only handwritten rules", "A web browser", "Random guesses"], 0, "Models adjust based on patterns in training data."],
      ["What is training data used for?", ["Checking the final score only", "Helping the model learn patterns", "Displaying the user interface", "Storing passwords"], 1, "Training data provides examples from which the model learns."],
      ["Why use separate test data?", ["To make the model larger", "To avoid using labels", "To check performance on unseen examples", "To replace training data"], 2, "Test data checks whether learned patterns generalize."],
      ["What is overfitting?", ["Learning a useful general pattern", "Memorizing training examples without generalizing", "Having too little computer memory", "Using more than one model"], 1, "An overfit model performs well on training data but poorly on new data."],
      ["Which task is a common use of machine learning?", ["Predicting whether an email is spam", "Replacing every human decision", "Guaranteeing a correct answer", "Writing a rule for every possible email"], 0, "Classifying emails is a common machine learning task."],
    ],
  },
  "space exploration": {
    explanation: `## Exploring beyond Earth

Space exploration uses spacecraft, telescopes, and scientific instruments to study places beyond Earth. A **satellite** orbits a planet or moon. A **probe** travels through space to collect information, while a **rover** can move across a surface.

### Why send robots first?

Robotic missions can reach distant or hazardous places without putting people at risk. They send measurements and images back to Earth by radio. Because signals travel at the speed of light, messages to distant spacecraft can take minutes or hours.

Scientists plan missions around a question, choose instruments to collect evidence, and compare the results with their predictions. Space missions have taught us about planetary atmospheres, geology, and the history of our solar system.`,
    simpler: `## Meet the remote explorers

Imagine you want to study a place that is too far away or dangerous to visit yourself. You send a robot with cameras and measuring tools. Space missions use different kinds of explorers for different jobs.

1. A **satellite** travels in an **orbit** around a larger body, such as a planet or moon. From above, it can repeatedly observe the same world.
2. A **probe** travels through space to gather information. It may fly past, orbit, or land near the place it studies.
3. A **rover** lands and moves across a surface. It can examine different spots instead of staying in one place.

### How do we hear from them?

The spacecraft sends its pictures and measurements to Earth using **radio signals**. Radio waves travel at the speed of light, but space is enormous. A message from a distant probe must cross that distance, so it can arrive minutes or even hours after it was sent. A reply takes time to travel back too.

Robotic missions let scientists investigate places that would be hazardous for astronauts. The robot collects evidence, sends it home, and scientists use that evidence to answer questions about the place.

**Remember:** satellite = orbits; probe = travels to investigate; rover = moves on a surface. Radio carries their data home, and distance causes the delay.`,
    questions: [
      ["What does a satellite do?", ["Orbits a larger body", "Always lands on a planet", "Only travels inside Earth", "Creates stars"], 0, "A satellite follows an orbit around a planet, moon, or other body."],
      ["Why are robotic missions useful?", ["They need no instruments", "They avoid risk to astronauts in hazardous places", "They move faster than light", "They answer every question"], 1, "Robots can explore dangerous and distant places without a human crew."],
      ["How does a distant spacecraft send data to Earth?", ["By radio signals", "By paper mail", "By sound through space", "By ocean cable"], 0, "Spacecraft commonly transmit measurements and images by radio."],
      ["Why can communication with a distant probe be delayed?", ["Signals must travel a long distance", "The probe has no clock", "Earth stops rotating", "The data becomes heavier"], 0, "Even light-speed radio signals take time to cross large distances."],
      ["What is a rover designed to do?", ["Move across a surface", "Orbit the Sun only", "Carry radio signals without instruments", "Turn into a telescope"], 0, "A rover moves around on a planet or moon to investigate its surface."],
    ],
  },
  "personal finance": {
    explanation: `## A starting point for personal finance

Personal finance is how you plan and manage money for everyday needs and future goals. A **budget** compares income with spending so you can see where money goes. It can help you make room for savings and avoid spending more than you earn.

An **emergency fund** is money set aside for unexpected expenses. Borrowing can help with large purchases, but interest makes repayment cost more than the amount borrowed. When saving or investing, consider your time horizon and the chance of losing money.

There is no single plan that fits everyone. Start by understanding your own income, expenses, debts, and goals.`,
    simpler: `## Follow the money

Picture your money as water in a bucket. **Income** adds water; **expenses** take it out. A **budget** is a written view of both: how much comes in and where it goes. It helps you see whether anything is left for your goals.

For example, if you receive 100 units and spend 80, you have 20 units to plan for. If you spend 110, you are using 10 more units than came in. Looking at the amounts makes it easier to decide what to change; a budget does not create extra income by itself.

1. **Plan for surprises.** An **emergency fund** is money kept aside for unexpected costs, such as a repair. It is a buffer, not a promise that every emergency will be covered.
2. **Understand borrowing.** If you borrow 100 units, you usually repay the 100 **plus interest**. Interest is the cost of using borrowed money, so the total repayment can be larger than the amount you received.
3. **Fit the plan to your life.** Your income, expenses, debts, and goals determine what is practical for you. Another person's exact budget may not fit your circumstances.

**Remember:** a budget compares income and spending; an emergency fund helps with surprise expenses; interest adds to the cost of a loan.`,
    questions: [
      ["What does a budget compare?", ["Income and spending", "Only investments", "Only taxes", "Prices in two countries"], 0, "A budget tracks money coming in and going out."],
      ["What is an emergency fund for?", ["Unexpected expenses", "Guaranteed investment profits", "Daily shopping only", "Paying interest to a bank"], 0, "An emergency fund provides a buffer for unplanned costs."],
      ["What is interest on a loan?", ["An extra cost of borrowing", "A refund on every purchase", "The same as income", "A guaranteed discount"], 0, "Interest is the cost charged for borrowing money."],
      ["Why can a budget help with saving?", ["It shows where money is going", "It creates income automatically", "It removes every expense", "It guarantees investment returns"], 0, "Knowing your spending helps you plan how much to set aside."],
      ["What should a personal plan reflect?", ["Your own goals and circumstances", "A stranger's exact spending", "Only last month's prices", "A promise of risk-free returns"], 0, "Income, expenses, debts, goals, and risk tolerance differ by person."],
    ],
  },
  "the human brain": {
    explanation: `## The brain as a communication network

The human brain helps us sense the world, move, remember, and make decisions. It contains billions of **neurons**, cells that pass signals to other cells. Neurons communicate across tiny gaps called **synapses**.

Different areas contribute to different tasks. The **cerebellum** helps coordinate movement and balance. The **brainstem** supports basic functions such as breathing and heart rate. Many complex abilities involve several areas working together.

Learning can strengthen or change connections between neurons. Sleep, practice, and attention all affect how well we remember new information.`,
    simpler: `## A network of messengers

Imagine a huge team passing messages so your body can respond to the world. The brain's messengers are cells called **neurons**. A neuron receives signals and passes signals onward. Neurons communicate at meeting points called **synapses**; a tiny gap separates the cells there.

Different parts of the brain help with different jobs, and many jobs involve several parts working together:

1. The **cerebellum** helps coordinate movement and balance. Think of adjusting your steps when you walk over uneven ground.
2. The **brainstem** supports essential functions such as breathing and heart rate, even while you sleep.

### What happens when you practice?

When you repeat a skill, such as playing a short tune, the brain's network can change. Connections between neurons can become stronger or work differently as you learn. Practice can help, though it does not guarantee perfect memory or instant mastery.

Here is the chain to remember: **neurons** are signaling cells; **synapses** are places where neurons communicate; brain areas contribute to tasks such as balance and breathing; learning can change connections in the network.`,
    questions: [
      ["What is a neuron?", ["A cell that passes signals", "A bone in the skull", "A type of blood vessel", "A muscle"], 0, "Neurons are cells that send and receive information."],
      ["What is a synapse?", ["A gap where neurons communicate", "A part of the stomach", "A kind of telescope", "A layer of skin"], 0, "Neurons communicate across tiny gaps called synapses."],
      ["Which area helps coordinate movement and balance?", ["Cerebellum", "Liver", "Retina", "Lung"], 0, "The cerebellum contributes to coordination and balance."],
      ["Which function does the brainstem support?", ["Breathing", "Digesting food in the stomach", "Filtering blood", "Growing hair"], 0, "The brainstem helps regulate basic functions including breathing."],
      ["What can practice do during learning?", ["Change connections between neurons", "Stop all brain activity", "Remove the need for sleep", "Guarantee perfect memory"], 0, "Learning and practice can alter the strength of neural connections."],
    ],
  },
};

export const demoTopics = Object.keys(lessons);

export function createDemoSession(topic) {
  const lesson = lessons[topic.trim().toLowerCase()];
  if (!lesson) {
    throw new Error("This sample includes four topics. Choose one of the suggestions below.");
  }

  return {
    sessionId: "sample",
    phase: "quiz",
    topic: topic.trim(),
    relevanceScore: null,
    explanation: lesson.explanation,
    questions: lesson.questions.map(([question, options]) => ({ question, options })),
    score: null,
    answerFeedback: null,
    feynmanExplanation: null,
  };
}

export function scoreDemoSession(session, answers) {
  const lesson = lessons[session.topic.trim().toLowerCase()];
  const answerFeedback = lesson.questions.map(([question, options, correctIndex, explanation], index) => ({
    question,
    selectedAnswer: answers[index],
    correctAnswer: options[correctIndex],
    correct: answers[index] === options[correctIndex],
    explanation,
  }));
  const score = (answerFeedback.filter(({ correct }) => correct).length / answerFeedback.length) * 100;

  return {
    ...session,
    phase: score >= 70 ? "complete" : "retry",
    score,
    answerFeedback,
    feynmanExplanation: score >= 70 ? null : lesson.simpler,
  };
}
