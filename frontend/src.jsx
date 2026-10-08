import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./style.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "";
const SUGGESTED_TOPICS = ["Machine learning", "Space exploration", "Personal finance", "The human brain"];

function FormattedExplanation({ children }) {
  return (
    <div className="prose">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{children || ""}</ReactMarkdown>
    </div>
  );
}

function LearningAgent() {
  const [topic, setTopic] = useState("");
  const [context, setContext] = useState("");
  const [session, setSession] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [readingProgress, setReadingProgress] = useState(0);
  const [copyStatus, setCopyStatus] = useState("");

  useEffect(() => {
    function updateReadingProgress() {
      const scrollableHeight =
        document.documentElement.scrollHeight - window.innerHeight;
      const progress =
        scrollableHeight <= 0 ? 100 : (window.scrollY / scrollableHeight) * 100;
      setReadingProgress(Math.min(100, Math.max(0, progress)));
    }

    updateReadingProgress();
    window.addEventListener("scroll", updateReadingProgress, { passive: true });
    window.addEventListener("resize", updateReadingProgress);
    return () => {
      window.removeEventListener("scroll", updateReadingProgress);
      window.removeEventListener("resize", updateReadingProgress);
    };
  }, [session]);

  async function send(path, body) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.detail || "The request failed. Please try again.");
    }
    return result;
  }

  async function startLearning(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setSession(null);
    setAnswers([]);
    try {
      const result = await send("/api/sessions", { topic, context });
      setSession(result);
      setAnswers(Array(result.questions.length).fill(""));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  async function submitQuiz(retry = false) {
    if (answers.some((answer) => !answer)) {
      setError("Please answer every question before submitting.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const route = retry
        ? `/api/sessions/${session.sessionId}/retry`
        : `/api/sessions/${session.sessionId}/answers`;
      const result = await send(route, { answers });
      setSession(result);
      setAnswers(Array(result.questions.length).fill(""));
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  function selectAnswer(questionIndex, option) {
    setAnswers((current) =>
      current.map((answer, index) => (index === questionIndex ? option : answer)),
    );
  }

  function startNewLesson() {
    setSession(null);
    setAnswers([]);
    setError("");
  }

  async function copyLesson() {
    const lessonText = `# ${session.topic}\n\n${session.explanation}`;
    try {
      await navigator.clipboard.writeText(lessonText);
      setCopyStatus("Copied!");
      setError("");
      window.setTimeout(() => setCopyStatus(""), 1800);
    } catch {
      setError("Could not copy the lesson. Check your browser clipboard permissions.");
    }
  }

  function downloadLesson() {
    const lessonText = `# ${session.topic}\n\n${session.explanation}`;
    const blob = new Blob([lessonText], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const filename = session.topic
      .trim()
      .replace(/[<>:"/\\|?*\u0000-\u001f]/g, "-")
      .replace(/\s+/g, "-")
      .slice(0, 80) || "learning-notes";
    link.href = url;
    link.download = `${filename}.md`;
    link.click();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  return (
    <main className="page-shell">
      {session && (
        <div
          className="reading-progress"
          role="progressbar"
          aria-label="Page reading progress"
          aria-valuemin="0"
          aria-valuemax="100"
          aria-valuenow={Math.round(readingProgress)}
          style={{ width: `${readingProgress}%` }}
        />
      )}
      <header className="topbar">
        <a className="brand" href="/" aria-label="Learning Agent home">
          <span className="brand-mark">L</span>
          <span>Learning Agent</span>
        </a>
        <div className="topbar-actions">
          <span className="topbar-note"><span className="status-dot" /> Your personal AI tutor</span>
          {session && <button className="text-button" onClick={startNewLesson}>＋ New lesson</button>}
        </div>
      </header>

      {!session ? (
        <section className="welcome-grid">
          <div className="hero">
            <div className="eyebrow"><span /> LEARN AT YOUR PACE</div>
            <h1>Big ideas,<br /><span>made simple.</span></h1>
            <p>Your AI tutor turns any topic into a clear lesson, then helps you check what you’ve learned. No pressure—just progress.</p>
            <div className="hero-points">
              <div><span className="point-icon">✦</span><span><strong>Learn your way</strong><small>Add your notes or start from scratch</small></span></div>
              <div><span className="point-icon">✓</span><span><strong>Build confidence</strong><small>Quick quizzes make progress visible</small></span></div>
              <div><span className="point-icon">↻</span><span><strong>Try again, differently</strong><small>Get a simpler explanation whenever needed</small></span></div>
            </div>
          </div>

          <div className="entry-column">
            <form className="topic-card" onSubmit={startLearning}>
              <div className="section-label">LET’S GET STARTED</div>
              <h2>What are you curious about?</h2>
              <p className="form-intro">Pick a topic and we’ll build a lesson just for you.</p>
              <label htmlFor="topic">YOUR TOPIC</label>
              <input
                id="topic"
                value={topic}
                onChange={(event) => setTopic(event.target.value)}
                placeholder="e.g. Machine learning"
                maxLength={300}
                required
              />
              <label htmlFor="context">YOUR NOTES <span className="optional">OPTIONAL</span></label>
              <textarea
                id="context"
                value={context}
                onChange={(event) => setContext(event.target.value)}
                placeholder="Paste notes or context you'd like the tutor to use..."
                rows={3}
                maxLength={20000}
              />
              <button className="primary-button start-button" disabled={loading}>
                {loading ? <><span className="spinner" /> Building your lesson...</> : <>Start learning <span aria-hidden="true">→</span></>}
              </button>
              {loading && <p className="loading-note">Your tutor is putting together a lesson and quiz.</p>}
              <div className="suggestions">
                <span>NEED AN IDEA?</span>
                <div>{SUGGESTED_TOPICS.map((suggestion) => (
                  <button className="suggestion-chip" type="button" key={suggestion} onClick={() => setTopic(suggestion)}>
                    {suggestion}
                  </button>
                ))}</div>
              </div>
            </form>
            {error && <div className="alert error-alert" role="alert">{error}</div>}
          </div>
        </section>
      ) : (
        <section className="session-page">
          <div className="session-heading">
            <div>
              <div className="eyebrow"><span /> YOUR LEARNING SESSION</div>
              <h1>{session.topic}</h1>
              <p>Take it one step at a time. You’re doing great.</p>
            </div>
            <div className="session-badge"><span>✦</span> PERSONALIZED LESSON</div>
          </div>
          <SessionProgress phase={session.phase} />
          {error && <div className="alert error-alert" role="alert">{error}</div>}
          <div className="lesson">
            <div className="lesson-main">
              <article className="explanation-card">
                <div className="lesson-toolbar">
                  <div>
                    <div className="section-label">YOUR LESSON</div>
                    <div className="reading-time">{estimateReadingTime(session.explanation)} min read</div>
                  </div>
                  <div className="lesson-actions">
                    <button type="button" className="lesson-action" onClick={copyLesson}>
                      {copyStatus || "Copy"}
                    </button>
                    <button type="button" className="lesson-action" onClick={downloadLesson}>
                      Download
                    </button>
                  </div>
                </div>
                <FormattedExplanation>{session.explanation}</FormattedExplanation>
              </article>

              {(session.phase === "retry" || session.phase === "complete") && session.answerFeedback && (
                <AnswerReview feedback={session.answerFeedback} />
              )}

              {session.phase === "retry" && (
                <>
                  <div className="score-card needs-practice">
                    <div className="score-number">{session.score?.toFixed(0)}<span>%</span></div>
                    <div><strong>Oh no! Your score is less than 70%, which is not up to the mark.</strong><p>Don’t worry, I’ll explain it again. Let’s make the tricky parts simpler, then give it another try.</p></div>
                  </div>
                  <article className="feynman-card">
                    <div className="section-label">A SIMPLER EXPLANATION</div>
                    <FormattedExplanation>{session.feynmanExplanation}</FormattedExplanation>
                  </article>
                </>
              )}

              {session.phase === "complete" && session.score !== null && (
                <div className={`score-card ${session.score >= 70 ? "passed" : "needs-practice"}`}>
                  <div className="score-number">{session.score.toFixed(0)}<span>%</span></div>
                  <div><strong>{session.score >= 70 ? "Great work—you've got it!" : "Thanks for giving it another try."}</strong><p>Your answers have been checked. Start a new topic when you’re ready.</p></div>
                </div>
              )}
            </div>
            <aside className="lesson-side">
              {session.relevanceScore !== null && (
                <div className="relevance-card">
                  <div className="section-label">CONTEXT MATCH</div>
                  <div className="relevance-value">{(session.relevanceScore * 100).toFixed(0)}<span>%</span></div>
                  <div className="progress-track"><div style={{ width: `${session.relevanceScore * 100}%` }} /></div>
                  <p>How closely your lesson matches your notes.</p>
                </div>
              )}
              {session.phase === "quiz" && (
                <Quiz
                  questions={session.questions}
                  answers={answers}
                  onSelect={selectAnswer}
                  onSubmit={() => submitQuiz(false)}
                  loading={loading}
                  title="Quick knowledge check"
                  buttonText="Check my answers"
                />
              )}
              {session.phase === "retry" && (
                <Quiz
                  questions={session.questions}
                  answers={answers}
                  onSelect={selectAnswer}
                  onSubmit={() => submitQuiz(true)}
                  loading={loading}
                  title="Try again"
                  buttonText="Submit retry"
                />
              )}
              {session.phase === "complete" && (
                <div className="next-step-card">
                  <div className="next-step-icon">✦</div>
                  <strong>Keep your curiosity going</strong>
                  <p>Choose another topic and keep building your knowledge.</p>
                  <button className="secondary-button" onClick={startNewLesson}>Explore a new topic <span>→</span></button>
                </div>
              )}
            </aside>
          </div>
        </section>
      )}
      <footer>Curiosity is a great place to start.</footer>
    </main>
  );
}

function estimateReadingTime(text = "") {
  const wordCount = text.trim().split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.ceil(wordCount / 200));
}

function SessionProgress({ phase }) {
  const steps = ["Choose a topic", "Explore the lesson", "Check understanding"];
  const activeStep = phase === "complete" ? 3 : 2;

  return (
    <nav className="session-progress" aria-label="Learning progress">
      {steps.map((step, index) => {
        const complete = index < activeStep;
        const active = index === activeStep;
        return (
          <div className={`progress-step ${complete ? "complete" : ""} ${active ? "active" : ""}`} key={step}>
            <span className="step-marker">{complete ? "✓" : `0${index + 1}`}</span>
            <span>{step}</span>
          </div>
        );
      })}
    </nav>
  );
}

function AnswerReview({ feedback }) {
  const [showAll, setShowAll] = useState(false);
  const missed = feedback.filter((item) => !item.correct);
  const shownAnswers = showAll || missed.length === 0 ? feedback : missed;

  return (
    <section className="answer-review" aria-live="polite">
      <div className="review-heading">
        <div>
          <div className="section-label">QUIZ REVIEW</div>
          <h2>{missed.length ? "Let’s learn from each answer" : "You got every answer right!"}</h2>
          <p>{missed.length ? `${missed.length} answer${missed.length === 1 ? "" : "s"} to review` : "Excellent understanding—keep it up."}</p>
        </div>
        {feedback.length > 0 && (
          <div className={`review-score ${missed.length ? "review-score-low" : ""}`}>
            {feedback.length - missed.length}<span>/{feedback.length}</span>
          </div>
        )}
      </div>
      {missed.length > 0 && (
        <button className="review-toggle" onClick={() => setShowAll((current) => !current)}>
          {showAll ? "Show only answers to review" : "Show all answers"}
          <span aria-hidden="true">{showAll ? "↑" : "↓"}</span>
        </button>
      )}
      <div className="review-list">
        {shownAnswers.map((item, index) => (
          <article className={`review-item ${item.correct ? "review-correct" : "review-incorrect"}`} key={`${item.question}-${index}`}>
            <div className="review-status">
              <span>{item.correct ? "✓" : "↻"}</span>
              {item.correct ? "Correct" : "Review this one"}
            </div>
            <h3>{item.question}</h3>
            {!item.correct && (
              <p className="review-answer">
                {item.selectedAnswer ? <>Your answer: <strong>{item.selectedAnswer}</strong><br /></> : null}
                Correct answer: <strong>{item.correctAnswer || "Not available"}</strong>
              </p>
            )}
            {item.explanation && <p className="review-explanation">{item.explanation}</p>}
          </article>
        ))}
      </div>
    </section>
  );
}

function Quiz({ questions, answers, onSelect, onSubmit, loading, title, buttonText }) {
  const answered = answers.filter(Boolean).length;
  const progress = questions.length ? (answered / questions.length) * 100 : 0;

  return (
    <section className="quiz-card">
      <div className="section-label">YOUR TURN</div>
      <h2>{title}</h2>
      <p className="quiz-intro">Choose the answer that feels right. You can change it any time.</p>
      <div className="quiz-progress">
        <div className="quiz-progress-label"><span>YOUR PROGRESS</span><strong>{answered} / {questions.length}</strong></div>
        <div className="progress-track"><div style={{ width: `${progress}%` }} /></div>
      </div>
      <div className="question-list">
        {questions.map((question, questionIndex) => (
          <fieldset className={`question ${answers[questionIndex] ? "answered" : ""}`} key={`${questionIndex}-${question.question}`}>
            <legend><span className="question-number">{String(questionIndex + 1).padStart(2, "0")}</span>{question.question}</legend>
            <div className="options">
              {question.options.map((option, optionIndex) => (
                <label className={`option ${answers[questionIndex] === option ? "selected" : ""}`} key={`${optionIndex}-${option}`}>
                  <input
                    type="radio"
                    name={`question-${questionIndex}`}
                    value={option}
                    checked={answers[questionIndex] === option}
                    onChange={() => onSelect(questionIndex, option)}
                  />
                  <span className="option-letter">{String.fromCharCode(65 + optionIndex)}</span>
                  <span>{option}</span>
                </label>
              ))}
            </div>
          </fieldset>
        ))}
      </div>
      <button className="primary-button quiz-submit" onClick={onSubmit} disabled={loading || answered !== questions.length}>
        {loading ? <><span className="spinner" /> Checking your answers...</> : <>{buttonText}<span aria-hidden="true">→</span></>}
      </button>
      {answered !== questions.length && <p className="quiz-hint">Answer all {questions.length} questions to continue.</p>}
    </section>
  );
}

createRoot(document.getElementById("root")).render(
  <React.StrictMode><LearningAgent /></React.StrictMode>,
);
